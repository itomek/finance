from typing import List
from src.parsers.base_parser import TransactionData

class Categorizer:
    def __init__(self):
        self.rules = {
            "grocery": ["kroger", "whole foods", "trader joe"],
            "dining": ["restaurant", "cafe", "starbucks", "mcdonalds"],
            "transport": ["uber", "lyft", "shell", "bp"],
            "utilities": ["electric", "water", "internet", "att", "verizon"],
            "income": ["payroll", "deposit", "salary"]
        }

    def categorize(self, transactions: List[TransactionData]) -> List[TransactionData]:
        """Assign categories to transactions based on rules."""
        for tx in transactions:
            if tx.category:
                continue
                
            desc_lower = tx.description.lower()
            for category, keywords in self.rules.items():
                if any(keyword in desc_lower for keyword in keywords):
                    tx.category = category
                    break
            
            if not tx.category:
                tx.category = "uncategorized"
                
        return transactions
