"""
Content definitions and utilities for the Cursor Docs Explainer App.

This module contains structured data about Cursor Rules vs Commands,
and functions to load and process example files.
"""

import io
import os
import re
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================================
# CORE DEFINITIONS
# ============================================================================

RULES_VS_COMMANDS = {
    "rules": {
        "purpose": "Provide persistent context/guidance to Cursor AI",
        "location": ".cursor/rules/ (*.mdc files)",
        "triggered_by": "File patterns (globs) or alwaysApply flag",
        "format": ".mdc — Markdown with YAML frontmatter",
        "use_cases": ["Coding standards", "Project structure", "Architecture guidelines"],
        "invocation": "Automatic (based on file patterns or alwaysApply)",
        "scope": "Project-wide context that persists across sessions",
    },
    "commands": {
        "purpose": "Execute specific actions on demand",
        "location": ".cursor/commands/",
        "triggered_by": "/slash-command in Cursor chat",
        "format": "Plain markdown with instructions",
        "use_cases": ["Code reviews", "Start/stop services", "Generate boilerplate"],
        "invocation": "Manual (user types /command-name)",
        "scope": "Single action triggered by user",
    }
}

FRONTMATTER_FIELDS = {
    "description": {
        "type": "string",
        "required": False,
        "description": "A brief summary of what this rule does. Shown in the Cursor UI when browsing rules. Also used by the AI agent to decide whether to include the rule when activation is set to 'Agent Decision'.",
        "example": 'description: "Coding standards for Python files"',
    },
    "globs": {
        "type": "array of strings",
        "required": False,
        "description": "File patterns that trigger this rule. When you open a file matching these patterns, the rule is automatically included in the AI context.",
        "example": 'globs:\n  - "**/*.py"\n  - "src/**/*.ts"',
    },
    "alwaysApply": {
        "type": "boolean",
        "required": False,
        "description": "If true, this rule is always included in the AI context regardless of which files are open. Useful for project-wide guidelines. Keep these minimal to preserve context space.",
        "example": "alwaysApply: true",
    },
}

# Rule activation modes documentation
RULE_ACTIVATION_MODES = {
    "always": {
        "name": "Always Active",
        "trigger": "alwaysApply: true",
        "description": "Rule is always included in every AI interaction. Use sparingly for essential project-wide context.",
        "best_for": "Project structure, core conventions",
    },
    "glob": {
        "name": "Auto-Attached (Glob)",
        "trigger": "globs: [\"**/*.ts\"]",
        "description": "Rule automatically applies when files matching the pattern are referenced or open.",
        "best_for": "Language/framework-specific rules",
    },
    "manual": {
        "name": "Manual (@mention)",
        "trigger": "@rule-name in chat",
        "description": "User explicitly includes the rule by typing @rule-name in Cmd-K or chat.",
        "best_for": "Specialized rules needed occasionally",
    },
    "agent": {
        "name": "Agent Decision",
        "trigger": "description field + no globs/alwaysApply",
        "description": "AI decides whether to include the rule based on the description and current task.",
        "best_for": "Context-dependent guidelines",
    },
}

# Types of rules in Cursor
RULE_TYPES = {
    "project": {
        "name": "Project Rules",
        "location": ".cursor/rules/ (*.mdc)",
        "description": "Version-controlled rules scoped to your codebase. Must use the .mdc extension — plain .md files are ignored. Can be organized in subdirectories.",
        "icon": "📁",
    },
    "user": {
        "name": "User Rules",
        "location": "Cursor Settings > Rules",
        "description": "Global personal rules that apply to all your projects. Apply to Agent chat only (not Inline Edit or Tab). Not version-controlled.",
        "icon": "👤",
    },
    "team": {
        "name": "Team Rules",
        "location": "Cursor Dashboard (Team/Enterprise)",
        "description": "Organization-wide rules managed from the dashboard. Highest precedence (Team → Project → User), and admins can enforce them.",
        "icon": "👥",
    },
    "agents_md": {
        "name": "AGENTS.md",
        "location": "Project root (+ subdirectories)",
        "description": "Simple markdown alternative that works with Cursor, GitHub Copilot, and other AI tools. Nested AGENTS.md files are supported — the closest one wins.",
        "icon": "📄",
    },
}

# Hooks documentation
CURSOR_HOOKS = {
    "overview": (
        "Cursor Hooks let you observe, control, and extend the agent loop with custom scripts "
        "(or LLM-evaluated prompt checks) that run at defined lifecycle stages. "
        "Command hooks receive JSON on stdin; exit code 0 allows the action, exit code 2 denies it."
    ),
    "location": "`.cursor/hooks.json` (project) · `~/.cursor/hooks.json` (user) · Team/Enterprise via dashboard/MDM — priority: Enterprise → Team → Project → User",
    "options_summary": (
        "`command` (script to run) · `type` (`command`, or LLM-evaluated `prompt`) · "
        "`matcher` (filter by tool/command/subagent) · `timeout` · "
        "`failClosed` (block the action if the hook fails) · `loop_limit`"
    ),
    "hook_groups": {
        "Agent lifecycle": [
            {"name": "sessionStart", "description": "Agent session begins — inject setup or extra context"},
            {"name": "sessionEnd", "description": "Agent session ends"},
            {"name": "beforeSubmitPrompt", "description": "User submits a prompt — validate or block it"},
            {"name": "preToolUse", "description": "Before any tool call — observe or deny"},
            {"name": "postToolUse", "description": "After a tool call succeeds"},
            {"name": "postToolUseFailure", "description": "After a tool call fails"},
            {"name": "beforeShellExecution", "description": "Before shell commands — gate risky commands"},
            {"name": "afterShellExecution", "description": "After shell commands complete"},
            {"name": "beforeMCPExecution", "description": "Before MCP tool calls — control MCP access"},
            {"name": "afterMCPExecution", "description": "After MCP tool calls"},
            {"name": "beforeReadFile", "description": "Before the agent reads a file — protect sensitive content"},
            {"name": "afterFileEdit", "description": "After the agent edits a file — auto-format, lint"},
            {"name": "subagentStart", "description": "A subagent is launched"},
            {"name": "subagentStop", "description": "A subagent finishes"},
            {"name": "preCompact", "description": "Before context-window compaction"},
            {"name": "afterAgentResponse", "description": "After each agent response"},
            {"name": "afterAgentThought", "description": "After each agent reasoning step"},
            {"name": "stop", "description": "Agent loop completes — cleanup, notifications, analytics"},
        ],
        "Tab (inline completions)": [
            {"name": "beforeTabFileRead", "description": "Gate file access for Tab completions"},
            {"name": "afterTabFileEdit", "description": "Post-process edits made by Tab"},
        ],
        "App lifecycle": [
            {"name": "workspaceOpen", "description": "A workspace opens or its folders change"},
        ],
    },
    "example": """{
  "version": 1,
  "hooks": {
    "afterFileEdit": [
      { "command": "./.cursor/hooks/format.sh" }
    ],
    "beforeShellExecution": [
      { "command": "./.cursor/hooks/guard-shell.sh", "failClosed": true }
    ]
  }
}""",
}

# Common glob pattern presets for the interactive rule builder
COMMON_GLOB_PRESETS = {
    "Python": ["**/*.py"],
    "JavaScript": ["**/*.js", "**/*.jsx"],
    "TypeScript": ["**/*.ts", "**/*.tsx"],
    "React": ["**/*.tsx", "**/*.jsx", "src/components/**/*"],
    "Next.js": ["**/*.tsx", "**/*.ts", "app/**/*"],
    "Vue": ["**/*.vue", "**/*.ts"],
    "Go": ["**/*.go"],
    "Rust": ["**/*.rs"],
    "Java": ["**/*.java"],
    "C#": ["**/*.cs"],
    "Ruby": ["**/*.rb"],
    "PHP": ["**/*.php"],
    "Swift": ["**/*.swift"],
    "Kotlin": ["**/*.kt"],
    "Markdown": ["**/*.md"],
    "CSS/SCSS": ["**/*.css", "**/*.scss"],
    "HTML": ["**/*.html"],
    "Config Files": ["**/*.json", "**/*.yaml", "**/*.yml", "**/*.toml"],
}

# ============================================================================
# COMPARISON UTILITIES
# ============================================================================

def get_comparison_table() -> str:
    """Returns a markdown table comparing Rules vs Commands."""
    table = """
| Aspect | Rules | Commands |
|--------|-------|----------|
| **Purpose** | Provide persistent context/guidance | Execute specific actions on demand |
| **Location** | `.cursor/rules/` | `.cursor/commands/` |
| **Triggered By** | File patterns (globs) or `alwaysApply` | `/slash-command` in chat |
| **Format** | Markdown + YAML frontmatter | Plain markdown |
| **Invocation** | Automatic | Manual |
| **Scope** | Project-wide persistent context | Single action |
| **Use Cases** | Coding standards, architecture docs | Code reviews, generators |
"""
    return table.strip()


def get_comparison_data() -> List[Dict]:
    """Returns comparison data as a list of dicts for programmatic use."""
    aspects = ["purpose", "location", "triggered_by", "format", "invocation", "scope", "use_cases"]
    return [
        {
            "aspect": aspect.replace("_", " ").title(),
            "rules": RULES_VS_COMMANDS["rules"].get(aspect, ""),
            "commands": RULES_VS_COMMANDS["commands"].get(aspect, ""),
        }
        for aspect in aspects
    ]


def get_rule_frontmatter_docs() -> str:
    """Returns documentation for rule frontmatter fields."""
    docs = "## Rule Frontmatter Fields\n\n"
    for field, info in FRONTMATTER_FIELDS.items():
        docs += f"### `{field}`\n"
        docs += f"- **Type**: `{info['type']}`\n"
        docs += f"- **Required**: {'Yes' if info['required'] else 'No'}\n"
        docs += f"- **Description**: {info['description']}\n"
        docs += f"- **Example**:\n```yaml\n{info['example']}\n```\n\n"
    return docs


# ============================================================================
# FILE LOADING UTILITIES
# ============================================================================

def get_project_root() -> Path:
    """Returns the project root directory (same directory as this file)."""
    current_file = Path(__file__).resolve()
    return current_file.parent


