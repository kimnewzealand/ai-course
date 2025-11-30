---
type: "always_apply"
---

# Project Guidelines

## Project Context

**Before starting any task:**
1. **Check for memory directory** - If a `memory/` directory exists in the project root, review relevant documentation files
2. Review existing documentation (README.md, CONTRIBUTING.md, docs/, etc.)
3. Understand the project's tech stack and architecture
4. Check for project-specific conventions and patterns
5. Review recent changes and current priorities

**Memory Directory Structure** (if exists):
- `memory/ABOUT.md` - Project overview, goals, and purpose
- `memory/ARCHITECTURE.md` - System design, component relationships, and technical stack
- `memory/CONVENTIONS.md` - Coding standards, naming conventions, and patterns
- `memory/DEVELOPMENT.md` - Setup instructions, development workflow, and environment
- `memory/PROGRESS.md` - Current implementation status and completed features
- `memory/TASKS.md` - Immediate next steps, priorities, and planned work

## General Rules

- **Don't be sycophantic** - Skip flattery, respond directly
- **Be concise** - Keep responses brief and actionable
- **Ask when uncertain** - Request clarification rather than making assumptions
- **Cite your sources** - When responding to user requests, explicitly state which rules and memory documents you referenced to inform your response


## Code Style
- Follow the existing naming conventions in the codebase
- Check `memory/CONVENTIONS.md` (if exists) for project-specific coding standards
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
- **HTTPS only** - Use HTTPS in production
- **Security headers** - Set appropriate security headers (CSP, HSTS, etc.)
- **Principle of least privilege** - Grant minimum necessary permissions
- **Error messages** - Don't expose sensitive information in error messages
- **Rate limiting** - Implement rate limiting to prevent abuse

## Package Management

### General Rules
- **Always use package managers** - Never manually edit dependency files
- **Keep lock files** - Commit lock files to version control

## Documentation Rules

- **Update documentation** when making significant changes:
   - README.md - Setup instructions, features, usage
   - `memory/PROGRESS.md` - After completing features (if memory directory exists)
   - `memory/TASKS.md` - When starting/completing tasks (if memory directory exists)
   - `memory/ARCHITECTURE.md` - When changing system design (if memory directory exists)
   - `memory/CONVENTIONS.md` - When establishing new patterns (if memory directory exists)

- **Don't create new documentation files** unless requested


## Scope Rules

- **Do what's asked, nothing more** - Don't add unsolicited features
- **Ask before major changes** - Deployment, dependencies, breaking changes, refactoring
- **No unsolicited documentation** - Only create docs when requested
- **Respect project boundaries** - Don't modify unrelated code
- **Backward compatibility** - Avoid breaking changes unless explicitly requested

## Git & Version Control

-  **Don't commit** - Never commit code
- **Don't push** - Never push to remote
- **Gitignore** - Ensure sensitive files are in .gitignore



---

## Usage Instructions

### Working with Memory Directory

If a `memory/` directory exists in the project:

1. **Before planning any task:**
   - Read `memory/ABOUT.md` to understand project goals and purpose
   - Review `memory/ARCHITECTURE.md` to understand system design
   - Check `memory/TASKS.md` for current priorities and planned work
   - Review `memory/CONVENTIONS.md` for coding standards

2. **During implementation:**
   - Follow patterns documented in `memory/CONVENTIONS.md`
   - Reference `memory/ARCHITECTURE.md` for component relationships
   - Check `memory/DEVELOPMENT.md` for setup and workflow instructions

3. **After completing work:**
   - Update `memory/PROGRESS.md` with completed features
   - Update `memory/TASKS.md` to mark tasks complete or add new ones
   - Update `memory/ARCHITECTURE.md` if system design changed
   - Update `memory/CONVENTIONS.md` if new patterns were established

### If No Memory Directory Exists

- Review README.md, CONTRIBUTING.md, and any docs/ directory
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
- Documentation Rules - "Update memory/PROGRESS.md" - Will update after completion

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
