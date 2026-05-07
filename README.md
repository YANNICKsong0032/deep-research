<div align="center">

# 🔍 Deep Research

**Autonomous deep research skill for AI Agents**

*Web search → Cross-validation → Report → Review → Knowledge base → Spaced repetition*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)](#-dependencies)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://github.com/openclaw/openclaw)

[Quick Start](#-quick-start) · [Features](#-features) · [Usage](#-usage) · [How It Works](#-how-it-works) · [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔬 Research Engine
- **Three learning modes** — quick scan / standard study / deep research
- **Multi-source search** — cross-validates multiple sources
- **Credibility scoring** — 1–5 rating per source
- **Code verification** — auto-validates code examples

</td>
<td width="50%">

### 🧠 Knowledge System
- **12 category directories** with JSON index & tags
- **Spaced repetition** — Ebbinghaus curve (1→3→7→14→30→90 days)
- **Knowledge linking** — prerequisite / complementary / extension
- **Resume on interrupt** — progress auto-saved

</td>
</tr>
<tr>
<td>

### 📊 Analytics
- **Learning dashboard** — knowledge count, mastery rate, study duration
- **Structured reports** — auto-generated, user-reviewed before ingestion
- **URL learning** — feed a link, extract key points

</td>
<td>

### ⚡ Developer Experience
- **Unified CLI** — one `learn.py` for everything
- **Zero dependencies** — pure Python standard library
- **Modular scripts** — use individually or as a pipeline

</td>
</tr>
</table>

---

## 🚀 Quick Start

```bash
git clone https://github.com/YANNICKsong0032/deep-research.git
cd deep-research
python3 scripts/knowledge.py init
```

```bash
# Quick scan (~15 min)
python3 learn.py quick "React Hooks"

# Standard study (~45 min)
python3 learn.py study "Python Async"

# Deep research (~90 min)
python3 learn.py deep "RAG Retrieval Augmented Generation"

# Learn from a URL
python3 learn.py url "https://example.com/article"

# Verify existing knowledge
python3 learn.py verify "React Hooks"
```

---

## 📖 Usage

### Learning Commands

| Command | Mode | Questions | Requests |
|---------|------|-----------|----------|
| `learn.py quick "X"` | 🔍 Quick scan | 3 | ~10 |
| `learn.py study "X"` | 📚 Standard study | 8 | ~25 |
| `learn.py deep "X"` | 🔬 Deep research | 12 | ~40 |
| `learn.py url "https://..."` | 🔗 URL learning | — | ~3 |
| `learn.py verify "X"` | ✅ Verification | — | ~5 |

### Knowledge Management

| Command | Purpose |
|---------|---------|
| `learn.py search "X"` | 🔎 Search the knowledge base |
| `learn.py stats` | 📊 Learning statistics |
| `learn.py review-due` | 📅 Items due for review today |
| `learn.py expire` | ⏰ Expiration check |
| `learn.py import-memory` | 📥 Import existing memories |

### Standalone Scripts

<details>
<summary><strong>Click to expand all scripts</strong></summary>

```bash
# Knowledge base management
python3 scripts/knowledge.py add --topic "X" --category "ai" --tags "tag1,tag2" --confidence 4.5 --sources 3
python3 scripts/knowledge.py search --query "X"
python3 scripts/knowledge.py stats

# Spaced repetition
python3 scripts/review.py schedule --topic "X" --category "ai"
python3 scripts/review.py due
python3 scripts/review.py done --topic "X"

# Sub-question generation
python3 scripts/questions.py generate --topic "X" --mode deep
python3 scripts/questions.py generate --topic "X" --mode quick

# Cross-validation
python3 scripts/validate.py check --topic "X"

# Source credibility
python3 scripts/credibility.py score --url "https://example.com"

# Report generation
python3 scripts/report.py create --topic "X" --format markdown
python3 scripts/report.py list

# Sub-knowledge import
python3 scripts/subknowledge.py scan --category "ai"
python3 scripts/subknowledge.py import --file "data.json"
```

</details>

---

## 🧠 How It Works

```
                         ┌─────────────────┐
                         │   User Topic    │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Sub-Question   │  3–12 focused questions
                         │   Generation    │  (based on learning mode)
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Multi-Source   │  Search & aggregate
                         │     Search      │  multiple sources
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Cross-Validate │  Compare & score
                         │  (credibility)  │  credibility 1–5
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Generate       │──→ User Review
                         │  Report         │    & Approval
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Knowledge      │  Store with tags
                         │  Ingestion      │  & relationships
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │    Spaced       │  Ebbinghaus curve
                         │   Repetition    │  1→3→7→14→30→90 days
                         └─────────────────┘
```

---

## 📁 Project Structure

```
deep-research/
├── SKILL.md                    # Core skill definition
├── learn.py                    # 🚀 Unified CLI entry
├── scripts/
│   ├── knowledge.py            # Knowledge base CRUD
│   ├── review.py               # Spaced repetition scheduler
│   ├── questions.py            # Sub-question generation
│   ├── validate.py             # Cross-validation engine
│   ├── credibility.py          # Source credibility scoring
│   ├── report.py               # Report generator
│   └── subknowledge.py         # Sub-knowledge importer
├── knowledge-base/             # 💾 Your knowledge data
│   ├── index.json              # Master index
│   ├── ai/  web/  python/      # 12 category dirs
│   ├── javascript/  devops/
│   ├── database/  security/
│   ├── mobile/  cloud/  data/
│   └── general/  uncategorized/
└── tests/                      # Test files
```

---

## ⚙️ Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REQUEST_BUDGET_QUICK` | `10` | Max requests for quick mode |
| `REQUEST_BUDGET_STUDY` | `25` | Max requests for standard mode |
| `REQUEST_BUDGET_DEEP` | `40` | Max requests for deep mode |
| `MIN_CREDIBILITY` | `3` | Minimum credibility to accept |
| `REVIEW_INTERVALS` | `1,3,7,14,30,90` | Days between reviews |

---

## 📦 Dependencies

**Zero.** Uses only Python standard library:

`json` · `datetime` · `pathlib` · `urllib` · `hashlib` · `argparse`

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** this repository
2. **Create** a feature branch — `git checkout -b feature/amazing`
3. **Commit** your changes — `git commit -m 'Add amazing feature'`
4. **Push** to the branch — `git push origin feature/amazing`
5. **Open** a Pull Request

---

## 📄 License

[MIT License](LICENSE) — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ for the [OpenClaw](https://github.com/openclaw/openclaw) ecosystem**

⭐ Star this repo if you find it useful!

</div>
