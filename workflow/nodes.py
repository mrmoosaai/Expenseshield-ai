"""
WORKFLOW NODES
Agent ke dimagh ke faislay (Decisions)
"""

import json
import google.genai as genai
from monitoring.logger import logger
import config

# ==========================================
# NODE 1: AUTO APPROVE (Python Logic)
# ==========================================
async def auto_approve_handler(expense: dict) -> dict:
    """
    $100 se kam — seedha approve, koi LLM nahi
    """
    amount = expense.get("amount", 0)
    logger.info(f"💰 Auto-approving expense: ${amount}")
    
    return {
        "status": "APPROVED",
        "reason": f"Auto-approved: ${amount} < ${config.AUTO_APPROVE_THRESHOLD}",
        "llm_used": False,
        "human_review": False,
        "processing_time": "instant"
    }

# ==========================================
# NODE 2: LLM REVIEW (Gemini Brain)
# ==========================================
async def llm_review_handler(expense: dict) -> dict:
    """
    $100+ expenses — Gemini se risk analysis
    """
    amount = expense.get("amount", 0)
    description = expense.get("description", "N/A")
    
    logger.info(f" Running LLM review for ${amount}")
    
    # Gemini Client
    client = genai.Client(api_key=config.LLM_CONFIG.get("api_key"))
    
    prompt = f"""
    Analyze this expense for compliance risks:
    Amount: ${amount}
    Description: {description}
    
    Return JSON only:
    {{"approved": true/false, "reason": "explanation", "risk_level": "low/medium/high"}}
    """
    
    try:
        response = client.models.generate_content(
            model=config.LLM_CONFIG["model"],
            contents=prompt
        )
        result = json.loads(response.text)
        
        return {
            "status": "LLM_REVIEW_COMPLETE",
            "llm_result": result,
            "requires_human": result.get("risk_level") in ["medium", "high"]
        }
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return {
            "status": "LLM_ERROR",
            "requires_human": True, # Agar LLM fail ho jaye toh human ko bhej do
            "llm_result": {"reason": "LLM failed, manual review needed"}
        }

# ==========================================
# NODE 3: HUMAN APPROVAL (Manager)
# ==========================================
async def human_approval_handler(expense: dict, llm_result: dict) -> dict:
    """
    Manager se approval (Abhi ke liye mock/simulated)
    """
    amount = expense.get("amount", 0)
    logger.info(f"⏸️ Requesting human approval for ${amount}...")
    
    # Note: Real ADK mein yahan RequestInput.ask() use hoga.
    # Abhi ke liye hum assume kar rahe hain manager ne 'yes' kaha.
    
    return {
        "status": "APPROVED",
        "approved_by": "human",
        "llm_used": True,
        "human_review": True
    }