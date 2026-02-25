#!/usr/bin/env python3
"""Monitor I-PAC 4X keyboard interface (requires sudo)."""

import hid

ULTIMARC_VENDOR_ID = 0xD209

def main():
    print("I-PAC 4X Monitor (sudo mode)")
    print("=" * 40)
    print("Press buttons on your I-PAC. Ctrl+C to quit.\n")

    devices = [d for d in hid.enumerate() if d["vendor_id"] == ULTIMARC_VENDOR_ID]

    # Find keyboard interface
    target = None
    for d in devices:
        if d["usage_page"] == 1 and d["usage"] == 6:
            target = d
            break

    if not target:
        print("ERROR: Keyboard interface not found")
        return

    try:
        h = hid.device()
        h.open_path(target["path"])
        print("Keyboard interface opened successfully!\n")
        h.set_nonblocking(False)

        prev_data = None
        while True:
            data = h.read(64, timeout_ms=100)
            if data and data != prev_data:
                hex_str = " ".join(f"{b:02x}" for b in data)
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
                    print("(released)")
                prev_data = list(data)
    except IOError as e:
        print(f"ERROR: {e}")
        print("Make sure you run with: sudo")
    except KeyboardInterrupt:
        print("\nDone.")

if __name__ == "__main__":
    main()
