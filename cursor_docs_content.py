"""
Content definitions and utilities for the Cursor Docs Explainer App.

This module contains structured data about Cursor Rules vs Commands,
and functions to load and process example files.
"""

import io
import os
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================================
# CORE DEFINITIONS
# ============================================================================

RULES_VS_COMMANDS = {
    "rules": {
        "purpose": "Provide persistent context/guidance to Cursor AI",
        "location": ".cursor/rules/",
        "triggered_by": "File patterns (globs) or alwaysApply flag",
        "format": "Markdown with YAML frontmatter",
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
        "location": ".cursor/rules/",
        "description": "Version-controlled rules scoped to your codebase. Shared with team via git.",
        "icon": "📁",
    },
    "user": {
        "name": "User Rules",
        "location": "Cursor Settings > Rules for AI",
        "description": "Global personal rules that apply to all your projects. Not version-controlled.",
        "icon": "👤",
    },
    "team": {
        "name": "Team Rules",
        "location": "Cursor Dashboard (Team/Enterprise)",
        "description": "Organization-wide rules managed from the Cursor dashboard. Requires Team or Enterprise plan.",
        "icon": "👥",
    },
    "agents_md": {
        "name": "AGENTS.md",
        "location": "Project root",
        "description": "Simple markdown file for project-wide AI guidance. Works with Cursor, GitHub Copilot, and other AI tools.",
        "icon": "📄",
    },
}

