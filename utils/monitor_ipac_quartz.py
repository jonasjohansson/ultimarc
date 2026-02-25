#!/usr/bin/env python3
"""Monitor I-PAC 4X inputs using macOS Quartz event taps.

Requires Accessibility permission for Terminal:
  System Settings > Privacy & Security > Accessibility > enable Terminal
"""

import Quartz
from AppKit import NSKeyUp, NSKeyDown, NSFlagsChanged, NSEvent

def callback(proxy, event_type, event, refcon):
    if event_type in (Quartz.kCGEventKeyDown, Quartz.kCGEventKeyUp):
        keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        ns_event = NSEvent.eventWithCGEvent_(event)
        chars = ns_event.charactersIgnoringModifiers() or ""
        action = "DOWN" if event_type == Quartz.kCGEventKeyDown else "UP  "
        print(f"{action}  keycode: {keycode:3d}  char: {repr(chars):8s}")
    elif event_type == Quartz.kCGEventFlagsChanged:
        keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        flags = Quartz.CGEventGetFlags(event)
        mods = []
        if flags & Quartz.kCGEventFlagMaskShift: mods.append("Shift")
        if flags & Quartz.kCGEventFlagMaskControl: mods.append("Ctrl")
        if flags & Quartz.kCGEventFlagMaskAlternate: mods.append("Alt")
        if flags & Quartz.kCGEventFlagMaskCommand: mods.append("Cmd")
        mod_str = "+".join(mods) if mods else "none"
        print(f"MOD   keycode: {keycode:3d}  modifiers: {mod_str}")
    return event

def main():
    print("I-PAC 4X Input Monitor (Quartz)")
    print("=" * 45)
    print("Press buttons on your I-PAC controller.")
    print("Press Ctrl+C in this terminal to quit.")
    print()
    print("NOTE: If nothing appears, grant Accessibility")
    print("permission to Terminal in System Settings.")
    print()

    mask = (
        Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
        Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp) |
        Quartz.CGEventMaskBit(Quartz.kCGEventFlagsChanged)
    )

    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionListenOnly,
        mask,
        callback,
        None,
    )

    if tap is None:
        print("ERROR: Could not create event tap!")
        print("Grant Accessibility access to your terminal app:")
        print("  System Settings > Privacy & Security > Accessibility")
        return

    source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    loop = Quartz.CFRunLoopGetCurrent()
    Quartz.CFRunLoopAddSource(loop, source, Quartz.kCFRunLoopCommonModes)
    Quartz.CGEventTapEnable(tap, True)

    try:
        Quartz.CFRunLoopRun()
    except KeyboardInterrupt:
        print("\nDone.")

if __name__ == "__main__":
    main()
