This document contains details necessary to create a prompt, which will later be used to create an implementation plan for a REST Web API. Please review the contents of this file and recommend a PROMPT that can be sent to an AI coding assistant for help with creating a plan for this service. 

The prompt should:
- ask the assistant to create a minimal plan that includes dependencies, file/folder structure, and architectural patterns for an MVP.
- recommend strict adherence to ALL of the details in this document.
- strongly encourage the assistant to not add any additional dependencies without approval.
- encourage the assistant to ask for more information if they need it.

- Programming language choice: Python

Python libraries and specific versions:
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy[asyncio]==2.0.23
aiosqlite==0.19.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
pytest-asyncio==0.21.1

- API endpoints and payloads details : 
  - GET /items - Retrieve a list of items (query parameters for pagination: limit, offset)
  - POST /items - Create a new item (payload: {"name": "string", "description": "string", "price": float})
  - GET /items/{id} - Retrieve a specific item by ID
  - PUT /items/{id} - Update an existing item (payload: same as POST)
  - DELETE /items/{id} - Delete an item by ID All endpoints should return appropriate HTTP status codes and error responses in JSON format, following REST API best practices.

- Migration : This is a new project. No migration is needed.
- Testing : Add minimal pytest unit tests for the API endpoints.
- Create the following files:
  README.md file with instructions on how to run and test the API locally. use uv for virtual environment management
  .env file template
.gitignore file
- Deployment preferences : Do not provide any specific instructions for deployment. This web api will be locally run and tested for now.
