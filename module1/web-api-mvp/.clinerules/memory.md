# Memory

## Role
Provide expert guidance as a software engineer experienced in TypeScript, web client libraries, and collaborative development practices. Use the context framework to maintain persistent project knowledge while guiding implementation of the config service web client library.

## Purpose
This context framework provides persistent project knowledge and decision rationales to inform all collaboration sessions. By loading these documents automatically, we maintain consistency in understanding, reduce repetition, and enable better decision-making for the web client library implementation.

## Scope
The context framework covers high-level project definition through specific implementation details, created collaboratively to document understanding and guide ongoing development of the TypeScript web client library for the config service.

## Document Structure

### cline_project/memory/ABOUT.md
- High-level project overview with description, justification, and stakeholder personas
- Domain context, implementation scope, and success criteria
- Essential for validating direction and understanding project goals

### cline_project/memory/DOMAIN.md
- Domain-specific knowledge and business rules
- Core problem space, data models, and user journeys
- Critical context for feature design and requirement analysis

### cline_project/memory/ARCHITECTURE.md
- System architecture decisions and technology stack choices
- Component relationships, data flow patterns, and integration points
- Blueprint for how the client library connects to the broader ecosystem

### cline_project/memory/TECHNICAL.md
- Implementation patterns, coding conventions, and development standards
- Tooling preferences, dependency management, and quality expectations
- Specific guidance for consistent code practices and patterns

### cline_project/memory/TESTING.md
- Testing strategy including unit, integration, and end-to-end approaches
- Automation frameworks, quality gates, and CI/CD pipeline requirements
- Standards for ensuring reliability and maintainability through comprehensive test coverage

## Usage
- Reference these documents by including file paths in prompts (e.g., "@cline_project/memory/ABOUT.md")
- Use BEFORE planning: "@cline_project/memory/ files for context before creating plans"
- Use DURING implementation: "@cline_project/memory/ files to validate against established decisions"
- Updates should follow plan-first protocol: create plan referencing existing context, then implement changes collaboratively
