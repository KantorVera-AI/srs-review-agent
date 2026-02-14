"""
Regulatory Compliance Agent.
Validates compliance with FDA, ISO, and IEC standards.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    """Agent specialized in regulatory compliance checking."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_name="Compliance Checker", **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are a regulatory compliance expert for medical device software.

Your role is to verify compliance with:
- 21 CFR Part 820 (FDA Quality System Regulation)
- IEC 62304 (Medical Device Software Lifecycle)
- ISO 13485 (Quality Management Systems)
- ISO 14971 (Risk Management)

Review the SRS for compliance with:
1. Design control requirements (21 CFR 820.30)
2. Software lifecycle processes (IEC 62304)
3. Documentation requirements
4. Verification and validation planning
5. Risk management integration
6. Configuration management

For each compliance gap:
- Cite specific regulation/standard clause
- Describe the non-conformance
- Assess regulatory risk
- Provide corrective action"""

    def review(self, srs_content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Review SRS for regulatory compliance."""
        
        user_message = f"""Check regulatory compliance of the following SRS:

<srs_document>
{srs_content}
</srs_document>

Identify all compliance gaps with specific regulatory citations."""

        response = self._call_llm(user_message)
        
        return {
            "agent": self.agent_name,
            "findings": response,
            "raw_response": response
        }
