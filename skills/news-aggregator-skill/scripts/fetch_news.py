import argparse
import json
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ============ RSS 数据源 ============

# BBC - 英国广播公司
BBC_CATEGORIES = {
    'home': 'https://feeds.bbci.co.uk/news/rss.xml',
    'world': 'https://feeds.bbci.co.uk/news/world/rss.xml',
    'tech': 'https://feeds.bbci.co.uk/news/technology/rss.xml',
    'business': 'https://feeds.bbci.co.uk/news/business/rss.xml',
    'science': 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
    'health': 'https://feeds.bbci.co.uk/news/health/rss.xml',
    'entertainment': 'https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
    'politics': 'https://feeds.bbci.co.uk/news/politics/rss.xml',
}

# NPR - 美国国家公共广播电台
NPR_CATEGORIES = {
    'news': 'https://feeds.npr.org/1001/rss.xml',
    'home': 'https://feeds.npr.org/1002/rss.xml',
    'national': 'https://feeds.npr.org/1003/rss.xml',
    'world': 'https://feeds.npr.org/1004/rss.xml',
    'business': 'https://feeds.npr.org/1006/rss.xml',
    'science': 'https://feeds.npr.org/1007/rss.xml',
    'politics': 'https://feeds.npr.org/1014/rss.xml',
    'tech': 'https://feeds.npr.org/1019/rss.xml',
    'space': 'https://feeds.npr.org/1026/rss.xml',
}

# NYTimes - 纽约时报
NYTIMES_CATEGORIES = {
    'home': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'world': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'tech': 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
}

# Al Jazeera - 半岛电视台
ALJAZEERA_URL = 'https://www.aljazeera.com/xml/rss/all.xml'

# The Guardian - 卫报 (英国)
GUARDIAN_URL = 'https://www.theguardian.com/world/rss'

# WSJ - 华尔街日报
WSJ_URL = 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml'

# Product Hunt - 产品发现平台
PRODUCTHUNT_URL = 'https://www.producthunt.com/feed'

# ============ API 数据源 ============

# V2EX - 中文技术社区
V2EX_API = 'https://www.v2ex.com/api/topics/hot.json'

# Weibo - 新浪微博热搜
WEIBO_API = 'https://weibo.com/ajax/side/hotSearch'

# Wall Street CN - 华尔街见闻
WALLSTREETCN_API = 'https://api-one.wallstcn.com/apiv1/content/information-flow?channel=global-channel&accept=article&limit=30'

# Tencent News - 腾讯新闻
TENCENT_API = 'https://i.news.qq.com/web_backend/v2/getTagInfo?tagId=aEWqxLtdgmQ%3D'

# ============ 网页爬虫数据源 ============

# Hacker News - 科技新闻聚合
HACKERNEWS_URL = 'https://news.ycombinator.com'

# GitHub - 开源项目趋势
GITHUB_URL = 'https://github.com/trending'

# 36Kr - 中国科技财经媒体
KR36_URL = 'https://36kr.com/newsflashes'

# ============ 分类映射 ============

CATEGORIES = {
    'domestic': ['weibo', 'tencent', '36kr'],
    'international': ['bbc-world', 'npr-world', 'aljazeera', 'nytimes-world', 'guardian'],
    'tech': ['hackernews', 'github', 'v2ex', 'producthunt', 'bbc-tech', 'npr-tech', 'nytimes-tech', '36kr'],
    'finance': ['wallstreetcn', 'bbc-business', 'npr-business', 'wsj', '36kr'],
    'health': ['bbc-health'],
    'politics': ['bbc-politics', 'npr-politics'],
    'science': ['bbc-science', 'npr-science', 'npr-space'],
}

def parse_rss_feed(url, source_name, limit=5):
    headers = {"User-Agent": UA}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        root = ET.fromstring(response.content)
        channel = root.find('channel')
        if channel is None:
            return []
        items = []
        for item in channel.findall('item')[:limit]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')
            pub_elem = item.find('pubDate')
            title = title_elem.text if title_elem is not None else ""
            link = link_elem.text if link_elem is not None else ""
            desc = desc_elem.text if desc_elem is not None else ""
            pub_date = pub_elem.text if pub_elem is not None else ""
            items.append({
                "source": source_name,
                "title": title,
                "url": link,
                "time": pub_date,
                "heat": ""
            })
        return items
    except Exception as e:
        return []

def fetch_bbc(limit=5, category=None):
    if category and category in BBC_CATEGORIES:
        return parse_rss_feed(BBC_CATEGORIES[category], "BBC", limit)
    return parse_rss_feed(BBC_CATEGORIES['home'], "BBC", limit)

def fetch_npr(limit=5, category=None):
    if category and category in NPR_CATEGORIES:
        return parse_rss_feed(NPR_CATEGORIES[category], "NPR", limit)
    return parse_rss_feed(NPR_CATEGORIES['news'], "NPR", limit)

