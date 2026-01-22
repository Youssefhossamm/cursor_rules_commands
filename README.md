# Cursor Docs Explainer App

A Streamlit-based educational application that helps developers understand and leverage Cursor IDE's powerful customization features — Commands and Rules.

## ✨ Features

- **📚 Learn the Difference** — Clear explanations of Cursor Commands vs Rules with side-by-side comparisons
- **🤖 AI-Powered Generation** — Generate project-specific rules tailored to your codebase using LLM prompts
- **⚡ Ready-to-Use Commands** — Generic slash commands that work with any project
- **🔗 Curated Resources** — Links to verified official documentation and community resources
- **🏗️ Interactive Generator** — Create `project-structure.md` files for your own projects

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key or Anthropic API key

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

4. **Set up environment variables**
   ```bash
   # Create a .env file or export directly
   export OPENAI_API_KEY=your_openai_key
   # OR
   export ANTHROPIC_API_KEY=your_anthropic_key
   ```

5. **Run the app**
   ```bash
   streamlit run cursor_docs_app.py
   ```

## 📁 Project Structure

```
cursor_rules_commands/
├── cursor_docs_app.py        # Main Streamlit entry point (6 tabs)
├── cursor_docs_content.py    # Content definitions, resources, examples
├── llm.py                    # LangChain LLM integration
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
│
└── .cursor/
    ├── commands/                           # Example slash commands
    │   ├── code-review-checklist.md       # /code-review-checklist
    │   ├── write-tests.md                 # /write-tests
    │   ├── debug.md                       # /debug
    │   └── explain.md                     # /explain
    ├── plans/
    │   └── *.plan.md                      # Cursor plan files
    └── rules/
        ├── cursor-rules.md                # Meta rule about writing rules
        └── project-structure.md           # Project architecture (alwaysApply)
```

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web UI framework |
| **LangChain** | LLM orchestration |
| **OpenAI / Anthropic** | AI model providers |

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI models (GPT-4, etc.) |
| `ANTHROPIC_API_KEY` | API key for Anthropic models (Claude) |

## 📖 What are Cursor Commands & Rules?

### Commands
Slash commands (like `/explain` or `/debug`) that you can invoke in Cursor's chat. They're stored in `.cursor/commands/` as markdown files.

### Rules
Background context that Cursor's AI always considers when working with your code. They're stored in `.cursor/rules/` and can be configured to apply globally or to specific file patterns.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ for the Cursor community
</p>
