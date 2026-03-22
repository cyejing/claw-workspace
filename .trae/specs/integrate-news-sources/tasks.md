# Tasks

- [x] Task 1: 创建通用 RSS 解析函数
  - [x] SubTask 1.1: 创建 `parse_rss_feed(url, source_name, limit)` 函数

- [x] Task 2: 添加 BBC RSS fetch 函数
  - [x] SubTask 2.1: 创建 `fetch_bbc(limit=5, category=None)` 函数支持多分类

- [x] Task 3: 添加 NPR RSS fetch 函数
  - [x] SubTask 3.1: 创建 `fetch_npr(limit=5, category=None)` 函数支持多分类

- [x] Task 4: 添加 Al Jazeera RSS fetch 函数
  - [x] SubTask 4.1: 创建 `fetch_aljazeera(limit=5)` 函数

- [x] Task 5: 添加 NYTimes RSS fetch 函数
  - [x] SubTask 5.1: 创建 `fetch_nytimes(limit=5, category=None)` 函数支持多分类

- [x] Task 6: 添加 The Guardian RSS fetch 函数
  - [x] SubTask 6.1: 创建 `fetch_guardian(limit=5)` 函数

- [x] Task 7: 添加 WSJ RSS fetch 函数
  - [x] SubTask 7.1: 创建 `fetch_wsj(limit=5)` 函数

- [x] Task 8: 创建分类映射
  - [x] SubTask 8.1: 定义各源分类映射 (BBC_CATEGORIES, NPR_CATEGORIES, NYTIMES_CATEGORIES)
  - [x] SubTask 8.2: 定义全局分类映射 `CATEGORIES` 映射分类到源列表
  - [x] SubTask 8.3: 更新 sources_map 包含新源

- [x] Task 9: 添加 --category 参数
  - [x] SubTask 9.1: 在 argparse 添加 --category 参数
  - [x] SubTask 9.2: 实现分类到源的转换逻辑
  - [x] SubTask 9.3: 处理 --source 和 --category 组合逻辑

- [x] Task 10: 测试验证
  - [x] SubTask 10.1: 测试各个新源是否能正常获取数据
  - [x] SubTask 10.2: 测试 --category 参数各分类
  - [x] SubTask 10.3: 测试 --source + --category 组合

# Task Dependencies
- [Task 2, 3, 4, 5, 6, 7] depends on [Task 1]
- [Task 8] depends on [Task 2, 3, 4, 5, 6, 7]
- [Task 9] depends on [Task 8]
- [Task 10] depends on [Task 9]
