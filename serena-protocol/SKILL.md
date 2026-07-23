---
name: serena-protocol
description: "MANDATORY skill for Serena (MCP) memory, knowledge base, and symbolic code exploration operations. Use whenever the agent needs to: read or write Serena memories, mutate or persist memory, explore code via symbolic MCP tools, resolve contradictions in stored knowledge, or follow memory metadata, naming, and routing conventions."
triggers:
  always: true
  reason: "Memory, knowledge-base, and symbolic code operations may occur in any session; this skill governs their mandatory rules."
requires:
  - entity-protocol
  - frontmatter-protocol
  - markdown-protocol
---

# SKILL: Serena Memory & MCP Protocol

You operate within the Serena MCP ecosystem. The **canonical rule set** lives in `references/rules.md` (naming, metadata, lifecycle, contradictions, examples, MCP tools) plus the mutation & persistence protocol in this file (§1).

Ownership boundary: the repo (entity) concept, the SINGLE namespace registry, findings routing/evidence, deprecations, card production, and the `repos/` layout live in `entity-protocol`. Type detection and per-type interface exhaustiveness live in `repo-audit`. Tracking fields, timestamps, git commands, and refresh-on-mutation live in the frontmatter-protocol tracking extension.

## 1. Memory Mutation & Persistence Protocol (HARD)

