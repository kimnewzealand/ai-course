# Admin Web UI Specifications 

## Overview

This document contains updated details necessary to create a prompt for an admin web interface to support the existing REST Web API implementation. Please review the contents and recommend a PROMPT that can be sent to an AI coding assistant for help with creating an implementation plan for this service.

The admin web interface should have features for adding and updating application entries as well as adding and updating the configuration name/value pairs.

## Prompt Requirements

The recommended prompt should:
- ✅ Ask the assistant to create a **comprehensive plan** that includes dependencies, file/folder structure, architectural patterns, testing, and developer experience improvements
- ✅ Recommend **strict adherence** to ALL of the details in this document
- ✅ Strongly encourage the assistant to **not add any additional dependencies** without approval
- ✅ Encourage the assistant to **ask for more information** if they need it

## Technical Specifications

### Programming Language
- **Choice**: TypeScript (for logic), HTML (for structure), CSS (for styling)

### Dependencies
Use pnpm to manage dependencies and run scripts.
Use specific library versions:

### Web Framework 
- **Framework**: All code should either be TypeScript, HTML, or CSS.
Only use the `fetch` feature of  modern browsers. 

### API Endpoints
Use `@config-service/svc/api/endpoints.py` to understand which endpoints and payloads are available.


### Input Validation
- **Name**: Required, 1-100 characters
- **Description**: Optional, 0-500 characters

### Testing
- **Framework**: unit testing with vitest and integration testing with Playwright.
- **Coverage**: Unit tests for all UI features

### Project Files
Update the following files:
- `README.md` with setup, run, test, and lint instructions
- `.env` template with DATABASE_URL
- `.gitignore` for Python and database files
- `pyproject.toml` with ruff linting configuration
- `requirements.txt` with exact versions

### Developer Experience
- **Linting**: Ruff configuration with comprehensive rules
- **Code Quality**: Type hints, docstrings, consistent formatting

### Deployment
- **Local Development**: Designed for local testing and development
- **Virtual Environment**: uv-based environment management
- **No Production Deployment**: Focus on development and testing

## Additional Requirements
- Add comprehensive error handling
- Ensure all code follows Python best practices