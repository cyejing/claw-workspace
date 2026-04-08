---
name: system-monitor
description: 系统状态监控技能。当用户说"查看系统情况"、"查看系统状态"、"系统监控"、"查看CPU/内存/磁盘"、"系统健康检查"时触发。采集5秒内5次数据取峰值（最大值），输出格式化的系统状态报告（CPU、内存、负载、磁盘、网络、温度）。
version: "1.0"
---

# System Monitor — 系统状态监控

## 执行脚本

运行采集脚本（uv 自动管理 psutil 依赖）：

```bash
uv run <SKILL_DIR>/scripts/collect_stats.py
```

## 输出格式（固定模板）

采集完成后，按以下模板输出给用户：

---

## 🖥️ 系统状态报告
> 采集时间：`<当前时间>` | 采样：5次 / 5秒峰值

### 📊 CPU
- **使用率：** `<cpu_percent>%` `████░░░░░░░` `<level>`
- **物理核心：** `<cpu_count_physical>` 核 | **逻辑核心：** `<cpu_count>` 个
- **温度：** `<temp_celsius>°C`

### 💾 内存
- **使用率：** `<mem_percent>%` `███████░░░` `<level>`
- **已用 / 总计：** `<mem_used_gb> GB` / `<mem_total_gb> GB`
- **可用：** `<mem_available_gb> GB`

### 🔄 交换分区
- **使用率：** `<swap_percent>%`
- **已用 / 总计：** `<swap_used_gb> GB` / `<swap_total_gb> GB`

### ⚖️ 系统负载（Load Average）
- **1分钟：** `<load_1>` `▓▓░░░`（< 核心数=正常）
- **5分钟：** `<load_5>`
- **15分钟：** `<load_15>`

### 💿 磁盘（根分区 /）
- **使用率：** `<disk_percent>%` `█████░░░░░` `<level>`
- **已用 / 总计：** `<disk_used_gb> GB` / `<disk_total_gb> GB`
- **可用：** `<disk_free_gb> GB`

### 🌐 网络（实时速率）
- **下载：** `<net_rx_mbps>` MB/s
- **上传：** `<net_tx_mbps>` MB/s

---

## 使用率等级说明

| 使用率区间 | 等级 | 颜色/标注 |
|-----------|------|----------|
| 0-50% | ✅ 正常 | 绿色 |
| 50-75% | ⚠️ 偏高 | 黄色 |
| 75-90% | 🔶 警告 | 橙色 |
| 90-100% | 🔴 危险 | 红色 |

## 注意事项

- 如果 `temp_celsius` 为 `null`，说明平台不支持温度读取（跳过温度行）
- 负载（load_1）判断标准：高于逻辑核心数表示负载偏高
- 网络速率为采集末次1秒内的瞬时值，仅供参考
