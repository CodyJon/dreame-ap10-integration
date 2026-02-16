# Dreame AP-10 Air Purifier Integration for Home Assistant

Custom Home Assistant integration for the **Dreame AP-10 Air Purifier** (model `dreame.airp.u2507`), built by reverse-engineering the Dreame Cloud API.

No official Dreame integration exists for air purifiers in Home Assistant — this is the first.

## Features

### Fan Entity
- **Power on/off** — "Off" uses Sleep mode at minimum speed to keep the device cloud-connected (the AP-10 cannot be woken remotely from true standby)
- **Preset modes** — Auto, Sleep, Custom, Pet
- **Fan speed** — 5 speed levels (shown as 20/40/60/80/100% in HA)
- Setting fan speed automatically switches to Custom mode

### Sensors
- **PM2.5** — Real-time particulate matter reading (µg/m³)
- **Air Quality Level** — Numeric air quality index from the device
- **Filter Life** — Remaining filter percentage
- **Filter Hours Used** — Total hours on the current filter

### Switches
- **Ionizer** — Toggle the ionizer on/off
- **LED Indicator** — Toggle the display LED
- **Buzzer** — Toggle button sounds
- **Child Lock** — Toggle the child lock

## Installation

### Via HACS (Recommended)

1. In Home Assistant: **HACS → Integrations**
2. Click **⋮** (top right) → **Custom repositories**
3. Paste URL: `https://github.com/CodyJon/dreame-ap10-integration`
4. Category: **Integration** → **Add**
5. Search **"Dreame AP-10"** → **Download** → restart HA
6. **Settings → Devices & Services → + Add Integration** → search "Dreame" → enter your Dreamehome app credentials

### Manual Installation

1. Download or clone this repo
2. Copy `custom_components/dreame_airpurifier/` into your HA `config/custom_components/` directory
3. Restart Home Assistant
4. **Settings → Devices & Services → + Add Integration** → search "Dreame"

## Setup

- Use your **Dreamehome app** credentials (email + password)
- Select your server region (US, EU, CN, etc.)
- The integration automatically discovers all AP-10 purifiers on your account
- Multiple purifiers are supported — each appears as a separate device in HA

## Important Notes

### Power Behavior
The AP-10 enters a deep standby when powered off that disconnects it from the cloud entirely. **Neither the Dreamehome app nor this integration can wake it remotely.** To keep the device controllable:

- **"Turn off" in HA** switches to Sleep mode at the lowest fan speed (near silent, minimal power draw)
- **"Turn on" in HA** switches back to Auto mode
- **Avoid using the physical power button to turn it off** if you want remote control to keep working

### Cloud Polling
This integration communicates via the Dreame Cloud API (same as the Dreamehome app). It polls for state updates every 30 seconds. Commands are sent through the cloud — there is no local API available for this device.

## Verified Property Map

For anyone looking to extend this integration or build their own, here's the complete MiOT property map we discovered through testing:

| siid | piid | Property | Values |
|------|------|----------|--------|
| 2 | 1 | Power | 1=on, 2=standby |
| 2 | 3 | Mode | 0=Auto, 2=Sleep, 3=Custom, 4=Pet |
| 2 | 4 | Fan Speed | 1-5 |
| 2 | 5 | Fan Speed % | Read-only percentage |
| 2 | 6 | Ionizer | -1=auto, 0=off, 1=on |
| 3 | 4 | Air Quality Level | Numeric index |
| 3 | 5 | PM2.5 | µg/m³ |
| 4 | 1 | Filter Life | 0-100% |
| 4 | 2 | Filter Lifespan | Total days |
| 4 | 3 | Filter Used | Hours |
| 6 | 5 | LED | 0=off, 1=on |
| 6 | 6 | Buzzer | 0=off, 1=on |
| 6 | 7 | Child Lock | 0=off, 1=on |
| 6 | 8 | Light Mode | Numeric |

**Key discovery:** Power control requires a toggle action (`siid=2, aiid=3`), not `set_properties`. Direct property writes to `siid=2, piid=1` time out. Mode and fan speed can be set via `set_properties` on `siid=2`. Settings switches (`siid=6`) also use `set_properties` normally.

## Troubleshooting

- **Login fails?** Verify your credentials work in the Dreamehome app. The integration uses the same login.
- **Device unavailable?** Make sure the purifier is powered on (not in deep standby). Check that it shows online in the Dreamehome app.
- **Commands not working?** Check HA logs under Developer Tools → Logs, search for `dreame_airpurifier`.
- **State not updating?** The integration polls every 30 seconds. Cloud state can sometimes lag behind physical changes.

## Contributing

Issues, feature requests, and PRs welcome.

## License

MIT License
