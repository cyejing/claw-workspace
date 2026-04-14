# LEARNINGS

## [LRN-20260411-001] best_practice

**Logged**: 2026-04-11T10:03:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Before attempting OpenClaw config changes for exec approval behavior, verify not only the schema path but also whether the path is protected against `gateway.config.patch`.

### Details
A schema lookup can show that `tools.exec.ask` exists, but `gateway.config.patch` may still reject changes because the path is protected. Existence in schema does not imply writeability.

### Suggested Action
When users ask to disable `/approve` globally, explain that the config key exists but may be protected, then look for a documented admin mechanism rather than assuming `config.patch` works.

### Metadata
- Source: error
- Related Files: /home/clawd/.openclaw/openclaw.json
- Tags: openclaw, config, approvals, protected-path

---
## [LRN-20260412-001] correction

**Logged**: 2026-04-12T12:04:29.754791+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
When user asks to verify news-hotspots ‘加分项’, confirm whether they mean local source bonus (`local_extra_score`) or cross-source same-title resonance (`cross_source_hot_score`) before answering.

### Details
I initially interpreted the user’s ‘同源加分项’ as `local_extra_score`, but they actually meant cross-source same-title/cross-source match bonus. For news-hotspots review requests, inspect the user wording carefully and prefer asking/confirming when ‘同源/跨源’ is ambiguous.

### Suggested Action
For future review of scoring in news-hotspots output JSON, map terms explicitly:
- 同源/源内热度 -> `local_extra_score`
- 跨源/同标题/多 source_type 命中 -> `cross_source_hot_score`

### Metadata
- Source: user_feedback
- Related Files: skills/news-hotspots/scripts/merge-sources.py, archive/news-hotspots/2026-04-12/json/daily.json
- Tags: correction, news-hotspots, scoring

---

## [LRN-20260413-002] correction

**Logged**: 2026-04-12T17:41:47.714228+00:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
不要仅凭 RSS 排序和运行时长就把 Chrome / next-server / openclaw-gateway 判定为“无效浪费内存”的进程；这些在该机器上属于正常且需要保留的常驻进程。

### Details
我根据 RSS、ELAPSED 和命令行参数推断 Chrome remote-debugging 进程与 next-server 可能是长期空转，但用户明确说明这些都是正常且需要用到的进程。对这台机器来说，Chrome 自动化/调试实例、next-server、本地 OpenClaw gateway 都可能是长期服务的一部分，不能因为占内存或运行天数长就默认建议清理。

### Suggested Action
以后在这台机器做“哪些进程浪费内存”的判断时，先把 Chrome（含 remote-debugging）、next-server、openclaw-gateway 视为默认白名单；除非用户明确说不用了，或先进一步核实对应用途，再建议关闭。

### Metadata
- Source: user_feedback
- Related Files: /home/clawd/.openclaw/workspace/TOOLS.md
- Tags: correction, process-audit, chrome, next-server, openclaw-gateway

---
