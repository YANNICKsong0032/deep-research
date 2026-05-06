#!/usr/bin/env python3
"""
智能子问题生成器
用法: python3 questions.py --topic "xxx" --depth medium
输出: JSON 格式的子问题列表
"""

import json
import sys
import argparse
from typing import List


# 问题模板库
TEMPLATES = {
    "concept": [
        "{topic} 的核心概念是什么？",
        "{topic} 解决了什么问题？",
        "{topic} 的基本原理是什么？",
        "{topic} 的关键术语有哪些？",
    ],
    "how": [
        "{topic} 的基本用法是什么？",
        "{topic} 的常见使用场景有哪些？",
        "{topic} 的最佳实践是什么？",
        "{topic} 的典型工作流程是什么？",
    ],
    "compare": [
        "{topic} 和 {alternative} 有什么区别？",
        "{topic} 相比其他方案的优势是什么？",
        "什么时候应该用 {topic}，什么时候不该用？",
    ],
    "advanced": [
        "{topic} 的高级特性有哪些？",
        "{topic} 的性能优化技巧？",
        "{topic} 的常见陷阱和避坑经验？",
        "{topic} 在生产环境中的使用经验？",
    ],
    "ecosystem": [
        "{topic} 的主流工具/库有哪些？",
        "{topic} 的社区资源有哪些？",
        "{topic} 的学习路线是什么？",
    ],
    "practice": [
        "{topic} 的实际项目案例？",
        "{topic} 的代码示例？",
        "{topic} 的调试技巧？",
    ]
}

# 主题 → 替代方案映射
ALTERNATIVES = {
    "react": "Vue, Angular, Svelte",
    "vue": "React, Angular, Svelte",
    "python": "JavaScript, Go, Rust",
    "typescript": "JavaScript, Flow",
    "docker": "Podman, LXC",
    "kubernetes": "Docker Swarm, Nomad",
    "zustand": "Redux, Jotai, Recoil",
    "tailwind": "Bootstrap, Styled Components",
    "vite": "Webpack, Parcel, Turbopack",
    "next.js": "Nuxt, Remix, Astro",
    "express": "Fastify, Koa, Hono",
    "fastapi": "Flask, Django REST",
    "rust": "C++, Go, Zig",
    "go": "Rust, Node.js",
    "llm": "传统 NLP, 规则引擎",
    "rag": "Fine-tuning, Prompt Engineering",
    "agent": "Chain-of-Thought, Few-shot",
}


def get_alternatives(topic: str) -> str:
    """获取主题的替代方案"""
    topic_lower = topic.lower()
    for key, alts in ALTERNATIVES.items():
        if key in topic_lower:
            return alts
    return "其他类似技术"


def generate_questions(topic: str, depth: str = "medium") -> List[str]:
    """生成子问题"""
    alternatives = get_alternatives(topic)
    
    if depth == "shallow":
        # 5 个问题：概念 + 用法 + 场景 + 示例 + 术语
        questions = [
            TEMPLATES["concept"][0].format(topic=topic),
            TEMPLATES["concept"][1].format(topic=topic),
            TEMPLATES["how"][0].format(topic=topic),
            TEMPLATES["how"][1].format(topic=topic),
            TEMPLATES["practice"][2].format(topic=topic),
        ]
    elif depth == "medium":
        # 8 个问题：概念×2 + 用法×2 + 对比 + 最佳实践 + 陷阱 + 工具
        questions = [
            TEMPLATES["concept"][0].format(topic=topic),
            TEMPLATES["concept"][1].format(topic=topic),
            TEMPLATES["how"][0].format(topic=topic),
            TEMPLATES["how"][2].format(topic=topic),
            TEMPLATES["compare"][0].format(topic=topic, alternative=alternatives),
            TEMPLATES["how"][3].format(topic=topic),
            TEMPLATES["advanced"][2].format(topic=topic),
            TEMPLATES["ecosystem"][0].format(topic=topic),
        ]
    else:  # deep
        # 12 个问题：全面覆盖
        questions = [
            TEMPLATES["concept"][0].format(topic=topic),
            TEMPLATES["concept"][1].format(topic=topic),
            TEMPLATES["concept"][2].format(topic=topic),
            TEMPLATES["how"][0].format(topic=topic),
            TEMPLATES["how"][1].format(topic=topic),
            TEMPLATES["how"][2].format(topic=topic),
            TEMPLATES["compare"][0].format(topic=topic, alternative=alternatives),
            TEMPLATES["compare"][1].format(topic=topic),
            TEMPLATES["advanced"][0].format(topic=topic),
            TEMPLATES["advanced"][2].format(topic=topic),
            TEMPLATES["practice"][0].format(topic=topic),
            TEMPLATES["ecosystem"][2].format(topic=topic),
        ]
    
    return questions


def main():
    parser = argparse.ArgumentParser(description="智能子问题生成器")
    parser.add_argument("--topic", required=True, help="学习主题")
    parser.add_argument("--depth", choices=["shallow", "medium", "deep"], default="medium", help="深度")
    args = parser.parse_args()
    
    questions = generate_questions(args.topic, args.depth)
    
    result = {
        "topic": args.topic,
        "depth": args.depth,
        "count": len(questions),
        "questions": questions,
        "estimated_minutes": {"shallow": 15, "medium": 45, "deep": 90}[args.depth]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
