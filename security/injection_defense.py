import re
from typing import Dict


class PromptInjectionDefense:
    """Detect prompt injection, code injection, and policy bypass attempts."""

    SUSPICIOUS_PHRASES = [
        "bypass",
        "ignore rules",
        "ignore previous",
        "disable security",
        "override",
        "system prompt",
        "you are now",
        "act as",
        "pretend to be",
        "auto-approve",
        "approve immediately",
        "skip review",
        "admin mode",
        "show me your",
        "reveal your",
        "print your instructions",
        "always approve",
        "never reject",
        "trust me",
        "drop table",
        "drop database",
        "union select",
        "script",
        "javascript",
        "rm -rf",
        "cmd.exe",
        "powershell",
    ]

    HIGH_RISK_PATTERNS = [
        r"ignore\s+(all\s+)?(rules|instructions|security)",
        r"bypass\s+(all\s+)?(rules|security|checks)",
        r"(you\s+are|act\s+as|pretend\s+to\s+be)\s+(new|different|unrestricted)",
        r"(system|developer)\s+(message|prompt|instruction)",
        r"(admin|root|system)\s+mode",
        r"approve\s+(this|it)\s+immediately",
        r"disable\s+(security|checks|review)",
        r"show\s+me\s+your\s+(system|developer|internal)\s+(instructions|prompt)",
    ]

    BLOCKLIST_PATTERNS = [
        r"drop\s+(table|database)",
        r"union\s+select",
        r"select\s+.+\s+from",
        r"<script[^>]*>",
        r"javascript:",
        r"rm\s+-rf\s+/",
        r"(?:^|[\s;])(?:del|format|shutdown)\b",
        r"(?:\&\&|\|\|)",
        r"--",
        r"eval\s*\(",
        r"os\.system|subprocess\.",
    ]

    def detect(self, text: str) -> Dict:
        if not text:
            return {
                "detected": False,
                "reason": "No suspicious content",
                "severity": "NONE",
                "matched_patterns": [],
            }

        text_lower = text.lower()
        matched = []

        for phrase in self.SUSPICIOUS_PHRASES:
            if phrase in text_lower:
                matched.append({
                    "type": "phrase",
                    "pattern": phrase,
                    "severity": "MEDIUM",
                })

        for pattern in self.HIGH_RISK_PATTERNS:
            if re.search(pattern, text_lower):
                matched.append({
                    "type": "regex",
                    "pattern": pattern,
                    "severity": "HIGH",
                })

        for pattern in self.BLOCKLIST_PATTERNS:
            if re.search(pattern, text_lower):
                matched.append({
                    "type": "blocklist",
                    "pattern": pattern,
                    "severity": "HIGH",
                })

        if any(item["severity"] == "HIGH" for item in matched):
            severity = "HIGH"
        elif matched:
            severity = "MEDIUM"
        else:
            severity = "NONE"

        return {
            "detected": len(matched) > 0,
            "reason": f"Found {len(matched)} suspicious pattern(s)",
            "severity": severity,
            "matched_patterns": matched,
        }