def load_example_files() -> Dict[str, Dict[str, str]]:
    """
    Loads actual rule and command files from the .cursor/ directory.

    Returns:
        Dict with 'rules' and 'commands' keys, each containing
        filename -> content mappings.
    """
    project_root = get_project_root()

    result = {
        "rules": {},
        "commands": {},
    }

    # Load rules (.mdc is the required extension; .md kept for legacy files)
    rules_dir = project_root / ".cursor" / "rules"
    if rules_dir.exists():
        for file_path in sorted(list(rules_dir.glob("*.mdc")) + list(rules_dir.glob("*.md"))):
            result["rules"][file_path.name] = file_path.read_text(encoding="utf-8")
    
    # Load commands
    commands_dir = project_root / ".cursor" / "commands"
    if commands_dir.exists():
        for file_path in commands_dir.glob("*.md"):
            result["commands"][file_path.name] = file_path.read_text(encoding="utf-8")
    
    return result


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """
    Parses YAML frontmatter from markdown content.
    
    Args:
        content: Full markdown file content
        
    Returns:
        Tuple of (frontmatter_dict, body_content)
        frontmatter_dict is None if no frontmatter found
    """
    import yaml
    
    if not content.startswith("---"):
        return None, content
    
    # Find the closing ---
    end_index = content.find("---", 3)
    if end_index == -1:
        return None, content
    
    frontmatter_str = content[3:end_index].strip()
    body = content[end_index + 3:].strip()
    
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter, body
    except yaml.YAMLError:
        return None, content


def get_file_annotations(filename: str, content: str) -> List[Dict]:
    """
    Returns annotations explaining different parts of a file.
    
    Args:
        filename: Name of the file
        content: File content
        
    Returns:
        List of annotation dicts with 'line', 'text', and 'explanation' keys
    """
    annotations = []
    frontmatter, body = parse_frontmatter(content)
    
    if frontmatter:
        if "description" in frontmatter:
            annotations.append({
                "field": "description",
                "value": frontmatter["description"],
                "explanation": "Brief summary shown in Cursor's UI when browsing rules",
            })
        if "globs" in frontmatter:
            annotations.append({
                "field": "globs",
                "value": frontmatter["globs"],
                "explanation": "File patterns that trigger this rule (e.g., **/*.py matches all Python files)",
            })
        if "alwaysApply" in frontmatter:
            annotations.append({
                "field": "alwaysApply",
                "value": frontmatter["alwaysApply"],
                "explanation": "When true, rule is always active regardless of open files",
            })
    
    return annotations


# ============================================================================
# GENERATOR TEMPLATES
# ============================================================================

PROJECT_STRUCTURE_TEMPLATE = """---
description: {description}
globs: []
alwaysApply: true
---

# Project Structure: {project_name}

## Overview

{overview}

## Directory Layout

```
{directory_tree}
```

## Architecture

{architecture}

## Key Technologies

{technologies}

## Running the Application

{run_instructions}

## Environment Variables

{env_vars}
"""


def get_project_structure_template() -> str:
    """Returns the template for project-structure.mdc files."""
    return PROJECT_STRUCTURE_TEMPLATE


def generate_template_based_structure(
    project_name: str,
    tech_stack: List[str],
    main_files: str,
    architecture_notes: str,
) -> str:
    """
    Generates a project-structure.mdc using template-based approach.
    Used as fallback when no API key is available.
    """
    tech_list = "\n".join([f"- **{tech}**" for tech in tech_stack]) if tech_stack else "- Not specified"
    
    return PROJECT_STRUCTURE_TEMPLATE.format(
        description=f"Project structure and architecture overview for {project_name}",
        project_name=project_name,
        overview=f"A project built with {', '.join(tech_stack) if tech_stack else 'various technologies'}.",
        directory_tree=main_files if main_files else "src/\n├── main.py\n└── utils.py",
        architecture=architecture_notes if architecture_notes else "Describe your architecture here.",
        technologies=tech_list,
        run_instructions="```bash\n# Add your run instructions here\n```",
        env_vars="- Add your environment variables here",
    )


# ============================================================================
# RULE BUILDER & VALIDATOR
# ============================================================================

def build_rule_content(
    description: str,
    globs: List[str],
    always_apply: bool,
    title: str,
    body: str,
) -> str:
    """Builds a complete Cursor rule (.mdc) file from structured inputs."""
    lines = ["---"]
    lines.append(f"description: {description}" if description else "description: ")

    if globs:
        lines.append("globs:")
        for g in globs:
            lines.append(f'  - "{g}"')
    else:
        lines.append("globs: []")

    lines.append(f"alwaysApply: {'true' if always_apply else 'false'}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}" if title else "# Untitled Rule")
    lines.append("")
    lines.append(body if body else "")

    return "\n".join(lines)


def validate_rule(content: str) -> List[Dict]:
    """
    Validates a Cursor rule file and returns a list of findings.

    Each finding: {"level": "pass"|"warning"|"error"|"info", "message": str, "detail": str}
    """
    results = []

    stripped = content.strip()
    if not stripped:
        results.append({"level": "error", "message": "Empty content", "detail": "The rule file is empty."})
        return results

    # Check frontmatter delimiters
    if not stripped.startswith("---"):
        results.append({
            "level": "error",
            "message": "Missing frontmatter",
            "detail": "Rule files must start with `---` YAML frontmatter delimiters.",
        })
        return results

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        results.append({
            "level": "error",
            "message": "Invalid YAML frontmatter",
            "detail": "Could not parse the YAML between `---` delimiters. Check for syntax errors.",
        })
        return results

    # --- Field checks ---

    # description
    if frontmatter.get("description"):
        desc = frontmatter["description"]
        results.append({"level": "pass", "message": "Description present", "detail": f'"{desc}"'})
        if len(str(desc)) > 200:
            results.append({"level": "warning", "message": "Description is very long", "detail": "Keep descriptions concise for the Cursor UI."})
    else:
        results.append({
            "level": "warning",
            "message": "Missing description",
            "detail": "Without a description, the rule won't work with Agent Decision mode and won't show context in the Cursor UI.",
        })

    # globs
    has_globs = bool(frontmatter.get("globs"))
    always_apply = bool(frontmatter.get("alwaysApply"))

    if has_globs:
        globs = frontmatter["globs"]
        results.append({"level": "pass", "message": f"Glob patterns defined ({len(globs)})", "detail": ", ".join(str(g) for g in globs)})

    if always_apply:
        if has_globs:
            results.append({
                "level": "warning",
                "message": "alwaysApply + globs both set",
                "detail": "Globs are redundant when alwaysApply is true — the rule is always loaded regardless.",
            })
        else:
            results.append({"level": "pass", "message": "alwaysApply is true", "detail": "This rule will always be included in AI context."})

    if not has_globs and not always_apply:
        if frontmatter.get("description"):
            results.append({
                "level": "info",
                "message": "Agent Decision mode",
                "detail": "No globs or alwaysApply. The AI will decide whether to include this rule based on the description.",
            })
        else:
            results.append({
                "level": "warning",
                "message": "Rule may never activate",
                "detail": "No globs, no alwaysApply, and no description. This rule can only be included via @mention.",
            })

    # Unknown frontmatter fields
    known_fields = {"description", "globs", "alwaysApply"}
    unknown = set(frontmatter.keys()) - known_fields
    if unknown:
        results.append({
            "level": "warning",
            "message": f"Unknown frontmatter fields: {', '.join(unknown)}",
            "detail": "Cursor only recognizes: description, globs, alwaysApply.",
        })

    # --- Size checks ---
    lines = stripped.split("\n")
    total_lines = len(lines)

    if not body or not body.strip():
        results.append({"level": "warning", "message": "Empty rule body", "detail": "The rule has frontmatter but no content. Add actionable guidelines."})
    elif total_lines > 500:
        results.append({
            "level": "error",
            "message": f"File is too long ({total_lines} lines)",
            "detail": "Official Cursor guidance: keep rules under 500 lines. Split into multiple, composable rules.",
        })
    elif total_lines > 150:
        results.append({
            "level": "warning",
            "message": f"File is long ({total_lines} lines)",
            "detail": "Recommended: 50–150 lines (official maximum is 500). Consider splitting into multiple focused rules.",
        })
    elif total_lines >= 50:
        results.append({"level": "pass", "message": f"Good length ({total_lines} lines)", "detail": "Within the recommended 50–150 line range."})
    else:
        results.append({"level": "pass", "message": f"Concise ({total_lines} lines)", "detail": "Short and focused — good for alwaysApply rules."})

    if always_apply and total_lines > 100:
        results.append({
            "level": "warning",
            "message": "Long alwaysApply rule",
            "detail": "alwaysApply rules always consume context. Try to keep them under 100 lines.",
        })

    # Heading check
    if body and not body.strip().startswith("#"):
        results.append({"level": "info", "message": "No markdown heading", "detail": "Consider starting the body with a # heading for readability."})

    # Large pasted code blocks — official guidance is to reference files instead
    fence_lines = 0
    in_fence = False
    for line in (body or "").split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            fence_lines += 1
    if fence_lines > 40:
        results.append({
            "level": "warning",
            "message": f"Large code blocks ({fence_lines} lines inside fences)",
            "detail": "Reference project files (e.g. @src/utils/helpers.ts) instead of pasting long code samples — pasted code goes stale as the codebase evolves.",
        })

    # Token estimate (~1 token per 4 chars for English text)
    char_count = len(content)
    estimated_tokens = char_count // 4
    results.append({
        "level": "info",
        "message": f"Estimated size: ~{estimated_tokens} tokens",
        "detail": f"{char_count} chars, {total_lines} lines. Budget: ~2,000–3,000 tokens across all active rules.",
    })

    # Extension reminder — .mdc is required for project rules
    results.append({
        "level": "info",
        "message": "Save as a .mdc file",
        "detail": "Project rules must use the .mdc extension inside .cursor/rules/ — plain .md files there are ignored by Cursor (AGENTS.md in the project root is the markdown alternative).",
    })

    return results


# ============================================================================
# PROMPT TEMPLATES FOR AI-ASSISTED GENERATION
# ============================================================================

