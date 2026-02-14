"""
Sequential orchestration strategy.
Agents run one after another, each seeing previous agents' outputs.
"""

from typing import List, Dict, Any
from ..agents.base_agent import BaseAgent


class SequentialOrchestrator:
    """Runs agents sequentially, passing results forward."""
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
    
    def orchestrate(
        self,
        srs_content: str,
        rag_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Run agents sequentially."""
        results = {
            "orchestration_strategy": "sequential",
            "agent_results": [],
            "total_cost": 0.0,
            "total_time": 0.0
        }
        
        accumulated_context = rag_context or {}
        previous_findings = []
        
        for agent in self.agents:
            context = {
                **accumulated_context,
                "previous_agent_findings": previous_findings
            }
            
            agent_result = agent.review(srs_content, context)
            results["agent_results"].append(agent_result)
            previous_findings.append({
                "agent": agent.agent_name,
                "findings": agent_result.get("findings")
            })
        
        return results
