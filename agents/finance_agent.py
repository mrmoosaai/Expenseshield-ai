from agents.base_agent import BaseAgent
from monitoring.logger import logger
from monitoring.audit_logger import audit_logger

class FinanceAgent(BaseAgent):
    """
    Finance/Expense ka specialized agent
    """
    
    def __init__(self):
        super().__init__("Finance Agent")
        self.budget_limits = {
            "Engineering": 10000,
            "Marketing": 15000,
            "Sales": 8000
        }
    
    async def process(self, event: dict) -> dict:
        logger.info(f"💰 {self.name} processing...")
        
        amount = event.get("amount", 0)
        category = event.get("category", "General")
        expense_id = event.get("expense_id", "unknown")
        
        # Budget check
        if amount > 1000:
            result = {
                "status": "REQUIRES_APPROVAL",
                "reason": f"High value expense: ${amount}",
                "needs_manager": True
            }
            
            # Log decision
            audit_logger.log_decision(
                agent_name="Finance Agent",
                expense_id=expense_id,
                decision="REQUIRES_APPROVAL",
                reason=result["reason"],
                amount=amount,
                category=category,
                details={"budget_check": "High value"}
            )
            
            return result
        
        result = {
            "status": "APPROVED",
            "reason": "Within budget limits"
        }
        
        # Log decision
        audit_logger.log_decision(
            agent_name="Finance Agent",
            expense_id=expense_id,
            decision="APPROVED",
            reason=result["reason"],
            amount=amount,
            category=category,
            details={"budget_check": "Passed"}
        )
        
        return result
    
    def get_capabilities(self) -> list:
        return ["Budget Tracking", "Expense Validation", "Category Management"]
