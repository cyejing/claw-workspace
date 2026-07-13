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

## Promoted From Short-Term Memory (2026-07-10)

<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:9:9 -->
- Conversation Summary: user: Use the "news-hotspots" skill for this request. [score=0.834 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:9-9]

## Promoted From Short-Term Memory (2026-07-11)

<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:18:18 -->
- 每日新闻热点报告（已完成）: **报告已通过 Feishu 发送。** [score=0.881 recalls=0 avg=0.620 source=memory/2026-07-07.md:18-18]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:22:22 -->
- 每日新闻热点报告（已完成）: **备注：** Pipeline 执行正常，耗时约 443 秒（数据抓取）+ 112 秒（合并处理）。 [score=0.881 recalls=0 avg=0.620 source=memory/2026-07-07.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:7:7 -->
- 每日新闻热点报告（已完成）: **数据来源：** [score=0.881 recalls=0 avg=0.620 source=memory/2026-07-07.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03-1105.md:30:33 -->
- 方案 1：直接让 multica 跳过 `openclaw config file`（推荐）: 在 workspace 的 `openclaw-config.json` 里设置 `OPENCLAW_CONFIG_PATH`，multica 可能通过环境变量读取而不是调用 CLI： assistant: 先快速回一下那个 mention，然后继续修这个 bug。 assistant: 好，继续修这个 bug。真正的解决方案是创建一个 `openclaw` wrapper，让 `config file` 子命令走快速路径： assistant: 找到了！`openclaw.mjs` launcher 会 spawn 另一个 node 子进程来处理命令。**总共两个 node 进程**（launcher + child），各 3-4 秒 = 总共 7-10 秒。 [score=0.849 recalls=0 avg=0.620 source=memory/2026-07-03-1105.md:30-33]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03-1105.md:44:44 -->
- 方案 1：直接让 multica 跳过 `openclaw config file`（推荐）: **根因：** `openclaw config file` 命令需要 7-10 秒（Node 冷启动 + launcher spawn 子进程），Multica daemon 在 `prepare execution environment` 阶段调用它时超时被 kill。 [score=0.849 recalls=0 avg=0.620 source=memory/2026-07-03-1105.md:44-44]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03-1105.md:46:46 -->
- 方案 1：直接让 multica 跳过 `openclaw config file`（推荐）: **修复：** 在 PATH 第一位（`~/.nvm/versions/node/v24.14.0/bin/openclaw`）放置了一个 wrapper 脚本，让 `config file` 子命令直接返回配置路径，绕过 Node 冷启动。执行时间从 7-10 秒降到 **1-2 毫秒**。 [score=0.849 recalls=0 avg=0.620 source=memory/2026-07-03-1105.md:46-46]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:11:11 -->
- 每日新闻热点报告（已完成）: **主要热点：** [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-07.md:11-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:12:15 -->
- 每日新闻热点报告（已完成）: 🧠 AI 安全：AI 智能体首次实施完全自主的勒索软件攻击（Langflow 漏洞）; ⚙️ AI 基础设施：AMD 股价大涨，Anthropic 签署 190 亿美元数据中心租约; 💼 商业：Rivian 股价下跌，A股三大股指齐跌科创50逆势上涨; 🌍 国际：澳大利亚牛肉 55% 关税落地，山姆澳洲牛肉涨价 [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-07.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:16:16 -->
- 每日新闻热点报告（已完成）: 📦 开源：PythonRobotics、home-llm、awesome-agent-evolution 等项目热度上升 [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-07.md:16-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:5:5 -->
- 每日新闻热点报告（已完成）: **执行时间：** 11:32 - 11:41（约 9 分钟） [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-07.md:5-5]

## Promoted From Short-Term Memory (2026-07-12)

<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:45:48 -->
- ⚙️ AI 基础设施: ⭐8.5 | 中国的科技崛起重塑全球太空竞赛 — 中国在科研排名中稳步前进，太空野心不断扩大 | DW.com; ⭐7.5 | 32GB Corsair Vengeance DDR5 降至 359 美元 — Woot 促销，数月来最低价 | Tom's Hardware; ⭐7.4 | AI 算力主题蓄势大反攻！非农仅增 5.7 万远不及预期，美联储鹰派叙事遭重创？ — 美国 6 月招聘速度急剧放缓，非农仅增 5.7 万人 | Moomoo; ⭐7.2 | Apple 的"隐藏我的邮箱"服务被曝轻易泄露真实邮箱 — 苹果已知情一年仍未修复 | Tom's Hardware [score=0.879 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:45-48]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:49:49 -->
- ⚙️ AI 基础设施: ⭐7.1 | 字节跳动开始在巴西建设 384 亿美元的数据中心 — 位于巴西塞阿拉州的佩森港 | W.Media [score=0.879 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:49-49]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:53:56 -->
- 🌍 国际: ⭐7.5 | "为了多肽而来"：未获批减肥药在布鲁克林小卖部出售 — 实验性减肥药 retatrutide 被违法销售 | CBS News; ⭐7.5 | "千年一遇"的探险行动启航，调查两艘传奇沉船 — 研究人员将前往北大西洋海底，调查两艘与 19 世纪极地探险家相关的传奇沉船 | CBS News; ⭐7.5 | 俄罗斯对基辅发动"最大规模"袭击，至少 20 人死亡 — 基辅市长宣布哀悼日 | BBC World; ⭐7.5 | "我们要为他赢下世界杯" — 葡萄牙队带着迪奥戈·若塔的记忆征战 2026 世界杯 | BBC News [score=0.879 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:53-56]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:8:9 -->
- 每日新闻热点报告（已完成）: 总计 40 篇精选文章; RSS (7篇)、Twitter (7篇)、Google News (11篇)、Reddit (7篇)、GitHub Trending (3篇)、GitHub (2篇)、API (2篇)、头条 (1篇) [score=0.862 recalls=0 avg=0.620 source=memory/2026-07-07.md:8-9]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:37:40 -->
- 📦 开源动态: ⭐8.5 | jd-opensource/JoySafeter — 企业级 AI Agent 平台：不仅聊天，还能构建、运行、测试和追踪自主 Agent 团队，支持可视化编排 | GitHub Trending; ⭐7.2 | simonw/llm — 从命令行访问大语言模型 | GitHub Trending; ⭐6.5 | skalesapp/skales — 你的个人 AI 桌面代理，支持 Windows/macOS/Linux/Android。设定目标后自主工作，支持团队协作、Agent2Agent、工作流 | GitHub Trending; ⭐6.0 | Ollama v0.31.1 — Apple Silicon 上 Gemma 4 速度提升近 90%，通过多 token 预测（MTP）实现，自动调优无需配置 | GitHub [score=0.847 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:37-40]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:41:41 -->
- 📦 开源动态: ⭐4.5 | OpenClaw v2026.6.11 — 修复了渠道投递可靠性问题，覆盖 Telegram、WhatsApp、Matrix、Google Chat、iMessage、飞书等多个渠道 | GitHub [score=0.847 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:41-41]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:57:57 -->
- 🌍 国际: ⭐7.5 | 两名帝国大厦攀爬者被捕，据称在塔顶求婚 — 两人爬到帝国大厦顶部展开横幅，然后求婚 | CBS News [score=0.847 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:57-57]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03-1105.md:35:38 -->
- 方案 1：直接让 multica 跳过 `openclaw config file`（推荐）: 最简单的修复：在 PATH 里放一个 wrapper，让 `config file` 子命令走快速路径： assistant: 现在我完全理解了。创建一个 wrapper 在 PATH 更靠前的位置，快速处理 `config file`： assistant: `/home/clawd/.nvm/versions/node/v24.14.0/bin` 在 PATH 第一位，所以 wrapper 会生效。验证一下： assistant: **从 7-10 秒降到 2 毫秒！** 现在重启 multica daemon 让新配置生效： [score=0.834 recalls=0 avg=0.620 source=memory/2026-07-03-1105.md:35-38]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03-1105.md:39:42 -->
- 方案 1：直接让 multica 跳过 `openclaw config file`（推荐）: assistant: Daemon 重启成功（PID 2588861）。等 10 秒让它连上，然后触发一个任务测试： assistant: Daemon 正常运行，3 个 runtime 都连上了。让我确认 wrapper 在 daemon 环境里也能生效： assistant: Daemon 的 PATH 第一位就是 `/home/clawd/.nvm/versions/node/v24.14.0/bin`，wrapper 会对 daemon 生效。直接用 daemon 的 PATH 测试： assistant: **修复完成！** [score=0.834 recalls=0 avg=0.620 source=memory/2026-07-03-1105.md:39-42]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03-1105.md:49:51 -->
- 方案 1：直接让 multica 跳过 `openclaw config file`（推荐）: Daemon 已重启（PID 2588861）; Wrapper 在 daemon PATH 里生效; `openclaw config file` 现在只需 1ms [score=0.834 recalls=0 avg=0.620 source=memory/2026-07-03-1105.md:49-51]

## Promoted From Short-Term Memory (2026-07-13)

<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:61:64 -->
- 💼 商业: ⭐7.5 | AI 产能过剩疑虑引爆芯片股抛售潮，韩国"国民财富"面临重估 — Meta 出售算力资源引发全球芯片股抛售。三星电子、SK 海力士自 6 月高点已跌 21%-30%。半导体占韩国出口超两成 | Wall Street CN; ⭐7.4 | 36氪 AI 工具测评，正在找第一批"抢跑者" — 发起 AI 工具使用社群，搭建高密度碰撞平台，帮助小白和资深用户一起进步 | 36氪; ⭐7.1 | 能源价格之外：海湾供应中断的连锁效应 | ECB Blog; ⭐7.1 | 买翻新电子产品？避免这些重大错误 — 分享购买二手 / 翻新电子产品的注意事项和防骗指南 | NBC News [score=0.879 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:61-64]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:65:65 -->
- 💼 商业: ⭐5.9 | 如果美联储不加息，市场会替它加 | Wall Street CN [score=0.879 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:65-65]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:81:81 -->
- 🧠 AI 前沿: ⭐5.0 | 2026 年 6 月 Google AI 新闻汇总 | Google AI Blog [score=0.879 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:81-81]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:69:72 -->
- 🫂 社会: ⭐7.5 | 00 后本科生抱儿子参加毕业典礼 | 头条热榜; ⭐7.2 | BLG 对战 T1 这场比赛有多重要？一场 Bo5 保底前三！ — MSI 正赛首轮相遇，胜者有望直通胜决锁定前三。Knight 对 Faker、Bin 对 Doran 是关键对位 | 腾讯新闻; ⭐6.0 | 一考生因嫉妒篡改 7 人高考志愿，被判破坏计算机信息系统 — 教育部发布预警，提醒考生保护个人信息，严防志愿被篡改 | 知乎热榜; ⭐5.7 | 开启 2026 年 7 月：跟着 TODAY 健身挑战动起来 — 全身力量训练和夏日健康饮食建议 | NBC News Health [score=0.847 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:69-72]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:73:73 -->
- 🫂 社会: ⭐5.7 | ZYN 尼古丁袋比吸烟更安全吗？FDA 表态 — 机构授权称使用该产品比吸烟的健康风险更低 | NBC News Health [score=0.847 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:73-73]
<!-- openclaw-memory-promotion:memory:memory/2026-07-05-1141.md:77:80 -->
- 🧠 AI 前沿: ⭐7.4 | AI 大模型品牌数据监测平台发布 — 国家广告研究院 AI 品牌数据分析中心正式挂牌成立 | 中国广告论坛; ⭐7.3 | Agentic AI 测试新加坡治理能力 — 企业采用 AI Agent 提升生产力，但治理差距引发对控制和问责的质疑 | Singapore Business Review; ⭐7.2 | Benchmark Co. 维持 Datadog(DDOG.US)买入评级，目标价上调至 330 美元 | Moomoo; ⭐5.5 | 纽约市教育工作者和行业领袖齐聚 Google 办公室，共议 AI 课堂未来 | Google AI Blog [score=0.847 recalls=0 avg=0.620 source=memory/2026-07-05-1141.md:77-80]
