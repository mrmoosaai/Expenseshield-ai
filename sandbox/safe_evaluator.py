"""
SAFE EVALUATOR
Code ko evaluate karke unsafe patterns detect karta hai
"""

import re
from typing import Dict, Any

class SafeEvaluator:
    """
    Simple evaluator to detect unsafe skill code
    """

    BLOCKED_PATTERNS = [
        r"\bimport\b",
        r"\bexec\b",
        r"\beval\b",
        r"\bos\b",
        r"\bsys\b",
        r"\bsubprocess\b",
        r"\bopen\b",
        r"\b__import__\b",
        r"\bexit\b",
        r"\bsystem\b",
        r"\brequests\b",
    ]

    def is_safe(self, code: str) -> bool:
        """
        Check karo ke code mein koi banned keyword ya pattern toh nahi hai
        """
        normalized_code = code.lower()
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, normalized_code):
                return False
        return True
