# Detective Agent Design Specification

## Recommended Order of Implementation

This section outlines an incremental, iterative approach to building the agent. Each step builds on the previous one with clear acceptance criteria.

### Step 0: Create Implementation Plan ✅
**Goal:** Translate the design document into a concrete implementation plan based on the steps defined in this document.

**Tasks:**
- [x] Review the entire design specification
- [x] Break down each component into implementable tasks
- [x] Identify dependencies between components
- [x] Define file structure and module organization
- [x] Create a detailed implementation plan document

**Acceptance Criteria:**
- [x] Implementation plan document exists (PLAN_kim.md, PLAN_after.md)
- [x] All components from design are represented in plan
- [x] Dependencies are clearly identified
- [x] File structure is defined
- [x] Plan includes specific tasks with clear deliverables

### Step 1: Say Hello to Your Agent (Basic Conversation) ✅
**Goal:** Build a minimal working agent that can have a conversation

**Components:**
- [x] Configuration system (API keys, model selection) - `config.py`
- [x] Message and Conversation data models - `models.py`
- [x] Provider abstraction interface - `providers/base.py`
- [x] Provider implementation (OpenRouter) - `providers/openrouter.py`
- [x] Agent core with conversation loop - `agent.py`
- [x] Filesystem-based conversation persistence - `persistence.py`
- [x] Simple CLI for testing - `cli.py`
- [x] Basic automated tests - `*_test.py` files

**Capabilities:**
- [x] Have a back-and-forth conversation with the provider model
- [x] Conversation history maintained in memory and persisted to filesystem
- [x] Can continue conversations across CLI sessions
- [x] Provider abstraction layer exists (even though only one is implemented)

**Acceptance Criteria:**
- [x] CLI starts and connects to provider model
- [x] User can send messages and receive responses
- [x] Conversation history is maintained in memory during session
- [x] Each conversation is saved to filesystem as JSON
- [ ] Can load and continue previous conversations from filesystem
- [x] Conversation includes all messages with timestamps
- [x] Basic error handling for API failures
- [x] At least 3 automated tests covering core functionality
- [x] Provider abstraction interface is defined and is implemented

### Step 2: Observability (Traces and Spans) ⏳
**Goal:** Add complete OpenTelemetry visibility into agent operations

**Components:**
- [ ] OpenTelemetry data structures
- [ ] Instrumentation for agent operations
- [ ] Instrumentation for provider calls
- [ ] Filesystem-based trace export (JSON files)
- [ ] Trace context propagation through conversation

**Capabilities:**
- [ ] Every conversation generates a trace
- [ ] Agent operations captured as spans (send_message, provider calls)
- [ ] Traces include timing, token counts, model info
- [ ] All traces saved to filesystem as JSON
- [ ] Trace IDs link conversations to their traces

**Acceptance Criteria:**
- [ ] Each conversation has a unique trace ID
- [ ] Traces saved to filesystem in structured JSON format
- [ ] Spans capture: operation name, duration, start/end times
- [ ] Provider call spans include: model, tokens (input/output), duration
- [ ] Conversation spans include: message count, total tokens
- [ ] Trace files are human-readable and well-organized
- [ ] Can correlate conversation JSON with its trace JSON via trace ID
- [ ] Automated tests verify trace generation

### Step 3: Context Window Management ⏳
**Goal:** Handle conversations that exceed model token limits

**Components:**
- [x] Token counting/estimation - `providers/openrouter.py:estimate_tokens()`
- [ ] Truncation strategy implementation
- [ ] Token budget allocation (system prompt, history, response, buffer)
- [ ] Context management integration into agent core

**Capabilities:**
- [x] Estimate token count for conversation history
- [ ] Automatically truncate old messages when approaching limit
- [ ] Reserve tokens for system prompt and response
- [ ] Maintain conversation coherence during truncation
- [ ] Track context window utilization in traces

**Acceptance Criteria:**
- [ ] Agent calculates token count before each provider call
- [ ] Conversation truncates when within 90% of token limit
- [ ] System prompt always preserved
- [ ] Most recent N messages preserved
- [ ] Context window state visible in traces
- [ ] Long conversations don't cause API errors
- [ ] Automated tests verify truncation behavior

