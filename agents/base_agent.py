"""
BASE AGENT - Sab agents isse inherit karenge
"""

from abc import ABC, abstractmethod
from monitoring.logger import logger

class BaseAgent(ABC):
    """
    Har agent ka base class
    """
    
    def __init__(self, name: str):
        self.name = name
        logger.info(f"🤖 {name} initialized")
    
    @abstractmethod
    async def process(self, event: dict) -> dict:
        """
        Event ko process karo
        """
        pass
    
    async def can_handle(self, event: dict) -> bool:
        """
        Check karo ke ye agent is event ko handle kar sakta hai
        """
        return True
    
    def get_capabilities(self) -> list:
        """
        Agent ki capabilities return karo
        """
        return []
