#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio_tuner.py - Acoustic & Sound Quality Tuning Engine
Expands media volume steps to 30, enables Hi-Res PCM offload, and inspects SmartPA DSP gains.
"""

import sys
import subprocess
import json
import argparse

def get_target_device(serial=None):
    if serial:
        return serial
    p = subprocess.run(["adb", "devices"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    lines = [l.strip() for l in p.stdout.splitlines() if l.strip() and not l.startswith("List of")]
    for l in lines:
        parts = l.split()
        if len(parts) >= 2 and parts[1] == "device":
            return parts[0]
    return None

def adb_shell(target, cmd, use_su=False):
    prefix = ["adb"]
    if target:
        prefix.extend(["-s", target])
    prefix.append("shell")
    if use_su:
        prefix.extend(["su", "-c", cmd])
    else:
        prefix.append(cmd)
    try:
        p = subprocess.run(prefix, capture_output=True, text=True, timeout=15, encoding="utf-8", errors="ignore")
        return (p.stdout or "").strip()
    except Exception as e:
        return ""

def tune_volume_steps(target, steps=30):
    print(f"[*] Expanding media volume steps to {steps} levels for fine-grained control...")
    cmd = f"setprop ro.config.media_vol_steps {steps}; setprop ro.config.vc_call_vol_steps 15"
    adb_shell(target, cmd, use_su=True)
    return {"media_vol_steps": steps, "call_vol_steps": 15}

def enable_hires_offload(target):
    print("[*] Enabling 24-bit / 32-bit Hi-Res PCM direct audio offload...")
    cmd = """
    setprop persist.audio.format.24bit true
    setprop persist.audio.format.32bit true
    setprop persist.audio.format.float true
    setprop persist.vendor.audio.format.24bit true
    setprop vendor.audio.offload.passthrough true
    """
    adb_shell(target, cmd, use_su=True)
    return {"hires_pcm_offload": "enabled"}

def inspect_smartpa_modules(target):
    out = adb_shell(target, "find /data/adb/modules -name '*sound*' -o -name '*Sound*' 2>/dev/null", use_su=True)
    mods = [m for m in out.splitlines() if m.strip()]
    return {"detected_sound_modules": mods}

def main():
    parser = argparse.ArgumentParser(description="Acoustic & Sound Quality Tuning Engine")
    parser.add_argument("-s", "--serial", help="Specific ADB device target")
    parser.add_argument("--tune-volume-steps", type=int, default=30, help="Expand media volume steps (default: 30)")
    parser.add_argument("--enable-hires", action="store_true", help="Enable 24/32bit PCM offload")
    parser.add_argument("--inspect", action="store_true", help="Inspect audio modules and configs")
    args = parser.parse_args()

    target = get_target_device(args.serial)
    if not target:
        print(json.dumps({"error": "No connected ADB device found."}, ensure_ascii=False))
        sys.exit(1)

    r1 = tune_volume_steps(target, args.tune_volume_steps)
    r2 = enable_hires_offload(target)
    r3 = inspect_smartpa_modules(target)
    print(json.dumps({"volume": r1, "hires": r2, "modules": r3}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
