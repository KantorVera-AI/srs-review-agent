"""
Traceability Validation Agent.
Ensures proper traceability between requirements, design, and test specifications.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class TraceabilityAgent(BaseAgent):
    """Agent specialized in traceability analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_name="Traceability Validator", **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert in requirements traceability for medical device software.

Your role is to verify traceability per IEC 62304 and FDA expectations:

1. Forward traceability: Requirements → Design → Implementation → Test
2. Backward traceability: Test → Implementation → Design → Requirements
3. Traceability matrix completeness
4. Unique requirement identifiers
5. Change impact analysis capability

Check for:
- Missing traceability links
- Orphaned requirements (no design/test)
- Ambiguous requirement IDs
- Inconsistent numbering schemes
- Gap in coverage

For each issue, specify:
- Type of traceability gap
- Affected requirement IDs
- Impact on validation
- Recommendation for fix"""

    def review(self, srs_content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Review SRS for traceability issues."""
        
        user_message = f"""Analyze traceability in the following SRS:

<srs_document>
{srs_content}
</srs_document>

Identify all traceability gaps and issues."""

        response = self._call_llm(user_message)
        
        return {
            "agent": self.agent_name,
            "findings": response,
            "raw_response": response
        }
