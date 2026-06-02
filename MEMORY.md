# 记忆文档

## 安全规则
- ⚠️ **任何影响系统的操作都必须先征求用户同意**
- 包括但不限于：sudo 命令、删除文件、修改系统配置、网络操作等

## 用户偏好
- 🚫 **对加密货币不感兴趣** — 股票分析时只关注股票，过滤加密货币
- 🔥 **新闻热点查看** — 当用户说"查看今日新闻热点"时，使用news-hotspots技能

## 工作习惯记录
- 以后给出答复的时候，需要在尾部标注使用了哪个工具/技能
- **使用原始工具名称进行标注**（如：web_fetch、news-hotspots等）
- 处理长任务/异步任务时：若系统完成通知被静默，不要只内部消化；应主动补发一句简短回执（如“已完成，结果如下/已发你了”）。若未被静默，则直接按用户原始要求发送结果，不额外重复。

## 操作授权偏好
- 默认直接执行一般操作，不需要先走 `/approve`
- **涉及系统危险操作**（如系统配置、高风险命令、潜在影响系统稳定性的操作）时，必须先征求用户确认
- **涉及删除操作** 时，必须先征求用户确认
- 若平台/运行时存在强制审批限制，需如实说明，不能承诺绕过系统限制

## 工作目录
- 完成任务需要记录的临时文件应该放到 temp 目录下

---

## Promoted From Short-Term Memory (2026-04-29)

<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:3:6 -->
- 1. `daily*.md` / `daily*.json` 顶部 summary 的 `fail=` 计数与新 meta（如 `twitter1.meta.json` 的 `failed_calls=1`）不一致，优先查 `scripts/merge-hotspots.py` 对 source overview / meta 选择或 summary 拼接逻辑 2. `local_extra_score` 仅参考、不参与 `final_score` 的语义尚未透传到最终对外产物，需覆盖 `merge-hotspots.py` / `daily*.json` / Markdown 输出链路 3. 修复入口以 `scripts/merge-hotspots.py` 为主，并同步补 `tests/test_hotspots.py` 回归用例 ## Light Sleep <!-- openclaw:dreaming:light:start --> - Candidate: 2026-04-21 新会话开始: 时间：Tuesday, April 21st, 2026 - 00:57 (Asia/Shanghai); 从 2026-04-20 的 pre-compaction 状态接续（session 已被压缩，context 从 summary 恢复）; workspace bootstrap 文件（SOUL.md / USER.md / MEMORY.md / AGENTS.md / TOOLS.md / IDENTITY.md / HEARTBEAT.md）均未变更，内容与上一 session 相同; 本 session [score=0.845 recalls=0 avg=0.620 source=memory/2026-04-21.md:9-16]
<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:10:12 -->
- ## Light Sleep <!-- openclaw:dreaming:light:start --> - Candidate: 2026-04-21 新会话开始: 时间：Tuesday, April 21st, 2026 - 00:57 (Asia/Shanghai); 从 2026-04-20 的 pre-compaction 状态接续（session 已被压缩，context 从 summary 恢复）; workspace bootstrap 文件（SOUL.md / USER.md / MEMORY.md / AGENTS.md / TOOLS.md / IDENTITY.md / HEARTBEAT.md）均未变更，内容与上一 session 相同; 本 session - confidence: 0.62 - evidence: memory/2026-04-21.md:3-6 - recalls: 0 - status: staged - Candidate: 待跟进尾巴（来自 2026-04-20 的 news-hotspots 修复）: `daily*.md` / `daily*.json` 顶部 summary 的 `fail=` 计数与新 meta（如 `twitter1.meta.json` 的 `failed_calls=1`）不一致，优先查 `scripts/merge-hotspots.py` 对 source overview / meta 选择或 summary 拼接逻辑; `local_extra_score` 仅参考、不参与 `final_score` 的语义尚未透传到最终对外产物，需覆 [score=0.845 recalls=0 avg=0.620 source=memory/2026-04-21.md:14-21]
<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:192:194 -->
- - Candidate: Possible Lasting Truths: 老板新增偏好：长任务/异步任务完成后，若完成通知被静默，需要主动补一句简短回执；若未静默，则直接发送原始结果，不重复补发。 [confidence=0.58 evidence=memory/2026-04-13.md:1-1]; 系统监控脚本修复: 问题：system-monitor 脚本执行后被 SIGKILL 杀死; 原因：exec session 处理 stdout 有问题，脚本内 sleep 会导致 session 卡住; 解决：脚本末尾使用 `os._exit(0)` 强制退出，通过 backg - confidence: 0.62 - evidence: memory/2026-04-20.md:199-201 [score=0.840 recalls=0 avg=0.620 source=memory/2026-04-21.md:31-33]
<!-- openclaw-memory-promotion:memory:memory/2026-04-22.md:89:91 -->
- - Candidate: Possible Lasting Truths: 老板新增偏好：长任务/异步任务完成后，若完成通知被静默，需要主动补一句简短回执；若未静默，则直接发送原始结果，不重复补发。 [confidence=0.58 evidence=memory/2026-04-13.md:1-1]; 系统监控脚本修复: 问题：system-monitor 脚本执行后被 SIGKILL 杀死; 原因：exec session 处理 stdout 有问题，脚本内 sleep 会导致 session 卡住; 解决：脚本末尾使用 `os._exit(0)` 强制退出，通过 backg - confidence: 0.62 - evidence: memory/2026-04-21.md:192-194 [score=0.840 recalls=0 avg=0.620 source=memory/2026-04-22.md:18-20]

