# ERRORS

## [ERR-20260411-001] gateway.config.patch protected path tools.exec.ask

**Logged**: 2026-04-11T10:03:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Tried to disable default exec approval prompts via OpenClaw config patch, but `tools.exec.ask` is a protected config path and cannot be changed through `gateway.config.patch`.

### Error
```
gateway config.patch cannot change protected config paths: tools.exec.ask
```

### Context
- Operation attempted: `gateway.config.patch`
- Intended patch: `{\"tools\":{\"exec\":{\"ask\":\"off\"}}}`
- User had explicitly approved a system config change.
- Schema lookup confirmed `tools.exec.ask` exists, but patching is blocked by protection rules.

### Suggested Fix
Need a different supported admin path/documented mechanism for changing protected exec approval defaults, if one exists.

### Metadata
- Reproducible: yes
- Related Files: /home/clawd/.openclaw/openclaw.json

---

## [ERR-20260411-002] stock-analysis watchlist check interrupted during uv dependency install

**Logged**: 2026-04-11T21:46:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Running the stock-analysis watchlist monitor via `uv run .../watchlist.py check` was interrupted twice with SIGTERM while `uv` was still downloading/building first-run dependencies.

### Error
```text
Exec failed (good-orbit, signal SIGTERM)
Building multitasking==0.0.12
Downloading pygments (1.2MiB)
Downloading numpy (15.9MiB)
Downloading pandas (10.4MiB)
Downloading curl-cffi (10.6MiB)

Exec failed (quick-sable, signal SIGTERM)
Building multitasking==0.0.12
Downloading numpy (15.9MiB)
Downloading pandas (10.4MiB)
Downloading pygments (1.2MiB)
Downloading curl-cffi (10.6MiB)
Built multitasking==0.0.12
```

### Context
- Operation attempted: `uv run /home/clawd/.openclaw/workspace/skills/stock-analysis/scripts/watchlist.py check`
- User intent: execute stock price monitoring on existing watchlist
- Environment: first run of the skill needed to fetch Python dependencies
- Result: monitoring script never reached alert evaluation before runtime interruption

### Suggested Fix
Pre-warm heavy `uv`-based finance skills before user-facing runs, or use a lighter fallback quote fetch when only a quick watchlist snapshot is needed.

### Metadata
- Reproducible: unknown
- Related Files: /home/clawd/.openclaw/workspace/skills/stock-analysis/SKILL.md, /home/clawd/.openclaw/workspace/skills/stock-analysis/scripts/watchlist.py
- See Also: none

---
## [ERR-20260412-001] archive-clear-zsh-shell-mismatch

**Logged**: 2026-04-12T22:26:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Tried to use bash-specific `shopt` in the default zsh shell while clearing the archive directory.

### Error
```
zsh:7: command not found: shopt
```

### Context
- Command/operation attempted: clear `/home/clawd/.openclaw/workspace/archive` contents while preserving the directory
- Shell environment: zsh
- Cause: used bash-only `shopt -s dotglob nullglob`

### Suggested Fix
Use zsh-compatible options like `setopt local_options null_glob glob_dots` when writing shell commands for this runtime.

### Metadata
- Reproducible: yes
- Related Files: /home/clawd/.openclaw/workspace/TOOLS.md

---
## [ERR-20260412-002] sessions_spawn-subagent-streamto-incompatibility

**Logged**: 2026-04-12T22:27:30+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Attempting to use `sessions_spawn` with `runtime=subagent` failed because the tool rejected `streamTo`, even though the structured schema exposes it.

### Error
```
streamTo is only supported for runtime=acp; got runtime=subagent
```

### Context
- Operation attempted: spawn subagent for news-hotspots daily pipeline
- Tool: sessions_spawn
- Runtime: subagent
- Result: incompatible parameter validation/runtime behavior

### Suggested Fix
Use a subagent-compatible spawn shape without `streamTo`, or update the tool schema/runtime contract so they agree.

### Metadata
- Reproducible: yes
- Related Files: /home/clawd/.openclaw/workspace/skills/news-hotspots/references/execution-guide.md

---
## [ERR-20260413-001] system-monitor-script-timeout

**Logged**: 2026-04-12T17:36:12.719892+00:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
system-monitor 技能脚本在当前 exec 环境中连续两次未返回输出并被 SIGTERM 终止。

### Error
```
Exec failed (nova-sea, signal SIGTERM)
Exec failed (glow-har, signal SIGTERM)
```

### Context
- Command/operation attempted: python3 /home/clawd/.openclaw/workspace/skills/system-monitor/scripts/collect_stats.py
- The script should sample for ~6s and print a formatted report, but no output was captured before termination.
- A manual fallback sampler using /proc succeeded and was used to answer the user.

### Suggested Fix
排查该脚本在当前运行时为何没有稳定输出；必要时让技能默认输出 JSON，或缩短采样/改成先写文件再输出，避免被 exec 截断。

### Metadata
- Reproducible: unknown
- Related Files: /home/clawd/.openclaw/workspace/skills/system-monitor/scripts/collect_stats.py
- See Also: none

---
## [ERR-20260420-001] pkill_pgrep_pattern_option_conflict

**Logged**: 2026-04-20T15:13:07.771559+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
使用 pkill/pgrep 按完整命令行匹配带 `--remote-debugging-port=...` 的参数时，未加稳妥处理会把模式误识别成命令自身选项，导致重启浏览器失败。

### Error
```
pkill: 未识别的选项 "--remote-debugging-port=19825 --user-data-dir=/home/clawd/.bb-browser/browser/user-data"
pgrep: 未识别的选项 "--remote-debugging-port=19825 --user-data-dir=/home/clawd/.bb-browser/browser/user-data"
```

### Context
- Command/operation attempted: 重启 bb-browser 使用的 Chrome 调试实例
- Input or parameters used: `pkill -TERM -f "--remote-debugging-port=19825 --user-data-dir=/home/clawd/.bb-browser/browser/user-data"`
- Environment details: Ubuntu procps-ng；模式字符串以 `--` 开头

### Suggested Fix
优先使用 Python 遍历 `/proc/*/cmdline` 按子串匹配并发信号，避免依赖 pkill/pgrep 对 `--` 开头模式的歧义处理；若继续用 pkill/pgrep，必须验证 `--` 分隔在目标环境下是否可靠。

### Metadata
- Reproducible: yes
- Related Files: /home/clawd/.openclaw/workspace/.learnings/ERRORS.md

---

