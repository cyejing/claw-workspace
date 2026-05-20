#!/usr/bin/env python3
"""
轻量级浏览器状态检查脚本（不重启）。
检查 Chrome 进程、bb-browser daemon 健康状态、知乎抓取链路。
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
RESULT = {
    "chrome_ok": False,
    "daemon_ok": False,
    "daemon_cdp_connected": False,
    "zhihu_ok": False,
    "zhihu_count": 0,
    "zhihu_error": None,
    "sample_titles": [],
    "message": "",
}


def run_cmd(cmd: list[str], timeout: int = 15) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout}s"
    except Exception as e:
        return -1, "", str(e)


def check_chrome() -> bool:
    """检查 Chrome 进程是否存在"""
    rc, out, err = run_cmd(["pgrep", "-f", "/opt/google/chrome/chrome"])
    chrome_ok = rc == 0
    RESULT["chrome_ok"] = chrome_ok
    return chrome_ok


def check_daemon() -> tuple[bool, bool]:
    """检查 bb-browser daemon 健康状态"""
    rc, out, err = run_cmd(["bb-browser", "daemon", "status"])
    daemon_ok = rc == 0
    cdp_connected = False
    if daemon_ok:
        for line in out.splitlines():
            if "CDP connected:" in line:
                cdp_connected = "yes" in line.lower()
                break
    RESULT["daemon_ok"] = daemon_ok
    RESULT["daemon_cdp_connected"] = cdp_connected
    return daemon_ok, cdp_connected


def check_zhihu() -> tuple[bool, int, list, str | None]:
    """
    执行 bb-browser site zhihu/hot --json，验证知乎抓取。
    通过临时文件读取 JSON 输出，避免 stdout 混入非 JSON 内容。
    """
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        tmp_path = f.name

    rc, out, err = run_cmd(
        ["bb-browser", "site", "zhihu/hot", "--json", "--output", tmp_path],
        timeout=30,
    )

    # 如果 --output 不支持，fallback 到 stdout 解析
    if rc == 0 and Path(tmp_path).exists() and Path(tmp_path).stat().st_size > 0:
        try:
            with open(tmp_path, "r") as f:
                raw = f.read()
            Path(tmp_path).unlink(missing_ok=True)
            data = json.loads(raw)
        except (json.JSONDecodeError, FileNotFoundError):
            data = None
    else:
        # fallback: 尝试从 stdout 解析
        Path(tmp_path).unlink(missing_ok=True)
        raw = out.strip()
        # bb-browser 可能在 JSON 前后输出版本/banner 信息，尝试提取 JSON 部分
        try:
            # 找到第一个 '{' 到最后一个 '}'
            start = raw.index("{")
            end = raw.rindex("}") + 1
            data = json.loads(raw[start:end])
        except (ValueError, json.JSONDecodeError):
            data = None

    if data is None:
        err_msg = (err or out or "No output")[:300]
        return False, 0, [], f"无法解析知乎返回: {err_msg}"

    # 支持两种格式: {"success":true,"data":{"items":[...]}} 或 直接是数组
    if isinstance(data, dict):
        items = data.get("data", {}).get("items", [])
    else:
        items = data if isinstance(data, list) else []

    count = len(items)
    titles = [item.get("title", "")[:50] for item in (items[:3]) if isinstance(item, dict)]
    ok = count > 0
    return ok, count, titles, None


def main():
    print("🔍 开始检查浏览器状态...\n")

    # 1. Chrome 进程
    chrome_ok = check_chrome()
    print(f"  Chrome 进程: {'✅ 存在' if chrome_ok else '❌ 不存在'}")

    # 2. daemon 状态
    daemon_ok, cdp_connected = check_daemon()
    print(f"  bb-browser daemon: {'✅ 运行中' if daemon_ok else '❌ 未运行'}")
    print(f"  CDP 连接: {'✅ 已连接' if cdp_connected else '❌ 未连接'}")

    # 3. 知乎抓取
    zhihu_ok, zhihu_count, sample_titles, zhihu_error = check_zhihu()
    RESULT["zhihu_ok"] = zhihu_ok
    RESULT["zhihu_count"] = zhihu_count
    RESULT["sample_titles"] = sample_titles
    RESULT["zhihu_error"] = zhihu_error

    if zhihu_ok:
        print(f"  知乎抓取: ✅ 成功（{zhihu_count} 条）")
        if sample_titles:
            print("  示例标题:")
            for t in sample_titles:
                print(f"    - {t}")
    else:
        print(f"  知乎抓取: ❌ 失败 - {zhihu_error}")

    # 汇总
    all_ok = chrome_ok and daemon_ok and cdp_connected and zhihu_ok
    RESULT["message"] = (
        "浏览器状态正常，知乎抓取链路完整" if all_ok
        else "浏览器存在异常，请检查上述问题"
    )

    print("\n--- 结果汇总 ---")
    print(json.dumps(RESULT, ensure_ascii=False, indent=2))
    print(f"\n{RESULT['message']}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
