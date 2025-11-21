from typing import List
from src.parsers.base_parser import TransactionData

class Validator:
    def validate_balance(self, transactions: List[TransactionData], start_balance: float, end_balance: float) -> bool:
        """
        Verify that start_balance + sum(transactions) == end_balance.
        Returns True if valid, False otherwise.
        """
        total_change = sum(tx.amount for tx in transactions)
        calculated_end = start_balance + total_change
        
        # Allow for small floating point differences
        return abs(calculated_end - end_balance) < 0.01

    def check_anomalies(self, transactions: List[TransactionData]) -> List[str]:
        """Return a list of warnings for anomalous transactions."""
        warnings = []
        for tx in transactions:
            if abs(tx.amount) > 10000:
                warnings.append(f"Large transaction detected: {tx.amount} on {tx.date}")
        return warnings
