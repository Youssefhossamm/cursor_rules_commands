"""
Cursor Commands vs Rules Explainer App

A Streamlit application that educates developers on the differences between
Cursor Commands and Rules, provides real examples, and includes an interactive
generator for project-structure.md files.

Run with: streamlit run cursor_docs_app.py
"""

import streamlit as st
from pathlib import Path

# Import our modules
from cursor_docs_content import (
    RULES_VS_COMMANDS,
    FRONTMATTER_FIELDS,
    get_comparison_table,
    get_comparison_data,
    get_rule_frontmatter_docs,
    load_example_files,
    parse_frontmatter,
    get_file_annotations,
    get_project_structure_template,
    generate_template_based_structure,
    get_quick_tips,
    get_prompt_templates,
    get_generic_commands,
    get_external_resources,
    get_community_rule_examples,
)
from llm import (
    generate_project_structure_sync,
    check_api_keys,
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
    /* Import distinctive fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for theming */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --accent-cyan: #58a6ff;
        --accent-green: #3fb950;
        --accent-orange: #f0883e;
        --accent-purple: #a371f7;
        --accent-pink: #f778ba;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --border-color: #30363d;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Headers with Outfit font */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
    }
    
    h1 {
        background: linear-gradient(135deg, #58a6ff 0%, #a371f7 50%, #f778ba 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Code blocks with JetBrains Mono */
    code, .stCode, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Custom card styling */
    .info-card {
        background: linear-gradient(145deg, rgba(88, 166, 255, 0.1) 0%, rgba(163, 113, 247, 0.05) 100%);
        border: 1px solid rgba(88, 166, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .command-card {
        background: linear-gradient(145deg, rgba(240, 136, 62, 0.1) 0%, rgba(247, 120, 186, 0.05) 100%);
        border: 1px solid rgba(240, 136, 62, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .rule-card {
        background: linear-gradient(145deg, rgba(63, 185, 80, 0.1) 0%, rgba(88, 166, 255, 0.05) 100%);
        border: 1px solid rgba(63, 185, 80, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
    }
    
    /* Comparison table styling */
    .comparison-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Annotation boxes */
    .annotation {
        background: rgba(163, 113, 247, 0.1);
        border-left: 3px solid #a371f7;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
    }
    
    /* Quick tip styling */
    .quick-tip {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(88, 166, 255, 0.05);
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .quick-tip::before {
        content: "💡";
        font-size: 1.1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(13, 17, 23, 0.95) 0%, rgba(22, 27, 34, 0.95) 100%);
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(88, 166, 255, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
    }
    
    /* Copy button area */
    .copy-area {
        position: relative;
        background: #161b22;
        border-radius: 8px;
        padding: 1rem;
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
    explore real examples, and generate your own project structure files.
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
    
    st.markdown("---")
    
    # API Key status
    st.markdown("### 🔑 API Status")
    api_status = check_api_keys()
    if api_status["openai"]:
        st.success("✓ OpenAI API key found")
    else:
        st.warning("○ OpenAI API key not set")
    
    if api_status["anthropic"]:
        st.success("✓ Anthropic API key found")
    else:
        st.warning("○ Anthropic API key not set")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown("# Cursor Commands vs Rules")
st.markdown("*Master Cursor's customization features to supercharge your AI-assisted coding*")

# Create tabs
tab_overview, tab_examples, tab_prompts, tab_commands, tab_resources, tab_generator = st.tabs([
    "📊 Overview", 
    "📁 Live Examples",
    "✨ AI Prompts",
    "⚡ Commands",
    "🔗 Resources",
    "🛠️ Generator"
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
# TAB 6: STRUCTURE GENERATOR
# ============================================================================

with tab_generator:
    st.markdown("## Project Structure Generator")
    st.markdown("Generate a `project-structure.md` file for your own project.")
    
    # Check API availability
    api_status = check_api_keys()
    has_api = api_status["openai"] or api_status["anthropic"]
    
    if has_api:
        st.success("🤖 AI-powered generation available!")
        provider = st.radio(
            "Select AI Provider",
            options=["openai", "anthropic"],
            format_func=lambda x: "OpenAI (GPT-4o-mini)" if x == "openai" else "Anthropic (Claude 3.5 Sonnet)",
            horizontal=True,
            disabled=not has_api,
        )
        # Filter to only available providers
        if provider == "openai" and not api_status["openai"]:
            provider = "anthropic"
        elif provider == "anthropic" and not api_status["anthropic"]:
            provider = "openai"
    else:
        st.warning("⚠️ No API keys found. Using template-based generation.")
        st.info("Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` environment variables for AI-powered generation.")
        provider = None
    
    st.markdown("---")
    
    # Input form
    st.markdown("### Project Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "Project Name",
            placeholder="My Awesome Project",
            help="The name of your project",
        )
        
        tech_stack = st.text_input(
            "Tech Stack",
            placeholder="Python, FastAPI, PostgreSQL, React",
            help="Comma-separated list of technologies",
        )
    
    with col2:
        architecture_notes = st.text_area(
            "Architecture Notes",
            placeholder="Describe your project's architecture...\n\nE.g., 'Monolithic backend with REST API, React frontend with Redux for state management'",
            height=120,
            help="Brief description of your architecture",
        )
    
    main_files = st.text_area(
        "Main Files/Directory Structure",
        placeholder="""src/
├── main.py
├── api/
│   └── routes.py
├── models/
│   └── user.py
└── utils/
    └── helpers.py""",
        height=180,
        help="Paste your directory tree or list main files",
    )
    
    st.markdown("---")
    
    # Generate button
    if st.button("🚀 Generate project-structure.md", type="primary", use_container_width=True):
        if not project_name:
            st.error("Please enter a project name.")
        else:
            with st.spinner("Generating..."):
                if has_api and provider:
                    # AI-powered generation
                    try:
                        result = generate_project_structure_sync(
                            project_name=project_name,
                            tech_stack=tech_stack or "Not specified",
                            main_files=main_files or "Not provided",
                            architecture_notes=architecture_notes or "Not provided",
                            provider=provider,
                        )
                        if result:
                            st.session_state.generated_content = result
                        else:
                            st.error("Failed to generate. Check your API key.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        # Fall back to template
                        tech_list = [t.strip() for t in tech_stack.split(",")] if tech_stack else []
                        st.session_state.generated_content = generate_template_based_structure(
                            project_name=project_name,
                            tech_stack=tech_list,
                            main_files=main_files,
                            architecture_notes=architecture_notes,
                        )
                else:
                    # Template-based generation
                    tech_list = [t.strip() for t in tech_stack.split(",")] if tech_stack else []
                    st.session_state.generated_content = generate_template_based_structure(
                        project_name=project_name,
                        tech_stack=tech_list,
                        main_files=main_files,
                        architecture_notes=architecture_notes,
                    )
    
    # Display generated content
    if "generated_content" in st.session_state and st.session_state.generated_content:
        st.markdown("---")
        st.markdown("### Generated Content")
        
        # Preview
        with st.expander("📄 Preview", expanded=True):
            st.code(st.session_state.generated_content, language="markdown")
        
        # Copy instructions
        st.markdown("### 📋 How to Use")
        st.markdown("""
        1. Copy the content above
        2. Create a file at `.cursor/rules/project-structure.md` in your project
        3. Paste the content and save
        4. The rule will automatically apply to all files (due to `alwaysApply: true`)
        """)
        
        # Download button
        st.download_button(
            label="⬇️ Download project-structure.md",
            data=st.session_state.generated_content,
            file_name="project-structure.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8b949e; padding: 1rem;">
    <p>Built with ❤️ using Streamlit</p>
    <p style="font-size: 0.85rem;">
        📘 <a href="https://docs.cursor.com/context/rules-for-ai" target="_blank">Official Rules Docs</a> |
        📗 <a href="https://cursor.com/docs/context/commands" target="_blank">Official Commands Docs</a> |
        🌐 <a href="https://cursor.directory" target="_blank">cursor.directory</a> |
        ⭐ <a href="https://github.com/PatrickJS/awesome-cursorrules" target="_blank">awesome-cursorrules</a>
    </p>
    <p style="font-size: 0.75rem; margin-top: 0.5rem;">
        Examples marked "Official" are from Cursor's documentation. Community examples are from cursor.directory and awesome-cursorrules.
    </p>
</div>
""", unsafe_allow_html=True)
