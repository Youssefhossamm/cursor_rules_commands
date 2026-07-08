# 🚀 Cursor Kickstart

A Streamlit app that helps developers **master Cursor Rules, Skills & Subagents** — from zero to productive in minutes.

**🌐 Live App:** [cursor-kickstart.streamlit.app](https://cursor-kickstart.streamlit.app/)

## ✨ Features

- **🤖 AI Generation Prompts** — The fastest way to add tailored rules to an existing project: one paste into Cursor chat generates rules from your own codebase (plus prompts for skills & subagents)
- **📦 Customizable Starter Kit** — 5 rules, 10 skills, 3 subagents, a hooks example, and AGENTS.md — pick only what you need
- **🤔 Decision Helper** — Answer two questions, learn whether you need a Rule, Skill, Subagent, Hook, or Automation
- **🏗️ Rule Builder & ⚡ Skill Builder** — Build `.mdc` rules and `SKILL.md` skills step by step with live preview
- **✅ Validator** — Paste any rule or skill to check for common issues, get token estimates, and improvement tips
- **⚡ Skills & Commands** — Full Skills documentation (the successor to slash commands), 10 ready-to-use skills, legacy command downloads, and migration notes
- **🤖 Subagents** — Docs plus verifier, code-reviewer, and test-writer templates
- **📄 AGENTS.md Support** — Template for the simpler alternative that works with multiple AI tools
- **🔗 Verified Resources** — Links to official Cursor documentation and curated community resources
- **📁 Live Examples** — Real example files from this project's `.cursor/` directory

## 📦 Starter Kit Contents

The downloadable starter kit includes:

### Rules (5 files)

Rule files use the `.mdc` extension — required by Cursor (plain `.md` files in `.cursor/rules/` are ignored).

| Rule | Purpose |
|------|---------|
| `cursor-rules.mdc` | Meta rule - guidelines for writing rules |
| `project-structure.mdc` | Project overview template (customize this!) |
| `coding-standards.mdc` | Generic coding conventions |
| `git-conventions.mdc` | Commit message and branch naming |
| `rule-self-improvement.mdc` | Guidelines for evolving rules |

### Skills (10 folders — successor to slash commands)
| Skill | Purpose |
|-------|---------|
| `/code-review-checklist` | Systematic code review |
| `/write-tests` | Generate comprehensive tests |
| `/debug` | Systematic debugging help |
| `/explain` | Detailed code explanation |
| `/refactor` | Refactoring suggestions |
| `/security-audit` | Security vulnerability scan |
| `/commit` | Generate commit messages |
| `/create-pr` | Generate PR descriptions |
| `/document` | Generate documentation |
| `/optimize` | Performance optimization |

### Subagents (3 files)
| Subagent | Purpose |
|----------|---------|
| `/verifier` | Read-only agent that double-checks finished work |
| `/code-reviewer` | Read-only reviewer for bugs, security & maintainability |
| `/test-writer` | Writes tests matching your project's conventions |

### Bonus
- **AGENTS.md** — Simple alternative for project-wide AI guidance
- **hooks.json.example** — Safe starting point for lifecycle hooks
- **Legacy commands** — The 10 classic `.cursor/commands/` files, available via the custom kit

## 🚀 Quick Start

### Prerequisites

- Python 3.8+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Youssefhossamm/cursor_rules_commands.git
   cd cursor_rules_commands
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run cursor_docs_app.py
   ```

## 📁 Project Structure

```
cursor_rules_commands/
├── cursor_docs_app.py        # UI: layout, CSS, sidebar, 5 tabs
├── cursor_docs_content.py    # Data: all content, templates, ZIP generation
├── requirements.txt          # Dependencies (streamlit, pyyaml)
├── requirements-dev.txt      # Dev dependencies (pytest)
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore patterns
│
├── tests/
│   ├── test_content.py       # Validators, builders, starter kit ZIPs
│   └── test_app.py           # Streamlit AppTest smoke & interaction tests
│
├── .github/
│   └── workflows/ci.yml      # Runs pytest on every push / PR
│
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
│
├── .devcontainer/
│   └── devcontainer.json     # GitHub Codespaces config (Python 3.11)
│
└── .cursor/
    ├── commands/              # Example slash commands (7 files)
    ├── plans/                 # Cursor plan files (gitignored)
    └── rules/
        ├── cursor-rules.mdc               # Meta rule about writing rules
        ├── project-structure.mdc          # Project architecture (alwaysApply)
        └── rule-self-improvement.mdc      # Meta rule for evolving rules
```

## 📚 New Cursor Features Covered

This app covers the latest Cursor documentation including:

- **Rule Types** — Project Rules (`.mdc`), User Rules, Team Rules, AGENTS.md (incl. nested)
- **Activation Modes** — Always, Glob patterns, Manual (`@rule-name`), Agent Decision
- **Hooks System** — 20+ lifecycle hooks (`hooks.json` v1) for observing and gating the agent loop
- **Skills Migration** — Commands are now legacy; notes on migrating to Skills with `/migrate-to-skills`
- **Best Practices** — Rule organization, file size guidelines (official 500-line max), referencing files instead of pasting code

## 🛠️ Build Tools

The **Build** tab includes interactive tools:

| Tool | Description |
|------|-------------|
| **AI Prompts** | Copy-paste prompts for generating project-specific rules, skills & subagents in Cursor |
| **Rule Builder** | Step-by-step wizard with activation mode picker, 18 glob presets, live preview |
| **Skill Builder** | Build a SKILL.md with invocation mode, path scoping, and inline validation |
| **Validator** | Paste any rule or skill to check frontmatter, detect conflicts, estimate tokens |

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web UI framework (deployed on Streamlit Cloud) |
| **PyYAML** | YAML frontmatter parsing |

## 📖 What are Cursor Rules, Skills & Subagents?

### Rules
Background context that Cursor's AI always considers when working with your code — *how the AI should behave*. Stored in `.cursor/rules/` as `.mdc` files; apply globally or to specific file patterns via YAML frontmatter.

### Skills
On-demand abilities — *how to do something*. Each skill is a `SKILL.md` in `.cursor/skills/<name>/`, invoked automatically or with `/name`. Skills superseded slash commands in Cursor 2.4 (commands in `.cursor/commands/` still work but are legacy).

### Subagents
Specialists the agent can delegate to — *who does the work*. Markdown files in `.cursor/agents/` with their own context window, model choice, and optional read-only mode.

## 🔗 Resources

### Official Documentation
- [Cursor Rules Documentation](https://cursor.com/docs/rules)
- [Cursor Skills Documentation](https://cursor.com/docs/skills) — successor to slash commands
- [Cursor Subagents Documentation](https://cursor.com/docs/subagents)
- [Cursor Hooks Documentation](https://cursor.com/docs/hooks)

### Community
- [cursor.directory](https://cursor.directory) - Browse community rules
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - GitHub collection (8k+ stars)
- [AGENTS.md](https://agentsmd.io/) - Open standard for AI agent guidance

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ for the Cursor community
</p>
