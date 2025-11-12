# REST Web API Specifications (Updated)

## Overview

This document contains updated details necessary to create a prompt for an enhanced REST Web API implementation. Please review the contents and recommend a PROMPT that can be sent to an AI coding assistant for help with creating an implementation plan for this service.

## Prompt Requirements

The recommended prompt should:
- ✅ Ask the assistant to create a **comprehensive plan** that includes dependencies, file/folder structure, architectural patterns, testing, and developer experience improvements
- ✅ Recommend **strict adherence** to ALL of the details in this document
- ✅ Strongly encourage the assistant to **not add any additional dependencies** without approval
- ✅ Encourage the assistant to **ask for more information** if they need it

## Technical Specifications

### Programming Language
- **Choice**: Python

### Dependencies
Python libraries and specific versions:
```python
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==1.4.50
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
pytest-asyncio==0.21.1
ruff==0.1.9
```

### Web Framework & ASGI Server
- **Framework**: FastAPI with automatic OpenAPI documentation
- **Server**: Uvicorn ASGI server
- **Features**: Lifespan management, dependency injection, response models

### API Design
**Endpoints and Payloads** (with versioning and backward compatibility):
- `GET /v1/items` & `GET /items` - Retrieve a list of items (query parameters: `limit`, `offset`)
- `POST /v1/items` & `POST /items` - Create a new item (payload:
  ```json
  {
    "name": "string (1-100 chars)",
    "description": "string (0-500 chars, optional)"
  }
  ```
  )
- `GET /v1/items/{id}` & `GET /items/{id}` - Retrieve a specific item by ID
- `PUT /v1/items/{id}` & `PUT /items/{id}` - Update an existing item (same payload as POST)
- `DELETE /v1/items/{id}` & `DELETE /items/{id}` - Delete an item by ID

**Health Check**:
- `GET /health` - Service health status

*All endpoints should return appropriate HTTP status codes and error responses in JSON format, following REST API best practices.*

### Input Validation
- **Name**: Required, 1-100 characters
- **Description**: Optional, 0-500 characters
- **ID**: Integer path parameter
- **Pagination**: limit (int, default 10), offset (int, default 0)

### Database & Storage
- **Engine**: SQLite with aiosqlite-style connection
- **ORM**: SQLAlchemy with async support
- **Models**: Item table with fields: id, name, description, created_at, updated_at
- **Timestamps**: Stored as ISO format strings

### Testing
- **Framework**: pytest with database isolation
- **Coverage**: Unit tests for all CRUD operations, validation, versioning, health check
- **Database**: Separate test database with automatic cleanup

### Project Files
Create and populate the following files:
- `README.md` with setup, run, test, and lint instructions
- `.env` template with DATABASE_URL
- `.gitignore` for Python and database files
- `pyproject.toml` with ruff linting configuration
- `requirements.txt` with exact versions

### Developer Experience
- **Linting**: Ruff configuration with comprehensive rules
- **Code Quality**: Type hints, docstrings, consistent formatting
- **API Documentation**: OpenAPI/Swagger UI with tags and summaries
- **Versioning**: /v1/ endpoints with backward compatibility
- **Health Monitoring**: Dedicated health check endpoint

### Deployment
- **Local Development**: Designed for local testing and development
- **Virtual Environment**: uv-based environment management
- **No Production Deployment**: Focus on development and testing

## Additional Requirements
- Use APIRouter for API versioning
- Implement proper dependency injection
- Add comprehensive error handling
- Include request/response models with descriptions
- Ensure all code follows Python best practices
- Provide clear separation of concerns (routes, models, schemas, CRUD)
