# Technical Implementation Guide

## Development Practices

### Coding Standards
- **Python**: Follow PEP 8 with line length of 88 characters (ruff configuration)
- **TypeScript**: Use strict typing, avoid `any` types, consistent naming conventions
- **Import Style**: Isort automatic sorting with Ruff
- **Data Classes**: Pydantic models for Python, interfaces for TypeScript

### Code Formatting and Linting
- **Ruff**: Combined linter and formatter for Python
  - Selects basic error checking, warning detection, and code quality
  - Ignores line length (handled by formatter), complex code warnings for tests


## Testing Strategy

### Testing Pyramid
- **Unit Tests**: 70% coverage minimum, test business logic and utilities
- **Integration Tests**: API endpoint testing with real database (pytest fixtures)
- **End-to-End Tests**: Full user workflows (Playwright for frontend)

### Python Backend Testing
- **Framework**: Pytest with FastAPI test client
- **Database Testing**: Separate test database, transaction rollback per test
- **Fixtures**: Reusable test data (sample items, users, configurations)
- **Test Organization**: Class-based test suites with descriptive method names

### TypeScript Frontend Testing
- **Unit Tests**: Vitest with React Testing Library
- **E2E Tests**: Playwright with realistic scenarios
- **Test Data**: Mock HTTP responses, fixture data for consistent testing

## API Design Patterns

### RESTful Conventions
- **Resource-Based URLs**: `/v1/applications`, `/v1/configs`
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: 200 (success), 201 (created), 400 (bad request), 404 (not found), 422 (validation error)
- **Endpoint Organization**: Logical grouping, version prefixes (/v1/)

### Error Handling
- **Standardized Error Responses**: {"detail": "Error message"}
- **Validation Errors**: Automatic 422 responses with field-specific messages
- **Authorization Errors**: 403 Forbidden for permission issues
- **Logging**: Server-side error logging with correlation IDs
