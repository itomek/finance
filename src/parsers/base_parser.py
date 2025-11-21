from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TransactionData:
    date: datetime
    amount: float
    description: str
    category: Optional[str] = None
    merchant: Optional[str] = None
    balance: Optional[float] = None

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> List[TransactionData]:
        """Parse a statement file and return a list of transactions."""
        pass

    @abstractmethod
    def validate(self, transactions: List[TransactionData]) -> bool:
        """Validate the parsed transactions (e.g. balance reconciliation)."""
        pass
