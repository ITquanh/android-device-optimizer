#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
model_intelligence.py - Model Intelligence & Community Scheme Extractor
Generates high-precision community search queries (CoolApk, XDA, GitHub) and compiles tailored recommendations.
"""

import sys
import json
import argparse
import subprocess

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

def analyze_device_model(device_data):
    identity = device_data.get("identity", {})
    system = device_data.get("system", {})
    battery = device_data.get("battery_bms", {})
    memory = device_data.get("memory", {})
    
    brand = identity.get("brand", "").lower()
    model = identity.get("model", "")
    codename = identity.get("device_codename", "").lower()
    soc = identity.get("soc_platform", "").lower()
    android_api = system.get("sdk_api", 0)
    is_root = system.get("is_root", False)
    
    # Generate search queries for community inspection
    search_queries = [
        f'"{identity.get("marketing_name", model)}" ("优化方案" OR "调速模块" OR "解锁高刷")',
        f'"{codename}" ("酷安" OR "GitHub") ("锁帧" OR "温控" OR "杜比音效")',
        f'"{soc}" ("调度" OR "掉帧" OR "墓碑" OR "BMS锁容")'
    ]

    tailored_recommendations = []
    
    # 1. SoC-specific recommendations
    if "mt6985" in soc or "dimensity" in soc or "天玑" in soc:
        tailored_recommendations.append({
            "category": "SoC 架构调优 (MediaTek Dimensity)",
            "finding": f"检测到联发科天玑平台 ({soc})，其 PPM/GED 调度器对虚拟内存和高频非常敏感。",
            "action": "建议关闭系统自带的'内存扩展'，避免 CPU 小核/中核频繁执行 lz4 压缩算法损耗算力并引发发热。"
        })
    elif "sm8" in soc or "snapdragon" in soc or "骁龙" in soc:
        tailored_recommendations.append({
            "category": "SoC 架构调优 (Qualcomm Snapdragon)",
            "finding": f"检测到高通骁龙平台 ({soc})，EAS 调速器具备优秀能效比。",
            "action": "推荐启用 FAS-RS 帧感知调度闭环，按需给频，杜绝暴力锁大核导致高温撞墙。"
        })

    # 2. Large RAM recommendations
    if memory.get("total_gb", 0) >= 12:
        tailored_recommendations.append({
            "category": "物理大内存释放 (RAM Management)",
            "finding": f"本机具备 {memory.get('total_gb')}GB 物理大内存，当前物理空闲内存极度充裕。",
            "action": "强烈建议彻底关闭虚拟内存扩展，释放被占用的 CPU 压缩能耗，可降低整机温度 1~2℃。"
        })

    # 3. Android 15/16 specific safeguards
    if android_api >= 35:
        tailored_recommendations.append({
            "category": "新一代系统安全避坑 (Android 15/16 16KB & RKP)",
            "finding": "系统版本为最新 Android 15/16，全面启用 16KB 页面对齐与硬件 RKP 密钥证明。",
            "action": "必须坚决清理旧版失效改机/IMEI伪装与旧版 Shamiko 模块；保留 KernelSU 内核级白名单隔离策略。"
        })

    # 4. Battery BMS recommendations
    cycles = battery.get("cycle_count", 0)
    soh = battery.get("health_soh_percent", 100)
    if cycles > 500:
        tailored_recommendations.append({
            "category": "电池健康与电量计校准 (BMS Reset)",
            "finding": f"电池已历经 {cycles} 次完整充放电循环，底层电量计学习了保守的高阻抗参数。",
            "action": "建议重置 batterystats 阻抗学习记录，并按照标准物理涓流慢充流程充满静置 20 分钟释放可用容量。"
        })

    # 5. Audio recommendations
    tailored_recommendations.append({
        "category": "声学与音频微调 (Acoustic Tuning)",
        "finding": "系统原生媒体音量仅 15 级，调控步进过粗糙。",
        "action": "建议将系统媒体音量档位扩容至 30 级平滑调节；开启 24-bit PCM 直通绕过 Android 48kHz 重采样。"
    })

    return {
        "device_signature": f"{identity.get('brand')} {identity.get('marketing_name')} ({codename})",
        "community_search_queries": search_queries,
        "tailored_recommendations": tailored_recommendations
    }

def main():
    parser = argparse.ArgumentParser(description="Model Intelligence & Community Scheme Extractor")
    parser.add_argument("-s", "--serial", help="Specific ADB device target")
    parser.add_argument("--json-input", help="Optional pre-extracted device inspector JSON")
    args = parser.parse_args()

    if args.json_input:
        with open(args.json_input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        from device_inspector import inspect_all, get_target_device
        target = get_target_device(args.serial)
        if not target:
            print(json.dumps({"error": "No connected ADB device found."}, ensure_ascii=False))
            sys.exit(1)
        data = inspect_all(target)

    analysis = analyze_device_model(data)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
