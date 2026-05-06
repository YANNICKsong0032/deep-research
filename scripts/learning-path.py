#!/usr/bin/env python3
"""
学习路径生成器 — 为复杂主题生成从浅到深的学习路线
用法: python3 learning-path.py --topic "xxx" --current-level beginner
"""

import json
import sys
import argparse
from typing import Dict, List

# 学习阶段模板
STAGES = {
    "beginner": {
        "name": "入门",
        "duration": "1-2 周",
        "focus": ["核心概念", "基本用法", "Hello World"],
        "resources": ["官方教程", "入门视频", "交互式教程"],
        "milestones": ["能独立写一个简单项目"]
    },
    "intermediate": {
        "name": "进阶",
        "duration": "2-4 周",
        "focus": ["设计模式", "最佳实践", "常见陷阱", "性能优化"],
        "resources": ["官方文档进阶部分", "技术博客", "GitHub 示例项目"],
        "milestones": ["能解决复杂问题", "能做 code review"]
    },
    "advanced": {
        "name": "精通",
        "duration": "1-3 月",
        "focus": ["源码阅读", "架构设计", "社区贡献", "跨领域应用"],
        "resources": ["源码", "论文", "会议演讲", "开源项目"],
        "milestones": ["能设计架构", "能给社区贡献代码"]
    }
}

# 主题 → 前置知识映射
PREREQUISITES = {
    "react": ["javascript", "html", "css"],
    "vue": ["javascript", "html", "css"],
    "typescript": ["javascript"],
    "next.js": ["react", "typescript"],
    "node.js": ["javascript"],
    "express": ["node.js"],
    "fastapi": ["python"],
    "django": ["python"],
    "docker": ["linux basics"],
    "kubernetes": ["docker", "networking basics"],
    "llm": ["python", "machine learning basics"],
    "rag": ["llm", "vector databases"],
    "agent": ["llm", "prompt engineering"],
    "rust": ["c/c++ basics (helpful)"],
    "webassembly": ["rust or c++", "javascript"],
    "graphql": ["rest api", "sql"],
    "tailwind": ["html", "css"],
    "zustand": ["react"],
    "redux": ["react"],
    "prisma": ["sql", "node.js"],
    "drizzle": ["sql", "typescript"],
}


def generate_path(topic: str, current_level: str = "beginner") -> Dict:
    """生成学习路径"""
    topic_lower = topic.lower()
    
    # 确定前置知识
    prereqs = PREREQUISITES.get(topic_lower, [])
    
    # 确定起始阶段
    levels = ["beginner", "intermediate", "advanced"]
    start_idx = levels.index(current_level) if current_level in levels else 0
    
    # 生成路径
    path = []
    for i, level in enumerate(levels[start_idx:], 1):
        stage = STAGES[level]
        
        # 根据主题定制焦点
        focus = list(stage["focus"])
        if "react" in topic_lower or "vue" in topic_lower:
            focus.extend(["组件化", "状态管理", "路由", "SSR"])
        elif "python" in topic_lower:
            focus.extend(["装饰器", "生成器", "异步编程", "类型提示"])
        elif "llm" in topic_lower or "ai" in topic_lower:
            focus.extend(["Prompt Engineering", "Fine-tuning", "RAG", "Agent"])
        elif "docker" in topic_lower or "k8s" in topic_lower:
            focus.extend(["容器编排", "网络", "存储", "CI/CD"])
        
        path.append({
            "stage": i,
            "level": level,
            "name": stage["name"],
            "duration": stage["duration"],
            "focus": focus[:6],  # 最多 6 个焦点
            "resources": stage["resources"],
            "milestones": stage["milestones"],
            "sub_questions": generate_stage_questions(topic, level)
        })
    
    result = {
        "topic": topic,
        "current_level": current_level,
        "prerequisites": prereqs,
        "total_stages": len(path),
        "estimated_total_duration": f"{sum(len(p['focus']) for p in path) * 2}-{sum(len(p['focus']) for p in path) * 4} 周",
        "path": path
    }
    
    return result


def generate_stage_questions(topic: str, level: str) -> List[str]:
    """为每个阶段生成子问题"""
    if level == "beginner":
        return [
            f"{topic} 是什么？解决了什么问题？",
            f"{topic} 的核心概念有哪些？",
            f"{topic} 的基本使用方法？",
            f"{topic} 的 Hello World 示例？",
        ]
    elif level == "intermediate":
        return [
            f"{topic} 的设计模式和最佳实践？",
            f"{topic} 的常见陷阱有哪些？",
            f"{topic} 的性能优化技巧？",
            f"{topic} 与类似技术的对比？",
        ]
    else:
        return [
            f"{topic} 的架构设计原理？",
            f"{topic} 的源码结构是怎样的？",
            f"{topic} 的社区生态和贡献方式？",
            f"{topic} 的未来发展趋势？",
        ]


def main():
    parser = argparse.ArgumentParser(description="学习路径生成器")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--current-level", choices=["beginner", "intermediate", "advanced"], default="beginner")
    args = parser.parse_args()
    
    result = generate_path(args.topic, args.current_level)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
