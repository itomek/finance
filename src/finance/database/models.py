"""SQLAlchemy models for the finance database."""

import enum
import hashlib
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class AccountType(enum.Enum):
    """Types of financial accounts."""

    CHECKING = "checking"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    CREDIT = "credit"
    LOAN = "loan"


class TransactionType(enum.Enum):
    """Types of transactions."""

    DEBIT = "debit"
    CREDIT = "credit"


class ImportStatus(enum.Enum):
    """Status of an import session."""

    PENDING = "pending"
    VALIDATED = "validated"
    COMPLETED = "completed"
    FAILED = "failed"


class Account(Base):
    """Financial account model."""

    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False)
    institution = Column(String(50), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    account_number_masked = Column(String(20))  # Last 4 digits only
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    transactions = relationship(
        "Transaction", back_populates="account", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Account(name='{self.name}', institution='{self.institution}')>"


class Transaction(Base):
    """Financial transaction model."""

    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id = Column(String(36), ForeignKey("accounts.id"), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))
    transaction_type = Column(Enum(TransactionType), nullable=False)
    import_session_id = Column(
        String(36), ForeignKey("import_sessions.id"), nullable=False
    )
    source_hash = Column(String(64))  # SHA-256 hash for duplicate detection
    extra_data = Column(JSON)  # Additional flexible data (avoiding 'metadata' which is reserved)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    account = relationship("Account", back_populates="transactions")
    import_session = relationship("ImportSession", back_populates="transactions")

    def calculate_hash(self) -> str:
        """Calculate a hash for duplicate detection."""
        hash_input = f"{self.account_id}:{self.transaction_date}:{self.amount}:{self.description}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<Transaction(date='{self.transaction_date}', amount={self.amount}, description='{self.description[:30]}...')>"


class ImportSession(Base):
    """Track import sessions for data lineage."""

    __tablename__ = "import_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    source_file = Column(String(255), nullable=False)
    institution = Column(String(50), nullable=False)
    import_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(Enum(ImportStatus), default=ImportStatus.PENDING, nullable=False)
    record_count = Column(Integer, default=0)
    validation_notes = Column(JSON)  # Store validation issues and warnings
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    transactions = relationship(
        "Transaction", back_populates="import_session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ImportSession(file='{self.source_file}', status='{self.status.value}')>"