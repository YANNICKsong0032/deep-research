#!/usr/bin/env python3
"""
学习进度追踪器 — 支持中断恢复
用法:
  python3 progress.py init --topic "xxx" --sub-questions '["q1","q2"]'
  python3 progress.py update --topic "xxx" --index 1 --status "done" --findings '{"title":"...","content":"..."}'
  python3 progress.py status --topic "xxx"
  python3 progress.py resume --topic "xxx"
  python3 progress.py list
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROGRESS_DIR = Path(__file__).parent.parent.parent.parent / "knowledge-base" / ".progress"


def init_progress(topic: str, sub_questions: List[str]):
    """初始化学习进度"""
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    slug = topic.lower().replace(" ", "-")
    
    progress = {
        "topic": topic,
        "slug": slug,
        "started_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "in_progress",  # in_progress | paused | completed | abandoned
        "sub_questions": [
            {
                "index": i + 1,
                "question": q,
                "status": "pending",  # pending | searching | done | failed | skipped
                "findings": [],
                "sources": [],
                "confidence": 0,
                "started_at": None,
                "completed_at": None
            }
            for i, q in enumerate(sub_questions)
        ],
        "stats": {
            "searches": 0,
            "pages_read": 0,
            "confirmed": 0,
            "uncertain": 0,
            "failed": 0
        },
        "report_file": None,
        "knowledge_file": None
    }
    
    path = PROGRESS_DIR / f"{slug}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    print(json.dumps({"status": "initialized", "topic": topic, "sub_questions": len(sub_questions), "file": str(path)}))


def update_progress(topic: str, index: int, status: str, 
                   findings: Dict = None, sources: List = None, confidence: float = 0):
    """更新子问题进度"""
    slug = topic.lower().replace(" ", "-")
    path = PROGRESS_DIR / f"{slug}.json"
    
    if not path.exists():
        print(json.dumps({"error": f"进度文件不存在: {slug}.json"}))
        return
    
    with open(path, "r", encoding="utf-8") as f:
        progress = json.load(f)
    
    # 找到对应的子问题
    sq = None
    for q in progress["sub_questions"]:
        if q["index"] == index:
            sq = q
            break
    
    if not sq:
        print(json.dumps({"error": f"子问题 {index} 不存在"}))
        return
    
    # 更新
    sq["status"] = status
    if findings:
        sq["findings"].append(findings)
    if sources:
        sq["sources"].extend(sources)
    if confidence:
        sq["confidence"] = confidence
    
    if status == "searching" and not sq["started_at"]:
        sq["started_at"] = datetime.now().isoformat()
    elif status in ("done", "failed", "skipped"):
        sq["completed_at"] = datetime.now().isoformat()
    
    # 更新统计
    if status == "done":
        if confidence >= 4.0:
            progress["stats"]["confirmed"] += 1
        elif confidence >= 2.5:
            progress["stats"]["uncertain"] += 1
    elif status == "failed":
        progress["stats"]["failed"] += 1
    
    progress["updated_at"] = datetime.now().isoformat()
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 计算总进度
    total = len(progress["sub_questions"])
    done = sum(1 for q in progress["sub_questions"] if q["status"] in ("done", "failed", "skipped"))
    
    print(json.dumps({
        "status": "updated",
        "question": index,
        "new_status": status,
        "progress": f"{done}/{total}",
        "percent": round(done / total * 100) if total else 0
    }))


def get_status(topic: str):
    """获取学习进度"""
    slug = topic.lower().replace(" ", "-")
    path = PROGRESS_DIR / f"{slug}.json"
    
    if not path.exists():
        print(json.dumps({"error": f"进度文件不存在: {slug}.json"}))
        return
    
    with open(path, "r", encoding="utf-8") as f:
        progress = json.load(f)
    
    total = len(progress["sub_questions"])
    done = sum(1 for q in progress["sub_questions"] if q["status"] in ("done", "failed", "skipped"))
    pending = [q for q in progress["sub_questions"] if q["status"] == "pending"]
    searching = [q for q in progress["sub_questions"] if q["status"] == "searching"]
    
    result = {
        "topic": progress["topic"],
        "status": progress["status"],
        "started_at": progress["started_at"],
        "updated_at": progress["updated_at"],
        "progress": f"{done}/{total}",
        "percent": round(done / total * 100) if total else 0,
        "pending": len(pending),
        "searching": len(searching),
        "stats": progress["stats"],
        "next_question": pending[0]["index"] if pending else None,
        "sub_questions": [
            {"index": q["index"], "question": q["question"], "status": q["status"]}
            for q in progress["sub_questions"]
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def resume_progress(topic: str):
    """恢复学习（返回下一个待处理的子问题）"""
    slug = topic.lower().replace(" ", "-")
    path = PROGRESS_DIR / f"{slug}.json"
    
    if not path.exists():
        print(json.dumps({"error": "没有找到学习进度"}))
        return
    
    with open(path, "r", encoding="utf-8") as f:
        progress = json.load(f)
    
    progress["status"] = "in_progress"
    progress["updated_at"] = datetime.now().isoformat()
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 返回待处理的子问题
    pending = [q for q in progress["sub_questions"] if q["status"] == "pending"]
    searching = [q for q in progress["sub_questions"] if q["status"] == "searching"]
    
    result = {
        "status": "resumed",
        "topic": progress["topic"],
        "pending": len(pending),
        "searching": len(searching),
        "next_questions": [
            {"index": q["index"], "question": q["question"]}
            for q in (searching + pending)[:3]  # 返回前 3 个待处理
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def list_progress():
    """列出所有学习进度"""
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    
    sessions = []
    for path in sorted(PROGRESS_DIR.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            progress = json.load(f)
        
        total = len(progress["sub_questions"])
        done = sum(1 for q in progress["sub_questions"] if q["status"] in ("done", "failed", "skipped"))
        
        sessions.append({
            "topic": progress["topic"],
            "status": progress["status"],
            "progress": f"{done}/{total}",
            "percent": round(done / total * 100) if total else 0,
            "updated_at": progress["updated_at"]
        })
    
    print(json.dumps({"sessions": sessions, "total": len(sessions)}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="学习进度追踪器")
    sub = parser.add_subparsers(dest="command")
    
    init_p = sub.add_parser("init")
    init_p.add_argument("--topic", required=True)
    init_p.add_argument("--sub-questions", required=True, help="JSON 数组")
    
    update_p = sub.add_parser("update")
    update_p.add_argument("--topic", required=True)
    update_p.add_argument("--index", type=int, required=True)
    update_p.add_argument("--status", required=True, choices=["searching", "done", "failed", "skipped"])
    update_p.add_argument("--findings", default=None, help="JSON 对象")
    update_p.add_argument("--sources", default=None, help="JSON 数组")
    update_p.add_argument("--confidence", type=float, default=0)
    
    status_p = sub.add_parser("status")
    status_p.add_argument("--topic", required=True)
    
    resume_p = sub.add_parser("resume")
    resume_p.add_argument("--topic", required=True)
    
    sub.add_parser("list")
    
    args = parser.parse_args()
    
    if args.command == "init":
        sub_questions = json.loads(args.sub_questions)
        init_progress(args.topic, sub_questions)
    elif args.command == "update":
        findings = json.loads(args.findings) if args.findings else None
        sources = json.loads(args.sources) if args.sources else None
        update_progress(args.topic, args.index, args.status, findings, sources, args.confidence)
    elif args.command == "status":
        get_status(args.topic)
    elif args.command == "resume":
        resume_progress(args.topic)
    elif args.command == "list":
        list_progress()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
