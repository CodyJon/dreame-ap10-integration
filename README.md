# Dreame AP-10 Air Purifier Integration for Home Assistant

Custom Home Assistant integration for the **Dreame AP-10 Air Purifier**.

This component lets you control your Dreame AP-10 locally and view real-time air quality data right in Home Assistant.

## Features
- Fan entity: on/off, speed levels, modes, oscillation (if supported by device)
- Sensors: PM2.5, temperature, humidity, filter life percentage, air quality index
- Switches: child lock, display, turbo mode, etc. (depending on your model/firmware)
- Config flow UI setup (no YAML editing required)
- Local communication (no cloud needed once set up)

## Installation

### Via HACS (Recommended)

[![Add Repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CodyJon&repository=dreame-ap10-integration)

1. Open **HACS → Integrations** in Home Assistant.
2. Click the **⋮** (three dots) in the top right → **Custom repositories**.
3. Paste this URL:  
   `https://github.com/CodyJon/dreame-ap10-integration`
4. Select **Integration** as the category → **Add**.
5. Search for **"Dreame AP-10"** in the HACS Integrations list.
6. Click **Download** → restart Home Assistant when prompted.
7. Go to **Settings → Devices & Services → + Add Integration** → search "Dreame" → follow the config flow.

### Manual Installation
1. Download this repository as ZIP.
2. Extract the `custom_components/dreame_airpurifier` folder to your Home Assistant config directory:  
   `<config>/custom_components/dreame_airpurifier/`
3. Restart Home Assistant.
4. Add the integration via **Settings → Devices & Services → + Add Integration** → search "Dreame".

## Setup
- Make sure your Dreame AP-10 is connected to the same Wi-Fi network as Home Assistant.
- During setup, you'll need the device's **local IP address** (find it in the Dreame app, your router's device list, or use a network scanner like Fing or Angry IP Scanner).
- If you have multiple AP-10 units, add each one as a separate integration.
- After setup, entities will appear like:
  - `fan.dreame_ap10_living_room`
  - `sensor.dreame_ap10_pm25`
  - `sensor.dreame_ap10_filter_life`

## Troubleshooting
- **Not discovering device?** Enter the IP manually during config flow.
- **Connection errors?** Check that the device is powered on and not in cloud-only mode. Restart HA and the purifier.
- **Values not updating?** Increase polling interval in advanced options if needed (default is usually fine).
- Check **Developer Tools → Logs** for entries starting with `dreame_airpurifier` if something goes wrong.

## Contributing
Bugs, missing features, or improvements?  
Please open an **Issue** or submit a **Pull Request** on GitHub.

## License
MIT License

---

Thanks for trying it out!  
If it works well for you, drop a ⭐ on the repo — it helps others find it too. 😊
