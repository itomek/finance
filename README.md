# Finance CLI

A powerful command-line tool for parsing financial documents, processing transactions, and managing personal finance data. Built with Python and designed for macOS.

## Overview

Finance CLI helps automate common financial data processing tasks:
- Extract transaction data from PDF bank statements
- Merge and deduplicate CSV transaction files
- Categorize transactions using customizable rules
- Integrate with AI assistants via MCP (Model Context Protocol)

## Features

- **PDF Parsing**: Extract tables from bank statements using Camelot, with fallback options for complex layouts
- **CSV Processing**: Merge multiple transaction files, remove duplicates, and standardize formats
- **Transaction Categorization**: Apply rules-based categorization for expense tracking
- **Batch Processing**: Process multiple files with glob patterns
- **MCP Integration**: Use with Claude, LM Studio, or Open WebUI for AI-assisted financial workflows
- **Local Storage**: All data processed locally for privacy

## Installation

### Via Homebrew (Coming Soon)

```bash
brew tap itomek/finance
brew install finance-cli
```

### From Source

```bash
git clone https://github.com/itomek/finance.git
cd finance
pip install -e .
```

## Usage

### Basic Commands

```bash
# Parse a PDF bank statement
finance parse statement.pdf --output transactions.csv

# Merge multiple CSV files
finance merge account1.csv account2.csv --output combined.csv --dedupe

# Categorize transactions
finance categorize transactions.csv --rules ~/.finance-cli/rules.yaml

# Batch process multiple PDFs
finance parse *.pdf --output-dir processed/
```

### Configuration

Finance CLI stores configuration and data in `~/.finance-cli/`:

```bash
# Initialize configuration
finance config --init

# Show configuration
finance config --show

# Edit configuration
finance config --edit
```

## MCP Server Integration

The Finance CLI includes an MCP server that exposes financial operations to AI assistants:

1. Install the MCP server:
   ```bash
   finance-mcp install
   ```

2. Configure your AI assistant to use the Finance MCP server

3. Available MCP tools:
   - `parse_financial_documents` - Parse PDFs into structured data
   - `process_transactions` - Merge, categorize, and transform CSVs
   - `manage_configuration` - Get/set configuration options

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   CLI Tool      │────▶│   MCP Server    │
│  (Python)       │     │   (Wrapper)     │
└─────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Direct Users   │     │  AI Assistants  │
│                 │     │ (Claude, etc.)  │
└─────────────────┘     └─────────────────┘
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/itomek/finance.git
cd finance

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy src/
```

### Project Structure

```
finance/
├── src/
│   ├── finance_cli/      # Core CLI implementation
│   ├── parsers/          # PDF parsing modules
│   ├── processors/       # CSV processing modules
│   └── mcp_server/       # MCP server implementation
├── tests/                # Test suite
├── examples/             # Example files and usage
└── docs/                 # Extended documentation
```

## Dependencies

- **PDF Parsing**: Camelot, pdfplumber, tabula-py
- **Data Processing**: pandas, numpy
- **CLI Framework**: Click or Typer
- **MCP Integration**: mcp-python-sdk

## Privacy & Security

- All processing happens locally on your machine
- No data is sent to external servers
- Configuration files are stored with restricted permissions (700/600)
- Financial data remains under your control

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to the `main` branch.

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Tomasz Iniewicz