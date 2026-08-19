---
name: subagents-protocol
description: Mandatory protocol for delegating work to built-in subagents (coder, explore, plan). Always active. Owns the context-hygiene delegation test (material vs answer, cost balance, warm-instance reuse), launch parameters (mandatory explicit `model`), the single-source model-selection table, answer budgets, degradation handling, and the launch checklist.
triggers:
  always: true
  reason: "Context hygiene must apply from session start — before any delegation is planned — so the skill is always active."
  request: "subagent, subagents, delegate, delegation, delegating, субагент, субагенты, делегируй, делегирование, coder subagent, explore subagent, plan subagent"
requires:
  - bootstrap
  - mandatory-tools
  - serena-protocol
version: 0.2.1
---

# SKILL: Subagent Delegation Protocol

This skill governs every interaction with the `Agent` tool and its built-in subagent instances.
The main agent is an orchestrator; subagents are specialized workers.
The skill is always active: its rules — including the Context Hygiene test — apply from session start, before any delegation is planned, and take precedence over any general heuristic about delegation.

## 1. When to Delegate

The delegation decision is governed EXACTLY by the three-question test of Context Hygiene (HARD) below. Typical delegation-positive cases:

- Codebase investigation beyond a few files or searches.
- Writing, refactoring, or debugging code.
- Multi-step file manipulations.
- Parallel exploration of independent questions.
- Long-running operations that can continue in the background.

Acting directly is legitimate exactly per the direct-action exceptions and sizing probes of Context Hygiene — nothing else.

## Context Hygiene (HARD)

