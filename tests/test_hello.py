"""Tests for the hello module."""

from finance import __version__, hello_world


class TestHelloWorld:
    """Test cases for the hello_world function."""

    def test_hello_world_returns_correct_message(self) -> None:
        """Test that hello_world returns the expected message."""
        result = hello_world()
        assert result == "Hello, World!"

    def test_hello_world_return_type(self) -> None:
        """Test that hello_world returns a string."""
        result = hello_world()
        assert isinstance(result, str)

    def test_hello_world_consistency(self) -> None:
        """Test that hello_world returns the same result consistently."""
        result1 = hello_world()
        result2 = hello_world()
        assert result1 == result2


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
