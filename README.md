# Dreame AP-10 Air Purifier Integration for Home Assistant

Custom Home Assistant integration for the **Dreame AP-10 Air Purifier**.

Control your purifier locally with real-time air quality data — no constant cloud dependency after initial setup.

## Features
- Fan control: on/off, speeds, modes, oscillation (if supported)
- Sensors: PM2.5, temperature, humidity, filter life, air quality
- Switches: child lock, display, turbo, etc. (model-dependent)
- UI config flow setup (no YAML needed)
- Cloud login for easy discovery (uses Dreame app credentials)

## Installation

### Via HACS (Recommended)

[![Add Repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CodyJon&repository=dreame-ap10-integration)

1. In Home Assistant: **HACS → Integrations**.
2. Click **⋮** (top right) → **Custom repositories**.
3. Paste URL: `https://github.com/CodyJon/dreame-ap10-integration`
4. Category: **Integration** → **Add**.
5. Search **"Dreame AP-10"** → **Download** → restart HA.
6. **Settings → Devices & Services → + Add Integration** → search "Dreame" → follow config flow.

### Manual Installation
1. Download repo ZIP.
2. Copy `custom_components/dreame_airpurifier/` to `<config>/custom_components/`.
3. Restart HA.
4. Add via **Settings → Devices & Services → + Add Integration** → "Dreame".

## Setup
- Use your **Dreame app credentials** (email/phone + password) during config flow.
  - These are the same as your login for the Dreamehome app.
  - The integration logs in to discover your AP-10(s) automatically.
- No manual IP or token needed — cloud login handles device binding and local access.
- Multiple purifiers? Add each one separately if not auto-discovered.
- Entities: `fan.dreame_ap10_xxxx`, `sensor.dreame_ap10_pm25`, etc.

## Troubleshooting
- **Login fails?** Double-check credentials in Dreame app (logout/login to verify). Reset password if needed.
- **No devices found?** Ensure purifiers are online in Dreame app. Restart HA/purifier.
- **Connection drops?** Check HA logs (Developer Tools → Logs → search "dreame_airpurifier") for errors.
- Values not updating? Device may need wake-up (fan on/off via app) or increase polling in advanced options.

## Contributing
Issues, feature requests, or PRs welcome! Open on GitHub.

## License
MIT License

---

Glad it's working — enjoy cleaner air with full HA control! ⭐ the repo if helpful.

---

Thanks for trying it out!  
If it works well for you, drop a ⭐ on the repo — it helps others find it too. 😊
