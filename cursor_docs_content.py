"""
Content definitions and utilities for the Cursor Docs Explainer App.

This module contains structured data about Cursor Rules vs Commands,
and functions to load and process example files.
"""

import os
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
        "description": "A brief summary of what this rule does. Shown in the Cursor UI when browsing rules.",
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
        "description": "If true, this rule is always included in the AI context regardless of which files are open. Useful for project-wide guidelines.",
        "example": "alwaysApply: true",
    },
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
            "prompt": """@.cursor/rules/cursor-rules.md List all source files and folders in the project, and create a new cursor rule outlining the directory structure, important files, and their purposes. Use alwaysApply: true in the frontmatter.""",
            "output_file": ".cursor/rules/project-structure.md",
        },
        {
            "name": "Coding Standards Rule",
            "description": "Generate coding standards based on your existing codebase",
            "prompt": """@Codebase Analyze the coding patterns, naming conventions, and style used in this project. Create a cursor rule that documents these coding standards so the AI maintains consistency. Include examples from the actual codebase.""",
            "output_file": ".cursor/rules/coding-standards.md",
        },
        {
            "name": "Tech Stack Guidelines",
            "description": "Generate guidelines specific to your tech stack",
            "prompt": """@Codebase Identify all frameworks, libraries, and tools used in this project (check package.json, requirements.txt, go.mod, etc.). Create a cursor rule with best practices and patterns specific to this tech stack.""",
            "output_file": ".cursor/rules/tech-stack.md",
        },
        {
            "name": "API Design Rule",
            "description": "Document API patterns and conventions",
            "prompt": """@Codebase Analyze the API endpoints, request/response patterns, and error handling in this project. Create a cursor rule documenting the API design conventions to maintain consistency.""",
            "output_file": ".cursor/rules/api-conventions.md",
        },
        {
            "name": "Testing Conventions Rule",
            "description": "Document testing patterns and requirements",
            "prompt": """@Codebase Analyze the test files and testing patterns used in this project. Create a cursor rule documenting the testing conventions, including file naming, test structure, mocking patterns, and coverage expectations.""",
            "output_file": ".cursor/rules/testing-conventions.md",
        },
        {
            "name": "Database & Models Rule",
            "description": "Document data models and database patterns",
            "prompt": """@Codebase Analyze the database models, schemas, and data access patterns. Create a cursor rule documenting the data modeling conventions, relationships, and query patterns used in this project.""",
            "output_file": ".cursor/rules/data-models.md",
        },
        {
            "name": "Component Architecture Rule",
            "description": "Document UI component patterns (for frontend projects)",
            "prompt": """@Codebase Analyze the UI components, their structure, and patterns used. Create a cursor rule documenting component architecture, state management patterns, and styling conventions.""",
            "output_file": ".cursor/rules/component-architecture.md",
        },
        {
            "name": "Rule Self-Improvement",
            "description": "Generate a meta-rule that keeps your rules evolving with your codebase",
            "prompt": """@.cursor/rules/cursor-rules.md @Codebase

Create a rule-self-improvement.md that helps keep Cursor rules updated as this project evolves.

Analyze the codebase and include:

1. **Project-specific triggers** for when to add/update rules:
   - Common patterns unique to THIS project
   - Repeated code structures you found
   - Error handling patterns used here

2. **Pattern recognition examples** using ACTUAL code from this project:
   - Show 2-3 real repeated patterns you found
   - Explain which rule file they belong in

3. **Quality checklist** tailored to this project's tech stack

4. **Update triggers** specific to this project:
   - Key files that when changed should trigger rule review
   - Dependencies that affect coding patterns

CONSTRAINTS:
- Keep under 70 lines
- Use real examples from this codebase
- Reference existing rule files if any
- Use alwaysApply: true""",
            "output_file": ".cursor/rules/rule-self-improvement.md",
        },
    ],
    "commands": [
        {
            "name": "Custom Code Review",
            "description": "Generate a code review command tailored to your project",
            "prompt": """@Codebase Analyze the coding standards, patterns, and common issues in this project. Create a cursor command for code review that checks for project-specific concerns, not just generic best practices.""",
            "output_file": ".cursor/commands/review.md",
        },
        {
            "name": "Project-Specific Test Generator",
            "description": "Generate a test writing command matching your test patterns",
            "prompt": """@Codebase Analyze the testing framework, patterns, and conventions used. Create a cursor command that generates tests matching this project's exact style and structure.""",
            "output_file": ".cursor/commands/write-tests.md",
        },
        {
            "name": "Feature Setup Command",
            "description": "Generate a feature scaffolding command for your project",
            "prompt": """@Codebase Analyze the project structure and patterns for features/modules. Create a cursor command that helps set up new features following this project's conventions (files to create, boilerplate, etc.).""",
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
            "name": "Cursor Forum",
            "url": "https://forum.cursor.com",
            "description": "Official Cursor community forum for discussions, tips, and rule sharing.",
            "type": "Community",
            "icon": "💬",
        },
    ],
}

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
