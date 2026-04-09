#!/usr/bin/env python3
"""
系统状态采集脚本：采集数据并输出报告
依赖：psutil（已安装于系统）
"""

import json
import time
import psutil
import platform
import subprocess
import sys

def get_top_processes(limit=5, threshold=5.0):
    """获取 CPU 或内存任一超过阈值的进程，去重后按消耗程度综合排序，取前N个"""
    processes = {}
    # 先拿 CPU
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = p.cpu_percent(interval=0.1)
            if cpu > 0:
                pid = p.info['pid']
                processes[pid] = processes.get(pid, {'pid': pid, 'name': p.info['name'], 'cpu_percent': 0.0, 'mem_percent': 0.0, 'rss_mb': 0.0})
                processes[pid]['cpu_percent'] = round(cpu, 1)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # 再拿内存（可能和上面重叠）
    for p in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
        try:
            mem_percent = p.info['memory_percent']
            if mem_percent and mem_percent > 0:
                pid = p.info['pid']
                mem_info = p.info['memory_info']
                rss_mb = mem_info.rss / 1024**2 if mem_info else 0
                if pid not in processes:
                    processes[pid] = {'pid': pid, 'name': p.info['name'], 'cpu_percent': 0.0, 'mem_percent': round(mem_percent, 1), 'rss_mb': round(rss_mb, 1)}
                else:
                    processes[pid]['mem_percent'] = round(mem_percent, 1)
                    processes[pid]['rss_mb'] = round(rss_mb, 1)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # 过滤：CPU > threshold 或 内存 > threshold
    filtered = [v for v in processes.values() if v['cpu_percent'] > threshold or v['mem_percent'] > threshold]
    # 按 max(cpu, mem) 排序
    filtered.sort(key=lambda x: max(x['cpu_percent'], x['mem_percent']), reverse=True)
    return filtered[:limit]

def get_temps():
    """获取CPU温度（支持多平台）"""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        # 优先取 coretemp / k10temp / cpu_thermal
        for key in ("coretemp", "k10temp", "cpu_thermal", "acpitz"):
            if key in temps:
                entries = temps[key]
                vals = [e.current for e in entries if e.current and e.current > 0]
                if vals:
                    return sum(vals) / len(vals)
        # fallback: 取第一个有效值
        for entries in temps.values():
            vals = [e.current for e in entries if e.current and e.current > 0]
            if vals:
                return sum(vals) / len(vals)
    except Exception:
        pass
    return None

def get_net_speed(interval=1.0):
    """计算网络速率（bytes/s）"""
    n1 = psutil.net_io_counters()
    time.sleep(interval)
    n2 = psutil.net_io_counters()
    elapsed = interval
    rx = (n2.bytes_recv - n1.bytes_recv) / elapsed
    tx = (n2.bytes_sent - n1.bytes_sent) / elapsed
    return rx, tx

def sample_once():
    """采集一次快照（不含网速，网速单独计算）"""
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    load = psutil.getloadavg()  # 1/5/15 min
    disk = psutil.disk_usage("/")
    temp = get_temps()
    return {
        "cpu_percent": cpu,
        "mem_percent": mem.percent,
        "mem_used_gb": mem.used / 1024**3,
        "mem_total_gb": mem.total / 1024**3,
        "mem_available_gb": mem.available / 1024**3,
        "swap_percent": swap.percent,
        "swap_used_gb": swap.used / 1024**3,
        "swap_total_gb": swap.total / 1024**3,
        "load_1": load[0],
        "load_5": load[1],
        "load_15": load[2],
        "disk_percent": disk.percent,
        "disk_used_gb": disk.used / 1024**3,
        "disk_total_gb": disk.total / 1024**3,
        "disk_free_gb": disk.free / 1024**3,
        "temp_celsius": temp,
    }

