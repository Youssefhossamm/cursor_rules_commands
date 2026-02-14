# 🚀 Cursor Kickstart

A Streamlit app that helps developers **master Cursor Rules & Commands** — from zero to productive in minutes.

**🌐 Live App:** [cursor-kickstart.streamlit.app](https://cursor-kickstart.streamlit.app/)

## ✨ Features

- **📦 Customizable Starter Kit** — Download a tailored set of rules and commands — pick only what you need
- **🏗️ Interactive Rule Builder** — Build Cursor rules step by step with live preview and instant download
- **✅ Rule Validator** — Paste any rule to check for common issues, get token estimates, and improvement tips
- **📊 Learn the Difference** — Clear explanations of Cursor Commands vs Rules with side-by-side comparisons
- **🤖 AI Generation Prompts** — Ready-to-use prompts to generate project-specific rules using Cursor's built-in AI
- **⚡ Ready-to-Use Commands** — 10 generic slash commands that work with any project
- **📄 AGENTS.md Support** — Template for the simpler alternative that works with multiple AI tools
- **🔗 Verified Resources** — Links to official Cursor documentation and curated community resources
- **📁 Live Examples** — Real example files from this project's `.cursor/` directory

## 📦 Starter Kit Contents

The downloadable starter kit includes:

### Rules (5 files)
| Rule | Purpose |
|------|---------|
| `cursor-rules.md` | Meta rule - guidelines for writing rules |
| `project-structure.md` | Project overview template (customize this!) |
| `coding-standards.md` | Generic coding conventions |
| `git-conventions.md` | Commit message and branch naming |
| `rule-self-improvement.md` | Guidelines for evolving rules |

### Commands (10 files)
| Command | Purpose |
|---------|---------|
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

### Bonus
- **AGENTS.md** — Simple alternative for project-wide AI guidance

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
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore patterns
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
        ├── cursor-rules.md                # Meta rule about writing rules
        ├── project-structure.md           # Project architecture (alwaysApply)
        └── rule-self-improvement.md       # Meta rule for evolving rules
```

## 📚 New Cursor Features Covered

This app covers the latest Cursor documentation including:

- **Rule Types** — Project Rules, User Rules, Team Rules, AGENTS.md
- **Activation Modes** — Always, Glob patterns, Manual (`@rule-name`), Agent Decision
- **Hooks System** — 6 lifecycle hooks for extending AI operations
- **Best Practices** — Rule organization, file size guidelines, numbered files

## 🛠️ Build Tools

The **Build** tab includes interactive tools:

| Tool | Description |
|------|-------------|
| **Rule Builder** | Step-by-step wizard with activation mode picker, 18 glob presets, live preview |
| **Rule Validator** | Paste any rule to check frontmatter, detect conflicts, estimate tokens |
| **AI Prompts** | Copy-paste prompts for generating project-specific rules in Cursor |

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web UI framework (deployed on Streamlit Cloud) |
| **PyYAML** | YAML frontmatter parsing |

## 📖 What are Cursor Commands & Rules?

### Commands
Slash commands (like `/explain` or `/debug`) that you can invoke in Cursor's chat. They're stored in `.cursor/commands/` as markdown files.

### Rules
Background context that Cursor's AI always considers when working with your code. They're stored in `.cursor/rules/` and can be configured to apply globally or to specific file patterns using YAML frontmatter.

## 🔗 Resources

### Official Documentation
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
- [Cursor Commands Documentation](https://cursor.com/docs/context/commands)
- [Cursor Hooks Documentation](https://cursor.com/docs/agent/hooks)
- [Cursor Quickstart Guide](https://docs.cursor.com/get-started/quickstart)

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
