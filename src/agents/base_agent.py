"""
Base Agent class for SRS review system.
All specialized agents inherit from this class.
"""

from typing import Dict, List, Any
from anthropic import Anthropic
import os


class BaseAgent:
    """Base class for all SRS review agents."""
    
    def __init__(
        self,
        agent_name: str,
        model: str = "claude-sonnet-4-5-20250929",
        temperature: float = 0.0,
        max_tokens: int = 4096
    ):
        self.agent_name = agent_name
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement get_system_prompt()")
    
    def review(self, srs_content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform review of SRS content.
        
        Args:
            srs_content: The SRS document content to review
            context: Additional context (RAG results, previous agent outputs, etc.)
            
        Returns:
            Dictionary containing findings, confidence scores, and citations
        """
        raise NotImplementedError("Subclasses must implement review()")
    
    def _call_llm(self, user_message: str, system_prompt: str = None) -> str:
        """Helper method to call the LLM API."""
        if system_prompt is None:
            system_prompt = self.get_system_prompt()
            
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.content[0].text
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage."""
        # Pricing as of Feb 2025 (update as needed)
        pricing = {
            "claude-opus-4-5-20251101": {"input": 0.015, "output": 0.075},
            "claude-sonnet-4-5-20250929": {"input": 0.003, "output": 0.015},
            "claude-haiku-4-5-20251001": {"input": 0.0008, "output": 0.004},
        }
        
        rates = pricing.get(self.model, {"input": 0.003, "output": 0.015})
        cost = (input_tokens / 1_000_000 * rates["input"]) + \
               (output_tokens / 1_000_000 * rates["output"])
        
        return cost
