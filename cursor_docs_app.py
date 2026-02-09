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
    get_comparison_table,
    load_example_files,
    parse_frontmatter,
    get_file_annotations,
    get_quick_tips,
    get_prompt_templates,
    get_generic_commands,
    get_external_resources,
    get_community_rule_examples,
    generate_starter_kit_zip,
    get_starter_kit_contents,
    get_rule_types,
    get_rule_activation_modes,
    get_hooks_documentation,
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
    - [Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
    - [Commands Documentation](https://cursor.com/docs/context/commands)
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
TAB_NAMES = ["📊 Overview", "📁 Live Examples", "✨ AI Prompts", "⚡ Commands", "🔗 Resources"]

# Create tabs
tab_overview, tab_examples, tab_prompts, tab_commands, tab_resources = st.tabs(TAB_NAMES)

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

with tab_overview:
    st.markdown("## Understanding the Difference")
    
    # Visual comparison cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="rule-card">
            <h3>📋 Rules</h3>
            <p><strong>Persistent context that guides the AI</strong></p>
            <ul>
                <li>Located in <code>.cursor/rules/</code></li>
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
                <li>Great for code reviews & generators</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =========================================================================
    # RULE TYPES SECTION
    # =========================================================================
    
    st.markdown("## Types of Cursor Rules")
    st.markdown("Cursor supports multiple ways to provide AI guidance:")
    
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
    
    st.markdown("---")
    
    # =========================================================================
    # RULE ACTIVATION MODES
    # =========================================================================
    
    st.markdown("## Rule Activation Modes")
    st.markdown("Rules can be triggered in 4 different ways:")
    
    activation_modes = get_rule_activation_modes()
    
    for mode_key, mode in activation_modes.items():
        with st.expander(f"**{mode['name']}** — `{mode['trigger']}`", expanded=False):
            st.markdown(f"**How it works:** {mode['description']}")
            st.markdown(f"**Best for:** {mode['best_for']}")
    
    st.info("💡 **Tip:** Use `@rule-name` in chat to manually include any rule. This works even for rules without `alwaysApply` or matching globs!")
    
    st.markdown("---")
    
    # Detailed comparison table
    st.markdown("## Side-by-Side Comparison")
    st.markdown(get_comparison_table())
    
    st.markdown("---")
    
    # Directory structure diagram
    st.markdown("## Directory Structure")
    st.code("""
.cursor/
├── rules/                          # Automatic context injection
│   ├── cursor-rules.md            # Guidelines for writing rules
│   └── project-structure.md       # Always-active project overview
│
└── commands/                       # Manual slash commands
    └── code-review-checklist.md   # Invoked with /code-review-checklist
    """, language="text")
    
    st.markdown("---")
    
    # Frontmatter documentation
    st.markdown("## Rule Frontmatter Fields")
    
    for field, info in FRONTMATTER_FIELDS.items():
        with st.expander(f"`{field}` - {info['type']}", expanded=False):
            st.markdown(f"**Description:** {info['description']}")
            st.markdown(f"**Required:** {'Yes' if info['required'] else 'No'}")
            st.markdown("**Example:**")
            st.code(info['example'], language="yaml")
    
    st.markdown("---")
    
    # When to use what
    st.markdown("## When to Use What?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Use **Rules** When...")
        st.markdown("""
        - You want context always available
        - Defining coding standards
        - Documenting project architecture
        - Setting up style guidelines
        - Creating language/framework-specific guidance
        """)
    
    with col2:
        st.markdown("### ✅ Use **Commands** When...")
        st.markdown("""
        - You need on-demand actions
        - Running code reviews
        - Generating boilerplate code
        - Performing specific tasks
        - Creating reusable workflows
        """)
    
    st.markdown("---")
    
    # =========================================================================
    # FILE SIZE GUIDELINES
    # =========================================================================
    
    st.markdown("## 📏 Rule File Size Guidelines")
    
    col_size1, col_size2 = st.columns([2, 1])
    
    with col_size1:
        st.markdown("""
        | Rule Type | Recommended Size | Notes |
        |-----------|------------------|-------|
        | Single rule file | **50-150 lines** | Keeps context focused |
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
    
    st.markdown("---")
    
    # =========================================================================
    # QUICK START SECTION - Interactive Getting Started Guide
    # =========================================================================
    
    st.markdown("## 🚀 Quick Start: Set Up Your Project")
    st.markdown("""
    <div class="info-card">
        <p style="margin-bottom: 1rem;"><strong>New to Cursor Rules & Commands?</strong> Get started instantly with our Starter Kit or follow the step-by-step guide below!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # STARTER KIT DOWNLOAD - Prominent Section
    # =========================================================================
    
    st.markdown("### 📦 One-Click Starter Kit")
    st.markdown("""
    Get everything you need to supercharge your AI-assisted coding in one download.
    """)
    
    col_kit1, col_kit2 = st.columns([2, 1])
    
    with col_kit1:
        st.markdown("""
        <div class="rule-card">
            <h4 style="margin-top: 0;">✨ What's Included:</h4>
            <ul style="margin-bottom: 0;">
                <li><strong>5 Essential Rules</strong> - Project structure, coding standards, git conventions & more</li>
                <li><strong>10 Ready-to-Use Commands</strong> - Code review, tests, debug, refactor, security audit...</li>
                <li><strong>AGENTS.md Template</strong> - Simpler alternative for AI guidance</li>
                <li><strong>Setup Instructions</strong> - Get running in seconds</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_kit2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <p style="font-size: 2.5rem; margin-bottom: 0.5rem;">📥</p>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">Works with any project</p>
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
    
    st.markdown("""
    **Quick Setup:**
    1. Download and extract the ZIP
    2. Copy the `.cursor/` folder to your project root
    3. Customize `project-structure.md` with your project details
    4. Start using `/commands` in Cursor chat!
    """)
    
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
    
    st.markdown("### 🛠️ Manual Setup (Step-by-Step)")
    
    # Step 1: Create directory structure
    st.markdown("### Step 1: Create the `.cursor/` Directory Structure")
    st.code("""
# In your project root, create:
.cursor/
├── rules/      # For persistent AI context
└── commands/   # For on-demand actions
    """, language="text")
    
    col_step1a, col_step1b = st.columns(2)
    with col_step1a:
        st.markdown("""
        <div class="rule-card">
            <strong>📋 Rules Folder</strong><br/>
            <code>.cursor/rules/</code><br/>
            <em>Markdown files with YAML frontmatter</em>
        </div>
        """, unsafe_allow_html=True)
    with col_step1b:
        st.markdown("""
        <div class="command-card">
            <strong>⚡ Commands Folder</strong><br/>
            <code>.cursor/commands/</code><br/>
            <em>Markdown files → /slash-commands</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Step 2: Create the META rule (cursor-rules.md)
    st.markdown("### Step 2: Create the Meta Rule (`cursor-rules.md`)")
    st.markdown("""
    **First, teach Cursor AI how to write rules!** This "meta rule" establishes the pattern for all future rules.
    """)
    
    with st.expander("📄 **Copy this cursor-rules.md template**", expanded=True):
        cursor_rules_template = """---
description: Guidelines for writing effective Cursor rules
globs: 
  - "**/*.md"
  - ".cursor/rules/*"
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

- Keep rules focused on a single concern
- Use specific globs to avoid noise
- Write clear, actionable instructions
- Keep content concise (avoid overwhelming detail)
- Include examples where helpful"""
        st.code(cursor_rules_template, language="markdown")
        st.download_button(
            label="⬇️ Download cursor-rules.md",
            data=cursor_rules_template,
            file_name="cursor-rules.md",
            mime="text/markdown",
            key="download_cursor_rules_template",
        )
    
    st.success("📍 **Save this to:** `.cursor/rules/cursor-rules.md`")
    
    # Step 3: Generate project-structure.md using AI
    st.markdown("### Step 3: Generate `project-structure.md` with AI")
    st.markdown("""
    Now use Cursor AI to create a rule documenting your project! The AI will follow the meta rule you just created.
    """)
    
    st.markdown("**Copy this prompt into Cursor Chat:**")
    
    bootstrap_prompt_quick = """@.cursor/rules/cursor-rules.md Analyze this project and create a project-structure.md rule.

CONSTRAINTS:
- Keep it under 80 lines total
- Focus on high-level architecture only
- List only main directories (max 2 levels deep)
- Summarize tech stack in bullet points
- Do NOT list every file - just key entry points

Include: Overview, Directory Layout, Tech Stack, How to Run."""
    
    st.code(bootstrap_prompt_quick, language="text")
    
    st.info("💡 **Why this works:** The `@.cursor/rules/cursor-rules.md` reference teaches the AI your rule format before it generates the new rule!")
    
    # Step 4: Add Ready-to-Use Commands
    st.markdown("### Step 4: Add Ready-to-Use Commands")
    st.markdown("""
    Commands are reusable actions triggered with `/command-name` in chat.
    """)
    
    col_cmd1, col_cmd2, col_cmd3 = st.columns(3)
    with col_cmd1:
        st.markdown("""
        <div class="command-card" style="min-height: 100px;">
            <strong>/code-review-checklist</strong><br/>
            <em>Systematic code review</em>
        </div>
        """, unsafe_allow_html=True)
    with col_cmd2:
        st.markdown("""
        <div class="command-card" style="min-height: 100px;">
            <strong>/write-tests</strong><br/>
            <em>Generate test cases</em>
        </div>
        """, unsafe_allow_html=True)
    with col_cmd3:
        st.markdown("""
        <div class="command-card" style="min-height: 100px;">
            <strong>/debug</strong><br/>
            <em>Systematic debugging</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.success("👉 **Go to the ⚡ Commands tab** to download ready-to-use commands!")
    
    # What's Next
    st.markdown("### 📚 What's Next?")
    st.markdown("""
    | Want to... | Go to... |
    |------------|----------|
    | See real examples from this project | **📁 Live Examples** tab |
    | Generate more rules (coding standards, API conventions) | **✨ AI Prompts** tab |
    | Download all ready-made commands | **⚡ Commands** tab |
    | Find rules for React, Python, Go, etc. | **🔗 Resources** tab |
    """)

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

with tab_prompts:
    st.markdown("## 🤖 AI-Powered Generation Prompts")
    st.markdown("""
    These prompts let you use **Cursor's AI** to generate rules and commands specific to your own project.
    Simply copy a prompt and paste it into Cursor chat - the AI will analyze your codebase and generate tailored content.
    """)
    
    st.warning("""
    ⚠️ **Before using these prompts:** Most prompts reference `@.cursor/rules/cursor-rules.md` to ensure consistent rule formatting. 
    If you haven't created this file yet, go to the **📊 Overview** tab → **Quick Start** section to download the template first!
    """)
    
    st.info("💡 **Tip**: These prompts use `@Codebase` and `@.cursor/rules/cursor-rules.md` references so Cursor AI can access your project files and follow your rule formatting guidelines.")
    
    st.markdown("---")
    
    # Rule generation prompts
    st.markdown("### 📋 Generate Cursor Rules")
    st.markdown("Copy these prompts to generate rules tailored to your project:")
    
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
    st.markdown("### ⚡ Generate Cursor Commands")
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
    
    st.markdown("---")
    
    # Bootstrap prompt - Most important prompt, kept prominently
    st.markdown("### 🎯 One-Shot Bootstrap Prompt")
    st.markdown("""
    Use this optimized prompt to generate a `project-structure.md` rule. 
    **Includes constraints** to keep output concise even for large projects.
    """)
    
    st.markdown("""
    <div class="info-card">
        <strong>⚠️ Important:</strong> First create <code>.cursor/rules/cursor-rules.md</code> (see Quick Start in Overview tab). 
        This prompt references it to ensure consistent formatting.
    </div>
    """, unsafe_allow_html=True)
    
    bootstrap_prompt = """@.cursor/rules/cursor-rules.md @Codebase

Create a project-structure.md rule for this project.

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
    
    st.markdown("---")
    
    # Alternative: Minimal prompt for experienced users
    st.markdown("### ⚡ Quick Version (for experienced users)")
    st.markdown("If you already have `cursor-rules.md`, use this minimal prompt:")
    
    minimal_prompt = """@.cursor/rules/cursor-rules.md Analyze this project. Create a concise project-structure.md rule (under 80 lines). Focus on: overview, directory layout (2 levels max), tech stack, run commands. Use alwaysApply: true."""
    
    st.code(minimal_prompt, language="text")
    
    st.markdown("---")
    
    # Starter Pack - Generate multiple essential rules
    st.markdown("### 🎁 Starter Pack Bootstrap")
    st.markdown("""
    **New to a project?** Generate all 3 essential rules in one go:
    """)
    
    col_pack1, col_pack2, col_pack3 = st.columns(3)
    with col_pack1:
        st.markdown("""
        <div class="rule-card" style="min-height: 80px; text-align: center;">
            <strong>📋 cursor-rules.md</strong><br/>
            <em>Meta rule</em>
        </div>
        """, unsafe_allow_html=True)
    with col_pack2:
        st.markdown("""
        <div class="rule-card" style="min-height: 80px; text-align: center;">
            <strong>🏗️ project-structure.md</strong><br/>
            <em>Architecture</em>
        </div>
        """, unsafe_allow_html=True)
    with col_pack3:
        st.markdown("""
        <div class="rule-card" style="min-height: 80px; text-align: center;">
            <strong>📝 coding-standards.md</strong><br/>
            <em>Conventions</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    starter_pack_prompt = """@Codebase

I need to set up Cursor AI rules for this project. Create these 3 essential rule files:

## 1. .cursor/rules/cursor-rules.md (Meta Rule)
A concise guide for writing Cursor rules (~40 lines):
- Frontmatter fields (description, globs, alwaysApply)
- Best practices for rule writing
- Use alwaysApply: false, globs: [".cursor/rules/*"]

## 2. .cursor/rules/project-structure.md (Architecture)
Document this project's structure (~60-80 lines):
- Brief overview (2-3 sentences)
- Directory layout (2 levels deep max)
- Key technologies (bullet points)
- How to run the app
- Use alwaysApply: true

## 3. .cursor/rules/coding-standards.md (Conventions)
Based on patterns found in this codebase (~50-60 lines):
- Naming conventions actually used
- Code style patterns observed
- Error handling approach
- Use globs for relevant file types (e.g., ["**/*.py"] or ["**/*.ts"])

CONSTRAINTS:
- Each file under 80 lines
- Use YAML frontmatter for all
- Include real examples from this codebase
- Be concise: bullet points > paragraphs

Output each file with a clear separator: --- FILE: path/to/file.md ---"""
    
    st.code(starter_pack_prompt, language="text")
    
    st.info("💡 **Tip:** After running this, you'll have a complete Cursor rules setup! The AI will analyze your codebase and create tailored rules.")


# ============================================================================
# TAB 4: GENERIC COMMANDS
# ============================================================================

with tab_commands:
    st.markdown("## ⚡ Ready-to-Use Commands")
    st.markdown("""
    These are **universal commands** that work for any project. Copy them directly 
    into your `.cursor/commands/` directory to use them immediately.
    """)
    
    st.markdown("""
    <div class="info-card">
        <strong>📖 Reference:</strong> Based on best practices from 
        <a href="https://cursor.com/docs/context/commands" target="_blank">Cursor's official documentation</a>
    </div>
    """, unsafe_allow_html=True)
    
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
                Run scripts <em>before</em> or <em>after</em> AI operations.
            </p>
            <p><strong>Available Hooks:</strong></p>
            <ul>
                <li><code>beforeSubmitPrompt</code> - Validate prompts</li>
                <li><code>beforeShellExecution</code> - Gate risky commands</li>
                <li><code>afterFileEdit</code> - Auto-format code</li>
                <li><code>stop</code> - Cleanup when done</li>
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
    with st.expander("📄 **Hooks Configuration Example** (`.cursor/hooks.json`)", expanded=False):
        st.markdown(f"**Location:** `{hooks_docs['location']}`")
        st.markdown(hooks_docs['overview'])
        st.code(hooks_docs['example'], language="json")
        st.markdown("**All Available Hooks:**")
        for hook in hooks_docs['available_hooks']:
            st.markdown(f"- **`{hook['name']}`** - {hook['description']}")
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

→ Add to `coding-standards.md` with standardized examples.

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

See @.cursor/rules/cursor-rules.md for formatting guidelines."""
        
        st.code(rule_self_improvement, language="markdown")
        st.download_button(
            label="⬇️ Download rule-self-improvement.md",
            data=rule_self_improvement,
            file_name="rule-self-improvement.md",
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
        ├── project-structure.md    # alwaysApply: true
        ├── coding-standards.md     # globs: ["**/*.py"]
        └── react-components.md     # globs: ["**/*.tsx"]
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
