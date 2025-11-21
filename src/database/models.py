from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # checking, savings, investment, credit_card
    institution: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, default="USD")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    positions: Mapped[list["Position"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    investment_transactions: Mapped[list["InvestmentTransaction"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    portfolio_snapshots: Mapped[list["PortfolioSnapshot"]] = relationship(back_populates="account", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Account(name='{self.name}', institution='{self.institution}')>"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    merchant: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    account: Mapped["Account"] = relationship(back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction(date='{self.date}', amount={self.amount}, description='{self.description}')>"

class ImportSession(Base):
    __tablename__ = "import_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String, default="pending")  # pending, completed, failed
    source_file: Mapped[str] = mapped_column(String, nullable=False)
    items_processed: Mapped[int] = mapped_column(Integer, default=0)
    items_failed: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<ImportSession(id={self.id}, status='{self.status}', source='{self.source_file}')>"

class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # stock, etf, crypto, mutual_fund
    currency: Mapped[str] = mapped_column(String, default="USD")
    
    positions: Mapped[list["Position"]] = relationship(back_populates="asset")

    def __repr__(self) -> str:
        return f"<Asset(symbol='{self.symbol}', name='{self.name}')>"

class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    cost_basis: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    current_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    account: Mapped["Account"] = relationship(back_populates="positions")
    asset: Mapped["Asset"] = relationship(back_populates="positions")

    def __repr__(self) -> str:
        return f"<Position(asset_id={self.asset_id}, quantity={self.quantity})>"

class InvestmentTransaction(Base):
    __tablename__ = "investment_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)  # buy, sell, dividend, interest
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_share: Mapped[float] = mapped_column(Float, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    account: Mapped["Account"] = relationship(back_populates="investment_transactions")
    asset: Mapped["Asset"] = relationship()

    def __repr__(self) -> str:
        return f"<InvestmentTransaction(type='{self.transaction_type}', asset_id={self.asset_id}, amount={self.total_amount})>"

class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_value: Mapped[float] = mapped_column(Float, nullable=False)
    cash_balance: Mapped[float] = mapped_column(Float, nullable=False)
    invested_value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    account: Mapped["Account"] = relationship(back_populates="portfolio_snapshots")

    def __repr__(self) -> str:
        return f"<PortfolioSnapshot(date='{self.date}', total_value={self.total_value})>"
