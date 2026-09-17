#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
system_tuner.py - Performance & Smoothness Optimization Engine
Executes cached_apps_freezer, 0.75x animation scale, global high refresh rate, and ART Speed-Profile dexopt.
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

def adb_shell(target, cmd):
    prefix = ["adb"]
    if target:
        prefix.extend(["-s", target])
    prefix.extend(["shell", cmd])
    try:
        p = subprocess.run(prefix, capture_output=True, text=True, timeout=120, encoding="utf-8", errors="ignore")
        return (p.stdout or "").strip()
    except Exception as e:
        return str(e)

def apply_freezer(target):
    print("[*] Activating Native Cached Apps Freezer (cgroup v2)...")
    res1 = adb_shell(target, "settings put global cached_apps_freezer enabled")
    res2 = adb_shell(target, "device_config put activity_manager_native_boot use_freezer true")
    return {"freezer_enabled": True}

def apply_animations(target, scale="0.75"):
    print(f"[*] Tuning animation scale to {scale}x for swift responsiveness...")
    adb_shell(target, f"settings put global window_animation_scale {scale}")
    adb_shell(target, f"settings put global transition_animation_scale {scale}")
    adb_shell(target, f"settings put global animator_duration_scale {scale}")
    return {"animation_scale": scale}

def apply_refresh_rate(target, min_hz=120, peak_hz=144):
    print(f"[*] Unlocking full refresh rates: min {min_hz}Hz, peak {peak_hz}Hz...")
    adb_shell(target, f"settings put system min_refresh_rate {min_hz}")
    adb_shell(target, f"settings put system peak_refresh_rate {peak_hz}")
    adb_shell(target, f"settings put secure user_refresh_rate {peak_hz}")
    adb_shell(target, f"settings put secure miui_refresh_rate {peak_hz} 2>/dev/null")
    return {"min_refresh_rate": min_hz, "peak_refresh_rate": peak_hz}

def apply_speed_mode(target):
    print("[*] Enabling system speed mode...")
    adb_shell(target, "settings put secure speed_mode 1 2>/dev/null")
    return {"speed_mode": 1}

def apply_dexopt(target, packages=None):
    if not packages:
        packages = [
            "com.android.systemui", "com.miui.home", "com.android.settings",
            "com.tencent.mm", "com.android.camera", "com.miui.gallery"
        ]
    results = {}
    print(f"[*] Precompiling {len(packages)} core packages with AOT Speed-Profile...")
    for pkg in packages:
        print(f"  [>] Compiling {pkg}...")
        out = adb_shell(target, f"cmd package compile -m speed-profile -f {pkg}")
        results[pkg] = "Success" if "Success" in out else out
    return results

def apply_fstrim(target):
    print("[*] Running UFS flash storage FSTRIM...")
    out = adb_shell(target, "sm fstrim 2>/dev/null || fstrim -v /data 2>/dev/null")
    return {"fstrim": out or "Triggered"}

def apply_all(target):
    r1 = apply_freezer(target)
    r2 = apply_animations(target)
    r3 = apply_refresh_rate(target)
    r4 = apply_speed_mode(target)
    r5 = apply_dexopt(target)
    r6 = apply_fstrim(target)
    return {
        "freezer": r1,
        "animations": r2,
        "refresh_rate": r3,
        "speed_mode": r4,
        "dexopt": r5,
        "fstrim": r6
    }

def main():
    parser = argparse.ArgumentParser(description="Performance & Smoothness Optimization Engine")
    parser.add_argument("-s", "--serial", help="Specific ADB device target")
    parser.add_argument("--apply-all", action="store_true", help="Apply all safe performance optimizations")
    parser.add_argument("--freezer", action="store_true", help="Enable cgroup v2 cached apps freezer")
    parser.add_argument("--animations", default=None, help="Set animation scales (e.g. 0.75)")
    parser.add_argument("--refresh-rate", nargs=2, type=int, metavar=("MIN", "PEAK"), help="Lock refresh rate")
    parser.add_argument("--dexopt", action="store_true", help="Run AOT speed-profile compilation on core apps")
    parser.add_argument("--fstrim", action="store_true", help="Trim UFS storage")
    args = parser.parse_args()

    target = get_target_device(args.serial)
    if not target:
        print(json.dumps({"error": "No connected ADB device found."}, ensure_ascii=False))
        sys.exit(1)

    if args.apply_all:
        res = apply_all(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.freezer:
        res = apply_freezer(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.animations:
        res = apply_animations(target, args.animations)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.refresh_rate:
        res = apply_refresh_rate(target, args.refresh_rate[0], args.refresh_rate[1])
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.dexopt:
        res = apply_dexopt(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.fstrim:
        res = apply_fstrim(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        res = apply_all(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
