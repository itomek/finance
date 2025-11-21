import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.database.models import Base, Account, Asset, Position, InvestmentTransaction, PortfolioSnapshot
from src.database.repository import AccountRepository, AssetRepository, PositionRepository, InvestmentTransactionRepository, PortfolioSnapshotRepository

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

def test_create_asset(db_session):
    repo = AssetRepository(db_session)
    asset = repo.create(
        symbol="AAPL",
        name="Apple Inc.",
        type="stock",
        currency="USD"
    )
    assert asset.id is not None
    assert asset.symbol == "AAPL"
    assert asset.name == "Apple Inc."

def test_create_position(db_session):
    # Setup
    account_repo = AccountRepository(db_session)
    account = account_repo.create(name="Test Investment", type="investment", institution="Fidelity")
    
    asset_repo = AssetRepository(db_session)
    asset = asset_repo.create(symbol="AAPL", name="Apple Inc.", type="stock")

    # Test
    repo = PositionRepository(db_session)
    position = repo.create(
        account_id=account.id,
        asset_id=asset.id,
        quantity=10.0,
        cost_basis=1500.0,
        current_price=160.0,
        current_value=1600.0
    )
    
    assert position.id is not None
    assert position.quantity == 10.0
    assert position.cost_basis == 1500.0
    
    # Check relationships
    db_session.refresh(account)
    assert len(account.positions) == 1
    assert account.positions[0].asset.symbol == "AAPL"

def test_investment_transaction(db_session):
    # Setup
    account_repo = AccountRepository(db_session)
    account = account_repo.create(name="Test Investment", type="investment", institution="Fidelity")
    
    asset_repo = AssetRepository(db_session)
    asset = asset_repo.create(symbol="VTI", name="Vanguard Total Stock Market", type="etf")

    # Test
    repo = InvestmentTransactionRepository(db_session)
    tx = repo.create(
        account_id=account.id,
        asset_id=asset.id,
        transaction_type="buy",
        quantity=5.0,
        price_per_share=200.0,
        total_amount=1000.0,
        date=datetime.now()
    )
    
    assert tx.id is not None
    assert tx.transaction_type == "buy"
    assert tx.total_amount == 1000.0

def test_portfolio_snapshot(db_session):
    # Setup
    account_repo = AccountRepository(db_session)
    account = account_repo.create(name="Test Investment", type="investment", institution="Fidelity")

    # Test
    repo = PortfolioSnapshotRepository(db_session)
    snapshot = repo.create(
        account_id=account.id,
        date=datetime.now(),
        total_value=10000.0,
        cash_balance=500.0,
        invested_value=9500.0
    )
    
    assert snapshot.id is not None
    assert snapshot.total_value == 10000.0
    
    # Test get_by_account
    snapshots = repo.get_by_account(account.id)
    assert len(snapshots) == 1
    assert snapshots[0].id == snapshot.id
