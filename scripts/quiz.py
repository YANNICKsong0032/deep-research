#!/usr/bin/env python3
"""
学习自测题生成器
用法: python3 quiz.py --topic "xxx" --knowledge-file path/to/knowledge.md
输出: JSON 格式的自测题
"""

import json
import sys
import argparse
import re
import random
from typing import List, Dict


def extract_key_concepts(content: str) -> List[str]:
    """从知识内容中提取关键概念"""
    concepts = []
    
    # 提取标题
    for match in re.finditer(r'^#{1,3}\s+(.+)$', content, re.MULTILINE):
        title = match.group(1).strip()
        if len(title) > 2 and len(title) < 50:
            concepts.append(title)
    
    # 提取表格中的术语
    for match in re.finditer(r'\|\s*([^|]+?)\s*\|', content):
        term = match.group(1).strip()
        if len(term) > 2 and len(term) < 30 and not term.startswith('-'):
            concepts.append(term)
    
    # 提取代码块前的说明
    for match in re.finditer(r'```[\s\S]*?```', content):
        pass  # 跳过代码块
    
    # 提取加粗文本
    for match in re.finditer(r'\*\*(.+?)\*\*', content):
        concept = match.group(1).strip()
        if len(concept) > 2 and len(concept) < 30:
            concepts.append(concept)
    
    # 去重
    seen = set()
    unique = []
    for c in concepts:
        c_lower = c.lower()
        if c_lower not in seen:
            seen.add(c_lower)
            unique.append(c)
    
    return unique[:20]  # 最多 20 个


def generate_fill_blank(concept: str, context: str = "") -> Dict:
    """生成填空题"""
    return {
        "type": "fill_blank",
        "question": f"______ 是 {concept} 的核心概念之一。",
        "answer": concept,
        "hint": f"这是一个与 {concept} 相关的术语"
    }


def generate_true_false(concept: str, context: str = "") -> Dict:
    """生成判断题"""
    return {
        "type": "true_false",
        "question": f"以下说法是否正确：{concept} 是一个重要的概念。",
        "answer": True,
        "explanation": f"{concept} 确实是该领域的重要概念"
    }


def generate_short_answer(concept: str, context: str = "") -> Dict:
    """生成简答题"""
    return {
        "type": "short_answer",
        "question": f"请简要说明 {concept} 的含义和用途。",
        "key_points": [concept],
        "sample_answer": f"（参考答案需根据具体知识内容生成）"
    }


def generate_quiz(topic: str, content: str = "", count: int = 5) -> Dict:
    """生成自测题"""
    concepts = extract_key_concepts(content) if content else [topic]
    
    if not concepts:
        concepts = [topic]
    
    questions = []
    used = set()
    
    # 尝试生成不同类型的题目
    question_types = [
        ("fill_blank", generate_fill_blank),
        ("short_answer", generate_short_answer),
    ]
    
    for i in range(count):
        # 随机选择概念
        available = [c for c in concepts if c not in used]
        if not available:
            available = concepts
            used.clear()
        
        concept = random.choice(available)
        used.add(concept)
        
        # 随机选择题型
        qtype, generator = random.choice(question_types)
        question = generator(concept, content)
        question["id"] = i + 1
        question["concept"] = concept
        questions.append(question)
    
    result = {
        "topic": topic,
        "total_questions": len(questions),
        "questions": questions,
        "instructions": "请回答以下问题，检验学习成果。回答后我会给出参考答案和解析。"
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description="学习自测题生成器")
    parser.add_argument("--topic", required=True, help="学习主题")
    parser.add_argument("--knowledge-file", help="知识文件路径（可选）")
    parser.add_argument("--count", type=int, default=5, help="题目数量")
    args = parser.parse_args()
    
    content = ""
    if args.knowledge_file:
        try:
            with open(args.knowledge_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(json.dumps({"error": f"读取知识文件失败: {e}"}))
            return
    
    quiz = generate_quiz(args.topic, content, args.count)
    print(json.dumps(quiz, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
