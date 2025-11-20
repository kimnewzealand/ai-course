# Web API MVP

A complete configuration management system with REST API backend, TypeScript client library, and web admin interface.

## Project Components

- **Backend API** (`/app`): FastAPI server with SQLite database
- **Client Library** (`/client`): TypeScript library for easy API integration
- **Admin UI** (`/ui`): Web interface for managing configurations

## Features

- ✅ **REST API**: CRUD operations with validation and versioning
- ✅ **TypeScript Client**: Simple wrapper for API consumption
- ✅ **Web Interface**: Modern admin UI for configuration management
- ✅ **Comprehensive Testing**: Unit, integration, and E2E tests
- ✅ **Developer Experience**: Linting, type safety, documentation

## Prerequisites

- **Python 3.8+** with `pip`
- **Node.js 18+** with `npm` (for client library and UI)
- **npm** (for UI): `npm install -g npm`

## Backend API Setup

### Install and Run

```bash
cd web-api-mvp

# Install uv package manager
pip install uv

# Create virtual environment
uv venv

# Activate environment
# Git Bash: source .venv/Scripts/activate
# Linux/Mac: source .venv/bin/activate
# Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run API server
uvicorn app.main:app --reload
```

**API available at**: `http://localhost:8000/docs`

### API Endpoints

- `GET /v1/items` - List items with pagination
- `POST /v1/items` - Create new item
- `GET /v1/items/{id}` - Get item by ID
- `PUT /v1/items/{id}` - Update item
- `DELETE /v1/items/{id}` - Delete item
- `GET /health` - Health check

**API Documentation**: `http://localhost:8000/docs`

## Client Library

The TypeScript client library simplifies API integration for applications.

### Development Setup

```bash
cd client

# Install dependencies
npm install

# Build library
npm run build

# Run tests
npm test
```

## Admin UI

Modern web interface for managing configurations through the API.

### Setup and Run

```bash
cd ui

# Install dependencies
npm install

# Start development server (requires API running)
npm run dev
```

**UI available at**: `http://localhost:3000`

### Development Commands

```bash
npm lint         # Code linting
npm dev          # Development server
npm test         # Unit tests
npm test:e2e     # End-to-end tests
```

## Development Workflow

1. **Start Backend**: Run API server first
2. **Develop Client**: Build library, integrate with applications
3. **Develop UI**: Build admin interface
4. **Test Integration**: Ensure all components work together

## Project Structure

```
web-api-mvp/
├── app/                 # FastAPI backend
├── client/              # TypeScript client library
├── ui/                  # Admin web interface
├── tests/              # Backend integration tests
├── pyproject.toml      # Python config
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Contributing

1. Follow existing code style and conventions
2. Add tests for new features
3. Update documentation as needed
4. Ensure cross-component compatibility

## License

MIT
