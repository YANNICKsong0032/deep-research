#!/usr/bin/env python3
"""
统一入口 — 一个脚本搞定所有操作，减少 exec 调用次数
用法:
  python3 learn.py quick "React Hooks"           # 快速学习（~10 次请求）
  python3 learn.py study "React Hooks"            # 标准学习（~25 次请求）
  python3 learn.py deep "React Hooks"             # 深度研究（~40 次请求）
  python3 learn.py url "https://..."              # 从 URL 学习
  python3 learn.py verify "React Hooks"           # 验证已有知识
  python3 learn.py import-memory                  # 导入记忆
  python3 learn.py review-due                     # 今日待复习
  python3 learn.py stats                          # 学习统计
  python3 learn.py search "query"                 # 搜索知识库
  python3 learn.py expire                         # 过期检查
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 将 scripts 目录加入 path
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from knowledge import load_index, search_kb, add_entry, get_stats, check_expired, load_history
from review import load_schedule, get_due_reviews


def cmd_quick(topic):
    """快速学习：生成 3 个子问题 + 研究计划"""
    from questions import generate_questions
    questions = generate_questions(topic, "shallow")
    result = {
        "mode": "quick",
        "topic": topic,
        "questions": questions,
        "estimated_requests": 10,
        "estimated_minutes": 15,
        "instructions": "按顺序搜索每个问题，web_search 1 次 + web_fetch top 1，完成后生成报告。"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_study(topic):
    """标准学习：生成 8 个子问题 + 研究计划"""
    from questions import generate_questions
    questions = generate_questions(topic, "medium")
    
    # 检查已有知识
    existing = search_kb(topic, limit=3)
    
    result = {
        "mode": "standard",
        "topic": topic,
        "questions": questions,
        "existing_knowledge": [{"topic": e["topic"], "confidence": e.get("confidence", 0)} for e in existing],
        "estimated_requests": 25,
        "estimated_minutes": 45,
        "instructions": "先检查缓存，缓存命中跳过搜索。每题 web_search 1-2 次 + web_fetch top 1。每 3 题更新进度。"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_deep(topic):
    """深度研究：生成 12 个子问题 + 研究计划"""
    from questions import generate_questions
    questions = generate_questions(topic, "deep")
    
    existing = search_kb(topic, limit=5)
    
    result = {
        "mode": "deep",
        "topic": topic,
        "questions": questions,
        "existing_knowledge": [{"topic": e["topic"], "confidence": e.get("confidence", 0)} for e in existing],
        "estimated_requests": 40,
        "estimated_minutes": 90,
        "instructions": "完整流程：多源搜索 + 交叉验证 + 代码验证 + 知识关联。"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_url(url):
    """从 URL 学习：直接抓取 + 提取知识点"""
    result = {
        "mode": "url",
        "url": url,
        "estimated_requests": 3,
        "instructions": "1. web_fetch(url) 抓取全文\n2. 提取关键知识点\n3. 评估可信度\n4. 生成总结\n5. 用户确认后入库"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_verify(topic):
    """验证已有知识"""
    existing = search_kb(topic, limit=10)
    result = {
        "mode": "verify",
        "topic": topic,
        "existing_knowledge": [{"topic": e["topic"], "confidence": e.get("confidence", 0), "learned_at": e.get("learned_at", "")} for e in existing],
        "estimated_requests": 5,
        "instructions": "1. 读取已有知识\n2. 联网搜索最新信息\n3. 对比差异\n4. 生成验证报告"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_search(query):
    """搜索知识库"""
    results = search_kb(query, limit=5)
    print(json.dumps({"query": query, "results": results}, ensure_ascii=False, indent=2))


def cmd_stats():
    """学习统计"""
    get_stats()


def cmd_review_due():
    """今日待复习"""
    get_due_reviews()


def cmd_expire():
    """过期检查"""
    check_expired()


def cmd_import_memory():
    """导入记忆"""
    from import_memory import import_from_file
    memory_file = Path.home() / ".openclaw" / "workspace" / "MEMORY.md"
    result = import_from_file(str(memory_file))
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    commands = {
        "quick": lambda: cmd_quick(sys.argv[2] if len(sys.argv) > 2 else ""),
        "study": lambda: cmd_study(sys.argv[2] if len(sys.argv) > 2 else ""),
        "deep": lambda: cmd_deep(sys.argv[2] if len(sys.argv) > 2 else ""),
        "url": lambda: cmd_url(sys.argv[2] if len(sys.argv) > 2 else ""),
        "verify": lambda: cmd_verify(sys.argv[2] if len(sys.argv) > 2 else ""),
        "search": lambda: cmd_search(sys.argv[2] if len(sys.argv) > 2 else ""),
        "stats": cmd_stats,
        "review-due": cmd_review_due,
        "expire": cmd_expire,
        "import-memory": cmd_import_memory,
    }
    
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
