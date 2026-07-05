"""
CODE RUNNER
Code ko isolated environment mein run karta hai
"""

from sandbox.safe_evaluator import SafeEvaluator
from monitoring.logger import logger

class SandboxRunner:
    """
    Isolated environment mein code run karta hai
    """
    
    def __init__(self):
        self.evaluator = SafeEvaluator()
    
    def run_skill_code(self, code: str, context: dict = None):
        """
        Skill code ko sandbox mein run karo
        """
        # 1. Safety check (Pehle check karo ke code safe hai)
        if not self.evaluator.is_safe(code):
            logger.warning("⛔ Unsafe code blocked by sandbox!")
            return {
                'success': False,
                'error': 'Code blocked by security sandbox'
            }
        
        # 2. Safe hai toh run karo
        try:
            # Restricted environment (Sirf ye functions available honge)
            safe_globals = {
                '__builtins__': {
                    'len': len,
                    'range': range,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'print': lambda *args: None,
                    'True': True,
                    'False': False,
                    'None': None,
                },
                'context': context or {}
            }
            
            # Code execute karo
            result = eval(code, safe_globals)
            
            logger.info("Code executed safely in sandbox")
            return {
                'success': True,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Sandbox execution error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
