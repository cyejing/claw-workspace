---
name: browser-restart
description: 当用户说“重启浏览器”“重启谷歌浏览器”“重启 Chrome”“启动浏览器”“浏览器抓不到数据了，重启一下”“bb-browser 抓不到了，重启浏览器”等意思相近的话时，使用此技能。执行关闭全部 Chrome、重启 Chrome、重建 bb-browser daemon、打开知乎并验证 `bb-browser site zhihu/hot --json` 能成功抓取数据，最后汇报是否恢复成功和抓取条数。脚本内部固定使用 `--user-data-dir /home/clawd/.cache/chrome`，不允许外部覆盖。
---

# Browser Restart

执行“重启浏览器并验收抓取链路”的固定流程。

## 用户意图识别

| 优先级 | 触发条件 | 执行操作 |
|--------|----------|----------|
| 1 | “重启浏览器”“重启谷歌浏览器”“重启 Chrome”“启动浏览器” | 直接运行 `python3 <SKILL_DIR>/scripts/restart_browser.py` |
| 2 | “浏览器抓不到数据了”“bb-browser 抓不到了，重启一下”“知乎抓不到了，重启浏览器” | 直接运行 `python3 <SKILL_DIR>/scripts/restart_browser.py` |
| 3 | 其他与浏览器恢复、Chrome 重启、bb-browser 抓取恢复相关的表达 | 默认按本技能执行，并以 `zhihu/hot` 验收结果为准 |

**完成定义**：不是“Chrome 打开了”就算完成，只有 `bb-browser site zhihu/hot --json` 成功返回并拿到条数，才算真正恢复成功。

## 核心规则

1. 不要只重启 Chrome 进程；必须同时校验 **Chrome CDP → bb-browser daemon → Zhihu 抓取** 这条链。
2. 完成定义不是“浏览器启动了”，而是：
   - Chrome 已启动并开放 CDP
   - bb-browser daemon 健康
   - `bb-browser site zhihu/hot --json` 成功返回
   - 明确汇报抓取条数
3. 如果最终抓取失败，必须如实说明失败原因；**不能伪造“已恢复”**。

## 默认执行方式

直接运行：

```bash
python3 <SKILL_DIR>/scripts/restart_browser.py
```

默认行为：
- 关闭所有 Chrome 相关进程
- 清理残留 `bb-browser daemon`
- 用稳定参数启动 Chrome
- 重启 `bb-browser daemon`
- 打开知乎热榜页面并重试抓取
- 输出最终 JSON 汇总

## 参数

```bash
python3 <SKILL_DIR>/scripts/restart_browser.py \
  --display :0 \
  --cdp-port 19825
```

常用可调参数：
- `--chrome-bin`：Chrome 可执行文件
- `--display`：X11 display，默认 `:0`
- `--cdp-port`：默认 `19825`
- `--zhihu-open-retries`：知乎页面打开重试次数
- `--zhihu-site-retries`：`zhihu/hot` 抓取重试次数
- `--wait-seconds`：重试间等待秒数

## 固定约束

- Chrome `user-data-dir` 必须固定为 `/home/clawd/.cache/chrome`
- 不要把 `user-data-dir` 暴露为可选参数
- 不要在调用时额外传入别的 profile 路径

## 推荐工作流

### 1) 运行脚本

优先使用脚本，而不是手写一串 shell 命令，以减少残留 daemon、旧 profile、等待时序等问题。

### 2) 读取脚本输出

如果成功，输出里必须包含：
- `success: true`
- `message: 浏览器启动成功，知乎数据可正常抓取`
- `count`
- `sample_titles`

### 3) 向用户汇报

成功时汇报：
- 浏览器已启动成功
- Zhihu 可正常抓取
- 本次抓取条数

失败时汇报：
- 卡在哪个阶段：Chrome / daemon / Zhihu open / zhihu/hot
- 具体错误摘要
- 若是登录态问题，明确说明需要有效 Zhihu 登录态

## 失败判定提示

遇到以下情况时，不要说“已恢复”：
- `bb-browser daemon.json` 没生成
- `/status` 不健康
- `bb-browser open https://www.zhihu.com/hot` 失败
- `bb-browser site zhihu/hot --json` 超时、返回错误、或没有条数

## 参考

如需查看这台机器上已验证过的现象与限制，读：
- `references/testing-notes.md`
