---
name: bb-browser
description: 强大的信息获取与浏览器自动化工具。通过浏览器 + 用户登录态，获取 site 网页数据（36 平台 103 命令一键调用）、带登录态的 fetch、网络请求拦截与 mock、操作录制等高级功能。
allowed-tools: Bash(bb-browser:*)
---

# bb-browser sites 用法 —— 网页即命令行

36 个平台，103 个命令。使用您的登录状态，从任何网站获取一行结构化数据。

## 快速开始

```bash
bb-browser site update                              # 首次使用：拉取社区适配器
bb-browser site list                                # 查看所有适配器
bb-browser site recommend                           # 查看与浏览习惯匹配的适配器
bb-browser site info xueqiu/stock                   # 查看适配器参数

bb-browser site reddit/hot
bb-browser site hackernews/top 5
bb-browser site v2ex/hot
bb-browser site twitter/search "AI agent"
bb-browser site zhihu/hot 10 --json
bb-browser site xueqiu/hot-stock 5 --jq '.items[] | {name, changePercent}'
```

## 数据提取示例

```bash
bb-browser site twitter/search "AI agent"
bb-browser site twitter/thread <tweet-url>
bb-browser site reddit/thread <post-url>
bb-browser site weibo/hot
bb-browser site xiaohongshu/search "query"
bb-browser site github/repo owner/repo
bb-browser site github/issues owner/repo
bb-browser site hackernews/top 10
bb-browser site stackoverflow/search "async await"
bb-browser site arxiv/search "transformer"
bb-browser site xueqiu/stock SH600519
bb-browser site xueqiu/hot-stock 5
bb-browser site eastmoney/stock "茅台"
bb-browser site zhihu/hot
bb-browser site 36kr/newsflash
bb-browser site wikipedia/summary "Python"
bb-browser site youtube/transcript VIDEO_ID
bb-browser site bilibili/search "query"
```

## --jq 过滤数据

```bash
bb-browser site xueqiu/hot-stock 5 -jq '.items[].name'
bb-browser site xueqiu/hot-stock 5 -jq '.items[] | {name, changePercent, heat}'
bb-browser site reddit/hot -jq '.posts[] | {title, score}'
```

## 查看适配器详情

```bash
# 检查适配器需要哪些参数
bb-browser site info xueqiu/stock

# 按关键词搜索适配器
bb-browser site search reddit
```

## 登录状态

适配器在浏览器标签页中运行。如果网站需要登录：

1. 适配器返回 `{"error": "HTTP 401", "hint": "Not logged in?"}`
2. 在浏览器窗口中手动登录
3. 重试命令

## 创建新适配器

```bash
bb-browser guide                                    # 阅读开发指南
```

或直接告诉我："将 notion.so 变成 bb-browser 适配器"，我会逆向工程 API，编写适配器。

## 全部 36 个平台

| 类别   | 平台                                                                            |
| ------ | ------------------------------------------------------------------------------- |
| 搜索   | Google、百度、Bing、DuckDuckGo、搜狗微信                                        |
| 社交   | Twitter/X、Reddit、微博、小红书、即刻、LinkedIn、虎扑                           |
| 新闻   | BBC、Reuters、36氪、头条、东方财富                                              |
| 开发者 | GitHub、StackOverflow、HackerNews、CSDN、博客园、V2EX、Dev.to、npm、PyPI、arXiv |
| 视频   | YouTube、哔哩哔哩                                                               |
| 娱乐   | 豆瓣、IMDb、Genius、起点                                                        |
| 金融   | 雪球、东方财富、Yahoo Finance                                                   |
| 招聘   | BOSS 直聘、LinkedIn                                                             |
| 知识   | Wikipedia、知乎、Open Library                                                   |
| 购物   | 什么值得买                                                                      |
| 工具   | 有道、GSMArena、Product Hunt、携程                                              |

# bb-browser 命令用法

详细命令指南见 [references/commands-guide.md](references/commands-guide.md)。

## 深入文档

| 文档                                                                   | 说明                                                     |
| ---------------------------------------------------------------------- | -------------------------------------------------------- |
| [references/commands-guide.md](references/commands-guide.md)           | 命令完整指南：导航、快照、元素交互、Tab 管理、网络调试   |
| [references/site-system.md](references/site-system.md)                 | Site 系统完整指南：35 平台列表、命令用法、自动 tab 管理  |
| [references/adapter-development.md](references/adapter-development.md) | 网页适配器开发指南：API 逆向、三层复杂度、元数据格式     |
| [references/fetch-and-network.md](references/fetch-and-network.md)     | Fetch 与 Network 高级功能：带登录态请求、请求拦截与 mock |
| [references/snapshot-refs.md](references/snapshot-refs.md)             | Ref 生命周期、最佳实践、常见问题                         |
