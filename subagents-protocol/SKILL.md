---
name: subagents-protocol
description: Mandatory protocol for delegating work to built-in subagents (coder, explore, plan). Governs when to delegate, how to pass context, launch parameters, timeouts, foreground/background choice, resume behavior, and the web-search bridge. Loaded at runtime when the user mentions subagents or when the agent plans to delegate.
runtime: true
triggers:
  request: "subagent, subagents, delegate, delegation, delegating, субагент, субагенты, делегируй, делегирование, coder subagent, explore subagent, plan subagent"
  reason: "The skill must activate whenever the user mentions subagents or the agent decides to delegate work."
requires:
  - bootstrap
  - shell-protocol
  - serena-protocol
---

# SKILL: Subagent Delegation Protocol

This skill governs every interaction with the `Agent` tool and its built-in subagent instances.
The main agent is an orchestrator; subagents are specialized workers.
When this skill is triggered at startup or loaded mid-session via `runtime: true`, its rules take precedence over any general heuristic about delegation.

## 1. When to Delegate

You MUST prefer launching a subagent for any non-trivial task that benefits from isolated context, focused execution, or parallel exploration.
Typical reasons to delegate:

- Codebase investigation that requires more than three searches or reading many files.
- Writing, refactoring, or debugging code.
- Multi-step file manipulations.
- Parallel exploration of independent questions.
- Long-running operations that can continue in the background.

You MAY handle directly only trivial, single-step, or purely conversational tasks that do not touch code or files.

## 2. Built-in Subagent Types

Use the correct `subagent_type` for the work:

| Type | Purpose | Use when |
|---|---|---|
| `coder` | General software engineering tasks. | Writing code, refactoring, debugging, running commands, building features, fixing tests. |
| `explore` | Fast read-only codebase exploration. | Finding files, understanding modules, tracing call sites, answering "how does X work?", architecture reconnaissance. |
| `plan` | Read-only implementation planning. | Designing a change, identifying key files, comparing approaches, producing a step-by-step plan before editing. |

If a task spans multiple types, split it or choose the dominant type.

## 3. Runtime Activation

This skill uses `runtime: true`.
After every new user message, re-evaluate the trigger.
If the user mentions subagents, delegation, or if you decide to delegate, load this skill immediately and apply its rules to all subsequent actions.

## 4. Launch Parameters

Every `Agent` call MUST include:

- `description`: a short 3–5 word summary.
- `subagent_type`: `coder`, `explore`, or `plan`.
- `prompt`: a complete, self-contained instruction.

Optional but important:

- `timeout`: minimum 600 seconds (10 minutes) for simple tasks; minimum 3300 seconds (55 minutes) for complex investigations or large code changes.
- `run_in_background`: default `false`. Use `true` only when the task can continue independently, you do not need the result immediately, and there is a clear benefit to returning control before it finishes.
- `model`: override only when the task specifically needs a different model.
- `resume`: reuse an existing `agent_id` when the new task clearly continues prior work or when that instance already holds relevant context.

## 5. Context Passing

Subagents do NOT have access to MCP tools, Serena memory operations, or Kagi web search.
Therefore:

- Pass all necessary context explicitly inside the `prompt`.
- When Serena memory pages are relevant, pass their file paths (e.g., `.serena/memories/decisions/project/xxx.md`) and instruct the subagent to read them via standard shell commands.
- NEVER paste large memory contents inline into the subagent prompt.
- NEVER assume the subagent sees the current conversation history or project context.

## 6. Web Search Bridge

Because subagents cannot use `kagimcp` tools, the main agent MUST perform any required internet research, documentation lookup, or web enrichment.
Distill the retrieved information and pass only the relevant facts to the subagent in its prompt.
If a subagent discovers it needs more web data, it should ask the main agent for a specific search.

## 7. Foreground vs Background

Default to foreground subagents.
Use a background subagent only if all of the following are true:

- The task can continue independently.
- You do not need the result to decide your next action.
- Returning control early provides a clear benefit to the user or the workflow.

After starting a background task, default to returning control to the user instead of immediately waiting.
Use `TaskOutput` for non-blocking progress snapshots and `TaskOutput(block=true)` only when you intentionally want to wait.
Use `TaskStop` only when cancellation is truly necessary.

## 8. Resume vs New Instance

The `Agent` tool can create a new instance or resume an existing one by `agent_id`.

- Create a new instance when the task is unrelated to previous subagent work.
- Resume an existing instance when the task is a direct continuation or when that instance already holds relevant context.
- Each instance keeps its own context history; repeated use of the same `agent_id` preserves prior findings.

## 9. What Subagents Cannot Do

Subagents operate in a standard shell/CLI environment without MCP access.
They MUST NOT:

- Call Serena memory tools (`read_memory`, `write_memory`, etc.).
- Call Kagi web search tools (`kagi_search_fetch`, `kagi_fastgpt`, etc.).
- Call Serena symbolic/LSP tools (`find_symbol`, `replace_symbol_body`, etc.).

If a subagent task needs any of these, the main agent performs the MCP operation and passes the result to the subagent.

## 10. Prompt Quality

A subagent prompt MUST be:

- Self-contained: include goals, constraints, file paths, and expected outputs.
- Specific: define success criteria and deliverables.
- Context-aware: mention relevant memories, previous findings, or project conventions.
- Bounded: set clear scope and tell the subagent what NOT to do.

## 11. Output Handling

- Subagent results are visible only to the main agent.
- Summarize subagent findings for the user in the final response; do not dump raw subagent output unless explicitly requested.
- If a subagent fails or times out, decide whether to retry, re-delegate with a clarified prompt, or handle the task directly.

## 12. Violation Protocol

If you delegate without passing required context, allow a subagent to rely on MCP tools, or choose parameters that violate this skill, halt immediately, recall the relevant section of this skill, and restart the delegation correctly.
