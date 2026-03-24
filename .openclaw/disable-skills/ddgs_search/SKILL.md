---
name: ddgs-search
description: 当用户需要搜索网络信息、查找当前内容、搜索新闻文章、图片或视频时使用此技能。使用 DuckDuckGo 搜索 API 返回格式化的结果（文本、Markdown 或 JSON）。适用于研究、事实核查、查找最新信息或收集网络资源。
---

# 网络搜索

## 概述

使用 DuckDuckGo 的 API 搜索网络，查找网页、新闻文章、图片和视频。返回多种格式（文本、Markdown、JSON），支持时间范围、地区和安全搜索过滤选项。

## 使用场景

当用户请求以下内容时使用此技能：
- 搜索网络信息或资源
- 查找当前或最新信息
- 搜索特定主题的新闻文章
- 按描述或主题搜索图片
- 搜索特定主题的视频
- 需要当前网络数据的研究
- 使用网络来源进行事实核查或验证
- 收集某主题的 URL 和资源

## 前置条件

安装所需依赖：

```bash
uv sync
```

此库提供简单的 Python 接口访问 DuckDuckGo 搜索 API，无需 API 密钥或认证。

## 核心功能

### 1. 基础网页搜索

搜索网页和信息：

```bash
uv run scripts/search.py "<查询词>"
```

**示例：**
```bash
uv run scripts/search.py "python asyncio 教程"
```

返回前 10 条网页结果，包含标题、URL 和描述，格式为清晰的文本。

### 2. 限制结果数量

控制返回的结果数量：

```bash
uv run scripts/search.py "<查询词>" --max-results <N>
```

**示例：**
```bash
uv run scripts/search.py "机器学习框架" --max-results 20
```

适用于：
- 获取更全面的结果（增加限制）
- 快速查找少量结果（减少限制）
- 平衡详细程度与处理时间

### 3. 时间范围过滤

按时间筛选结果：

```bash
uv run scripts/search.py "<查询词>" --time-range <d|w|m|y>
```

**时间范围选项：**
- `d` - 过去一天
- `w` - 过去一周
- `m` - 过去一月
- `y` - 过去一年

**示例：**
```bash
uv run scripts/search.py "人工智能新闻" --time-range w
```

适用于：
- 查找最新新闻或更新
- 过滤过时内容
- 追踪最新动态

### 4. 新闻搜索

专门搜索新闻文章：

```bash
uv run scripts/search.py "<查询词>" --type news
```

**示例：**
```bash
uv run scripts/search.py "气候变化" --type news --time-range w --max-results 15
```

新闻结果包含：
- 文章标题
- 来源媒体
- 发布日期
- URL
- 文章摘要/描述

### 5. 图片搜索

搜索图片：

```bash
uv run scripts/search.py "<查询词>" --type images
```

**示例：**
```bash
uv run scripts/search.py "山间日落" --type images --max-results 20
```

**图片过滤选项：**

尺寸过滤：
```bash
uv run scripts/search.py "风景照片" --type images --image-size Large
```
选项：`Small`、`Medium`、`Large`、`Wallpaper`

颜色过滤：
```bash
uv run scripts/search.py "抽象艺术" --type images --image-color Blue
```
选项：`color`、`Monochrome`、`Red`、`Orange`、`Yellow`、`Green`、`Blue`、`Purple`、`Pink`、`Brown`、`Black`、`Gray`、`Teal`、`White`

类型过滤：
```bash
uv run scripts/search.py "图标" --type images --image-type transparent
```
选项：`photo`、`clipart`、`gif`、`transparent`、`line`

布局过滤：
```bash
uv run scripts/search.py "壁纸" --type images --image-layout Wide
```
选项：`Square`、`Tall`、`Wide`

图片结果包含：
- 图片标题
- 图片 URL（直接链接）
- 缩略图 URL
- 来源网站
- 尺寸（宽 x 高）

### 6. 视频搜索

搜索视频：

```bash
uv run scripts/search.py "<查询词>" --type videos
```

**示例：**
```bash
uv run scripts/search.py "python 教程" --type videos --max-results 15
```

**视频过滤选项：**

时长过滤：
```bash
uv run scripts/search.py "烹饪食谱" --type videos --video-duration short
```
选项：`short`、`medium`、`long`

分辨率过滤：
```bash
uv run scripts/search.py "纪录片" --type videos --video-resolution high
```
选项：`high`、`standard`