def fetch_aljazeera(limit=5):
    return parse_rss_feed(ALJAZEERA_URL, "Al Jazeera", limit)

def fetch_nytimes(limit=5, category=None):
    if category and category in NYTIMES_CATEGORIES:
        return parse_rss_feed(NYTIMES_CATEGORIES[category], "NYTimes", limit)
    return parse_rss_feed(NYTIMES_CATEGORIES['home'], "NYTimes", limit)

def fetch_guardian(limit=5):
    return parse_rss_feed(GUARDIAN_URL, "The Guardian", limit)

def fetch_wsj(limit=5):
    return parse_rss_feed(WSJ_URL, "WSJ", limit)

def fetch_producthunt(limit=5):
    headers = {"User-Agent": UA}
    try:
        response = requests.get(PRODUCTHUNT_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'xml')
        if not soup.find('item'): soup = BeautifulSoup(response.text, 'html.parser')

        items = []
        for entry in soup.find_all(['item', 'entry']):
            title = entry.find('title').get_text(strip=True)
            link_tag = entry.find('link')
            url = link_tag.get('href') or link_tag.get_text(strip=True) if link_tag else ""

            pubBox = entry.find('pubDate') or entry.find('published')
            pub = pubBox.get_text(strip=True) if pubBox else ""

            items.append({
                "source": "Product Hunt",
                "title": title,
                "url": url,
                "time": pub,
                "heat": "Top Product"
            })
        return items[:limit]
    except: return []

def fetch_v2ex(limit=5):
    headers = {"User-Agent": UA}
    try:
        data = requests.get(V2EX_API, headers=headers, timeout=10).json()
        items = []
        for t in data:
            replies = t.get('replies', 0)
            items.append({
                "source": "V2EX",
                "title": t['title'],
                "url": t['url'],
                "heat": f"{replies} replies",
                "time": "Hot"
            })
        return items[:limit]
    except: return []

def fetch_weibo(limit=5):
    headers = {"User-Agent": UA, "Referer": "https://weibo.com/"}
    try:
        response = requests.get(WEIBO_API, headers=headers, timeout=10)
        data = response.json()
        items = data.get('data', {}).get('realtime', [])

        all_items = []
        for item in items:
            title = item.get('note', '') or item.get('word', '')
            if not title: continue

            heat = item.get('num', 0)
            full_url = f"https://s.weibo.com/weibo?q={requests.utils.quote(title)}&Refer=top"

            all_items.append({
                "source": "Weibo Hot Search",
                "title": title,
                "url": full_url,
                "heat": f"{heat}",
                "time": "Real-time"
            })

        return all_items[:limit]
    except Exception as e:
        return []

def fetch_wallstreetcn(limit=5):
    headers = {"User-Agent": UA}
    try:
        data = requests.get(WALLSTREETCN_API, headers=headers, timeout=10).json()
        items = []
        for item in data['data']['items']:
            res = item.get('resource')
            if res and (res.get('title') or res.get('content_short')):
                 ts = res.get('display_time', 0)
                 time_str = datetime.fromtimestamp(ts).strftime('%H:%M') if ts else ""
                 items.append({
                     "source": "Wall Street CN",
                     "title": res.get('title') or res.get('content_short'),
                     "url": res.get('uri'),
                     "time": time_str
                 })
        return items[:limit]
    except: return []

def fetch_tencent(limit=5):
    headers = {"User-Agent": UA, "Referer": "https://news.qq.com/"}
    try:
        data = requests.get(TENCENT_API, headers=headers, timeout=10).json()
        items = []
        for news in data['data']['tabs'][0]['articleList']:
            items.append({
                "source": "Tencent News",
                "title": news['title'],
                "url": news.get('url') or news.get('link_info', {}).get('url'),
                "time": news.get('pub_time', '') or news.get('publish_time', '')
            })
        return items[:limit]
    except:
        return []

def fetch_hackernews(limit=5):
    headers = {"User-Agent": UA}
    try:
        response = requests.get(HACKERNEWS_URL, headers=headers, timeout=10)
        if response.status_code != 200: return []
    except: return []

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('.athing')

    items = []
    for row in rows:
        try:
            id_ = row.get('id')
            title_line = row.select_one('.titleline a')
            if not title_line: continue
            title = title_line.get_text()
            link = title_line.get('href')

            score_span = soup.select_one(f'#score_{id_}')
            score = score_span.get_text() if score_span else "0 points"

            age_span = soup.select_one(f'.age a[href="item?id={id_}"]')
            time_str = age_span.get_text() if age_span else ""

            if link and link.startswith('item?id='): link = f"{HACKERNEWS_URL}/{link}"

            items.append({
                "source": "Hacker News",
                "title": title,
                "url": link,
                "heat": score,
                "time": time_str
            })
        except: continue

    return items[:limit]

