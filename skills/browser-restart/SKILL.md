---
name: browser-restart
description: 当用户说"重启浏览器""重启谷歌浏览器""重启 Chrome""启动浏览器""浏览器抓不到数据了，重启一下""bb-browser 抓不到了，重启浏览器""查询浏览器状态""检查浏览器"等意思相近的话时，使用此技能。执行关闭全部 Chrome、重启 Chrome、重建 bb-browser daemon、打开知乎并验证 `bb-browser site zhihu/hot --json` 能成功抓取数据，最后汇报是否恢复成功和抓取条数。脚本内部固定使用 `--user-data-dir /home/clawd/.cache/chrome`，不允许外部覆盖。
---

# Browser Restart

执行"重启浏览器并验收抓取链路"的固定流程。
也支持**仅查询浏览器状态**，不执行重启。

## 用户意图识别

| 优先级 | 触发条件 | 执行操作 |
|--------|----------|----------|
| 1 | "重启浏览器""重启谷歌浏览器""重启 Chrome""启动浏览器" | 直接运行 `python3 <SKILL_DIR>/scripts/restart_browser.py` |
| 2 | "浏览器抓不到数据了""bb-browser 抓不到了，重启一下""知乎抓不到了，重启浏览器" | 直接运行 `python3 <SKILL_DIR>/scripts/restart_browser.py` |
| 3 | "查询浏览器状态""检查浏览器""浏览器正常吗""知乎能抓到吗" | 运行 `python3 <SKILL_DIR>/scripts/check_browser_status.py`（仅检查，不重启） |
| 4 | 其他与浏览器恢复、Chrome 重启、bb-browser 抓取恢复相关的表达 | 默认按本技能执行，并以 `zhihu/hot` 验收结果为准 |

**完成定义**：
- 重启流程：不是"Chrome 打开了"就算完成，只有 `bb-browser site zhihu/hot --json` 成功返回并拿到条数，才算真正恢复成功。
- 状态查询流程：明确汇报 bb-browser daemon 是否健康、知乎抓取是否成功、返回条数，不断言"已恢复"或"正常"除非实际验证通过。

---

## 一、重启流程（单窗口版）

### 核心规则

1. **单窗口原则**：重启过程只产生一个 Chrome 窗口（你的 profile），
   不允许出现第二个空 profile 窗口。
2. 完成定义：
   - Chrome 已启动（端口 9222，你的 profile）
   - bb-browser daemon 自动重连
   - `bb-browser site zhihu/hot --json` 成功返回 20 条
   - 明确汇报抓取条数
3. 如果最终抓取失败，必须如实说明失败原因；**不能伪造"已恢复"**。

### 执行方式

```bash
python3 <SKILL_DIR>/scripts/restart_browser.py
```

**流程（5步）：**
1. 停掉 bb-browser daemon（防止它拉起独立 Chrome）
2. 杀掉所有 Chrome 进程
3. 用你的 profile 启动 Chrome（端口 9222，打开知乎热榜）
4. 等热榜页面加载完成（cookie 写入），再重启 daemon（它自动重连）
5. 验证 `bb-browser site zhihu/hot --json` 返回条数

### 参数

```bash
python3 <SKILL_DIR>/scripts/restart_browser.py \
  --display :0 \
  --cdp-port 9222 \
  --wait-seconds 8
```

常用可调参数：
- `--display`：X11 display，默认 `:0`
- `--cdp-port`：默认 `9222`（bb-browser daemon 默认端口）
- `--wait-seconds`：热榜页面加载等待时间，默认 8 秒

### 固定约束

- Chrome `user-data-dir` 必须固定为 `/home/clawd/.cache/chrome`
- CDP 端口固定为 `9222`（daemon 默认端口）
- 不要在调用时额外传入别的 profile 路径
- **不要**杀掉 bb-browser daemon 后手动起新 Chrome，daemon 会拉起独立窗口

### 向用户汇报

成功时汇报：
- 浏览器已启动成功
- Zhihu 可正常抓取
- 本次抓取条数

失败时汇报：
- 卡在哪个阶段：Chrome / daemon / Zhihu open / zhihu/hot
- 具体错误摘要
- 若是登录态问题，明确说明需要有效 Zhihu 登录态

---

## 二、状态查询流程（新增）

当用户说"查询浏览器状态""检查浏览器"时，**不执行重启**，只做轻量级检查。

### 执行命令

```bash
python3 <SKILL_DIR>/scripts/check_browser_status.py
```

### 检查内容

脚本依次检查：
1. **Chrome 进程**：是否存在 `/opt/google/chrome/chrome` 进程
2. **bb-browser daemon 健康**：运行 `bb-browser daemon status`，检查 `CDP connected`
3. **知乎抓取验证**：运行 `bb-browser site zhihu/hot --json`，验证返回条数 > 0
4. **输出汇总**：JSON 格式，包含 `daemon_ok`、`zhihu_ok`、`zhihu_count`、`sample_titles`

### 向用户汇报

**健康时**汇报：
- ✅ 浏览器状态正常
- bb-browser daemon 已连接 CDP
- 知乎热榜可正常抓取，本次返回 N 条

**异常时**汇报：
- ❌ 哪个环节异常（Chrome 进程 / daemon / 知乎抓取）
- 具体错误信息
- 建议操作（如：说"重启浏览器"来执行完整重启流程）

### 失败判定提示

遇到以下情况时，不要说"正常"：
- Chrome 进程不存在
- `bb-browser daemon status` 显示 `CDP connected: no`
- `bb-browser site zhihu/hot --json` 超时、返回错误、或没有条数

---

## 参考

如需查看这台机器上已验证过的现象与限制，读：
- `references/testing-notes.md`

## 变更记录

- 2026-08-05：从"脚本拉起 Chrome + daemon 独立窗口"改为"单窗口"模式。
  根因：bb-browser daemon 启动时若找不到已有 Chrome，会自己拉起一个空 profile 的 Chrome（端口 9222，`~/.bb-browser/browser/user-data`），造成双窗口。
  修复：先杀 Chrome 再用用户 profile 启动（端口 9222），然后重启 daemon 自动重连。
