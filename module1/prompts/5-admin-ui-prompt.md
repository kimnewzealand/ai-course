Based on the admin UI specifications, here's the recommended prompt:

---

I need help creating a comprehensive implementation plan for an admin web interface that supports the existing REST Web API. Please review the following specifications and create a detailed plan that includes dependencies with specific versions, file/folder structure, architectural patterns, code examples, testing strategy, and developer experience improvements. You must strictly adhere to ALL of the details provided below and not add any additional dependencies or features without explicit approval. If anything is unclear or you need more information, please ask for clarification.

## Technical Specifications

### Programming Language
- **Choice**: TypeScript (for logic), HTML (for structure), CSS (for styling)

### Dependencies
Use pnpm to manage dependencies and run scripts.

### Web Framework
- **Framework**: Vanilla TypeScript/HTML/CSS
- **Browser API**: Only use the `fetch` feature of modern browsers
- **No Frameworks**: Do not use React, Vue, Angular, or any other frontend frameworks

### API Integration
Use `@ai-course/modeule1/web-api-mvp/app/main.py` to understand which endpoints and payloads are available for:
- Adding and updating application entries
- Adding and updating configuration name/value pairs
Create UI in the `@ai-course/modeule1/web-api-mvp/ui/` folder.

### Features Required
- **Application Management**: UI for adding and updating application entries
- **Configuration Management**: UI for adding and updating configuration name/value pairs
- **API Integration**: Connect to the REST API endpoints using fetch
- **Form Validation**: Client-side validation for required fields and constraints

### Input Validation
- **Name**: Required, 1-100 characters
- **Description**: Optional, 0-500 characters
- **Configuration Keys/Values**: Appropriate validation based on API requirements

### Testing
- **Unit Testing**: vitest for component and utility function testing
- **Integration Testing**: Playwright for end-to-end UI testing
- **Coverage**: Unit tests for all UI features and API interactions

### Project Files
Update the following files:
- `README.md` with setup, run, test, and lint instructions
- `.env` template with API endpoint URLs
- `.gitignore` for web development files
- `package.json` with pnpm scripts and dependencies
- `tsconfig.json` for TypeScript configuration

### Developer Experience
- **Linting**: ESLint and Prettier configuration
- **Code Quality**: TypeScript strict mode, consistent formatting
- **Development Server**: Local development server with hot reload

### Deployment
- **Local Development**: Designed for local testing and development
- **Build Process**: pnpm-based build scripts
- **No Production Deployment**: Focus on development and testing

## Additional Requirements
- Add comprehensive error handling for API calls and user interactions
- Ensure all code follows TypeScript and web development best practices
- Implement responsive design for the admin interface
- Provide clear user feedback for form submissions and API responses
- Use modern CSS with custom properties and flexbox/grid layouts

Please provide a complete implementation plan that covers:

1. Project structure (folders and files for a web application)
2. Dependencies (pnpm packages for TypeScript, testing, linting)
3. Component architecture and file organization
4. API integration patterns using fetch
5. Form handling and validation
6. Error handling and user feedback
7. Testing strategy with vitest and Playwright
8. Build and development setup
9. File contents and configuration details

Ensure the plan follows modern web development best practices, provides excellent developer experience, and creates a maintainable admin interface for the REST API.
