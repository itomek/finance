# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based historical financial analysis and future planning tool with an API-first architecture. It processes bank statements (PNC) and brokerage statements (Robinhood) to provide insights, trends, and projections through both a CLI and MCP server for AI assistants.

**Key Focus**: This is NOT a real-time financial tracker. It analyzes completed statements to identify patterns and help users plan their financial future based on historical data.

## Technology Stack

**Primary Language:** Python
**License:** MIT License (Tomasz Iniewicz, 2025)
**API Framework:** FastAPI with uvicorn
**Database:** SQLite with SQLAlchemy ORM
**PDF Libraries:** Camelot (primary), pdfplumber, tabula-py (fallbacks), pytesseract (OCR)
**Data Processing:** pandas, numpy, scikit-learn
**MCP Integration:** mcp-python-sdk (wraps API endpoints)
**Security:** cryptography for encryption, python-jose for JWT

## Development Setup

1. Create a virtual environment using your preferred tool (pip, pipenv, poetry, pdm, uv, or pixi)
2. Install dependencies from `pyproject.toml` or `requirements.txt`
3. Set up linting with ruff and type checking with mypy
4. Run tests with pytest

## Code Architecture

```
finance/
├── src/
│   ├── api/              # Core REST API (FastAPI)
│   │   ├── __init__.py
│   │   ├── main.py       # FastAPI app entry point
│   │   ├── routes/       # API endpoint definitions
│   │   ├── models/       # Pydantic models
│   │   ├── services/     # Business logic layer
│   │   └── auth.py       # Authentication
│   ├── parsers/          # Institution-specific parsers
│   │   ├── __init__.py
│   │   ├── base_parser.py
│   │   ├── pnc_parser.py
│   │   └── robinhood_parser.py
│   ├── processors/       # Data processing & validation
│   │   ├── __init__.py
│   │   ├── validator.py  # Mathematical validation
│   │   ├── deduplicator.py
│   │   └── staging.py    # Import staging pipeline
│   ├── analysis/         # Historical analysis
│   │   ├── __init__.py
│   │   ├── spending.py
│   │   ├── income.py
│   │   ├── investments.py
│   │   └── trends.py
│   ├── planning/         # Future projections
│   │   ├── __init__.py
│   │   ├── projections.py
│   │   ├── scenarios.py
│   │   └── affordability.py
│   ├── insights/         # AI-powered insights
│   │   ├── __init__.py
│   │   ├── patterns.py
│   │   └── recommendations.py
│   ├── database/         # Database layer
│   │   ├── __init__.py
│   │   ├── models.py     # SQLAlchemy models
│   │   └── migrations/   # Alembic migrations
│   └── mcp_server/       # MCP wrapper for API
│       ├── __init__.py
│       ├── server.py
│       └── tools.py      # MCP tool definitions
├── tests/                # Comprehensive test suite
├── templates/            # Institution parsing templates
└── docs/                 # Extended documentation
```

## API-First Architecture

The system is built around a REST API that all clients (CLI, MCP, future web UI) consume:

### API Endpoints Structure
```
/api/v1/
├── /import/          # Statement import and validation
├── /analysis/        # Historical analysis endpoints
├── /planning/        # Future projection endpoints
├── /insights/        # AI-generated insights
├── /reports/         # Report generation
└── /config/          # Configuration management
```

### API Access
The API will be accessed through:
- **MCP Server**: Primary interface for AI assistants
- **Direct API**: For future web UI or other integrations
- **No CLI**: All functionality exposed through API endpoints only

## MCP Server Design

The MCP server wraps API endpoints to provide conversational financial analysis:

### Import & Validation Tools
- **import_statements** - Process bank/brokerage statements
- **validate_staged_data** - Review mathematical validation results
- **resolve_issues** - Handle duplicates and discrepancies

### Analysis Tools
- **analyze_spending** - Historical spending patterns
- **analyze_portfolio** - Investment performance analysis
- **net_worth_analysis** - Complete financial picture
- **financial_health_check** - Comprehensive assessment

### Planning Tools
- **project_cash_flow** - Future income/expense projections
- **calculate_affordability** - Test purchase/loan scenarios
- **scenario_planning** - Complex what-if analysis
- **investment_projections** - Portfolio growth modeling

### Insights & Reporting
- **get_insights** - AI-powered pattern detection
- **generate_dashboard** - Markdown report generation
- **search_transactions** - Query historical data

## Important Guidelines

### Data Import & Validation
- **Staging First**: Always import to staging area before database commit
- **Mathematical Validation**: Verify balances reconcile (beginning + transactions = ending)
- **Duplicate Detection**: Use fuzzy matching with configurable thresholds
- **User Confirmation**: Require explicit approval for imports with issues
- **Institution Templates**: Use YAML templates for parser configuration

### Historical Analysis Focus
- **Completed Periods Only**: Analyze full statements, not partial data
- **Pattern Detection**: Look for trends across multiple periods
- **Statistical Significance**: Require sufficient data for projections
- **Seasonality Awareness**: Account for cyclical patterns
- **Multi-Account Correlation**: Analyze relationships between accounts

### Future Planning
- **Confidence Intervals**: Always provide uncertainty ranges
- **Multiple Scenarios**: Best/worst/likely case projections
- **Historical Basis**: Ground all projections in actual data
- **Assumption Transparency**: Clearly state all assumptions
- **Monte Carlo Simulations**: For complex uncertainty modeling

### Security & Privacy
- **Encryption at Rest**: Use SQLite encryption extension
- **PII Masking**: Always mask account numbers in logs/exports
- **Audit Trail**: Log all data access with timestamps
- **Secure Deletion**: Cryptographic erasure for sensitive data
- **Local-Only Processing**: No external API calls for data

### API Design
- **RESTful Principles**: Use proper HTTP verbs and status codes
- **Pagination**: Support for large result sets
- **Async Operations**: Long-running tasks return job IDs
- **Versioning**: Include version in URL (/api/v1/)
- **OpenAPI Documentation**: Auto-generate from code

### Testing Requirements
- **Unit Tests**: All parsers and processors >90% coverage
- **Integration Tests**: Full import pipeline testing
- **Validation Tests**: Mathematical accuracy verification
- **Performance Tests**: Handle large statement files
- **Security Tests**: Attempt common attack vectors

## Development Commands

```bash
# Start API server
uvicorn src.api.main:app --reload

# Run tests
pytest
pytest tests/validation/ -v  # Run validation tests specifically

# Lint and format
ruff check .
ruff format .

# Type checking
mypy src/

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "Description"

# Build package
python -m build

# Install in development mode
pip install -e .
```

## Data Storage Structure

```
~/.finance-cli/
├── config.yaml           # User configuration
├── finance_history.db    # SQLite database (encrypted)
├── staging/              # Import staging area
│   └── {import_id}/      # Per-import session
│       ├── raw/          # Original files
│       ├── parsed/       # Parsed data
│       └── validation/   # Validation results
├── imports/              # Archived imports
├── templates/            # Institution templates
│   ├── pnc.yaml
│   └── robinhood.yaml
├── analysis/             # Cached analysis results
└── reports/              # Generated reports
```

## Important Notes

- **API-First**: All functionality exposed through REST API
- **Historical Focus**: Designed for past data analysis, not real-time tracking
- **Institution Support**: Initially PNC and Robinhood, extensible via templates
- **Privacy-First**: All processing local, no cloud dependencies
- **Cross-Platform**: API enables platform-agnostic clients