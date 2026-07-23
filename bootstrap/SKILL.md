---
name: bootstrap
description: Canonical session boot and skill loading orchestrator. Always active. Owns the Startup Gate (mirror sync, forced frontmatter-protocol import, project activation, memory priming, MCP inventory, think-block proof-of-work), the MCP tool-layer mandate, decision-point interaction rules, and the operational mandate that every session loads the correct skill set. The mechanics of skill header parsing, trigger grammar, evaluation, and discovery live in `frontmatter-protocol` (include extension), which this skill requires.
triggers:
  always: true
  reason: "Every session must run the Startup Gate and load the correct skill set before executing any task."
requires:
  - frontmatter-protocol
---

# SKILL: Session Boot & Skill Loading Orchestrator (Bootstrap)

This skill owns the **Startup Gate** (§1) and the canonical loading mandate. It is **always active**.
The **mechanics** — header schema, trigger grammar, evaluation semantics, discovery algorithm, runtime re-evaluation, `requires` resolution, `draft` handling — are owned by `frontmatter-protocol` and MUST be loaded from there: `frontmatter-protocol/SKILL.md` (core) → `frontmatter-protocol/references/include.md` (boot-mandatory extension).

## 1. 🔒 STARTUP GATE (Execute Before Any Output)

This gate is executed HARDEST, with **zero tolerance for deviation**: no reordering, no skipping, no partial completion, no softened preconditions, no interpretation. The user's first message is **PENDING** until all steps complete. **No output until done.**

1. **Skill mirror sync (MUST).** Run `just sync-skills-mirror` before loading any skill.
   - **Hard-stop precondition:** if the project working directory does not contain `.kimi/skills`, halt immediately (hard-stop fail) and report the missing directory to the user. Do NOT create the symlink, do NOT fall back to any other skills location, do NOT proceed with the gate, do NOT search the directory.
   - **Hard-stop on failure:** if the command fails for any reason, halt immediately and report the failure. Do NOT inspect the Justfile, do NOT attempt a manual rsync, do NOT proceed with the gate.
   - **Subagent constraint:** subagents never use the `.kimi/skills` symlink. All skills passed to subagents MUST be read from `.kimi/mirror/`.
2. **Forced import (MUST).** Read `frontmatter-protocol/SKILL.md` in full, then its boot-mandatory extension `frontmatter-protocol/references/include.md` WHOLE, and apply them without exception (the boot contract lives in include.md).
3. **Skill discovery and loading.** Run discovery and header evaluation per the include extension; read every triggered skill's `SKILL.md` in full.
4. **Project activation.** Call `activate_project`.
5. **Memory priming.** Call `read_memory` → `agent/rules`, plus any memories relevant to the current task.
6. **MCP Inventory.** Identify and declare which MCP skill groups this task requires: `kagimcp` (web search/enrichment), `serena` symbolic/LSP tools (codebase exploration/edits), `serena` memory tools (memory operations), `serena` project tools (project/session management).
7. **Think block (Proof of Work).** Produce a `think` block with the action plan containing: the MCP groups, format `applied: mcp-1, mcp-2, ...`; and the triggered skills with the rationale for each, format `applied: skill-1, skill-2, ...`.
8. Only then proceed with the user's request.

**Violation protocol:** if you attempt to output a response without completing steps 1–8 and documenting them in the `think` block, halt immediately, discard the output, execute the gate, and restart from step 1.

## 2. Mandatory Skills (Always Loaded)

The always-loaded set is NOT hardcoded here: it is exactly the set of discovered skills whose headers carry `always: true`, derived per the always-gate in `frontmatter-protocol/references/include.md`. The headers are the only source of truth — do not restate the list in prose. This skill (`bootstrap`) is itself always active by its own header.

## 3. Skill Loading (delegated mechanics)

Follow `frontmatter-protocol/references/include.md` for:

