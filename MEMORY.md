# 记忆文档

## 安全规则
- ⚠️ **任何影响系统的操作都必须先征求用户同意**
- 包括但不限于：sudo 命令、删除文件、修改系统配置、网络操作等

## 输出格式偏好
- ⚠️ **重要传闻**相关输出：**列表格式**，不用表格（飞书表格不好查看）

## 用户偏好
- 🚫 **对加密货币不感兴趣** — 股票分析时只关注股票，过滤加密货币；新闻热点（news-hotspots）也已过滤：工作区配置 `<WORKSPACE>/config/news-hotspots-runtime.json` 的 `content_filters.blocked_keywords: ["比特币","bitcoin","btc"]`，在最终热点输出前剔除命中条目（2026-10-30 实测过滤 4 条、0 漏网）
- 🔥 **新闻热点查看** — 当用户说“查看今日新闻热点”时，使用news-hotspots技能

## 搜索后端优先级（2026-10-30 实测固化）
搜索需求按以下顺序调用，某一层失败就降级到下一层，直到拿到结果：
1. **web_search**（首选，后端 gemini grounding，中英文质量最高）
2. **Exa 搜索**（skills/shikamaru-web-search，免 key，返回原文高亮+发布时间，质量高；中英文都好，适合找文档/评测/深度内容）
3. **Bing CN**（web_fetch 抓 cn.bing.com/search；国际内容加 `&ensearch=1`）
4. **搜狗网页**（sogou.com/web）；查公众号文章用**搜狗微信**（wx.sogou.com/weixin?type=2&query=…）
5. **bb-browser 站点抓取**（google/news、zhihu/hot 等，走 Chrome 登录态；浏览器健康时用）
6. **scrapling-web-fetch**（反爬正文抓取；首次超时先重试一次再判定失败）
7. **360 搜索**（so.com，结果薄，仅作垫底兑底）
- ❌ 别浪费时间尝试：Google/DuckDuckGo 等国际引擎直连（网关拦截内网 IP 解析）、百度（验证码）
- 搜索结果可疑/后端疑似坏了 → 先跑 `search-backend-audit` 技能实测再选路
- 已删除的失效后端：online-search、universal-search、tavily、alibabacloud-iqs-search（需 ALIYUN_IQS_API_KEY，已删）、temp 备份已按老板指示清空（详见 2026-10-30 日记）

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

## Promoted From Short-Term Memory (2026-08-22)

<!-- openclaw-memory-promotion:memory:memory/2026-08-17-1240.md:30:33 -->
- 伯克希尔哈撒韦（巴菲特）: 🍎 苹果 $66.0B 22.0% —（无变化）; 💳 美国运通 $51.3B 17.1% —; 🥤 可口可乐 $32.5B 10.9% —; 🔍 Alphabet（谷歌） $37.8B 12.6% 🔼 **+45% / +658%** ← 本季最大动作 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-17-1240.md:30-33]

## Promoted From Short-Term Memory (2026-08-23)

<!-- openclaw-memory-promotion:memory:memory/2026-08-18-1911.md:26:26 -->
- 新增脚本: `scripts/check_bb_browser.py` — bb-browser 可用性探测，核心逻辑： [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-18-1911.md:26-26]

## Promoted From Short-Term Memory (2026-08-25)

<!-- openclaw-memory-promotion:memory:memory/2026-08-20-1923.md:22:22 -->
- 抓取概要句: 本次热点汇总：共抓取 90 篇文章，主要来源包括 Google 新闻（217→26篇）、RSS（387→20篇，1个订阅源部分失败）、Twitter（243→33篇）、API（29→4篇）、雪球（20→3篇）、今日头条（20→2篇）、知乎（20→2篇）、微博（20→2篇，全部成功）。 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20-1923.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-08-20-1923.md:28:31 -->
- 💼 商业: 🔥 **Anthropic IPO 前冲刺**：年化收入已突破 650 亿美元，较去年底增速提升逾七倍，IPO 前信贷融资金额也将突破百亿美元，创始团队获超级投票权以保持控制权; 🔥 **H200 出口松绑**：北京允许小批量 Nvidia H200 芯片进口，助头部科技集团追赶美国竞争对手; 🔥 **AI 泡沫 vs 铁路泡沫**：科技分析师以 19 世纪铁路泡沫类比当前 AI 热潮——资本链条可能先于回报断裂，电力基础设施或成泡沫破裂后最大遗产; 🔥 **债市风暴冲击 AI 供应链**：美欧日长债收益率逼近数十年高点，AI 相关发债规模已达 4890 亿美元，芯片股与数据中心股集体承压 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20-1923.md:28-31]

## Promoted From Short-Term Memory (2026-08-28)

<!-- openclaw-memory-promotion:memory:memory/2026-08-20-1923.md:39:42 -->
- ⚙️ AI 基础设施: 🔥 **Unitree 港股上市首日大涨**：全球最大人形机器人制造商登陆科创板，股票首日表现强劲; 🔥 **AMD 能效四倍提升**：2026 年中数据中心 AI 系统能效预计提升四倍，缓解算力耗电焦虑; AMD 最大规模发债 50 亿美元直投 Anthropic，Nvidia、微软同步押注; BlackBerry 获新设计订单：Momenta 和 XHEART 选用 QNX OS for Safety 作为自动驾驶平台底座 [score=0.842 recalls=0 avg=0.620 source=memory/2026-08-20-1923.md:39-42]

