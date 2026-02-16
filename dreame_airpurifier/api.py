"""Dreame Air Purifier Cloud API Client."""
import hashlib
import logging
import requests
import time

_LOGGER = logging.getLogger(__name__)

DREAME_SALT = "RAylYC%fmSKp7%Tq"
DREAME_USER_AGENT = "Dreame_Smarthome/2.1.9 (iPhone; iOS 18.4.1; Scale/3.00)"
DREAME_AUTH_BASIC = "Basic ZHJlYW1lX2FwcHYxOkFQXmR2QHpAU1FZVnhOODg="
DREAME_TENANT_ID = "000000"
DREAME_RLC = "1c80b3787b2266776bcdc481f37d8fa42ba10a30af81a6df-1"

# === MiOT Property Map for dreame.airp.u2507 (Dreame AP10) ===
# VERIFIED by live testing 2025-02-15

# siid 2: Air Purifier Control
PROP_POWER = {"siid": 2, "piid": 1}         # int: 1=on, 2=standby/off
PROP_MODE = {"siid": 2, "piid": 3}          # int: 0=Auto, 2=Sleep, 3=Custom, 4=Pet
PROP_FAN_SPEED = {"siid": 2, "piid": 4}     # int: 1-5 fan speed level
PROP_FAN_PCT = {"siid": 2, "piid": 5}       # int: percentage (read-only)
PROP_IONIZER = {"siid": 2, "piid": 6}       # int: -1=auto, 0=off, 1=on

# siid 3: Environment Sensors
PROP_AQ_LEVEL = {"siid": 3, "piid": 4}
PROP_PM25 = {"siid": 3, "piid": 5}

# siid 4: Filter
PROP_FILTER_LIFE = {"siid": 4, "piid": 1}
PROP_FILTER_DAYS = {"siid": 4, "piid": 2}
PROP_FILTER_USED = {"siid": 4, "piid": 3}

# siid 6: Device Settings
PROP_LED = {"siid": 6, "piid": 5}
PROP_BUZZER = {"siid": 6, "piid": 6}
PROP_CHILD_LOCK = {"siid": 6, "piid": 7}
PROP_LIGHT_MODE = {"siid": 6, "piid": 8}

# Poll batches (small to avoid timeout)
POLL_BATCHES = [
    [PROP_POWER, PROP_MODE, PROP_FAN_SPEED, PROP_FAN_PCT, PROP_IONIZER],
    [PROP_AQ_LEVEL, PROP_PM25],
    [PROP_FILTER_LIFE, PROP_FILTER_DAYS, PROP_FILTER_USED],
    [PROP_LED, PROP_BUZZER, PROP_CHILD_LOCK, PROP_LIGHT_MODE],
]

# Mode mapping (VERIFIED)
MODE_AUTO = 0
MODE_SLEEP = 2
MODE_CUSTOM = 3
MODE_PET = 4

MODE_NAMES = {MODE_AUTO: "Auto", MODE_SLEEP: "Sleep", MODE_CUSTOM: "Custom", MODE_PET: "Pet"}
MODE_NAME_TO_VALUE = {v: k for k, v in MODE_NAMES.items()}

# Power: MUST use toggle action (set_properties times out on siid 2 piid 1)
ACTION_TOGGLE_POWER = {"siid": 2, "aiid": 3}


