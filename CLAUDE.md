# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based financial data processing CLI tool with MCP (Model Context Protocol) server integration. The tool parses financial PDFs, processes CSV transaction data, and exposes these capabilities to AI assistants.

## Technology Stack

**Primary Language:** Python
**License:** MIT License (Tomasz Iniewicz, 2025)
**PDF Libraries:** Camelot (primary), pdfplumber, tabula-py (fallbacks), pytesseract (OCR for scanned documents)
**Data Processing:** pandas, numpy
**CLI Framework:** Click or Typer
**MCP Integration:** mcp-python-sdk

## Development Setup

1. Create a virtual environment using your preferred tool (pip, pipenv, poetry, pdm, uv, or pixi)
2. Install dependencies from `pyproject.toml` or `requirements.txt`
3. Set up linting with ruff and type checking with mypy
4. Run tests with pytest

## Code Architecture

```
finance/
├── src/
│   ├── finance_cli/      # Core CLI implementation
│   │   ├── __init__.py
│   │   ├── cli.py        # Main CLI entry point
│   │   ├── config.py     # Configuration management
│   │   └── utils.py      # Shared utilities
│   ├── parsers/          # PDF parsing modules
│   │   ├── __init__.py
│   │   ├── camelot_parser.py
│   │   ├── pdfplumber_parser.py
│   │   └── base_parser.py
│   ├── processors/       # CSV processing modules
│   │   ├── __init__.py
│   │   ├── merger.py
│   │   ├── categorizer.py
│   │   └── deduplicator.py
│   └── mcp_server/       # MCP server implementation
│       ├── __init__.py
│       ├── server.py
│       └── tools.py
├── tests/                # Test suite
├── examples/             # Example files and usage
└── docs/                 # Extended documentation
```

## CLI Command Structure

Following industry standards from tools like ledger-cli and hledger:

```bash
finance [global-options] <command> [command-options] [arguments]
```

### Core Commands
- `finance parse <file.pdf>` - Parse PDF financial statements
- `finance merge <file1.csv> <file2.csv> ...` - Merge CSV files
- `finance categorize <file.csv>` - Categorize transactions
- `finance config` - Manage configuration

## MCP Server Design

The MCP server groups related CLI commands into logical tools:

1. **parse_financial_documents** - PDF parsing operations
2. **process_transactions** - CSV merge/categorize/dedupe operations  
3. **manage_configuration** - Configuration management

Each MCP tool wraps the corresponding CLI commands, providing structured input/output for AI assistants.

## Important Guidelines

### PDF Parsing
- Use Camelot as the primary parser for table extraction
- Fall back to pdfplumber for complex layouts
- Consider tabula-py as an additional option
- Implement OCR support with pytesseract for scanned documents
- Support bank-specific templates for reliable parsing

### Data Processing
- All operations should support batch processing with glob patterns
- Default output to stdout unless --output specified
- Support piping for command chaining
- Use pandas for CSV operations
- Implement robust deduplication logic

### Configuration
- Store config in `~/.finance-cli/config.yaml`
- Support environment variable overrides
- Include sample configuration in repository
- Set appropriate file permissions (700/600)

### Error Handling
- Use structured exit codes: 0 (success), 1 (general error), 2 (usage error)
- Provide clear error messages to stderr
- Include progress indicators for batch operations

### Testing
- Write comprehensive tests for all parsers
- Test edge cases in CSV processing
- Mock external dependencies appropriately
- Aim for >80% code coverage

### Security
- Never log or expose sensitive financial data
- Process all data locally
- Set restrictive permissions on config files
- Document privacy considerations clearly

## Development Commands

```bash
# Run tests
pytest

# Lint code
ruff check .
ruff format .

# Type checking
mypy src/

# Build package
python -m build

# Install in development mode
pip install -e .
```

## Important Notes

- The `.gitignore` covers Python development comprehensively
- Choose one package manager and stick with it for consistency
- The project supports Jupyter notebooks for financial analysis prototyping
- All financial data processing happens locally for privacy
- The tool is designed primarily for macOS but should work cross-platform