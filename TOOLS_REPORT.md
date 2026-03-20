# TOOLS_REPORT.md - 工具问题汇总

## web_search (Gemini Provider)

| 问题 | 错误类型 | 说明 | 解决方案 |
|------|----------|------|----------|
| 语言过滤 | unsupported_language | Gemini 不支持 language 参数 | 只用 Brave/Perplexity 时才传 language |
| 时间过滤 | unsupported_freshness | Gemini 不支持 freshness 参数 | 只用 Brave/Perplexity 时才传 freshness |

**注意：** 默认 provider 是 Gemini，调用时避免传这两个参数。

---