def fetch_github(limit=5):
    headers = {"User-Agent": UA}
    try:
        response = requests.get(GITHUB_URL, headers=headers, timeout=10)
    except: return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    for article in soup.select('article.Box-row'):
        try:
            h2 = article.select_one('h2 a')
            if not h2: continue
            title = h2.get_text(strip=True).replace('\n', '').replace(' ', '')
            link = "https://github.com" + h2['href']

            desc = article.select_one('p')
            desc_text = desc.get_text(strip=True) if desc else ""

            stars_tag = article.select_one('a[href$="/stargazers"]')
            stars = stars_tag.get_text(strip=True) if stars_tag else ""

            items.append({
                "source": "GitHub Trending",
                "title": f"{title} - {desc_text}",
                "url": link,
                "heat": f"{stars} stars",
                "time": "Today"
            })
        except: continue
    return items[:limit]

def fetch_36kr(limit=5):
    headers = {"User-Agent": UA}
    try:
        response = requests.get(KR36_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        for item in soup.select('.newsflash-item'):
            title = item.select_one('.item-title').get_text(strip=True)
            href = item.select_one('.item-title')['href']
            time_tag = item.select_one('.time')
            time_str = time_tag.get_text(strip=True) if time_tag else ""

            items.append({
                "source": "36Kr",
                "title": title,
                "url": f"https://36kr.com{href}" if not href.startswith('http') else href,
                "time": time_str,
                "heat": ""
            })
        return items[:limit]
    except: return []

def get_source_func(source_key):
    source_map = {
        'hackernews': lambda l: fetch_hackernews(l),
        'weibo': lambda l: fetch_weibo(l),
        'github': lambda l: fetch_github(l),
        '36kr': lambda l: fetch_36kr(l),
        'v2ex': lambda l: fetch_v2ex(l),
        'tencent': lambda l: fetch_tencent(l),
        'wallstreetcn': lambda l: fetch_wallstreetcn(l),
        'producthunt': lambda l: fetch_producthunt(l),
        'bbc': lambda l: fetch_bbc(l),
        'bbc-world': lambda l: fetch_bbc(l, 'world'),
        'bbc-tech': lambda l: fetch_bbc(l, 'tech'),
        'bbc-business': lambda l: fetch_bbc(l, 'business'),
        'bbc-science': lambda l: fetch_bbc(l, 'science'),
        'bbc-health': lambda l: fetch_bbc(l, 'health'),
        'bbc-politics': lambda l: fetch_bbc(l, 'politics'),
        'npr': lambda l: fetch_npr(l),
        'npr-world': lambda l: fetch_npr(l, 'world'),
        'npr-tech': lambda l: fetch_npr(l, 'tech'),
        'npr-business': lambda l: fetch_npr(l, 'business'),
        'npr-science': lambda l: fetch_npr(l, 'science'),
        'npr-politics': lambda l: fetch_npr(l, 'politics'),
        'npr-space': lambda l: fetch_npr(l, 'space'),
        'aljazeera': lambda l: fetch_aljazeera(l),
        'nytimes': lambda l: fetch_nytimes(l),
        'nytimes-world': lambda l: fetch_nytimes(l, 'world'),
        'nytimes-tech': lambda l: fetch_nytimes(l, 'tech'),
        'guardian': lambda l: fetch_guardian(l),
        'wsj': lambda l: fetch_wsj(l),
    }
    return source_map.get(source_key)

def main():
    parser = argparse.ArgumentParser(description='Fetch news from various sources')
    parser.add_argument('--source', default='all', help='Source(s) to fetch from (comma-separated)')
    parser.add_argument('--category', default=None, help='Category to fetch (domestic, international, tech, finance, health, politics, science)')
    parser.add_argument('--limit', type=int, default=10, help='Limit per source. Default 10')

    args = parser.parse_args()

    sources_to_run = []

    if args.category:
        category = args.category.lower()
        if category in CATEGORIES:
            sources_to_run = CATEGORIES[category]
        else:
            print(f"Unknown category: {category}")
            return

        if args.source != 'all':
            requested = [s.strip() for s in args.source.split(',')]
            sources_to_run = [s for s in sources_to_run if s in requested or s.split('-')[0] in requested]
    elif args.source != 'all':
        sources_to_run = [s.strip() for s in args.source.split(',')]
    else:
        sources_to_run = ['hackernews', 'weibo', 'github', '36kr', 'v2ex', 'tencent', 'wallstreetcn', 'producthunt',
                          'bbc', 'npr', 'aljazeera', 'nytimes', 'guardian', 'wsj']

    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_src = {}
        for src in sources_to_run:
            func = get_source_func(src)
            if func:
                future_to_src[executor.submit(func, args.limit)] = src

        for future in as_completed(future_to_src):
            src = future_to_src[future]
            try:
                fetched = future.result()
                results.extend(fetched)
            except Exception as e:
                print(f"Error fetching from {src}: {e}")

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
