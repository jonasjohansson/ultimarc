#!/usr/bin/env python3
"""Monitor I-PAC 4X button inputs in the terminal."""

import sys
import tty
import termios

def main():
    print("I-PAC 4X Input Monitor")
    print("=" * 40)
    print("Press buttons on your I-PAC controller.")
    print("Press Ctrl+C to quit.\n")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ord(ch) == 3:  # Ctrl+C
                break
            # Format output
            code = ord(ch)
            if 32 <= code <= 126:
                display = ch
            else:
                display = f"(non-printable)"
            sys.stdout.write(f"Key: {repr(ch):8s}  Char: {display:16s}  Dec: {code:3d}  Hex: 0x{code:02x}\r\n")
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print("\nDone.")

if __name__ == "__main__":
    main()
