#!/usr/bin/env python3
"""
系统状态采集脚本：采集5秒内5次数据并输出平均值（JSON格式）
依赖：psutil（自动通过uv安装）
"""
# /// script
# requires-python = ">=3.8"
# dependencies = ["psutil"]
# ///

import json
import time
import psutil
import platform
import subprocess
import sys

def get_top_cpu_processes(limit=5):
    """获取CPU使用率最高的进程"""
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            # 首次调用cpu_percent需要一定时间累积，设置较短等待
            cpu = p.cpu_percent(interval=0.1)
            if cpu > 0:
                processes.append({
                    'pid': p.info['pid'],
                    'name': p.info['name'],
                    'cpu_percent': round(cpu, 1)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # 按CPU使用率排序，取前N个
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:limit]


def get_top_mem_processes(limit=5):
    """获取内存使用率最高的进程"""
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
        try:
            mem_percent = p.info['memory_percent']
            if mem_percent and mem_percent > 0:
                # 获取内存信息用于展示 RSS
                mem_info = p.info['memory_info']
                rss_mb = mem_info.rss / 1024**2 if mem_info else 0
                processes.append({
                    'pid': p.info['pid'],
                    'name': p.info['name'],
                    'mem_percent': round(mem_percent, 1),
                    'rss_mb': round(rss_mb, 1)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # 按内存使用率排序，取前N个
    processes.sort(key=lambda x: x['mem_percent'], reverse=True)
    return processes[:limit]

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
    N = 5
    INTERVAL = 1.0  # 每次间隔1秒，共5次 = 5秒

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

    # 获取CPU使用最高的进程
    top_cpu_processes = get_top_cpu_processes(limit=5)
    # 获取内存使用最高的进程
    top_mem_processes = get_top_mem_processes(limit=5)

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
        "top_cpu_processes": top_cpu_processes,
        "top_mem_processes": top_mem_processes,
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
