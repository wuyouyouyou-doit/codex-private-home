#!/usr/bin/env python3
"""Resilient feed fetcher for ai-news-app-radar.

Usage:
  python skills/ai-news-app-radar/scripts/resilient_feed_fetch.py \
    --registry skills/ai-news-app-radar/references/source_registry_free.yaml \
    --out outputs/$(date +%F)/candidates.json
"""
from __future__ import annotations
import argparse
import glob
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

UA = "Mozilla/5.0 (compatible; ai-news-app-radar/1.0)"


def load_sources(path: str) -> list[dict]:
    sources = []
    cur = None
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if re.match(r"^\s*- id:", line):
                if cur:
                    sources.append(cur)
                cur = {"id": line.split(":", 1)[1].strip()}
            elif cur and re.match(r"^\s+name:", line):
                cur["name"] = line.split(":", 1)[1].strip()
            elif cur and re.match(r"^\s+url:", line):
                cur["url"] = line.split(":", 1)[1].strip()
            elif cur and re.match(r"^\s+layer:", line):
                cur["layer"] = line.split(":", 1)[1].strip()
            elif cur and re.match(r"^\s+weight:", line):
                cur["weight"] = float(line.split(":", 1)[1].strip())
    if cur:
        sources.append(cur)
    return [s for s in sources if s.get("url")]


def variants(url: str) -> list[tuple[str, str]]:
    encoded = urllib.parse.quote(url, safe="")
    return [
        ("direct", url),
        ("jina-ai-http", f"https://r.jina.ai/http://{url.removeprefix('https://').removeprefix('http://')}") ,
        ("jina-ai-https", f"https://r.jina.ai/{url}"),
        ("rsshub", f"https://rsshub.app/rsshub/atom?url={encoded}"),
    ]


def fetch(url: str, timeout: int) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return value


def parse_feed(blob: bytes) -> list[dict]:
    root = ET.fromstring(blob)
    out = []
    if root.tag.lower().endswith("rss") or "rss" in root.tag.lower():
        for it in root.findall(".//item"):
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            pub = parse_date(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date"))
            desc = (it.findtext("description") or "").strip()
            if title and link:
                out.append({"title": title, "url": link, "published": pub, "summary": desc})
    else:
        ns = "{http://www.w3.org/2005/Atom}"
        for it in root.findall(f".//{ns}entry"):
            title = (it.findtext(f"{ns}title") or "").strip()
            link_node = it.find(f"{ns}link")
            link = (link_node.attrib.get("href", "") if link_node is not None else "").strip()
            pub = parse_date(it.findtext(f"{ns}updated") or it.findtext(f"{ns}published"))
            desc = (it.findtext(f"{ns}summary") or it.findtext(f"{ns}content") or "").strip()
            if title and link:
                out.append({"title": title, "url": link, "published": pub, "summary": desc})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--cache-glob", default="outputs/*/candidates.json")
    ap.add_argument("--bootstrap", default="skills/ai-news-app-radar/references/bootstrap_candidates.json")
    args = ap.parse_args()

    sources = load_sources(args.registry)
    report = {"generated_at": datetime.utcnow().isoformat() + "Z", "sources": [], "items": []}

    for s in sources:
        status = {"id": s.get("id"), "name": s.get("name"), "url": s.get("url"), "ok": False, "method": None, "error": None, "count": 0}
        for method, u in variants(s["url"]):
            try:
                data = fetch(u, args.timeout)
                items = parse_feed(data)
                if items:
                    for item in items:
                        item["source"] = s.get("name")
                        item["source_id"] = s.get("id")
                        item["source_weight"] = s.get("weight")
                        report["items"].append(item)
                    status.update({"ok": True, "method": method, "count": len(items)})
                    break
            except Exception as e:
                status["error"] = str(e)
        report["sources"].append(status)


    # Outage fallback: reuse last successful local cache if all sources fail
    if not report["items"]:
        caches = sorted(glob.glob(args.cache_glob), reverse=True)
        for cp in caches:
            if cp == args.out:
                continue
            try:
                with open(cp, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                cached_items = cached.get("items", [])
                if cached_items:
                    report["items"] = cached_items
                    report["cache_fallback_used"] = cp
                    break
            except Exception:
                pass

    if not report["items"]:
        try:
            with open(args.bootstrap, "r", encoding="utf-8") as f:
                boot = json.load(f)
            if boot.get("items"):
                report["items"] = boot["items"]
                report["bootstrap_fallback_used"] = args.bootstrap
        except Exception:
            pass

    # simple dedupe
    seen = set()
    deduped = []
    for it in report["items"]:
        k = (re.sub(r"\W+", "", it.get("title", "").lower())[:120], it.get("url"))
        if k in seen:
            continue
        seen.add(k)
        deduped.append(it)
    report["items"] = deduped

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    ok = sum(1 for s in report["sources"] if s["ok"])
    print(f"sources_ok={ok}/{len(report['sources'])} items={len(report['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
