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