class DreameCloudAPI:
    """Client for the Dreame Cloud API."""

    def __init__(self, username: str, password: str, country: str = "us"):
        self._username = username
        self._password = password
        self._country = country
        self._session = requests.Session()
        self._access_token = None
        self._refresh_token = None
        self._uid = None
        self._tenant_id = DREAME_TENANT_ID
        self._token_expire = None

    @property
    def api_url(self) -> str:
        return f"https://{self._country}.iot.dreame.tech:13267"

    @property
    def logged_in(self) -> bool:
        return self._access_token is not None

    def login(self) -> bool:
        url = f"{self.api_url}/dreame-auth/oauth/token"
        pw_hash = hashlib.md5((self._password + DREAME_SALT).encode("utf-8")).hexdigest()
        data = f"platform=IOS&scope=all&grant_type=password&username={self._username}&password={pw_hash}&type=account"
        headers = {
            "User-Agent": DREAME_USER_AGENT, "Authorization": DREAME_AUTH_BASIC,
            "Tenant-Id": DREAME_TENANT_ID, "Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*",
        }
        if self._country == "cn":
            headers["Dreame-Rlc"] = DREAME_RLC
        try:
            response = self._session.post(url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if "access_token" in result:
                    self._access_token = result["access_token"]
                    self._refresh_token = result.get("refresh_token")
                    self._uid = result.get("uid")
                    self._tenant_id = result.get("tenant_id", DREAME_TENANT_ID)
                    self._token_expire = time.time() + result.get("expires_in", 3600) - 120
                    return True
                _LOGGER.error("Login failed: %s", result)
            else:
                _LOGGER.error("Login failed (HTTP %s): %s", response.status_code, response.text)
        except Exception as ex:
            _LOGGER.error("Login error: %s", ex)
        return False

    def _refresh_login(self) -> bool:
        if self._refresh_token and self._token_expire and time.time() > self._token_expire:
            url = f"{self.api_url}/dreame-auth/oauth/token"
            data = f"platform=IOS&scope=all&grant_type=refresh_token&refresh_token={self._refresh_token}"
            headers = {"User-Agent": DREAME_USER_AGENT, "Authorization": DREAME_AUTH_BASIC,
                       "Tenant-Id": self._tenant_id, "Content-Type": "application/x-www-form-urlencoded"}
            try:
                r = self._session.post(url, headers=headers, data=data, timeout=10)
                if r.status_code == 200:
                    result = r.json()
                    if "access_token" in result:
                        self._access_token = result["access_token"]
                        self._refresh_token = result.get("refresh_token", self._refresh_token)
                        self._token_expire = time.time() + result.get("expires_in", 3600) - 120
                        return True
            except Exception as ex:
                _LOGGER.warning("Token refresh failed: %s", ex)
            return self.login()
        return True

    def _auth_headers(self) -> dict:
        return {"User-Agent": DREAME_USER_AGENT, "Authorization": DREAME_AUTH_BASIC,
                "Tenant-Id": self._tenant_id, "Dreame-Auth": self._access_token,
                "Content-Type": "application/json", "Accept": "*/*"}

    def get_devices(self) -> list | None:
        if not self._refresh_login():
            return None
        url = f"{self.api_url}/dreame-user-iot/iotuserbind/device/listV2"
        try:
            r = self._session.post(url, headers=self._auth_headers(), json={}, timeout=10)
            if r.status_code == 200:
                result = r.json()
                if result.get("code") == 0 and "data" in result:
                    return result["data"]["page"]["records"]
        except Exception as ex:
            _LOGGER.error("Failed to get devices: %s", ex)
        return None

    def get_purifiers(self) -> list:
        devices = self.get_devices()
        if not devices:
            return []
        return [d for d in devices if ".airp." in d.get("model", "")]

    def send_command(self, did: str, method: str, params, host: str = None):
        if not self._refresh_login():
            return None
        host_prefix = f"-{host.split('.')[0]}" if host else ""
        url = f"{self.api_url}/dreame-iot-com{host_prefix}/device/sendCommand"
        payload = {"did": str(did), "id": 1, "data": {"did": str(did), "id": 1, "method": method, "params": params}}
        try:
            r = self._session.post(url, headers=self._auth_headers(), json=payload, timeout=10)
            if r.status_code == 200:
                result = r.json()
                if result.get("code") == 0:
                    if result.get("data") and "result" in result["data"]:
                        return result["data"]["result"]
                    if result.get("success"):
                        return {"code": 0}
            elif r.status_code == 401:
                if self.login():
                    return self.send_command(did, method, params, host)
        except Exception as ex:
            _LOGGER.error("Command failed: %s", ex)
        return None

    def get_properties(self, did: str, properties: list, host: str = None) -> dict:
        params = [{"did": str(did), "siid": p["siid"], "piid": p["piid"]} for p in properties]
        result = self.send_command(did, "get_properties", params, host)
        values = {}
        if result and isinstance(result, list):
            for prop in result:
                if prop.get("code", -1) == 0:
                    values[(prop["siid"], prop["piid"])] = prop.get("value")
        return values

    def set_property(self, did: str, siid: int, piid: int, value, host: str = None) -> bool:
        result = self.send_command(did, "set_properties", [{"did": str(did), "siid": siid, "piid": piid, "value": value}], host)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0].get("code", -1) == 0
        return False

    def call_action(self, did: str, siid: int, aiid: int, params: list = None, host: str = None) -> bool:
        result = self.send_command(did, "action", {"did": str(did), "siid": siid, "aiid": aiid, "in": params or []}, host)
        if result:
            return result.get("code", -1) == 0 if isinstance(result, dict) else True
        return False


