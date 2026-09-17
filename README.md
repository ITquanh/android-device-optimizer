# 🚀 Android Device Optimizer (安卓全场景全维调优中枢)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Android](https://img.shields.io/badge/Android-5.0%20~%2016%2B-green.svg)](https://www.android.com/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Antigravity Skill](https://img.shields.io/badge/Agent%20Skill-Ready-purple.svg)](https://github.com/ITquanh/android-device-optimizer)

**Android Device Optimizer** 是一款专为 Android 全版本 (Android 5.0 ~ 16+) 与多形态设备（手机、平板、电视、车机）打造的通用设备调优与诊断中枢。

支持 **HyperOS / MIUI、OriginOS、ColorOS、Flyme、EMUI / HarmonyOS、One UI 以及 AOSP / 类原生 ROM**。提供免 Root 稳健通道与极客 Root 通道双轨架构，涵盖六大支柱：**【性能 · 音质 · 电池 · 屏幕 · 网络 · 存储】**，并秉承**100% 初始快照防变砖安全准则**。

---

## ✨ 核心特性

- 🛡️ **防变砖绝对第一 (Zero-Risk Guarantee)**：执行任何变更前，自动通过 `snapshot_engine.py` 生成全量快照，任何时候输入回滚命令即可一键秒级 100% 逆向复原系统状态。
- ⚡ **双轨优化管线 (Dual Pipeline)**：
  - **免 Root 稳健通道 (Non-Root)**：通过标准有线 / 无线 ADB，安全修改系统属性、动效曲线、全局高刷、cgroup 进程墓碑、ART AOT 预编译与闪存修剪。
  - **极客 Root 通道 (KernelSU / Magisk / APatch)**：深入硬件底层，重置 BMS 阻抗学习记录释放虚标锁容、平滑 30 级音量阶梯、清除残留冲突模块。
- 🔍 **机型智能指纹与社区方案检索 (Model Intelligence)**：自动提取 SoC 架构、代号指纹与系统版本，检索酷安与 XDA 针对特定机型的成熟调优参数。
- 🤖 **AI Agent Skill 原生兼容**：自带标准 `SKILL.md`，可无缝接入 Claude、ChatGPT、Google Antigravity 等 AI 编程助手与自动化代理系统。

---

## 🛠️ 模块架构与工具箱索引

```
android-device-optimizer/
├── SKILL.md                     # AI Agent Skill 规则定义文件
├── README.md                    # 项目完整说明文档
├── LICENSE                      # MIT 开源协议
├── requirements.txt             # 环境说明（无第三方重型依赖）
├── references/                  # 参考指南与应急规范
│   ├── anti_brick_rules.md      # 防变砖核心准则与生命线包名白名单
│   └── bms_calibration_sop.md   # BMS 电池循环校准标准操作规程
└── scripts/                     # 调优核心执行引擎
    ├── adb_connector.py         # 有线/无线 ADB 配对连接与端口嗅探
    ├── device_inspector.py      # 六维硬件、系统、BMS、Root 体检
    ├── model_intelligence.py    # 提取机型指纹与方案智能分析
    ├── snapshot_engine.py       # 状态快照固化与一键安全复原引擎
    ├── system_tuner.py          # 动效、高刷、墓碑、AOT、FSTRIM
    ├── audio_tuner.py           # Hi-Res 直通、30 级平滑音量步进
    └── battery_tuner.py         # BMS 阻抗清除、锁容释放、Doze 深度休眠
```

### 核心脚本职责一览

| 脚本文件 | 核心职责 | 典型调用命令 |
| :--- | :--- | :--- |
| `adb_connector.py` | 原生有线 / 无线 ADB 连接与端口嗅探 | `python scripts/adb_connector.py --devices` |
| `device_inspector.py` | 六维硬件、系统、SoC、BMS 电池、Root 状态体检 | `python scripts/device_inspector.py` |
| `model_intelligence.py` | 提取机型代号指纹，分析酷安/XDA成熟方案 | `python scripts/model_intelligence.py` |
| `snapshot_engine.py` | 导出初始状态快照 / 一键 100% 逆向复原 | `python scripts/snapshot_engine.py --create` |
| `system_tuner.py` | 进程墓碑、0.75x 动效、全局高刷、AOT 预编译、FSTRIM | `python scripts/system_tuner.py --apply-all` |
| `audio_tuner.py` | Hi-Res 直通、30 级平滑音量步进、SmartPA 增益检查 | `python scripts/audio_tuner.py --tune-volume-steps` |
| `battery_tuner.py` | BMS 阻抗学习记录重置、锁容释放、Doze 深度休眠 | `python scripts/battery_tuner.py --reset-bms` |

---

## 📋 标杆 6 步 SOP 执行工作流

1. **连接与握手 (Connect)**：检测已有 ADB 设备或进行无线 ADB 配对。
2. **非侵入体检 (Inspect)**：采集芯片架构、BMS 物理电池健康度，输出《设备体检报告》。
3. **防砖筑底与快照 (Snapshot)**：导出全量初始状态快照，生成回滚凭证 ID。
4. **方案呈现与确认 (Confirm)**：展示【通用稳健项】+【机型专属项】，确认后渐进下发。
5. **梯度安全执行 (Execute)**：从系统动效、进程墓碑、AOT 编译到深度电池校准梯度生效。
6. **前后对比与报告 (Report)**：生成量化前后对比表，留存一键回滚凭据。

---

## 🚀 快速上手

### 前置要求
- Python 3.8+
- 安装 Android Platform Tools（确保 `adb` 命令在系统的 PATH 环境变量中）
- Android 设备开启【开发者选项】中的【USB 调试】（如需修改系统设置，小米设备需开启【USB 调试(安全设置)】）

### 常用命令

```bash
# 1. 检查已连接设备
python scripts/adb_connector.py --devices

# 2. 执行设备全维体检
python scripts/device_inspector.py

# 3. 创建执行前初始快照
python scripts/snapshot_engine.py --create

# 4. 执行全套稳健调优（0.75x动效 / 全局高刷 / cgroup墓碑 / FSTRIM）
python scripts/system_tuner.py --apply-all

# 5. 如有需要，一键逆向回滚到初始状态
python scripts/snapshot_engine.py --rollback
```

---

## 🛡️ 安全承诺与免责声明

- 本项目包含严格的包名生命线白名单保护（见 `references/anti_brick_rules.md`），任何对系统核心进程的破坏性操作均被强制阻断。
- 涉及 Root 特权操作请确保电量高于 50% 并知悉相关原理。
- 软件基于 MIT License 开源，开发者对极端不可抗力原因造成的数据损失不承担连带责任。

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源发布。
欢迎提交 Issue 和 Pull Request 完善各类特定 ROM 机型的调优方案！
