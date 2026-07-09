# Subagent Launch Checklist

Use this checklist before every `Agent` call.

## 1. Subagent type

- [ ] `coder` for writing, refactoring, debugging, running commands.
- [ ] `explore` for read-only codebase investigation.
- [ ] `plan` for implementation planning before edits.

## 2. Launch parameters

- [ ] `description` is 3–5 words.
- [ ] `subagent_type` matches the task.
- [ ] `prompt` is self-contained and specific.
- [ ] `timeout` is at least 600 s for simple tasks or 3300 s for complex tasks.
- [ ] `run_in_background` is `true` only when the task can proceed independently and returning early is useful.
- [ ] `model` is set only if a specific model is required.
- [ ] `resume` is used only when continuing prior work on the same `agent_id`.

## 3. Context

- [ ] All necessary context is in the prompt.
- [ ] Relevant Serena memory pages are referenced by file path, not pasted inline.
- [ ] Web search results, if needed, were fetched by the main agent and summarized in the prompt.

## 4. Constraints

- [ ] The subagent is not expected to use MCP tools.
- [ ] The subagent is not expected to call Serena memory or Kagi search.
- [ ] Success criteria and deliverables are explicit.
- [ ] Scope boundaries are clear.

## 5. After launch

- [ ] Foreground: wait for completion and summarize findings.
- [ ] Background: use `TaskOutput` for snapshots; wait with `TaskOutput(block=true)` only when intentionally blocking.
- [ ] Cancel with `TaskStop` only when necessary.
