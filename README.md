# 🔍 Deep Research

> An autonomous **deep research** skill for AI Agents — web search → cross-validation → report generation → user review → knowledge ingestion → spaced repetition

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-orange.svg)](#dependencies)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Three Learning Modes** | Quick scan (5–15 min) / Standard study (30–60 min) / Deep research (60–120 min) |
| 🌐 **Multi-Source Search** | Cross-validates multiple sources with a 1–5 credibility score |
| 📝 **Learning Reports** | Auto-generated structured reports; user reviews before ingestion |
| 📂 **Categorized Knowledge Base** | 12 category directories, JSON index, tag system |
| 🔄 **Spaced Repetition** | Ebbinghaus forgetting curve: 1→3→7→14→30→90 days |
| 💾 **Resume on Interrupt** | Progress auto-saved; pause and continue anytime |
| 🔗 **Knowledge Linking** | Prerequisite, complementary, and extension relationships |
| 📊 **Learning Analytics** | Dashboard: knowledge count, mastery rate, study duration |
| 🎯 **URL Learning** | Feed a link → extract & learn its key points |
| ✅ **Code Verification** | Auto-validates whether code examples actually run |
| 🚀 **Unified Entry** | One `learn.py` CLI handles everything |

---

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/YANNICKsong0032/deep-research.git
cd deep-research
```

### 2. Initialize the Knowledge Base

```bash
python3 scripts/knowledge.py init
```

### 3. Start Learning

```bash
# Quick scan (~10 requests, ~15 min)
python3 learn.py quick "React Hooks"

# Standard study (~25 requests, ~45 min)
python3 learn.py study "Python Async"

# Deep research (~40 requests, ~90 min)
python3 learn.py deep "RAG Retrieval Augmented Generation"

# Learn from a URL
python3 learn.py url "https://example.com/article"

# Verify existing knowledge
python3 learn.py verify "React Hooks"
```

---

## 📖 Usage

### Learning Commands

| Command | Purpose | Request Budget |
|---------|---------|---------------|
| `python3 learn.py quick "X"` | Quick scan (3 questions) | ~10 |
| `python3 learn.py study "X"` | Standard study (8 questions) | ~25 |
| `python3 learn.py deep "X"` | Deep research (12 questions) | ~40 |
| `python3 learn.py url "https://..."` | Learn from URL | ~3 |
| `python3 learn.py verify "X"` | Verify existing knowledge | ~5 |

### Knowledge Management

| Command | Purpose |
|---------|---------|
| `python3 learn.py search "X"` | Search the knowledge base |
| `python3 learn.py stats` | Learning statistics |
| `python3 learn.py review-due` | Items due for review today |
| `python3 learn.py expire` | Expiration check |
| `python3 learn.py import-memory` | Import existing memories |

### Standalone Scripts

```bash
# Knowledge base management
python3 scripts/knowledge.py add --topic "X" --category "ai" --tags "tag1,tag2" --confidence 4.5 --sources 3
python3 scripts/knowledge.py search --query "X"
python3 scripts/knowledge.py stats

# Spaced repetition
python3 scripts/review.py schedule --topic "X" --category "ai"
python3 scripts/review.py due
python3 scripts/review.py done --topic "X"

# Smart sub-question generation
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

---

## 📁 Directory Structure

```
deep-research/
├── SKILL.md                 # Core skill definition
├── README.md                # This file
├── learn.py                 # Unified CLI entry point
├── scripts/
│   ├── knowledge.py         # Knowledge base management
│   ├── review.py            # Spaced repetition
│   ├── questions.py         # Sub-question generation
│   ├── validate.py          # Cross-validation
│   ├── credibility.py       # Source credibility scoring
│   ├── report.py            # Report generation
│   └── subknowledge.py      # Sub-knowledge import
├── knowledge-base/          # Your knowledge data
│   ├── index.json           # Knowledge index
│   ├── ai/                  # AI category
│   ├── web/                 # Web technology
│   ├── python/              # Python
│   ├── javascript/          # JavaScript
│   ├── devops/              # DevOps
│   ├── database/            # Databases
│   ├── security/            # Security
│   ├── mobile/              # Mobile development
│   ├── cloud/               # Cloud computing
│   ├── data/                # Data science
│   ├── general/             # General
│   └── uncategorized/       # Uncategorized
└── tests/                   # Test files
```

---

## 🧠 How It Works

```
User Topic
    │
    ▼
┌─────────────┐
│ Sub-Question │  Generate 3-12 focused sub-questions
│  Generation  │  based on learning mode
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Multi-Source │  Search multiple sources for each
│   Search     │  sub-question
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Cross-     │  Compare & validate information
│ Validation   │  across sources (credibility 1-5)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Learning    │  Generate structured report
│   Report     │  → User review & approval
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Knowledge   │  Store in categorized base
│  Ingestion   │  with tags & relationships
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Spaced     │  Schedule reviews on the
│  Repetition  │  Ebbinghaus curve
└─────────────┘
```

---

## ⚙️ Configuration

Edit `SKILL.md` to customize:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REQUEST_BUDGET_QUICK` | 10 | Max requests for quick mode |
| `REQUEST_BUDGET_STUDY` | 25 | Max requests for standard mode |
| `REQUEST_BUDGET_DEEP` | 40 | Max requests for deep mode |
| `MIN_CREDIBILITY` | 3 | Minimum credibility to accept a source |
| `REVIEW_INTERVALS` | 1,3,7,14,30,90 | Days between reviews |

---

## 📦 Dependencies

**Zero external dependencies.** Uses only Python standard library modules:

- `json` — Data storage
- `datetime` — Time management
- `pathlib` — File paths
- `urllib` — Web requests
- `hashlib` — Data integrity
- `argparse` — CLI parsing

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Inspired by the Ebbinghaus forgetting curve and spaced repetition research
- Built for the [OpenClaw](https://github.com/openclaw/openclaw) agent ecosystem
- Thanks to all contributors and the open-source community
