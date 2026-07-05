---
name: license-header-adder
description: Adds standard open-source license headers to new source files. Use this when creating new code files that require copyright attribution.
version: 1.0
author: Moosa AI
---

# License Header Adder Skill

## Goal
Nayi code files mein automatic license header add karna.

## Supported Languages
- Python (.py) - Uses # comments
- JavaScript/TypeScript (.js, .ts) - Uses // comments
- Java/C/C++ (.java, .c, .cpp, .h) - Uses /* */ comments
- HTML (.html, .xml) - Uses <!-- --> comments

## Instructions
1. Pehle `resources/LICENSE_TEMPLATE.txt` file ko read karo
2. Target file ka extension check karo
3. Appropriate comment style use karo:
   - Python/Shell: `#` har line ke start mein
   - C-style: `/* ... */` block
   - HTML/XML: `<!-- ... -->`
4. License ko file ke start mein prepend karo
5. Original code ko intact rakho

## Examples

### Example 1: Python File
**Input:** New file `my_script.py`
**Output:**
```python
# Copyright (c) 2026 Moosa AI
# 
# Permission is hereby granted, free of charge...
# (rest of license)

def hello():
    print("Hello, World!")