PROMPT_TEMPLATES = {
    "rules": [
        {
            "name": "Project Structure Rule",
            "description": "Generate a rule documenting your project's directory structure",
            "prompt": """@.cursor/rules/cursor-rules.mdc @Codebase

Create a project-structure.mdc rule documenting this project's architecture.

## REQUIRED SECTIONS:
1. **Overview** - What the project does (2-3 sentences max)
2. **Directory Layout** - Tree format with annotations
3. **Key Technologies** - Bullet list of frameworks/tools
4. **Running the App** - Essential commands only

## CONSTRAINTS:
- Maximum 80 lines total
- Directory tree: max 2 levels deep
- Do NOT list every file - use annotations like "# API routes"
- Bullet points over paragraphs
- No version numbers unless critical

## FRONTMATTER:
```yaml
---
description: Project structure for [name]
globs: []
alwaysApply: true
---
```""",
            "output_file": ".cursor/rules/project-structure.mdc",
        },
        {
            "name": "Coding Standards Rule",
            "description": "Generate coding standards based on your existing codebase",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.mdc

Create a coding-standards.mdc rule based on patterns found in this codebase.

## REQUIRED SECTIONS:
1. **Naming Conventions** - Variables, functions, classes, files
2. **Code Style** - Formatting patterns actually used
3. **Error Handling** - How errors are handled in this project
4. **Import Organization** - Import ordering and grouping

## CONSTRAINTS:
- Maximum 60 lines total
- Include 1-2 real code examples from THIS codebase
- Bullet points only, no lengthy explanations
- Focus on patterns that repeat across 3+ files

## FRONTMATTER:
```yaml
---
description: Coding standards for [project name]
globs: ["**/*.[ext]"]  # Use actual file extensions
alwaysApply: false
---
```""",
            "output_file": ".cursor/rules/coding-standards.mdc",
        },
        {
            "name": "Tech Stack Guidelines",
            "description": "Generate guidelines specific to your tech stack",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.mdc

Create a tech-stack.mdc rule with best practices for this project's technologies.

## REQUIRED SECTIONS:
1. **Core Technologies** - Main frameworks/libraries with versions
2. **Project Patterns** - How these technologies are used HERE
3. **Best Practices** - Framework-specific patterns to follow
4. **Anti-patterns** - What to avoid (if observed in codebase)

## CONSTRAINTS:
- Maximum 70 lines total
- Check package.json, requirements.txt, go.mod, Cargo.toml, etc.
- Include only technologies actively used
- 1 example per major technology max
- Bullet points over prose

## FRONTMATTER:
```yaml
---
description: Tech stack guidelines for [project name]
globs: []
alwaysApply: false
---
```""",
            "output_file": ".cursor/rules/tech-stack.mdc",
        },
        {
            "name": "API Design Rule",
            "description": "Document API patterns and conventions",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.mdc

Create an api-conventions.mdc rule documenting API patterns in this project.

## REQUIRED SECTIONS:
1. **Endpoint Patterns** - URL structure and naming
2. **Request/Response** - Standard formats used
3. **Error Handling** - Error response structure
4. **Authentication** - Auth patterns (if applicable)

## CONSTRAINTS:
- Maximum 60 lines total
- Include 1 real endpoint example from codebase
- Focus on patterns, not exhaustive documentation
- Skip sections not applicable to this project

## FRONTMATTER:
```yaml
---
description: API conventions for [project name]
globs: ["**/routes/**", "**/api/**", "**/controllers/**"]
alwaysApply: false
---
```""",
            "output_file": ".cursor/rules/api-conventions.mdc",
        },
        {
            "name": "Testing Conventions Rule",
            "description": "Document testing patterns and requirements",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.mdc

Create a testing-conventions.mdc rule based on test patterns in this project.

## REQUIRED SECTIONS:
1. **File Structure** - Test file naming and location
2. **Test Patterns** - How tests are structured
3. **Mocking** - Mocking patterns used
4. **Run Commands** - How to run tests

## CONSTRAINTS:
- Maximum 50 lines total
- Include 1 real test example from codebase
- Only document patterns that exist in the project
- Skip if no tests exist (note this instead)

## FRONTMATTER:
```yaml
---
description: Testing conventions for [project name]
globs: ["**/*test*", "**/*spec*", "**/tests/**"]
alwaysApply: false
---
```""",
            "output_file": ".cursor/rules/testing-conventions.mdc",
        },
        {
            "name": "Database & Models Rule",
            "description": "Document data models and database patterns",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.mdc

Create a data-models.mdc rule documenting database patterns in this project.

## REQUIRED SECTIONS:
1. **Data Models** - Key models/schemas overview
2. **Relationships** - How models relate
3. **Query Patterns** - Common query approaches
4. **Migrations** - How schema changes are handled

## CONSTRAINTS:
- Maximum 60 lines total
- Include 1 model example from codebase
- Focus on patterns, not full schema documentation
- Skip sections not applicable

## FRONTMATTER:
```yaml
---
description: Data modeling conventions for [project name]
globs: ["**/models/**", "**/schemas/**", "**/entities/**"]
alwaysApply: false
---
```""",
            "output_file": ".cursor/rules/data-models.mdc",
        },
        {
            "name": "Component Architecture Rule",
            "description": "Document UI component patterns (for frontend projects)",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.mdc

Create a component-architecture.mdc rule for UI patterns in this project.

## REQUIRED SECTIONS:
1. **Component Structure** - File organization and naming
2. **State Management** - How state is handled
3. **Styling** - CSS/styling approach used
4. **Props Patterns** - How props are typed and passed

## CONSTRAINTS:
- Maximum 60 lines total
- Include 1 component example from codebase
- Focus on patterns used consistently
- Skip if not a frontend project

## FRONTMATTER:
```yaml
---
description: Component architecture for [project name]
globs: ["**/components/**", "**/*.tsx", "**/*.jsx"]
alwaysApply: false
---
```""",
            "output_file": ".cursor/rules/component-architecture.mdc",
        },
        {
            "name": "Rule Self-Improvement",
            "description": "Generate a meta-rule that keeps your rules evolving with your codebase",
            "prompt": """@.cursor/rules/cursor-rules.mdc @Codebase

Create a rule-self-improvement.mdc that helps keep Cursor rules updated.

## REQUIRED SECTIONS:
1. **When to Add Rules** - Triggers for new rules
2. **When to Update** - Triggers for updating existing rules
3. **Pattern Examples** - 2-3 real patterns from THIS codebase
4. **Quality Checklist** - Rule quality criteria

## CONSTRAINTS:
- Maximum 70 lines total
- Use REAL examples from this codebase
- Reference existing rule files if any
- Focus on project-specific triggers

## FRONTMATTER:
```yaml
---
description: Guidelines for improving Cursor rules
globs: [".cursor/rules/*"]
alwaysApply: true
---
```""",
            "output_file": ".cursor/rules/rule-self-improvement.mdc",
        },
    ],
    "commands": [
        {
            "name": "Custom Code Review",
            "description": "Generate a code review command tailored to your project",
            "prompt": """@Codebase

Create a review.md command for code reviews tailored to THIS project.

## REQUIRED SECTIONS:
1. **Overview** - What this review checks (1-2 sentences)
2. **Project-Specific Checks** - Checklist based on THIS codebase patterns
3. **Common Issues** - Problems specific to this project's tech stack
4. **Output Format** - How to structure review feedback

## CONSTRAINTS:
- Maximum 60 lines total
- Focus on project-specific concerns, not generic best practices
- Include checklist items from actual patterns found
- Reference coding standards if they exist in .cursor/rules/

## FORMAT:
Plain markdown (commands don't use frontmatter)
Title should be: # Code Review""",
            "output_file": ".cursor/commands/review.md",
        },
        {
            "name": "Project-Specific Test Generator",
            "description": "Generate a test writing command matching your test patterns",
            "prompt": """@Codebase

Create a write-tests.md command for generating tests matching THIS project's style.

## REQUIRED SECTIONS:
1. **Overview** - What this command does (1-2 sentences)
2. **Test Structure** - How tests are organized in THIS project
3. **Instructions** - Steps for generating tests
4. **Example Format** - Template matching project's test style

## CONSTRAINTS:
- Maximum 50 lines total
- Match the exact testing framework used (Jest, pytest, etc.)
- Include file naming convention from this project
- Reference actual test file as example if found

## FORMAT:
Plain markdown (commands don't use frontmatter)
Title should be: # Write Tests""",
            "output_file": ".cursor/commands/write-tests.md",
        },
        {
            "name": "Feature Setup Command",
            "description": "Generate a feature scaffolding command for your project",
            "prompt": """@Codebase

Create a new-feature.md command for scaffolding new features in THIS project.

## REQUIRED SECTIONS:
1. **Overview** - What this command creates (1-2 sentences)
2. **Files to Create** - List of files based on project structure
3. **Boilerplate** - Templates matching project conventions
4. **Checklist** - Post-creation steps

## CONSTRAINTS:
- Maximum 60 lines total
- Base file structure on existing features/modules in project
- Use actual naming conventions from codebase
- Include only files relevant to this project's architecture

## FORMAT:
Plain markdown (commands don't use frontmatter)
Title should be: # New Feature Setup""",
            "output_file": ".cursor/commands/new-feature.md",
        },
    ],
}

# Generic commands that work for any project (from Cursor docs best practices)
# The flagship "apply rules to an existing project" prompt — one paste in Cursor
# chat generates the 3 essential rules from the user's own codebase.
# Shown on the Overview hero and in Build > AI Prompts.
STARTER_PACK_PROMPT = """@Codebase

I need to set up Cursor AI rules for this project. Create these 3 essential rule files:

## 1. .cursor/rules/cursor-rules.mdc (Meta Rule)
A concise guide for writing Cursor rules (~40 lines):
- Frontmatter fields (description, globs, alwaysApply)
- Best practices for rule writing
- Use alwaysApply: false, globs: [".cursor/rules/*"]

## 2. .cursor/rules/project-structure.mdc (Architecture)
Document this project's structure (~60-80 lines):
- Brief overview (2-3 sentences)
- Directory layout (2 levels deep max)
- Key technologies (bullet points)
- How to run the app
- Use alwaysApply: true

## 3. .cursor/rules/coding-standards.mdc (Conventions)
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

Output each file with a clear separator: --- FILE: path/to/file.mdc ---"""


