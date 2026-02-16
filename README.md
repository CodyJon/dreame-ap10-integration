# Dreame AP-10 Air Purifier Integration for Home Assistant

![Dreame AP-10](https://via.placeholder.com/728x90.png?text=Dreame+AP-10+Air+Purifier) <!-- Optional: replace with real image URL if you have one -->

Custom Home Assistant integration for the **Dreame AP-10 Air Purifier**.

Control your device locally (no cloud dependency if your code supports it) with:
- Fan entity (on/off, speed modes, preset modes)
- Sensors: PM2.5, temperature, humidity, filter life, air quality, etc.
- Switches: child lock, display, etc.
- UI-based setup via config flow

## Features
- Full fan control (speeds, modes, oscillation if supported)
- Real-time air quality and environmental sensors
- Filter status and replacement reminders
- Configurable via Home Assistant UI (no YAML required)
- Local polling (or push if your API allows)

## Installation

### Recommended: via HACS

[![Add Repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CodyJon&repository=dreame-ap10-integration)

1. Make sure HACS is installed in your Home Assistant.
2. Go to **HACS → Integrations**.
3. Click the **⋮** (three dots) in the top right → **Custom repositories**.
4. Paste this URL:  
   `https://github.com/CodyJon/dreame-ap10-integration`
5. Category: **Integration** → **Add**.
6. Search for **"Dreame AP-10"** in HACS Integrations.
7. Click **Download** → restart Home Assistant when prompted.
8. Go to **Settings → Devices & Services → + Add Integration** → search "Dreame" → follow config flow.

### Manual Installation (Advanced)
1. Download this repo as ZIP (or clone it).
2. Extract/copy the `custom_components/dreame_airpurifier` folder to your Home Assistant config directory:  
   `<config>/custom_components/dreame_airpurifier/`
3. Restart Home Assistant.
4. Add the integration via **Settings → Devices & Services → + Add Integration** → search "Dreame".

## Configuration
- No YAML config needed — uses config flow (UI setup).
- You'll need your Dreame device's IP address or token (check your Dreame app or network scanner).
- If discovery doesn't work, add manually via IP.

## Troubleshooting
- Integration not showing? Restart HA twice or clear browser cache.
- "Not compliant" in HACS? Ensure you have the latest release and refresh custom repos.
- Errors in logs? Check Developer Tools → Logs for "dreame_airpurifier" entries and open an issue.
- Device not connecting? Confirm IP is static and firewall allows local access.

## Contributing
Found a bug? Have an improvement?  
Feel free to open an **Issue** or submit a **Pull Request**!

## License
MIT License (or choose your preferred open-source license).

---

Thanks for using this integration!  
If it works well, give the repo a ⭐ on GitHub.
