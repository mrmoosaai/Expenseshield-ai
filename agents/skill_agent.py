from agents.base_agent import BaseAgent
from skills.loader import SkillLoader
from monitoring.logger import logger
from monitoring.audit_logger import audit_logger

class SkillAgent(BaseAgent):
    """
    Skills ko manage karne wala agent
    """
    
    def __init__(self):
        super().__init__("Skill Agent")
        self.skill_loader = SkillLoader()
        self.active_skills = []
    
    async def process(self, event: dict) -> dict:
        logger.info(f"📚 {self.name} processing...")
        
        # Detect required skills
        skills_needed = self._detect_skills(event)
        
        expense_id = event.get("expense_id", "unknown")
        amount = event.get("amount", 0)
        category = event.get("category", "General")
        
        results = {}
        for skill_name in skills_needed:
            logger.info(f"  → Loading skill: {skill_name}")
            skill_data = self.skill_loader.load(skill_name)
            results[skill_name] = skill_data
        
        # Log decision
        audit_logger.log_decision(
            agent_name="Skill Agent",
            expense_id=expense_id,
            decision="SUCCESS",
            reason=f"Processed with {len(skills_needed)} skill(s)",
            amount=amount,
            category=category,
            details={
                "skills_used": skills_needed,
                "skill_count": len(skills_needed)
            }
        )
        
        return {
            "status": "SUCCESS",
            "skills_used": skills_needed,
            "results": results
        }
    
    def _detect_skills(self, event: dict) -> list:
        description = event.get("description", "").lower()
        skills = []
        
        if any(k in description for k in ["git", "commit"]):
            skills.append("git-commit-formatter")
        if any(k in description for k in ["database", "sql"]):
            skills.append("database-validator")
        if any(k in description for k in ["license", "copyright"]):
            skills.append("license-header-adder")
        if any(k in description for k in ["json", "pydantic"]):
            skills.append("json-to-pydantic")
        
        return list(set(skills))
    
    def get_capabilities(self) -> list:
        return ["Git Formatting", "Database Validation", "License Management", "JSON Conversion"]
