# Environment Setup for Web API MVP

The Web API MVP is designed to run in local development and production environments. All environments use the same SQLite database schema and FastAPI backend with a TypeScript client library and admin UI.

## Local Environment

### Prerequisites
- **Python 3.8+** with `uv` package manager
- **Node.js 18+** with `npm` package manager
- **Make**: For running project tasks

### Ports
- **API Service**: http://localhost:8000
- **UI Development**: http://localhost:3000 (Vite dev server)

### Environment Setup

1. **Dependencies**:
   - Backend: `uv venv && uv pip install -r requirements.txt` (or `uv sync --dev` if pyproject.toml includes dependencies)
   - Client Library: `cd client && npm install`
   - Admin UI: `cd ui && npm install`

2. **Database Setup**:
   - SQLite database is created automatically on first application startup.

## Non-Local Environment

Currently configured for local development only. Production deployment patterns to be established based on organizational infrastructure requirements.

Recommended deployment approach:
- **Backend**: Containerized FastAPI service with SQLite database
- **Client Library**: Publish to npm registry
- **Admin UI**: Static file hosting (CDN or web server)

## Environment-Specific Configs

No specific environment variables required for local development. The application uses default settings and auto-initializes the database.

## Deployment Rules

### Local Development
- Database initialized automatically on startup
- No build step required for development (live reloading)
- All components can run simultaneously

### Production Deployment
- **Backend**:
  - Ensure proper database path configuration if needed
  - Deploy FastAPI container
- **Client/UI**:
  - Build client: `cd client && npm run build`
  - Build UI: `cd ui && npm run build`
  - Deploy static assets

### CI/CD Pipeline Requirements
- Run full test suite: `make test`
- Code quality checks: `make lint`, `make format`
- Build validation: `make ui-build`

## Task Running

### IMPORTANT: Use Make Commands Only

**CRITICAL CONSISTENCY RULE**: All development tasks, verification processes, and regular operations MUST use Make commands. This ensures consistency across the entire development team and prevents configuration drift.

**When to use Make vs direct commands**:
- ✅ **ALWAYS Use Make For**: Development workflows, testing, building, deployment, code quality checks
- ⚠️  **Direct Commands Only For**: Specific troubleshooting, debugging individual components, one-off investigations

### Primary Task Runner: Make
All development tasks are orchestrated through the Makefile. Use `make help` to see all available commands:

```bash
make help          # Show available commands
make install       # Install all dependencies (backend, client, ui)
make test          # Run all tests (backend + ui)
make run-svc       # Start API server (localhost:8000)
make run-ui        # Start UI dev server (localhost:3000)
```

### Backend Tasks (Use Make Commands)
```bash
# Development workflow - USE THESE COMMANDS:
make run-svc       # Start development server
make test-svc      # Run backend tests (pytest)
make format        # Code formatting with ruff
make lint          # Code linting with ruff
make coverage-svc  # Tests with coverage analysis
```

### Frontend Tasks (Use Make + npm)
```bash
# Development workflow - USE THESE COMMANDS:
make run-ui        # Start Vite dev server (port 3000)
make test-ui       # Run Vitest tests
make ui-build      # Build UI for production
make client-build  # Build client library
make coverage-ui   # Tests with coverage analysis

# TypeScript validation (npm command - run in ui directory):
cd ui && npm run ts-check  # TypeScript validation (if available)
```

### Complete Development Workflow Commands
```bash
# Setup and Installation
make install     # Install all dependencies (backend, client, ui)

# Development Servers
make run-svc     # Start API development server (port 8000)
make run-ui      # Start UI development server (port 3000)

# Testing and Verification (REQUIRED BEFORE COMMITS)
make test        # Run all tests (backend + ui)
make lint        # Run Python linting checks
make format      # Format Python code with ruff

# Build and Deployment
make client-build  # Build client library
make ui-build      # Build UI for production deployment

# Cleanup
make clean       # Remove generated files and caches
```

### Quick Verification Workflow
```bash
# Run this sequence after changes:
make test && make lint && make format
