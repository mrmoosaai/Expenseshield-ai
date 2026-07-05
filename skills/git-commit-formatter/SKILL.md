---
name: git-commit-formatter
description: Formats git commit messages according to Conventional Commits specification. Use this when user asks to commit changes or write a commit message.
version: 1.0
author: Moosa AI
---

# Git Commit Formatter Skill

## Goal
Git commit messages ko professional format mein convert karna.

## Format
Use this structure:
- `type(scope): subject`
- `type` must be one of the allowed types below
- `scope` is optional but recommended when relevant
- `subject` should be short, clear, and in imperative mood

## Allowed Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting (no code change)
- **refactor**: Code improvement
- **test**: Adding tests
- **chore**: Maintenance

## Instructions
1. Changes ko analyze karo
2. Primary type determine karo
3. Identify the specific module or feature related to the changes
4. Clear description likho (imperative mood)
5. 72 characters se kam rakho

## Examples

### Example 1: Bug Fix
**Input:** "fixed the login bug"  
**Output:** `fix(auth): resolve login timeout issue`

### Example 2: New Feature
**Input:** "added google login"  
**Output:** `feat(auth): implement google OAuth login`

### Example 3: Documentation
**Input:** "updated the readme"  
**Output:** `docs(readme): add installation instructions`

## Constraints
- ❌ Vague messages mat use karo ("update", "fix stuff")
- ✅ Imperative mood use karo ("add" not "added")
- ✅ Scope include karo jab applicable ho
- ⚠️ 72 characters se kam rakho