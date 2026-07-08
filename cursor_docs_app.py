"""
Cursor Kickstart

A Streamlit app that helps developers master Cursor Rules & Commands —
from zero to productive in minutes.

Run with: streamlit run cursor_docs_app.py
"""

import streamlit as st

# Import our modules
from cursor_docs_content import (
    FRONTMATTER_FIELDS,
    COMMON_GLOB_PRESETS,
    get_comparison_table,
    load_example_files,
    parse_frontmatter,
    get_file_annotations,
    get_quick_tips,
    get_prompt_templates,
    STARTER_PACK_PROMPT,
    get_generic_commands,
    get_external_resources,
    get_community_rule_examples,
    generate_starter_kit_zip,
    generate_custom_starter_kit_zip,
    get_starter_kit_contents,
    get_starter_kit_options,
    get_rule_types,
    get_rule_activation_modes,
    get_hooks_documentation,
    build_rule_content,
    validate_rule,
    STARTER_KIT_AGENTS_MD,
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Cursor Kickstart",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* ===== UI ENHANCEMENTS ===== */
    
    /* Container width */
    .main .block-container {
        max-width: 1200px;
    }
    
    /* === CARDS with hover effects === */
    
    /* Rules card - green/teal accent */
    .rule-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        border: 1px solid #86efac;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        color: #1f2937;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .rule-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.15);
        border-color: #22c55e;
    }
    
    .rule-card h3 {
        color: #16a34a !important;
        margin-top: 0 !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Commands card - amber/orange accent */
    .command-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fcd34d;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        color: #1f2937;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .command-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.15);
        border-color: #f59e0b;
    }
    
    .command-card h3 {
        color: #d97706 !important;
        margin-top: 0 !important;
    }
    
    /* Info card - blue accent */
    .info-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #93c5fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        color: #1f2937;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        border-color: #3b82f6;
    }
    
    .info-card h4, .info-card strong {
        color: #2563eb !important;
    }
    
    /* === Annotation boxes === */
    .annotation {
        background: #f8fafc;
        border-left: 4px solid #6366f1;
        padding: 0.875rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #374151;
        transition: background 0.2s ease;
    }
    
    .annotation:hover {
        background: #f1f5f9;
    }
    
    .annotation strong {
        color: #4f46e5;
    }
    
    .annotation code {
        background: #e0e7ff;
        padding: 2px 6px;
        border-radius: 4px;
        color: #4338ca;
        font-size: 0.85em;
    }
    
    .annotation em {
        color: #6b7280;
    }
    
    /* === Buttons with hover === */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(74, 124, 148, 0.25);
    }
    
    /* === Download buttons === */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%) !important;
        border: 1px solid #6ee7b7 !important;
        color: #047857 !important;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        border-color: #10b981 !important;
    }
    
    /* === Expanders with polish === */
    .streamlit-expanderHeader {
        border-radius: 8px;
        transition: background 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f5f9;
    }
    
    /* === Tables with hover rows === */
    tr {
        transition: background 0.15s ease;
    }
    
    tr:hover td {
        background: #f8fafc !important;
    }
    
    th {
        background: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    /* === Links with underline animation === */
    a {
        transition: color 0.2s ease;
    }
    
    /* === Code blocks === */
    code {
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace !important;
        background: #f1f5f9;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 0.9em;
    }
    
    /* === Subtle dividers === */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0 20%, #e2e8f0 80%, transparent) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* === Sidebar polish === */
    [data-testid="stSidebar"] a:hover {
        color: #2563eb !important;
    }
    
    /* Sidebar dividers - more visible */
    [data-testid="stSidebar"] hr {
        background: #c9d1d9 !important;
        height: 1px !important;
        margin: 1rem 0 !important;
    }
    
    /* === Tabs - more visible === */
    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9;
        padding: 6px;
        border-radius: 10px;
        gap: 4px;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 🧭 Navigation")
    st.markdown("---")
    
    # Prominent download button in sidebar
    st.markdown("### 📦 Quick Start")
    zip_data_sidebar = generate_starter_kit_zip()
    st.download_button(
        label="⬇️ Download Starter Kit",
        data=zip_data_sidebar,
        file_name="cursor-starter-kit.zip",
        mime="application/zip",
        key="download_starter_kit_sidebar",
        use_container_width=True,
    )
    st.caption("5 rules + 10 commands + AGENTS.md")
    
    st.markdown("---")
    
    st.markdown("### 📖 About This App")
    st.markdown("""
    Learn the difference between **Cursor Rules** and **Cursor Commands**, 
    explore real examples, and get prompts to generate your own using Cursor AI.
    """)
    
    st.markdown("---")
    
    st.markdown("### 📘 Official Docs")
    st.markdown("""
    - [Rules Documentation](https://cursor.com/docs/context/rules)
    - [Skills Documentation](https://cursor.com/docs/skills)
    - [Hooks Documentation](https://cursor.com/docs/agent/hooks)
    - [Cursor Quickstart](https://docs.cursor.com/get-started/quickstart)
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌐 Community")
    st.markdown("""
    - [cursor.directory](https://cursor.directory) - Browse rules
    - [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - GitHub collection
    - [AGENTS.md](https://agentsmd.io/) - Open standard
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚡ Quick Tips")
    for tip in get_quick_tips("general"):
        st.markdown(f"• {tip}")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="
        font-size: 2.5rem; 
        margin-bottom: 0.5rem;
        color: #1f2937;
        font-weight: 700;
    ">🚀 Cursor Kickstart</h1>
    <p style="
        font-size: 1.1rem; 
        color: #6b7280; 
        max-width: 600px; 
        margin: 0 auto;
    ">Master Cursor Rules & Commands — from zero to productive in minutes</p>
</div>
""", unsafe_allow_html=True)

# Tab names for navigation
TAB_NAMES = ["📊 Overview", "📁 Live Examples", "🛠️ Build", "⚡ Commands", "🔗 Resources"]

# Create tabs
tab_overview, tab_examples, tab_build, tab_commands, tab_resources = st.tabs(TAB_NAMES)

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

with tab_overview:

    # =========================================================================
    # HERO — GET SET UP FAST
    # =========================================================================

    st.markdown("## 🚀 Get Set Up in 2 Minutes")
    st.markdown("**Two ways to start — pick the one that fits:**")

    col_path1, col_path2 = st.columns(2)

    with col_path1:
        st.markdown("""
        <div class="command-card" style="min-height: 215px;">
            <h4 style="margin-top: 0;">🤖 AI-Tailored Rules</h4>
            <p><em>Best for: existing projects</em></p>
            <ul style="margin-bottom: 0;">
                <li>Copy <strong>one prompt</strong> into Cursor chat</li>
                <li>The AI analyzes <strong>your</strong> codebase</li>
                <li>Rules match your real stack & conventions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("👇 **The prompt is right below** — more in **🛠️ Build → 🤖 AI Prompts**")

    with col_path2:
        st.markdown("""
        <div class="rule-card" style="min-height: 215px;">
            <h4 style="margin-top: 0;">📦 Starter Kit</h4>
            <p><em>Best for: new projects & instant generic setup</em></p>
            <ul style="margin-bottom: 0;">
                <li><strong>5 essential rules</strong> + <strong>10 commands</strong> + AGENTS.md</li>
                <li>Generic best practices — works everywhere</li>
                <li>Download, copy <code>.cursor/</code>, done</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Generate and offer ZIP download
        zip_data = generate_starter_kit_zip()
        st.download_button(
            label="⬇️ Download Starter Kit",
            data=zip_data,
            file_name="cursor-starter-kit.zip",
            mime="application/zip",
            key="download_starter_kit_main",
            use_container_width=True,
        )

    # Path 1: the flagship one-prompt setup for existing projects
    with st.expander("🤖 **One-Prompt Setup for Existing Projects** — copy, paste into Cursor chat, done", expanded=False):
        st.markdown("""
        Cursor's AI analyzes your codebase and creates the **3 essential rules** — meta rule,
        project structure, and coding standards — tailored to your project:
        """)
        st.code(STARTER_PACK_PROMPT, language="text")
        st.caption("💡 Want more? Prompts for API conventions, testing, data models and more live in **🛠️ Build → 🤖 AI Prompts**.")

    # Path 2: starter kit setup steps
    with st.expander("📦 **Starter Kit Setup** — 3 steps", expanded=False):
        st.markdown("""
        1. Extract the ZIP and copy the `.cursor/` folder (and optionally `AGENTS.md`) to your project root
        2. Customize `project-structure.mdc` with your project details
        3. Type `/` in Cursor chat — your commands are ready! 🎉
        """)

    # Customizable kit
    with st.expander("🎨 **Customize Your Kit** — pick only what you need", expanded=False):
        kit_options = get_starter_kit_options()

        col_rules_pick, col_cmds_pick = st.columns(2)

        selected_rules: list[str] = []
        selected_commands: list[str] = []

        with col_rules_pick:
            st.markdown("**📋 Rules**")
            for name, desc in kit_options["rules"].items():
                if st.checkbox(f"{name}", value=True, key=f"kit_r_{name}", help=desc):
                    selected_rules.append(name)

        with col_cmds_pick:
            st.markdown("**⚡ Commands**")
            for name, desc in kit_options["commands"].items():
                cmd_label = f"/{name.replace('.md', '')}"
                if st.checkbox(cmd_label, value=True, key=f"kit_c_{name}", help=desc):
                    selected_commands.append(name)

        include_agents = st.checkbox("📄 Include AGENTS.md", value=True, key="kit_agents")

        item_count = len(selected_rules) + len(selected_commands) + (1 if include_agents else 0)

        if item_count > 0:
            custom_zip = generate_custom_starter_kit_zip(selected_rules, selected_commands, include_agents)
            st.download_button(
                label=f"⬇️ Download Custom Kit ({len(selected_rules)} rules, {len(selected_commands)} commands)",
                data=custom_zip,
                file_name="cursor-starter-kit.zip",
                mime="application/zip",
                key="download_custom_kit",
                use_container_width=True,
            )
        else:
            st.warning("Select at least one item to download.")

    # Setup scripts
    with st.expander("🖥️ **One-Line Setup Scripts** (Alternative)", expanded=False):
        st.markdown("If you prefer command-line setup, use these scripts after downloading:")

        st.markdown("**PowerShell (Windows):**")
        ps_script = """# Run in your project directory after downloading cursor-starter-kit.zip
Expand-Archive cursor-starter-kit.zip -DestinationPath . -Force
Move-Item cursor-starter-kit\\.cursor . -Force
Move-Item cursor-starter-kit\\AGENTS.md . -Force
Remove-Item cursor-starter-kit -Recurse -Force
Remove-Item cursor-starter-kit.zip -Force"""
        st.code(ps_script, language="powershell")

        st.markdown("**Bash (macOS/Linux):**")
        bash_script = """# Run in your project directory after downloading cursor-starter-kit.zip
unzip cursor-starter-kit.zip
mv cursor-starter-kit/.cursor .
mv cursor-starter-kit/AGENTS.md .
rm -rf cursor-starter-kit cursor-starter-kit.zip"""
        st.code(bash_script, language="bash")

    st.markdown("---")

    # =========================================================================
    # FEATURE DIRECTORY — WHERE TO FIND EVERYTHING
    # =========================================================================

    st.markdown("## 🧭 Explore the App")

    feat_row1 = st.columns(3)
    with feat_row1[0]:
        st.markdown("""
        <div class="rule-card" style="min-height: 140px;">
            <strong>🤖 AI Prompts ⭐</strong><br/>
            <em>The fastest way to add tailored rules to an existing project</em><br/>
            <span style="font-size: 0.85rem; color: #6b7280;">→ 🛠️ Build tab</span>
        </div>
        """, unsafe_allow_html=True)
    with feat_row1[1]:
        st.markdown("""
        <div class="rule-card" style="min-height: 140px;">
            <strong>🏗️ Rule Builder</strong><br/>
            <em>Build a .mdc rule step by step with live preview & download</em><br/>
            <span style="font-size: 0.85rem; color: #6b7280;">→ 🛠️ Build tab</span>
        </div>
        """, unsafe_allow_html=True)
    with feat_row1[2]:
        st.markdown("""
        <div class="rule-card" style="min-height: 140px;">
            <strong>✅ Rule Validator</strong><br/>
            <em>Paste any rule — get issues, tips & a token estimate</em><br/>
            <span style="font-size: 0.85rem; color: #6b7280;">→ 🛠️ Build tab</span>
        </div>
        """, unsafe_allow_html=True)

    feat_row2 = st.columns(3)
    with feat_row2[0]:
        st.markdown("""
        <div class="command-card" style="min-height: 140px;">
            <strong>⚡ 10 Ready Commands</strong><br/>
            <em>Code review, tests, debug, refactor... + Skills migration notes</em><br/>
            <span style="font-size: 0.85rem; color: #6b7280;">→ ⚡ Commands tab</span>
        </div>
        """, unsafe_allow_html=True)
    with feat_row2[1]:
        st.markdown("""
        <div class="info-card" style="min-height: 140px;">
            <strong>📁 Live Examples</strong><br/>
            <em>Real rules & commands from this project, annotated</em><br/>
            <span style="font-size: 0.85rem; color: #6b7280;">→ 📁 Live Examples tab</span>
        </div>
        """, unsafe_allow_html=True)
    with feat_row2[2]:
        st.markdown("""
        <div class="info-card" style="min-height: 140px;">
            <strong>🔗 Resources & More</strong><br/>
            <em>Official docs, community rules, AGENTS.md, hooks reference</em><br/>
            <span style="font-size: 0.85rem; color: #6b7280;">→ 🔗 Resources tab</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # =========================================================================
    # THE 30-SECOND BASICS
    # =========================================================================

    st.markdown("## 📊 Rules vs Commands — the 30-Second Version")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="rule-card">
            <h3>📋 Rules</h3>
            <p><strong>Persistent context that guides the AI</strong></p>
            <ul>
                <li>Located in <code>.cursor/rules/</code> as <code>.mdc</code> files</li>
                <li>Triggered by file patterns or always active</li>
                <li>Uses YAML frontmatter + Markdown</li>
                <li>Great for coding standards & architecture</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="command-card">
            <h3>⚡ Commands</h3>
            <p><strong>On-demand actions triggered by you</strong></p>
            <ul>
                <li>Located in <code>.cursor/commands/</code></li>
                <li>Triggered by <code>/slash-command</code></li>
                <li>Plain Markdown instructions</li>
                <li>Legacy — superseded by <strong>Skills</strong>, but still supported</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.info("""
    🆕 **2026 update:** Rules now **must use the `.mdc` extension** (plain `.md` files in `.cursor/rules/` are ignored),
    and Cursor has introduced **Skills** (`SKILL.md`) as the successor to slash commands — existing commands still work.
    See the **⚡ Commands** tab for migration notes.
    """)

    st.markdown("---")

    # =========================================================================
    # DEEP DIVE — OPTIONAL READING, ALL COLLAPSED
    # =========================================================================

    st.markdown("## 📚 The Details (optional reading)")
    st.caption("The essentials above are enough to get productive — expand below only what you need.")

    with st.expander("📁 **Types of Cursor Rules** — Project, User, Team, AGENTS.md", expanded=False):
        rule_types = get_rule_types()
        cols_types = st.columns(4)

        for idx, (key, rule_type) in enumerate(rule_types.items()):
            with cols_types[idx]:
                card_class = "rule-card" if key != "agents_md" else "info-card"
                st.markdown(f"""
                <div class="{card_class}" style="min-height: 180px;">
                    <h4 style="margin-top: 0;">{rule_type['icon']} {rule_type['name']}</h4>
                    <p style="font-size: 0.85rem;"><code>{rule_type['location']}</code></p>
                    <p style="font-size: 0.85rem; color: #6b7280;">{rule_type['description']}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("""
        <div class="info-card">
            <strong>Also good to know:</strong>
            <ul style="margin-bottom: 0;">
                <li><strong>Precedence:</strong> Team Rules → Project Rules → User Rules (admins can enforce Team Rules)</li>
                <li><strong>Remote rules:</strong> import <code>.mdc</code> rules straight from GitHub repos via <em>Customize → Rules → Add Rule</em></li>
                <li><strong>Nested AGENTS.md:</strong> place additional AGENTS.md files in subdirectories — the closest one to a file wins</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("⚡ **Rule Activation Modes** — Always, Glob, Manual, Agent Decision", expanded=False):
        activation_modes = get_rule_activation_modes()

        for mode_key, mode in activation_modes.items():
            st.markdown(f"**{mode['name']}** — `{mode['trigger']}`")
            st.markdown(f"{mode['description']}  \n*Best for: {mode['best_for']}*")
            st.markdown("")

        st.info("💡 **Tip:** Use `@rule-name` in chat to manually include any rule. This works even for rules without `alwaysApply` or matching globs!")

    with st.expander("📊 **Side-by-Side Comparison** — Rules vs Commands in detail", expanded=False):
        st.markdown(get_comparison_table())

    with st.expander("🗂️ **Directory Structure & Frontmatter Fields**", expanded=False):
        st.code("""
.cursor/
├── rules/                          # Automatic context injection (.mdc required)
│   ├── cursor-rules.mdc            # Guidelines for writing rules
│   └── project-structure.mdc       # Always-active project overview
│
└── commands/                       # Manual slash commands (legacy — see Skills)
    └── code-review-checklist.md   # Invoked with /code-review-checklist
        """, language="text")

        st.markdown("#### Rule Frontmatter Fields")
        for field, info in FRONTMATTER_FIELDS.items():
            st.markdown(f"**`{field}`** — {info['type']} ({'required' if info['required'] else 'optional'})")
            st.markdown(info['description'])
            st.code(info['example'], language="yaml")

    with st.expander("📏 **Sizing Rules & When to Use What**", expanded=False):
        col_use1, col_use2 = st.columns(2)

        with col_use1:
            st.markdown("#### ✅ Use **Rules** When...")
            st.markdown("""
            - You want context always available
            - Defining coding standards
            - Documenting project architecture
            - Setting up style guidelines
            - Creating language/framework-specific guidance
            """)

        with col_use2:
            st.markdown("#### ✅ Use **Commands** When...")
            st.markdown("""
            - You need on-demand actions
            - Running code reviews
            - Generating boilerplate code
            - Performing specific tasks
            - Creating reusable workflows
            """)

        st.markdown("#### 📏 Rule File Size Guidelines")

        col_size1, col_size2 = st.columns([2, 1])

        with col_size1:
            st.markdown("""
            | Rule Type | Recommended Size | Notes |
            |-----------|------------------|-------|
            | Single rule file | **50-150 lines** | Keeps context focused |
            | Official maximum | **under 500 lines** | Split into composable rules |
            | `alwaysApply: true` rules | **Keep minimal!** | Always consumes context |
            | Total active rules | ~2000-3000 tokens | Leaves room for your code |
            """)

        with col_size2:
            st.markdown("""
            <div class="info-card" style="text-align: center;">
                <strong>📐 Rule of Thumb</strong><br/><br/>
                <em>If your rule file is longer than your average source file, it's too long.</em>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        **💡 Best Practices:** Multiple small focused rules > one giant rule • Use `globs` to load rules only when needed • Bullet points > paragraphs
        """)

    with st.expander("🛠️ **Manual Setup** — step-by-step, without the Starter Kit", expanded=False):
        st.markdown("#### Step 1: Create the `.cursor/` directory structure")
        st.code("""
# In your project root, create:
.cursor/
├── rules/      # For persistent AI context (.mdc files)
└── commands/   # For on-demand actions
        """, language="text")

        st.markdown("#### Step 2: Create the meta rule (`cursor-rules.mdc`)")
        st.markdown("**First, teach Cursor AI how to write rules!** This \"meta rule\" establishes the pattern for all future rules.")

        cursor_rules_template = """---
description: Guidelines for writing effective Cursor rules
globs:
  - ".cursor/rules/**"
alwaysApply: false
---

# Cursor Rules Best Practices

## Rule Structure

Every rule file must include:
1. **YAML Frontmatter** - Metadata controlling when/how the rule applies
2. **Markdown Content** - Clear, actionable instructions

## Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief summary shown in Cursor UI |
| `globs` | array | File patterns that trigger this rule |
| `alwaysApply` | boolean | If true, always includes this rule |

## Best Practices

- Save rules as `.mdc` files — plain `.md` files in `.cursor/rules/` are ignored
- Keep rules focused on a single concern
- Use specific globs to avoid noise
- Write clear, actionable instructions
- Keep content concise (official maximum: 500 lines)
- Include examples where helpful"""
        st.code(cursor_rules_template, language="markdown")
        st.download_button(
            label="⬇️ Download cursor-rules.mdc",
            data=cursor_rules_template,
            file_name="cursor-rules.mdc",
            mime="text/markdown",
            key="download_cursor_rules_template",
        )
        st.success("📍 **Save this to:** `.cursor/rules/cursor-rules.mdc`")

        st.markdown("#### Step 3: Generate `project-structure.mdc` with AI")
        st.markdown("Use Cursor AI to create a rule documenting your project — it will follow the meta rule you just created. **Copy this prompt into Cursor Chat:**")

        bootstrap_prompt_quick = """@.cursor/rules/cursor-rules.mdc Analyze this project and create a project-structure.mdc rule.

CONSTRAINTS:
- Keep it under 80 lines total
- Focus on high-level architecture only
- List only main directories (max 2 levels deep)
- Summarize tech stack in bullet points
- Do NOT list every file - just key entry points

Include: Overview, Directory Layout, Tech Stack, How to Run."""

        st.code(bootstrap_prompt_quick, language="text")

        st.info("💡 **Why this works:** The `@.cursor/rules/cursor-rules.mdc` reference teaches the AI your rule format before it generates the new rule!")

        st.markdown("#### Step 4: Add ready-to-use commands")
        st.success("👉 Grab `/code-review-checklist`, `/write-tests`, `/debug` and more from the **⚡ Commands** tab — or just use the Starter Kit above.")

# ============================================================================
# TAB 2: LIVE EXAMPLES
# ============================================================================

with tab_examples:
    st.markdown("## Real Examples from This Project")
    st.markdown("These are actual files from the `.cursor/` directory of this project.")
    
    # Load example files
    examples = load_example_files()
    
    # Rules section
    st.markdown("### 📋 Rules")
    
    if examples["rules"]:
        for filename, content in examples["rules"].items():
            with st.expander(f"📄 {filename}", expanded=False):
                # Parse and show annotations
                frontmatter, body = parse_frontmatter(content)
                
                if frontmatter:
                    st.markdown("#### Frontmatter Analysis")
                    annotations = get_file_annotations(filename, content)
                    for ann in annotations:
                        st.markdown(f"""
                        <div class="annotation">
                            <strong>{ann['field']}</strong>: <code>{ann['value']}</code><br/>
                            <em>{ann['explanation']}</em>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("---")
                
                st.markdown("#### Full Content")
                st.code(content, language="markdown")
    else:
        st.info("No rule files found in `.cursor/rules/`")
    
    st.markdown("---")
    
    # Commands section
    st.markdown("### ⚡ Commands")
    
    if examples["commands"]:
        for filename, content in examples["commands"].items():
            with st.expander(f"📄 {filename}", expanded=False):
                # Commands don't have frontmatter
                command_name = filename.replace(".md", "")
                st.markdown(f"""
                <div class="annotation">
                    <strong>Invoke with</strong>: <code>/{command_name}</code><br/>
                    <em>Type this in Cursor chat to trigger this command</em>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
                
                st.markdown("#### Full Content")
                st.code(content, language="markdown")
    else:
        st.info("No command files found in `.cursor/commands/`")
    
    st.markdown("---")
    
    # Key observations
    st.markdown("### 🔍 Key Observations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Rules have:**
        - YAML frontmatter with metadata
        - `globs` for file pattern matching
        - `alwaysApply` for persistent rules
        - `description` for UI display
        """)
    
    with col2:
        st.markdown("""
        **Commands have:**
        - Plain markdown content
        - No special metadata
        - Filename becomes the command
        - Clear action instructions
        """)

# ============================================================================
# TAB 3: AI PROMPTS FOR SELF-GENERATION
# ============================================================================

with tab_build:
    st.markdown("## 🛠️ Build Tools")
    st.markdown("Generate rules with AI, build them by hand, or validate what you already have:")

    build_tab_ai, build_tab_builder, build_tab_validator = st.tabs([
        "🤖 AI Prompts (recommended)",
        "🏗️ Rule Builder",
        "✅ Rule Validator",
    ])

    # =================================================================
    # SUB-TAB 1: AI-POWERED GENERATION PROMPTS
    # =================================================================

    with build_tab_ai:
        st.markdown("### 🤖 Let Cursor's AI Write Your Rules")
        st.markdown("""
        **The easiest way to add rules to an existing project.** Copy a prompt, paste it into Cursor chat
        (Cmd/Ctrl + L), and the AI analyzes **your** codebase to generate rules that match how your project
        actually works — your stack, your naming, your conventions.
        """)

        # Hero: full setup in one prompt
        st.markdown("#### 🎁 Full Setup in One Prompt — start here")
        st.markdown("No prerequisites. This single prompt generates all 3 essential rules straight from your codebase:")

        col_pack1, col_pack2, col_pack3 = st.columns(3)
        with col_pack1:
            st.markdown("""
            <div class="rule-card" style="min-height: 80px; text-align: center;">
                <strong>📋 cursor-rules.mdc</strong><br/>
                <em>Meta rule</em>
            </div>
            """, unsafe_allow_html=True)
        with col_pack2:
            st.markdown("""
            <div class="rule-card" style="min-height: 80px; text-align: center;">
                <strong>🏗️ project-structure.mdc</strong><br/>
                <em>Architecture</em>
            </div>
            """, unsafe_allow_html=True)
        with col_pack3:
            st.markdown("""
            <div class="rule-card" style="min-height: 80px; text-align: center;">
                <strong>📝 coding-standards.mdc</strong><br/>
                <em>Conventions</em>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        st.code(STARTER_PACK_PROMPT, language="text")

        st.info("💡 **Tip:** After running this, you'll have a complete Cursor rules setup! The AI will analyze your codebase and create tailored rules.")

        st.markdown("---")

        # Focused: project-structure only
        st.markdown("#### 🎯 Project Structure Only")
        st.markdown("""
        Already have the meta rule (`cursor-rules.mdc`)? Use this optimized prompt to generate just the
        `project-structure.mdc` rule — **includes constraints** to keep output concise even for large projects.
        """)

        bootstrap_prompt = """@.cursor/rules/cursor-rules.mdc @Codebase

Create a project-structure.mdc rule for this project.

## CONSTRAINTS (IMPORTANT):
- Maximum 100 lines total
- Directory tree: max 2 levels deep, only main folders
- Do NOT list every file - summarize with comments like "# API routes"
- Tech stack: bullet points only, no version numbers unless critical
- Skip boilerplate sections if not applicable

## REQUIRED SECTIONS:
1. **Overview** (2-3 sentences max)
2. **Directory Layout** (tree format, annotated)
3. **Key Technologies** (bullet list)
4. **Running the App** (essential commands only)

## FORMAT:
```yaml
---
description: Project structure for [name]
globs: []
alwaysApply: true
---
```

Be concise. Quality over quantity."""

        st.code(bootstrap_prompt, language="text")

        st.markdown("**⚡ Quick version** — if you're experienced and already have `cursor-rules.mdc`:")

        minimal_prompt = """@.cursor/rules/cursor-rules.mdc Analyze this project. Create a concise project-structure.mdc rule (under 80 lines). Focus on: overview, directory layout (2 levels max), tech stack, run commands. Use alwaysApply: true."""

        st.code(minimal_prompt, language="text")

        st.markdown("---")

        # Individual rule prompts
        st.markdown("#### 📋 Generate Specific Rules")
        st.markdown("One prompt per rule — coding standards, API conventions, testing, data models, and more:")

        st.warning("""
        ⚠️ These prompts reference `@.cursor/rules/cursor-rules.mdc` so the output stays consistently formatted.
        Don't have that file yet? Run the **Full Setup** prompt above first, or grab it from the Starter Kit (📊 Overview tab).
        """)

        rule_prompts = get_prompt_templates("rules")
        for prompt_data in rule_prompts:
            with st.expander(f"**{prompt_data['name']}** - {prompt_data['description']}", expanded=False):
                st.markdown(f"**Output file:** `{prompt_data['output_file']}`")
                st.markdown("**Prompt to copy:**")
                st.code(prompt_data['prompt'], language="text")
                st.markdown("---")
                st.markdown("**How to use:**")
                st.markdown(f"""
                1. Copy the prompt above
                2. Open Cursor chat (Cmd/Ctrl + L)
                3. Paste and press Enter — Cursor creates `{prompt_data['output_file']}` automatically
                """)

        st.markdown("---")

        # Command generation prompts
        st.markdown("#### ⚡ Generate Custom Commands")
        st.markdown("Copy these prompts to generate commands tailored to your project:")

        command_prompts = get_prompt_templates("commands")
        for prompt_data in command_prompts:
            with st.expander(f"**{prompt_data['name']}** - {prompt_data['description']}", expanded=False):
                st.markdown(f"**Output file:** `{prompt_data['output_file']}`")
                st.markdown("**Prompt to copy:**")
                st.code(prompt_data['prompt'], language="text")
                st.markdown("---")
                st.markdown("**How to use:**")
                st.markdown(f"""
                1. Copy the prompt above
                2. Open Cursor chat (Cmd/Ctrl + L)
                3. Paste and press Enter — Cursor creates `{prompt_data['output_file']}` automatically
                """)

    # =================================================================
    # SUB-TAB 2: INTERACTIVE RULE BUILDER
    # =================================================================

    with build_tab_builder:
        st.markdown("### 🏗️ Interactive Rule Builder")
        st.markdown("Build a Cursor rule step by step — preview and download instantly.")

        col_rb1, col_rb2 = st.columns(2)

        with col_rb1:
            rb_title = st.text_input(
                "Rule Title",
                placeholder="e.g., Coding Standards",
                key="rb_title",
            )
        with col_rb2:
            rb_description = st.text_input(
                "Description (shown in Cursor UI)",
                placeholder="e.g., Python coding conventions for this project",
                key="rb_desc",
            )

        rb_mode = st.radio(
            "Activation Mode",
            ["Always Active", "Glob Patterns", "Agent Decision", "Manual Only"],
            horizontal=True,
            key="rb_mode",
            help="How should Cursor trigger this rule?",
        )

        rb_globs: list[str] = []
        rb_always = False

        if rb_mode == "Always Active":
            rb_always = True
            st.caption("✅ This rule will always be included in AI context. Keep it concise.")
        elif rb_mode == "Glob Patterns":
            col_preset, col_custom = st.columns([1, 1])
            with col_preset:
                selected_presets = st.multiselect(
                    "Quick Select (presets)",
                    options=list(COMMON_GLOB_PRESETS.keys()),
                    key="rb_presets",
                )
                for preset in selected_presets:
                    rb_globs.extend(COMMON_GLOB_PRESETS[preset])
            with col_custom:
                custom_globs_str = st.text_input(
                    "Custom patterns (comma-separated)",
                    placeholder='src/api/**/*.ts, **/*.test.js',
                    key="rb_custom_globs",
                )
                if custom_globs_str:
                    rb_globs.extend([g.strip().strip('"').strip("'") for g in custom_globs_str.split(",") if g.strip()])
            # Deduplicate while preserving order
            rb_globs = list(dict.fromkeys(rb_globs))
            if rb_globs:
                st.caption(f"📁 Patterns: `{'`, `'.join(rb_globs)}`")
        elif rb_mode == "Agent Decision":
            st.caption("🤖 The AI decides whether to include this rule based on the description field.")
        else:
            st.caption("📌 Only included when you type `@rule-name` in Cursor chat.")

        rb_body = st.text_area(
            "Rule Content (Markdown)",
            value="## Guidelines\n\n- \n\n## Best Practices\n\n- \n\n## Examples\n\n(Add code examples here)",
            height=250,
            key="rb_body",
        )

        # Preview
        if rb_title:
            generated_rule = build_rule_content(
                description=rb_description,
                globs=rb_globs,
                always_apply=rb_always,
                title=rb_title,
                body=rb_body,
            )

            with st.expander("📄 Preview Generated Rule", expanded=True):
                st.code(generated_rule, language="markdown")

            rb_filename = rb_title.lower().replace(" ", "-").replace("/", "-") + ".mdc"
            st.download_button(
                label=f"⬇️ Download {rb_filename}",
                data=generated_rule,
                file_name=rb_filename,
                mime="text/markdown",
                key="rb_download",
            )
            st.caption(f"Save to: `.cursor/rules/{rb_filename}`")
        else:
            st.info("👆 Enter a rule title to see the preview and download button.")

    # =================================================================
    # SUB-TAB 3: RULE VALIDATOR
    # =================================================================

    with build_tab_validator:
        st.markdown("### ✅ Rule Validator")
        st.markdown("Paste an existing rule to check for common issues and get improvement suggestions.")

        rv_input = st.text_area(
            "Paste your rule content here",
            height=200,
            placeholder="---\ndescription: My coding standards\nglobs:\n  - \"**/*.py\"\nalwaysApply: false\n---\n\n# Coding Standards\n\n- Use type hints\n- ...",
            key="rv_input",
        )

        if rv_input.strip():
            results = validate_rule(rv_input)

            # Summary counts
            passes = sum(1 for r in results if r["level"] == "pass")
            warnings = sum(1 for r in results if r["level"] == "warning")
            errors = sum(1 for r in results if r["level"] == "error")

            st.markdown(f"**Results:** ✅ {passes} passed · ⚠️ {warnings} warnings · ❌ {errors} errors")

            for result in results:
                if result["level"] == "pass":
                    st.success(f"**{result['message']}** — {result['detail']}")
                elif result["level"] == "warning":
                    st.warning(f"**{result['message']}** — {result['detail']}")
                elif result["level"] == "error":
                    st.error(f"**{result['message']}** — {result['detail']}")
                elif result["level"] == "info":
                    st.info(f"**{result['message']}** — {result['detail']}")
        else:
            st.caption("Paste a rule above to validate it.")

# ============================================================================
# TAB 4: GENERIC COMMANDS
# ============================================================================

with tab_commands:
    st.markdown("## ⚡ Ready-to-Use Commands")

    st.warning("""
    ⚠️ **Commands are now a legacy feature (2026).** Cursor has superseded slash commands with
    **Skills** — `SKILL.md` files in `.cursor/skills/<skill-name>/` that can bundle scripts and assets,
    and can be invoked automatically or with the same `/name` syntax.

    Your existing `.cursor/commands/` files **still work**, so everything below remains usable.
    To modernize, run Cursor's built-in **`/migrate-to-skills`** — it converts commands into skills with
    `disable-model-invocation: true`, preserving the explicit `/name` behavior.
    [📘 Skills documentation](https://cursor.com/docs/skills)
    """)

    st.markdown("""
    These are **universal commands** that work for any project. Copy them directly
    into your `.cursor/commands/` directory to use them immediately.
    """)
    
    st.markdown("---")
    
    generic_commands = get_generic_commands()
    
    # Command categories
    categories = {
        "Code Quality": ["code-review-checklist", "refactor", "explain"],
        "Development": ["write-tests", "debug", "optimize"],
        "Workflow": ["create-pr", "commit", "document", "sync-docs"],
        "Security": ["security-audit"],
    }
    
    for category, command_keys in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(len(command_keys))
        for idx, key in enumerate(command_keys):
            if key in generic_commands:
                cmd = generic_commands[key]
                with cols[idx]:
                    st.markdown(f"**/{key}**")
                    st.caption(cmd['description'])
        
        for key in command_keys:
            if key in generic_commands:
                cmd = generic_commands[key]
                with st.expander(f"📄 **{cmd['name']}** (`/{key}`)"):
                    st.markdown(f"**Description:** {cmd['description']}")
                    st.markdown(f"**Filename:** `.cursor/commands/{key}.md`")
                    st.markdown("---")
                    st.markdown("**Content:**")
                    st.code(cmd['content'], language="markdown")
                    
                    # Download button
                    st.download_button(
                        label=f"⬇️ Download {key}.md",
                        data=cmd['content'],
                        file_name=f"{key}.md",
                        mime="text/markdown",
                        key=f"download_{key}",
                    )
        
        st.markdown("---")
    
    # Bulk download section
    st.markdown("### 📦 Download All Commands")
    
    col_bulk1, col_bulk2 = st.columns([2, 1])
    
    with col_bulk1:
        st.markdown("Get all commands in one download with the **Starter Kit**:")
        st.markdown("**Commands included:**")
        cmd_list = ", ".join([f"`/{k}`" for k in generic_commands.keys()])
        st.markdown(cmd_list)
    
    with col_bulk2:
        # Generate and offer ZIP download
        zip_data = generate_starter_kit_zip()
        st.download_button(
            label="⬇️ Download Complete Starter Kit",
            data=zip_data,
            file_name="cursor-starter-kit.zip",
            mime="application/zip",
            key="download_starter_kit_commands",
            use_container_width=True,
        )
        st.caption("Includes all commands + rules")
    
    st.markdown("""
    **Setup instructions:**
    1. Download the Starter Kit ZIP above
    2. Extract and copy `.cursor/` folder to your project
    3. Commands are immediately available when you type `/` in chat
    """)


# ============================================================================
# TAB 5: RESOURCES
# ============================================================================

with tab_resources:
    st.markdown("## 🔗 Verified Resources & Examples")
    st.markdown("""
    Curated collection of **official documentation** and **community resources** 
    to help you master Cursor Rules and Commands.
    """)
    
    # Quick download reminder
    col_res_dl1, col_res_dl2 = st.columns([3, 1])
    with col_res_dl1:
        st.markdown("""
        <div class="info-card">
            <strong>🚀 Quick Start:</strong> Download the complete Starter Kit with all rules, commands, and AGENTS.md template.
        </div>
        """, unsafe_allow_html=True)
    with col_res_dl2:
        zip_data = generate_starter_kit_zip()
        st.download_button(
            label="⬇️ Starter Kit",
            data=zip_data,
            file_name="cursor-starter-kit.zip",
            mime="application/zip",
            key="download_starter_kit_resources",
            use_container_width=True,
        )
    
    st.markdown("---")
    
    # Official Resources
    st.markdown("### 📘 Official Cursor Documentation")
    st.markdown("""
    <div class="info-card">
        <strong>✅ Verified Source</strong>: These links point directly to Cursor's official documentation.
        Always refer to official docs for the most accurate and up-to-date information.
    </div>
    """, unsafe_allow_html=True)
    
    resources = get_external_resources()
    
    cols = st.columns(2)
    for idx, resource in enumerate(resources["official"]):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="rule-card">
                <h4>{resource['icon']} {resource['name']}</h4>
                <p>{resource['description']}</p>
                <a href="{resource['url']}" target="_blank">🔗 View Documentation →</a>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Community Resources
    st.markdown("### 🌐 Community Resources")
    st.markdown("""
    <div class="command-card">
        <strong>⚠️ Community Content</strong>: These are popular community-maintained resources. 
        While widely used and helpful, always verify rules work for your specific project.
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, resource in enumerate(resources["community"]):
        with cols[idx % 3]:
            stars_badge = f"⭐ {resource.get('stars', '')}" if resource.get('stars') else ""
            st.markdown(f"""
            <div style="background: rgba(88, 166, 255, 0.05); border-radius: 8px; padding: 1rem; margin: 0.5rem 0; min-height: 180px;">
                <h4>{resource['icon']} {resource['name']}</h4>
                <p style="font-size: 0.9rem;">{resource['description']}</p>
                <p>{stars_badge}</p>
                <a href="{resource['url']}" target="_blank">Visit →</a>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tech-specific rule examples
    st.markdown("### 🛠️ Tech-Specific Rule Examples")
    st.markdown("""
    Ready-to-use rule templates for popular frameworks and languages. 
    These are based on **community best practices** from cursor.directory and other sources.
    """)
    
    community_rules = get_community_rule_examples()
    
    # Tech selector
    tech_options = list(community_rules.keys())
    tech_labels = {k: v["name"] for k, v in community_rules.items()}
    
    cols = st.columns(len(tech_options))
    for idx, tech_key in enumerate(tech_options):
        with cols[idx]:
            if st.button(
                f"📦 {tech_labels[tech_key]}", 
                key=f"tech_{tech_key}",
                use_container_width=True
            ):
                st.session_state.selected_tech = tech_key
    
    # Display selected tech rule
    selected_tech = st.session_state.get("selected_tech", "react-typescript")
    if selected_tech in community_rules:
        rule = community_rules[selected_tech]
        
        st.markdown(f"#### {rule['name']} Rule")
        st.caption(f"Source: {rule['source']}")
        
        with st.expander("📄 View Full Rule", expanded=True):
            st.code(rule['content'], language="markdown")
        
        st.download_button(
            label=f"⬇️ Download {rule['name'].lower().replace(' ', '-')}-rule.md",
            data=rule['content'],
            file_name=f"{selected_tech}-rule.md",
            mime="text/markdown",
            key=f"download_tech_{selected_tech}",
        )
    
    st.markdown("---")
    
    # =========================================================================
    # AGENTS.MD SECTION
    # =========================================================================
    
    st.markdown("### 📄 AGENTS.md - Simple Alternative")
    st.markdown("""
    **AGENTS.md** is an open standard for AI agent guidance that works with multiple tools including Cursor, GitHub Copilot, and others.
    It's a single markdown file placed in your project root — simpler than managing multiple rule files.
    """)
    
    col_agents1, col_agents2 = st.columns([2, 1])
    
    with col_agents1:
        st.markdown("""
        <div class="info-card">
            <h4 style="margin-top: 0;">When to Use AGENTS.md</h4>
            <ul>
                <li>You want one file instead of multiple rules</li>
                <li>You use multiple AI tools (Cursor + Copilot)</li>
                <li>Your team prefers simpler documentation</li>
                <li>You're starting a new project and want quick setup</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_agents2:
        st.download_button(
            label="⬇️ Download AGENTS.md Template",
            data=STARTER_KIT_AGENTS_MD,
            file_name="AGENTS.md",
            mime="text/markdown",
            key="download_agents_md_resources",
            use_container_width=True,
        )
        st.caption("Place in your project root")
    
    with st.expander("📄 Preview AGENTS.md Template", expanded=False):
        st.code(STARTER_KIT_AGENTS_MD, language="markdown")
    
    st.markdown("---")
    
    # Advanced Topics section
    st.markdown("### 🔧 Advanced Topics")
    
    col_adv1, col_adv2 = st.columns(2)
    
    hooks_docs = get_hooks_documentation()
    
    with col_adv1:
        st.markdown("""
        <div class="info-card">
            <h4>🪝 Cursor Hooks</h4>
            <p>
                Observe, gate, and extend the agent loop with scripts at <strong>20+ lifecycle stages</strong>.
            </p>
            <p><strong>Examples:</strong></p>
            <ul>
                <li><code>beforeShellExecution</code> - Gate risky commands</li>
                <li><code>afterFileEdit</code> - Auto-format code</li>
                <li><code>preToolUse</code> / <code>postToolUse</code> - Wrap any tool call</li>
                <li><code>sessionStart</code> / <code>stop</code> - Setup & cleanup</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_adv2:
        st.markdown("""
        <div class="rule-card">
            <h4>🔄 Rule Self-Improvement</h4>
            <p>
                A meta-rule that keeps your rules <em>evolving</em> with your codebase.
            </p>
            <p><strong>Triggers updates when:</strong></p>
            <ul>
                <li>New patterns appear in 3+ files</li>
                <li>Code reviews repeat same feedback</li>
                <li>New libraries used consistently</li>
            </ul>
            <p style="font-size: 0.85rem; color: #6b7280;">
                <em>💡 Great for growing projects!</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hooks configuration example
    with st.expander("📄 **Hooks Configuration** (`hooks.json`)", expanded=False):
        st.markdown(hooks_docs['overview'])
        st.markdown(f"**Locations & priority:** {hooks_docs['location']}")
        st.markdown('Every `hooks.json` must declare `"version": 1`, and each hook name maps to a **list** of entries:')
        st.code(hooks_docs['example'], language="json")
        st.markdown(f"**Per-entry options:** {hooks_docs['options_summary']}")
        st.markdown("**All Available Hooks:**")
        for group_name, hooks in hooks_docs['hook_groups'].items():
            st.markdown(f"**{group_name}:**")
            for hook in hooks:
                st.markdown(f"- **`{hook['name']}`** — {hook['description']}")
        st.markdown("[📘 View Official Hooks Documentation](https://cursor.com/docs/agent/hooks)")
    
    # Rule Self-Improvement template download
    with st.expander("📄 **Download Rule Self-Improvement Template**", expanded=False):
        rule_self_improvement = """---
description: Guidelines for continuously improving Cursor rules based on emerging patterns
globs: []
alwaysApply: true
---

# Rule Self-Improvement Guidelines

## When to Add New Rules

- A pattern is used in **3+ files** consistently
- Common bugs could be prevented by standardization
- Code reviews repeatedly mention the same feedback
- New security or performance patterns emerge

## When to Update Existing Rules

- Better examples exist in the codebase
- Additional edge cases are discovered
- Implementation details have changed
- Related rules have been updated

## Pattern Recognition Examples

When you see repeated patterns like:

```python
# Repeated logging setup
from utils.logging import get_logger
logger = get_logger(__name__)
```

→ Add to `coding-standards.mdc` with standardized examples.

When you see repeated error handling:

```python
try:
    result = await operation()
except SpecificError as e:
    logger.error(f"Failed: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

→ Document in your API conventions rule.

## Rule Quality Checklist

- [ ] Rules are actionable and specific
- [ ] Examples come from actual codebase
- [ ] Patterns are consistently enforced
- [ ] No outdated references

## Continuous Improvement

- Monitor code review comments for patterns
- Update rules after major refactors
- Deprecate rules that no longer apply
- Cross-reference related rules

See @.cursor/rules/cursor-rules.mdc for formatting guidelines."""
        
        st.code(rule_self_improvement, language="markdown")
        st.download_button(
            label="⬇️ Download rule-self-improvement.mdc",
            data=rule_self_improvement,
            file_name="rule-self-improvement.mdc",
            mime="text/markdown",
            key="download_rule_self_improvement",
        )
    
    st.markdown("---")
    
    # Quick reference card
    st.markdown("### 📋 Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Rule File Location**
        ```
        .cursor/rules/
        ├── project-structure.mdc    # alwaysApply: true
        ├── coding-standards.mdc     # globs: ["**/*.py"]
        └── react-components.mdc     # globs: ["**/*.tsx"]
        ```
        """)
    
    with col2:
        st.markdown("""
        **Command File Location**
        ```
        .cursor/commands/
        ├── code-review.md          # /code-review
        ├── write-tests.md          # /write-tests
        └── debug.md                # /debug
        ```
        """)
    
    st.markdown("""
    **Key Frontmatter Fields**
    | Field | Type | Purpose |
    |-------|------|---------|
    | `description` | string | Summary shown in Cursor UI |
    | `globs` | array | File patterns to trigger rule |
    | `alwaysApply` | boolean | Always include this rule |
    """)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem 1rem;">
    <p style="font-size: 0.95rem; margin-bottom: 1rem; color: #6b7280;">
        Built with ❤️ using Streamlit
    </p>
    <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 1rem;">
        <a href="https://docs.cursor.com/context/rules-for-ai" target="_blank" 
           style="color: #2563eb; text-decoration: none; font-weight: 500;">📘 Rules Docs</a>
        <a href="https://cursor.com/docs/context/commands" target="_blank" 
           style="color: #16a34a; text-decoration: none; font-weight: 500;">📗 Commands Docs</a>
        <a href="https://cursor.directory" target="_blank" 
           style="color: #d97706; text-decoration: none; font-weight: 500;">🌐 cursor.directory</a>
        <a href="https://github.com/PatrickJS/awesome-cursorrules" target="_blank" 
           style="color: #7c3aed; text-decoration: none; font-weight: 500;">⭐ awesome-cursorrules</a>
    </div>
    <p style="font-size: 0.75rem; color: #9ca3af; max-width: 600px; margin: 0 auto;">
        Official examples from Cursor docs · Community examples from cursor.directory
    </p>
</div>
""", unsafe_allow_html=True)
