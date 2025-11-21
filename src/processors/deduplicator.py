from typing import List
from src.parsers.base_parser import TransactionData

class Deduplicator:
    def find_duplicates(self, new_transactions: List[TransactionData], existing_transactions: List[TransactionData]) -> List[TransactionData]:
        """
        Identify transactions in new_list that already exist in existing_list.
        Matching criteria: Date, Amount, and Description (fuzzy match).
        """
        duplicates = []
        for new_tx in new_transactions:
            for existing_tx in existing_transactions:
                if self._is_match(new_tx, existing_tx):
                    duplicates.append(new_tx)
                    break
        return duplicates

    def _is_match(self, tx1: TransactionData, tx2: TransactionData) -> bool:
        # Exact match on date and amount
        if tx1.date.date() != tx2.date.date():
            return False
        if abs(tx1.amount - tx2.amount) > 0.01:
            return False
            
        # Simple description check (can be enhanced with fuzzy matching)
        return tx1.description.strip().lower() == tx2.description.strip().lower()
