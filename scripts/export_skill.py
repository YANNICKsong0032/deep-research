#!/usr/bin/env python3
"""
知识导出为 Skill
用法: python3 export_skill.py --topic "xxx" --category "programming"
"""

import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

KB_ROOT = Path(__file__).parent.parent.parent.parent / "knowledge-base"
SKILLS_ROOT = Path(__file__).parent.parent.parent.parent / "skills"


def export_skill(topic: str, category: str):
    """将知识导出为 skill"""
    # 查找知识文件
    slug = topic.lower().replace(" ", "-")
    kb_file = KB_ROOT / category / f"{slug}.md"
    
    if not kb_file.exists():
        print(json.dumps({"error": f"知识文件不存在: {kb_file}"}))
        return
    
    # 创建 skill 目录
    skill_dir = SKILLS_ROOT / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    
    # 读取知识内容
    with open(kb_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 生成 SKILL.md
    skill_md = f"""---
name: {slug}
description: {topic} 相关知识和最佳实践。当用户问到 {topic} 相关问题时使用。
---

# {topic}

{content}

---

## 使用说明

这个 skill 包含了关于 {topic} 的结构化知识。

### 何时使用

- 用户问到 {topic} 相关问题
- 需要 {topic} 的代码示例
- 需要 {topic} 的最佳实践

### 知识来源

- 学习时间：{datetime.now().strftime('%Y-%m-%d')}
- 分类：{category}
- 自动生成于 knowledge-base
"""
    
    # 写入 SKILL.md
    with open(skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_md)
    
    # 复制原始知识文件到 references
    shutil.copy2(kb_file, skill_dir / "references" / f"{slug}.md")
    
    result = {
        "status": "exported",
        "topic": topic,
        "skill_dir": str(skill_dir),
        "files": [
            str(skill_dir / "SKILL.md"),
            str(skill_dir / "references" / f"{slug}.md")
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="知识导出为 Skill")
    parser.add_argument("--topic", required=True, help="知识主题")
    parser.add_argument("--category", required=True, help="知识分类")
    args = parser.parse_args()
    
    export_skill(args.topic, args.category)


if __name__ == "__main__":
    main()
