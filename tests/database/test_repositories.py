"""Tests for database repositories."""

from datetime import datetime, timedelta
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
from finance.database.repositories import (
    AccountRepository,
    ImportSessionRepository,
    TransactionRepository,
)


class TestBaseRepository:
    """Test base repository functionality through AccountRepository."""

    def test_create(self, db_session):
        """Test creating a record."""
        repo = AccountRepository(db_session)
        account = repo.create(
            name="Test Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        db_session.commit()

        assert account.id is not None
        assert account.name == "Test Account"

    def test_get(self, db_session):
        """Test getting a record by ID."""
        repo = AccountRepository(db_session)
        account = repo.create(
            name="Test Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        db_session.commit()

        retrieved = repo.get(account.id)
        assert retrieved is not None
        assert retrieved.id == account.id
        assert retrieved.name == "Test Account"

        # Test non-existent ID
        assert repo.get("non-existent-id") is None

    def test_list(self, db_session):
        """Test listing records."""
        repo = AccountRepository(db_session)
        
        # Create multiple accounts
        for i in range(3):
            repo.create(
                name=f"Account {i}",
                institution="Test Bank",
                account_type=AccountType.CHECKING,
            )
        db_session.commit()

        accounts = repo.list()
        assert len(accounts) == 3

        # Test with filters
        filtered = repo.list(institution="Test Bank")
        assert len(filtered) == 3

        filtered = repo.list(institution="Other Bank")
        assert len(filtered) == 0

    def test_update(self, db_session):
        """Test updating a record."""
        repo = AccountRepository(db_session)
        account = repo.create(
            name="Original Name",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        db_session.commit()

        updated = repo.update(account.id, name="Updated Name")
        db_session.commit()

        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.institution == "Test Bank"  # Unchanged

    def test_delete(self, db_session):
        """Test deleting a record."""
        repo = AccountRepository(db_session)
        account = repo.create(
            name="To Delete",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        db_session.commit()

        # Delete the account
        result = repo.delete(account.id)
        db_session.commit()

        assert result is True
        assert repo.get(account.id) is None

        # Try deleting non-existent
        assert repo.delete("non-existent") is False

    def test_count(self, db_session):
        """Test counting records."""
        repo = AccountRepository(db_session)
        
        assert repo.count() == 0

        # Create accounts
        for i in range(5):
            repo.create(
                name=f"Account {i}",
                institution="Bank A" if i < 3 else "Bank B",
                account_type=AccountType.CHECKING,
            )
        db_session.commit()

        assert repo.count() == 5
        assert repo.count(institution="Bank A") == 3
        assert repo.count(institution="Bank B") == 2


class TestAccountRepository:
    """Test AccountRepository specific methods."""

    def test_soft_delete(self, db_session):
        """Test soft deleting an account."""
        repo = AccountRepository(db_session)
        account = repo.create(
            name="Active Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
            is_active=True,
        )
        db_session.commit()

        # Soft delete
        updated = repo.soft_delete(account.id)
        db_session.commit()

        assert updated is not None
        assert updated.is_active is False
        # Account still exists in database
        assert repo.get(account.id) is not None

    def test_get_active(self, db_session):
        """Test getting active accounts."""
        repo = AccountRepository(db_session)
        
        # Create mix of active and inactive accounts
        active1 = repo.create(
            name="Active 1",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
            is_active=True,
        )
        inactive = repo.create(
            name="Inactive",
            institution="Test Bank",
            account_type=AccountType.SAVINGS,
            is_active=False,
        )
        active2 = repo.create(
            name="Active 2",
            institution="Test Bank",
            account_type=AccountType.INVESTMENT,
            is_active=True,
        )
        db_session.commit()

        active_accounts = repo.get_active()
        assert len(active_accounts) == 2
        assert active1 in active_accounts
        assert active2 in active_accounts
        assert inactive not in active_accounts

    def test_find_by_institution(self, db_session):
        """Test finding accounts by institution."""
        repo = AccountRepository(db_session)
        
        # Create accounts for different institutions
        pnc1 = repo.create(
            name="PNC Checking",
            institution="PNC",
            account_type=AccountType.CHECKING,
        )
        pnc2 = repo.create(
            name="PNC Savings",
            institution="PNC",
            account_type=AccountType.SAVINGS,
        )
        chase = repo.create(
            name="Chase Account",
            institution="Chase",
            account_type=AccountType.CHECKING,
        )
        db_session.commit()

        pnc_accounts = repo.find_by_institution("PNC")
        assert len(pnc_accounts) == 2
        assert pnc1 in pnc_accounts
        assert pnc2 in pnc_accounts
        assert chase not in pnc_accounts


class TestTransactionRepository:
    """Test TransactionRepository specific methods."""

    @pytest.fixture
    def setup_data(self, db_session):
        """Set up test data."""
        account = Account(
            name="Test Account",
            institution="Test Bank",
            account_type=AccountType.CHECKING,
        )
        import_session = ImportSession(
            source_file="test.pdf",
            institution="Test Bank",
            status=ImportStatus.COMPLETED,
        )
        db_session.add_all([account, import_session])
        db_session.commit()
        return account, import_session

    def test_create_bulk(self, db_session, setup_data):
        """Test bulk creating transactions."""
        account, import_session = setup_data
        repo = TransactionRepository(db_session)

        transactions_data = [
            {
                "account_id": account.id,
                "transaction_date": datetime(2024, 1, i),
                "amount": Decimal(f"{i * 10}.50"),
                "description": f"Transaction {i}",
                "transaction_type": TransactionType.DEBIT,
                "import_session_id": import_session.id,
            }
            for i in range(1, 6)
        ]

        transactions = repo.create_bulk(transactions_data)
        db_session.commit()

        assert len(transactions) == 5
        for i, trans in enumerate(transactions, 1):
            assert trans.description == f"Transaction {i}"
            assert trans.source_hash is not None  # Hash should be calculated

    def test_get_by_account(self, db_session, setup_data):
        """Test getting transactions by account."""
        account, import_session = setup_data
        repo = TransactionRepository(db_session)

        # Create transactions
        for i in range(10):
            repo.create(
                account_id=account.id,
                transaction_date=datetime(2024, 1, i + 1),
                amount=Decimal("50.00"),
                description=f"Trans {i}",
                transaction_type=TransactionType.DEBIT,
                import_session_id=import_session.id,
            )
        db_session.commit()

        # Get all transactions
        transactions = repo.get_by_account(account.id)
        assert len(transactions) == 10

        # Get with limit
        limited = repo.get_by_account(account.id, limit=5)
        assert len(limited) == 5

    def test_get_by_date_range(self, db_session, setup_data):
        """Test getting transactions by date range."""
        account, import_session = setup_data
        repo = TransactionRepository(db_session)

        # Create transactions across January 2024
        for day in [5, 10, 15, 20, 25]:
            repo.create(
                account_id=account.id,
                transaction_date=datetime(2024, 1, day),
                amount=Decimal("100.00"),
                description=f"Day {day}",
                transaction_type=TransactionType.DEBIT,
                import_session_id=import_session.id,
            )
        db_session.commit()

        # Get transactions from 10th to 20th
        start = datetime(2024, 1, 10)
        end = datetime(2024, 1, 20)
        transactions = repo.get_by_date_range(account.id, start, end)

        assert len(transactions) == 3
        dates = [t.transaction_date.day for t in transactions]
        assert dates == [10, 15, 20]

    def test_find_duplicates(self, db_session, setup_data):
        """Test finding duplicate transactions."""
        account, import_session = setup_data
        repo = TransactionRepository(db_session)

        # Create transaction with specific hash
        trans1 = repo.create(
            account_id=account.id,
            transaction_date=datetime(2024, 1, 15),
            amount=Decimal("100.00"),
            description="Duplicate Test",
            transaction_type=TransactionType.DEBIT,
            import_session_id=import_session.id,
            source_hash="abc123",
        )
        
        # Create another with same hash (duplicate)
        trans2 = repo.create(
            account_id=account.id,
            transaction_date=datetime(2024, 1, 15),
            amount=Decimal("100.00"),
            description="Duplicate Test",
            transaction_type=TransactionType.DEBIT,
            import_session_id=import_session.id,
            source_hash="abc123",
        )
        db_session.commit()

        duplicates = repo.find_duplicates("abc123")
        assert len(duplicates) == 2
        assert trans1 in duplicates
        assert trans2 in duplicates

    def test_get_total_by_category(self, db_session, setup_data):
        """Test getting totals by category."""
        account, import_session = setup_data
        repo = TransactionRepository(db_session)

        # Create transactions with different categories
        transactions = [
            ("Food", Decimal("50.00")),
            ("Food", Decimal("30.00")),
            ("Transport", Decimal("100.00")),
            ("Transport", Decimal("25.00")),
            ("Entertainment", Decimal("75.00")),
        ]

        for category, amount in transactions:
            repo.create(
                account_id=account.id,
                transaction_date=datetime(2024, 1, 15),
                amount=amount,
                description=f"{category} expense",
                category=category,
                transaction_type=TransactionType.DEBIT,
                import_session_id=import_session.id,
            )
        db_session.commit()

        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        totals = repo.get_total_by_category(account.id, start, end)

        assert totals["Food"] == 80.0
        assert totals["Transport"] == 125.0
        assert totals["Entertainment"] == 75.0


class TestImportSessionRepository:
    """Test ImportSessionRepository specific methods."""

    def test_update_status(self, db_session):
        """Test updating import session status."""
        repo = ImportSessionRepository(db_session)
        
        session = repo.create(
            source_file="test.pdf",
            institution="Test Bank",
            status=ImportStatus.PENDING,
        )
        db_session.commit()

        # Update status with notes
        notes = {"errors": ["Invalid date format on line 5"]}
        updated = repo.update_status(session.id, ImportStatus.FAILED, notes)
        db_session.commit()

        assert updated is not None
        assert updated.status == ImportStatus.FAILED
        assert updated.validation_notes == notes

    def test_get_pending(self, db_session):
        """Test getting pending import sessions."""
        repo = ImportSessionRepository(db_session)
        
        # Create sessions with different statuses
        pending1 = repo.create(
            source_file="pending1.pdf",
            institution="Bank A",
            status=ImportStatus.PENDING,
        )
        completed = repo.create(
            source_file="completed.pdf",
            institution="Bank B",
            status=ImportStatus.COMPLETED,
        )
        pending2 = repo.create(
            source_file="pending2.pdf",
            institution="Bank C",
            status=ImportStatus.PENDING,
        )
        db_session.commit()

        pending_sessions = repo.get_pending()
        assert len(pending_sessions) == 2
        assert pending1 in pending_sessions
        assert pending2 in pending_sessions
        assert completed not in pending_sessions

    def test_get_by_source_file(self, db_session):
        """Test getting import session by source file."""
        repo = ImportSessionRepository(db_session)
        
        session = repo.create(
            source_file="unique_file.pdf",
            institution="Test Bank",
            status=ImportStatus.COMPLETED,
        )
        db_session.commit()

        retrieved = repo.get_by_source_file("unique_file.pdf")
        assert retrieved is not None
        assert retrieved.id == session.id

        # Test non-existent file
        assert repo.get_by_source_file("non_existent.pdf") is None