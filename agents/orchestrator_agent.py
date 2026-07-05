from agents.base_agent import BaseAgent
from agents.security_agent import SecurityAgent
from agents.finance_agent import FinanceAgent
from agents.skill_agent import SkillAgent
from monitoring.logger import logger
from monitoring.audit_logger import audit_logger
import uuid

class OrchestratorAgent(BaseAgent):
    """
    Master agent - sab agents ko coordinate karta hai
    """
    
    def __init__(self):
        super().__init__("Orchestrator Agent")
        
        # Sab specialized agents
        self.security_agent = SecurityAgent()
        self.finance_agent = FinanceAgent()
        self.skill_agent = SkillAgent()
        
        self.agents = [
            self.security_agent,
            self.finance_agent,
            self.skill_agent
        ]
    
    async def process(self, event: dict) -> dict:
        logger.info(f"🎯 {self.name} starting orchestration...")
        
        # Generate unique transaction ID for this workflow
        transaction_id = str(uuid.uuid4())
        expense_id = event.get("expense_id", "unknown")
        amount = event.get("amount", 0)
        category = event.get("category", "General")
        
        results = {}
        
        # 1. Pehle Security Agent
        logger.info("🔒 Calling Security Agent...")
        security_result = await self.security_agent.process(event)
        results["security"] = security_result
        
        if security_result.get("blocked"):
            logger.warning("⛔ Event blocked by Security Agent")
            
            # Log security block decision
            audit_logger.log_decision(
                agent_name="Security Agent",
                expense_id=expense_id,
                decision="BLOCKED",
                reason=security_result.get("reason", "Security check failed"),
                amount=amount,
                category=category,
                details={"blocked_reason": security_result.get("reason")},
                transaction_id=transaction_id
            )
            
            return {
                "status": "BLOCKED",
                "reason": security_result.get("reason"),
                "agent": "Security Agent",
                "transaction_id": transaction_id
            }
        
        # 2. Phir Finance Agent
        logger.info("💰 Calling Finance Agent...")
        finance_result = await self.finance_agent.process(event)
        results["finance"] = finance_result
        
        # Log finance decision
        finance_decision = finance_result.get("status", "UNKNOWN")
        audit_logger.log_decision(
            agent_name="Finance Agent",
            expense_id=expense_id,
            decision=finance_decision,
            reason=finance_result.get("reason", "No reason provided"),
            amount=amount,
            category=category,
            details=finance_result,
            transaction_id=transaction_id
        )
        
        # 3. Last mein Skill Agent
        logger.info("📚 Calling Skill Agent...")
        skill_result = await self.skill_agent.process(event)
        results["skills"] = skill_result
        
        # Log skill agent decision
        skill_decision = skill_result.get("status", "SUCCESS")
        audit_logger.log_decision(
            agent_name="Skill Agent",
            expense_id=expense_id,
            decision=skill_decision,
            reason=f"Skills used: {', '.join(skill_result.get('skills_used', []))}",
            amount=amount,
            category=category,
            details=skill_result,
            transaction_id=transaction_id
        )
        
        logger.info("✅ Orchestration complete!")
        
        # Log final orchestrator decision
        audit_logger.log_decision(
            agent_name="Orchestrator Agent",
            expense_id=expense_id,
            decision="SUCCESS",
            reason="All agents processed successfully",
            amount=amount,
            category=category,
            details={"all_results": results},
            transaction_id=transaction_id
        )
        
        return {
            "status": "SUCCESS",
            "results": results,
            "orchestrated_by": "Orchestrator Agent",
            "transaction_id": transaction_id
        }
    
    def get_capabilities(self) -> list:
        all_caps = []
        for agent in self.agents:
            all_caps.extend(agent.get_capabilities())
        return all_caps
