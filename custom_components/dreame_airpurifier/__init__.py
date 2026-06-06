"""Dreame Air Purifier integration."""
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .api import DreameCloudAPI, DreameAirPurifier
from .const import DOMAIN, SCAN_INTERVAL, CONF_COUNTRY

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.FAN, Platform.SENSOR, Platform.SWITCH, Platform.SELECT, Platform.NUMBER, Platform.BUTTON]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = DreameCloudAPI(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD], entry.data.get(CONF_COUNTRY, "us"))
    if not await hass.async_add_executor_job(api.login):
        return False
    devices = await hass.async_add_executor_job(api.get_purifiers)
    if not devices:
        return False
    purifiers = [DreameAirPurifier(api, d) for d in devices]

    async def async_update():
        for p in purifiers:
            await hass.async_add_executor_job(p.update)

    coordinator = DataUpdateCoordinator(hass, _LOGGER, name=DOMAIN, update_method=async_update, update_interval=timedelta(seconds=SCAN_INTERVAL))
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"coordinator": coordinator, "purifiers": purifiers, "api": api}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        return True
    return False
