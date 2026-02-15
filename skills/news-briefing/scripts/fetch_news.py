#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict

FEEDS_JP = {
    "y_top": "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
    "y_dom": "https://news.yahoo.co.jp/rss/topics/domestic.xml",
    "y_world": "https://news.yahoo.co.jp/rss/topics/world.xml",
    "y_bus": "https://news.yahoo.co.jp/rss/topics/business.xml",
    "y_ent": "https://news.yahoo.co.jp/rss/topics/entertainment.xml",
    "y_spt": "https://news.yahoo.co.jp/rss/topics/sports.xml",
    "y_it": "https://news.yahoo.co.jp/rss/topics/it.xml",
    "g_top": "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
    "g_jp": "https://news.google.com/rss/headlines/section/geo/Japan?hl=ja&gl=JP&ceid=JP:ja",
    "g_world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ja&gl=JP&ceid=JP:ja",
    "g_bus": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ja&gl=JP&ceid=JP:ja",
    "g_ent": "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=ja&gl=JP&ceid=JP:ja",
    "g_spt": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=ja&gl=JP&ceid=JP:ja",
    "g_tech": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ja&gl=JP&ceid=JP:ja",
}

WEIGHTS = {
    "y_top": 1.8,
    "y_dom": 1.2,
    "y_world": 1.2,
    "y_bus": 1.2,
    "y_ent": 1.1,
    "y_spt": 1.1,
    "y_it": 1.2,
    "g_top": 1.4,
    "g_jp": 1.2,
    "g_world": 1.1,
    "g_bus": 1.1,
    "g_ent": 1.0,
    "g_spt": 1.0,
    "g_tech": 1.1,
}

CATEGORY_ORDER = [
    "社会新闻",
    "日本政局",
    "国际关系",
    "经济",
    "在日生活",
    "娱乐",
    "体育",
    "AI/科技",
    "币圈/金融科技",
]

CATEGORY_EMOJI = {
    "社会新闻": "📰",
    "日本政局": "🏛️",
    "国际关系": "🌍",
    "经济": "💹",
    "在日生活": "🏠",
    "娱乐": "🎬",
    "体育": "🏅",
    "AI/科技": "🤖",
    "币圈/金融科技": "🪙",
}

KEYWORDS = [
    ("币圈/金融科技", ["ビットコイン", "暗号資産", "仮想通貨", "ETF", "ブロックチェーン"]),
    ("AI/科技", ["AI", "生成AI", "OpenAI", "半導体", "サイバー", "情報流出", "データ"]),
    ("日本政局", ["首相", "衆院選", "選挙", "自民", "立憲", "幹事長", "官邸", "議員"]),
    ("国际关系", ["中国", "米", "ロシア", "ウクライナ", "外交", "国際", "外相", "戦争"]),
    ("经济", ["経済", "企業", "賃金", "市場", "投資", "不動産", "物価", "太陽光"]),
    ("在日生活", ["寒暖差", "子育て", "養育", "交通", "医療", "生活", "保育", "学校"]),
    ("娱乐", ["芸能", "映画", "ドラマ", "音楽", "俳優", "女優", "タレント"]),
    ("体育", ["スポーツ", "野球", "サッカー", "カーリング", "相撲", "阪神", "大会"]),
    ("社会新闻", ["事故", "火災", "食中毒", "捜索", "病院", "デマ", "死亡", "事件", "警察"]),
]


def norm_title(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"（[^）]*）", "", t)
    t = re.sub(r"\([^\)]*\)", "", t)
    t = re.sub(r"\s*[-｜|].*$", "", t)
    return t.strip(" ・-–—")


def keyify(t: str) -> str:
    chunks = re.findall(r"[\u3040-\u30ff\u3400-\u9fffA-Za-z0-9]{2,}", t)
    return " ".join(chunks[:6]) if chunks else t


def classify(title: str) -> str:
    for cat, kws in KEYWORDS:
        for kw in kws:
            if kw in title:
                return cat
    return "社会新闻"


def fetch_items(url: str, limit: int = 20):
    data = urllib.request.urlopen(url, timeout=20).read()
    root = ET.fromstring(data)
    out = []
    for it in root.findall("./channel/item")[:limit]:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        if title:
            out.append((title, link))
    return out


def collect(region: str, concurrency: int = 6):
    if region != "jp":
        raise ValueError("Only --region jp is supported currently")

    concurrency = max(1, concurrency)
    bykey = defaultdict(list)

    def fetch_feed(entry):
        feed_name, url = entry
        try:
            return feed_name, fetch_items(url)
        except Exception:
            return feed_name, []

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        for feed_name, items in executor.map(fetch_feed, FEEDS_JP.items()):
            for idx, (title, link) in enumerate(items, start=1):
                ntitle = norm_title(title)
                key = keyify(ntitle)
                score = WEIGHTS.get(feed_name, 1.0) * (1.0 / (0.6 + 0.15 * idx))
                bykey[key].append(
                    {
                        "score": score,
                        "feed": feed_name,
                        "rank": idx,
                        "title": ntitle,
                        "link": link,
                    }
                )

    merged = []
    for k, vals in bykey.items():
        vals_sorted = sorted(vals, key=lambda x: x["score"], reverse=True)
        rep = vals_sorted[0]
        total = sum(v["score"] for v in vals)
        feeds = sorted(set(v["feed"] for v in vals))
        merged.append(
            {
                "key": k,
                "title": rep["title"],
                "link": rep["link"],
                "score": round(total, 3),
                "sources": feeds,
                "source_count": len(feeds),
                "category": classify(rep["title"]),
            }
        )

    merged.sort(key=lambda x: (x["score"], x["source_count"]), reverse=True)
    return merged


def render_telegram(items):
    grouped = defaultdict(list)
    for it in items:
        grouped[it["category"]].append(it)

    lines = []
    idx = 1
    for cat in CATEGORY_ORDER:
        arr = grouped.get(cat, [])
        if not arr:
            continue
        lines.append(f"{CATEGORY_EMOJI.get(cat, '🗞️')} {cat}")
        lines.append("•")
        for it in arr:
            lines.append(f"{idx}. **{it['title']}**")
            lines.append("（待补充中文解读）")
            lines.append("-")
            idx += 1
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--region", default="jp")
    p.add_argument("--format", choices=["json", "telegram"], default="json")
    p.add_argument("--concurrency", type=int, default=6)
    args = p.parse_args()

    merged = collect(args.region, concurrency=args.concurrency)[: args.top]

    if args.format == "json":
        print(json.dumps(merged, ensure_ascii=False, indent=2))
    else:
        print(render_telegram(merged))


if __name__ == "__main__":
    main()
