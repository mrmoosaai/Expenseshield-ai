from agents.base_agent import BaseAgent
from security.shield import SecurityShield
from monitoring.logger import logger
from monitoring.audit_logger import audit_logger

class SecurityAgent(BaseAgent):
    """
    Security ka specialized agent
    """
    
    def __init__(self):
        super().__init__("Security Agent")
        self.shield = SecurityShield()
    
    async def process(self, event: dict) -> dict:
        logger.info(f"🛡️ {self.name} processing...")
        result = await self.shield.screen(event)
        
        # Log decision
        expense_id = event.get("expense_id", "unknown")
        amount = event.get("amount", 0)
        category = event.get("category", "General")
        
        if result.get("blocked"):
            audit_logger.log_decision(
                agent_name="Security Agent",
                expense_id=expense_id,
                decision="BLOCKED",
                reason=result.get("reason", "Security check failed"),
                amount=amount,
                category=category,
                details={
                    "severity": result.get("severity"),
                    "pii_findings": result.get("pii_findings", [])
                }
            )
        else:
            audit_logger.log_decision(
                agent_name="Security Agent",
                expense_id=expense_id,
                decision="APPROVED",
                reason="Security screening passed",
                amount=amount,
                category=category,
                details={
                    "pii_findings": result.get("pii_findings", [])
                }
            )
        
        return result
    
    def get_capabilities(self) -> list:
        return ["PII Redaction", "Injection Defense", "Security Screening"]
