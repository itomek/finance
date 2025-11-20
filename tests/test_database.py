import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.database.models import Base, Account, Transaction, ImportSession
from src.database.repository import AccountRepository, TransactionRepository, ImportSessionRepository

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)

def test_create_account(db_session):
    repo = AccountRepository(db_session)
    account = repo.create(
        name="Test Account",
        type="checking",
        institution="Test Bank"
    )
    assert account.id is not None
    assert account.name == "Test Account"
    assert account.type == "checking"
    assert account.institution == "Test Bank"

def test_create_transaction(db_session):
    account_repo = AccountRepository(db_session)
    account = account_repo.create(
        name="Test Account",
        type="checking",
        institution="Test Bank"
    )

    transaction_repo = TransactionRepository(db_session)
    transaction = transaction_repo.create(
        account_id=account.id,
        date=datetime.now(),
        amount=100.0,
        description="Test Transaction"
    )
    assert transaction.id is not None
    assert transaction.amount == 100.0
    assert transaction.account_id == account.id

def test_transaction_relationship(db_session):
    account_repo = AccountRepository(db_session)
    account = account_repo.create(
        name="Test Account",
        type="checking",
        institution="Test Bank"
    )

    transaction_repo = TransactionRepository(db_session)
    transaction = transaction_repo.create(
        account_id=account.id,
        date=datetime.now(),
        amount=100.0,
        description="Test Transaction"
    )
    
    # Refresh account to load relationship
    db_session.refresh(account)
    assert len(account.transactions) == 1
    assert account.transactions[0].id == transaction.id
    assert transaction.account.id == account.id

def test_import_session(db_session):
    repo = ImportSessionRepository(db_session)
    session = repo.create(
        source_file="test.pdf",
        status="pending"
    )
    assert session.id is not None
    assert session.source_file == "test.pdf"
    assert session.status == "pending"