# Hooks documentation
CURSOR_HOOKS = {
    "overview": "Cursor Hooks allow you to observe, control, and extend the agent loop using custom scripts. They run before or after defined stages of the agent lifecycle.",
    "location": ".cursor/hooks.json",
    "available_hooks": [
        {
            "name": "beforeSubmitPrompt",
            "description": "Runs when the prompt is first submitted",
            "use_case": "Validate or modify prompts before sending",
        },
        {
            "name": "beforeShellExecution",
            "description": "Runs before any shell command executes",
            "use_case": "Gate risky commands, add logging",
        },
        {
            "name": "beforeMCPExecution",
            "description": "Runs before MCP (Model Context Protocol) execution",
            "use_case": "Control MCP tool access",
        },
        {
            "name": "beforeReadFile",
            "description": "Runs before a file is read",
            "use_case": "Scan for sensitive content, access control",
        },
        {
            "name": "afterFileEdit",
            "description": "Runs after a file is edited",
            "use_case": "Auto-format, lint, run tests",
        },
        {
            "name": "stop",
            "description": "Runs when the task is completed",
            "use_case": "Cleanup, notifications, analytics",
        },
    ],
    "example": """{
  "hooks": {
    "afterFileEdit": {
      "command": "prettier --write {filePath}"
    }
  }
}""",
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
    Loads actual .md files from the .cursor/ directory.
    
    Returns:
        Dict with 'rules' and 'commands' keys, each containing
        filename -> content mappings.
    """
    project_root = get_project_root()
    
    result = {
        "rules": {},
        "commands": {},
    }
    
    # Load rules
    rules_dir = project_root / ".cursor" / "rules"
    if rules_dir.exists():
        for file_path in rules_dir.glob("*.md"):
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
    """Returns the template for project-structure.md files."""
    return PROJECT_STRUCTURE_TEMPLATE


def generate_template_based_structure(
    project_name: str,
    tech_stack: List[str],
    main_files: str,
    architecture_notes: str,
) -> str:
    """
    Generates a project-structure.md using template-based approach.
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
# PROMPT TEMPLATES FOR AI-ASSISTED GENERATION
# ============================================================================

PROMPT_TEMPLATES = {
    "rules": [
        {
            "name": "Project Structure Rule",
            "description": "Generate a rule documenting your project's directory structure",
            "prompt": """@.cursor/rules/cursor-rules.md @Codebase

Create a project-structure.md rule documenting this project's architecture.

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
            "output_file": ".cursor/rules/project-structure.md",
        },
        {
            "name": "Coding Standards Rule",
            "description": "Generate coding standards based on your existing codebase",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.md

Create a coding-standards.md rule based on patterns found in this codebase.

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
            "output_file": ".cursor/rules/coding-standards.md",
        },
        {
            "name": "Tech Stack Guidelines",
            "description": "Generate guidelines specific to your tech stack",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.md

Create a tech-stack.md rule with best practices for this project's technologies.

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
            "output_file": ".cursor/rules/tech-stack.md",
        },
        {
            "name": "API Design Rule",
            "description": "Document API patterns and conventions",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.md

Create an api-conventions.md rule documenting API patterns in this project.

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
            "output_file": ".cursor/rules/api-conventions.md",
        },
        {
            "name": "Testing Conventions Rule",
            "description": "Document testing patterns and requirements",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.md

Create a testing-conventions.md rule based on test patterns in this project.

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
            "output_file": ".cursor/rules/testing-conventions.md",
        },
        {
            "name": "Database & Models Rule",
            "description": "Document data models and database patterns",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.md

Create a data-models.md rule documenting database patterns in this project.

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
            "output_file": ".cursor/rules/data-models.md",
        },
        {
            "name": "Component Architecture Rule",
            "description": "Document UI component patterns (for frontend projects)",
            "prompt": """@Codebase @.cursor/rules/cursor-rules.md

Create a component-architecture.md rule for UI patterns in this project.

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
            "output_file": ".cursor/rules/component-architecture.md",
        },
        {
            "name": "Rule Self-Improvement",
            "description": "Generate a meta-rule that keeps your rules evolving with your codebase",
            "prompt": """@.cursor/rules/cursor-rules.md @Codebase

Create a rule-self-improvement.md that helps keep Cursor rules updated.

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
            "output_file": ".cursor/rules/rule-self-improvement.md",
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
        "description": "Update README.md and project-structure.md together",
        "content": """# Sync Documentation

## Overview
Update both README.md and project-structure.md to reflect current project state.

## Instructions

Analyze the current project and update documentation:

### 1. Update `.cursor/rules/project-structure.md`
- Scan directory structure (2 levels deep)
- Update tech stack if dependencies changed
- Update run commands if changed
- Keep under 80 lines

### 2. Update `README.md`
- Sync project description with project-structure.md
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
            "url": "https://docs.cursor.com/context/rules-for-ai",
            "description": "Official Cursor documentation on Rules for AI - the authoritative source for project rules, global rules, and frontmatter syntax.",
            "type": "Official",
            "icon": "📘",
        },
        {
            "name": "Cursor Commands Documentation",
            "url": "https://cursor.com/docs/context/commands",
            "description": "Official guide on creating and using custom commands with /slash syntax. Includes team commands for Enterprise users.",
            "type": "Official",
            "icon": "📗",
        },
        {
            "name": "Cursor Hooks Documentation",
            "url": "https://cursor.com/docs/agent/hooks",
            "description": "Official guide on lifecycle hooks - run scripts before/after AI operations for formatting, validation, logging.",
            "type": "Official",
            "icon": "🪝",
        },
        {
            "name": "Cursor Quickstart Guide",
            "url": "https://docs.cursor.com/get-started/quickstart",
            "description": "Getting started with Cursor - covers basic setup and initial configuration.",
            "type": "Official",
            "icon": "🚀",
        },
        {
            "name": "Working with Context",
            "url": "https://docs.cursor.com/guides/working-with-context",
            "description": "Advanced guide on managing context in Cursor including @symbols, codebase indexing, and ignore files.",
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
    "cursor-rules.md": """---
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

- Keep rules focused on a single concern
- Use specific globs to avoid noise (e.g., `src/**/*.ts` not `**/*`)
- Write clear, actionable instructions
- Keep content concise (50-150 lines recommended)
- Include examples where helpful
- Multiple small focused rules > one giant rule
""",

    "project-structure.md": """---
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

    "coding-standards.md": """---
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

    "git-conventions.md": """---
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

    "rule-self-improvement.md": """---
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

Ready-to-use Cursor Rules and Commands for any project.

## Quick Setup

1. Copy the `.cursor/` folder to your project root
2. (Optional) Copy `AGENTS.md` to your project root
3. Customize `project-structure.md` with your project details
4. Start using commands by typing `/` in Cursor chat!

## What's Included

### Rules (`.cursor/rules/`)

| Rule | Purpose |
|------|---------|
| `cursor-rules.md` | Guidelines for writing effective rules |
| `project-structure.md` | Project overview template (customize this!) |
| `coding-standards.md` | Generic coding conventions |
| `git-conventions.md` | Commit message and branch naming |
| `rule-self-improvement.md` | Guidelines for evolving rules |

### Commands (`.cursor/commands/`)

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

### AGENTS.md

A simpler alternative to `.cursor/rules/` that works with multiple AI tools.
Place in your project root for project-wide AI guidance.

## Customization

1. **Edit `project-structure.md`** - Fill in your project details
2. **Edit `coding-standards.md`** - Adjust to your team's conventions
3. **Add tech-specific rules** - Create rules for your framework

## Learn More

- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
- [Cursor Commands Documentation](https://cursor.com/docs/context/commands)
- [cursor.directory](https://cursor.directory) - Community rules

---

Generated by [Cursor Kickstart](https://github.com/Youssefhossamm/cursor_rules_commands)
"""


def generate_starter_kit_zip() -> bytes:
    """
    Generates a ZIP file containing the complete Cursor starter kit.
    
    Returns:
        bytes: The ZIP file content as bytes
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add rules
        for filename, content in STARTER_KIT_RULES.items():
            zf.writestr(f"cursor-starter-kit/.cursor/rules/{filename}", content)
        
        # Add commands
        for filename, content in STARTER_KIT_COMMANDS.items():
            zf.writestr(f"cursor-starter-kit/.cursor/commands/{filename}", content)
        
        # Add AGENTS.md
        zf.writestr("cursor-starter-kit/AGENTS.md", STARTER_KIT_AGENTS_MD)
        
        # Add README
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
