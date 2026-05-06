# 知识分类体系

学习到的知识按以下分类入库。每个知识点归属一个主分类。

## 一级分类

| 分类 | 目录 | 说明 | 标签 |
|------|------|------|------|
| **编程技术** | `programming/` | 语言、框架、库、设计模式 | python, js, ts, react, go, rust, sql, git |
| **AI/机器学习** | `ai/` | LLM、prompt、模型、训练、部署 | llm, prompt, fine-tune, rag, agent, embedding |
| **前端开发** | `frontend/` | UI/UX、CSS、动画、浏览器 | css, tailwind, animation, a11y, seo |
| **后端开发** | `backend/` | API、数据库、缓存、消息队列 | api, database, redis, kafka, graphql |
| **运维部署** | `devops/` | Docker、CI/CD、监控、云服务 | docker, k8s, github-actions, aws, linux |
| **工具软件** | `tools/` | 编辑器、CLI、效率工具 | vscode, vim, cli, tmux, neovim |
| **产品设计** | `design/` | 设计系统、交互、用户研究 | figma, design-system, ux, prototyping |
| **商业/创业** | `business/` | 商业模式、增长、融资、运营 | startup, growth, monetization, marketing |
| **科学** | `science/` | 数学、物理、计算机科学 | math, algorithm, data-structure, theory |
| **文化/历史** | `culture/` | 历史、哲学、社会、语言学 | history, philosophy, linguistics, society |
| **生活** | `life/` | 健康、理财、学习方法 | health, finance, learning, productivity |
| **其他** | `other/` | 无法归类的知识 | misc |

## 分类规则

1. **优先选择最具体的分类**：React hooks → `frontend/`，不是 `programming/`
2. **跨分类时选主要用途**：Python 写 AI → `ai/`，Python 写 Web → `backend/`
3. **不确定时放 `other/`**，后续整理时再归类
4. **每个知识点最多 3 个标签**，用于细粒度检索

## 文件命名

- 格式：`{主题}.md`，用英文小写 + 连字符
- 例：`python-async.md`、`react-hooks.md`、`llm-fine-tuning.md`
- 中文主题用拼音或英文翻译：`提示词工程.md` → `prompt-engineering.md`
