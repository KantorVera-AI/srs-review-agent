"""
Reranking for RAG results.
"""

from typing import List, Dict, Any


class Reranker:
    """Reranks retrieved documents for better relevance."""
    
    def __init__(self, use_reranking: bool = True):
        self.use_reranking = use_reranking
    
    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Rerank documents based on relevance to query."""
        if not self.use_reranking:
            return documents
        
        # TODO: Implement reranking
        return documents
