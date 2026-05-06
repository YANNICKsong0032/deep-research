# 可信度评估规则

## URL 评分（满分 5 分）

### 5 分 — 官方/权威来源
- 官方文档：docs.python.org, developer.mozilla.org, react.dev, kubernetes.io
- 学术论文：arxiv.org, openreview.net, papers.nips.cc
- 官方仓库：github.com/{org}/{repo}（star > 1000）
- 权威百科：wikipedia.org

### 4 分 — 知名社区/平台
- Stack Overflow（高票回答，vote > 10）
- 知名技术博客：medium.com, dev.to, hashnode.com
- 中文权威：zhihu.com（专栏，关注 > 1000）
- 行业报告：gartner.com, statista.com

### 3 分 — 一般技术网站
- 中文技术社区：juejin.cn, cnblogs.com, csdn.net
- 个人技术博客（github.io, gitlab.io）
- 教程网站：w3schools.com, runoob.com
- npmjs.com, pypi.org 的包文档

### 2 分 — 社区/论坛
- Reddit 帖子
- V2EX, SegmentFault 问答
- 个人论坛

### 1 分 — 不可靠来源
- 匿名内容
- 明显广告/推广
- 无法验证的断言

## 内容评分（满分 5 分）

### 加分项
- 包含代码示例：+0.5
- 包含数据/图表：+0.5
- 有明确日期（2024 年以后）：+0.3
- 有引用链接（> 3 个）：+0.3
- 内容充实（> 2000 字）：+0.3
- 有版本号/兼容性说明：+0.2（技术类）

### 扣分项
- 内容过短（< 200 字）：-1.0
- 发现广告信号：-0.5（每个）
- 较多个人观点（> 3 处"我觉得/我认为"）：-0.3
- 过时内容（日期 > 2 年前的技术文档）：-1.0
- 无来源断言：-0.5

## 最终计算

```
final_score = url_score × 0.6 + content_score × 0.4
```

| 分数区间 | 等级 | 处理方式 |
|---------|------|---------|
| 4.5 - 5.0 | 高 | 直接采用 |
| 3.5 - 4.4 | 中高 | 交叉验证后采用 |
| 2.5 - 3.4 | 中 | 多源验证 |
| 1.5 - 2.4 | 低 | 标记为待验证 |
| 1.0 - 1.4 | 极低 | 自动排除 |
