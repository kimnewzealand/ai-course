---
type: "always_apply"
---

# Project Guidelines

## Project Context

**Before starting any task:**
1. Review Augment rules in `.augment/rules/` directory
2. Review existing documentation (README.md, CONTRIBUTING.md, docs/, etc.)
3. Understand the project's tech stack and architecture
4. Check for project-specific conventions and patterns
5. Review recent changes and current priorities

**Augment Rules** (for AI context - automatically loaded):
- `.augment/rules/about.md` - Project overview, goals, purpose, and technology stack
- `.augment/rules/conventions.md` - Coding standards, naming conventions, and patterns
- `.augment/rules/development.md` - **CRITICAL: Make commands workflow** - ALWAYS use Make commands for development tasks

**Project Documentation** (for human developers):
- `README.md` - Project overview, setup instructions, and quick start
- `CONTRIBUTING.md` - Developer workflow, Make commands, testing, and contribution guidelines
- `docs/ARCHITECTURE.md` - Detailed system design, component relationships, and architectural decisions
- `CHANGELOG.md` - Release history, completed features, and stakeholder communication (semantic versioning)

## General Rules

- **Don't be sycophantic** - Skip flattery, respond directly
- **Be concise** - Keep responses brief and actionable
- **Ask when uncertain** - Request clarification rather than making assumptions
- **Cite your sources** - When responding to user requests, explicitly state which rules and memory documents you referenced to inform your response


## Code Style
- Follow the existing naming conventions in the codebase
- Check `.augment/rules/conventions.md` for project-specific coding standards
- Maintain consistency with existing code patterns

## Testing
- Write unit tests for all new functions
- Follow existing test patterns and organization
- Mock external dependencies (APIs, databases, services)


## Security Rules

- **Never commit secrets** - Use environment variables or secret management tools
- **Validate all inputs** - Sanitize and validate user data on both client and server
- **Use parameterized queries** - Prevent SQL injection attacks
- **Authentication & Authorization** - Implement proper auth checks
- **HTTPS only** - Use HTTPS only
- **Security headers** - Set appropriate security headers (CSP, HSTS, etc.)
- **Principle of least privilege** - Grant minimum necessary permissions
- **Error messages** - Don't expose sensitive information in error messages
- **Rate limiting** - Implement rate limiting to prevent abuse

## Documentation Rules

- **Update documentation** when making significant changes:
   - README.md - Setup instructions, features, usage
   - `CHANGELOG.md` - After completing user-facing features (use semantic versioning)
   - `docs/ARCHITECTURE.md` - When changing system design
   - `.augment/rules/conventions.md` - When establishing new patterns (ask first)

- **Don't create new documentation files** unless requested


## Scope Rules

- **Do what's asked, nothing more** - Don't add unsolicited features
- **Ask before major changes** - Deployment, dependencies, breaking changes, refactoring
- **No unsolicited documentation** - Only create docs when requested
- **Respect project boundaries** - Don't modify unrelated code
- **Backward compatibility** - Avoid breaking changes unless explicitly requested

## Git & Version Control

- **Don't commit** - Never commit code
- **Don't push** - Never push to remote
- **Gitignore** - Always Ensure sensitive files are in .gitignore



---

## Usage Instructions

### Working with This Project

1. **Before planning any task:**
   - Read `.augment/rules/about.md` to understand project goals and purpose
   - Review `docs/ARCHITECTURE.md` to understand system design
   - Check `.augment/rules/conventions.md` for coding standards
   - Review `CONTRIBUTING.md` for developer workflow

2. **During implementation:**
   - **ALWAYS use Make commands** - Check `.augment/rules/development.md` for required Make commands
   - Follow patterns documented in `.augment/rules/conventions.md`
   - Reference `docs/ARCHITECTURE.md` for component relationships
   - Check `CONTRIBUTING.md` for setup and workflow instructions
   - Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.


3. **After completing work:**
   - Update `CHANGELOG.md` with user-facing features (in [Unreleased] section)
   - Update `docs/ARCHITECTURE.md` if system design changed
   - Ask to update `.augment/rules/conventions.md` if new patterns were established

4. **At release time:**
   - Move items from [Unreleased] to a new version section in `CHANGELOG.md`
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Include release date in YYYY-MM-DD format
- Look for inline code comments and existing patterns
- Ask the user for clarification on conventions and priorities

---

## Citing Sources

**When responding to user requests, always include a section that explicitly states:**

1. **Which rules you applied** - List the specific sections from this rules document (e.g., "General Rules - Cite your sources", "Testing - Mock external dependencies")

2. **Which memory documents you referenced** - If the memory directory exists, list which files you consulted (e.g., "memory/ARCHITECTURE.md", "memory/TASKS.md")

3. **What information you used** - Briefly explain what you learned from each source and how it informed your response

**Format:**
```
## 📚 Sources Referenced

### Rules Applied:
- [Rule Section] - [How it was applied]

### Memory Documents Consulted:
- memory/[FILE].md - [What information was used]

### Codebase Files Reviewed:
- [file path] - [What was learned]
```

**Example:**
```
## 📚 Sources Referenced

### Rules Applied:
- General Rules - "Cite your sources" - Documenting all sources used
- Testing - "Mock external dependencies" - Planned to use mockProfileAPI
- Documentation Rules - "Update CHANGELOG.md" - Will update after completion

### Memory Documents Consulted:
- memory/TASKS.md - Identified this as a high-priority task
- memory/ARCHITECTURE.md - Understood the profile API structure
- memory/CONVENTIONS.md - Followed existing test naming patterns

### Codebase Files Reviewed:
- tests/profile.spec.ts - Analyzed current test coverage
- app/api/profile/route.ts - Understood API validation rules
```

**When to cite:**
- ✅ When creating implementation plans
- ✅ When making code changes
- ✅ When answering questions about project conventions
- ✅ When suggesting architectural decisions
- ❌ Not required for simple clarifying questions
- ❌ Not required for acknowledging user input
