"""
PII REDACTOR - Detect and Mask Sensitive Information
Personal data ko [REDACTED] se replace karta hai
"""

import re
from typing import Dict, List

class PIIRedactor:
    """
    Detects and redacts personally identifiable information
    """
    
    # Enhanced patterns for sensitive data
    PATTERNS = {
        # SSN: 123-45-6789
        "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
        
        # Credit Card: Multiple formats
        "CREDIT_CARD": r'\b(?:\d{4}[-\s.]?){3}\d{4}\b|\b\d{16}\b',
        
        # Phone: Multiple formats (US)
        "PHONE_US": r'(?:\+\d{1,2}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        
        # Email
        "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        
        # IP Address
        "IP_ADDRESS": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        
        # Date of Birth (various formats)
        "DOB": r'\b\d{2}[/-]\d{2}[/-]\d{4}\b|\b\d{4}[/-]\d{2}[/-]\d{2}\b',
    }
    
    def redact(self, text: str) -> Dict:
        """
        Redact all PII from text
        
        Args:
            text: Input text potentially containing PII
            
        Returns:
            dict: {
                "original": str,
                "redacted": str,
                "findings": List[dict]
            }
        """
        redacted = text
        findings = []
        
        for category, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            if matches:
                findings.append({
                    "category": category,
                    "count": len(matches),
                    "examples": matches[:3]  # First 3 matches for debugging
                })
                
                # Replace with redaction marker
                redacted = re.sub(
                    pattern,
                    f"[REDACTED {category}]",
                    redacted,
                    flags=re.IGNORECASE
                )
        
        return {
            "original": text,
            "redacted": redacted,
            "findings": findings
        }