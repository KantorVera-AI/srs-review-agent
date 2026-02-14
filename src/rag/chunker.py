"""
Document chunking for RAG system.
"""

from typing import List, Dict, Any


class DocumentChunker:
    """Chunks documents for embedding and retrieval."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_document(
        self,
        document: str,
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Chunk a document into smaller pieces."""
        chunks = []
        start = 0
        
        while start < len(document):
            end = min(start + self.chunk_size, len(document))
            chunk_text = document[start:end]
            
            chunks.append({
                "text": chunk_text,
                "start_char": start,
                "end_char": end,
                "metadata": metadata or {}
            })
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
