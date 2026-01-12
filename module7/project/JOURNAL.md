## Module 7 – Investigator Agent


I ran out of time to get the full investigator agent working as per the exercise but got a basic interaction running as below:

```
(project) (.venv) ~/ai-course/module7/project$ uv run python -m cli
============================================================
Investigator Agent - Feature Readiness Assessment
============================================================
Type 'exit' or 'quit' to end the conversation
Type 'reset' to start a new conversation
============================================================

✓ Agent initialized with Groq (llama-3.1-8b-instant)

You: hello

Agent: Hello. I'm the Investigator Agent, an automated feature readiness assessor. I'm here to help determine if software features are ready to progress to the next development phase.

I'm currently in a learning phase, so I don't have any specific features to assess yet. However, I'd be happy to discuss the general process of feature readiness assessment with you.
```

### New process in Module 7

- **Tried Augment cli Auggie**
  - After reading about [Claude cli compared to Auggie cli](https://hyperdev.matsuoka.com/p/augment-codes-auggie-when-focused), it seems like they have similar commands and UI 
  > The terminal UI looks remarkably similar—so much so that muscle memory transfers immediately.
  - Augment appears to have good context indexing and so it doesn't seem like you need to context management or watch tokens very much as it just reindixes whereas Claude's offering was using subagents but it seems like you need to be concerned with context management.  However Augment have just released a [subagents feature](https://docs.augmentcode.com/cli/subagents)
  - I decided to continue with Augment subscription given I use this for other projects.

- **Automated tests and manual tests**

  - The cli would run the tests but I also manually ran the cli and tests to verify ( human in the loop)

- **Detailed plan anchored in a single spec file**
  - Used `PLAN_before.md` as the source of truth for Phase 1 implementation  (Steps 1.1–1.4 so far) based on the DESIGN.md. I didn't use the separate STEPS.md as I wanted to see if having a single document helped with context and scope management. ( I asked it to compare after a couple tasks and it did appear to help)
  - Each step in the single plan had explicit deliverables, acceptance criteria and tasks to check out.
  - I created GitHub issues to keep track work separately to the codebase after planning in the codebase and copying the details to the issues. I included tasks checklist in issues to manually (human in the loop) check off to track and verify progress.

- **Branch-per-task workflow**
  - Created task focused branches like `feature/1-1-project-init`
  - Kept each branch scoped to only the work for that step 

- **Use Augment in GitHub for PR code review**
  - Read [Training Your AI to Master Git & GitHub: The How-To Guide blog](https://hyperdev.matsuoka.com/p/how-i-trained-augment-code-to-run)
  - Created a new workflow.md file for GitHub
  - It was easy to connect Augment to Github to automate code reviews on small PRs

It seems like using CLIs for coding agents is a real shift in personal way of working from IDEs where you potentially micromanage the coding agent rather than delegating but using PR code review allows you still see the diffs as a final check of the actual code.



Overall, Module 7 felt like a more controlled iterative practice with an improved workflow.