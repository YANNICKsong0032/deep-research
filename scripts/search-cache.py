#!/usr/bin/env python3
"""
搜索缓存 — 避免重复 fetch 同一 URL
用法:
  python3 search-cache.py get --url "https://..."
  python3 search-cache.py set --url "https://..." --content "..." --title "..."
  python3 search-cache.py stats
  python3 search-cache.py clean [--days 30]
"""

import json
import sys
import argparse
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

KB_ROOT = Path(__file__).parent.parent.parent.parent / "knowledge-base"
CACHE_PATH = KB_ROOT / ".search-cache.json"
MAX_CACHE_SIZE = 500  # 最多缓存 500 条


def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": {}, "hits": 0, "misses": 0, "created_at": datetime.now().isoformat()}


def save_cache(cache):
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


def url_hash(url):
    return hashlib.md5(url.encode()).hexdigest()[:12]


def get_cached(url):
    cache = load_cache()
    key = url_hash(url)
    
    if key in cache["entries"]:
        entry = cache["entries"][key]
        if entry.get("url") == url:
            cache["hits"] += 1
            save_cache(cache)
            
            # 检查是否过期（7 天）
            cached_at = entry.get("cached_at", "")
            if cached_at:
                age_days = (datetime.now() - datetime.fromisoformat(cached_at)).days
                if age_days > 7:
                    print(json.dumps({"status": "expired", "age_days": age_days}))
                    return
            
            print(json.dumps({
                "status": "hit",
                "title": entry.get("title", ""),
                "content": entry.get("content", "")[:200] + "...",
                "cached_at": entry.get("cached_at"),
                "hits": cache["hits"]
            }))
            return
    
    cache["misses"] += 1
    save_cache(cache)
    print(json.dumps({"status": "miss", "url": url}))


def set_cached(url, content, title=""):
    cache = load_cache()
    key = url_hash(url)
    
    # 如果缓存满了，删除最旧的
    if len(cache["entries"]) >= MAX_CACHE_SIZE:
        oldest_key = min(cache["entries"], key=lambda k: cache["entries"][k].get("cached_at", ""))
        del cache["entries"][oldest_key]
    
    cache["entries"][key] = {
        "url": url,
        "title": title,
        "content": content[:5000],  # 限制缓存大小
        "cached_at": datetime.now().isoformat(),
        "fetch_count": cache["entries"].get(key, {}).get("fetch_count", 0) + 1
    }
    save_cache(cache)
    print(json.dumps({"status": "cached", "key": key, "size": len(content)}))


def get_stats():
    cache = load_cache()
    total = len(cache["entries"])
    hits = cache.get("hits", 0)
    misses = cache.get("misses", 0)
    hit_rate = f"{hits/(hits+misses)*100:.0f}%" if (hits + misses) > 0 else "N/A"
    
    # 最常访问的
    top = sorted(cache["entries"].values(), key=lambda e: e.get("fetch_count", 0), reverse=True)[:5]
    
    result = {
        "total_entries": total,
        "max_size": MAX_CACHE_SIZE,
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "top_accessed": [{"title": e.get("title", ""), "url": e.get("url", ""), "count": e.get("fetch_count", 0)} for e in top]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def clean_cache(days=30):
    cache = load_cache()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    
    before = len(cache["entries"])
    cache["entries"] = {k: v for k, v in cache["entries"].items() if v.get("cached_at", "") > cutoff}
    after = len(cache["entries"])
    
    save_cache(cache)
    print(json.dumps({"status": "cleaned", "removed": before - after, "remaining": after}))


def main():
    parser = argparse.ArgumentParser(description="搜索缓存")
    sub = parser.add_subparsers(dest="command")
    
    get_p = sub.add_parser("get")
    get_p.add_argument("--url", required=True)
    
    set_p = sub.add_parser("set")
    set_p.add_argument("--url", required=True)
    set_p.add_argument("--content", required=True)
    set_p.add_argument("--title", default="")
    
    sub.add_parser("stats")
    
    clean_p = sub.add_parser("clean")
    clean_p.add_argument("--days", type=int, default=30)
    
    args = parser.parse_args()
    
    if args.command == "get":
        get_cached(args.url)
    elif args.command == "set":
        set_cached(args.url, args.content, args.title)
    elif args.command == "stats":
        get_stats()
    elif args.command == "clean":
        clean_cache(args.days)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
