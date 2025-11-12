# REST Web API Specifications

## Overview

This document contains details necessary to create a prompt, which will later be used to create an implementation plan for a REST Web API. Please review the contents of this file and recommend a PROMPT that can be sent to an AI coding assistant for help with creating a plan for this service.

## Prompt Requirements

The recommended prompt should:

- ✅ Ask the assistant to create a __minimal plan__ that includes dependencies, file/folder structure, and architectural patterns for an __MVP__
- ✅ Recommend __strict adherence__ to ALL of the details in this document
- ✅ Strongly encourage the assistant to __not add any additional dependencies__ without approval
- ✅ Encourage the assistant to __ask for more information__ if they need it

## Technical Specifications

### Programming Language

- __Choice__: Python

### Dependencies

Python libraries and specific versions:

```python
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy[asyncio]==2.0.23
aiosqlite==0.19.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
pytest-asyncio==0.21.1
```

### API Design

__Endpoints and Payloads__:

- __GET /items__ - Retrieve a list of items (query parameters for pagination: `limit`, `offset`)

- __POST /items__ - Create a new item (payload:

  ```json
  {
    "name": "string",
    "description": "string",
    "price": 0.0
  }
  ```

  )

- __GET /items/{id}__ - Retrieve a specific item by ID

- __PUT /items/{id}__ - Update an existing item (payload: same as POST)

- __DELETE /items/{id}__ - Delete an item by ID

*All endpoints should return appropriate HTTP status codes and error responses in JSON format, following REST API best practices.*

### Database & Storage

- __Migration__: This is a new project. *No migration is needed.*

### Testing

- __Strategy__: Add minimal pytest unit tests for the API endpoints

### Project Files

Create and populate the following files:

- `README.md` file with instructions on how to run and test the API locally. *Use uv for virtual environment management*
- `.env` file template
- `.gitignore` file

### Deployment

- __Preferences__: Do not provide any specific instructions for deployment. *This web API will be locally run and tested for now.*
