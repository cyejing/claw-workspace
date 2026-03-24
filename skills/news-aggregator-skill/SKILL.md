---
name: news-aggregator-skill
description: "综合新闻聚合器，从 14 大来源获取热点新闻：Hacker News、GitHub Trending、Product Hunt、36Kr、腾讯新闻、华尔街见闻、V2EX、微博、BBC、NPR、NYTimes、Al Jazeera、The Guardian、WSJ。支持按分类（国内、国际、科技、财经、健康、政治、科学）筛选。"
---

# 新闻聚合器技能

从多个来源获取实时热点新闻，支持分类筛选。

## 工具

### 依赖安装

```bash
uv sync
```

### fetch_news.py

**用法：**

```bash
# 全局扫描 - 获取所有来源的热点
uv run scripts/fetch_news.py --source all --limit 15

# 按分类获取
uv run scripts/fetch_news.py --category tech --limit 10
uv run scripts/fetch_news.py --category finance --limit 10
uv run scripts/fetch_news.py --category international --limit 10

# 单一来源
uv run scripts/fetch_news.py --source hackernews --limit 20
uv run scripts/fetch_news.py --source bbc-tech --limit 10
uv run scripts/fetch_news.py --source npr-world --limit 10
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--source` | 来源（见下方列表），支持逗号分隔多选，默认 `all` |
| `--category` | 分类：`domestic`、`international`、`tech`、`finance`、`health`、`politics`、`science` |
| `--limit` | 每个来源的最大条目数（默认 10） |

### 数据源列表

| 来源标识 | 说明 | 类型 |
|---------|------|------|
| `hackernews` | Hacker News 科技新闻 | 网页爬虫 |
| `github` | GitHub Trending 开源趋势 | 网页爬虫 |
| `weibo` | 微博热搜 | API |
| `tencent` | 腾讯新闻 | API |
| `36kr` | 36Kr 科技财经快讯 | 网页爬虫 |
| `v2ex` | V2EX 热门话题 | API |
| `wallstreetcn` | 华尔街见闻 | API |
| `producthunt` | Product Hunt 产品发现 | RSS |
| `bbc` | BBC 新闻首页 | RSS |
| `bbc-world` | BBC 国际新闻 | RSS |
| `bbc-tech` | BBC 科技新闻 | RSS |
| `bbc-business` | BBC 商业新闻 | RSS |
| `bbc-science` | BBC 科学新闻 | RSS |
| `bbc-health` | BBC 健康新闻 | RSS |
| `bbc-politics` | BBC 政治新闻 | RSS |
| `npr` | NPR 新闻首页 | RSS |
| `npr-world` | NPR 国际新闻 | RSS |
| `npr-tech` | NPR 科技新闻 | RSS |
| `npr-business` | NPR 商业新闻 | RSS |
| `npr-science` | NPR 科学新闻 | RSS |
| `npr-politics` | NPR 政治新闻 | RSS |
| `npr-space` | NPR 太空新闻 | RSS |
| `nytimes` | 纽约时报首页 | RSS |
| `nytimes-world` | 纽约时报国际 | RSS |
| `nytimes-tech` | 纽约时报科技 | RSS |
| `aljazeera` | 半岛电视台 | RSS |
| `guardian` | 卫报国际新闻 | RSS |
| `wsj` | 华尔街日报市场 | RSS |

### 分类映射

| 分类 | 包含来源 |
|------|---------|
| `domestic` (国内) | weibo, tencent, 36kr |
| `international` (国际) | bbc-world, npr-world, aljazeera, nytimes-world, guardian |
| `tech` (科技) | hackernews, github, v2ex, producthunt, bbc-tech, npr-tech, nytimes-tech, 36kr |
| `finance` (财经) | wallstreetcn, bbc-business, npr-business, wsj, 36kr |
| `health` (健康) | bbc-health |
| `politics` (政治) | bbc-politics, npr-politics |
| `science` (科学) | bbc-science, npr-science, npr-space |

### 输出格式

```json
[
  {
    "source": "Hacker News",
    "title": "Show HN: A new approach to...",
    "url": "https://example.com/article",
    "heat": "256 points",
    "time": "2 hours ago"
  }
]
```

## 交互式菜单

当用户说 "如意如意" 或类似的"菜单/帮助"触发词 时：
1. 读取 `templates.md` 内容
2. 展示可用命令列表
3. 引导用户选择执行

## 智能时间过滤与报告（关键）

当用户请求特定时间窗口（如"过去 X 小时"）且结果稀少（< 5 条）时：

1. **优先用户窗口**：首先列出严格落在用户请求时间内的所有条目
2. **智能填充**：如果列表较短，必须包含更广范围（如过去 24 小时）的高价值/高热度条目，确保报告至少提供 5 条有意义的洞察
3. **标注**：清晰标记较旧条目（如 "⚠️ 18小时前"、"🔥 24小时热门"），让用户知道是补充内容
4. **高价值优先**：始终优先考虑"SOTA"、"重大发布"或"高热度"条目，即使略微超出时间窗口

**GitHub Trending 例外**：对于纯列表形式的来源（如 GitHub Trending），严格返回获取列表中的有效条目（前 10 条）。**列出所有获取的条目**，**不执行智能填充**。

每条需进行**深度分析（必需）**：
- **核心价值**：解决了什么具体问题？为什么流行？
- **启发思考**：可以得出什么技术或产品洞察？
- **场景标签**：3-5 个关键词（如 `#RAG #LocalFirst #Rust`）

## 响应指南（关键）

### 内容抓取

如需深度分析某篇文章，使用网页抓取技能（如 `scrapling-web-fetch`）提取正文内容。

### 格式与风格

- **语言**：简体中文
- **风格**：杂志/通讯风格（如"经济学人"、"Morning Brew"），专业、简洁、引人入胜
- **结构**：
  - **全球头条**：跨所有领域最重要的 3-5 条新闻
  - **科技与 AI**：AI、LLM 和科技条目的专门板块
  - **财经/社交**：其他相关的重要类别

### 条目格式

- **标题**：**必须是 Markdown 链接**，指向原始 URL
  - ✅ 正确：`### 1. [OpenAI 发布 GPT-5](https://...)`
  - ❌ 错误：`### 1. OpenAI 发布 GPT-5`
- **元数据行**：必须包含来源、**时间/日期**和热度/评分
- **一句话摘要**：有力的"那又怎样"式摘要
- **深度解读**：2-3 个要点解释为什么重要、技术细节或背景

### 输出产物

- 始终将完整报告保存到 `reports/` 目录，使用带时间戳的文件名（如 `reports/hn_news_YYYYMMDD_HHMM.md`）
- 在聊天中向用户展示完整报告内容