def main():
    N = 5  # 5次采样取峰值
    INTERVAL = 1.0  # 每次间隔1秒，共5秒

    # 先初始化CPU采集（第一次调用interval=None需要先调用一次）
    psutil.cpu_percent(interval=0.1)

    samples = []
    for i in range(N):
        s = sample_once()
        samples.append(s)
        if i < N - 1:
            time.sleep(INTERVAL)

    # 计算网络速率（最后1秒）
    rx_bps, tx_bps = get_net_speed(interval=1.0)

    # 最大值
    def maxv(key):
        vals = [s[key] for s in samples if s[key] is not None]
        return max(vals) if vals else None

    # 获取高消耗进程（CPU或内存 > 5%）
    top_processes = get_top_processes(limit=5, threshold=5.0)

    result = {
        "cpu_percent": maxv("cpu_percent"),
        "mem_percent": maxv("mem_percent"),
        "mem_used_gb": maxv("mem_used_gb"),
        "mem_total_gb": samples[0]["mem_total_gb"],
        "mem_available_gb": min([s["mem_available_gb"] for s in samples if s["mem_available_gb"] is not None]),  # 可用取最小
        "swap_percent": maxv("swap_percent"),
        "swap_used_gb": maxv("swap_used_gb"),
        "swap_total_gb": samples[0]["swap_total_gb"],
        "load_1": maxv("load_1"),
        "load_5": maxv("load_5"),
        "load_15": maxv("load_15"),
        "disk_percent": maxv("disk_percent"),
        "disk_used_gb": maxv("disk_used_gb"),
        "disk_total_gb": samples[0]["disk_total_gb"],
        "disk_free_gb": min([s["disk_free_gb"] for s in samples if s["disk_free_gb"] is not None]),  # 剩余取最小
        "temp_celsius": maxv("temp_celsius"),
        "net_rx_mbps": rx_bps / 1024**2,
        "net_tx_mbps": tx_bps / 1024**2,
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "platform": platform.system(),
        "samples": N,
        "top_processes": top_processes,
    }

    # 格式化输出报告
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def level(pct):
        if pct < 50: return "✅ 正常"
        if pct < 75: return "⚠️ 偏高"
        if pct < 90: return "🔶 警告"
        return "🔴 危险"
    
    def bar(pct, total=10):
        filled = int(pct / 100 * total)
        return "█" * filled + "░" * (total - filled)
    
    cpu = result["cpu_percent"]
    mem = result["mem_percent"]
    
    report = f"""## 🖥️ 系统状态报告
> 采集时间：`{now}` | 采样：5次 / 5秒峰值

### 📊 CPU
- **使用率：** `{cpu:.1f}%` `{bar(cpu)}` {level(cpu)}
- **物理核心：** `{result['cpu_count_physical']}` 核 | **逻辑核心：** `{result['cpu_count']}` 个
- **温度：** `{result['temp_celsius']:.1f}°C`

### 💾 内存
- **使用率：** `{mem:.1f}%` `{bar(mem)}` {level(mem)}
- **已用 / 总计：** `{result['mem_used_gb']:.1f} GB` / `{result['mem_total_gb']:.1f} GB`
- **可用：** `{result['mem_available_gb']:.1f} GB`

### 🔄 交换分区
- **使用率：** `{result['swap_percent']:.1f}%`
- **已用 / 总计：** `{result['swap_used_gb']:.2f} GB` / `{result['swap_total_gb']:.2f} GB`

### ⚖️ 系统负载（Load Average）
- **1分钟：** `{result['load_1']:.2f}` {'✅' if result['load_1'] < result['cpu_count'] else '⚠️'}（< {result['cpu_count']}核=正常）
- **5分钟：** `{result['load_5']:.2f}`
- **15分钟：** `{result['load_15']:.2f}`

### 💿 磁盘（根分区 /）
- **使用率：** `{result['disk_percent']:.1f}%` `{bar(result['disk_percent'])}` {level(result['disk_percent'])}
- **已用 / 总计：** `{result['disk_used_gb']:.1f} GB` / `{result['disk_total_gb']:.1f} GB`
- **可用：** `{result['disk_free_gb']:.1f} GB`

### 🌐 网络（实时速率）
- **下载：** `{result['net_rx_mbps']:.2f} MB/s`
- **上传：** `{result['net_tx_mbps']:.3f} MB/s`

"""
    
    # 高消耗进程
    if result["top_processes"]:
        report += "### 🔥 高消耗进程 Top 5（阈值: CPU>5% 或 内存>5%）\n"
        for i, p in enumerate(result["top_processes"], 1):
            report += f"""{i}. {p['name']} (PID: {p['pid']})
    CPU: {p['cpu_percent']:.1f}% | 内存: {p['mem_percent']:.1f}% ({p['rss_mb']:.0f} MB)

"""
    else:
        report += "### 🔥 高消耗进程 Top 5\n无高消耗进程（CPU/内存均 < 5%）\n\n"
    
    print(report, flush=True)

if __name__ == "__main__":
    main()
    import os
    os._exit(0)
