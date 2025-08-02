# Finance Analysis & Planning Tool

A comprehensive historical financial analysis and future planning tool that processes bank and brokerage statements to provide insights, trends, and projections. Built with Python, API-first architecture, and MCP integration for AI assistants.

## Overview

This tool analyzes your financial history to help you understand patterns and plan for the future:
- **Historical Analysis**: Process past bank statements (PNC) and brokerage statements (Robinhood)
- **Trend Detection**: Identify spending patterns, income trends, and investment performance
- **Future Planning**: Project cash flows, test affordability scenarios, and model "what-if" situations
- **AI Integration**: Connect with LM Studio, Claude, or other AI assistants via MCP for conversational analysis

**Note**: This is NOT a real-time financial tracking tool. It focuses on analyzing completed statements to provide insights and projections based on historical data.

## Key Features

### Data Import & Validation
- **Multi-Source Support**: Parse PDFs from PNC Bank and Robinhood (more institutions coming)
- **Staging Pipeline**: Validate data mathematically before committing to database
- **Duplicate Detection**: Intelligent detection across imports with fuzzy matching
- **Balance Reconciliation**: Ensure mathematical accuracy of all statements

### Historical Analysis
- **Spending Patterns**: Identify trends, categories, and anomalies in your spending
- **Income Analysis**: Track multiple income sources and their stability
- **Investment Performance**: Monitor portfolio returns, dividends, and trading patterns
- **Net Worth Tracking**: See how your overall financial position evolves over time

### Future Planning
- **Cash Flow Projections**: Forecast future income and expenses based on historical patterns
- **Affordability Calculator**: Test scenarios like "Can I afford a $40k car loan?"
- **What-If Analysis**: Model changes to spending, income, or investments
- **Goal Planning**: Set and track progress toward financial objectives

### Privacy & Security
- **Local Processing**: All data stays on your machine
- **Encrypted Storage**: Financial data encrypted at rest
- **No External Services**: No cloud dependencies or data transmission
- **Audit Trail**: Complete history of all data operations

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

The tool is designed to be used through AI assistants via the MCP server. You can ask questions like:
- "What were my dining expenses last year?"
- "Can I afford a $2,000/month mortgage based on my income history?"
- "Show me my investment performance over the past 2 years"
- "If I reduce dining out by 30%, how much could I save annually?"
- "Project my net worth for the next 5 years"

### Configuration

The tool stores all data in `~/.finance-cli/`:

```
~/.finance-cli/
├── config.yaml           # Configuration
├── finance_history.db    # SQLite database with all financial data
├── staging/              # Temporary import staging area
├── imports/              # Archived statements
├── templates/            # Institution-specific parsing templates
└── reports/              # Generated analysis reports
```

## MCP Server Integration

The MCP server exposes financial analysis capabilities to AI assistants like LM Studio:

### Available MCP Tools

#### Import & Processing
- `import_statements` - Import bank/brokerage statements with validation
- `validate_staged_data` - Review validation results before committing
- `resolve_issues` - Handle duplicates and discrepancies

#### Analysis Tools
- `analyze_spending` - Analyze spending patterns by period/category
- `analyze_portfolio` - Investment performance and allocation analysis
- `net_worth_analysis` - Comprehensive financial position over time
- `financial_health_check` - Overall financial health assessment

#### Planning Tools
- `project_cash_flow` - Forecast future income and expenses
- `calculate_affordability` - Test loan/purchase affordability
- `scenario_planning` - Run complex what-if scenarios
- `investment_projections` - Model portfolio growth

#### Insights & Reporting
- `get_insights` - AI-generated insights and recommendations
- `generate_dashboard` - Create markdown dashboards
- `search_transactions` - Query historical transactions

## Architecture

### API-First Design

```
         ┌─────────────────┐     ┌─────────────────┐
         │   MCP Server    │     │   Web UI        │
         │   (Wrapper)     │     │   (Future)      │
         └────────┬────────┘     └────────┬────────┘
                  │                        │
                  └────────────┬───────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Core REST API    │
                    │     (FastAPI)       │
                    └──────────┬──────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌────────▼────────┐     ┌────────▼────────┐     ┌───────▼────────┐
│ Import Pipeline │     │ Analysis Engine │     │ Planning Engine │
│   & Validation  │     │   & Insights    │     │  & Projections │
└────────┬────────┘     └────────┬────────┘     └───────┬────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                      ┌──────────▼──────────┐
                      │   SQLite Database   │
                      │  (Historical Data)  │
                      └─────────────────────┘
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
│   ├── api/              # Core REST API (FastAPI)
│   │   ├── routes/       # API endpoints
│   │   ├── models/       # Request/response models
│   │   └── services/     # Business logic
│   ├── parsers/          # Statement parsing (PNC, Robinhood)
│   ├── processors/       # Transaction processing & validation
│   ├── analysis/         # Historical analysis engine
│   ├── planning/         # Future projection engine
│   ├── insights/         # AI-powered insights
│   └── mcp_server/       # MCP wrapper for API
├── tests/                # Comprehensive test suite
├── templates/            # Institution parsing templates
└── docs/                 # Extended documentation
```

## Dependencies

- **API Framework**: FastAPI, uvicorn, pydantic
- **PDF Parsing**: Camelot, pdfplumber, tabula-py, pytesseract
- **Data Processing**: pandas, numpy, scikit-learn
- **Database**: SQLite with SQLAlchemy ORM
- **MCP Integration**: mcp-python-sdk
- **Security**: cryptography, python-jose

## Privacy & Security

- **100% Local**: All processing happens on your machine - no cloud services
- **Encrypted Storage**: Database and sensitive files encrypted at rest
- **Data Anonymization**: Built-in tools for anonymizing exports
- **Audit Trail**: Complete logging of all data access and modifications
- **Secure Deletion**: Cryptographic erasure of deleted data
- **Access Control**: API key authentication and rate limiting

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to the `main` branch.

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Tomasz Iniewicz