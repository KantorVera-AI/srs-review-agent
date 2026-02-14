"""
Iterative refinement orchestration.
Agents critique and refine each other's findings through multiple rounds.
"""

from typing import List, Dict, Any
from ..agents.base_agent import BaseAgent


class IterativeOrchestrator:
    """Runs agents in iterative refinement cycles."""
    
    def __init__(
        self,
        agents: List[BaseAgent],
        max_iterations: int = 3
    ):
        self.agents = agents
        self.max_iterations = max_iterations
    
    def orchestrate(
        self,
        srs_content: str,
        rag_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Run agents iteratively with refinement."""
        results = {
            "orchestration_strategy": "iterative",
            "iterations": []
        }
        
        current_findings = {}
        
        for iteration in range(self.max_iterations):
            iteration_results = {
                "iteration": iteration + 1,
                "agent_results": []
            }
            
            for agent in self.agents:
                context = {
                    **(rag_context or {}),
                    "other_agent_findings": {
                        k: v for k, v in current_findings.items()
                        if k != agent.agent_name
                    }
                }
                
                agent_result = agent.review(srs_content, context)
                iteration_results["agent_results"].append(agent_result)
                current_findings[agent.agent_name] = agent_result
            
            results["iterations"].append(iteration_results)
        
        return results
