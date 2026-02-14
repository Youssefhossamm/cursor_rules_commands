---
description: Project structure and architecture overview for Cursor Kickstart
globs: []
alwaysApply: true
---

# Project Structure: Cursor Kickstart

## Overview

A Streamlit app that helps developers master Cursor Rules & Commands — from zero to productive in minutes. Deployed on **Streamlit Cloud** at [cursor-kickstart.streamlit.app](https://cursor-kickstart.streamlit.app/). Features a customizable starter kit, interactive rule builder, rule validator, AI generation prompts, live examples, and curated resources.

## Deployment

- **Production**: Streamlit Cloud — auto-deploys from `master` branch
- **URL**: https://cursor-kickstart.streamlit.app/
- **Constraints**: No local file paths, all dependencies must be in `requirements.txt`, no secrets needed

## Directory Layout

```
cursor_rules_commands/
├── cursor_docs_app.py        # UI: layout, CSS, sidebar, 5 tabs (~1660 lines)
├── cursor_docs_content.py    # Data: all content, templates, ZIP gen (~2175 lines)
├── requirements.txt          # Dependencies (streamlit, pyyaml)
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .gitignore               # Ignores venv/, .cursor/plans/, __pycache__/
│
├── .streamlit/
│   └── config.toml           # Streamlit theme (light, #4a7c94 primary)
│
├── .devcontainer/
│   └── devcontainer.json     # GitHub Codespaces config (Python 3.11)
│
└── .cursor/
    ├── commands/              # Slash commands (7 files)
    ├── plans/                 # Cursor plan files (gitignored)
    └── rules/                 # AI context rules (3 files)
```

## Architecture & Key Patterns

- **Two-file architecture**: `cursor_docs_app.py` owns UI/layout, `cursor_docs_content.py` owns all data/logic. New content goes in content module, new UI goes in app module.
- **Data-as-code**: All content stored in Python dicts/constants — no external DB or files
- **Custom HTML cards**: Three CSS classes (`.rule-card`, `.command-card`, `.info-card`) rendered via `st.markdown(html, unsafe_allow_html=True)`
- **Customizable Starter Kit**: ZIP generation supports full or user-selected subsets of rules/commands
- **Interactive Build Tools**: Rule Builder (form-based wizard) and Rule Validator (frontmatter checker, token estimator) in the Build tab
- **5-tab interface**: Overview, Live Examples, Build, Commands, Resources
- **YAML frontmatter parsing**: Custom parser in content module for live rule examples

## Streamlit Conventions

- `st.set_page_config()` must be the first Streamlit call in `cursor_docs_app.py`
- Custom CSS injected in a single `st.markdown()` block after page config
- Uses `wide` layout, `expanded` sidebar
- Session state used for tech rule selector and rule builder fields

## Key Technologies

- **Streamlit** - Web UI framework (deployed on Streamlit Cloud)
- **PyYAML** - YAML frontmatter parsing for live examples

## Running Locally

```bash
# Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
streamlit run cursor_docs_app.py
```
