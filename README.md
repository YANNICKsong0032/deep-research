<div align="center">

<img src="https://img.shields.io/badge/🔍-Deep_Research-0A0A0A?style=for-the-badge&labelColor=1a1a2e&color=16213e" alt="Deep Research" />

# 🔍 Deep Research

### Autonomous Deep Research Skill for AI Agents

*Web search → Cross-validation → Report → Review → Knowledge base → Spaced repetition*

<br>

[![MIT License](https://img.shields.io/badge/License-MIT-2ecc71?style=flat-square)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Zero Deps](https://img.shields.io/badge/Dependencies-Zero-f39c12?style=flat-square)](#-dependencies)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-9b59b6?style=flat-square)](https://github.com/openclaw/openclaw)

<br>

**[Quick Start](#-quick-start)** · **[Features](#-features)** · **[Usage](#-usage)** · **[How It Works](#-how-it-works)**

</div>

---

## ✨ Features

```
🔬 RESEARCH ENGINE                    🧠 KNOWLEDGE SYSTEM
─────────────────────                 ─────────────────────
▸ Three learning modes                ▸ 12 category directories
  quick / standard / deep               with JSON index & tags
▸ Multi-source search                 ▸ Spaced repetition
  cross-validates sources               Ebbinghaus 1→3→7→14→30→90d
▸ Credibility scoring 1-5             ▸ Knowledge linking
▸ Auto code verification                prerequisite / complement / extend

📊 ANALYTICS                          ⚡ EXPERIENCE
─────────────────────                 ─────────────────────
▸ Learning dashboard                  ▸ Unified CLI — one entry point
  count / mastery / duration          ▸ Zero dependencies
▸ Structured reports                    pure Python stdlib
▸ URL → extract key points            ▸ Modular & composable
```

---

## 🚀 Quick Start

> **3 commands. That's it.**

```bash
git clone https://github.com/YANNICKsong0032/deep-research.git && cd deep-research
python3 scripts/knowledge.py init
python3 learn.py quick "React Hooks"      # ← start here
```

### All Commands at a Glance

| | Command | What it does | Time |
|---|---------|-------------|------|
| 🔍 | `learn.py quick "X"` | Quick scan (3 questions) | ~15 min |
| 📚 | `learn.py study "X"` | Standard study (8 questions) | ~45 min |
| 🔬 | `learn.py deep "X"` | Deep research (12 questions) | ~90 min |
| 🔗 | `learn.py url "https://..."` | Learn from URL | ~5 min |
| ✅ | `learn.py verify "X"` | Verify existing knowledge | ~10 min |

---

## 📖 Usage

### Knowledge Management

```bash
learn.py search "X"          # 🔎 Search the knowledge base
learn.py stats               # 📊 Learning statistics
learn.py review-due          # 📅 Items due for review
learn.py expire              # ⏰ Expiration check
learn.py import-memory       # 📥 Import existing memories
```

<details>
<summary><strong>📂 Standalone Scripts</strong> <em>(click to expand)</em></summary>

<br>

**Knowledge Base**
```bash
python3 scripts/knowledge.py add --topic "X" --category "ai" --tags "a,b" --confidence 4.5
python3 scripts/knowledge.py search --query "X"
python3 scripts/knowledge.py stats
```

**Spaced Repetition**
```bash
python3 scripts/review.py schedule --topic "X" --category "ai"
python3 scripts/review.py due
python3 scripts/review.py done --topic "X"
```

**Research Pipeline**
```bash
python3 scripts/questions.py generate --topic "X" --mode deep
python3 scripts/validate.py check --topic "X"
python3 scripts/credibility.py score --url "https://example.com"
python3 scripts/report.py create --topic "X" --format markdown
```

</details>

---

## 🧠 How It Works

```
  ┌──────────────┐
  │  User Topic  │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Generate    │  3–12 focused sub-questions
  │  Questions   │  based on learning mode
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Multi-Source│  Search & aggregate
  │  Search      │  multiple sources
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Cross-      │  Compare & score
  │  Validate    │  credibility 1–5
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Report      │──── User Review ────┐
  │  & Ingest    │     & Approval      │
  └──────┬───────┘                     │
         ▼                             │
  ┌──────────────┐                     │
  │  Spaced      │  Ebbinghaus curve   │
  │  Repetition  │  1→3→7→14→30→90d   │
  └──────────────┘                     │
                                       │
                    ┌──────────────────┘
                    ▼
              ┌──────────┐
              │  Stored  │  tagged + linked
              │  Forever │  in knowledge base
              └──────────┘
```

---

## 📁 Structure

```
deep-research/
├── SKILL.md                    # Core definition
├── learn.py                    # 🚀 Unified CLI
├── scripts/
│   ├── knowledge.py            # CRUD
│   ├── review.py               # Scheduler
│   ├── questions.py            # Generator
│   ├── validate.py             # Validator
│   ├── credibility.py          # Scorer
│   ├── report.py               # Reporter
│   └── subknowledge.py         # Importer
└── knowledge-base/             # 💾 Data
    ├── index.json
    ├── ai/  web/  python/  js/
    ├── devops/  db/  security/
    └── mobile/  cloud/  data/
```

---

## ⚙️ Config

| Param | Default | Description |
|-------|---------|-------------|
| `REQUEST_BUDGET_QUICK` | `10` | Max requests — quick |
| `REQUEST_BUDGET_STUDY` | `25` | Max requests — standard |
| `REQUEST_BUDGET_DEEP` | `40` | Max requests — deep |
| `MIN_CREDIBILITY` | `3` | Min source credibility |
| `REVIEW_INTERVALS` | `1,3,7,14,30,90` | Days between reviews |

---

## 📦 Dependencies

> **None.** Pure Python standard library.

`json` · `datetime` · `pathlib` · `urllib` · `hashlib` · `argparse`

---

## 🤝 Contributing

```
Fork → Branch → Commit → Push → PR
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

[MIT](LICENSE) — use freely.

<br>

<div align="center">

**Made with ❤️ for [OpenClaw](https://github.com/openclaw/openclaw)**

*If this saved you time, a ⭐ goes a long way!*

</div>
