"""Database connection and session management."""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

# Default database location
DEFAULT_DB_PATH = Path.home() / ".finance-cli" / "finance.db"


class DatabaseConfig:
    """Database configuration."""

    def __init__(self, db_path: Path | None = None):
        """Initialize database configuration.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses default.
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_url = f"sqlite:///{self.db_path}"


# Global database configuration
_config = DatabaseConfig()
_engine = None
_SessionLocal = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            _config.db_url,
            connect_args={"check_same_thread": False},  # SQLite specific
            echo=False,  # Set to True for SQL logging
        )
    return _engine


def get_session_factory():
    """Get or create the session factory."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _SessionLocal


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions.
    
    Yields:
        Session: A SQLAlchemy session.
    
    Example:
        with get_db_session() as session:
            account = session.query(Account).first()
    """
    SessionLocal = get_session_factory()
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_database(db_path: Path | None = None, force: bool = False) -> None:
    """Initialize the database.
    
    Args:
        db_path: Optional path to the database file.
        force: If True, recreate all tables (WARNING: destroys existing data).
    """
    global _config, _engine, _SessionLocal
    
    if db_path:
        _config = DatabaseConfig(db_path)
        _engine = None
        _SessionLocal = None
    
    engine = get_engine()
    
    if force:
        Base.metadata.drop_all(bind=engine)
    
    Base.metadata.create_all(bind=engine)


def get_database_path() -> Path:
    """Get the current database path.
    
    Returns:
        Path: The path to the database file.
    """
    return _config.db_path


def set_database_path(db_path: Path) -> None:
    """Set a new database path.
    
    Args:
        db_path: The new database path.
    """
    global _config, _engine, _SessionLocal
    _config = DatabaseConfig(db_path)
    _engine = None
    _SessionLocal = None