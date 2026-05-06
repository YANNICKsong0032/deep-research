# 🧠 Self-Learning Skill

> 一个具备**自主学习、知识管理、间隔复习**能力的 AI Agent Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-orange.svg)](#依赖)

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| 🔍 **三种学习模式** | 快速扫描(5-15min) / 标准学习(30-60min) / 深度研究(60-120min) |
| 🌐 **多源搜索** | 交叉验证多个来源，可信度评分 1-5 分 |
| 📝 **学习报告** | 自动生成结构化报告，用户审核后入库 |
| 📂 **分类知识库** | 12 个分类目录，JSON 索引，标签系统 |
| 🔄 **间隔复习** | 艾宾浩斯遗忘曲线：1→3→7→14→30→90 天 |
| 💾 **中断恢复** | 进度自动保存，支持暂停后继续学习 |
| 🔗 **知识关联** | 前置知识、互补知识、扩展知识三种关系 |
| 📊 **学习分析** | 统计面板：知识点数、掌握率、学习时长 |
| 🎯 **URL 直接学习** | 给一个链接就能读取 + 提取知识点 |
| ✅ **代码验证** | 自动验证代码示例能否运行 |
| 🚀 **统一入口** | 一个 `learn.py` 搞定所有操作 |

---

## 🚀 快速开始

### 1. 安装

```bash
git clone https://github.com/YANNICKsong0032/self-learning-skill.git
cd self-learning-skill
```

### 2. 初始化知识库

```bash
python3 scripts/knowledge.py init
```

### 3. 开始学习

```bash
# 快速了解（~10 次请求，~15 分钟）
python3 learn.py quick "React Hooks"

# 标准学习（~25 次请求，~45 分钟）
python3 learn.py study "Python Async"

# 深度研究（~40 次请求，~90 分钟）
python3 learn.py deep "RAG 检索增强生成"

# 从 URL 学习
python3 learn.py url "https://example.com/article"

# 验证已有知识
python3 learn.py verify "React Hooks"
```

---

## 📖 使用方法

### 学习命令

| 命令 | 用途 | 请求预算 |
|------|------|---------|
| `python3 learn.py quick "X"` | 快速了解（3 题） | ~10 次 |
| `python3 learn.py study "X"` | 标准学习（8 题） | ~25 次 |
| `python3 learn.py deep "X"` | 深度研究（12 题） | ~40 次 |
| `python3 learn.py url "https://..."` | 从 URL 学习 | ~3 次 |
| `python3 learn.py verify "X"` | 验证已有知识 | ~5 次 |

### 知识管理

| 命令 | 用途 |
|------|------|
| `python3 learn.py search "X"` | 搜索知识库 |
| `python3 learn.py stats` | 学习统计 |
| `python3 learn.py review-due` | 今日待复习 |
| `python3 learn.py expire` | 过期检查 |
| `python3 learn.py import-memory` | 导入已有记忆 |

### 单独脚本

```bash
# 知识库管理
python3 scripts/knowledge.py add --topic "X" --category "ai" --tags "tag1,tag2" --confidence 4.5 --sources 3
python3 scripts/knowledge.py search --query "X"
python3 scripts/knowledge.py stats

# 间隔复习
python3 scripts/review.py schedule --topic "X" --category "ai"
python3 scripts/review.py due
python3 scripts/review.py done --topic "X"

# 智能子问题生成
python3 scripts/questions.py --topic "X" --depth medium

# 学习路径
python3 scripts/learning-path.py --topic "X" --current-level beginner

# 搜索缓存
python3 scripts/search-cache.py get --url "https://..."
python3 scripts/search-cache.py set --url "https://..." --content "..."

# 学习进度
python3 scripts/progress.py init --topic "X" --sub-questions '["q1","q2"]'
python3 scripts/progress.py update --topic "X" --index 1 --status "done" --confidence 4.5
python3 scripts/progress.py status --topic "X"
```

---

## 📁 项目结构

```
self-learning-skill/
├── SKILL.md                      ← 主文件（精简版，66行）
├── learn.py                      ← 统一入口（166行）
├── scripts/
│   ├── knowledge.py              ← 知识库管理（索引/搜索/统计/过期/关联）
│   ├── progress.py               ← 学习进度追踪（中断恢复）
│   ├── credibility.py            ← 来源可信度评估（URL+内容评分）
│   ├── report.py                 ← 学习报告生成
│   ├── questions.py              ← 智能子问题生成（3种深度）
│   ├── review.py                 ← 间隔复习调度（艾宾浩斯曲线）
│   ├── search-cache.py           ← 搜索缓存（避免重复fetch）
│   ├── learning-path.py          ← 学习路径生成（入门→进阶→精通）
│   ├── import-memory.py          ← 从MEMORY.md导入已有知识
│   ├── export_skill.py           ← 知识导出为Skill
│   └── quiz.py                   ← 学习自测题生成
├── references/
│   ├── credibility-rules.md      ← 可信度评分规则
│   └── knowledge-categories.md   ← 12级知识分类体系
└── knowledge-base/               ← 知识存储目录（自动创建）
    ├── INDEX.json                ← 全局索引
    ├── learning-history.json     ← 学习历史
    ├── review-schedule.json      ← 复习计划
    ├── .progress/                ← 学习进度（中断恢复）
    ├── .search-cache.json        ← 搜索缓存
    ├── programming/              ← 编程技术
    ├── ai/                       ← AI/ML
    ├── frontend/                 ← 前端开发
    ├── backend/                  ← 后端开发
    ├── devops/                   ← 运维部署
    ├── tools/                    ← 工具软件
    ├── design/                   ← 产品设计
    ├── business/                 ← 商业/创业
    ├── science/                  ← 科学
    ├── culture/                  ← 文化/历史
    ├── life/                     ← 生活
    └── other/                    ← 其他
```

---

## 🔄 学习流程

```
用户："去学习 React Hooks"
        ↓
┌─────────────────────────────┐
│  1. 生成子问题（3/8/12个）    │
│  2. 初始化进度追踪            │
│  3. 逐题研究：               │
│     a. 检查搜索缓存          │
│     b. web_search + web_fetch │
│     c. 可信度评估            │
│     d. 写入缓存              │
│  4. 综合验证（交叉检查矛盾）   │
│  5. 生成报告 + 简短摘要       │
│  6. 发给用户审核              │
│  7. 用户确认 → 入库           │
│  8. 安排间隔复习              │
│  9. 推荐下一步学习方向         │
└─────────────────────────────┘
```

---

## 📊 可信度评分

| 分数 | 来源类型 | 处理方式 |
|------|---------|---------|
| 5 | 官方文档、论文、权威百科 | 直接采用 |
| 4 | Stack Overflow、知名博客 | 交叉验证 |
| 3 | 一般教程、技术社区 | 多源验证 |
| 2 | 论坛帖子、个人经验 | 标记待验证 |
| 1 | 匿名内容、广告 | 自动排除 |

**计算公式**：`final = URL评分 × 0.6 + 内容评分 × 0.4`

---

## 📅 间隔复习

知识入库后自动安排复习计划：

```
学习当天 → +1天 → +3天 → +7天 → +14天 → +30天 → +90天
```

查看今日待复习：
```bash
python3 learn.py review-due
```

---

## 📂 知识分类

| 分类 | 目录 | 说明 |
|------|------|------|
| 编程技术 | `programming/` | 语言、框架、库、设计模式 |
| AI/机器学习 | `ai/` | LLM、prompt、模型、训练、部署 |
| 前端开发 | `frontend/` | UI/UX、CSS、动画、浏览器 |
| 后端开发 | `backend/` | API、数据库、缓存、消息队列 |
| 运维部署 | `devops/` | Docker、CI/CD、监控、云服务 |
| 工具软件 | `tools/` | 编辑器、CLI、效率工具 |
| 产品设计 | `design/` | 设计系统、交互、用户研究 |
| 商业/创业 | `business/` | 商业模式、增长、融资、运营 |
| 科学 | `science/` | 数学、物理、计算机科学 |
| 文化/历史 | `culture/` | 历史、哲学、社会、语言学 |
| 生活 | `life/` | 健康、理财、学习方法 |
| 其他 | `other/` | 无法归类的知识 |

---

## ⚡ 效率优化

### Token 优化

| 优化 | 节省 |
|------|------|
| SKILL.md 精简（66行 vs 930行） | -93% |
| 详细指令按需加载 | -80% |
| 统一入口减少 exec 调用 | -66% |

### 请求优化

| 优化 | 节省 |
|------|------|
| 每题只 fetch 1 个结果 | -66% |
| 搜索缓存命中跳过 | -100% |
| 批量 exec 用 `&&` 合并 | -50% |
| 增量学习跳过已知 | -30% |

### 请求预算

| 模式 | 请求上限 | 子问题 |
|------|---------|--------|
| 快速 | ~10 次 | 3 个 |
| 标准 | ~25 次 | 5-8 个 |
| 深度 | ~40 次 | 8-12 个 |
| URL | ~3 次 | 0 个 |
| 验证 | ~5 次 | 0 个 |

---

## 🤝 贡献

欢迎 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送并开 PR

## 📄 License

[MIT](LICENSE) © 2026
