---
name: serena-protocol
description: >
  MANDATORY skill for Serena (MCP) memory, knowledge base, and symbolic code
  exploration operations. Use whenever the agent needs to: read or write Serena
  memories, create or update service/entity cards, explore code via symbolic MCP
  tools, resolve contradictions in stored knowledge, or follow memory metadata,
  naming, and routing conventions.
triggers:
  always: true
  reason: "Memory and knowledge-base tools are used in every session."
---

# SKILL: Serena Memory & MCP Protocol

You operate within the Serena MCP ecosystem. The **canonical rule set** lives in
`references/rules.md`. All memory scopes, naming conventions, routing rules,
metadata headers, mutation protocol, entity-analysis gate, and hard fails are
defined there.

## 1. Lazy-Load Protocol (CRITICAL)

You **MUST NOT** read `references/rules.md` in full. Use the Routing Index below
to extract only the section you need.

**Extraction Execution:**
1. Match your task to a Trigger in the Routing Index below.
2. Note the exact Anchor tag."
3. Use your CLI tool to extract ONLY the relevant section."
   *Example:* `rg -A 40 "\[ref: #serena-metadata\]" references/rules.md`
4. Apply the extracted rules strictly.

## 2. Mandatory Lookups by Task (The Routing Index)

| Trigger / Situation | Section Header | Anchor |
|---|---|---|
| Overview of Serena memory and available scopes. | 1. What Serena memory is | `[ref: #serena-what-is]` |
| Deciding the filename for a new memory entry. | 2. Memory naming convention | `[ref: #serena-naming]` |
| Memory namespaces and strict routing. | 3. Memory namespaces & routing | `[ref: #serena-namespaces-routing]` |
| Checking whether an entity is usable before writing memory. | Entity analysis prerequisite | `[ref: #serena-entity-prerequisite]` |
| Writing or updating the mandatory Metadata Header. | 4. Metadata header rules | `[ref: #serena-metadata]` |
| The strict metadata contract and Git source resolution. | 5. The metadata contract | `[ref: #serena-metadata-contract]` |
| When to record memory; routing findings from exploration. | 6. Memory lifecycle / workflow | `[ref: #serena-lifecycle]` |
| Adding text to an existing memory without overwriting it. | 7. Memory mutation protocol | `[ref: #serena-memory-mutation]` |
| Creating a new service/entity card (root vs subagent roles). | 8. Entity card creation workflow | `[ref: #serena-card-workflow]` |
| Determining if a repo is REST, gRPC, Worker, Infra, or Library. | 9. Deterministic type detection algorithm | `[ref: #serena-algo-type-detection]` |
| Root vs subagent responsibilities during card creation. | 10. Card creation segregation | `[ref: #serena-agent-segregation]` |
| Quality checklist for entity cards. | 11. Quality checklist | `[ref: #serena-quality]` |
| Extracting endpoints, gRPC methods, or Temporal workflows. | 12. Interface exhaustiveness matrix | `[ref: #serena-interface-exhaustiveness]` |
| Resolving contradictions between existing memory entries. | 13. Contradiction resolution | `[ref: #serena-contradictions]` |
| Strict contradiction resolution protocol. | 14. Contradiction resolution protocol | `[ref: #serena-contradiction-resolution]` |
| Core tools, git commands, and persistence command. | 15. Core tools and commands | `[ref: #serena-core-tools]` |
| Handling deprecated services and legacy aliases. | 16. Deprecated services and aliases | `[ref: #serena-deprecations]` |
| Logging a bug, note, or style issue with proper traceability. | 17. Findings & traceability | `[ref: #serena-findings-traceability]` |
| Hard fails and forbidden actions. | 18. Hard fails & forbidden actions | `[ref: #serena-forbidden-actions]` |
| Syntax examples for bugs, notes, decisions, proposals, and cards. | 19. Examples of memory entries | `[ref: #serena-examples]` |
| Checking whether an entity-specific memory is stale against its source repo. | 6. Memory lifecycle / workflow — When reading entity-specific memories | `[ref: #serena-memory-freshness]` |
| Troubleshooting: hand-written trees, stale metadata, wrong repos. | 20. Common mistakes and gotchas | `[ref: #serena-mistakes]` |
| Detailed guide on using Serena MCP Tools. | 21. Serena MCP tools reference | `[ref: #serena-mcp-tools]` |

## 3. Master Execution Workflow

1. **Analyze Task:** Determine if you need to read memory, write memory, explore code, or create an entity card.
2. **Consult Index:** Find the relevant Anchor in the table above.
3. **Extract & Read:** Extract the exact section from `references/rules.md`.
4. **Validate Header:** When reading or editing an existing memory, verify that its frontmatter matches the current standard in `[ref: #serena-metadata]`. If the header is outdated (e.g., plain-text metadata, missing or renamed fields), refresh it to the current YAML frontmatter format without losing information. Prefer direct file editing at `.serena/memories/<path>.md` for header-only updates, preserving all content below the header.
5. **Execute:** Perform the memory/MCP operation strictly following the extracted guidelines.
6. **Persist:** After any memory write/edit, read the memory back to verify it and run the configured persistence command (e.g., `just agent-memory-commit`).
