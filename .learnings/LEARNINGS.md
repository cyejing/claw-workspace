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
