"""Tests for the hello module."""

from importlib.metadata import PackageNotFoundError
from io import StringIO
from unittest.mock import patch

from finance import __version__, hello_world
from finance.hello import get_version


class TestHelloWorld:
    """Test cases for the hello_world function."""

    def test_hello_world_default(self) -> None:
        """Test that hello_world prints the expected message with no args."""
        with patch("sys.argv", ["finance"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                with patch("sys.exit") as mock_exit:
                    hello_world()
                    mock_exit.assert_called_once_with(0)
                    assert fake_output.getvalue().strip() == "Hello, World!"

    def test_hello_world_hello_command(self) -> None:
        """Test that hello_world prints message with hello command."""
        with patch("sys.argv", ["finance", "hello"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                with patch("sys.exit") as mock_exit:
                    hello_world()
                    mock_exit.assert_called_once_with(0)
                    assert fake_output.getvalue().strip() == "Hello, World!"

    def test_hello_world_version_command(self) -> None:
        """Test that hello_world prints version with --version flag."""
        with patch("sys.argv", ["finance", "--version"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                with patch("sys.exit") as mock_exit:
                    hello_world()
                    mock_exit.assert_called_once_with(0)
                    output = fake_output.getvalue().strip()
                    # Should print a version string
                    assert len(output) > 0
                    # Version should contain dots (semantic versioning)
                    assert "." in output

    def test_hello_world_unknown_command(self) -> None:
        """Test that hello_world handles unknown commands."""
        with patch("sys.argv", ["finance", "unknown"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                with patch("sys.exit") as mock_exit:
                    hello_world()
                    mock_exit.assert_called_once_with(1)
                    output = fake_output.getvalue()
                    assert "Unknown command: unknown" in output
                    assert "Usage:" in output

    def test_get_version(self) -> None:
        """Test that get_version returns a version string."""
        version = get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_get_version_fallback(self) -> None:
        """Test that get_version returns fallback when package not found."""
        with patch("finance.hello.version", side_effect=PackageNotFoundError):
            version = get_version()
            assert version == "0.1.4"  # Fallback version


class TestModule:
    """Test cases for module-level functionality."""

    def test_module_import(self) -> None:
        """Test that the module can be imported."""
        import finance

        assert hasattr(finance, "hello_world")

    def test_version_exists(self) -> None:
        """Test that the version is defined."""
        assert __version__ is not None

    def test_version_format(self) -> None:
        """Test that version follows semantic versioning."""
        parts = __version__.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()

    def test_module_exports(self) -> None:
        """Test that __all__ is properly defined."""
        import finance

        assert hasattr(finance, "__all__")
        assert "hello_world" in finance.__all__
        assert "__version__" in finance.__all__
