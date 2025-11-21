import pytest
from datetime import datetime
from src.parsers.base_parser import TransactionData
from src.processors.validator import Validator
from src.processors.deduplicator import Deduplicator
from src.analysis.spending import Categorizer

def test_validator_balance():
    validator = Validator()
    txs = [
        TransactionData(date=datetime.now(), amount=100.0, description="Deposit"),
        TransactionData(date=datetime.now(), amount=-50.0, description="Withdrawal")
    ]
    
    # 1000 + 100 - 50 = 1050
    assert validator.validate_balance(txs, 1000.0, 1050.0) is True
    assert validator.validate_balance(txs, 1000.0, 1000.0) is False

def test_deduplicator():
    deduplicator = Deduplicator()
    existing = [
        TransactionData(date=datetime(2023, 1, 1), amount=100.0, description="Test")
    ]
    new_txs = [
        TransactionData(date=datetime(2023, 1, 1), amount=100.0, description="Test"),
        TransactionData(date=datetime(2023, 1, 2), amount=50.0, description="Other")
    ]
    
    duplicates = deduplicator.find_duplicates(new_txs, existing)
    assert len(duplicates) == 1
    assert duplicates[0].amount == 100.0

def test_categorizer():
    categorizer = Categorizer()
    txs = [
        TransactionData(date=datetime.now(), amount=-10.0, description="Starbucks Coffee"),
        TransactionData(date=datetime.now(), amount=-50.0, description="Kroger Grocery"),
        TransactionData(date=datetime.now(), amount=-20.0, description="Unknown Store")
    ]
    
    categorized = categorizer.categorize(txs)
    
    assert categorized[0].category == "dining"
    assert categorized[1].category == "grocery"
    assert categorized[2].category == "uncategorized"
