---
name: proxy-log-analyzer
description: "Analyze proxy logs to extract domains from Connect to patterns. When user asks to view proxy log network requests, extract and display new domains; when user asks to view known domains, display all recorded domains. Supports incremental detection and deduplication."
---

# Proxy Log Analyzer

## Overview

分析 Shuttle 代理日志中的网络连接请求，提取目标域名并跟踪新增请求。自动过滤已知域名，仅展示新增连接，实现增量监控。

## Quick Start

使用 `scripts/analyze_log.py` 脚本进行日志分析，脚本提供确定性的执行结果。

## Usage Scenarios

### 查看代理日志网络请求情况

触发条件：用户说"查看代理日志网络请求情况"或类似表达

**执行脚本：**

```bash
uv run /home/clawd/.openclaw/workspace/skills/proxy-log-analyzer/scripts/analyze_log.py new
```

**脚本功能：**
- 从 `/home/clawd/rp/shuttle/logs/app.log` 提取所有 `Http Connect to:` 和 `Socks Connect to:` 格式的域名
- 读取 `/home/clawd/rp/shuttle/logs/known_domains.txt`（文件不存在时视为空）
- 对比并找出新增域名
- 展示新增域名列表
- 自动追加新域名到 `known_domains.txt`（去重）

**示例输出：**

```
本次检测到新增域名：
- api.example.com
- cdn.example.org

共 2 个域名
已追加到 /home/clawd/rp/shuttle/logs/known_domains.txt
```

### 查看已知域名

触发条件：用户说"查看已知的"或类似表达

**执行脚本：**

```bash
uv run /home/clawd/.openclaw/workspace/skills/proxy-log-analyzer/scripts/analyze_log.py known
```

**脚本功能：**
- 读取并展示所有已记录域名

**示例输出：**

```
已记录域名列表：
- api.example.com
- cdn.example.org
- static.example.net

共 3 个域名
```

## Files

- **日志文件**: `/home/clawd/rp/shuttle/logs/app.log` - Shuttle 代理日志
- **域名记录**: `/home/clawd/rp/shuttle/logs/known_domains.txt` - 已知域名列表（每行一个）

## Script Details

脚本位置：`scripts/analyze_log.py`

**可用参数：**
- `new` - 查看新增域名并更新记录
- `known` - 查看所有已记录域名

**特性：**
- 使用 Python 正则表达式精确匹配域名
- 自动去重
- 字母顺序排序输出
- 自动创建目录和文件
- 错误处理和提示
