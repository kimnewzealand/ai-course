## Module 7 – Investigator Agent

### New process I tried in Module 7

- **Tried Augment cli Auggie**
  - After reading about [Claude cli compared to Auggie cli](https://hyperdev.matsuoka.com/p/augment-codes-auggie-when-focused), it seems like they have similar commands and UI 
  > The terminal UI looks remarkably similar—so much so that muscle memory transfers immediately.
  - Augment appears to have good context  inddexing and good for focused tasks rather than using subagents
  - Decided to continue with Augment

- **Plan-first development anchored in a single spec file**
  - Used `PLAN_before.md` as the source of truth for Phase 1 implementation  (Steps 1.1–1.4 so far). Didn't use a separate STEPS.md
  - Each step in the single plan had explicit deliverables and acceptance criteria and tasks.
  - Created PR issues to track work. Included tasks checklist in issues to manually check off to verify progress.

- **Branch-per-step workflow**
  - Created focused branches like `feature/1-1-project-init`
  - Kept each branch scoped to only the work for that step 

- **Use Augment in GitHub for PR code review**
  - Read [Training Your AI to Master Git & GitHub: The How-To Guide blog](https://hyperdev.matsuoka.com/p/how-i-trained-augment-code-to-run)
  - Created a new workflow.md file for GitHub
  - Easy to integrated existing Augment subscription into GitHub 
  - Easy to automate code reviews on small PRs

Overall, Module 7 felt like a deliberate practice and improved workflow.