"""Tests for database connection management."""

import tempfile
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from finance.database.connection import (
    DatabaseConfig,
    get_database_path,
    get_db_session,
    init_database,
    set_database_path,
)
from finance.database.models import Account, AccountType


class TestDatabaseConnection:
    """Test database connection and configuration."""

    def test_database_config_default_path(self):
        """Test default database configuration."""
        config = DatabaseConfig()
        assert config.db_path == Path.home() / ".finance-cli" / "finance.db"
        assert str(config.db_path) in config.db_url

    def test_database_config_custom_path(self):
        """Test custom database path configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "custom.db"
            config = DatabaseConfig(custom_path)
            assert config.db_path == custom_path
            assert str(custom_path) in config.db_url

    def test_get_db_session_context_manager(self):
        """Test database session context manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            set_database_path(db_path)
            init_database()

            # Use context manager
            with get_db_session() as session:
                assert isinstance(session, Session)
                
                # Create a test account
                account = Account(
                    name="Test Account",
                    institution="Test Bank",
                    account_type=AccountType.CHECKING,
                )
                session.add(account)
                # Session should commit on exit

            # Verify account was committed
            with get_db_session() as session:
                accounts = session.query(Account).all()
                assert len(accounts) == 1
                assert accounts[0].name == "Test Account"

    def test_get_db_session_rollback_on_exception(self):
        """Test that session rolls back on exception."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            set_database_path(db_path)
            init_database()

            # Try to create account but raise exception
            with pytest.raises(ValueError):
                with get_db_session() as session:
                    account = Account(
                        name="Should Rollback",
                        institution="Test Bank",
                        account_type=AccountType.CHECKING,
                    )
                    session.add(account)
                    raise ValueError("Test exception")

            # Verify account was not committed
            with get_db_session() as session:
                accounts = session.query(Account).all()
                assert len(accounts) == 0

    def test_init_database_creates_tables(self):
        """Test that init_database creates all tables."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            
            # Initialize database
            init_database(db_path)
            
            # Verify database file exists
            assert db_path.exists()
            
            # Verify tables can be used
            with get_db_session() as session:
                # Should not raise any errors
                session.query(Account).count()

    def test_init_database_force_recreates_tables(self):
        """Test that force=True recreates tables."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            init_database(db_path)

            # Add some data
            with get_db_session() as session:
                account = Account(
                    name="Will Be Deleted",
                    institution="Test Bank",
                    account_type=AccountType.CHECKING,
                )
                session.add(account)

            # Reinitialize with force=True
            init_database(db_path, force=True)

            # Verify data was deleted
            with get_db_session() as session:
                accounts = session.query(Account).all()
                assert len(accounts) == 0

    def test_get_and_set_database_path(self):
        """Test getting and setting database path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_path = get_database_path()
            
            # Set new path
            new_path = Path(tmpdir) / "new.db"
            set_database_path(new_path)
            assert get_database_path() == new_path
            
            # Restore original (for other tests)
            set_database_path(original_path)