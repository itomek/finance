"""Repository layer for database operations."""

from datetime import datetime, timezone
from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from .models import Account, Base, ImportSession, ImportStatus, Transaction

# Generic type for models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, session: Session, model: Type[ModelType]):
        """Initialize repository.
        
        Args:
            session: SQLAlchemy session.
            model: SQLAlchemy model class.
        """
        self.session = session
        self.model = model

    def create(self, **kwargs: Any) -> ModelType:
        """Create a new record.
        
        Args:
            **kwargs: Model field values.
            
        Returns:
            Created model instance.
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.flush()  # Flush to get ID without committing
        return instance

    def get(self, id: str) -> Optional[ModelType]:
        """Get a record by ID.
        
        Args:
            id: Record ID.
            
        Returns:
            Model instance or None if not found.
        """
        return self.session.query(self.model).filter(self.model.id == id).first()

    def list(self, **filters: Any) -> List[ModelType]:
        """List records with optional filters.
        
        Args:
            **filters: Field filters.
            
        Returns:
            List of model instances.
        """
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()

    def update(self, id: str, **kwargs: Any) -> Optional[ModelType]:
        """Update a record.
        
        Args:
            id: Record ID.
            **kwargs: Fields to update.
            
        Returns:
            Updated model instance or None if not found.
        """
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            if hasattr(instance, "updated_at"):
                instance.updated_at = datetime.now(timezone.utc)
            self.session.flush()
        return instance

    def delete(self, id: str) -> bool:
        """Delete a record.
        
        Args:
            id: Record ID.
            
        Returns:
            True if deleted, False if not found.
        """
        instance = self.get(id)
        if instance:
            self.session.delete(instance)
            self.session.flush()
            return True
        return False

    def count(self, **filters: Any) -> int:
        """Count records with optional filters.
        
        Args:
            **filters: Field filters.
            
        Returns:
            Record count.
        """
        query = self.session.query(func.count(self.model.id))
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.scalar()


class AccountRepository(BaseRepository[Account]):
    """Repository for Account operations."""

    def __init__(self, session: Session):
        """Initialize AccountRepository."""
        super().__init__(session, Account)

    def soft_delete(self, id: str) -> Optional[Account]:
        """Soft delete an account by marking it as inactive.
        
        Args:
            id: Account ID.
            
        Returns:
            Updated account or None if not found.
        """
        return self.update(id, is_active=False)

    def get_active(self) -> List[Account]:
        """Get all active accounts.
        
        Returns:
            List of active accounts.
        """
        return self.list(is_active=True)

    def find_by_institution(self, institution: str) -> List[Account]:
        """Find accounts by institution.
        
        Args:
            institution: Institution name.
            
        Returns:
            List of accounts.
        """
        return self.list(institution=institution)


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for Transaction operations."""

    def __init__(self, session: Session):
        """Initialize TransactionRepository."""
        super().__init__(session, Transaction)

    def create_bulk(self, transactions: List[dict]) -> List[Transaction]:
        """Create multiple transactions.
        
        Args:
            transactions: List of transaction data.
            
        Returns:
            List of created transactions.
        """
        instances = []
        for trans_data in transactions:
            # Calculate hash if not provided
            if "source_hash" not in trans_data:
                temp_trans = Transaction(**trans_data)
                trans_data["source_hash"] = temp_trans.calculate_hash()
            
            instance = Transaction(**trans_data)
            self.session.add(instance)
            instances.append(instance)
        
        self.session.flush()
        return instances

    def get_by_account(
        self, account_id: str, limit: Optional[int] = None
    ) -> List[Transaction]:
        """Get transactions for an account.
        
        Args:
            account_id: Account ID.
            limit: Optional limit on number of results.
            
        Returns:
            List of transactions.
        """
        query = (
            self.session.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .order_by(Transaction.transaction_date.desc())
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()

    def get_by_date_range(
        self,
        account_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Transaction]:
        """Get transactions within a date range.
        
        Args:
            account_id: Account ID.
            start_date: Start date.
            end_date: End date.
            
        Returns:
            List of transactions.
        """
        return (
            self.session.query(Transaction)
            .filter(
                and_(
                    Transaction.account_id == account_id,
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                )
            )
            .order_by(Transaction.transaction_date)
            .all()
        )

    def find_duplicates(self, source_hash: str) -> List[Transaction]:
        """Find transactions with the same hash.
        
        Args:
            source_hash: Transaction hash.
            
        Returns:
            List of potential duplicate transactions.
        """
        return self.list(source_hash=source_hash)

    def get_total_by_category(
        self, account_id: str, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get transaction totals grouped by category.
        
        Args:
            account_id: Account ID.
            start_date: Start date.
            end_date: End date.
            
        Returns:
            Dictionary of category totals.
        """
        results = (
            self.session.query(
                Transaction.category,
                func.sum(Transaction.amount).label("total"),
            )
            .filter(
                and_(
                    Transaction.account_id == account_id,
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                )
            )
            .group_by(Transaction.category)
            .all()
        )
        
        return {category: float(total) for category, total in results}


class ImportSessionRepository(BaseRepository[ImportSession]):
    """Repository for ImportSession operations."""

    def __init__(self, session: Session):
        """Initialize ImportSessionRepository."""
        super().__init__(session, ImportSession)

    def update_status(
        self, id: str, status: ImportStatus, notes: Optional[dict] = None
    ) -> Optional[ImportSession]:
        """Update import session status.
        
        Args:
            id: Session ID.
            status: New status.
            notes: Optional validation notes.
            
        Returns:
            Updated session or None if not found.
        """
        update_data = {"status": status}
        if notes:
            update_data["validation_notes"] = notes
        return self.update(id, **update_data)

    def get_pending(self) -> List[ImportSession]:
        """Get all pending import sessions.
        
        Returns:
            List of pending sessions.
        """
        return self.list(status=ImportStatus.PENDING)

    def get_by_source_file(self, source_file: str) -> Optional[ImportSession]:
        """Get import session by source file.
        
        Args:
            source_file: Source file name.
            
        Returns:
            Import session or None.
        """
        return (
            self.session.query(ImportSession)
            .filter(ImportSession.source_file == source_file)
            .first()
        )