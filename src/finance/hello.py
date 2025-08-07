"""Hello world module for testing CI/CD pipeline."""

import sys
from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    """Get the package version.

    Returns:
        str: The package version or 'unknown' if not found.
    """
    try:
        return version("finance")
    except PackageNotFoundError:
        return "0.1.4"  # Fallback version


def hello_world() -> None:
    """Main entry point for the finance CLI.

    Handles --version flag and hello command.
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version":
            print(get_version())
            sys.exit(0)
        elif sys.argv[1] == "hello":
            print("Hello, World!")
            sys.exit(0)
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Usage: finance [--version | hello]")
            sys.exit(1)
    else:
        # Default to hello for now
        print("Hello, World!")
        sys.exit(0)
