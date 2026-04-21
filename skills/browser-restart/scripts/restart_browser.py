#!/usr/bin/env python3
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

DEFAULT_DISPLAY = ':0'
DEFAULT_CDP_PORT = 19825
FIXED_USER_DATA_DIR = '/home/clawd/.cache/chrome'
DEFAULT_CHROME_BIN = 'google-chrome-stable'
DEFAULT_ZHIHU_URL = 'https://www.zhihu.com/hot'
DAEMON_JSON = Path.home() / '.bb-browser' / 'daemon.json'
CHROME_LOG = '/tmp/browser-restart-chrome.log'
DAEMON_LOG = '/tmp/browser-restart-daemon.log'


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


def kill_named_processes(pairs, name: str):
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


def http_get(url: str, headers=None, timeout=5):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', 'ignore')


def wait_for_cdp(port: int, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        try:
            body = http_get(f'http://127.0.0.1:{port}/json/version', timeout=3)
            return json.loads(body)
        except Exception:
            time.sleep(1)
    return None


def wait_for_daemon_json(timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        if DAEMON_JSON.exists():
            try:
                data = json.loads(DAEMON_JSON.read_text())
                if all(k in data for k in ('pid', 'host', 'port', 'token')):
                    return data
            except Exception:
                pass
        time.sleep(1)
    return None


def wait_for_daemon_health(info, timeout=15):
    end = time.time() + timeout
    headers = {'Authorization': f"Bearer {info['token']}"}
    while time.time() < end:
        try:
            body = http_get(f"http://{info['host']}:{info['port']}/status", headers=headers, timeout=4)
            data = json.loads(body)
            if data.get('running'):
                return data
        except Exception:
            pass
        time.sleep(1)
    return None


def run(cmd, timeout=60):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def shell_quote(parts):
    return ' '.join(subprocess.list2cmdline([p]) if any(c in p for c in ' \t') else p for p in parts)


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
        'about:blank',
    ]
    shell = shell_quote(cmd) + f' > {CHROME_LOG} 2>&1 &'
    log(f'[INFO] Launching Chrome: {shell_quote(cmd)}')
    subprocess.Popen(shell, shell=True, executable='/bin/bash', start_new_session=True)


def launch_daemon():
    shell = f'nohup bb-browser daemon > {DAEMON_LOG} 2>&1 &'
    log('[INFO] Launching bb-browser daemon')
    subprocess.Popen(shell, shell=True, executable='/bin/bash', start_new_session=True)


def ensure_zhihu_tab(open_retries: int, wait_seconds: int):
    last = None
    for i in range(1, open_retries + 1):
        log(f'[INFO] Opening Zhihu tab ({i}/{open_retries})')
        try:
            code, out, err = run(['bb-browser', 'open', DEFAULT_ZHIHU_URL], timeout=40)
        except subprocess.TimeoutExpired:
            last = ('timeout', '', 'bb-browser open timeout')
            time.sleep(wait_seconds)
            continue
        last = (code, out, err)
        if code == 0:
            if out:
                log(out)
            time.sleep(wait_seconds)
            return True
        if err:
            log(f'[WARN] bb-browser open stderr: {err}')
        time.sleep(wait_seconds)
    raise RuntimeError(f'打开知乎失败: {last}')


def run_zhihu_hot(site_retries: int, wait_seconds: int):
    last_error = None
    last_payload = None
    for i in range(1, site_retries + 1):
        log(f'[INFO] Running zhihu/hot ({i}/{site_retries})')
        try:
            code, out, err = run(['bb-browser', 'site', 'zhihu/hot', '--json'], timeout=60)
        except subprocess.TimeoutExpired:
            last_error = 'bb-browser site zhihu/hot timeout'
            log(f'[WARN] {last_error}')
            time.sleep(wait_seconds)
            continue
        if err:
            log(f'[WARN] stderr: {err}')
        if code == 0 and out:
            try:
                payload = json.loads(out)
                last_payload = payload
            except Exception as e:
                last_error = f'JSON parse failed: {e}'
                time.sleep(wait_seconds)
                continue

            if isinstance(payload, dict) and payload.get('success') is False:
                last_error = payload.get('error') or 'adapter returned failure'
                time.sleep(wait_seconds)
                continue

            data = payload.get('data') if isinstance(payload, dict) and isinstance(payload.get('data'), dict) else payload
            if isinstance(data, dict) and isinstance(data.get('count'), int):
                return data
            if isinstance(data, dict) and isinstance(data.get('items'), list):
                data['count'] = len(data['items'])
                return data
            last_error = 'adapter output missing count/items'
        else:
            last_error = err or out or f'non-zero exit: {code}'
        time.sleep(wait_seconds)
    raise RuntimeError(json.dumps({'error': last_error or 'zhihu/hot failed', 'last_payload': last_payload}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description='Restart Chrome and verify bb-browser Zhihu scraping')
    ap.add_argument('--chrome-bin', default=DEFAULT_CHROME_BIN)
    ap.add_argument('--display', default=DEFAULT_DISPLAY)
    ap.add_argument('--cdp-port', type=int, default=DEFAULT_CDP_PORT)
    ap.add_argument('--zhihu-open-retries', type=int, default=2)
    ap.add_argument('--zhihu-site-retries', type=int, default=4)
    ap.add_argument('--wait-seconds', type=int, default=8)
    args = ap.parse_args()

    self_pid = os.getpid()
    parent_pid = os.getppid()
    exclude_pids = {self_pid, parent_pid}

    daemon_pairs = find_processes(
        lambda cl: 'bb-browser/dist/daemon.js' in cl or 'bb-browser daemon' in cl,
        exclude_pids=exclude_pids,
    )
    kill_named_processes(daemon_pairs, 'bb-browser daemon')
    if DAEMON_JSON.exists():
        DAEMON_JSON.unlink()
        log(f'[INFO] Removed stale daemon.json: {DAEMON_JSON}')

    chrome_pairs = find_processes(
        lambda cl: ('/chrome ' in f' {cl} ' or 'google-chrome' in cl or 'chromium' in cl),
        exclude_pids=exclude_pids,
    )
    kill_named_processes(chrome_pairs, 'Chrome')

    launch_chrome(args.chrome_bin, args.display, args.cdp_port)
    cdp = wait_for_cdp(args.cdp_port, timeout=30)
    if not cdp:
        raise SystemExit('[FAIL] Chrome CDP did not become ready in time')
    log(f"[INFO] Chrome CDP ready: {cdp.get('Browser', 'unknown')}")

    launch_daemon()
    daemon_info = wait_for_daemon_json(timeout=20)
    if not daemon_info:
        raise SystemExit('[FAIL] bb-browser daemon.json not created in time')
    health = wait_for_daemon_health(daemon_info, timeout=15)
    if not health:
        raise SystemExit('[FAIL] bb-browser daemon is not healthy')
    log('[INFO] bb-browser daemon is healthy')

    ensure_zhihu_tab(args.zhihu_open_retries, args.wait_seconds)
    data = run_zhihu_hot(args.zhihu_site_retries, args.wait_seconds)

    items = data.get('items', []) if isinstance(data, dict) else []
    count = data.get('count', len(items)) if isinstance(data, dict) else 0
    result = {
        'success': True,
        'message': '浏览器启动成功，知乎数据可正常抓取',
        'count': count,
        'cdp_port': args.cdp_port,
        'daemon_port': daemon_info.get('port'),
        'user_data_dir': FIXED_USER_DATA_DIR,
        'sample_titles': [item.get('title') for item in items[:3]],
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
