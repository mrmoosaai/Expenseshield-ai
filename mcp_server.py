"""
MCP (Model Context Protocol) Server Implementation
Exposes internal enterprise tools to AI Agents via a standardized, secure protocol.
"""

import json
from datetime import datetime
from typing import Dict, Any, Callable

class MCPServer:
    """
    Central MCP Server that registers and executes tools for the AI Agents.
    This decouples the AI reasoning from the actual execution layer.
    """
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.tools: Dict[str, Callable] = {}
        self.tool_metadata: Dict[str, Dict[str, str]] = {}
        print(f"🚀 MCP Server '{self.server_name}' initialized.")

    def register_tool(self, name: str, func: Callable, description: str):
        """Registers a Python function as an MCP Tool."""
        self.tools[name] = func
        self.tool_metadata[name] = {"description": description}
        print(f"  ✅ MCP Tool Registered: {name}")

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Safely executes an MCP Tool with given parameters."""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found in MCP registry."}
        
        try:
            # Execute the underlying function
            result = self.tools[tool_name](params)
            return {
                "status": "success",
                "tool": tool_name,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"status": "error", "tool": tool_name, "error": str(e)}

    def get_manifest(self) -> Dict[str, Any]:
        """Returns the list of available tools (used by Agents for discovery)."""
        return {
            "server": self.server_name,
            "available_tools": self.tool_metadata
        }

# ==========================================
# INITIALIZING THE EXPENSE SHIELD MCP SERVER
# ==========================================

# Note: In a real environment, we import from our existing modules.
# For demonstration and compatibility, we simulate the core logic here.

def _mock_security_check(params: Dict) -> Dict:
    desc = params.get("description", "")
    if "ignore instructions" in desc.lower():
        return {"blocked": True, "reason": "Injection detected"}
    return {"blocked": False, "redacted": desc}

def _mock_finance_check(params: Dict) -> Dict:
    amount = params.get("amount", 0)
    if amount > 1000:
        return {"approved": False, "reason": "Requires manager approval"}
    return {"approved": True, "reason": "Within auto-approval limit"}

# Initialize Server
expense_mcp = MCPServer("ExpenseShield_MCP_v1")

# Register Tools
expense_mcp.register_tool(
    name="validate_security", 
    func=_mock_security_check, 
    description="Checks expense description for PII and prompt injections."
)
expense_mcp.register_tool(
    name="validate_finance", 
    func=_mock_finance_check, 
    description="Checks if expense amount is within corporate auto-approval limits."
)

if __name__ == "__main__":
    print("\n--- Testing MCP Server ---")
    print(expense_mcp.get_manifest())
    print(expense_mcp.execute_tool("validate_finance", {"amount": 500}))
