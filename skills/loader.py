"""
SKILL LOADER
Skills ko dynamically load/unload karta hai
"""

import os
import json
from monitoring.logger import logger

class SkillLoader:
    """
    Skills ko manage karta hai
    """
    
    def __init__(self, skills_dir="skills"):
        """
        Skills folder set karo
        """
        self.skills_dir = skills_dir
        self.loaded_skills = {}  # Cache: loaded skills yahan rahengi
        self.skill_metadata = {}  # Metadata: har skill ki basic info
        
        # Startup par sab skills scan karo
        self._scan_skills()
    
    def _scan_skills(self):
        """
        skills/ folder mein sab skills scan karo
        """
        if not os.path.exists(self.skills_dir):
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return
        
        # Har skill folder ko check karo
        for skill_name in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_name)
            
            # Sirf folders ko process karo
            if os.path.isdir(skill_path):
                skill_md = os.path.join(skill_path, "SKILL.md")
                
                # SKILL.md exist karta hai?
                if os.path.exists(skill_md):
                    # Metadata extract karo (YAML frontmatter)
                    metadata = self._extract_metadata(skill_md)
                    self.skill_metadata[skill_name] = metadata
                    
                    logger.info(f"📚 Skill discovered: {skill_name}")
    
    def _extract_metadata(self, skill_md_path):
        """
        SKILL.md se YAML frontmatter extract karo
        """
        metadata = {
            "name": "",
            "description": "",
            "triggers": []
        }
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML frontmatter extract karo (--- ke beech)
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    yaml_content = content[3:end].strip()
                    
                    # Simple parsing (name, description)
                    for line in yaml_content.split("\n"):
                        if line.startswith("name:"):
                            metadata["name"] = line.split(":", 1)[1].strip()
                        elif line.startswith("description:"):
                            metadata["description"] = line.split(":", 1)[1].strip()
            
        except Exception as e:
            logger.error(f"Error reading {skill_md_path}: {e}")
        
        return metadata
    
    def load(self, skill_name):
        """
        Ek specific skill load karo
        """
        # Pehle se loaded hai?
        if skill_name in self.loaded_skills:
            logger.info(f"  ✓ Skill already loaded: {skill_name}")
            return self.loaded_skills[skill_name]
        
        # Skill path banao
        skill_path = os.path.join(self.skills_dir, skill_name, "SKILL.md")
        
        if not os.path.exists(skill_path):
            logger.error(f"  ✗ Skill not found: {skill_name}")
            return None
        
        # SKILL.md padho
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Cache mein save karo
            self.loaded_skills[skill_name] = content
            
            logger.info(f"  ✓ Skill loaded: {skill_name} ({len(content)} chars)")
            
            return content
            
        except Exception as e:
            logger.error(f"  ✗ Error loading {skill_name}: {e}")
            return None
    
    def unload(self, skill_name):
        """
        Ek skill ko memory se hatao
        """
        if skill_name in self.loaded_skills:
            del self.loaded_skills[skill_name]
            logger.info(f"  🗑️ Skill unloaded: {skill_name}")
    
    def unload_all(self):
        """
        Sab skills ko unload karo
        """
        self.loaded_skills.clear()
        logger.info("🗑️ All skills unloaded")
    
    def get_loaded_skills(self):
        """
        Currently loaded skills ki list
        """
        return list(self.loaded_skills.keys())
    
    def get_all_skills(self):
        """
        Sab available skills ki list
        """
        return list(self.skill_metadata.keys())
    
    def find_skill_by_keyword(self, keyword):
        """
        Keyword se skill dhundo
        """
        keyword_lower = keyword.lower()
        matches = []
        
        for skill_name, metadata in self.skill_metadata.items():
            description = metadata.get("description", "").lower()
            name = metadata.get("name", "").lower()
            
            if keyword_lower in description or keyword_lower in name:
                matches.append(skill_name)
        
        return matches