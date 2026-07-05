"""Main agent entry point for the multi-agent expense system."""

from agents.orchestrator_agent import OrchestratorAgent
from monitoring.logger import logger
from monitoring.metrics import metrics
from monitoring.audit_logger import audit_logger
from database.repository import save_expense
from notifications.email_service import email_service
import config


class MultiAgentSystem:
    """Coordinates the full multi-agent workflow."""

    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        logger.info("🤖 Multi-Agent System initialized!")

    async def process(self, event: dict) -> dict:
        metrics.record_request()

        try:
            logger.info(f"🚀 Processing event: {event.get('description', '')[:50]}")

            result = await self.orchestrator.process(event)

            save_expense(event, result)

            amount = event.get("amount", 0)
            if amount >= config.AUTO_APPROVE_THRESHOLD:
                email_service.send_expense_notification(
                    amount=amount,
                    description=event.get("description", ""),
                    status=result.get("status", ""),
                    reason=str(result),
                )

            return result

        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            metrics.record_error()
            
            # Log error to audit trail
            audit_logger.log_decision(
                agent_name="MultiAgentSystem",
                expense_id=event.get("expense_id", "unknown"),
                decision="ERROR",
                reason=str(e)[:200],
                amount=event.get("amount", 0),
                category=event.get("category", "General"),
                details={"error": str(e)}
            )
            
            return {"status": "ERROR", "error": str(e)}


agent_system = MultiAgentSystem()
