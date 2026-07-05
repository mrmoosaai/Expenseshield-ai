"""
WORKFLOW GRAPH
Ye file pura agent flow control karti hai (Nodes + Edges)
"""

from workflow.nodes import (
    auto_approve_handler,
    llm_review_handler,
    human_approval_handler
)
from workflow.edges import get_next_node_after_security
from monitoring.logger import logger
import config

class ExpenseWorkflow:
    """
    Complete Expense Approval Workflow
    """
    
    def __init__(self):
        self.name = "expense_approval"
        logger.info(f"🕸️ Workflow '{self.name}' initialized")
    
    async def execute(self, expense: dict) -> dict:
        """
        Pura workflow execute karo
        """
        logger.info(f"🚀 Starting workflow for amount: ${expense.get('amount', 0)}")
        
        # Step 1: Security Check (Yahan hum assume kar rahe hain ke security pass ho gayi)
        # Real implementation mein yahan SecurityShield call hoga
        logger.info("🛡️ Security check passed (simulated)")
        
        # Step 2: Routing Logic (Edges use karo)
        next_node = get_next_node_after_security(expense)
        logger.info(f"➡️ Routing to: {next_node}")
        
        # Step 3: Node Execute karo
        if next_node == "auto_approve":
            result = await auto_approve_handler(expense)
        elif next_node == "llm_review":
            result = await llm_review_handler(expense)
            
            # Agar LLM ne kaha human review chahiye
            if result.get("requires_human", False):
                logger.info("➡️ Routing to human_approval")
                result = await human_approval_handler(expense, result.get("llm_result", {}))
        else:
            result = {"status": "ERROR", "reason": "Unknown node"}
            
        logger.info(f"✅ Workflow completed with status: {result.get('status')}")
        return result