GENERIC_COMMANDS = {
    "code-review-checklist": {
        "name": "Code Review Checklist",
        "description": "Comprehensive checklist for thorough code reviews",
        "content": """# Code Review Checklist

## Overview
Systematic review to ensure code quality, security, and maintainability.

## Review Steps

### 1. Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled appropriately
- [ ] Error handling is comprehensive
- [ ] No obvious bugs or logic errors

### 2. Code Quality
- [ ] Code is readable and well-structured
- [ ] Functions are small and focused (single responsibility)
- [ ] Variable and function names are descriptive
- [ ] No unnecessary code duplication (DRY)
- [ ] Follows project coding conventions

### 3. Security
- [ ] No obvious security vulnerabilities
- [ ] Input validation is present where needed
- [ ] Sensitive data is handled properly
- [ ] No hardcoded secrets or credentials
- [ ] SQL queries are parameterized (if applicable)

### 4. Performance
- [ ] No obvious performance issues
- [ ] Database queries are efficient
- [ ] No unnecessary work in loops
- [ ] Appropriate caching where needed

### 5. Testing
- [ ] Adequate test coverage
- [ ] Tests cover edge cases
- [ ] Tests are readable and maintainable

### 6. Documentation
- [ ] Complex logic is commented
- [ ] Public APIs are documented
- [ ] README updated if needed

Please review the selected code against this checklist and provide specific feedback.
""",
    },
    "write-tests": {
        "name": "Write Tests",
        "description": "Generate comprehensive tests for selected code",
        "content": """# Write Tests

## Overview
Generate comprehensive tests for the selected code, following testing best practices.

## Instructions

1. **Analyze the code** to understand its purpose and behavior
2. **Identify test cases**:
   - Happy path (normal operation)
   - Edge cases (boundary conditions)
   - Error cases (invalid inputs, failures)
   - Integration points (if applicable)

3. **Write tests** that are:
   - Descriptive (clear test names)
   - Independent (no test dependencies)
   - Repeatable (consistent results)
   - Fast (quick execution)

4. **Include**:
   - Unit tests for individual functions
   - Mock external dependencies
   - Assertions with clear error messages
   - Setup and teardown if needed

## Output Format
Provide complete, runnable test code with imports and any necessary setup.
""",
    },
    "security-audit": {
        "name": "Security Audit",
        "description": "Comprehensive security review of the codebase",
        "content": """# Security Audit

## Overview
Perform a comprehensive security review to identify vulnerabilities.

## Audit Checklist

### 1. Authentication & Authorization
- [ ] Authentication is properly implemented
- [ ] Authorization checks on all protected routes
- [ ] Session management is secure
- [ ] Password policies are enforced

### 2. Input Validation
- [ ] All user inputs are validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Path traversal prevention

### 3. Sensitive Data
- [ ] No hardcoded secrets or API keys
- [ ] Sensitive data encrypted at rest
- [ ] Secure transmission (HTTPS/TLS)
- [ ] Proper logging (no sensitive data logged)

### 4. Dependencies
- [ ] No known vulnerabilities in dependencies
- [ ] Dependencies are up to date
- [ ] Minimal dependency footprint

### 5. Error Handling
- [ ] Errors don't expose sensitive information
- [ ] Proper error logging
- [ ] Graceful failure handling

Please analyze the codebase for security issues and provide:
1. List of vulnerabilities found (severity: Critical/High/Medium/Low)
2. Specific code locations
3. Recommended fixes
""",
    },
    "create-pr": {
        "name": "Create PR Description",
        "description": "Generate a well-structured pull request description",
        "content": """# Create PR Description

## Overview
Generate a comprehensive pull request description based on the changes made.

## Instructions

Analyze the current changes (git diff) and create a PR description with:

### PR Title
A clear, concise title following the format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore

### Description Template

```markdown
## Summary
[Brief description of what this PR does]

## Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] All tests passing

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Related Issues
Closes #[issue_number]
```

Please generate a complete PR description based on the staged changes.
""",
    },
    "debug": {
        "name": "Debug Assistant",
        "description": "Systematic debugging help for issues",
        "content": """# Debug Assistant

## Overview
Systematic approach to debugging issues in the code.

## Debugging Process

### 1. Understand the Problem
- What is the expected behavior?
- What is the actual behavior?
- When did this start happening?
- Can it be reproduced consistently?

### 2. Gather Information
- Error messages and stack traces
- Relevant log output
- Input data that causes the issue
- Environment details (OS, versions, etc.)

### 3. Isolate the Issue
- Identify the smallest code path that reproduces the bug
- Check recent changes that might have introduced it
- Test with different inputs

### 4. Analyze
- Review the code logic step by step
- Check variable values at key points
- Verify assumptions about data types and values
- Look for common issues:
  - Null/undefined references
  - Off-by-one errors
  - Race conditions
  - Type mismatches

### 5. Fix and Verify
- Implement the fix
- Test the original failing case
- Test related functionality for regressions
- Add tests to prevent recurrence

Please describe the issue you're experiencing, and I'll help debug it systematically.
""",
    },
    "refactor": {
        "name": "Refactor Suggestions",
        "description": "Analyze code and suggest refactoring improvements",
        "content": """# Refactor Suggestions

## Overview
Analyze the selected code and suggest refactoring improvements.

## Analysis Criteria

### 1. Code Smells to Look For
- Long methods/functions (>20 lines)
- Deep nesting (>3 levels)
- Duplicate code
- Large classes/modules
- Long parameter lists
- Feature envy (using other object's data extensively)
- Dead code

### 2. Improvement Patterns
- Extract method/function
- Extract class/module
- Introduce parameter object
- Replace conditionals with polymorphism
- Simplify boolean expressions
- Use early returns

### 3. Clean Code Principles
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)

## Output Format
For each suggestion, provide:
1. What to change and why
2. Before and after code examples
3. Benefits of the change
""",
    },
    "document": {
        "name": "Generate Documentation",
        "description": "Generate documentation for code",
        "content": """# Generate Documentation

## Overview
Generate comprehensive documentation for the selected code.

## Documentation Types

### 1. Inline Documentation
- Function/method docstrings
- Complex logic comments
- TODO/FIXME annotations

### 2. API Documentation
- Endpoint descriptions
- Request/response formats
- Error codes and handling
- Authentication requirements
- Example requests

### 3. README Content
- Project overview
- Installation instructions
- Usage examples
- Configuration options
- Contributing guidelines

## Format Guidelines
- Use clear, concise language
- Include code examples
- Document parameters and return values
- Note any side effects
- Mention error conditions

Please generate appropriate documentation for the selected code.
""",
    },
    "explain": {
        "name": "Explain Code",
        "description": "Get a detailed explanation of complex code",
        "content": """# Explain Code

## Overview
Provide a detailed explanation of the selected code.

## Explanation Format

### 1. High-Level Summary
What does this code do overall? What problem does it solve?

### 2. Step-by-Step Breakdown
Walk through the code line by line or block by block:
- What each section does
- Why it's done that way
- Any important algorithms or patterns used

### 3. Key Concepts
Explain any:
- Design patterns used
- Language-specific features
- Framework conventions
- Algorithm complexity

### 4. Dependencies & Context
- What other code does this depend on?
- What depends on this code?
- Are there any side effects?

### 5. Potential Issues
- Edge cases to be aware of
- Performance considerations
- Maintainability concerns

Please explain the selected code in detail.
""",
    },
    "optimize": {
        "name": "Optimize Performance",
        "description": "Analyze and suggest performance optimizations",
        "content": """# Optimize Performance

## Overview
Analyze the code for performance issues and suggest optimizations.

## Analysis Areas

### 1. Time Complexity
- Algorithm efficiency (Big O)
- Unnecessary iterations
- Redundant calculations
- Opportunities for caching/memoization

### 2. Space Complexity
- Memory usage
- Data structure choices
- Temporary object creation
- Memory leaks

### 3. I/O Operations
- Database query efficiency
- Network request optimization
- File system operations
- Batching opportunities

### 4. Concurrency
- Parallelization opportunities
- Async/await usage
- Race conditions
- Resource contention

### 5. Language-Specific
- Framework best practices
- Built-in optimizations
- Profiling hotspots

## Output Format
For each optimization:
1. Current issue and impact
2. Suggested improvement
3. Before/after code
4. Expected performance gain
""",
    },
    "commit": {
        "name": "Generate Commit Message",
        "description": "Generate a conventional commit message",
        "content": """# Generate Commit Message

## Overview
Generate a well-formatted commit message following conventional commits.

## Format
```
type(scope): subject

body

footer
```

## Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Guidelines
- Subject: imperative mood, lowercase, no period, <50 chars
- Body: explain what and why (not how), wrap at 72 chars
- Footer: reference issues, breaking changes

## Examples
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with Google and GitHub providers.
Includes token refresh and secure storage.

Closes #123
```

```
fix(api): handle null response in user endpoint

The /api/users endpoint was crashing when the database returned null
for deleted users. Now returns 404 with appropriate message.

Fixes #456
```

Please analyze the staged changes and generate an appropriate commit message.
""",
    },
    "sync-docs": {
        "name": "Sync Documentation",
        "description": "Update README.md and project-structure.mdc together",
        "content": """# Sync Documentation

## Overview
Update both README.md and project-structure.mdc to reflect current project state.

## Instructions

Analyze the current project and update documentation:

### 1. Update `.cursor/rules/project-structure.mdc`
- Scan directory structure (2 levels deep)
- Update tech stack if dependencies changed
- Update run commands if changed
- Keep under 80 lines

### 2. Update `README.md`
- Sync project description with project-structure.mdc
- Update installation/setup instructions
- Update usage examples if needed
- Keep human-friendly (more detail than rules file)

### 3. Ensure Consistency
- Project name matches in both files
- Tech stack listed in both
- Run commands identical in both
- Directory structure aligned

## Output

Show a summary of changes made to each file.
""",
    },
}


def get_prompt_templates(category: str = "rules") -> List[Dict]:
    """Returns prompt templates for the specified category."""
    return PROMPT_TEMPLATES.get(category, [])


def get_generic_commands() -> Dict:
    """Returns all generic commands."""
    return GENERIC_COMMANDS


def get_generic_command(name: str) -> Optional[Dict]:
    """Returns a specific generic command by name."""
    return GENERIC_COMMANDS.get(name)


# ============================================================================
# EXTERNAL RESOURCES (VERIFIED)
# ============================================================================

