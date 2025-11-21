import json
from dataclasses import asdict
from typing import List, Dict, Any
from src.parsers.base_parser import TransactionData

class StagingManager:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def stage_transactions(self, import_id: str, transactions: List[TransactionData]) -> None:
        """Save parsed transactions to staging area."""
        data = [asdict(tx) for tx in transactions]
        # Serialize datetime objects
        for item in data:
            item['date'] = item['date'].isoformat()
            
        # In a real app, we'd write to a file or DB. For now, just print or mock.
        # print(f"Staged {len(transactions)} transactions for import {import_id}")
        
    def get_staged_transactions(self, import_id: str) -> List[TransactionData]:
        """Retrieve transactions from staging."""
        # Mock retrieval
        return []
