#!/usr/bin/env python3
"""
间隔复习调度器 — 基于艾宾浩斯遗忘曲线
用法:
  python3 review.py schedule --topic "xxx" --category "programming"
  python3 review.py due                                  # 列出今天需要复习的
  python3 review.py done --topic "xxx"                   # 标记已复习
  python3 review.py stats                                # 复习统计
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

KB_ROOT = Path(__file__).parent.parent.parent.parent / "knowledge-base"
REVIEW_PATH = KB_ROOT / "review-schedule.json"

# 艾宾浩斯复习间隔（天）
REVIEW_INTERVALS = [1, 3, 7, 14, 30, 90]


def load_schedule() -> Dict:
    if REVIEW_PATH.exists():
        with open(REVIEW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"items": [], "completed_reviews": 0, "total_items": 0}


def save_schedule(schedule: Dict):
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    with open(REVIEW_PATH, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)


def schedule_review(topic: str, category: str):
    """为新学的知识安排复习计划"""
    schedule = load_schedule()
    
    # 检查是否已有
    for item in schedule["items"]:
        if item["topic"].lower() == topic.lower():
            print(json.dumps({"status": "already_scheduled", "topic": topic}))
            return
    
    now = datetime.now()
    review_dates = []
    for interval in REVIEW_INTERVALS:
        review_date = now + timedelta(days=interval)
        review_dates.append({
            "interval_days": interval,
            "due_date": review_date.strftime("%Y-%m-%d"),
            "completed": False,
            "completed_at": None
        })
    
    item = {
        "topic": topic,
        "category": category,
        "learned_at": now.strftime("%Y-%m-%d"),
        "review_dates": review_dates,
        "current_level": 0,  # 当前复习等级（0=刚学，6=完全掌握）
        "last_reviewed": None
    }
    
    schedule["items"].append(item)
    schedule["total_items"] += 1
    save_schedule(schedule)
    
    print(json.dumps({
        "status": "scheduled",
        "topic": topic,
        "next_review": review_dates[0]["due_date"],
        "total_intervals": len(REVIEW_INTERVALS)
    }))


def get_due_reviews():
    """获取今天需要复习的知识"""
    schedule = load_schedule()
    today = datetime.now().strftime("%Y-%m-%d")
    
    due = []
    for item in schedule["items"]:
        for review in item["review_dates"]:
            if not review["completed"] and review["due_date"] <= today:
                due.append({
                    "topic": item["topic"],
                    "category": item["category"],
                    "interval_days": review["interval_days"],
                    "due_date": review["due_date"],
                    "learned_at": item["learned_at"],
                    "current_level": item["current_level"]
                })
                break  # 只取最近一个未完成的复习
    
    # 按到期日排序
    due.sort(key=lambda x: x["due_date"])
    
    result = {
        "today": today,
        "due_count": len(due),
        "items": due
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def mark_reviewed(topic: str):
    """标记已复习"""
    schedule = load_schedule()
    today = datetime.now().strftime("%Y-%m-%d")
    
    for item in schedule["items"]:
        if item["topic"].lower() == topic.lower():
            for review in item["review_dates"]:
                if not review["completed"] and review["due_date"] <= today:
                    review["completed"] = True
                    review["completed_at"] = datetime.now().isoformat()
                    item["current_level"] += 1
                    item["last_reviewed"] = today
                    schedule["completed_reviews"] += 1
                    save_schedule(schedule)
                    
                    # 计算下次复习
                    next_due = None
                    for r in item["review_dates"]:
                        if not r["completed"]:
                            next_due = r["due_date"]
                            break
                    
                    print(json.dumps({
                        "status": "reviewed",
                        "topic": topic,
                        "level": item["current_level"],
                        "next_review": next_due or "全部完成 ✅"
                    }))
                    return
    
    print(json.dumps({"error": f"没有找到待复习的: {topic}"}))


def get_review_stats():
    """复习统计"""
    schedule = load_schedule()
    
    total = len(schedule["items"])
    fully_mastered = sum(1 for i in schedule["items"] if i["current_level"] >= len(REVIEW_INTERVALS))
    in_progress = total - fully_mastered
    
    # 按分类统计
    by_category = {}
    for item in schedule["items"]:
        cat = item["category"]
        if cat not in by_category:
            by_category[cat] = {"total": 0, "mastered": 0}
        by_category[cat]["total"] += 1
        if item["current_level"] >= len(REVIEW_INTERVALS):
            by_category[cat]["mastered"] += 1
    
    # 即将到期
    today = datetime.now().strftime("%Y-%m-%d")
    week_later = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    upcoming = 0
    for item in schedule["items"]:
        for review in item["review_dates"]:
            if not review["completed"] and review["due_date"] <= week_later:
                upcoming += 1
                break
    
    result = {
        "total_topics": total,
        "fully_mastered": fully_mastered,
        "in_progress": in_progress,
        "completed_reviews": schedule.get("completed_reviews", 0),
        "upcoming_7_days": upcoming,
        "by_category": by_category,
        "mastery_rate": f"{fully_mastered/total*100:.0f}%" if total else "N/A"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="间隔复习调度器")
    sub = parser.add_subparsers(dest="command")
    
    sched_p = sub.add_parser("schedule")
    sched_p.add_argument("--topic", required=True)
    sched_p.add_argument("--category", default="other")
    
    sub.add_parser("due")
    
    done_p = sub.add_parser("done")
    done_p.add_argument("--topic", required=True)
    
    sub.add_parser("stats")
    
    args = parser.parse_args()
    
    if args.command == "schedule":
        schedule_review(args.topic, args.category)
    elif args.command == "due":
        get_due_reviews()
    elif args.command == "done":
        mark_reviewed(args.topic)
    elif args.command == "stats":
        get_review_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