### Step 4: Retry Mechanism ⏳
**Goal:** Handle transient failures gracefully

**Components:**
- [ ] Retry configuration (max attempts, delays, backoff)
- [ ] Exponential backoff with jitter
- [ ] Retry logic for provider calls
- [x] Error classification (retryable vs non-retryable) - `providers/errors.py`
- [ ] Retry tracking in traces

**Capabilities:**
- [ ] Automatic retry for rate limits (429)
- [ ] Automatic retry for network errors
- [ ] Automatic retry for temporary server errors (500, 502, 503)
- [ ] Exponential backoff between attempts
- [x] No retry for auth, validation, or permanent errors (errors defined)
- [ ] Full retry visibility in traces

**Acceptance Criteria:**
- [ ] Rate limit errors trigger retries
- [ ] Retries use exponential backoff
- [ ] Max retry attempts configurable
- [ ] Jitter added to prevent thundering herd
- [x] Auth/validation errors fail immediately
- [ ] Retry attempts tracked in traces with timing
- [ ] Automated tests verify retry behavior
- [ ] Manual test of rate limit handling

### Step 5: System Prompt Engineering ✅
**Goal:** Give the agent personality, capability awareness, and clear instructions

**Components:**
- [x] Enhanced system prompt with agent purpose - `config.py` default
- [x] Instructions for tool usage (when tools are added)
- [x] Response format guidance
- [x] Capability boundaries and limitations
- [x] Configuration to customize system prompt

**Capabilities:**
- [x] Agent has clear sense of purpose
- [x] Agent understands its capabilities
- [x] Agent responds appropriately to out-of-scope requests
- [x] System prompt can be customized per use case

**Acceptance Criteria:**
- [x] Default system prompt defines agent purpose
- [x] System prompt explains how to behave
- [x] System prompt is easily configurable
- [x] Agent behavior reflects system prompt instructions
- [ ] Tested with various prompt configurations

### Step 6: Tool Abstraction ✅
**Goal:** Enable agent to use external tools for release risk assessment

**Components:**
- [x] Tool definition data model - `tools/definitions.py`
- [x] Tool call and tool result data models - `models.py`
- [x] Tool registry and execution framework - `tools/registry.py`
- [x] Tool loop in agent core - `agent.py`
- [x] Release risk assessment tools (get_release_summary, list_releases, file_risk_report) - `tools/release_tools.py`
- [x] Tool formatting for provider-specific APIs - `tools/registry.py:format_for_openai()`
- [x] Static test data for tools - `data/releases.json`

**Capabilities:**
- [x] Register tools with agent
- [x] Agent receives tool definitions in LLM calls
- [x] LLM can request tool execution
- [x] Agent executes tools and returns results
- [x] Tool loop continues until LLM provides final response
- [x] Release assessment workflow functional and tested
- [ ] Tool calls tracked in traces

**Acceptance Criteria:**
- [x] Tool abstraction interface defined
- [x] Tools can be registered with agent
- [x] Agent formats tools for provider API
- [x] Tool execution loop works end-to-end
- [x] get_release_summary returns mock release data
- [x] file_risk_report accepts and validates risk reports
- [x] Tool calls and results visible in conversation history
- [ ] Tool execution captured in traces with timing
- [x] Error handling for tool failures
- [x] Automated tests for tool framework and both tools
- [x] CLI demo of release risk assessment workflow

**Optional Enhancement:**
- [ ] Add web search tool (DuckDuckGo) as additional capability demonstration

### Step 7: Evaluation System ⏳
**Goal:** Validate agent behavior through automated evaluation

**Components:**
- [ ] Test case definitions with expected behaviors
- [ ] Tool usage evaluation (behavioral validation)
- [ ] Decision quality evaluation (output validation)
- [ ] Error handling evaluation (robustness validation)
- [ ] Regression tracking (performance over time)
- [ ] Structured report generation (machine-readable output)
- [ ] Eval runner and reporting

**Evaluation Dimensions:**

