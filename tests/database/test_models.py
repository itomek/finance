"""Tests for database models."""

from datetime import datetime
from decimal import Decimal

import pytest

from finance.database.models import (
    Account,
    AccountType,
    ImportSession,
    ImportStatus,
    Transaction,
    TransactionType,
)


class TestAccount:
    """Test Account model."""

    def test_create_account(self, db_session):
        """Test creating an account."""
        account = Account(
            name="Test Checking",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
            account_number_masked="****1234",
            is_active=True,
        )
        db_session.add(account)
        db_session.commit()

        assert account.id is not None
        assert account.name == "Test Checking"
        assert account.institution == "Test Bank"
        assert account.account_type == AccountType.CHECKING
        assert account.is_active is True
        assert account.created_at is not None
        assert account.updated_at is not None

    def test_account_repr(self, db_session):
        """Test account string representation."""
        account = Account(
            name="Savings Account",
            institution="Bank ABC",
            account_type=AccountType.SAVINGS,
        )
        assert repr(account) == "<Account(name='Savings Account', institution='Bank ABC')>"

    def test_account_relationships(self, db_session):
        """Test account relationships."""
        account = Account(
            name="Test Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        db_session.add(account)
        db_session.commit()

        # Initially no transactions
        assert account.transactions == []


class TestTransaction:
    """Test Transaction model."""

    def test_create_transaction(self, db_session):
        """Test creating a transaction."""
        # Create account and import session first
        account = Account(
            name="Test Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        import_session = ImportSession(
            source_file="test.pdf",
            institution="Test Bank",
            status=ImportStatus.PENDING,
        )
        db_session.add_all([account, import_session])
        db_session.commit()

        transaction = Transaction(
            account_id=account.id,
            transaction_date=datetime(2024, 1, 15),
            amount=Decimal("100.50"),
            description="Test Transaction",
            category="Food",
            transaction_type=TransactionType.DEBIT,
            import_session_id=import_session.id,
        )
        db_session.add(transaction)
        db_session.commit()

        assert transaction.id is not None
        assert transaction.amount == Decimal("100.50")
        assert transaction.description == "Test Transaction"
        assert transaction.category == "Food"
        assert transaction.transaction_type == TransactionType.DEBIT

    def test_transaction_calculate_hash(self):
        """Test transaction hash calculation."""
        transaction = Transaction(
            account_id="acc123",
            transaction_date=datetime(2024, 1, 15),
            amount=Decimal("100.50"),
            description="Test Transaction",
            transaction_type=TransactionType.DEBIT,
            import_session_id="import123",
        )
        
        hash1 = transaction.calculate_hash()
        assert len(hash1) == 64  # SHA-256 produces 64 character hex string
        
        # Same data should produce same hash
        hash2 = transaction.calculate_hash()
        assert hash1 == hash2

    def test_transaction_relationships(self, db_session):
        """Test transaction relationships."""
        account = Account(
            name="Test Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        import_session = ImportSession(
            source_file="test.pdf",
            institution="Test Bank",
            status=ImportStatus.PENDING,
        )
        db_session.add_all([account, import_session])
        db_session.commit()

        transaction = Transaction(
            account_id=account.id,
            transaction_date=datetime(2024, 1, 15),
            amount=Decimal("100.50"),
            description="Test Transaction",
            transaction_type=TransactionType.DEBIT,
            import_session_id=import_session.id,
        )
        db_session.add(transaction)
        db_session.commit()

        # Check relationships
        assert transaction.account == account
        assert transaction.import_session == import_session
        assert transaction in account.transactions
        assert transaction in import_session.transactions


class TestImportSession:
    """Test ImportSession model."""

    def test_create_import_session(self, db_session):
        """Test creating an import session."""
        import_session = ImportSession(
            source_file="statement_2024_01.pdf",
            institution="Test Bank",
            status=ImportStatus.PENDING,
            record_count=50,
            validation_notes={"warnings": ["Missing category for 5 transactions"]},
        )
        db_session.add(import_session)
        db_session.commit()

        assert import_session.id is not None
        assert import_session.source_file == "statement_2024_01.pdf"
        assert import_session.institution == "Test Bank"
        assert import_session.status == ImportStatus.PENDING
        assert import_session.record_count == 50
        assert import_session.validation_notes == {"warnings": ["Missing category for 5 transactions"]}
        assert import_session.import_date is not None
        assert import_session.created_at is not None

    def test_import_session_status_progression(self, db_session):
        """Test import session status changes."""
        import_session = ImportSession(
            source_file="test.pdf",
            institution="Test Bank",
            status=ImportStatus.PENDING,
        )
        db_session.add(import_session)
        db_session.commit()

        # Change status
        import_session.status = ImportStatus.VALIDATED
        db_session.commit()
        assert import_session.status == ImportStatus.VALIDATED

        # Change to completed
        import_session.status = ImportStatus.COMPLETED
        db_session.commit()
        assert import_session.status == ImportStatus.COMPLETED

    def test_import_session_repr(self):
        """Test import session string representation."""
        import_session = ImportSession(
            source_file="statement.pdf",
            institution="Bank XYZ",
            status=ImportStatus.COMPLETED,
        )
        assert repr(import_session) == "<ImportSession(file='statement.pdf', status='completed')>"