视频结果包含：
- 视频标题
- 发布者/频道
- 时长
- 发布日期
- 视频 URL
- 描述

### 7. 地区特定搜索

按地区搜索：

```bash
uv run scripts/search.py "<查询词>" --region <地区代码>
```

**常用地区代码：**

| 代码 | 地区 |
|------|------|
| `wt-wt` | 全球（默认） |
| `us-en` | 美国（英语） |
| `uk-en` | 英国（英语） |
| `cn-zh` | 中国（中文） |
| `ca-en` | 加拿大（英语） |
| `au-en` | 澳大利亚（英语） |
| `de-de` | 德国（德语） |
| `fr-fr` | 法国（法语） |
| `jp-jp` | 日本（日语） |

**示例：**
```bash
uv run scripts/search.py "本地新闻" --region us-en --type news
```

### 8. 安全搜索控制

控制安全搜索过滤：

```bash
uv run scripts/search.py "<查询词>" --safe-search <on|moderate|off>
```

**选项：**
- `on` - 严格过滤
- `moderate` - 平衡过滤（默认）
- `off` - 不过滤

**示例：**
```bash
uv run scripts/search.py "医疗信息" --safe-search on
```

### 9. 输出格式

选择结果格式：

**文本格式（默认）：**
```bash
uv run scripts/search.py "量子计算"
```

清晰可读的纯文本，带编号结果。

**Markdown 格式：**
```bash
uv run scripts/search.py "量子计算" --format markdown
```

格式化的 Markdown，包含标题、粗体文本和链接。

**JSON 格式：**
```bash
uv run scripts/search.py "量子计算" --format json
```

结构化 JSON 数据，便于程序处理。

### 10. 保存结果到文件

保存搜索结果到文件：

```bash
uv run scripts/search.py "<查询词>" --output <文件路径>
```

**示例：**
```bash
uv run scripts/search.py "人工智能" --output ai_results.txt
uv run scripts/search.py "AI 新闻" --type news --format markdown --output ai_news.md
uv run scripts/search.py "AI 研究" --format json --output ai_data.json
```

文件格式由 `--format` 参数决定，而非文件扩展名。

## 输出格式示例

### 文本格式
```
1. 页面标题
   URL: https://example.com/page
   页面内容简介...

2. 另一个结果
   URL: https://example.com/another
   另一个描述...
```

### Markdown 格式
```markdown
## 1. 页面标题

**URL:** https://example.com/page

页面内容简介...

## 2. 另一个结果

**URL:** https://example.com/another

另一个描述...
```

### JSON 格式
```json
[
  {
    "title": "页面标题",
    "href": "https://example.com/page",
    "body": "页面内容简介..."
  },
  {
    "title": "另一个结果",
    "href": "https://example.com/another",
    "body": "另一个描述..."
  }
]
```

## 常见使用模式

### 主题研究

收集某主题的全面信息：

```bash
# 获取网页概览
uv run scripts/search.py "机器学习基础" --max-results 15 --output ml_web.txt

# 获取最新新闻
uv run scripts/search.py "机器学习" --type news --time-range m --output ml_news.txt

# 查找教程视频
uv run scripts/search.py "机器学习教程" --type videos --max-results 10 --output ml_videos.txt
```

### 时事监控

追踪特定主题的新闻：

```bash
uv run scripts/search.py "气候峰会" --type news --time-range d --format markdown --output daily_climate_news.md
```

### 查找视觉资源

按特定条件搜索图片：

```bash
uv run scripts/search.py "数据可视化示例" --type images --image-type photo --image-size Large --max-results 25 --output viz_images.txt
```

### 事实核查

用最新来源验证信息：

```bash
uv run scripts/search.py "待验证的具体说法" --time-range w --max-results 20
```

### 学术研究

查找学术主题资源：

```bash
uv run scripts/search.py "量子纠缠研究" --time-range y --max-results 30 --output quantum_research.txt
```

### 市场调研

收集产品或公司信息：

```bash
uv run scripts/search.py "电动汽车市场 2025" --max-results 20 --format markdown --output ev_market.md
uv run scripts/search.py "EV 新闻" --type news --time-range m --output ev_news.txt
```

## 实现方法

当用户请求网络搜索时：

1. **识别搜索意图**：
   - 需要什么类型的内容（网页、新闻、图片、视频）？
   - 结果需要多新？
   - 需要多少结果？
   - 有过滤需求吗？

