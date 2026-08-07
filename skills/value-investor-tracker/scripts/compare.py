#!/usr/bin/env python3
"""
Fetch the latest two 13F filings from SEC EDGAR and diff them directly.
No local baseline needed — SEC itself keeps the history.

Usage:
  python3 compare.py --config config/watchlist.json
"""
import argparse
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

SEC_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_INDEX = "https://www.sec.gov/Archives/edgar/data/{num}/{acc_no_dash}/index.json"
SEC_FILE = "https://www.sec.gov/Archives/edgar/data/{num}/{acc_no_dash}/{file}"
UA = "value-investor-tracker research (contact: user@example.com)"

# 股数变动小于此比例不报增持/减持（避免噪音）
MIN_CHANGE_PCT = 2.0


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def find_recent_filings(cik, n=2):
    """Return list of (filing_date, accession) for the most recent n 13F filings."""
    url = SEC_SUBMISSIONS.format(cik=cik)
    data = json.loads(http_get(url))
    r = data["filings"]["recent"]
    found = []
    for i, f in enumerate(r["form"]):
        if f in ("13F-HR", "13F-HR/A"):
            found.append((r["filingDate"][i], r["accessionNumber"][i]))
        if len(found) >= n:
            break
    if not found:
        raise RuntimeError(f"No 13F-HR for CIK {cik}")
    return found


def find_info_table_file(num, acc_no_dash):
    url = SEC_INDEX.format(num=num, acc_no_dash=acc_no_dash)
    idx = json.loads(http_get(url))
    for item in idx.get("directory", {}).get("item", []):
        n = item["name"].lower()
        if n.endswith(".xml") and "primary_doc" not in n and ("13f" in n or "info" in n):
            return item["name"]
    for item in idx.get("directory", {}).get("item", []):
        if item["name"].lower().endswith(".xml") and "primary_doc" not in item["name"].lower():
            return item["name"]
    raise RuntimeError("info table not found")