class DreameAirPurifier:
    """Represents a single Dreame Air Purifier device."""

    def __init__(self, api: DreameCloudAPI, device_info: dict):
        self._api = api
        self._did = str(device_info["did"])
        self._host = device_info.get("bindDomain")
        self._model = device_info.get("model", "unknown")
        self._mac = device_info.get("mac", "")
        self._name = device_info.get("customName") or device_info.get("deviceInfo", {}).get("displayName", "Dreame Air Purifier")
        self._power = False
        self._mode = MODE_AUTO
        self._fan_speed = 0
        self._fan_pct = 0
        self._ionizer = False
        self._pm25 = 0
        self._aq_level = 0
        self._filter_life = 100
        self._filter_days = 365
        self._filter_used = 0
        self._led = False
        self._buzzer = False
        self._child_lock = False
        self._light_mode = 0
        self._available = True

    @property
    def unique_id(self): return self._mac.replace(":", "").lower()
    @property
    def name(self): return self._name
    @property
    def model(self): return self._model
    @property
    def device_id(self): return self._did
    @property
    def mac(self): return self._mac
    @property
    def available(self): return self._available
    @property
    def is_on(self):
        """Device is 'on' unless in sleep mode at speed 1 (our soft-off state)."""
        if not self._power:
            return False
        # Sleep mode + speed 1 = our "off" state
        if self._mode == MODE_SLEEP and self._fan_speed <= 1:
            return False
        return True
    @property
    def mode(self): return MODE_NAMES.get(self._mode, f"Unknown ({self._mode})")
    @property
    def mode_value(self): return self._mode
    @property
    def fan_speed(self): return self._fan_speed
    @property
    def fan_speed_percent(self): return max(0, self._fan_speed * 20) if self._fan_speed > 0 else 0
    @property
    def ionizer(self): return self._ionizer
    @property
    def pm25(self): return self._pm25
    @property
    def air_quality_level(self): return self._aq_level
    @property
    def filter_life(self): return self._filter_life
    @property
    def filter_days_total(self): return self._filter_days
    @property
    def filter_hours_used(self): return self._filter_used
    @property
    def led(self): return self._led
    @property
    def buzzer(self): return self._buzzer
    @property
    def child_lock(self): return self._child_lock

    def update(self) -> bool:
        all_values = {}
        for batch in POLL_BATCHES:
            values = self._api.get_properties(self._did, batch, self._host)
            if values:
                all_values.update(values)
        if not all_values:
            self._available = False
            return False
        self._available = True
        self._power = all_values.get((2, 1), 0) == 1
        self._mode = all_values.get((2, 3), 0)
        self._fan_speed = all_values.get((2, 4), 0)
        self._fan_pct = all_values.get((2, 5), 0)
        ionizer_val = all_values.get((2, 6), 0)
        self._ionizer = ionizer_val == 1
        self._aq_level = all_values.get((3, 4), 0)
        self._pm25 = all_values.get((3, 5), 0)
        self._filter_life = all_values.get((4, 1), 0)
        self._filter_days = all_values.get((4, 2), 365)
        self._filter_used = all_values.get((4, 3), 0)
        self._led = bool(all_values.get((6, 5), 0))
        self._buzzer = bool(all_values.get((6, 6), 0))
        self._child_lock = bool(all_values.get((6, 7), 0))
        self._light_mode = all_values.get((6, 8), 0)
        return True

    def toggle_power(self) -> bool:
        return self._api.call_action(self._did, ACTION_TOGGLE_POWER["siid"], ACTION_TOGGLE_POWER["aiid"], host=self._host)

    def turn_on(self) -> bool:
        """Turn on: restore to Auto mode (or previous mode)."""
        # If in standby (power=2), toggle won't work. If in sleep "off", just set mode.
        if self._power:
            # Device is on but in "sleep off" state - switch to Auto
            return self.set_mode(MODE_AUTO)
        else:
            # Try toggle first, then set Auto
            self.toggle_power()
            return self.set_mode(MODE_AUTO)

    def turn_off(self) -> bool:
        """Turn off: switch to Sleep mode speed 1 (keeps device cloud-connected)."""
        # Don't actually power off - device can't be woken remotely
        self.set_mode(MODE_SLEEP)
        return self.set_fan_speed(1)

    def set_mode(self, mode: int) -> bool:
        return self._api.set_property(self._did, 2, 3, mode, self._host)

    def set_fan_speed(self, speed: int) -> bool:
        return self._api.set_property(self._did, 2, 4, max(1, min(5, speed)), self._host)

    def set_fan_speed_percent(self, percent: int) -> bool:
        if percent <= 0:
            return self.turn_off()
        return self.set_fan_speed(max(1, min(5, round(percent / 20))))

    def set_ionizer(self, enabled: bool) -> bool:
        return self._api.set_property(self._did, 2, 6, 1 if enabled else 0, self._host)

    def set_led(self, enabled: bool) -> bool:
        return self._api.set_property(self._did, 6, 5, 1 if enabled else 0, self._host)

    def set_buzzer(self, enabled: bool) -> bool:
        return self._api.set_property(self._did, 6, 6, 1 if enabled else 0, self._host)

    def set_child_lock(self, enabled: bool) -> bool:
        return self._api.set_property(self._did, 6, 7, 1 if enabled else 0, self._host)

    def reset_filter(self) -> bool:
        return self._api.call_action(self._did, 4, 1, host=self._host)