#### 1. Tool Usage Evaluation
Validates the agent's behavioral choices:
- Does the agent call the correct tools for the task?
- Does it call them in a reasonable order?
- Does it provide valid parameters?
- Does it handle tool errors appropriately?

**Example Test Cases:**
```python
{
  "scenario": "high_risk_release",
  "release_data": {
    "version": "v2.1.0",
    "changes": ["Payment processing"],
    "tests": {"passed": 140, "failed": 5},
    "deployment_metrics": {"error_rate": 0.08}
  },
  "expected_tools": ["get_release_summary", "file_risk_report"],
  "expected_tool_order": "get before post"
}
```

#### 2. Decision Quality Evaluation
Validates the agent's risk assessment accuracy:
- Does the severity classification match expected severity?
- Are key risks identified in the report?
- Is the reasoning sound given the data?

**Example Evaluation:**
```python
def eval_risk_assessment(agent_output, expected):
    severity_correct = agent_output.severity == expected.severity
    risks_identified = check_overlap(
        agent_output.findings,
        expected.key_risks
    )
    return {
        "severity_correct": severity_correct,
        "risk_recall": risks_identified,
        "pass": severity_correct and risks_identified >= 0.7
    }
```

#### 3. Error Handling Evaluation
Validates the agent's robustness and error handling:
- Does the agent handle missing or malformed data gracefully?
- Does it report errors clearly to the user?
- Does it avoid hallucinating data when tools fail?
- Does it make appropriate decisions when data is incomplete?

#### 4. Regression Tracking
Monitors evaluation performance over time:
- Establishes a baseline of expected performance
- Detects when changes degrade agent behavior
- Tracks improvements over time
- Provides comparison reports showing deltas

**Key Features:**
- Save baseline results for future comparison
- Compare current results to baseline
- Identify regressions (performance drops >5%)
- Identify improvements (performance gains >5%)
- Track overall score and pass rate trends

#### 5. Structured Report Generation
Produces machine-readable evaluation output:
- Summary metrics (pass rate, average score)
- Per-scenario results with status and scores
- Regression comparison data
- Designed for CI/CD integration
- Enables automated quality gates

**Test Scenarios:**
- High risk: Failed tests in critical areas, elevated error rates
- Medium risk: Minor test failures, slight metric degradation
- Low risk: All tests passing, healthy metrics
- Error handling: Missing releases, malformed data, tool failures
- Edge cases: Missing data fields, API errors, unexpected responses

**Acceptance Criteria:**
- [ ] Eval framework can run test scenarios automatically
- [ ] Tool usage evaluated for correctness and ordering
- [ ] Decision quality measured against expected outcomes
- [ ] Error handling scenarios validate robustness
- [ ] Test suite includes 5+ scenarios covering risk spectrum and error cases
- [ ] Regression tracking compares to baseline
- [ ] Structured JSON reports generated for automation
- [ ] Eval results include pass/fail and diagnostic details
- [ ] Automated tests verify eval framework itself
- [ ] Documentation explains how to add new eval cases
- [ ] CLI supports baseline establishment and comparison

**Future Evaluation Options:**
- [ ] Conversation quality: Can the agent explain its reasoning when asked?
- [ ] Robustness testing: How does it handle errors, timeouts, edge cases?
- [ ] Performance benchmarks: Latency, token efficiency, tool call efficiency
- [ ] LLM-as-judge: Use another LLM to evaluate response quality

### Step 8: Additional Capabilities (Future) ⏳

**Goal:** Expand agent capabilities with more tools and features

**Potential Additions:**
- [ ] Additional tools (file operations, calculator, web search, etc.)
- [ ] Multi-provider support (expand beyond initial provider)
- [ ] Advanced context management (summarization, importance-based)
- [ ] Async tool execution
- [ ] Tool composition and chaining
- [ ] User confirmation for sensitive tools
- [ ] Feedback loops and self-correction
- [ ] Conversation branching and exploration
- [ ] Progressive investigation (drill-down tools)
- [ ] Multi-agent coordination

**Note:** These are not prescribed steps but rather areas for future exploration based on specific use cases and requirements.

