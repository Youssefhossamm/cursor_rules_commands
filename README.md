# Cursor Docs Explainer App

A Streamlit-based educational application that helps developers understand and leverage Cursor IDE's powerful customization features — Commands and Rules.

## ✨ Features

- **📊 Learn the Difference** — Clear explanations of Cursor Commands vs Rules with side-by-side comparisons
- **✨ AI Generation Prompts** — Ready-to-use prompts to generate project-specific rules using Cursor's built-in AI
- **⚡ Ready-to-Use Commands** — Generic slash commands that work with any project
- **🔗 Verified Resources** — Links to official Cursor documentation and curated community resources
- **📁 Live Examples** — Real example files from this project's `.cursor/` directory

## 🚀 Quick Start

### Prerequisites

- Python 3.8+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cursor_rules_commands.git
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
├── cursor_docs_app.py        # Main Streamlit entry point (5 tabs)
├── cursor_docs_content.py    # Content definitions, resources, examples
├── requirements.txt          # Python dependencies (streamlit, pyyaml)
├── .gitignore               # Git ignore patterns
│
└── .cursor/
    ├── commands/                           # Example slash commands
    │   ├── code-review-checklist.md       # /code-review-checklist
    │   ├── write-tests.md                 # /write-tests
    │   ├── debug.md                       # /debug
    │   ├── explain.md                     # /explain
    │   ├── run-app.md                     # /run-app - Start app in venv
    │   ├── stop-app.md                    # /stop-app - Stop running app
    │   └── sync-docs.md                   # /sync-docs - Sync README & rules
    ├── plans/                              # Cursor plan files
    └── rules/
        ├── cursor-rules.md                # Meta rule about writing rules
        ├── project-structure.md           # Project architecture (alwaysApply)
        └── rule-self-improvement.md       # Meta rule for evolving rules
```

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web UI framework |
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

### Community
- [cursor.directory](https://cursor.directory) - Browse community rules
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - GitHub collection (8k+ stars)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ for the Cursor community
</p>
