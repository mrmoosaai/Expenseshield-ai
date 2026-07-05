---
name: json-to-pydantic
description: Converts JSON data snippets into Python Pydantic data models. Use this when user needs to create Pydantic models from JSON.
version: 1.0
author: Moosa AI
---

# JSON to Pydantic Converter Skill

## Goal
JSON data ko strongly-typed Python Pydantic models mein convert karna.

## Type Mapping Rules
- string → str
- number (integer) → int
- number (float) → float
- boolean → bool
- array → List[Type]
- null → Optional[Type]
- nested object → Separate class

## Instructions
1. JSON structure ko analyze karo
2. Har field ka type determine karo
3. Nested objects ke liye separate classes banao
4. Optional fields ko Optional[] mein wrap karo
5. PascalCase class names use karo
6. from pydantic import BaseModel add karo
7. from typing import List, Optional add karo

## Examples

### Example 1: Simple JSON

Input: {"user_id": 12345, "username": "moosa_ai"}

Output:
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: str

### Example 2: Nested JSON

Input: {"product": "Widget", "price": 19.99, "tags": ["new", "sale"]}

Output:
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product: str
    price: float
    tags: List[str]

## Constraints
- Raw JSON ko direct return mat karo
- Hamesha valid Pydantic syntax use karo
- Proper type hints lagao
- Class names ko descriptive rakho