#!/usr/bin/env python3
"""Monitor I-PAC 4X - read from all accessible HID interfaces."""

import hid
import time
import threading

ULTIMARC_VENDOR_ID = 0xD209

def read_interface(path, label):
    try:
        h = hid.device()
        h.open_path(path)
        h.set_nonblocking(False)
        print(f"[{label}] Listening...")
        while True:
            data = h.read(64, timeout_ms=100)
            if data:
                hex_str = " ".join(f"{b:02x}" for b in data)
                print(f"[{label}] Data: [{hex_str}]")
    except Exception as e:
        print(f"[{label}] Error: {e}")

def main():
    print("I-PAC 4X Raw HID Monitor")
    print("=" * 45)
    print("Press buttons on your I-PAC. Ctrl+C to quit.\n")

    devices = [d for d in hid.enumerate() if d["vendor_id"] == ULTIMARC_VENDOR_ID]
    threads = []

    for d in devices:
        iface = d["interface_number"]
        usage = d["usage"]
        upage = d["usage_page"]
        label = f"iface{iface}/up{upage}/u{usage}"

        # Skip the keyboard interface (will fail on macOS)
        if upage == 1 and usage == 6:
            print(f"[{label}] Skipped (keyboard - blocked by macOS)")
            continue

        t = threading.Thread(target=read_interface, args=(d["path"], label), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDone.")

if __name__ == "__main__":
    main()
