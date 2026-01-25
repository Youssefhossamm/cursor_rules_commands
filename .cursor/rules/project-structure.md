---
description: Project structure and architecture overview for the Cursor Docs Explainer App
globs: []
alwaysApply: true
---

# Project Structure: Cursor Docs Explainer App

## Overview

This is a Streamlit-based educational application that:
- Explains the differences between Cursor Commands and Rules
- Provides AI-powered prompts to generate project-specific rules
- Includes ready-to-use generic commands for any project
- Links to verified official and community resources
- Offers an interactive project-structure.md generator

## Directory Layout

```
cursor_rules_commands/
├── cursor_docs_app.py        # Main Streamlit entry point (5 tabs)
├── cursor_docs_content.py    # Content definitions, resources, examples
├── requirements.txt          # Python dependencies (streamlit, pyyaml)
├── .gitignore               # Git ignore patterns
├── venv/                     # Python virtual environment
│
└── .cursor/
    ├── commands/                           # Example slash commands
    │   ├── code-review-checklist.md       # /code-review-checklist
    │   ├── write-tests.md                 # /write-tests
    │   ├── debug.md                       # /debug
    │   ├── explain.md                     # /explain
    │   ├── run-app.md                     # /run-app - Start app in venv
    │   └── stop-app.md                    # /stop-app - Stop running app
    ├── plans/
    │   └── *.plan.md                      # Cursor plan files
    └── rules/
        ├── cursor-rules.md                # Meta rule about writing rules
        ├── project-structure.md           # This file (alwaysApply)
        └── rule-self-improvement.md       # Meta rule for evolving rules
```

## Architecture

- **UI Layer**: Streamlit with 5-tab interface
- **Logic Layer**: Content module with definitions, resources, and examples
- **Data Sources**: Live `.cursor/` directory files

## Key Technologies

- **Streamlit** - Web UI framework
- **PyYAML** - YAML frontmatter parsing

## Running the Application

```bash
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run cursor_docs_app.py
```
