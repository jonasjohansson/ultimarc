# Ultimarc Tools for macOS

Configure [Ultimarc](https://www.ultimarc.com) arcade boards from macOS via USB. Ported from [Ultimarc-linux](https://github.com/katie-snow/Ultimarc-linux) by Robert Abram & Katie Snow.

## Supported Boards

- **PacLED64** — 64-channel LED controller (with flash script recording)
- **I-PAC 2 / 4** — Keyboard encoders (pre-2015 and 2015+)
- **Mini-PAC / J-PAC** — Keyboard encoders
- **IPAC Ultimate I/O** — Keyboard encoder with LED control
- **UltraStik 360** — Analog joystick
- **PacDrive** — LED driver (accent lighting)
- **USBButton** — Illuminated USB button
- **ServoStik** — 4/8-way restrictor servo
- **U-HID / U-HID Nano** — Custom HID interface

## Install

```bash
brew install json-c libusb
make
```

## Usage

```bash
sudo ./umtool <config.json> [config2.json ...]
```

Root access (`sudo`) is required because macOS claims USB HID devices exclusively.

## PacLED64

The PacLED64 has 64 individually controllable LED outputs. For RGB LEDs, each color channel uses one output (3 outputs per LED).

**LED numbering is zero-indexed** — physical pin 1 on the board = `"led": 0` in the config.

### Set all LEDs to full brightness

```json
{
  "version": 1,
  "product": "pacled64",
  "board id": 1,
  "LED intensity all": 255
}
```

### Set individual LEDs (RGB example)

```json
{
  "version": 1,
  "product": "pacled64",
  "board id": 1,
  "intensity": [
    {"led": 0, "intensity": 255},
    {"led": 1, "intensity": 0},
    {"led": 2, "intensity": 255}
  ]
}
```

### Intensity & fade reference

| Parameter | Range | Description |
|-----------|-------|-------------|
| `led` | 0–63 | LED output (zero-indexed from board label) |
| `intensity` | 0–255 | Brightness (0 = off) |
| `fade` | 0–7 | Fade speed (0 = instant, 7 = slowest) |

### Flash script recording

When you run `umtool` with a PacLED64 config, the commands are **automatically saved to the board's flash memory**. The board will replay the stored script on every power-up — no computer needed.

The protocol supports these flash commands:

| Command | Description |
|---------|-------------|
| `0xFF, 0x01` | Start recording |
| `0xFF, 0x03` | Stop recording (save to flash) |
| `0xFF, 0x00` | Run stored script |
| `0xFF, 0x04` | Clear flash |
| `0xC1, delay` | Set step delay between commands |

### 4-player RGB example

See [`examples/pacled64/all_players.json`](examples/pacled64/all_players.json) for a complete 4-player setup with magenta, orange, blue, and yellow LED colors.

## I-PAC 4

```bash
sudo ./umtool examples/ipac4/ipac4_2015_default.json
```

See `examples/ipac4/` for default pin mappings. Configs support pin remapping, shift keys, macros, debounce, and PacLink settings.

## Examples

```
examples/
├── pacled64/          # PacLED64 LED controller
├── ipac4/             # I-PAC 4 keyboard encoder
├── ipac2/             # I-PAC 2 keyboard encoder
├── ipac-ultimate/     # IPAC Ultimate I/O
└── other/             # Mini-PAC, J-PAC, UltraStik, PacDrive, etc.
```

## macOS Notes

- Requires `sudo` — macOS claims HID devices exclusively
- Uses `libusb_set_auto_detach_kernel_driver` to temporarily release the macOS HID driver
- You may see `no capture entitlements` warnings — these can be ignored, the transfers still work
- Tested on macOS Sequoia (Apple Silicon)

## Credits

Based on [Ultimarc-linux](https://github.com/katie-snow/Ultimarc-linux) by Robert Abram & Katie Snow (GPL-2.0).
PacLED64 flash protocol from [PacDriveSDK](https://github.com/benbaker76/PacDriveSDK) by Ben Baker.

## License

GPL-2.0 — see [LICENSE](LICENSE).
