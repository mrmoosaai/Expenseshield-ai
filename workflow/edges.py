"""
WORKFLOW EDGES (Routing Logic)
Ye file decide karti hai ke agla step kaunsa hoga (Traffic Police)
"""

import config

def get_next_node_after_security(expense: dict) -> str:
    """
    Security check ke baad amount ko dekho aur faisla karo
    """
    amount = expense.get("amount", 0)
    
    # Agar $100 se kam hai toh Auto Approve bhejo
    if amount < config.AUTO_APPROVE_THRESHOLD:
        return "auto_approve"
    
    # Agar $100 ya zyada hai toh LLM Review bhejo
    else:
        return "llm_review"


# def get_next_node_after_llm(llm_result: dict) -> str:
#     """
#     LLM review ke baad check karo ke Manager ki zaroorat hai ya nahi
#     """
#     # Agar LLM ne kaha risk zyada hai (medium/high)
#     if llm_result.get("requires_human", False):
#         return "human_approval"
#     
#     # Agar LLM ne kaha sab theek hai (low risk)
#     else:
#         return "auto_approve"