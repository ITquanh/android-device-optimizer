# 防变砖四大铁律与核心白名单安全标准

### 1. 防变砖四大防御铁律
1. **铁律一【执行前全量快照 (Snapshot)】**：任何修改执行前，必须自动落盘生成 `snapshot_<timestamp>.json`。
2. **铁律二【Root 路径救砖熔断前置 (Bootloop Protector)】**：执行内核敏感修改前，强检救砖模块。连续 3 次开机未进桌面自动在底层禁用全部模块。
3. **铁律三【免 Root 纯净沙盒隔离】**：仅走官方开放的 `settings` 与 `cmd package`，物理杜绝破坏启动引导链。
4. **铁律四【核心生命线禁动绝对白名单】**：硬编码拦截器强制拒绝任何涉及核心组件的禁用或删除指令。

### 2. 绝对受保护的核心生命线包名
* `android` (framework-res 框架基石)
* `com.android.systemui` (系统界面 / 状态栏 / 导航栏)
* `com.android.settings` & `com.android.providers.settings` (系统设置与数据源)
* `com.android.keyguard` (锁屏中心)
* `com.android.phone` & `com.android.server.telecom` (基带电话)
* `com.android.packageinstaller` (应用包安装解析器)
* **厂商核心生命线**：小米 `com.xiaomi.joyose` (狂暴引擎FEAS通信底层，删后必锁60帧)、`com.miui.home`；vivo `com.bbk.launcher2`；OPPO `com.oppo.launcher`
