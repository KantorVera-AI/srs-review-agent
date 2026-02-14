"""
Parallel orchestration strategy.
All agents run independently, then results are aggregated.
"""

from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..agents.base_agent import BaseAgent


class ParallelOrchestrator:
    """Runs agents in parallel and aggregates results."""
    
    def __init__(self, agents: List[BaseAgent], max_workers: int = 4):
        self.agents = agents
        self.max_workers = max_workers
    
    def orchestrate(
        self,
        srs_content: str,
        rag_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Run all agents in parallel."""
        results = {
            "orchestration_strategy": "parallel",
            "agent_results": []
        }
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_agent = {
                executor.submit(agent.review, srs_content, rag_context): agent
                for agent in self.agents
            }
            
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    agent_result = future.result()
                    results["agent_results"].append(agent_result)
                except Exception as e:
                    results["agent_results"].append({
                        "agent": agent.agent_name,
                        "error": str(e)
                    })
        
        return results
