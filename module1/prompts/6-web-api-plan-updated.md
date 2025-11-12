# Enhanced REST Web API Implementation Plan

## 1. Project Structure

```
web-api-mvp/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app with routers and health check
│   ├── database.py      # SQLAlchemy database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas with validation
│   └── crud.py          # CRUD operations
├── tests/
│   ├── __init__.py
│   └── test_api.py      # Comprehensive test suite
├── .env                 # Environment variables
├── .gitignore           # Git ignore rules
├── pyproject.toml       # Ruff configuration
├── README.md            # Documentation
└── requirements.txt     # Dependencies
```

## 2. Dependencies

Using exact versions as specified:
- **fastapi==0.104.1**: Web framework with OpenAPI docs
- **uvicorn[standard]==0.24.0**: ASGI server
- **pydantic==2.5.0**: Data validation with Field constraints
- **sqlalchemy==1.4.50**: ORM with SQLite support
- **python-dotenv==1.0.0**: Environment variable management
- **pytest==7.4.3**: Testing framework
- **httpx==0.25.2**: HTTP client for testing
- **pytest-asyncio==0.21.1**: Async testing support
- **ruff==0.1.9**: Fast Python linter

## 3. Database Schemas and Models

**Item Model** (`app/models.py`):
```python
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
```

**Database Configuration** (`app/database.py`):
- Environment-based DATABASE_URL
- Session management with proper cleanup
- SQLite with check_same_thread for safety

## 4. API Route Implementations with Versioning

**Router Structure** (`app/main.py`):
- `api_v1`: APIRouter with `/v1` prefix and "items" tags
- `api_root`: APIRouter for backward compatibility
- Separate route functions to avoid conflicts

**Endpoints**:
- CRUD operations for items with proper HTTP methods
- Pagination support (limit/offset)
- Path parameters for item IDs
- JSON request/response bodies

**Health Check**:
- `GET /health` endpoint with status and version info

## 5. Data Models and Validation

**Pydantic Schemas** (`app/schemas.py`):
```python
class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None
```

- Field-level validation with min/max lengths
- Optional fields properly typed
- ORM mode for SQLAlchemy integration

## 6. Error Handling and Health Checks

**Error Handling**:
- HTTPException for 404s and validation errors
- Consistent JSON error responses
- Proper status codes (200, 404, 422)

**Health Check**:
- Simple endpoint returning service status
- Includes API version for monitoring

## 7. Configuration Management

**Environment Variables** (`.env`):
```
DATABASE_URL=sqlite:///./items.db
```

**FastAPI App Config**:
- Title, description, version metadata
- Lifespan management for database initialization

## 8. Testing Strategy with Database Isolation

**Test Structure** (`tests/test_api.py`):
- Session-scoped fixtures for database setup/teardown
- Per-test database isolation with transactions
- Comprehensive test classes for different features

**Test Coverage**:
- CRUD operations (create, read, update, delete)
- Input validation (field constraints)
- API versioning (/v1/ vs root)
- Health check functionality
- Error handling (404s, validation errors)
- Pagination parameters

**Database Isolation**:
- Separate test database file
- Automatic cleanup after test sessions
- Transaction rollback for test isolation

## 9. Developer Experience Features

**Linting** (`pyproject.toml`):
- Ruff configuration with comprehensive rules
- Import sorting, code formatting, type checking
- Per-file ignores for special cases

**Documentation**:
- OpenAPI/Swagger UI auto-generation
- Endpoint summaries and descriptions
- Request/response examples

**Code Quality**:
- Type hints throughout
- Docstrings for functions
- Consistent naming and structure

## 10. File Contents and Setup Instructions

**README.md**:
- Installation with uv
- Virtual environment activation
- Running the server
- Testing commands
- Linting instructions
- API documentation access

**Setup Process**:
1. Install uv and create virtual environment
2. Install dependencies
3. Configure environment variables
4. Run database migrations (table creation)
5. Start development server
6. Run tests and linting

## Architecture Patterns

**Separation of Concerns**:
- Routes in main.py (API layer)
- Business logic in crud.py
- Data models in models.py
- Validation schemas in schemas.py
- Database config in database.py

**Dependency Injection**:
- FastAPI's Depends for database sessions
- Test overrides for database isolation

**RESTful Design**:
- Proper HTTP methods and status codes
- Resource-based URLs
- JSON request/response format
- Pagination for list endpoints

This implementation provides a production-ready foundation with excellent developer experience, comprehensive testing, and proper API design patterns.
