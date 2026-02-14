"""
Ground truth data loader.
"""

from typing import List, Dict, Any
import json
from pathlib import Path


class GroundTruthLoader:
    """Loads and manages ground truth data for evaluation."""
    
    def __init__(self, data_dir: str = "data/ground_truth"):
        self.data_dir = Path(data_dir)
    
    def load_ground_truth(self, dataset_name: str = "validation") -> List[Dict[str, Any]]:
        """Load ground truth dataset."""
        ground_truth_file = self.data_dir / f"{dataset_name}.json"
        
        if not ground_truth_file.exists():
            return []
        
        with open(ground_truth_file, 'r') as f:
            return json.load(f)
    
    def save_ground_truth(
        self,
        data: List[Dict[str, Any]],
        dataset_name: str = "validation"
    ):
        """Save ground truth dataset."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        ground_truth_file = self.data_dir / f"{dataset_name}.json"
        
        with open(ground_truth_file, 'w') as f:
            json.dump(data, f, indent=2)
