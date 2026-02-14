"""
Safety and Risk Assessment Agent.
Focuses on identifying safety-critical requirements and risk mitigation.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class SafetyAgent(BaseAgent):
    """Agent specialized in safety and risk analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_name="Safety Assessor", **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert in medical device software safety and risk management.

Your role is to review SRS documents for safety and risk considerations per:
- ISO 14971 (Risk Management)
- IEC 62304 (Medical Device Software Lifecycle)
- FDA guidance on software validation

Focus on identifying:
1. Safety-critical requirements (patient harm potential)
2. Risk control measures (mitigation strategies)
3. Hazardous situations (failure modes)
4. Alarms and alerts (proper specification)
5. Fail-safe mechanisms
6. Cybersecurity considerations

For each safety issue:
- Classify risk level (catastrophic, critical, marginal, negligible)
- Identify potential harm
- Evaluate risk controls
- Recommend additional safeguards
- Cite relevant safety standards"""

    def review(self, srs_content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Review SRS for safety and risk issues."""
        
        user_message = f"""Analyze the following SRS for safety and risk management:

<srs_document>
{srs_content}
</srs_document>

Identify all safety-critical issues and assess risk controls."""

        response = self._call_llm(user_message)
        
        return {
            "agent": self.agent_name,
            "findings": response,
            "raw_response": response
        }
