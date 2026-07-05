"""
SECURITY SHIELD - Pre-LLM Protection Layer
Screens all inputs before they reach the LLM
"""

from security.pii_redactor import PIIRedactor
from security.injection_defense import PromptInjectionDefense
from monitoring.logger import logger


class SecurityShield:
    """Main security orchestrator for pre-LLM protection."""

    def __init__(self):
        self.pii_redactor = PIIRedactor()
        self.injection_defense = PromptInjectionDefense()

    async def screen(self, event: dict) -> dict:
        logger.info("🛡️ Starting security screening...")

        description = event.get("description", "")

        injection_result = self.injection_defense.detect(description)
        if injection_result["detected"]:
            logger.warning(f"🚨 Prompt injection detected: {injection_result['reason']}")
            return {
                "blocked": True,
                "reason": f"Security threat: {injection_result['reason']}",
                "severity": injection_result.get("severity", "HIGH"),
            }

        redaction_result = self.pii_redactor.redact(description)
        if redaction_result["findings"]:
            logger.warning(f"🚨 Sensitive data detected: {redaction_result['findings']}")
            clean_event = event.copy()
            clean_event["description"] = redaction_result["redacted"]
            return {
                "blocked": True,
                "reason": "Security threat: Sensitive data detected in request",
                "severity": "HIGH",
                "redacted_event": clean_event,
                "pii_findings": redaction_result["findings"],
            }

        clean_event = event.copy()
        clean_event["description"] = redaction_result["redacted"]

        return {
            "blocked": False,
            "redacted_event": clean_event,
            "pii_findings": redaction_result["findings"],
        }