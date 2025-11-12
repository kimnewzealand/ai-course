- Prompt (what we're asking of our assistant): Read @/prompts/1-web-api-specs.md and follow the instructions at the top of the file.
- Tool (our AI assistant): Cline
- Mode (plan, act, etc.): Plan
- Context (clean, from previous, etc.): Clean. I have not yet set any Cline rules.
- Model (LLM model and version): grok-code-fast-1
- Input (file added to the prompt): prompts/1-web-api-specs.md
- Output (file that contains the response): prompts/2-web-api-prompt.md
- Cost (total cost of the full run): 12k tokens in context window. Free cost.
- Reflections (narrative assessments of the response): 

Separate markdown input/output files and using the Cline Plan mode seems easier to review and iterate than just using a sequential chat window which is how I have mostly interacted with coding agents. 
Although in this exercise I still used the chat window to discuss options and get recommendations for the specs. I manually updated the specs md and then asked it to reread the specs md to regenerate the prompt and then plan as a way to iterate.
I  updated the spec to make make the make the initial implementation smaller ie an MVP and to run locally.

- Prompt (what we're asking of our assistant): Read @/prompts/2-web-api-prompt.md and follow the instructions at the top of the file.
- Tool (our AI assistant): Cline
- Mode (plan, act, etc.): Plan
- Context (clean, from previous, etc.): from previous
- Model (LLM model and version): grok-code-fast-1
- Input: prompts/2-web-api-specs.md
- Output: prompts/3-web-api-plan.md
- Cost (total cost of the full run): 33.3k tokens. Free cost.
- Reflections (narrative assessments of the response):

First version of the plan looks specific enough at face value. 
I was surprised at the quality of the outputs using the free grok model ( again based on face value of markdown outputs in plan mode. I have not run the act yet)

I asked Cline to reformat the specs md into a more readable format as I knew headings made a difference, but I was surprised by the other formatting and hierarchical changes when I asked Cline if this made a difference:

```
Yes, the reformatted 'prompts/1-web-api-specs.md' significantly improved the structure and readability of 'prompts/2-web-api-prompt.md'. Here are the key differences and improvements:

## Structural Enhancements

- __Clear Headings__: The prompt now uses proper markdown headings (### Programming Language, ### Dependencies, etc.) instead of plain text, making sections easily scannable
- __Consistent Formatting__: Bold text for key terms (__Choice__, __Migration__) and italics for clarifications provide visual hierarchy
- __Code Blocks__: Dependencies are properly formatted in a Python code block with syntax highlighting
- __JSON Formatting__: The payload example is now in a proper JSON code block for clarity

## Content Organization

- __Logical Grouping__: Specifications are grouped into coherent sections (API Design, Database & Storage, etc.) rather than scattered bullet points
- __Removed Redundancy__: The prompt requirements section was removed from the generated prompt, keeping it focused on the technical specs
- __Improved Flow__: The document flows from high-level requirements to specific implementation details

## Readability Improvements

- __Visual Separation__: Empty lines and consistent indentation make the content easier to parse
- __Emphasis Markers__: Checkmarks (✅) and bold/italic text highlight important requirements
- __Structured Lists__: API endpoints are clearly listed with descriptions and parameters

The reformatted specs made the generated prompt much more professional and easier for AI assistants to process, reducing ambiguity and improving the overall developer experience when working with these documents.
```

- Prompt:  Please create a Config API Service in the `config-service` folder, according to the Implementation Plan defined in @/prompts/3-create-web-api-plan.md
- Mode: Act
- Context: Continue from previous
- Model (LLM model and version): grok-code-fast-1
- Input: prompts/3-web-api-plan.md
- Output: config-service/
- Reflections (narrative assessments of the response):

I didn't need to run a command. By switching to Act, Cline created the files and folders as specified in the plan.

I had a few issues which the free grok model couldn't debug which was frustrating so I switched to Augment to fix these to get the web api tests passing and the server running.

I then updated the code including the unit testing framework to follow suggested best practices. I then added some further features to the web api including:
- API versioning
- Health check
- OpenAPI documentation
- Linting

I then asked Cline to create a new set of updated prompt files in the prompts folder based on this updated code to see where I could have specified these better.


- Prompt: Read @/prompts/4-admin-ui-specs.md and follow the instructions at the top of the file.
- Tool: Cline
- Mode: Plan
- Context: Continue from previous
- Model (LLM model and version): grok-code-fast-1
- Input: prompts/4-admin-ui-specs.md
- Output: prompts/5-admin-ui-prompt.md
- Reflections (narrative assessments of the response): 
The prompt didn't include enough detail such as specific library numbers or folder structure so I updated the prompt and then asked it to regenerate the prompt.


- Prompt: Read @/prompts/5-admin-ui-prompt.md and follow the instructions at the top of the file.
- Tool: Cline
- Mode: Plan
- Context: Continue from previous
- Model (LLM model and version): grok-code-fast-1
- Input: prompts/5-admin-ui-prompt.md
- Output: prompts/6-admin-ui-plan.md
- Reflections (narrative assessments of the response): 