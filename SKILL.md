---
name: self-learning
description: 自主学习系统。触发词：去学习、研究一下、深入了解、learn、research、快速了解、验证一下。联网研究→辨别真伪→生成报告→用户审核→入库分类。
---

# 自主学习系统

## 唯一入口

```bash
python3 learn.py <command> [topic]
```

| 命令 | 用途 | 请求预算 |
|------|------|---------|
| `quick "X"` | 快速了解（3 题） | ~10 次 |
| `study "X"` | 标准学习（8 题） | ~25 次 |
| `deep "X"` | 深度研究（12 题） | ~40 次 |
| `url "https://..."` | 从 URL 学习 | ~3 次 |
| `verify "X"` | 验证已有知识 | ~5 次 |
| `search "X"` | 搜索知识库 | 0 次 |
| `stats` | 学习统计 | 0 次 |
| `review-due` | 今日待复习 | 0 次 |
| `expire` | 过期检查 | 0 次 |
| `import-memory` | 导入记忆 | 0 次 |

## 执行流程

```
1. learn.py study "X" → 输出子问题 + 已有知识 + 预算
2. 逐题：web_search 1次 + web_fetch top 1
3. 每 3 题：learn.py 更新进度
4. learn.py 生成报告
5. 发摘要给用户
6. 等审核 → learn.py 入库
```

## 省请求规则

- 每题只 fetch 1 个结果
- 每 3 题更新一次进度
- 缓存命中跳过搜索
- 批量 exec 用 `&&` 合并
- 报告存文件，聊天只发摘要
- 快速模式 ≤10 次，标准 ≤25 次，深度 ≤40 次

## 省 Token 规则

- 本文件只加载快速参考（不读 references/）
- 详细指令按需加载
- 脚本输出精简 JSON
- 知识入库后不重复加载

## 入库流程

用户确认后：
```bash
# 批量入库（一次 exec）
python3 scripts/knowledge.py add --topic "X" --category "ai" --tags "tag1" --confidence 4.5 --sources 3 && \
python3 scripts/review.py schedule --topic "X" --category "ai"
```

## 心跳任务

- 每次：`learn.py review-due` + `learn.py stats`
- 每周：`learn.py expire`
