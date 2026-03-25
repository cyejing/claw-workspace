# 数据源推荐计划 v4

## 任务目标

根据用户提供的详细数据源列表，验证 RSS 可用性后添加到 `sources.json`

***

## 实施步骤

### Step 1: 验证 RSS 可用性

使用用户提供的代理验证每个新增的 RSS 源：

```bash
export ALL_PROXY=socks5h://127.0.0.1:1080
export HTTP_PROXY=http://127.0.0.1:1080
export HTTPS_PROXY=http://127.0.0.1:1080
```

验证标准：

* URL 可访问 (HTTP 200)

* 返回有效 XML/JSON

* 有近期更新内容

### Step 2: 添加验证通过的数据源

将验证通过的数据源添加到 `sources.json`

### Step 3: 测试运行

运行 `fetch-rss.py` 验证新数据源能正常抓取

***

## 待验证数据源 (41 个)

### 国内科技类 (9个)

| ID            | 名称          | RSS URL                                  | 状态 |
| ------------- | ----------- | ---------------------------------------- | -- |
| solidot-rss   | Solidot     | `https://www.solidot.org/index.rss`      | 新增 |
| huxiu-rss     | 虎嗅网         | `https://www.huxiu.com/rss.xml`          | 新增 |
| pingwest-rss  | 品玩 PingWest | `https://www.pingwest.com/feed`          | 新增 |
| oschina-rss   | 开源中国        | `https://www.oschina.net/news/rss`       | 新增 |
| v2ex-rss      | V2EX 综合     | `https://www.v2ex.com/index.xml`         | 新增 |
| v2ex-hot-rss  | V2EX 热门     | `https://www.v2ex.com/feed/tab/hot.xml`  | 新增 |
| v2ex-tech-rss | V2EX 技术     | `https://www.v2ex.com/feed/tab/tech.xml` | 新增 |
| linuxdo-rss   | LinuxDo     | `https://linux.do/latest.rss`            | 新增 |
| juejin-rss    | 掘金          | `https://juejin.cn/rss`                  | 新增 |

### 国内财经类 (11个)

| ID               | 名称       | RSS URL                                          |
| ---------------- | -------- | ------------------------------------------------ |
| caixin-rss       | 财新网      | `https://www.caixin.com/feed/`                   |
| yicai-rss        | 第一财经     | `https://www.yicai.com/rss/home.xml`             |
| ftchinese-rss    | FT中文网    | `https://www.ftchinese.com/rss/news`             |
| wallstreetcn-rss | 华尔街见闻    | `https://wallstreetcn.com/rss/news`              |
| 21jingji-rss     | 21世纪经济报道 | `https://www.21jingji.com/rss.xml`               |
| eeo-rss          | 经济观察报    | `http://www.eeo.com.cn/rss/`                     |
| stcn-rss         | 证券时报     | `https://www.stcn.com/rss.xml`                   |
| nbd-rss          | 每日经济新闻   | `https://www.nbd.com.cn/rss.xml`                 |
| eastmoney-rss    | 东方财富网    | `https://www.eastmoney.com/rss/finance.xml`      |
| sina-finance-rss | 新浪财经     | `https://finance.sina.com.cn/rss/globalnews.xml` |
| fortunechina-rss | 财富中文网    | `https://www.fortunechina.com/rss/index.xml`     |

### 海外新闻类 (7个)

| ID                   | 名称     | RSS URL                                                     |
| -------------------- | ------ | ----------------------------------------------------------- |
| reuters-global-rss   | 路透社全球  | `https://www.reutersagency.com/feed/`                       |
| reuters-tech-rss     | 路透社科技  | `https://www.reuters.com/technology/feed`                   |
| reuters-markets-rss  | 路透社财经  | `https://www.reuters.com/markets/feed`                      |
| apnews-rss           | 美联社    | `https://apnews.com/rss/ap`                                 |
| cnn-rss              | CNN头条  | `http://rss.cnn.com/rss/cnn_topstories.rss`                 |
| nytimes-business-rss | 纽约时报财经 | `https://rss.nytimes.com/services/xml/rss/nyt/Business.xml` |
| wapo-rss             | 华盛顿邮报  | `http://feeds.washingtonpost.com/rss/homepage`              |

### 海外科技类 (6个)

| ID              | 名称          | RSS URL                            |
| --------------- | ----------- | ---------------------------------- |
| cnet-rss        | CNET        | `https://www.cnet.com/rss/news/`   |
| engadget-rss    | Engadget    | `https://www.engadget.com/rss.xml` |
| github-blog-rss | GitHub Blog | `https://github.blog/feed/`        |
| arxiv-ai-rss    | arXiv AI    | `https://rss.arxiv.org/rss/cs.AI`  |
| arxiv-ml-rss    | arXiv ML    | `https://rss.arxiv.org/rss/cs.LG`  |
| chengst-rss     | Cheng.st    | `https://cheng.st/atom.xml`        |

### 海外财经类 (9个)

| ID                | 名称            | RSS URL                                                |
| ----------------- | ------------- | ------------------------------------------------------ |
| bloomberg-rss     | 彭博社           | `https://www.bloomberg.com/feeds/bbiz/latest-news.rss` |
| ft-uk-rss         | 金融时报          | `https://www.ft.com/rss/home/uk`                       |
| economist-rss     | 经济学人          | `https://www.economist.com/rss/printedition`           |
| forbes-rss        | Forbes        | `https://www.forbes.com/feed/`                         |
| fortune-rss       | Fortune       | `https://fortune.com/feed/`                            |
| marketwatch-rss   | MarketWatch   | `https://www.marketwatch.com/rss/topstories`           |
| yahoo-finance-rss | Yahoo Finance | `https://finance.yahoo.com/news/rss`                   |
| barrons-rss       | Barron's      | `https://www.barrons.com/rss/`                         |
| investing-rss     | Investing.com | `https://www.investing.com/rss/news.rss`               |

***

## 已有数据源 (无需添加)

以下数据源已在 `sources.json` 中：

* BBC News: `https://feeds.bbci.co.uk/news/rss.xml` ✅

* 纽约时报首页: `https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml` ✅

* InfoQ中文: `https://www.infoq.cn/feed` ✅

***

## 验证方法

使用 curl 验证 RSS 可用性：

```bash
# 设置代理
export ALL_PROXY=socks5h://127.0.0.1:1080
export HTTP_PROXY=http://127.0.0.1:1080
export HTTPS_PROXY=http://127.0.0.1:1080

# 验证单个 RSS
curl -s -I "RSS_URL" | head -5
curl -s "RSS_URL" | head -20
```

验证通过标准：

* HTTP 状态码 200

* 返回内容包含 XML 声明或 RSS 标签

* 内容不为空

***

## 预期输出

验证完成后生成报告：

* ✅ 可用：添加到 sources.json

* ❌ 不可用：记录原因（403/404/超时/格式错误等）

