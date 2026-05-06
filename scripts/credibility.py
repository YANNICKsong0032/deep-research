#!/usr/bin/env python3
"""
来源可信度评估器
用法: python3 credibility.py --url "https://example.com" --content "..."
输出: JSON 格式的可信度评分和理由
"""

import re
import sys
import json
import argparse
from urllib.parse import urlparse
from typing import Dict, Tuple


# 高可信度域名
HIGH_TRUST_DOMAINS = {
    # 官方文档
    "docs.python.org", "developer.mozilla.org", "reactjs.org", "react.dev",
    "nodejs.org", "typescriptlang.org", "rust-lang.org", "go.dev",
    "kubernetes.io", "docker.com", "docs.github.com",
    # 权威百科/知识库
    "en.wikipedia.org", "zh.wikipedia.org", "stackoverflow.com",
    "arxiv.org", "papers.nips.cc", "openreview.net",
    # 知名技术平台
    "github.com", "gitlab.com", "npmjs.com", "pypi.org",
    "medium.com", "dev.to", "hashnode.com", "zhihu.com",
    # AI/技术公司官方
    "openai.com", "anthropic.com", "huggingface.co", "pytorch.org",
    "tensorflow.org", "arxiv.org", "deepmind.com",
}

# 低可信度信号
LOW_TRUST_SIGNALS = [
    r"点击购买", r"限时优惠", r"免费领取", r"广告",
    r"buy now", r"limited offer", r"sponsored", r"advertisement",
    r"affiliate", r"referral",
]


def evaluate_url(url: str) -> Tuple[float, str]:
    """评估 URL 可信度"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().lstrip("www.")
    except Exception:
        return 1.0, "无法解析 URL"
    
    # 检查高可信度域名
    for trusted in HIGH_TRUST_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return 5.0, f"权威来源: {trusted}"
    
    # 检查域名特征
    if domain.endswith(".edu") or domain.endswith(".edu.cn"):
        return 4.5, "教育机构域名"
    if domain.endswith(".gov") or domain.endswith(".gov.cn"):
        return 4.5, "政府机构域名"
    if domain.endswith(".org"):
        return 3.5, "组织机构域名"
    
    # 知名博客平台
    blog_platforms = ["github.io", "gitlab.io", "netlify.app", "vercel.app", "substack.com"]
    for platform in blog_platforms:
        if domain.endswith(platform):
            return 3.5, f"个人博客平台: {platform}"
    
    # 中文技术社区
    cn_tech = ["juejin.cn", "csdn.net", "cnblogs.com", "jianshu.com", "segmentfault.com"]
    for site in cn_tech:
        if domain.endswith(site):
            return 3.0, f"中文技术社区: {site}"
    
    # 默认
    return 2.5, "一般网站，需人工验证"


def evaluate_content(content: str) -> Tuple[float, str]:
    """评估内容质量"""
    if not content:
        return 1.0, "内容为空"
    
    score = 3.0
    reasons = []
    
    # 长度检查
    if len(content) < 100:
        score -= 1.0
        reasons.append("内容过短")
    elif len(content) > 2000:
        score += 0.3
        reasons.append("内容充实")
    
    # 检查低可信度信号
    for pattern in LOW_TRUST_SIGNALS:
        if re.search(pattern, content, re.IGNORECASE):
            score -= 0.5
            reasons.append(f"发现广告信号: {pattern}")
    
    # 检查代码块（技术内容加分）
    if "```" in content or "    " in content:
        score += 0.3
        reasons.append("包含代码示例")
    
    # 检查引用/链接
    links = re.findall(r'https?://\S+', content)
    if len(links) > 2:
        score += 0.2
        reasons.append(f"包含 {len(links)} 个引用链接")
    
    # 检查日期信息
    dates = re.findall(r'20[2-3]\d[-/]\d{2}', content)
    if dates:
        score += 0.2
        reasons.append("包含日期信息")
    
    # 检查第一人称（可能是个人观点，可信度降低）
    first_person = len(re.findall(r'我觉得|我认为|我个人|IMO|IMHO|personally', content, re.IGNORECASE))
    if first_person > 3:
        score -= 0.3
        reasons.append("较多个人观点")
    
    score = max(1.0, min(5.0, score))
    return score, "; ".join(reasons) if reasons else "内容质量一般"


def evaluate(url: str, content: str = "") -> Dict:
    """综合评估"""
    url_score, url_reason = evaluate_url(url)
    content_score, content_reason = evaluate_content(content)
    
    # URL 权重 60%，内容权重 40%
    final_score = url_score * 0.6 + content_score * 0.4
    final_score = round(final_score, 1)
    
    # 等级
    if final_score >= 4.5:
        level = "高"
        action = "可直接采用"
    elif final_score >= 3.5:
        level = "中高"
        action = "建议交叉验证"
    elif final_score >= 2.5:
        level = "中"
        action = "需要多源验证"
    else:
        level = "低"
        action = "标记为待验证"
    
    return {
        "score": final_score,
        "level": level,
        "action": action,
        "url": {"score": url_score, "reason": url_reason},
        "content": {"score": content_score, "reason": content_reason}
    }


def main():
    parser = argparse.ArgumentParser(description="来源可信度评估")
    parser.add_argument("--url", required=True, help="来源 URL")
    parser.add_argument("--content", default="", help="内容文本")
    args = parser.parse_args()
    
    result = evaluate(args.url, args.content)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
