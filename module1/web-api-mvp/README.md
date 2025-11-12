# Web API MVP

A REST API for managing items with FastAPI, featuring input validation, API versioning, health checks, and comprehensive testing.

## Features

- ✅ **CRUD Operations**: Create, Read, Update, Delete items
- ✅ **Input Validation**: Pydantic models with field constraints
- ✅ **API Versioning**: `/v1/` prefixed endpoints with backward compatibility
- ✅ **Health Checks**: `/health` endpoint for monitoring
- ✅ **OpenAPI Documentation**: Auto-generated docs with tags
- ✅ **Automated Unit Testing**: Unit tests with database isolation
- ✅ **Linting**: Ruff configuration for code quality

## Setup

1. Install uv: `pip install uv`
2. Create virtual environment: `uv venv`
3. Activate: `source .venv/Scripts/activate` (Windows Git Bash) or `source .venv/bin/activate` (Linux/Mac)
4. Install dependencies: `uv pip install -r requirements.txt`

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

## Lint

```bash
ruff check .
ruff format .
```

## API Endpoints

### Items API (v1)
- `GET /v1/items` - List items with pagination
- `POST /v1/items` - Create new item
- `GET /v1/items/{id}` - Get item by ID
- `PUT /v1/items/{id}` - Update item
- `DELETE /v1/items/{id}` - Delete item

### Health Check
- `GET /health` - Service health status

### Backward Compatibility
All endpoints also work without `/v1/` prefix for backward compatibility.

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Validation Rules

- **Name**: 1-100 characters, required
- **Description**: 0-500 characters, optional
- **Pagination**: `limit` (default 10), `offset` (default 0)
