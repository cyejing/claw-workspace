#!/usr/bin/env python3
"""
Proxy Log Analyzer - 提取并分析代理日志中的域名
"""

import re
import sys
from pathlib import Path
from typing import List, Set


def extract_domains_from_log(log_file: Path) -> Set[str]:
    """从日志文件中提取所有域名"""
    domains = set()

    if not log_file.exists():
        print(f"日志文件不存在: {log_file}", file=sys.stderr)
        return domains

    # 匹配 Http Connect to: 或 Socks Connect to: 格式
    pattern = re.compile(r'(?:Http|Socks) Connect to: ([^:]+)')

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                domain = match.group(1).strip()
                if domain:
                    domains.add(domain)

    return domains


def load_known_domains(known_file: Path) -> Set[str]:
    """加载已知域名列表"""
    domains = set()

    if known_file.exists():
        with open(known_file, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                if domain:
                    domains.add(domain)

    return domains


def save_known_domains(domains: List[str], known_file: Path) -> None:
    """保存域名列表到文件"""
    known_file.parent.mkdir(parents=True, exist_ok=True)

    with open(known_file, 'w', encoding='utf-8') as f:
        for domain in domains:
            f.write(f"{domain}\n")


def show_new_domains():
    """查看新增域名"""
    log_file = Path("/home/clawd/rp/shuttle/logs/app.log")
    known_file = Path("/home/clawd/rp/shuttle/logs/known_domains.txt")

    # 提取当前日志中的所有域名
    current_domains = extract_domains_from_log(log_file)

    if not current_domains:
        print("日志中没有发现任何域名连接")
        return

    # 加载已知域名
    known_domains = load_known_domains(known_file)

    # 找出新增域名
    new_domains = sorted(current_domains - known_domains)

    if not new_domains:
        print("未发现新增域名")
        return

    # 展示新增域名
    print("本次检测到新增域名：")
    for domain in new_domains:
        print(f"- {domain}")

    print(f"\n共 {len(new_domains)} 个域名")

    # 追加新域名到已知域名列表
    all_domains = sorted(known_domains | current_domains)
    save_known_domains(all_domains, known_file)

    print(f"已追加到 {known_file}")


def show_known_domains():
    """查看所有已知域名"""
    known_file = Path("/home/clawd/rp/shuttle/logs/known_domains.txt")

    if not known_file.exists():
        print("暂无已记录域名")
        return

    known_domains = load_known_domains(known_file)

    if not known_domains:
        print("暂无已记录域名")
        return

    sorted_domains = sorted(known_domains)

    print("已记录域名列表：")
    for domain in sorted_domains:
        print(f"- {domain}")

    print(f"\n共 {len(sorted_domains)} 个域名")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 analyze_log.py <new|known>")
        print("  new   - 查看新增域名")
        print("  known - 查看已知域名")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "new":
        show_new_domains()
    elif command == "known":
        show_known_domains()
    else:
        print(f"未知命令: {command}", file=sys.stderr)
        print("有效命令: new, known", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
