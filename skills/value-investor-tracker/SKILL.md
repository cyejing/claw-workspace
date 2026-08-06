---
name: value-investor-tracker
description: 监控价值投资人（巴菲特/伯克希尔、段永平等）持仓变化。SEC 13F 直接拉取最近两期自动对比季度变化 + web_search 补充现金仓位、最新动态、最新观点、港股披露。适合独立使用或接定时任务。
version: "3.0.0"
metadata:
  openclaw:
    requires:
      bins: [ "python3", "curl" ]
      skills: [ "web_search" ]  # online-search 为降级方案
    optionalBins: [ "uv" ]
files:
  read:
    - <SKILL_DIR>/config/watchlist.json: 监控对象配置（CIK、名称、别名）
    - <SKILL_DIR>/scripts/compare.py: 13F 抓取 + 两期对比
---

# Value Investor Tracker

监控价值投资人持仓变化，数据源整合：
- **SEC 13F**：直接拉取**最近两期**官方申报自动 diff，得出季度持仓变化（新增/清仓/增持/减持），无需本地基线
- **web_search**：补充资讯信息——现金仓位、最新动态、最新观点、港股披露等

## 用户指令

### 指令 1：价值投资监控（综合报告）

**触发**："价值投资监控"、"看看巴菲特最近持仓变化"、"段永平最新动态"

**执行步骤**：

#### 1.1 SEC 13F 季度对比（脚本自动完成）
```bash
cd <SKILL_DIR> && python3 scripts/compare.py \
  --config config/watchlist.json \
  --mode check
```

- 自动拉取 SEC 上最近两期 13F（本期 vs 上期）
- 自动 diff 输出：🟢 新建仓 / 🔴 清仓 / 🔼 增持 / 🔽 减持
- 附前10大持仓列表（占比从大到小，其余合并"等 N 只"）
- **持仓变化已由 13F 覆盖，无需再搜索季度变化**

#### 1.2 资讯搜索（web_search）
**优先使用 web_search**，online-search 作为降级方案。

时效限定最近7天，搜索以下关键字（只搜 13F 覆盖不了的信息）：

**巴菲特/伯克希尔：**
1. 巴菲特 现金储备 最新
2. 伯克希尔 最新动态 观点

**段永平：**
1. 段永平 最新动态 观点
2. 段永平 港股 披露 权益变动

每次搜索完成后，给出一句话总结（说明这件事的核心内容），不展示原始结果列表。

> 如 web_search 失败，则降级使用 online-search，执行相同关键字搜索。

#### 1.3 输出格式

按以下结构整理汇报：

```
## 价值投资监控（2026-08-06）

### 一、SEC 13F 季度对比（SEC 官方数据）
#### 伯克希尔哈撒韦（巴菲特）
📅 本期 2026-05-15 vs 上期 2026-02-17 | 29只 | $263.1B
🟢 新建仓：...
🔴 清仓：...
🔼 增持：...
🔽 减持：...
**前10大持仓：**
- 苹果 $57.8B (22.0%)
- ...

#### H&H International（段永平）
📅 本期 2026-05-19 vs 上期 2026-02-17 | 19只 | $20.0B
（同上格式）

### 二、资讯动态（web_search）
#### 巴菲特/伯克希尔
- 一句话总结

#### 段永平
- 一句话总结

### 三、港股披露动态（如有）
- 一句话总结

---
数据来源：SEC EDGAR 13F（自动季度对比）+ web_search
```

---

### 指令 2：价值投资抓取（最新一期全量展示）

**触发**："价值投资抓取"、"抓一下巴菲特最新持仓全量"

**执行**：
```bash
cd <SKILL_DIR> && python3 scripts/compare.py \
  --config config/watchlist.json \
  --mode fetch [--top N]
```

- 只展示最新一期 13F 全量持仓（不做对比）
- 可选 `--top N` 只显示前 N 只
- 用途：raw 数据查看、核对

---

## 数据源

- **SEC EDGAR 13F-HR**：官方季度持仓申报（滞后约 45 天），自动对比最近两期
- **web_search**：现金仓位、最新动态、最新观点、港股披露等资讯
- **港股披露易**：香港联交所权益披露（通过搜索获取）

## 监控对象配置（config/watchlist.json）

```json
{
  "investors": [
    {
      "name": "Berkshire Hathaway",
      "alias": ["巴菲特", "Buffett"],
      "cik": "0001067983",
      "note": "伯克希尔哈撒韦，巴菲特掌舵"
    },
    {
      "name": "H&H International Investment",
      "alias": ["段永平", "Duan Yongping"],
      "cik": "0001759760",
      "note": "段永平美股持仓主体"
    }
  ]
}
```

## 变化判定逻辑

对每只股票（按 cusip 聚合）：
- **新增**：本期有、上期无 → 🟢 新建仓
- **清仓**：上期有、本期无 → 🔴 已清仓
- **增持**：股数增加 >2% → 🔼 +X%
- **减持**：股数减少 >2% → 🔽 -X%
- **微调**：股数变动 ≤2% → 不报告

## 接定时任务

```json
{
  "name": "价值投资监控",
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "使用 value-investor-tracker 技能，执行指令 1「价值投资监控」，输出综合报告。"
  }
}
```

## 限制

- 13F 每季度申报一次，不是实时
- 只覆盖美股多头持仓，不含私人公司、债券、空头
- 网络资讯可能有谣言或不实传闻，需甄别
- 港股披露通过搜索获取，非直接 API

## 技能依赖

- 必需：`web_search`（资讯搜索，online-search 降级）
- 必需：`python3`（13F 解析脚本）
