#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

CANDIDATES = []
if os.getenv("SEARXNG_URL"):
    CANDIDATES.extend([x.strip().rstrip("/") for x in os.getenv("SEARXNG_URL", "").split(",") if x.strip()])
CANDIDATES.extend([
    "http://127.0.0.1:8889",
    "http://127.0.0.1:8765",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
])


def fetch_once(base: str, q: str, count: int, categories: str, time_range: str, page: int = 1):
    params = {
        "q": q,
        "format": "json",
        "language": "zh-CN",
        "safesearch": "0",
        "pageno": str(page),
        "categories": categories,
    }
    if time_range:
        params["time_range"] = time_range
    url = base.rstrip("/") + "/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "researcher-search/1.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        body = r.read().decode("utf-8", errors="ignore")
    data = json.loads(body)
    rows = []
    for it in data.get("results", []):
        rows.append(
            {
                "title": (it.get("title") or "").strip(),
                "url": it.get("url") or "",
                "snippet": (it.get("content") or "").strip(),
                "engine": it.get("engine") or "",
                "publishedDate": it.get("publishedDate") or "",
            }
        )
    return rows[:count]


def fetch(q: str, count: int, categories: str, time_range: str):
    errs = []
    for base in CANDIDATES:
        try:
            rows = fetch_once(base, q, count, categories, time_range)
            return base, rows
        except Exception as e:
            errs.append(f"{base}: {e}")
    raise RuntimeError("all searxng endpoints failed; " + " | ".join(errs[:3]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--count", type=int, default=15)
    ap.add_argument("--categories", default="news,general")
    ap.add_argument("--time-range", default="day")
    args = ap.parse_args()

    base, rows = fetch(args.query, args.count, args.categories, args.time_range)
    out = {
        "query": args.query,
        "engine_base": base,
        "count": len(rows),
        "categories": args.categories,
        "time_range": args.time_range,
        "results": rows,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if len(rows) < 1:
        sys.exit(2)


if __name__ == "__main__":
    main()
