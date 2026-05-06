#!/usr/bin/env python3
"""
学习报告生成器
用法: python3 report.py --topic "xxx" --report-file reports/xxx-report.md
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def generate_checklist(topic: str, sub_questions: List[str]) -> str:
    """生成学习清单"""
    lines = [
        f"# 学习清单：{topic}",
        f"",
        f"**创建时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**子问题数量**：{len(sub_questions)}",
        f"",
        f"## 子问题",
        f"",
    ]
    for i, q in enumerate(sub_questions, 1):
        lines.append(f"- [ ] {i}. {q}")
    
    lines.extend([
        f"",
        f"## 进度",
        f"",
        f"| # | 子问题 | 状态 | 来源数 | 可信度 |",
        f"|---|--------|------|--------|--------|",
    ])
    for i, q in enumerate(sub_questions, 1):
        lines.append(f"| {i} | {q} | ⏳ 待研究 | - | - |")
    
    return "\n".join(lines)


def generate_report(topic: str, sub_questions: List[str], 
                   findings: List[Dict], stats: Dict,
                   skill_recommendations: List[str] = None) -> str:
    """生成完整学习报告"""
    
    now = datetime.now()
    
    # 统计
    total = len(findings)
    confirmed = sum(1 for f in findings if f.get("confidence", 0) >= 4.0)
    uncertain = sum(1 for f in findings if 2.5 <= f.get("confidence", 0) < 4.0)
    unverified = sum(1 for f in findings if f.get("confidence", 0) < 2.5)
    
    lines = [
        f"# 学习报告：{topic}",
        f"",
        f"**学习时间**：{now.strftime('%Y-%m-%d %H:%M')}",
        f"**耗时**：{stats.get('duration_minutes', '?')} 分钟",
        f"**子问题完成**：{stats.get('completed', 0)}/{len(sub_questions)}",
        f"",
        f"---",
        f"",
        f"## 📋 学习清单",
        f"",
    ]
    
    # 清单
    for i, q in enumerate(sub_questions, 1):
        # 查找对应的发现
        finding = next((f for f in findings if f.get("question_index") == i), None)
        if finding:
            status = "✅" if finding.get("confidence", 0) >= 4.0 else "⚠️" if finding.get("confidence", 0) >= 2.5 else "❓"
            lines.append(f"- [x] {i}. {q} {status}")
        else:
            lines.append(f"- [ ] {i}. {q} ❌ 未找到可靠来源")
    
    lines.extend([
        f"",
        f"---",
        f"",
        f"## 📝 核心知识点",
        f"",
    ])
    
    # 知识点详情
    for i, finding in enumerate(findings, 1):
        conf = finding.get("confidence", 0)
        if conf >= 4.0:
            status = "✅ 确定"
            stars = "⭐" * int(conf)
        elif conf >= 2.5:
            status = "⚠️ 待验证"
            stars = "⭐" * int(conf)
        else:
            status = "❓ 低可信度"
            stars = "⭐" * max(1, int(conf))
        
        sources = finding.get("sources", [])
        source_links = "、".join([f"[{s.get('title', '来源')}]({s.get('url', '')})" for s in sources[:3]])
        
        lines.extend([
            f"### {i}. {finding.get('title', f'知识点 {i}')}",
            f"",
            f"- **内容**：{finding.get('content', '...')}",
            f"- **来源**：{source_links or '无'}",
            f"- **可信度**：{stars} ({conf}/5)",
            f"- **状态**：{status}",
            f"",
        ])
    
    # 遗留问题
    unverified_questions = [q for i, q in enumerate(sub_questions, 1) 
                           if not any(f.get("question_index") == i for f in findings)]
    if unverified_questions:
        lines.extend([
            f"---",
            f"",
            f"## ❓ 遗留问题",
            f"",
        ])
        for q in unverified_questions:
            lines.append(f"- {q}")
        lines.append("")
    
    # 推荐 skills
    if skill_recommendations:
        lines.extend([
            f"---",
            f"",
            f"## 🔧 推荐安装的 Skills",
            f"",
            f"根据本次学习，建议安装以下 skills：",
            f"",
        ])
        for rec in skill_recommendations:
            lines.append(f"- {rec}")
        lines.append("")
    
    # 统计
    lines.extend([
        f"---",
        f"",
        f"## 📊 学习统计",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 搜索次数 | {stats.get('searches', 0)} |",
        f"| 阅读页面 | {stats.get('pages_read', 0)} |",
        f"| 知识点总数 | {total} |",
        f"| ✅ 确定 | {confirmed} |",
        f"| ⚠️ 待验证 | {uncertain} |",
        f"| ❓ 低可信度 | {unverified} |",
        f"",
        f"---",
        f"",
        f"*请审核以上内容。确认无误后回复「确认」，我会将知识入库。*",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="学习报告生成器")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--sub-questions", required=True, help="JSON 格式的子问题列表")
    parser.add_argument("--findings", default="[]", help="JSON 格式的发现列表")
    parser.add_argument("--stats", default="{}", help="JSON 格式的统计信息")
    parser.add_argument("--output", help="输出文件路径")
    args = parser.parse_args()
    
    sub_questions = json.loads(args.sub_questions)
    findings = json.loads(args.findings)
    stats = json.loads(args.stats)
    
    report = generate_report(args.topic, sub_questions, findings, stats)
    
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(json.dumps({"status": "saved", "path": args.output}))
    else:
        print(report)


if __name__ == "__main__":
    main()
