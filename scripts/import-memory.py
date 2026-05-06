#!/usr/bin/env python3
"""
从已有记忆导入知识到 knowledge-base
用法:
  python3 import-memory.py                    # 扫描 MEMORY.md
  python3 import-memory.py --file memory/2026-05-06.md  # 扫描指定文件
  python3 import-memory.py --dry-run          # 只预览不写入
"""

import json
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
KB_ROOT = WORKSPACE / "knowledge-base"
MEMORY_FILE = WORKSPACE / "MEMORY.md"


def extract_knowledge_from_text(text: str, source: str) -> list:
    """从文本中提取知识点"""
    findings = []
    
    # 提取项目信息
    projects = re.findall(r'###?\s*(\w[\w\s-]+)\n([\s\S]*?)(?=###|\Z)', text)
    for title, content in projects:
        title = title.strip()
        if len(content.strip()) > 50:
            findings.append({
                "topic": title,
                "content": content.strip()[:500],
                "source": source,
                "type": "project"
            })
    
    # 提取技术栈
    tech_patterns = [
        r'(?:技术栈|Tech Stack|Stack)[：:]\s*(.+)',
        r'(?:使用|Using|用)[：:]\s*(.+)',
        r'(?:安装|Installed)[：:]\s*(.+)',
    ]
    for pattern in tech_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            findings.append({
                "topic": f"技术栈: {match[:50]}",
                "content": match,
                "source": source,
                "type": "tech_stack"
            })
    
    # 提取经验教训
    lessons = re.findall(r'(?:教训|经验|Lesson|Tip)[：:]\s*(.+)', text, re.IGNORECASE)
    for lesson in lessons:
        findings.append({
            "topic": f"经验: {lesson[:50]}",
            "content": lesson,
            "source": source,
            "type": "lesson"
        })
    
    return findings


def categorize_finding(finding: dict) -> str:
    """自动分类"""
    topic_lower = finding["topic"].lower()
    content_lower = finding.get("content", "").lower()
    combined = topic_lower + " " + content_lower
    
    if any(kw in combined for kw in ["react", "vue", "frontend", "css", "tailwind", "animation"]):
        return "frontend"
    elif any(kw in combined for kw in ["python", "node", "api", "backend", "express", "fastapi"]):
        return "backend"
    elif any(kw in combined for kw in ["ai", "llm", "model", "prompt", "agent", "mimo"]):
        return "ai"
    elif any(kw in combined for kw in ["docker", "linux", "deploy", "ci", "server"]):
        return "devops"
    elif any(kw in combined for kw in ["electron", "react", "typescript", "vite", "tailwind"]):
        return "frontend"
    elif any(kw in combined for kw in ["email", "qq", "feishu", "tool"]):
        return "tools"
    elif any(kw in combined for kw in ["ppt", "design", "ui", "ux"]):
        return "design"
    else:
        return "other"


def import_from_file(filepath: str, dry_run: bool = False) -> dict:
    """从文件导入知识"""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"文件不存在: {filepath}"}
    
    text = path.read_text(encoding="utf-8")
    source = str(path.name)
    findings = extract_knowledge_from_text(text, source)
    
    imported = []
    for f in findings:
        category = categorize_finding(f)
        entry = {
            "topic": f["topic"],
            "category": category,
            "content": f["content"],
            "source": source,
            "type": f["type"]
        }
        imported.append(entry)
        
        if not dry_run:
            # 这里会调用 knowledge.py add
            pass
    
    return {
        "source": source,
        "findings": len(findings),
        "imported": len(imported),
        "dry_run": dry_run,
        "entries": imported[:20]  # 最多显示 20 条
    }


def main():
    parser = argparse.ArgumentParser(description="从记忆导入知识")
    parser.add_argument("--file", default=str(MEMORY_FILE))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    result = import_from_file(args.file, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