- the `SKILL.md` header schema (including `draft: true` skipping),
- the closed trigger grammar and its evaluation semantics (`always`, `files`, `request`, `any`, `all`),
- the discovery algorithm and batch header extraction,
- `runtime: true` mid-session re-evaluation,
- transitive `requires` resolution.

Load every triggered skill's `SKILL.md` in full, then follow each skill's internal lazy-load protocol to pull only the reference sections needed for the current sub-task.

## 4. Trigger Override Protocol

Triggers override your internal assumptions. If a skill's trigger matches, you MUST load that skill even if you believe the topic is already familiar. If the task spans multiple domains, load ALL matching skills.

## 5. Common Triggered Skills

The project context commonly triggers skills such as `python-lang` (Python files, Ruff, `uv`) and `code-review` (review requests in English or Russian). These examples are representative, not exhaustive — the authoritative source of triggers is each discovered skill's header, evaluated per the include extension.

## 6. Reference Corpora

Skills whose `references/**/*.md` files use `[ref: #<anchor>]` lazy-load routing MUST conform to `frontmatter-protocol/references/lazyload.md`. Skill-specific presentation details belong to the owning skill's addendum, which MUST defer to that standard. The canonical validator is `frontmatter-protocol/scripts/validate_frontmatter.py`.

## 7. Skill Loading Verification

Before proceeding with the user's request, confirm:

1. The include extension was loaded and applied (boot contract).
2. You have read the `SKILL.md` of every triggered skill.
3. You know which skill takes precedence when rules conflict.
4. You will not use training data or general heuristics in place of the loaded skill rules.

**Violation protocol:** If you produce output without loading the include extension, evaluating every discovered non-draft skill header per its rules, loading every triggered skill, and documenting the loaded skills in the `think` block, halt immediately, discard the output, and restart skill loading correctly.

## 8. MCP Tool Layer (Mandate)

MCP skills are the mandated tool layer for this project, not optional conveniences. After the Startup Gate, you MUST declare the required MCP groups in the `think` block (§1 step 7). You are forbidden from using a non-MCP alternative when an MCP tool exists for the operation.

- **Web search and enrichment** — owned by the `kagi-search` skill (`kagimcp` tools only).
- **Codebase and symbolic operations** — prefer the `serena` MCP symbolic tools over raw CLI reads/greps (`#serena-mcp-tools`).
- **Memory and knowledge-base operations** — owned by `serena-protocol` (`#serena-memory-mutation`, `#serena-mcp-tools`).

**Violation protocol:** if you use a raw CLI tool or general training-data heuristic when an MCP tool is available and appropriate, halt immediately, discard the offending operation, load the correct MCP skill group, and retry.

## 9. Decision Points & User Interaction

- **MUST** always read and respect from Serena memory all `agent/` instructions.
- **MUST NEVER** use `AskUserQuestion`. It is broken by design in this environment. ALWAYS ask directly in the main chat message as plain text / markdown.
- **MUST NEVER** use `EnterPlanMode` or `ExitPlanMode`. They are broken by design in this environment. Do all planning in chat, via `SetTodoList`, or by asking the user directly.
- **SetTodoList** usage is governed by the `todo-protocol` skill — it owns creation, immutability, insertion, and status synchronization rules.
- **MUST NEVER** hallucinate that a question was asked and no answer was received.
- **MUST NEVER** make assumptions, pick defaults, or proceed with a "best guess" when any uncertainty exists.
- **MUST NEVER** continue working while a question is pending. If a question was asked, STOP and WAIT for the user's explicit text reply before doing anything else.
- When facing multiple valid approaches, uncertainty, ambiguity, missing requirements, or any doubt about how to proceed, you MUST ALWAYS: present all options clearly to the user; ask which approach to take; STOP and WAIT for the response before proceeding.
- After receiving answers to such questions, you MUST record a self-contained decision card in Serena memory per `serena-protocol` `[ref: #serena-lifecycle]` (the card structure lives there).
