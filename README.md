# Dreame AP-10 Air Purifier for Home Assistant

Custom integration for the **Dreame AP-10** (`dreame.airp.u2507`) via the Dreame Cloud API.

**Supported device:** AP-10 only. Other Dreame air or fan models are out of scope unless someone submits a PR with a probed property map and a tester for that hardware.

- PM10: use [shaunsingh/dreame-pm10-integration](https://github.com/shaunsingh/dreame-pm10-integration)
- MF10 Air / other `dreame.fan.*`: not an air purifier; needs its own map, not this repo

## Features

### Fan
- Power on/off — "Off" uses Sleep mode at speed 1 so the device stays cloud-connected (AP-10 cannot be woken from deep standby)
- Preset modes: AI Purify, Strong Purification, Sleep Purification, Custom Mode, Pet Purify
- Fan speed 1–5 (shown as 20/40/60/80/100% in HA)
- Manual speed changes switch the device into Custom Mode

### Sensors
- PM2.5 (µg/m³)
- Air quality level
- Filter life %
- Filter days left
- Filter hours used
- Device location

### Controls
- Light color (Off / Blue / Orange / Green)
- Voice interaction volume
- Timer (hours)
- Keypress tone, play mode, voice interaction, child lock
- Filter reset button

## Installation

### HACS

1. **HACS → Integrations → ⋮ → Custom repositories**
2. URL: `https://github.com/CodyJon/dreame-ap10-integration`
3. Category: **Integration** → Add
4. Search **Dreame AP-10** → Download → restart Home Assistant
5. **Settings → Devices & Services → Add Integration** → Dreame → Dreamehome credentials

Use a GitHub **release** (latest is what HACS installs). Tracking `main` is only needed if you want unreleased commits.

### Manual

Copy `custom_components/dreame_airpurifier/` into `config/custom_components/`, restart, then add the integration.

## Setup

- Dreamehome **email + password** (set a password in the app if you signed up with Google/Apple)
- Server region: `us`, `eu`, `cn`, `sg`, `kr`, `ru`
- Discovers AP-10 units on that account (`dreame.airp.*`). Multiple purifiers are supported.

## Power behavior

The AP-10 drops off the cloud in true standby. This integration never sends a hard power-off:

- **Off in HA** → Sleep Purification + speed 1
- **On in HA** → AI Purify
- Do not use the physical power button if you want remote control to keep working

State is polled from the Dreame cloud every 30 seconds. There is no local API.

## AP-10 property map

Verified on `dreame.airp.u2507`. Do not assume this matches PM10, MF10, or other models.

| siid | piid | Property | Values |
|------|------|----------|--------|
| 2 | 1 | Power | 1=on, 2=standby |
| 2 | 3 | Mode | 0=AI Purify, 1=Strong, 2=Sleep, 3=Custom, 4=Pet |
| 2 | 4 | Fan speed | 1–5 |
| 2 | 5 | Voice volume | 80 / 90 / 100 |
| 2 | 6 | Light | -1=off, 0=blue, 1=orange, 2=green |
| 2 | 7 | Keypress tone | 0=off, 1=on |
| 3 | 4 | Air quality level | int |
| 3 | 5 | PM2.5 | µg/m³ |
| 4 | 1 | Filter life | 0–100% |
| 4 | 2 | Filter days left | days |
| 4 | 3 | Filter hours used | hours |
| 6 | 3 | Device location | string |
| 6 | 5 | Child lock | 0=off, 1=on |
| 6 | 6 | Play mode | 0=off, 1=on |
| 6 | 7 | Voice interaction | 0=off, 1=on |
| 6 | 8 | Timer | 0–12 hours |

Power uses toggle action `siid=2, aiid=3`. Direct writes to power (`siid=2, piid=1`) time out. Filter reset is action `siid=4, aiid=1`.

## Troubleshooting

- **Login fails** — same credentials as Dreamehome; pick the region your account was created in
- **No devices** — this integration only lists `*.airp.*` models
- **Unavailable** — purifier is in deep standby, or offline in the app
- Logs: Developer Tools → Logs → `dreame_airpurifier`

## Contributing

PRs welcome for AP-10 fixes, extra regions, and other `dreame.airp.*` models **with a probed map plus someone who can test that device**.

Please do not open PRs that:
- Guess mappings from another model
- Add `dreame.fan.*` / MF10 support in this repo
- Merge PM10 or vacuum code into this tree

## License

MIT
