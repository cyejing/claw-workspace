# 记忆文档

## 安全规则
- ⚠️ **任何影响系统的操作都必须先征求用户同意**
- 包括但不限于：sudo 命令、删除文件、修改系统配置、网络操作等

## 输出格式偏好
- ⚠️ **重要传闻**相关输出：**列表格式**，不用表格（飞书表格不好查看）

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

## Promoted From Short-Term Memory (2026-08-08)

<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1144.md:14:14 -->
- Conversation Summary: `/` 根分区：59G 总容量，已用 48G，可用 8.4G（使用率 85%） [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1144.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1144.md:16:19 -->
- Conversation Summary: **主要占用（~2G 以上）** | 路径 | 大小 | 说明 | |------|------|------| | `/var/log/syslog` | 4.5G | 系统日志，非常大 | [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1144.md:16-19]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1144.md:20:23 -->
- Conversation Summary: | `/var/log/journal` | 3.5G | systemd 日志 | | `/home/clawd/.cache/chrome` | 1.3G | Chrome 浏览器缓存 | | `~/.cache/uv` | 322M | uv 包管理器缓存 | | `~/.cache/pnpm` | 211M | pnpm 缓存 | [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1144.md:20-23]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1144.md:3:5 -->
- Session: 2026-08-04 11:44:51 GMT+8: **Session Key**: agent:main:feishu:direct:ou_77fa18f196aa0559f70cdd7e1ffdd567; **Session ID**: a350374d-32e0-4603-b5a4-dcefaae64696; **Source**: feishu [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1144.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1144.md:9:11 -->
- Conversation Summary: user: [message_id: om_x100b6821b34578acde77cb070117710] ou_77fa18f196aa0559f70cdd7e1ffdd567: 查看磁盘情况，清理磁盘空间 assistant: 磁盘情况如下： [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1144.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1725.md:13:14 -->
- Conversation Summary: assistant: 系统日志已清理掉 2.9G。再清几块明确安全的残留（apt 包缓存、任务临时目录、测试缓存目录）： assistant: 清理完毕 🦐 汇报： [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1725.md:13-14]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1725.md:18:21 -->
- Conversation Summary: | 项目 | 释放空间 | |------|---------| | journalctl 历史日志归档 | **2.9 GB** | | apt 包缓存 | ~108 MB | [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1725.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1725.md:22:23 -->
- Conversation Summary: | news-hotspots pipeline 临时文件 | ~7 MB | | chrome 测试缓存目录 | ~13 MB | [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1725.md:22-23]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1725.md:3:5 -->
- Session: 2026-08-04 17:25:36 GMT+8: **Session Key**: agent:main:feishu:direct:ou_77fa18f196aa0559f70cdd7e1ffdd567; **Session ID**: 6e581db6-de1c-4d44-b6e9-52ed82b00a8c; **Source**: feishu [score=0.828 recalls=0 avg=0.620 source=memory/2026-08-04-1725.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1725.md:9:12 -->
- Conversation Summary: user: [message_id: om_x100b68224a4800a0dee18d3f9c63cd8] ou_77fa18f196aa0559f70cdd7e1ffdd567: 可以安全清理的就清理掉，系统日志的话识别安全的进行清理 assistant: 系统盘已用 85%（48G/59G），日志是大头。先全面看下还有哪些可清理的： assistant: 已释放 2.9G 日志空间。继续检查更多可清理项： [score=0.818 recalls=0 avg=0.620 source=memory/2026-08-04-1725.md:9-12]

## Promoted From Short-Term Memory (2026-08-09)

<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1144.md:13:13 -->
- Conversation Summary: **磁盘整体** [score=0.841 recalls=0 avg=0.620 source=memory/2026-08-04-1144.md:13-13]
<!-- openclaw-memory-promotion:memory:memory/2026-08-04-1725.md:16:16 -->
- Conversation Summary: **已清理（安全）** [score=0.841 recalls=0 avg=0.620 source=memory/2026-08-04-1725.md:16-16]
<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:13:14 -->
- 主要议题: SK海力士股价"深V"反转; 房企前七月销售总额1.8万亿 [score=0.830 recalls=0 avg=0.620 source=memory/2026-08-02.md:13-14]
<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:4:6 -->
- 热点新闻任务: 执行了 news-hotspots daily pipeline; 归档: /home/clawd/.openclaw/workspace/archive/news-hotspots/2026-08-02/markdown/daily.md; 产出 36 条热点（API 10条 + RSS 26条） [score=0.830 recalls=0 avg=0.620 source=memory/2026-08-02.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:9:12 -->
- 主要议题: 伊朗政治危机（哈梅内伊去世后应急决策）; 中东局势升温（卡塔尔LNG船霍尔木兹海峡遭袭）; AI前沿：Word文档自传播蠕虫、OpenAI Astra数学突破、ByteDance Seedance 2.5视频生成; 政治局会议定调逆周期调节加码 [score=0.830 recalls=0 avg=0.620 source=memory/2026-08-02.md:9-12]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1039.md:13:16 -->
- Conversation Summary: assistant: 还在跑，已抓完 RSS(751) 和 API(44)，微博/头条/知乎源失败（可能被限流）。继续等待剩余源完成。 assistant: Google News 抓了 5 分钟也扑空了。继续等... assistant: 第 6 个源（Google News）已完，还剩最后 1 个源（应该是 X/Twitter，通常耗时最长）。继续等。 assistant: 抓取完成！现在读取归档报告： [score=0.806 recalls=0 avg=0.620 source=memory/2026-08-05-1039.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1039.md:17:17 -->
- Conversation Summary: assistant: **🦐 今日全球科技与 AI 热点 · 2026-08-04** [score=0.806 recalls=0 avg=0.620 source=memory/2026-08-05-1039.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1039.md:22:25 -->
- Conversation Summary: RSS 源：751 条 → 55 条精选; API 源：44 条 → 15 条精选; 微博/头条/知乎/Google News/Twitter：抓取失败（限流/网络问题）; 共汇聚 **70 条热点** [score=0.806 recalls=0 avg=0.620 source=memory/2026-08-05-1039.md:22-25]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1039.md:3:5 -->
- Session: 2026-08-05 10:39:16 GMT+8: **Session Key**: agent:main:feishu:direct:ou_77fa18f196aa0559f70cdd7e1ffdd567; **Session ID**: 0305ee52-1539-4334-96ea-4b592199e27d; **Source**: feishu [score=0.806 recalls=0 avg=0.620 source=memory/2026-08-05-1039.md:3-5]

## Promoted From Short-Term Memory (2026-08-10)

<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1039.md:21:21 -->
- Conversation Summary: **📡 抓取概要** [score=0.820 recalls=0 avg=0.620 source=memory/2026-08-05-1039.md:21-21]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1039.md:9:12 -->
- Conversation Summary: user: [message_id: om_x100b682f4f735ca0b208c37fcc44191] ou_77fa18f196aa0559f70cdd7e1ffdd567: 运行 定时任务 每日新闻热点 assistant: 收到！正在抓取今日新闻热点，稍等 15-30 分钟 🦐 assistant: 任务已启动 (session quiet-orbit)，正在抓取中，我持续监控进度。 [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1039.md:9-12]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1133.md:13:13 -->
- Conversation Summary: assistant: 发现了！新的 daemon（PID 121165）命令行里参数是对的，但 PPID=1（systemd），说明它被 systemd 重启了。更关键的是——它在读 `~/.bb-browser/browser/cdp-port` 的默认值（9222），而不是用命令行传的 19825。 [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1133.md:13-13]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1133.md:15:16 -->
- Conversation Summary: 让我换个思路，直接用 Python + CDP 绕过 daemon 来做抓取，彻底甩掉这个双 Chrome 问题： assistant: 问题清楚了！`bb-browser open zhihu/hot` 会自动启动一个新 daemon（用默认参数 `--cdp-port 9222`），它又拉起一个 Chrome。两条链路互不干扰。 [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1133.md:15-16]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1133.md:18:21 -->
- Conversation Summary: 彻底解决要绕开 daemon CLI，改用 Python 直连 CDP。写一个小脚本替代： assistant: WebSocket 连接有问题，让我换更简单的方式——用 Python 直接调用 bb-sites 的 adapter 代码，不走 CLI： assistant: 好，Chrome 只剩一个（19825）了，daemon 那边的也清了。现在让我看一下 bb-sites 的 adapter 源码，找一个不触发 CLI 自动起 daemon 的调用方式： assistant: adapter 用的是 `fetch` API 调知乎接口，需要登录态。我换一个更简单的思路：Chrome 打开知乎页面后，直接用 CDP 执行 JavaScript 提取渲染后的 DOM 数据： [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1133.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1133.md:22:25 -->
- Conversation Summary: assistant: 让我用一个更简单的方案——用 `node` 直接调用 bb-sites adapter，不走 bb-browser CLI： assistant: 让我换个角度——把 Chrome 的 cookie 直接注入 adapter 来绕过登录态问题： assistant: 只有一个 Chrome 了 ✅ 验证一下： assistant: 双窗口问题彻底解决了 🦐 [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1133.md:22-25]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1133.md:3:5 -->
- Session: 2026-08-05 11:33:31 GMT+8: **Session Key**: agent:main:feishu:direct:ou_77fa18f196aa0559f70cdd7e1ffdd567; **Session ID**: 8bef2e74-e46f-46df-9ea7-755e31ae3867; **Source**: feishu [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1133.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1133.md:9:12 -->
- Conversation Summary: assistant: PPID 是 systemd --user，不是 daemon 自己。说明有 systemd user service 在自动拉 Chrome。查一下： assistant: `--no-chrome` 也没挡住，daemon 依然拉了 Chrome。让我看 daemon 源码确认 `--no-chrome` 实际行为，同时换个策略： assistant: 问题找到了——`--no-chrome` 改进去了，但 `--cdp-port` 还是没生效。让我当场确认脚本当前内容并重新修复： assistant: 脚本里确实写了 `--no-chrome --cdp-port 19825`，但进程显示 daemon 用的是 `--cdp-port 9222` 且没带 `--no-chrome`。说明还有另一个 daemon 实例！让我查一下： [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1133.md:9-12]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1140.md:11:11 -->
- Conversation Summary: **2026-08-05 daily 全球科技与 AI 热点** [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1140.md:11-11]
<!-- openclaw-memory-promotion:memory:memory/2026-08-05-1140.md:15:15 -->
- Conversation Summary: **今日最突出的信号是 AI 基础设施的"军备竞赛"与地缘政治博弈交织。** 企业层面，Anthropic 与一家成立仅 6 个月的云计算初创公司 Volta 签下 100 亿美元算力协议，AMD 数据中心收入同比翻倍突破 67 亿美元，Arista 单季营收首破 30 亿美元——这些数字共同勾勒出一个事实：算力需求远未饱和，供应链（尤其是网络层）才是下一瓶颈。Google 则通过与 Broadcom、Apollo 的复杂融资结构，悄悄将 Anthropic 芯片风险从资产负债表转移出去，规避监管压力。 [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-05-1140.md:15-15]
