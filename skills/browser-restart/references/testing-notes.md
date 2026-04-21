# Browser Restart Testing Notes

这些是为本机调试得到的经验，供技能执行时参考。

## 已验证现象

### 1. 残留 daemon 会造成“假活着”状态

出现过这种情况：
- `bb-browser daemon` 进程仍在
- 19824 端口被占用
- 但 `~/.bb-browser/daemon.json` 不存在
- CLI 因此报：`Daemon did not start in time`

所以稳定流程必须先：
- 杀掉残留 `bb-browser daemon`
- 删除残留 `~/.bb-browser/daemon.json`
- 再启动新 daemon

### 2. 成功标准必须以 `bb-browser site zhihu/hot` 为准

只看到：
- Chrome 进程起来了
- CDP 端口通了
- daemon `/status` 健康

都还不够。

真正的验收点是：

```bash
bb-browser site zhihu/hot --json
```

只有这个返回成功并且能拿到 `count/items`，才算恢复。

### 3. Zhihu 抓取依赖登录态 / 页面环境

本机测试时，直接访问 Zhihu API 会出现认证相关响应；因此如果 profile 中没有可用登录态，可能无法完成最终验收。

结论：
- 技能必须固定使用用户现有 profile：`/home/clawd/.cache/chrome`
- 不要把 profile 路径做成可调参数，避免误用其他目录导致登录态/扩展状态不一致
- 若最终失败且错误指向认证/抓取超时，应如实报告“当前登录态或页面环境不可用”

### 4. `bb-browser site ... --json` 返回体外面可能有 success/data 包装

例如：

```json
{"success": true, "data": {"count": 20, "items": [...]}}
```

所以脚本不能只检查顶层 `count/items`，还要兼容 `payload.data.count/items`。

## 当前脚本设计目标

脚本优先保证：
1. 杀残留 daemon
2. 杀所有 Chrome 进程
3. 启动 Chrome
4. 等 CDP
5. 启动 daemon
6. 等 daemon.json + `/status`
7. 打开 Zhihu
8. 重试 `zhihu/hot`

## 不应做的事

- 不要仅凭“Chrome 起来了”就报告成功
- 不要仅凭“open zhihu 页面成功”就报告成功
- 不要在 `zhihu/hot` 失败时伪造抓取条数
