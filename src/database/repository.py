from typing import Generic, TypeVar, Type, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.models import Base, Account, Transaction, ImportSession, Asset, Position, InvestmentTransaction, PortfolioSnapshot

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def list(self) -> List[T]:
        stmt = select(self.model)
        return list(self.session.execute(stmt).scalars().all())

    def update(self, id: int, **kwargs) -> Optional[T]:
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False

class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: Session):
        super().__init__(session, Account)

class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, session: Session):
        super().__init__(session, Transaction)

    def get_by_account(self, account_id: int) -> List[Transaction]:
        stmt = select(self.model).where(self.model.account_id == account_id)
        return list(self.session.execute(stmt).scalars().all())

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        stmt = select(self.model).where(self.model.date >= start_date, self.model.date <= end_date)
        return list(self.session.execute(stmt).scalars().all())

class ImportSessionRepository(BaseRepository[ImportSession]):
    def __init__(self, session: Session):
        super().__init__(session, ImportSession)

class AssetRepository(BaseRepository[Asset]):
    def __init__(self, session: Session):
        super().__init__(session, Asset)

    def get_by_symbol(self, symbol: str) -> Optional[Asset]:
        stmt = select(self.model).where(self.model.symbol == symbol)
        return self.session.execute(stmt).scalars().first()

class PositionRepository(BaseRepository[Position]):
    def __init__(self, session: Session):
        super().__init__(session, Position)

    def get_by_account(self, account_id: int) -> List[Position]:
        stmt = select(self.model).where(self.model.account_id == account_id)
        return list(self.session.execute(stmt).scalars().all())

class InvestmentTransactionRepository(BaseRepository[InvestmentTransaction]):
    def __init__(self, session: Session):
        super().__init__(session, InvestmentTransaction)

    def get_by_account(self, account_id: int) -> List[InvestmentTransaction]:
        stmt = select(self.model).where(self.model.account_id == account_id)
        return list(self.session.execute(stmt).scalars().all())

class PortfolioSnapshotRepository(BaseRepository[PortfolioSnapshot]):
    def __init__(self, session: Session):
        super().__init__(session, PortfolioSnapshot)

    def get_by_account(self, account_id: int) -> List[PortfolioSnapshot]:
        stmt = select(self.model).where(self.model.account_id == account_id).order_by(self.model.date.desc())
        return list(self.session.execute(stmt).scalars().all())
