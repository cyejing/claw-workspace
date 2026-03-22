# 新闻源整合与分类功能 Spec

## Why

当前 news-aggregator-skill 只有国内和科技类新闻源，缺少国际新闻源。需要整合多个国际 RSS 资源，并增加分类参数让用户可以按类别获取新闻。

## What Changes

* 新增 6 个国际新闻源 fetch 函数：BBC、NPR、Al Jazeera、NYTimes、Guardian、WSJ

* 每个源支持多个分类 RSS 订阅

* 创建 sources\_map 分类映射（国内、国际、科技、财经、健康、政治、科学）

* main 入参加入 `--category` 参数支持按分类获取新闻

* **BREAKING** 无破坏性变更，`--source` 参数保持兼容

## Impact

* Affected code: `skills/news-aggregator-skill/scripts/fetch_news.py`

## ADDED Requirements

### Requirement: BBC RSS 新闻源集成

系统应支持从 BBC RSS 获取多分类新闻：

| 分类    | RSS URL                                                         |
| ----- | --------------------------------------------------------------- |
| 首页头条  | `https://feeds.bbci.co.uk/news/rss.xml`                         |
| 世界    | `https://feeds.bbci.co.uk/news/world/rss.xml`                   |
| 科技    | `https://feeds.bbci.co.uk/news/technology/rss.xml`              |
| 商业    | `https://feeds.bbci.co.uk/news/business/rss.xml`                |
| 科学与环境 | `https://feeds.bbci.co.uk/news/science_and_environment/rss.xml` |
| 健康    | `https://feeds.bbci.co.uk/news/health/rss.xml`                  |
| 娱乐与艺术 | `https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml`  |
| 政治    | `https://feeds.bbci.co.uk/news/politics/rss.xml`                |

### Requirement: NPR RSS 新闻源集成

系统应支持从 NPR RSS 获取多分类新闻：

| 分类 | RSS URL                              |
| -- | ------------------------------------ |
| 新闻 | `https://feeds.npr.org/1001/rss.xml` |
| 头条 | `https://feeds.npr.org/1002/rss.xml` |
| 国内 | `https://feeds.npr.org/1003/rss.xml` |
| 世界 | `https://feeds.npr.org/1004/rss.xml` |
| 商业 | `https://feeds.npr.org/1006/rss.xml` |
| 科学 | `https://feeds.npr.org/1007/rss.xml` |
| 政治 | `https://feeds.npr.org/1014/rss.xml` |
| 科技 | `https://feeds.npr.org/1019/rss.xml` |
| 太空 | `https://feeds.npr.org/1026/rss.xml` |

### Requirement: Al Jazeera RSS 新闻源集成

系统应支持从 Al Jazeera RSS 获取新闻：

* 全部新闻: `https://www.aljazeera.com/xml/rss/all.xml`

### Requirement: NYTimes RSS 新闻源集成

系统应支持从 NYTimes RSS 获取多分类新闻：

| 分类 | RSS URL                                                       |
| -- | ------------------------------------------------------------- |
| 首页 | `https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml`   |
| 世界 | `https://rss.nytimes.com/services/xml/rss/nyt/World.xml`      |
| 科技 | `https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml` |

### Requirement: The Guardian RSS 新闻源集成

系统应支持从 The Guardian RSS 获取新闻：

* 世界: `https://www.theguardian.com/world/rss`

### Requirement: WSJ RSS 新闻源集成

系统应支持从 WSJ RSS 获取财经新闻：

* 市场: `https://feeds.a.dj.com/rss/RSSMarketsMain.xml`

### Requirement: 新闻源分类

系统应支持按分类获取新闻，分类定义如下：

| 分类                 | 包含源                                                                           |
| ------------------ | ----------------------------------------------------------------------------- |
| domestic (国内)      | weibo, tencent, 36kr                                                          |
| international (国际) | bbc-world, npr-world, aljazeera, nytimes-world, guardian-world                |
| tech (科技)          | hackernews, github, v2ex, producthunt, bbc-tech, npr-tech, nytimes-tech, 36kr |
| finance (财经)       | wallstreetcn, bbc-business, npr-business, wsj, 36kr                           |
| health (健康)        | bbc-health                                                                    |
| politics (政治)      | bbc-politics, npr-politics                                                    |
| science (科学)       | bbc-science, npr-science, npr-space                                           |

### Requirement: 分类参数

系统应在 main 函数中支持 `--category` 参数：

* 支持值：domestic, international, tech, finance, health, politics, science, all

* 默认值：all

* 与 `--source` 参数可组合使用

#### Scenario: 使用分类参数

* **WHEN** 用户指定 `--category domestic`

* **THEN** 返回国内分类下所有新闻源的新闻

#### Scenario: 组合使用 source 和 category

* **WHEN** 用户指定 `--source bbc --category tech`

* **THEN** 返回 BBC 科技分类的新闻