EXTERNAL_RESOURCES = {
    "official": [
        {
            "name": "Cursor Rules Documentation",
            "url": "https://cursor.com/docs/rules",
            "description": "Official Cursor documentation on Rules - the authoritative source for project rules (.mdc), team rules, AGENTS.md, and frontmatter syntax.",
            "type": "Official",
            "icon": "📘",
        },
        {
            "name": "Cursor Skills Documentation",
            "url": "https://cursor.com/docs/skills",
            "description": "Official guide to Agent Skills — the successor to slash commands. Covers the SKILL.md format, bundled scripts/references, and /migrate-to-skills.",
            "type": "Official",
            "icon": "📗",
        },
        {
            "name": "Cursor Hooks Documentation",
            "url": "https://cursor.com/docs/hooks",
            "description": "Official guide on lifecycle hooks - run scripts before/after AI operations for formatting, validation, logging.",
            "type": "Official",
            "icon": "🪝",
        },
        {
            "name": "Cursor Subagents Documentation",
            "url": "https://cursor.com/docs/subagents",
            "description": "Official guide to subagents — delegated specialists with isolated context windows, built-in Explore/Bash/Browser agents, and cloud subagents.",
            "type": "Official",
            "icon": "🤖",
        },
        {
            "name": "Cursor Documentation Home",
            "url": "https://cursor.com/docs",
            "description": "The full Cursor documentation — quickstart, context management, agent features, and everything else.",
            "type": "Official",
            "icon": "📚",
        },
    ],
    "community": [
        {
            "name": "cursor.directory",
            "url": "https://cursor.directory",
            "description": "Community-curated collection of Cursor rules. Browse, search, and contribute rules for various frameworks and languages.",
            "type": "Community",
            "icon": "🌐",
            "stars": "Popular",
        },
        {
            "name": "awesome-cursorrules",
            "url": "https://github.com/PatrickJS/awesome-cursorrules",
            "description": "GitHub repository with curated list of cursor rules for different tech stacks and use cases.",
            "type": "Community",
            "icon": "⭐",
            "stars": "8k+",
        },
        {
            "name": "AGENTS.md",
            "url": "https://agentsmd.io/",
            "description": "Open standard for AI agent guidance. Single markdown file that works with Cursor, GitHub Copilot, and other AI tools.",
            "type": "Community",
            "icon": "📄",
            "stars": "New",
        },
        {
            "name": "Agent Skills Standard",
            "url": "https://agentskills.io",
            "description": "Open standard specification behind SKILL.md — portable skills that work across Cursor, Claude Code, and other AI agents.",
            "type": "Community",
            "icon": "🧩",
            "stars": "New",
        },
        {
            "name": "Cursor Forum",
            "url": "https://forum.cursor.com",
            "description": "Official Cursor community forum for discussions, tips, and rule sharing.",
            "type": "Community",
            "icon": "💬",
        },
    ],
}


def get_rule_types() -> Dict:
    """Returns the different types of Cursor rules."""
    return RULE_TYPES


def get_rule_activation_modes() -> Dict:
    """Returns rule activation modes documentation."""
    return RULE_ACTIVATION_MODES


def get_hooks_documentation() -> Dict:
    """Returns Cursor hooks documentation."""
    return CURSOR_HOOKS

# Tech-specific rule examples from community best practices
COMMUNITY_RULE_EXAMPLES = {
    "react-typescript": {
        "name": "React + TypeScript",
        "description": "Best practices for React projects with TypeScript",
        "source": "cursor.directory",
        "content": """---
description: React and TypeScript coding standards
globs:
  - "**/*.tsx"
  - "**/*.ts"
  - "src/components/**/*"
alwaysApply: false
---

# React + TypeScript Standards

## Component Guidelines
- Use functional components with hooks
- Prefer named exports for components
- Use TypeScript interfaces for props (not types)
- Implement proper error boundaries

## Naming Conventions
- Components: PascalCase (e.g., `UserProfile.tsx`)
- Hooks: camelCase with 'use' prefix (e.g., `useAuth.ts`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Constants: SCREAMING_SNAKE_CASE

## State Management
- Use React Query for server state
- Use Zustand or Context for client state
- Avoid prop drilling beyond 2 levels

## Code Style
- Destructure props in function signature
- Use optional chaining and nullish coalescing
- Prefer early returns for cleaner code
""",
    },
    "python-fastapi": {
        "name": "Python + FastAPI",
        "description": "Best practices for FastAPI backend projects",
        "source": "cursor.directory",
        "content": """---
description: Python FastAPI coding standards
globs:
  - "**/*.py"
  - "app/**/*"
  - "src/**/*"
alwaysApply: false
---

# Python FastAPI Standards

## Project Structure
- Use `app/` or `src/` as main package
- Separate routers, models, schemas, and services
- Use dependency injection for shared resources

## API Design
- Use Pydantic models for request/response schemas
- Implement proper HTTP status codes
- Use path operations decorators consistently
- Document endpoints with OpenAPI descriptions

## Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Prefer f-strings for string formatting
- Use async/await for I/O operations

## Error Handling
- Create custom exception classes
- Use HTTPException for API errors
- Implement global exception handlers
- Log errors with proper context
""",
    },
    "nextjs": {
        "name": "Next.js",
        "description": "Best practices for Next.js applications",
        "source": "cursor.directory",
        "content": """---
description: Next.js App Router best practices
globs:
  - "**/*.tsx"
  - "**/*.ts"
  - "app/**/*"
  - "components/**/*"
alwaysApply: false
---

# Next.js App Router Standards

## File Conventions
- Use `page.tsx` for route pages
- Use `layout.tsx` for shared layouts
- Use `loading.tsx` for loading states
- Use `error.tsx` for error boundaries

## Component Types
- Default to Server Components
- Use 'use client' only when needed
- Keep client components small and focused

## Data Fetching
- Fetch data in Server Components
- Use React Suspense for loading states
- Implement proper caching strategies
- Use server actions for mutations

## Performance
- Optimize images with next/image
- Use dynamic imports for code splitting
- Implement proper metadata for SEO
- Use Route Handlers for API endpoints
""",
    },
    "go": {
        "name": "Go",
        "description": "Best practices for Go projects",
        "source": "Community Best Practices",
        "content": """---
description: Go coding standards and best practices
globs:
  - "**/*.go"
alwaysApply: false
---

# Go Standards

## Project Structure
- Follow standard Go project layout
- Use `internal/` for private packages
- Use `pkg/` for public packages
- Keep `cmd/` for entry points

## Code Style
- Follow Effective Go guidelines
- Use gofmt for formatting
- Keep functions focused and small
- Prefer composition over inheritance

## Error Handling
- Always check errors explicitly
- Wrap errors with context
- Use custom error types when needed
- Avoid panic except for unrecoverable errors

## Testing
- Use table-driven tests
- Mock external dependencies
- Keep tests close to source files
- Use testify for assertions
""",
    },
    "rust": {
        "name": "Rust",
        "description": "Best practices for Rust projects",
        "source": "Community Best Practices",
        "content": """---
description: Rust coding standards and best practices
globs:
  - "**/*.rs"
  - "Cargo.toml"
alwaysApply: false
---

# Rust Standards

## Code Organization
- One module per file
- Use `mod.rs` for module directories
- Keep `lib.rs` clean with re-exports
- Separate binary and library code

## Error Handling
- Use Result<T, E> for recoverable errors
- Define custom error types with thiserror
- Use anyhow for application errors
- Avoid unwrap() in production code

## Memory & Performance
- Prefer borrowing over cloning
- Use iterators instead of loops where appropriate
- Leverage zero-cost abstractions
- Profile before optimizing

## Code Style
- Run clippy and fix warnings
- Use rustfmt for formatting
- Write descriptive variable names
- Document public APIs with rustdoc
""",
    },
}


def get_external_resources(category: str = "all") -> Dict:
    """Returns external resources filtered by category."""
    if category == "all":
        return EXTERNAL_RESOURCES
    return {category: EXTERNAL_RESOURCES.get(category, [])}


def get_community_rule_examples() -> Dict:
    """Returns community rule examples by tech stack."""
    return COMMUNITY_RULE_EXAMPLES


def get_community_rule_example(tech: str) -> Optional[Dict]:
    """Returns a specific community rule example."""
    return COMMUNITY_RULE_EXAMPLES.get(tech)


# ============================================================================
# QUICK TIPS CONTENT
# ============================================================================

QUICK_TIPS = {
    "rules": [
        "Use `alwaysApply: true` for project-wide context that should always be available",
        "Use specific globs like `src/components/**/*.tsx` to target specific file types",
        "Keep rules focused - one rule per concern",
        "Include code examples in rules to guide the AI's style",
    ],
    "commands": [
        "Name commands descriptively: `/generate-api-endpoint` not `/gen`",
        "Include clear instructions for what the command should do",
        "Commands are great for repetitive tasks with specific steps",
        "Use commands for actions, rules for context",
    ],
    "general": [
        "Rules = Persistent context, Commands = On-demand actions",
        "Test rules by opening a file that matches your glob pattern",
        "Commands appear in chat when you type `/`",
        "You can have multiple rules active at once based on open files",
    ],
}


def get_quick_tips(category: str = "general") -> List[str]:
    """Returns quick tips for the specified category."""
    return QUICK_TIPS.get(category, QUICK_TIPS["general"])


# ============================================================================
# STARTER KIT - ZIP DOWNLOAD CONTENT
# ============================================================================

