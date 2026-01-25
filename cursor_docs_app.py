"""
Cursor Commands vs Rules Explainer App

A Streamlit application that educates developers on the differences between
Cursor Commands and Rules, provides real examples, AI prompts for generation,
and links to verified resources.

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
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Cursor Commands vs Rules",
    page_icon="📚",
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
    - [Cursor Quickstart](https://docs.cursor.com/get-started/quickstart)
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌐 Community")
    st.markdown("""
    - [cursor.directory](https://cursor.directory) - Browse rules
    - [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - GitHub collection
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
    ">📚 Cursor Commands vs Rules</h1>
    <p style="
        font-size: 1.1rem; 
        color: #6b7280; 
        max-width: 600px; 
        margin: 0 auto;
    ">Master Cursor's customization features to supercharge your AI-assisted coding</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab_overview, tab_examples, tab_prompts, tab_commands, tab_resources = st.tabs([
    "📊 Overview", 
    "📁 Live Examples",
    "✨ AI Prompts",
    "⚡ Commands",
    "🔗 Resources"
])

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
    
    st.info("💡 **Tip**: These prompts use `@Codebase` and `@.cursor/rules/...` references so Cursor AI can access your actual project files!")
    
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
            3. Paste the prompt and press Enter
            4. Save the AI's response to `{prompt_data['output_file']}`
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
            3. Paste the prompt and press Enter
            4. Save the AI's response to `{prompt_data['output_file']}`
            """)
    
    st.markdown("---")
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start: Set Up Your Project")
    st.markdown("""
    <div class="info-card">
        <h4>Recommended Setup Steps</h4>
        <ol>
            <li><strong>Create the cursor rules template:</strong><br/>
                First, create <code>.cursor/rules/cursor-rules.md</code> with basic frontmatter documentation</li>
            <li><strong>Generate project structure:</strong><br/>
                Use the "Project Structure Rule" prompt to document your codebase</li>
            <li><strong>Add tech-specific rules:</strong><br/>
                Use "Tech Stack Guidelines" or "Coding Standards" prompts</li>
            <li><strong>Set up common commands:</strong><br/>
                Copy generic commands from the "Generic Commands" tab</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Bootstrap prompt
    st.markdown("### 🎯 One-Shot Bootstrap Prompt")
    st.markdown("Use this single prompt to set up Cursor rules for a new project:")
    
    bootstrap_prompt = """@Codebase I want to set up Cursor AI rules for this project. Please:

1. Analyze the project structure, tech stack, and coding patterns
2. Create a comprehensive project-structure.md rule with:
   - Directory layout
   - Key files and their purposes
   - Architecture overview
   - Tech stack summary
3. Use YAML frontmatter with alwaysApply: true

Format the output as a complete .cursor/rules/project-structure.md file."""
    
    st.code(bootstrap_prompt, language="text")


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
        "Workflow": ["create-pr", "commit", "document"],
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
    st.markdown("Get all generic commands as a zip file to quickly set up your project.")
    
    # Create combined content for bulk info
    st.markdown("**Commands included:**")
    cmd_list = ", ".join([f"`/{k}`" for k in generic_commands.keys()])
    st.markdown(cmd_list)
    
    st.markdown("""
    **Setup instructions:**
    1. Create `.cursor/commands/` directory in your project
    2. Download individual commands above or copy the content
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
