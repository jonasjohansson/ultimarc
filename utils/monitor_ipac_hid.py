#!/usr/bin/env python3
"""Monitor I-PAC 4X inputs directly via HID (bypasses keyboard layer)."""

import hid

ULTIMARC_VENDOR_ID = 0xD209
IPAC4_PRODUCT_ID = 0x0430

def main():
    print("I-PAC 4X Direct HID Monitor")
    print("=" * 40)

    # List all Ultimarc devices
    devices = [d for d in hid.enumerate() if d["vendor_id"] == ULTIMARC_VENDOR_ID]
    if not devices:
        print("ERROR: No Ultimarc devices found!")
        return

    print(f"Found {len(devices)} Ultimarc HID interface(s):")
    for d in devices:
        print(f"  - {d['product_string']} (usage_page={d['usage_page']}, usage={d['usage']})")
        print(f"    path: {d['path']}")

    # Try to open the keyboard interface (usage_page=1, usage=6 = keyboard)
    target = None
    for d in devices:
        if d["usage_page"] == 1 and d["usage"] == 6:
            target = d
            break

    if not target:
        # Fallback: try the first device
        target = devices[0]
        print(f"\nNo keyboard interface found, trying first device...")

    print(f"\nOpening: {target['product_string']} (usage_page={target['usage_page']}, usage={target['usage']})")
    print("Press buttons on your I-PAC. Ctrl+C to quit.\n")

    try:
        h = hid.device()
        h.open_path(target["path"])
        h.set_nonblocking(False)

        prev_data = None
        while True:
            data = h.read(64)
            if data and data != prev_data:
                hex_str = " ".join(f"{b:02x}" for b in data)
                # For keyboard HID reports: byte 0 = modifier, byte 1 = reserved, bytes 2-7 = keycodes
                if target["usage"] == 6:
                    modifier = data[0] if len(data) > 0 else 0
                    keys = [b for b in data[2:] if b != 0] if len(data) > 2 else []
                    if keys or modifier:
                        mod_names = []
                        if modifier & 0x01: mod_names.append("L-Ctrl")
                        if modifier & 0x02: mod_names.append("L-Shift")
                        if modifier & 0x04: mod_names.append("L-Alt")
                        if modifier & 0x08: mod_names.append("L-Super")
                        if modifier & 0x10: mod_names.append("R-Ctrl")
                        if modifier & 0x20: mod_names.append("R-Shift")
                        if modifier & 0x40: mod_names.append("R-Alt")
                        if modifier & 0x80: mod_names.append("R-Super")
                        mod_str = "+".join(mod_names) if mod_names else "none"
                        key_str = ", ".join(f"0x{k:02x}" for k in keys) if keys else "none"
                        print(f"Modifier: {mod_str:20s}  Keys: {key_str:20s}  Raw: [{hex_str}]")
                    elif all(b == 0 for b in data):
                        print(f"(released)")
                else:
                    print(f"Data: [{hex_str}]")
                prev_data = list(data)
    except IOError as e:
        print(f"\nERROR opening device: {e}")
        print("You may need to grant Input Monitoring permission to Terminal.")
        print("Go to: System Settings > Privacy & Security > Input Monitoring")
    except KeyboardInterrupt:
        print("\nDone.")

if __name__ == "__main__":
    main()