STARTER_KIT_RULES = {
    "cursor-rules.mdc": """---
description: Guidelines for writing effective Cursor rules
globs: 
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

## Rule Activation Modes

Rules can be triggered through:
- **Always**: `alwaysApply: true` for persistent application
- **Glob Patterns**: Auto-apply when matching files are referenced
- **Manual**: Using `@rule-name` in Cmd-K or chat
- **Agent Decision**: AI determines relevance based on description

## Best Practices

- Save rules as `.mdc` files — plain `.md` files in `.cursor/rules/` are ignored by Cursor
- Keep rules focused on a single concern
- Use specific globs to avoid noise (e.g., `src/**/*.ts` not `**/*`)
- Write clear, actionable instructions
- Keep content concise (50-150 lines recommended, official maximum 500)
- Reference project files instead of pasting their content (pasted code goes stale)
- Include examples where helpful
- Multiple small focused rules > one giant rule
""",

    "project-structure.mdc": """---
description: Project structure and architecture overview
globs: []
alwaysApply: true
---

# Project Structure

## Overview

[Brief description of what this project does - 2-3 sentences]

## Directory Layout

```
project-root/
├── src/                    # Source code
│   ├── components/         # UI components
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── docs/                   # Documentation
└── .cursor/
    ├── rules/              # AI context rules
    └── commands/           # Slash commands
```

## Key Technologies

- [Technology 1] - Purpose
- [Technology 2] - Purpose
- [Technology 3] - Purpose

## Running the Application

```bash
# Install dependencies
[package manager] install

# Start development server
[command to run]

# Run tests
[test command]
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VAR_NAME` | Description | Yes/No |
""",

    "coding-standards.mdc": """---
description: Coding standards and conventions for this project
globs: []
alwaysApply: true
---

# Coding Standards

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | camelCase | `userName`, `isActive` |
| Functions | camelCase | `getUserById`, `calculateTotal` |
| Classes | PascalCase | `UserService`, `DataManager` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| Files | kebab-case | `user-service.ts`, `api-utils.py` |

## Code Style

- Use meaningful, descriptive names
- Keep functions small and focused (single responsibility)
- Prefer early returns for cleaner code
- Use optional chaining and nullish coalescing where available
- Destructure objects/arrays for cleaner access

## Error Handling

- Always handle errors explicitly
- Use try/catch for async operations
- Log errors with context (what operation failed, relevant IDs)
- Return meaningful error messages to users
- Never expose internal errors to end users

## Comments

- Write self-documenting code first
- Comment the "why", not the "what"
- Keep comments up-to-date with code changes
- Use TODO/FIXME for tracking issues
""",

    "git-conventions.mdc": """---
description: Git commit and branching conventions
globs:
  - ".git/**"
  - "*.md"
alwaysApply: false
---

# Git Conventions

## Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

## Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style (formatting, semicolons) |
| `refactor` | Code refactoring (no functional change) |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

## Guidelines

- Subject: imperative mood, lowercase, no period, <50 chars
- Body: explain what and why (not how), wrap at 72 chars
- Reference issues in footer: `Closes #123`

## Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Refactoring

## Examples

```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication with Google and GitHub providers.
Includes token refresh and secure storage.

Closes #123
```
""",

    "rule-self-improvement.mdc": """---
description: Guidelines for continuously improving Cursor rules
globs:
  - ".cursor/rules/*"
alwaysApply: false
---

# Rule Self-Improvement Guidelines

## When to Add New Rules

- A pattern is used in **3+ files** consistently
- Common bugs could be prevented by standardization
- Code reviews repeatedly mention the same feedback
- New security or performance patterns emerge
- New libraries/frameworks added to the project

## When to Update Existing Rules

- Better examples exist in the codebase
- Additional edge cases are discovered
- Implementation details have changed
- Related rules have been updated
- Outdated patterns need deprecation

## Rule Quality Checklist

- [ ] Rules are actionable and specific
- [ ] Examples come from actual codebase
- [ ] Patterns are consistently enforced
- [ ] No outdated references
- [ ] File size under 150 lines
- [ ] Clear, concise language

## Continuous Improvement

- Monitor code review comments for patterns
- Update rules after major refactors
- Deprecate rules that no longer apply
- Cross-reference related rules
- Keep `alwaysApply` rules minimal
""",
}

STARTER_KIT_COMMANDS = {
    "code-review-checklist.md": GENERIC_COMMANDS["code-review-checklist"]["content"],
    "write-tests.md": GENERIC_COMMANDS["write-tests"]["content"],
    "debug.md": GENERIC_COMMANDS["debug"]["content"],
    "explain.md": GENERIC_COMMANDS["explain"]["content"],
    "refactor.md": GENERIC_COMMANDS["refactor"]["content"],
    "security-audit.md": GENERIC_COMMANDS["security-audit"]["content"],
    "commit.md": GENERIC_COMMANDS["commit"]["content"],
    "create-pr.md": GENERIC_COMMANDS["create-pr"]["content"],
    "document.md": GENERIC_COMMANDS["document"]["content"],
    "optimize.md": GENERIC_COMMANDS["optimize"]["content"],
}

STARTER_KIT_AGENTS_MD = """# AGENTS.md

> Project-wide AI agent guidance for Cursor, GitHub Copilot, and other AI tools.

## Project Overview

[Brief description of the project - what it does, who it's for]

## Build & Run

```bash
# Install dependencies
[package manager] install

# Run development server
[dev command]

# Run tests
[test command]

# Build for production
[build command]
```

## Code Conventions

- **Language**: [Primary language]
- **Framework**: [Main framework]
- **Style Guide**: [Link or description]

## Architecture Notes

[Key architectural decisions and patterns used]

## Important Files

- `src/index.ts` - Entry point
- `src/config.ts` - Configuration
- [Other key files]

## Testing

- Test framework: [Jest/pytest/etc.]
- Run all tests: `[command]`
- Test location: `tests/` or `__tests__/`

## Common Tasks

### Adding a new feature
1. Create feature branch: `git checkout -b feature/name`
2. Implement in `src/`
3. Add tests in `tests/`
4. Submit PR

### Debugging
- Check logs in `[location]`
- Use `[debug command]` for verbose output

---

*This file provides context to AI coding assistants. Keep it updated!*
"""

STARTER_KIT_README = """# Cursor Starter Kit

Ready-to-use Cursor Rules, Skills, and Subagents for any project.

## Quick Setup

1. Copy the `.cursor/` folder to your project root
2. (Optional) Copy `AGENTS.md` to your project root
3. Customize `project-structure.mdc` with your project details
4. Type `/` in Cursor chat — your skills are ready!

## What's Included

### Rules (`.cursor/rules/`)

> **Note:** Rule files use the `.mdc` extension — this is required by Cursor.
> Plain `.md` files inside `.cursor/rules/` are silently ignored.

| Rule | Purpose |
|------|---------|
| `cursor-rules.mdc` | Guidelines for writing effective rules |
| `project-structure.mdc` | Project overview template (customize this!) |
| `coding-standards.mdc` | Generic coding conventions |
| `git-conventions.mdc` | Commit message and branch naming |
| `rule-self-improvement.mdc` | Guidelines for evolving rules |

### Skills (`.cursor/skills/`)

Skills are the successor to slash commands — same `/name` invocation, more capable.
Each lives in its own folder as `SKILL.md`.

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

These skills use `disable-model-invocation: true`, so they only run when you
explicitly type the `/name` — exactly like classic commands.

### Subagents (`.cursor/agents/`)

Specialized assistants the main agent can delegate to:

| Subagent | Purpose |
|----------|---------|
| `/verifier` | Read-only agent that double-checks finished work |
| `/code-reviewer` | Read-only reviewer for bugs, security & maintainability |
| `/test-writer` | Writes tests matching your project's conventions |

### Hooks example (`.cursor/hooks.json.example`)

A minimal, safe `hooks.json` starting point (auto-format after edits, gate risky
shell commands). To activate: rename it to `hooks.json` and create the scripts it
references — hooks run real code, so review before enabling.

### AGENTS.md

A simpler alternative to `.cursor/rules/` that works with multiple AI tools.
Place in your project root for project-wide AI guidance.

## Customization

1. **Edit `project-structure.mdc`** - Fill in your project details
2. **Edit `coding-standards.mdc`** - Adjust to your team's conventions
3. **Add tech-specific rules and skills** - Create them for your framework

## Learn More

- [Cursor Rules Documentation](https://cursor.com/docs/rules)
- [Cursor Skills Documentation](https://cursor.com/docs/skills)
- [Cursor Subagents Documentation](https://cursor.com/docs/subagents)
- [cursor.directory](https://cursor.directory) - Community rules

> **Note:** Legacy `.cursor/commands/` files still work in Cursor, but this kit ships
> the same 10 actions as Skills. If you need classic commands (e.g. for an older
> Cursor version), build a custom kit in the app and tick the Legacy Commands section.

---

Generated by [Cursor Kickstart](https://github.com/Youssefhossamm/cursor_rules_commands)
"""


