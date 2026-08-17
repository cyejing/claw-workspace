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

## Promoted From Short-Term Memory (2026-08-11)

<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:66:67 -->
- ⚙️ AI 基础设施: AMD 收购 Taalas 落地：将模型刻入硅片提升推理性能，"模型即芯片"路线获实质进展，多源同步报道; Agentic 工作负载挤压 CPU：亚马逊内部 EC2 CPU 需求激增、等待时间从小时延至天，Agentic AI 的 CPU-GPU 协同瓶颈显现 [score=0.831 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:66-67]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:41:43 -->
- 💼 商业: AI 债务狂潮遇冷：英伟达、亚马逊等科技巨头今年在美投资级债市融资超 2000 亿美元，新债普遍破发、二级市场走弱，华尔街开始重新审视 AI 基建融资的可持续性; AI 语音克隆入侵华尔街：黑客用 3 秒样本生成高度相似声音实施"语音钓鱼"，攻击成本降至几十美元且已产业化，金融、律所、医疗轮番陷落; OpenAI Astra 安全疑云：OpenAI 承认 Astra 尚未发布、无法排除其具备关键网络攻击能力，已发布初步网络安全评估 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:41-43]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:46:47 -->
- 🫂 社会: Anthropic 官宣造芯：首次确认组建内部芯片团队，最高 327 万年薪招揽芯片工程师，协同优化模型与硬件; 乌克兰防空危机：7 月俄发射 195 枚弹道导弹仅拦截 29 枚，泽连斯基紧急求援，美方称援乌致自身库存锐减 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:46-47]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:50:51 -->
- 🌍 国际: 泰国校园枪击：一名受霸凌青少年先杀祖父母、再枪杀 5 名教职工，震动泰国社会; 欧洲极端高温：多瑙河水位骤降暴露二战沉船、韩国热浪被定为"国家灾难"，气候议题持续升温 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:50-51]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:54:55 -->
- 🔬 科技: 字节 10 万亿参数大模型：TikTok 母公司训练参数规模达 10 万亿的模型，直接对标 Anthropic，中国大模型军备竞赛再升级; AI 创作悖论：WAIC 2026 上"10 万人排队、一键出片"背后，AI 让创作变简单却让爆款更难做，引发行业反思 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:54-55]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:58:59 -->
- 🐦 推特动态: Musk 叙事刷屏：多条高互动推文（"建墙的是坏人"2.6 万赞、Grok Build V1.0 发布、Terafab 香蕉类比），太空+AI 叙事持续霸榜; Altman 双线操作：一边详谈 HuggingFace "留言板"事件与模型对齐问题，一边祝贺 Oklo 核反应堆临界，OpenAI 安全与能源布局并进 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:58-59]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:62:63 -->
- 🧠 AI 前沿: Agentic AI 加速落地：Salesforce 数据显示 agent workforce 年增超一倍、部署周期缩短；Credo AI 警示"agent 部署即获全权是设计错误"，治理成为新焦点; ChatGPT 免费扩容：GPT-5.6 Sol 聊天体验提升、Luna 向免费用户开放无限聊天，AI 普惠化继续推进 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:62-63]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:71:71 -->
- 📌 今日总结: **AI 安全与治理成今日最强主线：** OpenAI 承认 Astra 模型潜在网络攻击能力、HuggingFace "留言板"对齐事件持续发酵，Credo AI 在伯克利峰会上警示"agent 部署即获全权是设计错误"——三条信号共同指向一个趋势：行业关注点正从"能力竞赛"快速转向"可控性与安全边界"，多源共振明显。 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:71-71]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:73:73 -->
- 📌 今日总结: **AI 基建融资现分化：** 一面是英伟达、亚马逊等巨头在债市融资超 2000 亿美元却遭遇新债破发、华尔街重新审视可持续性；另一面是 AMD 收购 Taalas、Anthropic 自研芯片、亚马逊 CPU 因 Agentic 负载告急——资本与算力都在从"通用堆量"转向"专用优化"，供需错配开始暴露。 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:73-73]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08-0135.md:75:75 -->
- 📌 今日总结: **中国大模型军备再升级：** 字节跳动 10 万亿参数模型浮出水面，直接对标 Anthropic；与此同时 AI 语音克隆已产业化入侵华尔街，显示中国 AI 应用与安全攻防同步进入实战阶段。 [score=0.801 recalls=0 avg=0.620 source=memory/2026-08-08-0135.md:75-75]

## Promoted From Short-Term Memory (2026-08-15)

<!-- openclaw-memory-promotion:memory:memory/2026-08-11-0106.md:26:29 -->
- 🫂 社会: iPhone物料成本: iPhone 18 Pro 物料成本预计同比大涨近40%，内存占比从10%飙升至34%，苹果面临毛利率压力; 🔥 哥伦比亚地震: 哥伦比亚7.4级地震，已致 Cali 市至少20栋建筑倒塌，与厄瓜多尔均有震感（RSS 与 API 同步报道）; FIFA信任危机: 欧足联、亚足联、中北美洲及加勒比海足联联名发公开信，指责国际足联主席因凡蒂诺欺骗破坏信任，目前因凡蒂诺已宣布竞选连任; 伯克希尔Q2: 伯克希尔Q2净利润256.67亿美元，时隔3年首次净买入股票，现金储备降至3655亿美元，回购约45亿美元库存股 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-11-0106.md:26-29]

## Promoted From Short-Term Memory (2026-08-16)

<!-- openclaw-memory-promotion:memory:memory/2026-08-11-1207.md:23:26 -->
- 🌍 国际: 加拿大野火：加拿大 Okanagan 地区周末爆发野火，迫使超过 12000 人撤离，居民担忧家园是否仍在; 地震：哥伦比亚 7.4 级地震至少已致 50 人死亡，震中距 San José del Palmar 约 5 公里; 特朗普与伊朗：Trump 拒绝 6 月 MOU 后，伊朗被指掌握主动权，筹码上升；制裁解除、停火等条件已不再适用，现在需谈赔偿与资产解冻; 30 年悬案：Tupac 遇害案时隔 30 年，一名昔日对手将接受审判 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-11-1207.md:23-26]
