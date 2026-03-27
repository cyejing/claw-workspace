# bb-browser 命令用法 —— 自动化浏览器操作

## 快速开始

```bash
bb-browser open <url>                               # 打开页面（新 tab）
bb-browser snapshot -i                              # 获取可交互元素
bb-browser click @5                                 # 点击元素
bb-browser fill @3 "text"                           # 填写输入框
bb-browser close                                    # 关闭 tab
```

## 核心工作流

1. `open` 打开页面
2. `snapshot -i` 查看可操作元素（返回 @ref）
3. 用 `@ref` 执行操作（click, fill, etc.）
4. 页面变化后重新 `snapshot -i`
5. 任务完成后 `close` 关闭 tab

## Site 系统

site 系统是 bb-browser 的核心特性，通过 adapter 将网站功能 CLI 化。adapter 自动处理 tab 管理（查找匹配域名的 tab 或新建），自动检测登录错误并提示。

详细用法见「bb-browser sites 用法」部分。

## fetch — 带登录态的 curl

在浏览器上下文中执行 fetch，自动携带 Cookie 和登录态。

```bash
bb-browser fetch <url>                              # GET 请求
bb-browser fetch <url> --method POST --body '{"k":"v"}'
bb-browser fetch <url> --headers '{"Auth":"Bearer xxx"}'
bb-browser fetch <url> --output data.json
bb-browser fetch /api/me.json                       # 相对路径（用当前 tab 的 origin）
```

## 命令速查

### 导航

```bash
bb-browser open <url>                               # 打开 URL（新 tab）
bb-browser open <url> --tab current                 # 在当前 tab 打开
bb-browser open <url> --tab <tabId>                 # 在指定 tabId 打开
bb-browser back                                     # 后退
bb-browser forward                                  # 前进
bb-browser refresh                                  # 刷新
bb-browser close                                    # 关闭当前 tab
```

### 快照

```bash
bb-browser snapshot                                 # 完整页面结构
bb-browser snapshot -i                              # 只显示可交互元素（推荐）
bb-browser snapshot -c                              # 移除空结构节点
bb-browser snapshot -d 3                            # 限制树深度为 3 层
bb-browser snapshot -s ".main"                      # 限定 CSS 选择器范围
bb-browser snapshot --json                          # JSON 格式输出
bb-browser snapshot -i -c -d 5                      # 选项可组合
```

### 元素交互

```bash
bb-browser click @5                                 # 点击
bb-browser hover @5                                 # 悬停
bb-browser fill @3 "text"                           # 清空并填写
bb-browser type @3 "text"                           # 追加输入（不清空）
bb-browser check @7                                 # 勾选复选框
bb-browser uncheck @7                               # 取消勾选
bb-browser select @4 "option"                       # 下拉选择
bb-browser press Enter                              # 按键
bb-browser press Control+a                          # 组合键
bb-browser scroll down                              # 向下滚动（默认 300px）
bb-browser scroll up 500                            # 向上滚动 500px
```

### 获取信息

```bash
bb-browser get text @5                              # 获取元素文本
bb-browser get url                                  # 获取当前 URL
bb-browser get title                                # 获取页面标题
```

### Tab 管理

```bash
bb-browser tab                                      # 列出所有 tab
bb-browser tab new [url]                            # 新建 tab
bb-browser tab 2                                    # 切换到第 2 个 tab（按 index）
bb-browser tab select --id 123                      # 切换到指定 tabId 的 tab
bb-browser tab close                                # 关闭当前 tab
bb-browser tab close 3                              # 关闭第 3 个 tab（按 index）
bb-browser tab close --id 123                       # 关闭指定 tabId 的 tab
```

操作完成后必须关闭自己打开的 tab：

```bash
bb-browser open https://site-a.com                  # tabId: 123
bb-browser open https://site-b.com                  # tabId: 456
bb-browser tab close                                # 关闭当前 tab
bb-browser tab close                                # 关闭剩余 tab
```

### 截图

```bash
bb-browser screenshot                               # 截图（自动保存）
bb-browser screenshot path.png                      # 截图到指定路径
```

### 等待

```bash
bb-browser wait 2000                                # 等待 2 秒
bb-browser wait @5                                  # 等待元素出现
```

### JavaScript 执行

```bash
bb-browser eval "document.title"                    # 执行 JS
bb-browser eval "window.scrollTo(0, 1000)"          # 滚动到指定位置
bb-browser eval "document.querySelector('#js_content').innerText"
bb-browser eval "[...document.querySelectorAll('a')].map(a => a.href).join('\n')"
```

### Frame 切换

```bash
bb-browser frame "#iframe-id"                       # 切换到 iframe
bb-browser frame main                               # 返回主 frame
```

### 对话框处理

```bash
bb-browser dialog accept                            # 确认对话框
bb-browser dialog dismiss                           # 取消对话框
bb-browser dialog accept "text"                     # 确认并输入（prompt）
```

### 网络与调试

```bash
bb-browser network requests                         # 查看网络请求
bb-browser network requests "api" --with-body       # 过滤 + 完整请求/响应体
bb-browser network route "*analytics*" --abort      # 拦截并阻止请求
bb-browser network route "*/api/user" --body '{}'   # 拦截并 mock 响应
bb-browser network unroute                          # 移除所有拦截规则
bb-browser network clear                            # 清空请求记录
bb-browser console                                  # 查看控制台消息
bb-browser console --clear                          # 清空控制台
bb-browser errors                                   # 查看 JS 错误
bb-browser errors --clear                           # 清空错误记录
bb-browser trace start                              # 开始录制用户操作
bb-browser trace stop                               # 停止录制，输出事件列表
bb-browser trace status                             # 查看录制状态
```

## 全局选项

```bash
--json                                              # JSON 格式输出（所有命令通用）
--tab <tabId>                                       # 指定操作的标签页 ID
--mcp                                               # 启动 MCP server
```

## Ref 使用说明

snapshot 返回的 `@ref` 是元素的临时标识：

```
@1 [button] "提交"
@2 [input type="text"] placeholder="请输入姓名"
@3 [a] "查看详情"
```

注意：
- 页面导航后 ref 失效，需重新 snapshot
- 动态内容加载后需重新 snapshot
- ref 格式：`@1`, `@2`, `@3`...

## 信息提取 vs 页面操作

**提取内容用 `eval`**（文章、正文等长文本）：

```bash
bb-browser eval "document.querySelector('#js_content').innerText"
bb-browser eval "document.body.innerText.substring(0, 5000)"
```

**操作元素用 `snapshot -i`**（点击、填写、选择）：

```bash
bb-browser snapshot -i
bb-browser fill @2 "username"
bb-browser click @1
```

## 并发操作

```bash
bb-browser open https://site-a.com &
bb-browser open https://site-b.com &
bb-browser open https://site-c.com &
wait
```

## 常见任务示例

```bash
bb-browser open https://example.com/form
bb-browser snapshot -i
bb-browser fill @1 "张三"
bb-browser fill @2 "zhangsan@example.com"
bb-browser click @3
bb-browser wait 2000
bb-browser close
```