2. **配置搜索参数**：
   - 选择合适的搜索类型（`--type`）
   - 如果时效性重要，设置时间范围（`--time-range`）
   - 调整结果数量（`--max-results`）
   - 应用过滤器（图片尺寸、视频时长等）

3. **选择输出格式**：
   - 文本：快速阅读
   - Markdown：文档记录
   - JSON：后续处理

4. **执行搜索**：
   - 运行搜索命令
   - 如需保存结果，使用 `--output`
   - 打印到标准输出以便即时查看

5. **处理结果**：
   - 如需要，读取保存的文件
   - 提取 URL 或特定信息
   - 合并多次搜索的结果

## 快速参考

**命令结构：**
```bash
uv run scripts/search.py "<查询词>" [选项]
```

**常用选项：**
- `-t, --type` - 搜索类型（web、news、images、videos）
- `-n, --max-results` - 最大结果数（默认：10）
- `--time-range` - 时间过滤（d、w、m、y）
- `-r, --region` - 地区代码（默认：wt-wt，常用：us-en、cn-zh、uk-en 等）
- `--safe-search` - 安全搜索级别（on、moderate、off）
- `-f, --format` - 输出格式（text、markdown、json）
- `-o, --output` - 保存到文件

**图片专用选项：**
- `--image-size` - 尺寸过滤（Small、Medium、Large、Wallpaper）
- `--image-color` - 颜色过滤
- `--image-type` - 类型过滤（photo、clipart、gif、transparent、line）
- `--image-layout` - 布局过滤（Square、Tall、Wide）

**视频专用选项：**
- `--video-duration` - 时长过滤（short、medium、long）
- `--video-resolution` - 分辨率过滤（high、standard）

**获取完整帮助：**
```bash
uv run scripts/search.py --help
```

## 最佳实践

1. **具体明确** - 使用清晰、具体的搜索词以获得更好的结果
2. **使用时间过滤** - 查找当前信息时使用 `--time-range`
3. **调整结果数量** - 从 10-20 条开始，按需增加
4. **保存重要搜索** - 使用 `--output` 保存结果
5. **选择合适类型** - 新闻搜索用于时事，网页搜索用于一般信息
6. **JSON 用于自动化** - JSON 格式最易于程序解析
7. **合理使用** - 不要频繁快速重复搜索

## 故障排除

**常见问题：**

- **"缺少依赖"**：运行 `uv sync` 安装依赖
- **无结果**：尝试更宽泛的搜索词或移除时间过滤
- **超时错误**：搜索服务可能暂时不可用，稍后重试
- **频率限制**：如需多次请求，请间隔开
- **结果不符预期**：DuckDuckGo 结果可能与 Google 不同，尝试优化查询词

**限制：**

- 结果质量取决于 DuckDuckGo 的索引和算法
- 无高级搜索运算符（不像 Google 的 site:、filetype: 等）
- 图片和视频搜索结果可能少于网页搜索
- 无法控制结果排名或相关性评分
- 某些专业搜索在专用搜索引擎上效果更好

## 高级用例

### 组合多次搜索

通过组合搜索类型收集全面信息：

```bash
# 网页概览
uv run scripts/search.py "主题" --max-results 15 --output topic_web.txt

# 最新新闻
uv run scripts/search.py "主题" --type news --time-range w --output topic_news.txt

# 图片
uv run scripts/search.py "主题" --type images --max-results 20 --output topic_images.txt
```

### 程序化处理

使用 JSON 输出进行自动化处理：

```bash
uv run scripts/search.py "研究主题" --format json --output results.json
# 然后用其他脚本处理
python analyze_results.py results.json
```

### 构建知识库

从网络结果创建可搜索的文档：

```bash
# 搜索多个相关主题
uv run scripts/search.py "主题1" --format markdown --output kb/topic1.md
uv run scripts/search.py "主题2" --format markdown --output kb/topic2.md
uv run scripts/search.py "主题3" --format markdown --output kb/topic3.md
```

## 资源

### scripts/search.py

实现 DuckDuckGo 搜索功能的主要搜索工具。主要特性：

- **多种搜索类型** - 网页、新闻、图片和视频
- **灵活过滤** - 时间范围、地区、安全搜索和类型专用过滤
- **多种输出格式** - 文本、Markdown 和 JSON
- **文件输出** - 保存结果供后续处理
- **清晰格式** - 人类可读的输出，包含所有关键信息
- **错误处理** - 优雅处理网络错误和空结果

脚本可直接执行，通过 `--help` 获取完整的命令行帮助。
