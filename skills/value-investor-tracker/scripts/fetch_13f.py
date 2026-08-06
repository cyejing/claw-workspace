#!/usr/bin/env python3
"""
Fetch and parse SEC 13F-HR holdings for a given CIK.

Usage:
  python3 fetch_13f.py --cik 0001067983 [--out /path/to/out.json]

Output JSON:
  {
    "cik": "...",
    "filing_date": "2026-05-15",
    "accession": "0001193125-26-226661",
    "total_value": 263095700000,   # dollars
    "holdings": [
      {"cusip":"...", "name":"APPLE INC", "cls":"COM",
       "shares": 227917808, "value": 57843260000, "pct": 22.0, "type":"SH"},
      ...
    ]
  }
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from collections import defaultdict

SEC_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_INDEX = "https://www.sec.gov/Archives/edgar/data/{num}/{acc_no_dash}/index.json"
SEC_FILE = "https://www.sec.gov/Archives/edgar/data/{num}/{acc_no_dash}/{file}"
UA = "value-investor-tracker research (contact: user@example.com)"


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def find_latest_13f(cik: str):
    """Return (filing_date, accession_with_dash) of latest 13F-HR."""
    url = SEC_SUBMISSIONS.format(cik=cik)
    data = json.loads(http_get(url))
    r = data["filings"]["recent"]
    forms = r["form"]
    dates = r["filingDate"]
    accs = r["accessionNumber"]
    for i, f in enumerate(forms):
        if f in ("13F-HR", "13F-HR/A"):
            return dates[i], accs[i]
    raise RuntimeError(f"No 13F-HR found for CIK {cik}")


def find_info_table_file(num: str, acc_no_dash: str) -> str:
    """Find the information table XML filename from the filing index."""
    url = SEC_INDEX.format(num=num, acc_no_dash=acc_no_dash)
    idx = json.loads(http_get(url))
    for item in idx.get("directory", {}).get("item", []):
        name = item["name"]
        low = name.lower()
        # info table file usually contains '13f' or 'informationtable' or is xml with 'info'
        if low.endswith(".xml") and ("13f" in low or "info" in low) and "primary_doc" not in low:
            return name
    # fallback: first xml that is not primary_doc
    for item in idx.get("directory", {}).get("item", []):
        if item["name"].lower().endswith(".xml") and "primary_doc" not in item["name"].lower():
            return item["name"]
    raise RuntimeError("info table xml not found in index")


def parse_13f(xml_text: str) -> list:
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
        ty = (sn.findtext("ns:sshPrnamtType", namespaces=ns) if sn is not None else "") or ""
        out.append({
            "name": name, "cls": cls, "cusip": cusip,
            "value": val, "shares": sh, "type": ty,
        })
    return out


def aggregate(holdings: list) -> list:
    agg = {}
    for h in holdings:
        k = h["cusip"]
        if k not in agg:
            agg[k] = {"cusip": k, "name": h["name"], "cls": h["cls"],
                      "shares": 0, "value": 0, "type": h["type"]}
        agg[k]["shares"] += h["shares"]
        agg[k]["value"] += h["value"]
    total = sum(v["value"] for v in agg.values()) or 1
    items = []
    for v in agg.values():
        v["pct"] = round(v["value"] / total * 100, 2)
        items.append(v)
    items.sort(key=lambda x: x["value"], reverse=True)
    return items, total


def fetch(cik: str) -> dict:
    filing_date, accession = find_latest_13f(cik)
    num = str(int(cik))  # strip leading zeros
    acc_no_dash = accession.replace("-", "")
    fname = find_info_table_file(num, acc_no_dash)
    xml_url = SEC_FILE.format(num=num, acc_no_dash=acc_no_dash, file=fname)
    xml_text = http_get(xml_url)
    holdings = parse_13f(xml_text)
    items, total = aggregate(holdings)
    return {
        "cik": cik,
        "filing_date": filing_date,
        "accession": accession,
        "total_value": total,
        "holdings_count": len(items),
        "holdings": items,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    try:
        result = fetch(args.cik)
    except Exception as e:
        print(json.dumps({"error": str(e), "cik": args.cik}), file=sys.stderr)
        sys.exit(1)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"[OK] {result['name'] if 'name' in result else args.cik} | "
              f"filing {result['filing_date']} | {result['holdings_count']} holdings | "
              f"${result['total_value']/1e9:.1f}B -> {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
