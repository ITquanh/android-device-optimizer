#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adb_connector.py - Native ADB and Wireless ADB Connection Engine
Handles native USB ADB direct connect and Wireless ADB TLS pairing / port scanning.
"""

import sys
import subprocess
import socket
import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor

def run_cmd(cmd_list, timeout=15):
    try:
        p = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="ignore")
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -2, "", str(e)

def get_connected_devices():
    code, out, err = run_cmd(["adb", "devices", "-l"])
    devices = []
    if code == 0:
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("List of devices"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                serial = parts[0]
                state = parts[1]
                details = " ".join(parts[2:]) if len(parts) > 2 else ""
                devices.append({
                    "serial": serial,
                    "state": state,
                    "details": details,
                    "is_wireless": ":" in serial
                })
    return devices

def pair_wireless(ip_port, pairing_code):
    print(f"[*] Pairing with {ip_port} using code {pairing_code}...")
    code, out, err = run_cmd(["adb", "pair", ip_port, pairing_code], timeout=20)
    success = "Successfully paired" in out or "already paired" in out or code == 0
    return {"success": success, "output": out or err}

def connect_wireless(ip_port):
    print(f"[*] Connecting to {ip_port}...")
    code, out, err = run_cmd(["adb", "connect", ip_port], timeout=15)
    success = "connected to" in out.lower() or "already connected" in out.lower()
    return {"success": success, "output": out or err}

def scan_single_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.35)
        res = s.connect_ex((ip, port))
        s.close()
        if res == 0:
            return port
    except:
        pass
    return None

def auto_detect_wireless_port(ip, start_port=30000, end_port=49999):
    print(f"[*] Scanning {ip} for open wireless debugging ports...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=60) as executor:
        futures = [executor.submit(scan_single_port, ip, p) for p in range(start_port, end_port + 1)]
        for f in futures:
            p = f.result()
            if p:
                open_ports.append(p)
    return open_ports

def full_auto_pair_connect(ip, pair_port, pairing_code):
    res_pair = pair_wireless(f"{ip}:{pair_port}", pairing_code)
    print(f"[+] Pair result: {res_pair['output']}")
    if not res_pair["success"]:
        return {"success": False, "step": "pair", "error": res_pair["output"]}
    
    time.sleep(1)
    open_ports = auto_detect_wireless_port(ip)
    print(f"[+] Discovered open ports on {ip}: {open_ports}")
    
    for port in open_ports:
        if port == int(pair_port):
            continue
        res_conn = connect_wireless(f"{ip}:{port}")
        if res_conn["success"]:
            print(f"[✓] Successfully connected to {ip}:{port}")
            return {"success": True, "target": f"{ip}:{port}", "details": res_conn["output"]}
            
    res_conn = connect_wireless(f"{ip}:{pair_port}")
    return {"success": res_conn["success"], "target": f"{ip}:{pair_port}", "details": res_conn["output"]}

def main():
    parser = argparse.ArgumentParser(description="Native ADB and Wireless ADB Connection Engine")
    parser.add_argument("--devices", action="store_true", help="List all connected ADB devices")
    parser.add_argument("--pair", nargs=2, metavar=("IP:PORT", "CODE"), help="Pair wireless device")
    parser.add_argument("--connect", metavar="IP:PORT", help="Connect to wireless device")
    parser.add_argument("--auto-connect", metavar="IP", help="Scan and connect to device on LAN")
    parser.add_argument("--pair-and-connect", nargs=3, metavar=("IP", "PAIR_PORT", "CODE"), help="Full auto pair and connect")

    args = parser.parse_args()

    if args.devices:
        devs = get_connected_devices()
        print(json.dumps({"devices": devs}, indent=2, ensure_ascii=False))
    elif args.pair:
        res = pair_wireless(args.pair[0], args.pair[1])
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.connect:
        res = connect_wireless(args.connect)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.auto_connect:
        ports = auto_detect_wireless_port(args.auto_connect)
        print(f"Open ports: {ports}")
        for p in ports:
            c = connect_wireless(f"{args.auto_connect}:{p}")
            if c["success"]:
                print(f"Connected: {args.auto_connect}:{p}")
                break
    elif args.pair_and_connect:
        res = full_auto_pair_connect(args.pair_and_connect[0], args.pair_and_connect[1], args.pair_and_connect[2])
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        devs = get_connected_devices()
        print(json.dumps({"devices": devs}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