def parse_13f_xml(xml_text):
    ns = {"ns": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
    root = ET.fromstring(xml_text)
    rows = root.findall(".//ns:infoTable", ns)
    if not rows:
        rows = root.findall(".//infoTable")
    out = []
    for r in rows:
        name = (r.findtext("ns:nameOfIssuer", namespaces=ns) or "").strip()
        cls = (r.findtext("ns:titleOfClass", namespaces=ns) or "").strip()
        cusip = (r.findtext("ns:cusip", namespaces=ns) or "").strip()
        val = int(r.findtext("ns:value", namespaces=ns) or "0")
        sn = r.find("ns:shrsOrPrnAmt", namespaces=ns)
        sh = int((sn.findtext("ns:sshPrnamt", namespaces=ns) if sn is not None else "0") or "0")
        out.append({"name": name, "cls": cls, "cusip": cusip, "value": val, "shares": sh})
    return out


def aggregate(holdings):
    agg = {}
    for h in holdings:
        k = h["cusip"]
        if k not in agg:
            agg[k] = {"cusip": k, "name": h["name"], "cls": h["cls"], "shares": 0, "value": 0}
        agg[k]["shares"] += h["shares"]
        agg[k]["value"] += h["value"]
    total = sum(v["value"] for v in agg.values()) or 1
    items = sorted(agg.values(), key=lambda x: x["value"], reverse=True)
    for v in items:
        v["pct"] = round(v["value"] / total * 100, 2)
    return items, total


def fetch_filing(cik, filing_date, accession):
    num = str(int(cik))
    acc_no_dash = accession.replace("-", "")
    fname = find_info_table_file(num, acc_no_dash)
    xml_url = SEC_FILE.format(num=num, acc_no_dash=acc_no_dash, file=fname)
    xml_text = http_get(xml_url)
    holdings = parse_13f_xml(xml_text)
    items, total = aggregate(holdings)
    return {
        "cik": cik, "filing_date": filing_date,
        "accession": accession, "total_value": total,
        "holdings_count": len(items), "holdings": items,
    }


def compare(current, previous):
    """Diff two filings (both from SEC, no local state)."""
    cur_map = {h["cusip"]: h for h in current["holdings"]}
    base_map = {h["cusip"]: h for h in previous["holdings"]}
    changes = []
    # New / increased
    for cusip, ch in cur_map.items():
        old = base_map.get(cusip)
        if old is None:
            changes.append({"type": "new", "cusip": cusip, "name": ch["name"], "cls": ch["cls"],
                            "cur_shares": ch["shares"], "cur_pct": ch["pct"],
                            "cur_value": ch["value"]})
        elif ch["shares"] != old["shares"]:
            delta = (ch["shares"] - old["shares"]) / max(old["shares"], 1) * 100
            if abs(delta) < MIN_CHANGE_PCT:
                continue  # 微调不报
            pct_ch = ch["pct"] - old["pct"]
            changes.append({"type": "changed", "cusip": cusip, "name": ch["name"], "cls": ch["cls"],
                            "cur_shares": ch["shares"], "cur_pct": ch["pct"],
                            "old_shares": old["shares"], "old_pct": old["pct"],
                            "delta_pct": round(delta, 1), "pct_change": round(pct_ch, 2)})
    # Sold / removed
    for cusip, bh in base_map.items():
        if cusip not in cur_map:
            changes.append({"type": "sold", "cusip": cusip, "name": bh["name"], "cls": bh["cls"],
                            "old_shares": bh["shares"], "old_pct": bh["pct"],
                            "old_value": bh["value"]})
    return changes


def status_tag(c):
    """返回单只股票的变动状态标签"""
    if c is None:
        return "—"
    if c["type"] == "new":
        return "🟢 新建仓"
    elif c["type"] == "sold":
        return "🔴 清仓"
    elif c["type"] == "changed":
        delta = c["delta_pct"]
        arrow = "🔼" if delta > 0 else "🔽"
        sign = "+" if delta > 0 else ""
        return f"{arrow} {'增持' if delta > 0 else '减持'} {sign}{delta:.0f}%"
    return "—"


def fmt_holdings_with_status(items, change_map):
    """按占比从大到小排序，一行一个：名称 市值(占比%) | 变动状态"""
    lines = []
    for h in items:
        tag = status_tag(change_map.get(h["cusip"]))
        lines.append(f"- {h['name']} ${h['value']/1e9:.1f}B ({h['pct']:.1f}%) | {tag}")
    return lines


def format_sold(c):
    return (f"🔴 清仓：{c['name']}（原 {c['old_shares']:,}股，"
            f"原占比 {c['old_pct']:.1f}%，约 ${c['old_value']/1e9:.1f}B）")


def main():
    ap = argparse.ArgumentParser(description="SEC 13F 两期持仓对比（无需本地基线）")
    ap.add_argument("--config", required=True, help="监控对象配置文件路径")
    args = ap.parse_args()

    with open(args.config) as f:
        cfg = json.load(f)

    output_lines = []

    for inv in cfg["investors"]:
        cik = inv["cik"]
        alias = " / ".join(inv["alias"])
        name = inv["name"]

        try:
            filings = find_recent_filings(cik, 2)
            current = fetch_filing(cik, *filings[0])
        except Exception as e:
            output_lines.append(f"❌ {name}（{alias}）：抓取失败 - {e}")
            continue

        if len(filings) < 2:
            output_lines.append(f"ℹ️ {name}（{alias}）：仅有一期 13F 申报，无法对比")
            continue

        try:
            previous = fetch_filing(cik, *filings[1])
        except Exception as e:
            output_lines.append(f"⚠️ {name}（{alias}）：上一期抓取失败 - {e}，仅展示本期")
            previous = None

        output_lines.append(f"### {name}（{alias}）")

        if previous is None:
            output_lines.append(
                f"📅 申报日期：{current['filing_date']} | "
                f"共 {current['holdings_count']} 只 | "
                f"组合总值 ${current['total_value']/1e9:.1f}B")
            output_lines.extend(fmt_holdings_with_status(current["holdings"], {}))
            output_lines.append("")
            continue

        changes = compare(current, previous)
        change_map = {c["cusip"]: c for c in changes
                      if c["type"] in ("new", "changed")}
        sold = [c for c in changes if c["type"] == "sold"]

        output_lines.append(
            f"📅 本期 {current['filing_date']} vs 上期 {previous['filing_date']} | "
            f"{current['holdings_count']}只 | ${current['total_value']/1e9:.1f}B")

        output_lines.append("**持仓明细（按占比排序）：**")
        output_lines.extend(fmt_holdings_with_status(current["holdings"], change_map))

        if sold:
            output_lines.append("**已清仓：**")
            for c in sold:
                output_lines.append(format_sold(c))

        if not changes:
            output_lines.append("✅ 与上期相比无显著变化")

        output_lines.append("")

    print("\n".join(output_lines))


if __name__ == "__main__":
    main()
