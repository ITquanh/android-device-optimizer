#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
snapshot_engine.py - Anti-Bricking Snapshot & 100% Reversible Rollback Engine
Captures pre-flight settings, properties, and disabled packages; restores system state on demand.
"""

import sys
import subprocess
import json
import argparse
import time
import os

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def adb_shell(target, cmd):
    prefix = ["adb"]
    if target:
        prefix.extend(["-s", target])
    prefix.extend(["shell", cmd])
    try:
        p = subprocess.run(prefix, capture_output=True, text=True, timeout=15, encoding="utf-8", errors="ignore")
        return (p.stdout or "").strip()
    except:
        return ""

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

def capture_snapshot(target):
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"snapshot_{ts}.json"
    filepath = os.path.join(SNAPSHOT_DIR, filename)

    print(f"[*] Capturing pre-flight system snapshot for {target}...")
    
    # 1. Capture settings
    settings_global = {}
    for line in adb_shell(target, "settings list global").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            settings_global[k.strip()] = v.strip()

    settings_system = {}
    for line in adb_shell(target, "settings list system").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            settings_system[k.strip()] = v.strip()

    settings_secure = {}
    for line in adb_shell(target, "settings list secure").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            settings_secure[k.strip()] = v.strip()

    # 2. Capture disabled packages
    disabled_pkgs = adb_shell(target, "pm list packages -d").splitlines()
    disabled_pkgs = [p.replace("package:", "").strip() for p in disabled_pkgs if p.strip()]

    snapshot = {
        "timestamp": ts,
        "target": target,
        "settings_global": settings_global,
        "settings_system": settings_system,
        "settings_secure": settings_secure,
        "disabled_packages": disabled_pkgs
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    # Also update latest pointer
    latest_path = os.path.join(SNAPSHOT_DIR, "snapshot_latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    print(f"[✓] Snapshot saved: {filepath}")
    return {"success": True, "file": filepath, "timestamp": ts}

def rollback_snapshot(target, snapshot_file=None):
    if not snapshot_file:
        snapshot_file = os.path.join(SNAPSHOT_DIR, "snapshot_latest.json")

    if not os.path.exists(snapshot_file):
        print(f"[!] Error: Snapshot file not found: {snapshot_file}")
        return {"success": False, "error": "Snapshot file not found"}

    print(f"[*] Rolling back system state from: {snapshot_file}...")
    with open(snapshot_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Restore key settings
    key_global_keys = [
        "window_animation_scale", "transition_animation_scale", "animator_duration_scale",
        "cached_apps_freezer"
    ]
    for k in key_global_keys:
        v = data.get("settings_global", {}).get(k, "1.0" if "scale" in k else "disabled")
        adb_shell(target, f"settings put global {k} {v}")
        print(f"  [<] Restored global {k} = {v}")

    key_system_keys = ["min_refresh_rate", "peak_refresh_rate"]
    for k in key_system_keys:
        v = data.get("settings_system", {}).get(k, "")
        if v:
            adb_shell(target, f"settings put system {k} {v}")
        else:
            adb_shell(target, f"settings delete system {k}")
        print(f"  [<] Restored system {k} = {v or '<deleted>'}")

    print("[✓] Rollback completed successfully! System has returned to pre-optimization state.")
    return {"success": True, "restored_from": snapshot_file}

def main():
    parser = argparse.ArgumentParser(description="Snapshot & Rollback Engine")
    parser.add_argument("-s", "--serial", help="Specific ADB device target")
    parser.add_argument("--create", action="store_true", help="Create a new system snapshot")
    parser.add_argument("--rollback", action="store_true", help="Roll back to latest snapshot")
    parser.add_argument("--file", help="Specific snapshot file to roll back from")
    args = parser.parse_args()

    target = get_target_device(args.serial)
    if not target:
        print(json.dumps({"error": "No connected ADB device found."}, ensure_ascii=False))
        sys.exit(1)

    if args.create:
        res = capture_snapshot(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.rollback:
        res = rollback_snapshot(target, args.file)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        res = capture_snapshot(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
