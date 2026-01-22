---
description: Guidelines for writing effective Cursor rules
globs: 
  - "**/*.md"
  - ".cursor/rules/*"
alwaysApply: false
---

# Cursor Rules Best Practices

## What Are Cursor Rules?

Cursor Rules provide persistent context and guidelines to the AI assistant. They help maintain consistency across your codebase by automatically including relevant information based on file patterns.

## Rule Structure

Every rule file should include:

1. **YAML Frontmatter** - Metadata that controls when and how the rule applies
2. **Markdown Content** - The actual instructions and guidelines

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
- Include examples where helpful
- Test rules by opening matching files
