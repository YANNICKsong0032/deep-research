#!/usr/bin/env python3
"""
知识库管理器 v2 — 索引、搜索、统计、学习历史、过期检查
用法:
  python3 knowledge.py init                                    # 初始化
  python3 knowledge.py add --topic "xxx" --category "ai" --tags "llm,prompt" --confidence 4.5 --sources 3
  python3 knowledge.py search --query "python async"
  python3 knowledge.py stats
  python3 knowledge.py list [--category ai]
  python3 knowledge.py history [--limit 10]
  python3 knowledge.py expire [--months 6]
  python3 knowledge.py relations --topic "xxx"
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

KB_ROOT = Path(__file__).parent.parent.parent.parent / "knowledge-base"
INDEX_PATH = KB_ROOT / "INDEX.json"
HISTORY_PATH = KB_ROOT / "learning-history.json"

# 分类 → 过期月数
EXPIRY_MONTHS = {
    "programming": 6, "ai": 6, "frontend": 6, "backend": 6,
    "devops": 6, "tools": 6, "design": 12, "business": 12,
    "science": 24, "culture": 24, "life": 12, "other": 12,
}


def init_kb():
    """初始化知识库"""
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    categories = [
        "programming", "ai", "frontend", "backend", "devops",
        "tools", "design", "business", "science", "culture", "life", "other"
    ]
    for cat in categories:
        (KB_ROOT / cat).mkdir(exist_ok=True)

    if not INDEX_PATH.exists():
        index = {
            "version": 2,
            "last_updated": datetime.now().isoformat(),
            "entries": [],
            "categories": {cat: {"count": 0, "topics": []} for cat in categories},
            "relations": []
        }
        save_index(index)
        print(json.dumps({"status": "initialized", "categories": len(categories)}))
    else:
        print(json.dumps({"status": "already_exists"}))

    if not HISTORY_PATH.exists():
        save_history({"sessions": [], "total_sessions": 0, "total_duration_minutes": 0, "most_studied": {}})


def load_index() -> Dict[str, Any]:
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 2, "last_updated": "", "entries": [], "categories": {}, "relations": []}


def save_index(index: Dict[str, Any]):
    index["last_updated"] = datetime.now().isoformat()
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def load_history() -> Dict[str, Any]:
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sessions": [], "total_sessions": 0, "total_duration_minutes": 0, "most_studied": {}}


def save_history(history: Dict[str, Any]):
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_entry(topic: str, category: str, tags: List[str],
              confidence: float, sources: int, summary: str = "",
              related: List[str] = None):
    """添加知识条目"""
    index = load_index()

    # 检查是否已存在
    for entry in index["entries"]:
        if entry["topic"].lower() == topic.lower():
            entry["confidence"] = round((entry["confidence"] + confidence) / 2, 1)
            entry["sources"] = max(entry["sources"], sources)
            entry["learned_at"] = datetime.now().strftime("%Y-%m-%d")
            entry["tags"] = list(set(entry["tags"] + tags))
            if summary:
                entry["summary"] = summary
            save_index(index)
            print(json.dumps({"status": "updated", "topic": topic}))
            return

    entry = {
        "topic": topic,
        "category": category,
        "file": f"{category}/{topic.lower().replace(' ', '-')}.md",
        "learned_at": datetime.now().strftime("%Y-%m-%d"),
        "confidence": confidence,
        "sources": sources,
        "tags": tags,
        "summary": summary,
        "related": related or []
    }
    index["entries"].append(entry)

    if category not in index["categories"]:
        index["categories"][category] = {"count": 0, "topics": []}
    index["categories"][category]["count"] += 1
    index["categories"][category]["topics"].append(topic)

    save_index(index)
    print(json.dumps({"status": "added", "topic": topic, "category": category}))


def add_relation(topic_a: str, topic_b: str, relation_type: str):
    """添加知识关联"""
    index = load_index()
    relation = {
        "from": topic_a,
        "to": topic_b,
        "type": relation_type,  # prerequisite / complementary / extends
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    if "relations" not in index:
        index["relations"] = []
    index["relations"].append(relation)
    save_index(index)
    print(json.dumps({"status": "relation_added", "from": topic_a, "to": topic_b, "type": relation_type}))


def search_kb(query: str, limit: int = 5) -> List[Dict]:
    """搜索知识库"""
    index = load_index()
    query_lower = query.lower()
    query_words = set(query_lower.split())

    results = []
    for entry in index["entries"]:
        score = 0
        topic_lower = entry["topic"].lower()
        tags = [t.lower() for t in entry.get("tags", [])]
        summary = entry.get("summary", "").lower()

        if query_lower == topic_lower:
            score += 10
        elif query_lower in topic_lower:
            score += 5
        tag_hits = len(query_words & set(tags))
        score += tag_hits * 2
        if summary:
            for word in query_words:
                if word in summary:
                    score += 1

        if score > 0:
            results.append({**entry, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def get_relations(topic: str) -> Dict:
    """获取知识关联"""
    index = load_index()
    relations = index.get("relations", [])

    related = {
        "prerequisite": [],  # 前置知识
        "complementary": [],  # 互补知识
        "extends": [],  # 扩展知识
        "extended_by": []  # 被扩展
    }

    for r in relations:
        if r["from"].lower() == topic.lower():
            rtype = r.get("type", "complementary")
            if rtype in related:
                related[rtype].append(r["to"])
        if r["to"].lower() == topic.lower():
            if r.get("type") == "extends":
                related["extended_by"].append(r["from"])
            else:
                related["complementary"].append(r["from"])

    return related


def record_learning_session(topic: str, category: str, duration: int,
                            sub_questions: int, completed: int,
                            confirmed: int, uncertain: int, contradicted: int,
                            report_file: str = "", knowledge_file: str = ""):
    """记录学习历史"""
    history = load_history()

    session = {
        "id": f"{datetime.now().strftime('%Y-%m-%d')}-{topic.lower().replace(' ', '-')}",
        "topic": topic,
        "started_at": (datetime.now() - timedelta(minutes=duration)).isoformat(),
        "completed_at": datetime.now().isoformat(),
        "duration_minutes": duration,
        "sub_questions": sub_questions,
        "completed": completed,
        "findings": {
            "confirmed": confirmed,
            "uncertain": uncertain,
            "contradicted": contradicted
        },
        "category": category,
        "status": "completed",
        "report_file": report_file,
        "knowledge_file": knowledge_file
    }

    history["sessions"].append(session)
    history["total_sessions"] += 1
    history["total_duration_minutes"] += duration

    if category not in history["most_studied"]:
        history["most_studied"][category] = 0
    history["most_studied"][category] += 1

    save_history(history)
    print(json.dumps({"status": "recorded", "session_id": session["id"]}))


def get_history(limit: int = 10):
    """获取学习历史"""
    history = load_history()
    sessions = history["sessions"][-limit:]
    result = {
        "total_sessions": history["total_sessions"],
        "total_duration_minutes": history["total_duration_minutes"],
        "most_studied": history["most_studied"],
        "recent_sessions": sessions
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def check_expired(months: int = 6):
    """检查过期知识"""
    index = load_index()
    cutoff = datetime.now() - timedelta(days=months * 30)
    cutoff_str = cutoff.strftime("%Y-%m-%d")

    expired = []
    expiring_soon = []

    for entry in index["entries"]:
        learned = entry.get("learned_at", "")
        if not learned:
            continue

        category = entry.get("category", "other")
        expiry_months = EXPIRY_MONTHS.get(category, 12)
        expiry_date = datetime.strptime(learned, "%Y-%m-%d") + timedelta(days=expiry_months * 30)
        days_left = (expiry_date - datetime.now()).days

        if days_left < 0:
            expired.append({"topic": entry["topic"], "category": category, "learned_at": learned, "days_expired": -days_left})
        elif days_left < 30:
            expiring_soon.append({"topic": entry["topic"], "category": category, "days_left": days_left})

    result = {
        "expired": expired,
        "expiring_soon": expiring_soon,
        "total_expired": len(expired),
        "total_expiring_soon": len(expiring_soon)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def list_entries(category: Optional[str] = None):
    index = load_index()
    entries = index["entries"]
    if category:
        entries = [e for e in entries if e["category"] == category]
    print(json.dumps({"total": len(entries), "entries": entries}, ensure_ascii=False, indent=2))


def get_stats():
    index = load_index()
    history = load_history()
    total = len(index["entries"])
    confidences = [e.get("confidence", 0) for e in index["entries"]]
    avg_confidence = sum(confidences) / total if total else 0
    total_sources = sum(e.get("sources", 0) for e in index["entries"])

    result = {
        "total_topics": total,
        "average_confidence": round(avg_confidence, 2),
        "total_sources": total_sources,
        "categories": {k: v["count"] for k, v in index.get("categories", {}).items() if v["count"] > 0},
        "relations_count": len(index.get("relations", [])),
        "learning_sessions": history.get("total_sessions", 0),
        "total_learning_hours": round(history.get("total_duration_minutes", 0) / 60, 1),
        "last_updated": index.get("last_updated", "never")
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="知识库管理器 v2")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init")

    add_p = sub.add_parser("add")
    add_p.add_argument("--topic", required=True)
    add_p.add_argument("--category", required=True)
    add_p.add_argument("--tags", default="")
    add_p.add_argument("--confidence", type=float, default=3.0)
    add_p.add_argument("--sources", type=int, default=1)
    add_p.add_argument("--summary", default="")
    add_p.add_argument("--related", default="")

    search_p = sub.add_parser("search")
    search_p.add_argument("--query", required=True)
    search_p.add_argument("--limit", type=int, default=5)

    list_p = sub.add_parser("list")
    list_p.add_argument("--category", default=None)

    sub.add_parser("stats")

    hist_p = sub.add_parser("history")
    hist_p.add_argument("--limit", type=int, default=10)

    expire_p = sub.add_parser("expire")
    expire_p.add_argument("--months", type=int, default=6)

    rel_p = sub.add_parser("relations")
    rel_p.add_argument("--topic", required=True)

    rec_p = sub.add_parser("record")
    rec_p.add_argument("--topic", required=True)
    rec_p.add_argument("--category", required=True)
    rec_p.add_argument("--duration", type=int, default=0)
    rec_p.add_argument("--sub-questions", type=int, default=0)
    rec_p.add_argument("--completed", type=int, default=0)
    rec_p.add_argument("--confirmed", type=int, default=0)
    rec_p.add_argument("--uncertain", type=int, default=0)
    rec_p.add_argument("--contradicted", type=int, default=0)
    rec_p.add_argument("--report-file", default="")
    rec_p.add_argument("--knowledge-file", default="")

    args = parser.parse_args()

    if args.command == "init":
        init_kb()
    elif args.command == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        related = [r.strip() for r in args.related.split(",") if r.strip()]
        add_entry(args.topic, args.category, tags, args.confidence, args.sources, args.summary, related)
    elif args.command == "search":
        results = search_kb(args.query, args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.command == "list":
        list_entries(args.category)
    elif args.command == "stats":
        get_stats()
    elif args.command == "history":
        get_history(args.limit)
    elif args.command == "expire":
        check_expired(args.months)
    elif args.command == "relations":
        rels = get_relations(args.topic)
        print(json.dumps(rels, ensure_ascii=False, indent=2))
    elif args.command == "record":
        record_learning_session(args.topic, args.category, args.duration,
                                args.sub_questions, args.completed,
                                args.confirmed, args.uncertain, args.contradicted,
                                args.report_file, args.knowledge_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
