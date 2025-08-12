"""Pytest fixtures for database tests."""

import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from finance.database.models import Base


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = Path(tmp.name)

    # Create engine and tables
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)

    yield db_path

    # Cleanup
    engine.dispose()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def db_session(temp_db):
    """Create a database session for testing."""
    engine = create_engine(f"sqlite:///{temp_db}")
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = session_factory()
    yield session

    session.close()
    engine.dispose()