## Promoted From Short-Term Memory (2026-04-30)

<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:419:421 -->
- - Candidate: Possible Lasting Truths: 2026-04-16 会话记录: `~/.openclaw/openclaw.json` 已写入 `session.maintenance`：`mode=enforce`、`pruneAfter=7d`、`maxEntries=80`、`rotateBytes=10mb`。; `plugins.entries.memory-core.config.dreaming.enabled` 已改为 `false`，关闭 dreaming。; Node.js 内存上限已为 gateway 设置为 1GB，配置位置是 - confidence: 0.62 - evidence: memory/2026-04-23.md:149-151 [score=0.856 recalls=0 avg=0.620 source=memory/2026-04-24.md:8-10]

## Promoted From Short-Term Memory (2026-05-01)

<!-- openclaw-memory-promotion:memory:memory/2026-04-25.md:419:421 -->
- - Candidate: Possible Lasting Truths: 2026-04-16 会话记录: `~/.openclaw/openclaw.json` 已写入 `session.maintenance`：`mode=enforce`、`pruneAfter=7d`、`maxEntries=80`、`rotateBytes=10mb`。; `plugins.entries.memory-core.config.dreaming.enabled` 已改为 `false`，关闭 dreaming。; Node.js 内存上限已为 gateway 设置为 1GB，配置位置是 - confidence: 0.62 - evidence: memory/2026-04-23.md:149-151 [score=0.856 recalls=0 avg=0.620 source=memory/2026-04-25.md:298-300]

## Promoted From Short-Term Memory (2026-05-02)

<!-- openclaw-memory-promotion:memory:memory/2026-04-26.md:439:441 -->
- - Candidate: Possible Lasting Truths: 2026-04-16 会话记录: `~/.openclaw/openclaw.json` 已写入 `session.maintenance`：`mode=enforce`、`pruneAfter=7d`、`maxEntries=80`、`rotateBytes=10mb`。; `plugins.entries.memory-core.config.dreaming.enabled` 已改为 `false`，关闭 dreaming。; Node.js 内存上限已为 gateway 设置为 1GB，配置位置是 - confidence: 0.62 - evidence: memory/2026-04-24.md:419-421 [score=0.856 recalls=0 avg=0.620 source=memory/2026-04-26.md:168-170]
<!-- openclaw-memory-promotion:memory:memory/2026-04-27.md:444:446 -->
- - Candidate: Possible Lasting Truths: 2026-04-16 会话记录: `~/.openclaw/openclaw.json` 已写入 `session.maintenance`：`mode=enforce`、`pruneAfter=7d`、`maxEntries=80`、`rotateBytes=10mb`。; `plugins.entries.memory-core.config.dreaming.enabled` 已改为 `false`，关闭 dreaming。; Node.js 内存上限已为 gateway 设置为 1GB，配置位置是 - confidence: 0.62 - evidence: memory/2026-04-24.md:419-421 [score=0.827 recalls=0 avg=0.620 source=memory/2026-04-27.md:223-225]

## Promoted From Short-Term Memory (2026-05-13)

<!-- openclaw-memory-promotion:memory:memory/2026-05-08.md:3:3 -->
- Today I checked the fund purchase restrictions for three funds: [score=0.857 recalls=0 avg=0.620 source=memory/2026-05-08.md:3-3]
<!-- openclaw-memory-promotion:memory:memory/2026-05-08.md:8:8 -->
- These limits represent the maximum single-day purchase amounts allowed for each fund. [score=0.857 recalls=0 avg=0.620 source=memory/2026-05-08.md:8-8]

## Promoted From Short-Term Memory (2026-05-27)

<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:6:9 -->
- | 股票 | 当前价 | 买入价 | 涨跌幅 | |------|--------|--------|--------| | AAPL | $304.99 | $258.53 | **+17.97%** | | NVDA | $219.51 | $181.68 | **+20.82%** | [score=0.872 recalls=0 avg=0.620 source=memory/2026-05-22.md:6-9]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:10:13 -->
- | TSLA | $417.85 | $348.36 | **+19.95%** | | MSFT | $419.09 | $424.16 | **-1.20%** | | AMD | $449.59 | $284.49 | **+58.03%** | | META | $607.38 | $668.84 | **-9.19%** | [score=0.872 recalls=0 avg=0.620 source=memory/2026-05-22.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:14:15 -->
- | TSM | $407.15 | $368.08 | **+10.61%** | | MU | $762.10 | $449.38 | **+69.59%** | [score=0.872 recalls=0 avg=0.620 source=memory/2026-05-22.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:18:21 -->
- | 基金 | 限购金额 | |------|----------| | 270042 广发纳斯达克100联接A | **每日10元** | | 017731 嘉实全球产业升级(QDII)C | **每日100元** | [score=0.822 recalls=0 avg=0.620 source=memory/2026-05-22.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:22:22 -->
- | 018147 建信新兴市场混合(QDII)C | **每日20元** | [score=0.822 recalls=0 avg=0.620 source=memory/2026-05-22.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:24:24 -->
- > ⚠️ QDII额度依然极度紧张，广发纳斯达克仅剩10元/天额度。 [score=0.822 recalls=0 avg=0.620 source=memory/2026-05-22.md:24-24]
