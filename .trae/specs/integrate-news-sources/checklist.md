# Checklist

## BBC RSS
- [x] fetch_bbc 函数能正常返回 BBC RSS 新闻
- [x] fetch_bbc --category world 返回世界新闻
- [x] fetch_bbc --category tech 返回科技新闻
- [x] fetch_bbc --category business 返回商业新闻
- [x] fetch_bbc --category science 返回科学新闻
- [x] fetch_bbc --category health 返回健康新闻
- [x] fetch_bbc --category politics 返回政治新闻

## NPR RSS
- [x] fetch_npr 函数能正常返回 NPR RSS 新闻
- [x] fetch_npr --category world 返回世界新闻
- [x] fetch_npr --category tech 返回科技新闻
- [x] fetch_npr --category business 返回商业新闻
- [x] fetch_npr --category science 返回科学新闻
- [x] fetch_npr --category politics 返回政治新闻

## Al Jazeera RSS
- [x] fetch_aljazeera 函数能正常返回 Al Jazeera RSS 新闻

## NYTimes RSS
- [x] fetch_nytimes 函数能正常返回 NYTimes RSS 新闻
- [x] fetch_nytimes --category world 返回世界新闻
- [x] fetch_nytimes --category tech 返回科技新闻

## The Guardian RSS
- [x] fetch_guardian 函数能正常返回 Guardian RSS 新闻

## WSJ RSS
- [x] fetch_wsj 函数能正常返回 WSJ RSS 新闻

## 分类映射
- [x] CATEGORIES 字典包含 domestic, international, tech, finance, health, politics, science 分类
- [x] --category 参数支持所有分类值
- [x] --category domestic 返回 weibo, tencent, 36kr 新闻
- [x] --category international 返回 bbc-world, npr-world, aljazeera, nytimes-world, guardian-world 新闻
- [x] --category tech 返回 hackernews, github, v2ex, producthunt, bbc-tech, npr-tech, nytimes-tech, 36kr 新闻
- [x] --category finance 返回 wallstreetcn, bbc-business, npr-business, wsj, 36kr 新闻

## 组合参数
- [x] --source bbc --category tech 返回 BBC 科技新闻
- [x] --source npr --category finance 返回 NPR 商业新闻
- [x] --source 参数仍然正常工作（无 category 时返回默认分类）