def generate_starter_kit_zip() -> bytes:
    """
    Generates a ZIP file containing the complete Cursor starter kit:
    rules (.mdc), skills (successor to slash commands), subagent templates,
    a hooks.json example, AGENTS.md, and a README.

    Legacy .cursor/commands/ files are NOT included by default — the same 10
    actions ship as skills to avoid duplicate /name entries. Use the custom
    kit to include them instead.

    Returns:
        bytes: The ZIP file content as bytes
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add rules
        for filename, content in STARTER_KIT_RULES.items():
            zf.writestr(f"cursor-starter-kit/.cursor/rules/{filename}", content)

        # Add skills (successor to slash commands; same /name invocation)
        for skill_name, content in STARTER_KIT_SKILLS.items():
            zf.writestr(f"cursor-starter-kit/.cursor/skills/{skill_name}/SKILL.md", content)

        # Add subagent templates
        for filename, content in STARTER_KIT_SUBAGENTS.items():
            zf.writestr(f"cursor-starter-kit/.cursor/agents/{filename}", content)

        # Add hooks example (users rename to hooks.json to activate)
        zf.writestr("cursor-starter-kit/.cursor/hooks.json.example", STARTER_KIT_HOOKS_EXAMPLE)

        # Add AGENTS.md
        zf.writestr("cursor-starter-kit/AGENTS.md", STARTER_KIT_AGENTS_MD)

        # Add README
        zf.writestr("cursor-starter-kit/README.md", STARTER_KIT_README)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def get_starter_kit_options() -> Dict[str, Dict[str, str]]:
    """Returns starter kit items organized for the customizer UI."""
    rule_descriptions = {
        "cursor-rules.mdc": "Meta rule — guidelines for writing rules",
        "project-structure.mdc": "Project overview template (customize this!)",
        "coding-standards.mdc": "Generic coding conventions",
        "git-conventions.mdc": "Commit message and branch naming",
        "rule-self-improvement.mdc": "Guidelines for evolving rules",
    }
    command_descriptions = {}
    for name in STARTER_KIT_COMMANDS:
        cmd_key = name.replace(".md", "")
        command_descriptions[name] = GENERIC_COMMANDS.get(cmd_key, {}).get("description", "")

    skill_descriptions = {
        name: GENERIC_COMMANDS.get(name, {}).get("description", "")
        for name in STARTER_KIT_SKILLS
    }

    subagent_descriptions = {
        "verifier.md": "Read-only agent that double-checks finished work",
        "code-reviewer.md": "Read-only reviewer for bugs, security & maintainability",
        "test-writer.md": "Writes tests matching your project's conventions",
    }

    return {
        "rules": {name: rule_descriptions.get(name, "") for name in STARTER_KIT_RULES},
        "skills": skill_descriptions,
        "commands": command_descriptions,
        "subagents": {name: subagent_descriptions.get(name, "") for name in STARTER_KIT_SUBAGENTS},
    }


def generate_custom_starter_kit_zip(
    selected_rules: List[str],
    selected_commands: List[str],
    include_agents_md: bool = True,
    selected_skills: Optional[List[str]] = None,
    selected_subagents: Optional[List[str]] = None,
    include_hooks_example: bool = False,
) -> bytes:
    """Generates a ZIP file containing only the selected starter kit items."""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in selected_rules:
            if filename in STARTER_KIT_RULES:
                zf.writestr(f"cursor-starter-kit/.cursor/rules/{filename}", STARTER_KIT_RULES[filename])

        for skill_name in (selected_skills or []):
            if skill_name in STARTER_KIT_SKILLS:
                zf.writestr(f"cursor-starter-kit/.cursor/skills/{skill_name}/SKILL.md", STARTER_KIT_SKILLS[skill_name])

        for filename in selected_commands:
            if filename in STARTER_KIT_COMMANDS:
                zf.writestr(f"cursor-starter-kit/.cursor/commands/{filename}", STARTER_KIT_COMMANDS[filename])

        for filename in (selected_subagents or []):
            if filename in STARTER_KIT_SUBAGENTS:
                zf.writestr(f"cursor-starter-kit/.cursor/agents/{filename}", STARTER_KIT_SUBAGENTS[filename])

        if include_hooks_example:
            zf.writestr("cursor-starter-kit/.cursor/hooks.json.example", STARTER_KIT_HOOKS_EXAMPLE)

        if include_agents_md:
            zf.writestr("cursor-starter-kit/AGENTS.md", STARTER_KIT_AGENTS_MD)

        zf.writestr("cursor-starter-kit/README.md", STARTER_KIT_README)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def get_starter_kit_contents() -> Dict[str, Dict[str, str]]:
    """Returns the starter kit contents for display."""
    return {
        "rules": STARTER_KIT_RULES,
        "commands": STARTER_KIT_COMMANDS,
        "agents_md": STARTER_KIT_AGENTS_MD,
        "readme": STARTER_KIT_README,
    }


# ============================================================================
# SKILLS (the successor to slash commands — Cursor 2.4+)
# ============================================================================

SKILL_FRONTMATTER_FIELDS = {
    "name": {
        "type": "string",
        "required": True,
        "description": "Skill identifier — lowercase letters, numbers, and hyphens only. Must match the parent folder name. Invoked as /name.",
        "example": "name: deploy-checklist",
    },
    "description": {
        "type": "string",
        "required": True,
        "description": "What the skill does AND when to use it. The agent reads this to decide whether to invoke the skill automatically — invest in it.",
        "example": 'description: "How to safely deploy this app. Use when asked to deploy or release."',
    },
    "paths": {
        "type": "array of strings (or comma-separated string)",
        "required": False,
        "description": "Glob patterns restricting when the skill is surfaced to matching files. Preferred over the legacy 'globs' field. Unset = available everywhere.",
        "example": 'paths:\n  - "**/*.tsx"\n  - "packages/ui/**"',
    },
    "disable-model-invocation": {
        "type": "boolean",
        "required": False,
        "description": "When true, the agent never invokes the skill automatically — it only runs when you explicitly type /skill-name. This is how migrated slash commands behave.",
        "example": "disable-model-invocation: true",
    },
    "metadata": {
        "type": "key-value map",
        "required": False,
        "description": "Free-form custom metadata for additional context.",
        "example": "metadata:\n  team: platform",
    },
}

SKILLS_DOCS = {
    "overview": (
        "Skills are reusable sets of instructions that teach the Agent how to handle specific tasks — "
        "the successor to slash commands. Each skill is a folder containing a SKILL.md file (plus optional "
        "scripts, references, and assets). The agent invokes skills automatically when the description matches "
        "the task, or you trigger them explicitly with /skill-name."
    ),
    "locations": [
        (".cursor/skills/<skill-name>/", "Project-level (version-controlled)"),
        (".agents/skills/<skill-name>/", "Project-level, open-standard path"),
        ("~/.cursor/skills/<skill-name>/", "User-level — available in all projects"),
        ("~/.agents/skills/<skill-name>/", "User-level, open-standard path"),
        (".claude/skills/ · .codex/skills/", "Legacy compatibility (Claude Code, Codex)"),
    ],
    "bundled_dirs": [
        ("scripts/", "Executable code (Bash, Python, JavaScript...) the agent can run"),
        ("references/", "Extra documentation — loaded on demand to save context"),
        ("assets/", "Templates, images, configuration files, data"),
    ],
    "builtin_skills": [
        "/create-skill", "/migrate-to-skills", "/review", "/automate", "/canvas",
        "/sdk", "/shell", "/split-to-prs", "/worktree", "/best-of-n", "/in-cloud", "/babysit",
    ],
    "migration": (
        "Run the built-in /migrate-to-skills to modernize: slash commands become skills with "
        "disable-model-invocation: true (same /name behavior), and dynamic 'Agent Decision' rules become "
        "standard skills. Rules with alwaysApply or globs stay as rules."
    ),
    "example": """---
name: deploy-checklist
description: How to safely deploy this app to production. Use when asked to deploy or release.
---

# Deploy Checklist

1. Run the full test suite: `npm test`
2. Check for pending migrations: `npm run db:status`
3. Build: `npm run build`
4. Deploy: `npm run deploy -- --env production`
5. Verify the health endpoint returns 200 before announcing success.""",
}


def build_skill_content(
    name: str,
    description: str,
    paths: List[str],
    disable_model_invocation: bool,
    body: str,
) -> str:
    """Builds a complete SKILL.md file from structured inputs."""
    lines = ["---"]
    lines.append(f"name: {name}" if name else "name: ")
    lines.append(f"description: {description}" if description else "description: ")

    if paths:
        lines.append("paths:")
        for p in paths:
            lines.append(f'  - "{p}"')

    if disable_model_invocation:
        lines.append("disable-model-invocation: true")

    lines.append("---")
    lines.append("")
    lines.append(body if body else "")

    return "\n".join(lines)


def validate_skill(content: str, folder_name: Optional[str] = None) -> List[Dict]:
    """
    Validates a SKILL.md file and returns a list of findings.

    Each finding: {"level": "pass"|"warning"|"error"|"info", "message": str, "detail": str}
    """
    results = []

    stripped = content.strip()
    if not stripped:
        results.append({"level": "error", "message": "Empty content", "detail": "The SKILL.md file is empty."})
        return results

    if not stripped.startswith("---"):
        results.append({
            "level": "error",
            "message": "Missing frontmatter",
            "detail": "SKILL.md must start with `---` YAML frontmatter containing at least `name` and `description`.",
        })
        return results

    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        results.append({
            "level": "error",
            "message": "Invalid YAML frontmatter",
            "detail": "Could not parse the YAML between `---` delimiters. Check for syntax errors.",
        })
        return results

    # --- name ---
    name = frontmatter.get("name")
    if not name:
        results.append({
            "level": "error",
            "message": "Missing name",
            "detail": "Required. Lowercase letters, numbers, and hyphens; must match the skill's folder name.",
        })
    else:
        if re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(name)):
            results.append({"level": "pass", "message": f"Valid name: {name}", "detail": f"Invoked as /{name}."})
        else:
            results.append({
                "level": "error",
                "message": f"Invalid name format: {name}",
                "detail": "Use lowercase letters, numbers, and hyphens only (e.g. deploy-checklist).",
            })
        if folder_name and str(folder_name) != str(name):
            results.append({
                "level": "error",
                "message": "Name/folder mismatch",
                "detail": f"The skill folder is '{folder_name}' but name is '{name}' — they must match.",
            })

    # --- description ---
    desc = frontmatter.get("description")
    if not desc:
        results.append({
            "level": "error",
            "message": "Missing description",
            "detail": "Required. The agent uses it to decide when to invoke the skill automatically.",
        })
    else:
        results.append({"level": "pass", "message": "Description present", "detail": f'"{desc}"'})
        if len(str(desc)) < 20:
            results.append({
                "level": "warning",
                "message": "Description is very short",
                "detail": "Say what the skill does AND when to use it — this is what drives automatic invocation.",
            })
        elif len(str(desc)) > 300:
            results.append({
                "level": "warning",
                "message": "Description is very long",
                "detail": "Keep it focused; move detail into the skill body.",
            })

    # --- paths / legacy globs ---
    paths = frontmatter.get("paths")
    if paths is not None:
        if isinstance(paths, list) or isinstance(paths, str):
            shown = ", ".join(paths) if isinstance(paths, list) else paths
            results.append({"level": "pass", "message": "Path scoping defined", "detail": shown})
        else:
            results.append({
                "level": "warning",
                "message": "paths should be a list or comma-separated string",
                "detail": 'Example: paths: ["**/*.tsx", "packages/ui/**"]',
            })
    if frontmatter.get("globs") and not paths:
        results.append({
            "level": "info",
            "message": "Legacy 'globs' field",
            "detail": "Still supported, but 'paths' is preferred for new skills.",
        })

    # --- disable-model-invocation ---
    dmi = frontmatter.get("disable-model-invocation")
    if dmi is not None:
        if isinstance(dmi, bool):
            if dmi:
                results.append({
                    "level": "info",
                    "message": "Slash-only skill",
                    "detail": "disable-model-invocation: true — behaves like a classic /command; the agent won't invoke it automatically.",
                })
        else:
            results.append({
                "level": "warning",
                "message": "disable-model-invocation should be a boolean",
                "detail": "Use true or false (unquoted).",
            })

    # --- unknown fields ---
    known_fields = {"name", "description", "paths", "globs", "disable-model-invocation", "metadata", "license"}
    unknown = set(frontmatter.keys()) - known_fields
    if unknown:
        results.append({
            "level": "warning",
            "message": f"Unknown frontmatter fields: {', '.join(sorted(unknown))}",
            "detail": "Cursor recognizes: name, description, paths, disable-model-invocation, metadata (plus legacy globs).",
        })

    # --- body ---
    if not body or not body.strip():
        results.append({
            "level": "warning",
            "message": "Empty skill body",
            "detail": "Add the step-by-step instructions the agent should follow.",
        })

    # --- size ---
    char_count = len(content)
    estimated_tokens = char_count // 4
    results.append({
        "level": "info",
        "message": f"Estimated size: ~{estimated_tokens} tokens",
        "detail": f"{char_count} chars. Keep SKILL.md focused — move long reference material into a references/ folder; it loads on demand.",
    })

    # --- layout reminder ---
    results.append({
        "level": "info",
        "message": "File layout reminder",
        "detail": "Save as SKILL.md inside .cursor/skills/<name>/ — the folder name must match the 'name' field.",
    })

    return results


def _command_to_skill(cmd_key: str, cmd: Dict) -> str:
    """Converts a legacy command definition into a slash-only SKILL.md."""
    return (
        "---\n"
        f"name: {cmd_key}\n"
        f"description: {cmd['description']}\n"
        "disable-model-invocation: true\n"
        "---\n\n"
        + cmd["content"]
    )


# The 10 starter-kit commands, converted to skills (mirrors /migrate-to-skills output)
STARTER_KIT_SKILLS = {
    filename.replace(".md", ""): _command_to_skill(filename.replace(".md", ""), GENERIC_COMMANDS[filename.replace(".md", "")])
    for filename in STARTER_KIT_COMMANDS
}


# ============================================================================
# SUBAGENTS
# ============================================================================

SUBAGENTS_DOCS = {
    "overview": (
        "Subagents are specialized AI assistants the main agent can delegate to. Each runs in its own "
        "isolated context window — so long research or verbose output doesn't pollute your main conversation — "
        "and multiple subagents can run in parallel or in the background."
    ),
    "locations": [
        (".cursor/agents/", "Project-level (version-controlled, wins name conflicts)"),
        ("~/.cursor/agents/", "User-level — available in all projects"),
        (".claude/agents/ · .codex/agents/", "Legacy compatibility paths"),
    ],
    "frontmatter": [
        ("name", "Display identifier (lowercase, hyphenated). Defaults to the filename."),
        ("description", "When to delegate to this subagent — phrases like 'use proactively' encourage automatic delegation."),
        ("model", "'inherit' (default) or a specific model id, e.g. composer-2."),
        ("readonly", "true restricts file edits and state-changing commands — ideal for reviewers/verifiers."),
        ("is_background", "true runs the subagent in the background and returns immediately."),
    ],
    "builtins": [
        ("Explore", "Searches and analyzes the codebase with fast models — keeps noisy search output out of your context"),
        ("Bash", "Runs shell command sequences and isolates their verbose output"),
        ("Browser", "Controls a browser and filters noisy DOM snapshots"),
    ],
    "invocation": (
        "Invoke explicitly with /name (e.g. /verifier confirm the auth flow is complete), mention one naturally "
        "('use the verifier subagent'), or let the agent auto-delegate based on the description."
    ),
    "cloud": (
        "/in-cloud runs your next task as a cloud subagent on a dedicated VM; /babysit has a cloud agent "
        "iterate on a pull request remotely."
    ),
    "best_practices": [
        "Start with 2–3 focused subagents — one clear purpose each",
        "Invest in descriptions: they determine when auto-delegation happens",
        "Use readonly: true for anything that reviews or verifies",
        "Check .cursor/agents/ into git so the team shares them",
    ],
    "example": """---
