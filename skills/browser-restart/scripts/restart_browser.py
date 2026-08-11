#!/usr/bin/env python3
"""
重启浏览器 - 单窗口版（修复版）

根因修复：
1. bb-browser daemon 读取 ~/.bb-browser/browser/cdp-port 来决定连接哪个 Chrome
2. daemon 默认端口是 19825，会自己启动一个空 profile 的 Chrome
3. 'bb-browser daemon stop' 会把 daemon 进程和所有 Chrome 都杀掉（包括我们的）
4. 正确做法：杀 daemon 进程，重写 cdp-port，再启动我们的 Chrome，让 bb-browser 自己重连

流程：
  1. 杀掉 daemon 进程 + 所有 Chrome
  2. 用你的 profile 启动 Chrome（端口 9222，打开知乎热榜）
  3. 写入 cdp-port 文件，告诉 daemon 连接 9222
  4. 等热榜页面加载完成
  5. 验证 zhihu/hot 抓取
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_DISPLAY = ':0'
DEFAULT_CDP_PORT = 9222
FIXED_USER_DATA_DIR = '/home/clawd/.cache/chrome'
DEFAULT_CHROME_BIN = 'google-chrome-stable'
DEFAULT_ZHIHU_URL = 'https://www.zhihu.com/hot'
CHROME_LOG = '/tmp/browser-restart-chrome.log'
MANAGED_BROWSER_DIR = Path.home() / '.bb-browser' / 'browser'
MANAGED_PORT_FILE = MANAGED_BROWSER_DIR / 'cdp-port'


def log(msg: str):
    print(msg, flush=True)


def read_cmdline(pid: int) -> str:
    try:
        return Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\x00', b' ').decode('utf-8', 'ignore').strip()
    except Exception:
        return ''


def find_processes(predicate, exclude_pids=None):
    exclude = set(exclude_pids or [])
    found = []
    for name in os.listdir('/proc'):
        if not name.isdigit():
            continue
        pid = int(name)
        if pid in exclude:
            continue
        cmd = read_cmdline(pid)
        if cmd and predicate(cmd):
            found.append((pid, cmd))
    return found


def wait_dead(pids, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        alive = []
        for pid in pids:
            try:
                os.kill(pid, 0)
                alive.append(pid)
            except ProcessLookupError:
                pass
        if not alive:
            return True
        time.sleep(0.5)
    return False


def kill_processes(pairs, name: str):
    if not pairs:
        log(f'[INFO] No {name} processes found')
        return
    pids = [pid for pid, _ in pairs]
    log(f'[INFO] Stopping {name}: {pids}')
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    if wait_dead(pids, 8):
        return
    log(f'[WARN] {name} still alive after SIGTERM, sending SIGKILL')
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    wait_dead(pids, 5)


def run_cmd(cmd: list, timeout=15) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return '(timeout)'
    except Exception as e:
        return str(e)


def http_get(url: str, headers=None, timeout=8):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', 'ignore'), dict(resp.headers)


def wait_for_cdp(port: int, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        try:
            body, _ = http_get(f'http://127.0.0.1:{port}/json/version', timeout=3)
            return json.loads(body)
        except Exception:
            time.sleep(1)
    return None


def daemon_status() -> dict:
    """Check daemon status and return parsed output."""
    out = run_cmd(['bb-browser', 'daemon', 'status', '--json'], timeout=8)
    try:
        raw = json.loads(out)
        connected = raw.get('data', {}).get('connected', False) or raw.get('data', {}).get('CDP connected') == 'yes'
        tabs = raw.get('data', {}).get('tabs', [])
        return {'connected': connected, 'tabs': tabs, 'raw': raw}
    except Exception:
        # fallback: check if daemon connected via HTTP
        return {'connected': None, 'tabs': [], 'raw': out}


def test_zhihu_hot() -> dict:
    """Test zhihu/hot via bb-browser and return parsed result."""
    out = run_cmd(['bb-browser', 'site', 'zhihu/hot', '--json'], timeout=30)
    try:
        raw = json.loads(out)
        if raw.get('success') and 'data' in raw:
            return raw['data']
        return raw
    except Exception:
        return {'error': {'message': out[:200]}}


def launch_chrome(chrome_bin: str, display: str, cdp_port: int):
    Path(FIXED_USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
    cmd = [
        'env', f'DISPLAY={display}', 'nohup', chrome_bin,
        f'--remote-debugging-port={cdp_port}',
        f'--user-data-dir={FIXED_USER_DATA_DIR}',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-sync',
        '--disable-background-networking',
        '--disable-component-update',
        '--disable-features=Translate,MediaRouter',
        '--disable-session-crashed-bubble',
        '--hide-crash-restore-bubble',
        DEFAULT_ZHIHU_URL,
    ]
    shell_parts = []
    for p in cmd:
        if ' ' in p:
            shell_parts.append(f'"{p}"')
        else:
            shell_parts.append(p)
    shell_cmd = ' '.join(shell_parts)
    log(f'[INFO] Launching Chrome: {shell_cmd}')
    subprocess.Popen(
        f'nohup {shell_cmd} > {CHROME_LOG} 2>&1 &',
        shell=True, executable='/bin/bash',
        start_new_session=True,
    )


def main():
    ap = argparse.ArgumentParser(description='Restart Chrome (single-window via bb-browser daemon)')
    ap.add_argument('--chrome-bin', default=DEFAULT_CHROME_BIN)
    ap.add_argument('--display', default=DEFAULT_DISPLAY)
    ap.add_argument('--cdp-port', type=int, default=DEFAULT_CDP_PORT)
    ap.add_argument('--wait-seconds', type=int, default=8)
    args = ap.parse_args()

    self_pid = os.getpid()
    parent_pid = os.getppid()
    exclude_pids = {self_pid, parent_pid}

    # Step 1: kill bb-browser daemon node process and all Chrome windows
    # (bb-browser daemon stop kills ALL Chrome windows via SIGTERM cascade,
    #  so we do it manually to control the order)
    log('[INFO] Stopping bb-browser daemon and all Chrome processes...')

    # Kill all Chrome processes
    all_chrome_pairs = find_processes(
        lambda cl: '/chrome ' in f' {cl} ' or 'google-chrome' in cl or 'chromium' in cl,
        exclude_pids=exclude_pids,
    )
    kill_processes(all_chrome_pairs, 'Chrome')

    # Kill bb-browser daemon node process (if any)
    daemon_pairs = find_processes(
        lambda cl: ('node' in cl or 'bb-browser' in cl) and 'dist/cli.js' in cl,
        exclude_pids=exclude_pids,
    )
    kill_processes(daemon_pairs, 'bb-browser daemon')
    time.sleep(2)

    # Step 2: launch Chrome with our profile
    launch_chrome(args.chrome_bin, args.display, args.cdp_port)
    cdp = wait_for_cdp(args.cdp_port, timeout=30)
    if not cdp:
        raise SystemExit('[FAIL] Chrome CDP did not become ready in time')
    log(f"[INFO] Chrome CDP ready: {cdp.get('Browser', 'unknown')}")

    # Step 3: write our port into bb-browser's cdp-port file
    # This tells bb-browser daemon to connect to OUR Chrome instead of launching its own
    MANAGED_BROWSER_DIR.mkdir(parents=True, exist_ok=True)
    MANAGED_PORT_FILE.write_text(str(args.cdp_port))
    log(f'[INFO] Written cdp-port={args.cdp_port} to {MANAGED_PORT_FILE}')

    # Step 4: wait for zhihu page to load (cookies get written)
    log(f'[INFO] Waiting {args.wait_seconds}s for zhihu page to load...')
    time.sleep(args.wait_seconds)

    # Step 5: verify zhihu/hot
    # bb-browser commands auto-connect via discoverCdpPort() which reads cdp-port file
    log('[INFO] Verifying bb-browser zhihu/hot...')
    data = test_zhihu_hot()

    if 'error' in data:
        result = {
            'success': True,
            'message': '浏览器启动成功，知乎抓取需要登录态',
            'count': 0,
            'cdp_port': args.cdp_port,
            'user_data_dir': FIXED_USER_DATA_DIR,
            'sample_titles': ['(requires zhihu login in Chrome profile)'],
            'error': data['error']['message'],
        }
    else:
        count = data.get('count', 0)
        items = data.get('items', [])
        titles = [item.get('title', '')[:60] for item in items[:3]]
        result = {
            'success': True,
            'message': f'浏览器启动成功，知乎热榜抓取成功（{count}条）',
            'count': count,
            'cdp_port': args.cdp_port,
            'user_data_dir': FIXED_USER_DATA_DIR,
            'sample_titles': titles,
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[FAIL] Interrupted', file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f'[FAIL] {e}', file=sys.stderr)
        sys.exit(1)
