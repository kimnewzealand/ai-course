# Collaborative Development Workflow

## Overview
This document defines the collaborative workflow for developing features in the web-api-mvp project. The workflow is designed for effective AI-assisted development, with clear stages, inputs, outputs, and transition rules.

## Workflow Stages

### 1. PLANNING Phase

**Required Inputs:**
- Feature request or issue description
- Business requirements or user stories
- Acceptance criteria (if available)

**Activities:**
- Analyze requirements and break down into tasks
- Identify impacted components (API, models, schemas, client, UI)
- Create or update work item file
- List dependencies and prerequisites
- Define acceptance criteria if not provided
- Identify any architectural decisions needed

**Outputs:**
- Complete task breakdown with effort estimates
- Updated work item file with acceptance criteria
- Dependencies and risks identified

**Transition Rules:**
- Advance to IMPLEMENTATION when all tasks are defined and prioritized
- Must have at least 1-2 clear tasks identified
- Can transition early if requirements are simple

**Status Tracking:**
- File: `changes/XXX-feature_name.md`
- Status: `[ ] PLANNING` → `[x] PLANNING`

---

### 2. IMPLEMENTATION Phase

**Required Inputs:**
- Complete task breakdown from PLANNING
- Approved design decisions
- All dependencies ready

**Activities:**
- Implement API endpoints (FastAPI routes, models, schemas)
- Update client library (TypeScript ConfigClient)
- Modify UI components as needed
- Write unit tests
- Update documentation
- Follow TDD principles where appropriate

**Outputs:**
- Working code changes
- Unit tests passing
- Basic integration tests performed
- Documentation updated
- Code formatted and linted

**Transition Rules:**
- Advance to TESTING when:
  - All core functionality implemented
  - Unit tests passing (≥70% coverage)
  - No critical TODOs remaining
  - Code review ready
- Can stay in implementation for partial deliveries if requested

**Status Tracking:**
- File: `changes/XXX-feature_name.md`
- Status: `[ ] IMPLEMENTATION` → `[x] IMPLEMENTATION`

---

### 3. TESTING Phase

**Required Inputs:**
- Implemented code changes
- Passing unit tests
- Basic integration tests completed

**Activities:**
- Run full test suite (`make test`)
- Execute E2E tests with Playwright
- Perform manual testing of acceptance criteria
- Validate API endpoints with client requests
- Check UI functionality
- Verify no regressions

**Outputs:**
- All tests passing
- Acceptance criteria verified
- Test results documented
- Screenshots/videos for UI changes
- Performance check results

**Transition Rules:**
- Advance to REVIEW when:
  - All acceptance criteria met
  - Critical tests passing (≥90% success rate)
  - No blocking bugs found
- Stay in TESTING for bug fixes
- Can transition to IMPLEMENTATION if major issues require re-architecting

**Status Tracking:**
- File: `changes/XXX-feature_name.md`
- Status: `[ ] TESTING` → `[x] TESTING`

---

### 4. REVIEW Phase

**Required Inputs:**
- Fully tested feature
- Test results and documentation
- Self-review completed

**Activities:**
- Final code review and cleanup
- Documentation completion
- Integration testing in staging environment
- Security scan with appropriate tools
- Performance testing
- Peer review or AI-assisted review
- Final validation of acceptance criteria

**Outputs:**
- Production-ready code
- Complete PR with description
- Documentation updated
- Migration scripts if needed
- Rollback plan defined

**Transition Rules:**
- Complete when:
  - Code merged to main/develop
  - No remaining blockers
  - Stakeholders approve
- Restart at appropriate phase if significant issues found

**Status Tracking:**
- File: `changes/XXX-feature_name.md`
- Status: `[ ] REVIEW` → `[x] REVIEW`

---

## Work Item Structure

### File Location
`changes/NNN-feature_name.md` where NNN is the sequential number

### File Format
```markdown
# Feature: Brief Description

## Status
- [ ] PLANNING
- [ ] IMPLEMENTATION
- [ ] TESTING
- [ ] REVIEW

## Context & Requirements
[Describe the feature, business value, and requirements]

## Acceptance Criteria
- [x] Criterion 1 (when completed)
- [ ] Criterion 2 (remaining)
- [ ] Criterion 3

## Tasks
### PLANNING
- [x] Break down requirements
- [x] Define acceptance criteria
- [x] Identify dependencies

### IMPLEMENTATION
- [ ] Implement API endpoint `/api/items`
- [ ] Add request validation
- [ ] Update response models
- [ ] Write unit tests

### TESTING
- [ ] Run unit tests
- [ ] Execute E2E tests
- [ ] Manual acceptance testing

### REVIEW
- [ ] Code review
- [ ] Documentation update
- [ ] Final integration test

## Notes
[Any additional context, decisions, or blockers]

## Dependencies
- [Link to related issues/PRs]
- [External dependencies]
```

## Acceptance Criteria Validation

**Format:**
- Clear, testable statements
- Written from user perspective: "As a user, I can..."
- Include both positive and negative scenarios
- Preferably quantifiable

**Validation Process:**
- Checked during TESTING phase
- Must be manually verified by developer
- Document evidence (screenshots, test results)
- Re-testing required after any bugs fixed

## Status Maintenance

**Global Status:**
- Maintained in individual work item files
- Active work tracked in separate dashboard (future enhancement)
- Weekly reviews of open items

**File Integration:**
- This WORKFLOW_STATUS.md defines the process
- Individual work items contain specific progress
- Avoid duplication between workflow definition and task tracking

## Building & Testing Protocol

**Daily Development:**
- `uv run python -m pytest tests/` - Run unit tests
- `make test` - Full test suite and linting
- `make run` - Start development server

**Pre-commit:**
- All tests pass
- Code formatted with black/isort
- Type checking with mypy (Python), tsc (TypeScript)
- No ESLint errors in client/UI

**Integration:**
- Features tested in staging before production
- E2E tests run on merge to main
- Automated deployment validation

**Exception Handling:**
- Simple bug fixes may skip formal workflow
- Emergency hotfixes follow abbreviated process
- Major architectural changes require full workflow

## Adaptation Protocol

**Weekly Reviews:**
- Assess workflow effectiveness
- Identify bottlenecks or inefficiencies
- Update this document as needed
- Refine based on project growth

**Metrics to Track:**
- Feature delivery time
- Bug discovery rate
- Test coverage trends
- Blocker identification speed
