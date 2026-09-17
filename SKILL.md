---
name: android-device-optimizer
description: >
  Universal Android device optimization and diagnostic skill supporting Android 5.0 to 16+.
  Auto-adapts to Phones, Tablets, Android TVs, and Car Head Units across HyperOS, OriginOS,
  ColorOS, and AOSP ROMs. Provides dual optimization pipelines: a non-invasive Non-Root route
  (via standard USB/Wireless ADB) and an extreme Root route (KernelSU/Magisk/APatch) covering
  performance, audio enhancement, battery BMS calibration, display refresh rate, network BBR,
  storage maintenance, automated web search for device-specific community schemes, and 100%
  safe snapshot-based one-click rollback.
---

# Android Device Optimizer Skill (安卓全场景全维调优中枢)

本技能专为 Android 全版本 (5.0 ~ 16+) 与多形态设备（手机、平板、电视、车机）打造，提供六大核心支柱【性能 · 音质 · 电池 · 屏幕 · 网络 · 存储】的诊断与调优。

> [!IMPORTANT]
> **两大核心原则**：
> 1. **防变砖绝对第一**：在执行任何写入修改前，**必须先通过 `snapshot_engine.py` 导出全量初始快照**；Root 路径下必须确认救砖防卡米保护；核心生命线包名绝对禁止禁用。
> 2. **连接后标准 6 步 SOP**：严格按照【连接】->【只读体检与机型方案检索】->【防砖筑底与快照】->【方案推荐与用户确认】->【渐进式执行】->【量化对比与回滚凭证】闭环作业。

---

## 🛠️ 技能脚本工具箱索引

| 脚本文件 | 核心职责 | 典型调用命令 |
| :--- | :--- | :--- |
| `adb_connector.py` | 原生有线 / 无线 ADB 连接与端口嗅探 | `python scripts/adb_connector.py --devices` |
| `device_inspector.py` | 六维硬件、系统、SoC、BMS 电池、Root 状态体检 | `python scripts/device_inspector.py [-s SERIAL]` |
| `model_intelligence.py` | 提取机型指纹，检索酷安/XDA成熟调优方案 | `python scripts/model_intelligence.py [-s SERIAL]` |
| `snapshot_engine.py` | 导出初始状态快照 / 一键 100% 逆向复原 | `python scripts/snapshot_engine.py --create / --rollback` |
| `system_tuner.py` | 进程墓碑、0.75x 动效、全局高刷、AOT 预编译、FSTRIM | `python scripts/system_tuner.py --apply-all` |
| `audio_tuner.py` | Hi-Res 直通、30 级平滑音量步进、SmartPA 增益检查 | `python scripts/audio_tuner.py --tune-volume-steps` |
| `battery_tuner.py` | BMS 阻抗学习记录重置、锁容释放、Doze 深度休眠 | `python scripts/battery_tuner.py --reset-bms` |

---

## 📋 用户连接后执行流程规范 (Execution Runbook)

### 第 1 步：连接与握手 (Connect)
* 检查已有设备：`python scripts/adb_connector.py --devices`
* 若为无线 ADB 初次配对：`python scripts/adb_connector.py --pair-and-connect <IP> <PAIR_PORT> <CODE>`

### 第 2 步：非侵入体检与全网机型方案检索 (Inspect & Search)
* 执行全维体检：`python scripts/device_inspector.py`
* 采集芯片架构、BMS 物理电池数据（设计容量、当前满充容量、循环次数、健康度）；
* 运行机型智能分析：`python scripts/model_intelligence.py`，根据机型代号检索成熟方案。
* 向用户输出《全维设备体检报告卡》与《针对本机的成熟调优情报》。

### 第 3 步：防砖筑底与前置快照固化 (Snapshot)
* 固化初始状态快照：`python scripts/snapshot_engine.py --create`
* 告知用户快照已建立（快照 ID），承诺随时可输入【恢复默认】一键秒级还原。

### 第 4 步：双层融合方案呈现与用户确认 (Recommend & Confirm)
* 呈现【A. 通用稳健优化项】+【B. 本机型专属定制优化项】；
* 明确列出各项改动，等待用户确认执行。

### 第 5 步：渐进式梯度执行 (Execute)
* 按照安全梯度执行：
  1. 动效比例 0.75x、全局高刷锁定、cgroup 进程墓碑激活；
  2. 核心应用 AOT Speed-Profile 预编译；
  3. UFS 闪存 FSTRIM 修剪；
  4. (已 Root 路径) 音量步进细化为 30 级、清除 BMS 阻抗记忆；
  5. (已 Root 路径) 根据用户选择清理失效改机模块。

### 第 6 步：输出前后量化报告与回滚凭证 (Report)
* 重新读取数据，输出优化前后对比表；
* 告知用户回滚承诺：“随时回复【恢复默认】即可原样还原”。