## Promoted From Short-Term Memory (2026-08-29)

<!-- openclaw-memory-promotion:memory:memory/2026-08-20-1923.md:43:43 -->
- ⚙️ AI 基础设施: 中国贵州数据中心的乡村化：欧洲风格建筑群中隐藏的低功耗数据中心，为 AI 提供电力 [score=0.804 recalls=0 avg=0.620 source=memory/2026-08-20-1923.md:43-43]
<!-- openclaw-memory-promotion:memory:memory/2026-08-24.md:12:12 -->
- AI 产业链: SpaceX Starship 第13次飞行完成回收，计划9月15日第14次并首次塔架捕获；年度第100次发射完成；宣布 Terafab 芯片项目 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-24.md:12-12]
<!-- openclaw-memory-promotion:memory:memory/2026-08-24.md:15:18 -->
- 中国楼市: 上海"沪八条"8月21日执行：外环外二套首付15%，购房补贴最高8万元; 北京：非京籍购房社保降至1年，公积金最高贷340万; LPR 5年期 3.5%（连续15个月未变）；公积金利率1月下调25BP; 海南安居房政策：100%产权，满5年可上市；多县购房补贴最高1.6万/套 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-24.md:15-18]
<!-- openclaw-memory-promotion:memory:memory/2026-08-24.md:4:5 -->
- 价值投资 SEC 13F（2026-08-14 申报）: 巴菲特：增持 Alphabet（+45%/658%），新建仓 D.R. Horton，清仓 Constellation Brands；现金储备 Q1 $3970亿 → Q2 $3650亿（开始净买入）; 段永平：减持英伟达 -55%、谷歌 -47%；增持拼多多 +27%（跃升第三大）；新建仓阿里巴巴；港股增持泡泡玛特至 7.7%（第二大股东） [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-24.md:4-5]
<!-- openclaw-memory-promotion:memory:memory/2026-08-24.md:8:11 -->
- AI 产业链: 谷歌云 Q1 增长 63%，完成 $320亿 Wiz 收购，2026年投入 $1750-1850亿; 英伟达 Blackwel/Rubin 需求上调至 $1万亿，2027年涨价 15%+，Q3 收入 $57B; HBM 市场规模 $546亿（+58%），美光全年售罄，SK海力士 59% 份额; 特斯拉 Cybercab 9月3日发布；Q2 交付 48万辆（+25%），运营利润降 57%；中国召回 300万辆 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-24.md:8-11]

## Promoted From Short-Term Memory (2026-08-31)

<!-- openclaw-memory-promotion:memory:memory/2026-08-20-1923.md:47:49 -->
- 🌍 国际: 🔥 **美加关税暂停**：特朗普在 50% 对加关税最后时刻宣布三天暂缓并声称接近达成协议，同时暗示重启 Keystone XL 输油管道; 🔥 **加拿大危机谈判**：加总理 Mark Carney 与美方展开"紧张"谈判，成功避免对 200 亿美元商品的冲击性关税; Vinted 误封争议：数千用户反映被错误封禁二手衣物交易平台账号，引发英国及欧洲多国投诉 [score=0.812 recalls=0 avg=0.620 source=memory/2026-08-20-1923.md:47-49]

## Promoted From Short-Term Memory (2026-09-02)

<!-- openclaw-memory-promotion:memory:memory/2026-08-20-1923.md:32:35 -->
- 💼 商业: 🔥 **高盛警告美联储两难**：债券供给压力空前叠加传统买家萎缩，长端利率被迫走高，美联储或被迫在数据走弱时仍加息; ABC 诉特朗普政府：ABC 正式起诉 FCC，指控其暂停电视执照威胁违反第一修正案; Cerebras 押注专用芯片：后 IPO 股价低迷，寄望专用芯片在 AI Agent 时代弯道超车; 西孟加拉酒店火灾：加尔各答五层酒店凌晨起火，9 人遇难、6 人受伤 [score=0.803 recalls=0 avg=0.620 source=memory/2026-08-20-1923.md:32-35]

## Promoted From Short-Term Memory (2026-09-07)

<!-- openclaw-memory-promotion:memory:memory/2026-09-02.md:11:13 -->
- 待办/后续关注: [ ] 关注 GPT-6 正式发布动态（预计9月3日）; [ ] 关注 Claude Fable 5.1 实际落地效果; [ ] 关注宇树科技后续舆情 [score=0.847 recalls=0 avg=0.620 source=memory/2026-09-02.md:11-13]
<!-- openclaw-memory-promotion:memory:memory/2026-09-02.md:5:7 -->
- 今日热点报告: Pipeline 正常运行：87篇，来源覆盖 RSS/API/Twitter/雪球/知乎; 主要热点：OpenAI Astra 发布（Critical 阈值）、Anthropic Fable 5.1 降价45%、GPT-6 即将灰测、NVIDIA 35亿美元投资 MediaTek、宇树管理争议、华为问界/小米销量; 本次报告由 cron 定时任务自动生成并投递 [score=0.847 recalls=0 avg=0.620 source=memory/2026-09-02.md:5-7]
