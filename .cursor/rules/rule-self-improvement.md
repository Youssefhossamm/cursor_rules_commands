---
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

## Documentation Sync

Keep these files in sync when project structure changes:
- `README.md` ↔ `.cursor/rules/project-structure.md`

**Trigger sync when:**
- New directories or key files added
- Tech stack changes (new dependencies)
- Run/build commands change
- Architecture decisions made

Use `/sync-docs` command to update both files together.

See @.cursor/rules/cursor-rules.md for formatting guidelines.