[ref: #sp-context-hygiene]

The main agent's context is the scarcest resource in the session. Bulk material needed only as the SOURCE OF AN ANSWER never enters it — a subagent eats the volume and returns the distillate.

**The three-question test** (before any read/search/explore operation):

1. **Material or answer?** Do I need the material itself (I will edit it, quote it exactly, reason over it repeatedly) — or only an answer derived from it?
2. **Does the volume pay for the delegation?** The prompt and the returned answer are also main-context tokens; delegate only when the volume kept out clearly outweighs that overhead.
3. **New instance or a warm one?** A subagent that already read this corpus holds it in context — follow-ups go to the same `agent_id`; a fresh instance pays the reading cost twice (resume rule, §8).

If you need only an answer AND the volume pays → delegate (to a warm instance when one covers this corpus, otherwise to a new one). Otherwise act directly.

**MUST-delegate triggers:**

- open-ended exploration: more than 3 files to read or grep for one question;
- large files, logs, dumps, or command output read for a single fact or a summary (did tests pass, what failed in the build);
- serial "what's in these N files" questions on one corpus — ONE subagent with the full question list (batching amortizes the prompt).

**Sizing probes (allowed):** when the material's size is unknown, a single careful probe — a toe in the water, never a swim — is legal before deciding: `wc -l`, a `head`, one bounded grep. The probe exists to size the volume, not to read the content; if the probe already answers the question, the question was small — act directly and move on.

**Direct-action exceptions (no delegation, no guilt):**

- material you will EDIT or must quote exactly;
- material that IS the deliverable;
- the small critical core of the current reasoning (the approved blueprint, the active rules);
- a single known file at a known place, a single grep hit, anything small enough that prompt+answer would cost about as much.

**Subagent reuse (STRONG):**

- contextual subagents are assets: an instance that has read a corpus is a warm index over it — follow-ups, refinements, and adjacent tasks on the same material go to the SAME instance via `resume`;
- keep a mental roster of live instances and their coverage; check the roster before any new launch;
- retire an instance when its corpus is exhausted or the topic shifts — stretching one instance across unrelated domains pollutes the subagent's own context and is also waste.

**The answer budget:**

- every delegation prompt carries an explicit cap: "≤5 sentences", "a ≤10-row table", "yes/no + path + one-line why";
- the cap governs ANSWERS TO QUESTIONS, not deliverables: when the task's output IS an artifact, the deliverable-in-report rule (§12) overrides — the cap then applies to everything except the deliverable;
- a raw dump from a subagent defeats the answer budget: ask the SAME instance to compress — never paste the dump into your own reasoning.

**Carve-out (web):** subagents cannot search the web (§6); the main agent performs Kagi calls itself and distills the results (per `kagi-search`) — the hygiene rule does not redirect web work, it governs local corpora.

**Violation protocol:** violations of this section — including over-delegation — follow §15; the balance cuts both ways.

## 2. Built-in Subagent Types

Use the correct `subagent_type` for the work:

| Type | Purpose | Use when |
|---|---|---|
| `coder` | General software engineering tasks. | Writing code, refactoring, debugging, running commands, building features, fixing tests. |
| `explore` | Fast read-only codebase exploration. | Finding files, understanding modules, tracing call sites, answering "how does X work?", architecture reconnaissance. |
| `plan` | Read-only implementation planning. | Designing a change, identifying key files, comparing approaches, producing a step-by-step plan before editing. |

If a task spans multiple types, split it or choose the dominant type.

## 3. Always-Active Semantics

This skill is always active: there is no load event to wait for and no trigger to re-evaluate. The Context Hygiene test applies from the very first read operation of the session, even before any delegation is planned.

## 4. Launch Parameters

Every `Agent` call MUST include:

- `description`: a short 3–5 word summary.
- `subagent_type`: `coder`, `explore`, or `plan`.
- `prompt`: a complete, self-contained instruction.
- `model` (HARD): MANDATORY on every launch, chosen per the Model Selection section below — the SINGLE SOURCE of model names, tiers, and selection criteria. NEVER omit the parameter: the fallback chain (built-in type default → the parent's current model) silently runs the subagent on a more expensive model and burns tokens. An omitted `model` is a protocol violation (§15).
- `prompt` carries an explicit answer cap per the answer budget (`[ref: #sp-context-hygiene]`).

Optional but important:

- `timeout`: `1200` seconds for simple tasks; `3600` seconds (the maximum) for complex investigations or large code changes. These two constants are owned HERE — every other mention (the checklist included) references this rule and never restates the numbers.
- `run_in_background`: default `false`. Use `true` only when the task can continue independently, you do not need the result immediately, and there is a clear benefit to returning control before it finishes.
- `resume`: reuse an existing `agent_id` when the new task clearly continues prior work or when that instance already holds relevant context.

## Model Selection (SINGLE SOURCE)

[ref: #sp-model-selection]

This section is the ONLY place in the project where subagent model names, tiers, and selection criteria live. Every other document, checklist, or memory references this section by anchor and NEVER names a model — names change; the pointer does not.

| Tier | Model | Use for |
|---|---|---|
| **Default** | `kimi-code/kimi-for-coding` | Everything routine: focused file/symbol lookups, known-file reads, mechanical edits, command runs, artifact attestation, template fills, single-file analysis. |
| **Upgrade** | `kimi-code/kimi-for-coding` | Tasks needing extra attention and judgment: complex or cross-cutting research (thorough exploration, architecture reconnaissance), judgment-heavy adversarial review or audit, synthesis over many inputs, work where a miss is expensive (security detection, validation). |

**Escalation ladder:** if a default-tier subagent returns shallow or wrong work, escalate by resuming the SAME instance on the upgrade tier (its corpus context is preserved); start a new instance only when the original instance's context is polluted or lost — do not iterate against a model that is too weak for the task.

**Explicit-parameter rule:** the `model` parameter is passed on EVERY launch (§4), always from this table — never from memory, never from other documents.

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

- Read `AGENTS.md` — under NO circumstances, at any directory level, for any reason. A subagent's entire context is its launch prompt (§5); `AGENTS.md` is main-agent boot material and user preferences that carry nothing a subagent needs and only burn its context.
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

## 12. Subagent Tool Degradation (HARD)

The approval layer may block a subagent's tools at runtime: `Shell` calls can be rejected (observed empirically for `coder` and `explore`; `plan` has no Shell tool at all), and mutation tools (`WriteFile`, `StrReplaceFile`) can be rejected likewise. This is environment-dependent and cannot be detected in advance.

Every delegation MUST follow these rules:

1. **Fallback to read tools.** A subagent whose Shell is blocked reads files with `ReadFile` instead of `cat`, enumerates paths with `Glob` instead of `tree`/`ls`, and searches with `Grep` instead of `rg`.
2. **Never retry, never bypass.** A rejected call is final: the subagent MUST NOT retry the same call and MUST NOT attempt indirect bypasses.
3. **State the limitation.** The subagent's final report MUST explicitly list which operations were blocked and what was omitted because of it.
4. **Deliverable-in-report.** When delegating drafting or editing work, instruct the subagent to ALWAYS include the full deliverable text in its report — the report doubles as a fallback transport when writes are blocked; the main agent then applies the edits and runs verification itself (workaround proven 2026-07-22).
5. Skills MAY add artifact-specific degradation addenda (e.g. repo-audit's evidence-hash omission rule) but MUST NOT contradict this section.

## 13. Directory Trees Belong to the Root Agent (HARD)

Applies whenever a delegated artifact would contain a directory tree. A subagent NEVER generates a directory tree for an artifact. Tree generation is a root-agent duty:

1. The root agent has reliable shell access; a subagent's Shell may be blocked (§12) or absent (`plan`).
2. A tree embedded in a deliverable must be byte-deterministic — produced by the canonical command, never paraphrased from exploration.

The canonical command and its mandatory flags live in `mandatory-tools` — `[ref: #tree-agent-rules]` (`references/tree.md`). Consumers reference that anchor instead of restating the command. If a consuming skill needs a fallback for a missing `tree` binary, the fallback is defined by that skill (e.g. the flat-list fallback defined in `entity-protocol` `[ref: #entity-card-workflow]`).

## 14. Subagent Launch Checklist

Use this checklist before every `Agent` call.

### 0. Before delegating

- [ ] Context hygiene checked (`[ref: #sp-context-hygiene]`): for exploration — only an answer is needed and the volume pays; for execution tasks — delegation serves isolation/focus per §1; a warm instance was considered before a new launch.
- [ ] The prompt carries an explicit answer cap (the answer budget).

### 1. Subagent type

- [ ] `coder` for writing, refactoring, debugging, running commands.
- [ ] `explore` for read-only codebase investigation.
- [ ] `plan` for implementation planning before edits.

### 2. Launch parameters

- [ ] `description` is 3–5 words.
- [ ] `subagent_type` matches the task.
- [ ] `prompt` is self-contained and specific.
- [ ] `timeout` follows the §4 rule (the constants are owned there).
- [ ] `model` is set EXPLICITLY on every launch (never omitted), chosen per `[ref: #sp-model-selection]`.
- [ ] `run_in_background` is `true` only when the task can proceed independently and returning early is useful.
- [ ] `resume` is used only when continuing prior work on the same `agent_id`.

### 3. Context

- [ ] All necessary context is in the prompt.
- [ ] Relevant Serena memory pages are referenced by file path, not pasted inline.
- [ ] Web search results, if needed, were fetched by the main agent and summarized in the prompt.

### 4. Constraints

- [ ] The subagent is not expected to use MCP tools.
- [ ] The subagent is not expected to call Serena memory or Kagi search.
- [ ] Success criteria and deliverables are explicit.
- [ ] Scope boundaries are clear.

### 5. After launch

- [ ] Foreground: wait for completion and summarize findings.
- [ ] Background: use `TaskOutput` for snapshots; wait with `TaskOutput(block=true)` only when intentionally blocking.
- [ ] Cancel with `TaskStop` only when necessary.

## 15. Violation Protocol

Violations of any rule in this skill follow ONE protocol: halt immediately, recall the violated section, and restart the action correctly. When the violation is already unrecoverable (the launch already fired, the output already produced), disclose it to the user in one line and apply the correct form on the very next action. This section is the single violation protocol of the skill; other sections reference it instead of restating their own.
