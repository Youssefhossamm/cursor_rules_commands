# Sync Documentation

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

## What to Check

```
README.md                          project-structure.md
─────────────────────────────────────────────────────────
Project description        ←→     Overview section
Installation steps         ←→     Running the Application
Tech stack / Dependencies  ←→     Key Technologies
Directory overview         ←→     Directory Layout
```

## Output

Show a summary of changes made to each file:
- Files modified
- Sections updated
- Any inconsistencies found and fixed
