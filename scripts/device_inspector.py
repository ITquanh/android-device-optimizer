#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
device_inspector.py - Multi-Dimensional Android Device Inspector
Collects Hardware, SoC, Android version, Form factor, ROM, BMS Battery, Memory, and Root status.
"""

import sys
import subprocess
import json
import argparse
import re

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
        p = subprocess.run(prefix, capture_output=True, text=True, timeout=10, encoding="utf-8", errors="ignore")
        return (p.stdout or "").strip()
    except Exception as e:
        return ""

def check_root(target):
    out = adb_shell(target, "id", use_su=True)
    is_root = "uid=0(root)" in out
    return is_root, out

def inspect_all(target):
    is_root, root_info = check_root(target)
    
    props_raw = adb_shell(target, "getprop")
    props = {}
    for line in props_raw.splitlines():
        m = re.match(r"\[([^\]]+)\]: \[(.*)\]", line)
        if m:
            props[m.group(1)] = m.group(2)

    brand = props.get("ro.product.brand", props.get("ro.product.manufacturer", "Unknown"))
    model = props.get("ro.product.model", "Unknown")
    device = props.get("ro.product.device", props.get("ro.product.name", "Unknown"))
    marketing_name = props.get("ro.product.marketname", model)
    android_ver = props.get("ro.build.version.release", "Unknown")
    sdk_api = int(props.get("ro.build.version.sdk", 0))
    build_id = props.get("ro.build.display.id", props.get("ro.build.id", "Unknown"))
    soc_model = props.get("ro.soc.model", props.get("ro.board.platform", props.get("ro.hardware", "Unknown")))
    miui_ver = props.get("ro.miui.ui.version.name", props.get("ro.build.version.incremental", ""))

    # Form factor determination
    form_factor = "phone"
    characteristics = props.get("ro.build.characteristics", "").lower()
    if "tv" in characteristics or "box" in characteristics:
        form_factor = "tv"
    elif "tablet" in characteristics or "pad" in device.lower():
        form_factor = "tablet"
    elif "automotive" in characteristics or "car" in device.lower():
        form_factor = "car"

    # Memory info
    mem_info_raw = adb_shell(target, "cat /proc/meminfo")
    mem_total_kb = 0
    mem_avail_kb = 0
    for line in mem_info_raw.splitlines():
        if line.startswith("MemTotal:"):
            mem_total_kb = int(re.findall(r"\d+", line)[0])
        elif line.startswith("MemAvailable:"):
            mem_avail_kb = int(re.findall(r"\d+", line)[0])
    
    mem_total_gb = round(mem_total_kb / (1024 * 1024), 2)
    mem_avail_gb = round(mem_avail_kb / (1024 * 1024), 2)

    # Battery BMS info
    bms_raw = adb_shell(target, "cat /sys/class/power_supply/battery/uevent 2>/dev/null || cat /sys/class/power_supply/bms/uevent 2>/dev/null", use_su=is_root)
    bms_props = {}
    for line in bms_raw.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            bms_props[k.strip()] = v.strip()

    design_mah = int(bms_props.get("POWER_SUPPLY_CHARGE_FULL_DESIGN", 0)) // 1000 if int(bms_props.get("POWER_SUPPLY_CHARGE_FULL_DESIGN", 0)) > 100000 else int(bms_props.get("POWER_SUPPLY_CHARGE_FULL_DESIGN", 0))
    full_mah = int(bms_props.get("POWER_SUPPLY_CHARGE_FULL", 0)) // 1000 if int(bms_props.get("POWER_SUPPLY_CHARGE_FULL", 0)) > 100000 else int(bms_props.get("POWER_SUPPLY_CHARGE_FULL", 0))
    cycle_count = int(bms_props.get("POWER_SUPPLY_CYCLE_COUNT", 0))
    temp_c = int(bms_props.get("POWER_SUPPLY_TEMP", 0)) / 10.0
    
    soh_percent = round((full_mah / design_mah) * 100, 2) if design_mah > 0 and full_mah > 0 else None

    # Modules info (if Root)
    modules = []
    if is_root:
        mod_raw = adb_shell(target, "ls -1 /data/adb/modules 2>/dev/null", use_su=True)
        if mod_raw:
            modules = [m.strip() for m in mod_raw.splitlines() if m.strip()]

    result = {
        "identity": {
            "brand": brand,
            "marketing_name": marketing_name,
            "model": model,
            "device_codename": device,
            "soc_platform": soc_model,
            "form_factor": form_factor
        },
        "system": {
            "android_version": android_ver,
            "sdk_api": sdk_api,
            "build_id": build_id,
            "custom_rom_version": miui_ver,
            "is_root": is_root,
            "root_info": root_info
        },
        "memory": {
            "total_gb": mem_total_gb,
            "available_gb": mem_avail_gb,
            "available_ratio": round((mem_avail_gb / mem_total_gb) * 100, 1) if mem_total_gb > 0 else 0
        },
        "battery_bms": {
            "charge_full_design_mah": design_mah,
            "charge_full_actual_mah": full_mah,
            "cycle_count": cycle_count,
            "health_soh_percent": soh_percent,
            "current_temp_c": temp_c
        },
        "root_ecosystem": {
            "installed_modules": modules,
            "module_count": len(modules)
        }
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Multi-Dimensional Android Device Inspector")
    parser.add_argument("-s", "--serial", help="Specific ADB device target")
    args = parser.parse_args()

    target = get_target_device(args.serial)
    if not target:
        print(json.dumps({"error": "No connected ADB device found. Please connect via USB or wireless ADB."}, ensure_ascii=False))
        sys.exit(1)

    data = inspect_all(target)
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
