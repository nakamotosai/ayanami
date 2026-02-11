#!/usr/bin/env python3
import hashlib
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = SKILL_ROOT / "config" / "sources.yaml"
DOCS_DIR = SKILL_ROOT / "docs"
REFS_DIR = SKILL_ROOT / "references"
REFS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

CORE_NAMESPACE = "docs/"


def sanitize_filename(url: str) -> str:
    cleaned = re.sub(r"https?://", "", url)
    cleaned = re.sub(r"[^0-9a-zA-Z._-]+", "_", cleaned)
    return cleaned.strip("_")


def fetch_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_sources():
    if not CONFIG_FILE.exists():
        return []
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", []) or []


def fetch_for_source(source):
    sitemap = source.get("sitemap")
    if not sitemap:
        return {}
    print(f"Fetching sitemap for {source['name']}…")
    try:
        data = fetch_url(sitemap)
    except Exception as exc:
        print("  sitemap failed:", exc)
        return {}
    root = ET.fromstring(data)
    urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    urls = [u for u in urls if u]
    max_pages = source.get("max_pages", 30)
    manifest = {}
    for idx, url in enumerate(urls[:max_pages]):
        print(f"[{idx+1}/{min(max_pages, len(urls))}] {url}")
        try:
            content = fetch_url(url)
        except Exception as exc:
            print("  failed:", exc)
            continue
        name = sanitize_filename(url)
        site_folder = DOCS_DIR / source["name"]
        site_folder.mkdir(parents=True, exist_ok=True)
        file_path = site_folder / f"{name}.html"
        file_path.write_text(content, encoding="utf-8")
        manifest[url] = {
            "source": source["name"],
            "path": str(file_path.relative_to(SKILL_ROOT)),
            "digest": digest(content),
            "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        }
    return manifest


def main():
    sources = load_sources()
    if not sources:
        print("No sources configured, please add entries to config/sources.yaml")
        return
    aggregated = {}
    for source in sources:
        aggregated.update(fetch_for_source(source))
    manifest_path = REFS_DIR / "docs_manifest.json"
    manifest_path.write_text(json.dumps(aggregated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved manifest with {len(aggregated)} entries to {manifest_path}")


if __name__ == "__main__":
    main()
