## Examples

### Example 1: Simple JSON

**Input:**
```json
{"user_id": 12345, "username": "moosa_ai"}
```

**Output:**
```python
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: str
```

### Example 2: Nested JSON

**Input:**
```json
{"product": "Widget", "price": 19.99, "tags": ["new", "sale"]}
```

**Output:**
```python
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product: str
    price: float
    tags: List[str]
```
