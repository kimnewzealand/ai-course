# Git Workflow & Version Control

We treat Git as a tool for narrating engineering decisions—not just storing code. Use it intentionally to reflect clarity, atomicity, and collaboration.

This workflow is only for module7/project.

## Commit Philosophy

Commit early, commit often, but only once the change is coherent.

Each commit should answer: What changed, and why?

Prefer small, purposeful commits over monolithic ones.

## Conventional Commit Format

We follow Conventional Commits:

<type>(issue_number-optional-scope): short summary


Examples:

feat(1-phase-1-foundation)
feat(34-auth): add OAuth login

fix(76-api): correct rate limit handling

chore(lint): update prettier config

### Valid types: 

feat: new feature
fix: bug fix
refactor: internal changes
chore: tooling, config, etc.
docs: documentation
test: tests only

## Branch Naming Convention
Branches should reflect purpose and follow a type/slug format:

feature/3-search-api
fix/4-token-refresh
chore/update-deps

## GitHub Issue Tracking
We use GitHub Issues for all tracked work—features, bugs, ideas, spikes. Each issue answers: What are we doing, why does it matter, and how will we know it's done?

### Issue Fields to Fill
Title – human-readable and emoji-tagged (e.g. 🚀 Add login flow)

Description – context, proposed approach, and acceptance criteria

Labels – use taxonomy below

Assignee – assign only when actively in progress

Milestone – for cycles/themes

## Versioning & Releases 

No releases in this workflow yet.


## Reference

https://hyperdev.matsuoka.com/p/how-i-trained-augment-code-to-run