name: verifier
description: Independently verifies that claimed work is complete. Use proactively after finishing a feature.
model: inherit
readonly: true
---

You are an independent verification agent...""",
}

STARTER_KIT_SUBAGENTS = {
    "verifier.md": """---
name: verifier
description: Independently verifies that claimed work is complete and correct. Use proactively after finishing a feature, fix, or refactor.
model: inherit
readonly: true
---

You are an independent verification agent. Your job is to check whether work
the main agent claims to have finished is actually complete and correct.

## Process

1. Restate the original requirement in one sentence.
2. Read the relevant code — do not trust summaries or commit messages.
3. Check each acceptance criterion explicitly: implemented? tested? edge cases handled?
4. Run the test suite or build if one exists and report the real output.
5. List anything missing, stubbed, or inconsistent with the requirement.

## Rules

- Be skeptical: your default assumption is that something was missed.
- Never modify files — you are read-only.
- Report findings as a checklist: verified / partial / missing.
- Quote file paths and line numbers as evidence for every claim.
""",

    "code-reviewer.md": """---
name: code-reviewer
description: Reviews code changes for bugs, security issues, and maintainability problems. Use after completing a change set or before opening a PR.
model: inherit
readonly: true
---

You are a thorough, constructive code reviewer.

## Review Checklist

- **Correctness**: logic errors, unhandled edge cases, error handling
- **Security**: injection risks, secrets in code, unsafe input handling
- **Performance**: obvious inefficiencies (N+1 queries, repeated work in loops)
- **Maintainability**: naming, duplication, dead code
- **Tests**: are the changes covered? do existing tests still make sense?

## Output

- Ordered list of findings, most severe first
- Each finding: file:line, what's wrong, why it matters, suggested fix
- End with a verdict: approve / approve with nits / request changes
""",

    "test-writer.md": """---
name: test-writer
description: Writes tests for recently changed code, matching the project's existing test framework and conventions. Use after implementing a feature.
model: inherit
---

You write tests that match this project's existing conventions.

## Process

1. Find the project's test framework and existing test patterns first.
2. Identify the changed code paths that need coverage.
3. Write tests: happy path, edge cases, error cases.
4. Run the tests and fix failures before finishing.

## Rules

- Mirror existing test style — naming, structure, fixtures.
- Prefer small, focused tests over one giant test.
- Never weaken an assertion just to make a test pass.
""",
}


# ============================================================================
# HOOKS EXAMPLE FILE (shipped in the starter kit as hooks.json.example)
# ============================================================================

STARTER_KIT_HOOKS_EXAMPLE = """{
  "version": 1,
  "hooks": {
    "afterFileEdit": [
      { "command": "./.cursor/hooks/format.sh" }
    ],
    "beforeShellExecution": [
      { "command": "./.cursor/hooks/guard-shell.sh", "failClosed": true }
    ]
  }
}
"""


# ============================================================================
# AI PROMPTS FOR SKILLS & SUBAGENTS
# ============================================================================

PROMPT_TEMPLATES["skills"] = [
    {
        "name": "Workflow Skill",
        "description": "Turn your project's deploy/release/setup workflow into a skill",
        "prompt": """@Codebase

Create a Cursor skill that teaches the agent this project's most important workflow
(deploy, release, environment setup — pick the one this project clearly has).

Requirements:
- File: .cursor/skills/<workflow-name>/SKILL.md
- Frontmatter: name (lowercase-hyphens, matching the folder), description that says
  what the skill does AND when to use it
- Body: numbered, copy-pasteable steps using this project's real commands
- Include verification steps (how to confirm each stage worked)
- Keep it under 60 lines; reference project files instead of pasting their content""",
        "output_file": ".cursor/skills/<workflow-name>/SKILL.md",
    },
    {
        "name": "Convert a Repeated Task",
        "description": "Describe any task you keep re-explaining — get a skill",
        "prompt": """@Codebase

I keep re-explaining this task to the agent: [DESCRIBE THE TASK HERE]

Create a Cursor skill for it:
- File: .cursor/skills/<task-name>/SKILL.md
- Frontmatter: name + a description that makes automatic invocation work
  (what it does AND when to use it)
- If the task should only run when I explicitly ask, add disable-model-invocation: true
- Body: precise instructions with this project's real conventions and commands
- Under 60 lines""",
        "output_file": ".cursor/skills/<task-name>/SKILL.md",
    },
]

PROMPT_TEMPLATES["subagents"] = [
    {
        "name": "Project Verifier Subagent",
        "description": "A read-only verifier tailored to this project's stack",
        "prompt": """@Codebase

Create a verifier subagent tailored to THIS project.

Requirements:
- File: .cursor/agents/verifier.md
- Frontmatter: name: verifier, readonly: true, model: inherit, and a description
  containing "use proactively after finishing a feature"
- Body: a verification process using this project's real test/build/lint commands,
  plus a checklist of the failure modes most likely in this stack
- Under 50 lines""",
        "output_file": ".cursor/agents/verifier.md",
    },
    {
        "name": "Domain Expert Subagent",
        "description": "A specialist for your project's trickiest subsystem",
        "prompt": """@Codebase

Find the trickiest / most complex subsystem in this project and create a subagent
that specializes in it.

Requirements:
- File: .cursor/agents/<subsystem>-expert.md
- Frontmatter: name, model: inherit, and a description that tells the main agent
  exactly when to delegate to this expert
- Body: the subsystem's key files, invariants that must not break, common pitfalls,
  and how to test changes safely
- Under 60 lines""",
        "output_file": ".cursor/agents/<subsystem>-expert.md",
    },
]


def get_skills_docs() -> Dict:
    """Returns the skills documentation data."""
    return SKILLS_DOCS


def get_subagents_docs() -> Dict:
    """Returns the subagents documentation data."""
    return SUBAGENTS_DOCS


def get_starter_kit_skills() -> Dict[str, str]:
    """Returns the starter kit skills (name -> SKILL.md content)."""
    return STARTER_KIT_SKILLS


def get_starter_kit_subagents() -> Dict[str, str]:
    """Returns the starter kit subagent templates (filename -> content)."""
    return STARTER_KIT_SUBAGENTS


# ============================================================================
# WHAT'S NEW IN CURSOR (release timeline the app's content is based on)
# ============================================================================

WHATS_NEW = [
    {
        "version": "3.10",
        "date": "June 2026",
        "highlights": "Team MCP marketplaces — admins configure MCP servers once and distribute them across cloud agents, the IDE, and the CLI; organization groups for access control.",
    },
    {
        "version": "3.9",
        "date": "June 2026",
        "highlights": "Cursor for iOS (public beta) with Remote Control of desktop agents; unified **Customize Cursor** page managing plugins, skills, MCPs, subagents, rules, commands, and hooks; marketplace leaderboard.",
    },
    {
        "version": "3.8",
        "date": "June 2026",
        "highlights": "Automations improvements: `/automate` skill, Slack emoji triggers, five new GitHub triggers, computer-use tool for producing demos.",
    },
    {
        "version": "3.7",
        "date": "June 2026",
        "highlights": "Cloud environment setup in under 10 minutes; cloud subagents via `/in-cloud`; `/babysit` for remote PR iteration; local-to-cloud session handoff.",
    },
    {
        "version": "3.5",
        "date": "May 2026",
        "highlights": "**Cloud Agents**: isolated VMs with full terminal, browser, and desktop access; work across multiple repos in parallel and report back to your IDE.",
    },
    {
        "version": "3.3",
        "date": "May 2026",
        "highlights": "Build-in-parallel subagents, pinned-skill pills, Composer 2.5 multi-file refactors at file-tree scale, native Jira integration.",
    },
    {
        "version": "3.0–3.1",
        "date": "April 2026",
        "highlights": "New interface for running many agents in parallel — worktrees, cloud, remote SSH; `/worktree` and `/best-of-n`; tiled Agents Window panes.",
    },
    {
        "version": "2.4",
        "date": "January 2026",
        "highlights": "**Skills** and **Subagents** introduced; `/migrate-to-skills` converts slash commands and dynamic rules; commands become legacy.",
    },
]


def get_whats_new() -> List[Dict]:
    """Returns the Cursor release timeline entries, newest first."""
    return WHATS_NEW
