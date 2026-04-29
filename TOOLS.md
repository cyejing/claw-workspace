# TOOLS.md - 本地配置笔记

> 这里存放你的**个性化配置**，比如设备名称、偏好设置等。Skills 是共享的通用工具，这个文件是你的私人备忘录。

---

## Tool gotchas

- `stock-analysis` 首次用 `uv run .../watchlist.py check` 可能会先下载/构建 `numpy`、`pandas`、`curl-cffi`、`multitasking` 等依赖，用户面前容易超时或被 SIGTERM 中断。
- 如果只是要快速查看现有观察列表行情，优先准备轻量兜底方案；需要正式告警检查时，再考虑预热依赖后运行原脚本。
- 在这台机器上，`chrome`（含 `--remote-debugging-port` 的自动化/调试实例）、`next-server`、`openclaw-gateway` 默认视为正常常驻进程；不要仅凭 RSS 高、运行时间长就判定为“无效浪费内存”，除非老板明确说暂时不用或先核实用途。
