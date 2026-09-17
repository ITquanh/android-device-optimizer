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

## 🤖 AI Agent 自动化集成与调用规范 (AI Agent Integration Runbook)

### 1. 触发意图与意图识别 (Intent Recognition)
当用户输入包含以下意图时，AI Agent 应自主激活并调用本 Skill：
- **设备调优与提速**：“帮我优化这台安卓机”、“HyperOS/MIUI 用久了很卡”、“车机/电视盒子响应慢”。
- **电池与续航**：“电池虚标怎么校准”、“如何释放被系统锁住的电池容量”、“优化后台耗电”。
- **显示与音质**：“如何强制锁定全局 120Hz 高刷”、“提升蓝牙耳机/外放音质”、“微调音量阶梯”。
- **系统恢复与回滚**：“还原之前的优化”、“恢复默认安卓设置”。

### 2. AI Agent 决策状态机 (State Machine)
AI Agent 在对话中必须维护以下状态转移，切勿跳步：

```
[DISCOVERY] ──> [INSPECT] ──> [SNAPSHOT (必须)] ──> [PLAN & CONFIRM] ──> [EXECUTE] ──> [REPORT & PROOF]
      │                                                                               ▲
      └────────────────────────── 用户回复【恢复默认】 ────────────────────────────────┘
```

### 3. Agent 与用户的交互输出模板

#### A. 体检阶段输出：《全维设备体检报告卡》
Agent 执行 `python scripts/device_inspector.py` 后，向用户输出结构化 Markdown 表格，包含：
- **设备身份**：品牌、机型、SoC、Android 版本、ROM 定制层
- **Root 与提权状态**：Non-Root (ADB) / Root (KernelSU/Magisk/APatch)
- **电池 BMS 健康度**：设计容量、当前满充学得容量、健康度百分比、阻抗状态
- **核心瓶颈预警**：例如“存在多余动画延迟”、“高刷策略存在黑名单降频”

#### B. 确认阶段输出：《梯度优化方案建议书》
Agent 必须向用户明确标示：
- **A. 通用免 Root 稳健方案**（0 风险，0.75x 动效 + 全局高刷 + 进程墓碑 + AOT 预编译 + 存储 Trim）
- **B. 极客 Root 专属方案**（BMS 阻抗重置 + 30 级音量平滑）
- **安全承诺语**：“已为您生成初始快照 ID: `[SNAPSHOT_ID]`，后续随时输入【恢复默认】即可原样复原。”

#### C. 回滚阶段：无条件逆向复原
用户输入“恢复默认”、“回滚”、“还原”时，Agent 立即无缝调用：
```bash
python scripts/snapshot_engine.py --rollback
```

---

## 📋 标准 6 步 SOP 执行工作流

### 第 1 步：连接与握手 (Connect)
* 检查已有设备：`python scripts/adb_connector.py --devices`
* 若为无线 ADB 初次配对：`python scripts/adb_connector.py --pair-and-connect <IP> <PAIR_PORT> <CODE>`

### 第 2 步：非侵入体检与全网机型方案检索 (Inspect & Search)
* 执行全维体检：`python scripts/device_inspector.py`
* 采集芯片架构、BMS 物理电池数据；
* 运行机型智能分析：`python scripts/model_intelligence.py`。

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