[ref: #serena-memory-mutation]

The single recipe for creating, appending, updating, verifying, and persisting memories. Applies to EVERY memory operation, every session.

**Tool semantics:**

- `write_memory` **completely overwrites** a file. You MUST NEVER use it to append to an existing memory.
- `edit_memory` edits in place (`literal` or `regex` mode). In `regex` mode the pattern compiles with `re.MULTILINE | re.DOTALL`: NEVER use bare `.*` in needles (it eats the rest of the file — use `[^\n]*` for single lines), and `repl` is inserted VERBATIM (`\1`-style backreferences are NOT expanded).

**To CREATE a new memory:**

1. Call `list_memories` to ensure the name does not exist.
2. Call `write_memory` with the complete YAML frontmatter (`[ref: #tracking-fields]`) and body.

**To APPEND to an existing memory:** call `edit_memory` with the following EXACT payload:

```json
{
  "mode": "regex",
  "needle": "\\Z",
  "repl": "\n\n## <New Section>\n<new content>"
}
```

**To UPDATE specific lines:** use `edit_memory` with a highly specific `regex` targeting only the outdated paragraph/table row, or `literal` mode with the exact old string.

**On EVERY mutation:**

1. Refresh the header per the tracking extension (`[ref: #tracking-refresh]`, `[ref: #tracking-timestamps]`): bump `updated_at`, and `branch`/`commit`/`committed_at` when the git state changed.
2. **Read the memory back** and verify it was saved correctly.
3. Run the configured persistence command (commonly `just serena-checkpoint`) from the workspace root. Do not stop until everything is persisted.

**Working directory (HARD):** every Serena operation that touches `.serena/` — including `write_memory`, `edit_memory`, `list_memories`, `delete_memory`, `rename_memory`, and the persistence command — MUST be executed from the workspace root (`cd <workspace-root>`). Before running the command, verify that the target `.serena/` directory is the workspace-root `.serena/` and not a nested instance inside a subdirectory. Never run Serena commands from within an entity directory or any other nested project that may contain its own `.serena/`. Exception: reading source code or collecting raw git metadata inside an entity repository is allowed as long as no Serena memory operation is triggered from there.

**Hard fails:**

- **HARD FAIL:** forgetting the persistence command after writing/editing memories.
- **HARD FAIL:** executing any Serena memory operation or persistence command from anywhere other than the workspace root when a nested `.serena/` could be affected.
- **HARD FAIL:** using `write_memory` to append to an existing memory (it overwrites).
- Card-specific hard fails live in `entity-protocol` `[ref: #entity-card-hard-fails]`.

## 2. Lazy-Load Protocol (CRITICAL)

You **MUST NOT** read `references/rules.md` in full. Use the Routing Index below to extract only the section you need.

**Extraction Execution:**

1. Match your task to a Trigger in the Routing Index below.
2. Note the exact Anchor tag.
3. Extract ONLY that section per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (bounded extraction — never a blind `rg -A N` window; the exact command lives there, not here).
4. Apply the extracted rules strictly.

## 3. Mandatory Lookups by Task (The Routing Index)

| Trigger / Situation | Where | Anchor |
|---|---|---|
| Any memory create/append/update/persist — the mutation protocol. | THIS FILE §1 | `[ref: #serena-memory-mutation]` |
| Overview of Serena memory (location, AGENTS.md relationship, language). | rules.md | `[ref: #serena-what-is]` |
| Namespaces, scopes, findings routing, when-to-record, meta-entity. | `entity-protocol/SKILL.md` | `[ref: #entity-namespace-registry]` |
| Deciding the filename for a new memory entry; normalizing non-compliant names. | rules.md | `[ref: #serena-naming]` |
| Checking whether a repo is usable before writing repo-scoped memory. | `entity-protocol/SKILL.md` | `[ref: #entity-prerequisite]` |
| Writing or updating the mandatory metadata header. | rules.md | `[ref: #serena-metadata]` |
| MANDATORY for every memory write/edit: tracking fields, field semantics, timestamps, refresh-on-mutation, git commands; `repo` value semantics in `entity-protocol`. | `frontmatter-protocol/references/tracking.md` | `[ref: #tracking-fields]`, `[ref: #tracking-field-semantics]`, `[ref: #tracking-timestamps]`, `[ref: #tracking-refresh]`, `[ref: #tracking-git-commands]`; `[ref: #entity-repo-field]` |
| Checking freshness of a tracked memory; reconciling a stale one. | `frontmatter-protocol/references/tracking.md` | `[ref: #tracking-validation-timing]`, `[ref: #tracking-staleness]`, `[ref: #tracking-reconciliation]` |
| Checking whether a repo-specific memory is stale against its source repo. | `entity-protocol/SKILL.md` | `[ref: #entity-freshness]` |
| When to record memory; the proactive-population mandate. | rules.md | `[ref: #serena-lifecycle]` |
| Logging a bug, note, or other finding with proper evidence. | `entity-protocol` | `[ref: #entity-namespace-registry]`, `[ref: #entity-findings-traceability]` |
| Resolving contradictions between memory entries; the contradictions log. | rules.md | `[ref: #serena-contradictions]` |
| Handling deprecated names and aliases. | `entity-protocol/references/repo_memory.md` | `[ref: #entity-deprecations]` |
| Syntax examples of memory entries per findings domain. | rules.md | `[ref: #serena-examples]` |
| Producing a repo card: workflow, quality, exclusions, hard fails, header. | `entity-protocol/references/card_production.md` | `[ref: #entity-card-workflow]`, `[ref: #entity-card-quality]`, `[ref: #entity-card-exclusions]`, `[ref: #entity-card-hard-fails]`, `[ref: #entity-card-header-example]` |
| Determining repo type; per-type interface exhaustiveness. | `repo-audit/references/analysis/type_detection.md` | `[ref: #repo-type-detection]`, `[ref: #repo-interface-exhaustiveness]` |
| Symbolic code search/edit via Serena MCP tools. | rules.md | `[ref: #serena-mcp-tools]` |

## 4. Master Execution Workflow

1. **Analyze Task:** determine if you need to read memory, write memory, explore code, or create an entity card.
2. **Consult Index:** find the relevant Anchor in the table above.
3. **Extract & Read:** extract the exact section from the referenced file.
4. **Validate Header:** when reading or editing an existing memory, verify that its frontmatter matches the current standard (`[ref: #serena-metadata]`). If the header is outdated (plain-text metadata, missing or renamed fields), refresh it to the current YAML frontmatter format without losing information. Prefer direct file editing at `.serena/memories/<path>.md` for header-only updates, preserving all content below the header.
5. **Execute:** perform the memory/MCP operation strictly following the extracted guidelines.
6. **Persist:** follow §1 — read back, then run the persistence command from the workspace root.
