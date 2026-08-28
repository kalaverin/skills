# Agent Skills Registry
[ref: #asr-intro]

A curated collection of execution skills for Kimi Code CLI and compatible agentic runtimes.
Each skill is a self-contained directory with a `SKILL.md` entry point, a human-facing `README.md` for quick orientation, and usually a `references/` folder containing routing tables, subagent prompts, checklists, and rulebooks. Thin integration skills may keep all rules inline and omit the `references/` folder.

Skills are not libraries. They are operational protocols: they define when the agent must activate, which tools it must use, which subagents it must spawn, and where artifacts must be written. Every skill follows the same layout so an agent can discover, load, and route against it deterministically.

## Repository Layout
[ref: #asr-layout]

```text
.
├── AGENTS.md                    # Runtime-wide startup gate and MCP usage contract
├── Drafts/                      # In-development skills (excluded from discovery)
│   └── <skill-name>/
├── OnDemand/                    # Runtime header-only manifest + rarely used skills
│   ├── SKILL.md                 # Compressed trigger registry for on-demand skills
│   └── <skill-name>/
├── <core-skill-name>/           # Always-loaded core protocols and meta skills
│   ├── README.md                # Human-facing overview, gotchas, and layout
│   ├── SKILL.md                 # Entry point: frontmatter, triggers, routing index
│   ├── references/              # Lazy-loaded sections referenced by [ref: #...] anchors
│   ├── prompts/                 # Optional: generation / review prompts
│   └── scripts/                 # Optional: helper scripts
└── README.md                    # This file
```

A skill is active when its trigger matches the user request or project context. The agent then loads `SKILL.md`, resolves the relevant `[ref: #...]` anchors, and executes the referenced section only. Core skills live in the repository root; rarely used skills are registered in `OnDemand/SKILL.md` and loaded only when their trigger fires; draft skills live in `Drafts/` and are ignored by discovery.

## Skill Catalog
[ref: #asr-catalog]

### Runtime Protocols
[ref: #asr-runtime]

Skills that govern the agent itself, its tool selection, and its startup behavior.

| Skill | Purpose |
|-------|---------|
| **bootstrap** | Canonical skill discovery, auto-loading, and Startup Gate orchestrator. Always active. Discovers skill directories, parses `SKILL.md` frontmatter, evaluates triggers, resolves `requires:` dependencies transitively, and lazy-loads reference sections. |
| **preflight-checklist** | A compliance gate loaded in every session. Verifies that all required skills have been discovered and loaded and that the Startup Gate completed before any user-facing output. |
| **mandatory-tools** | Owns every tool choice: Serena/Kagi MCP tools first, Patchloom for structured/multi-file edits, RTK for token-optimized shell output, modern UNIX replacements (`lsd`, `fd`, `rg`, `ruplacer`, `uv`, `ruff`, `tree`) for base operations. Forbids legacy `ls`, `find`, `grep`, `sed`, `pip`, `black`, `flake8`, etc. Always active. |
| **serena-protocol** | Defines the Serena MCP contract: memory namespaces, YAML frontmatter schema, entity-card prerequisites, mutation rules, and the `just serena-checkpoint` persistence ritual. |
| **entity-protocol** | Defines the repo concept, the prerequisite gate, the one-repo-per-run rule, identity/provenance/freshness rules, and the canonical `repos/` memory layout. |
| **frontmatter-protocol** | The single normative standard for YAML frontmatter across skills, reference corpora, and Serena memories. Owns the extension mechanism and lazy-load routing. |
| **markdown-protocol** | Mandatory Markdown authoring rules for every `.md` file the agent creates or edits, including `SKILL.md` frontmatter, READMEs, and Serena memory entries. Always active. |
| **subagents-protocol** | Mandatory protocol for delegating work to built-in `coder`, `explore`, and `plan` subagents. Governs when to delegate, prompt quality, context passing, launch parameters, foreground/background execution, resume behavior, and the web-search bridge. |
| **todo-protocol** | Mandatory protocol for using the `SetTodoList` tool. Governs when to create a todo list, how to update it without violating immutability rules, how to synchronize item status after every tool call, and the forbidden mutations. |
| **read-for-comments** | Always-active local reference library for technical standards (RFC, OWASP, STD, etc.). Agents MUST check the Serena `standard/` archive and this skill's `references/` seed before fetching a standard from the internet. |
| **kagi-search** | Mandatory and exclusive protocol for web search and page enrichment through the `kagimcp` MCP tools. Governs `kagi_search_fetch`, `kagi_fastgpt`, `kagi_extract`, and `kagi_summarizer`. Always active. |
| **dash-protocol** | Mandatory protocol for the Dash MCP documentation layer: installed docset enumeration, documentation search, full-text search enablement, and page loading through local Dash docsets. |
| **discuss-first** | Co-implementation mode. The agent plans the implementation top-down, shows full signatures and pseudocode, collects per-part approvals, requests master approval, and only then writes code. |

### Languages & API Design
[ref: #asr-lang]

Skills that enforce language-specific and API-specific rules.

| Skill | Purpose |
|-------|---------|
| **api-design** | Enforces Google AIP compliance for resource-oriented APIs: resource naming, standard methods, custom methods, pagination, filtering, planes, compatibility guarantees, and HTTP/gRPC transcoding. |
| **python-lang** | Mandatory Google Python Style Guide enforcement plus a Ruff self-linting protocol. Covers imports, mutability, exceptions, type hints, comprehensions, decorators, docstrings, and formatting. |

### Integration Skills
[ref: #asr-integration]

Read-only connectors to external systems and observability tools. These skills never mutate data in the target system.

| Skill | Purpose |
|-------|---------|
| **atlassian-skill** | Read-only access to Atlassian Jira and Confluence via MCP: issue search/reading, project issues, page search/reading, daily page diffs, and page history. |
| **loki-skill** | Read-only Grafana Loki log investigation through `logcli`: querying logs, labels, series, and metadata with narrow-first guardrails and output size limits. |

### On-Demand Skills
[ref: #asr-ondemand]

Rarely used skills registered in `OnDemand/SKILL.md`. The agent evaluates their compressed triggers at runtime and loads the full `SKILL.md` only on a match.

| Skill | Purpose |
|-------|---------|
| **bobplus-api** | Integration knowledge for the Bobplus Payments API (Africa): bearer auth, RSA request signing, `X-Hash`, C2B payins, B2C payouts, account services, bank/MNO lookups, transaction status, and webhook callbacks. |
| **code-review** | Language-agnostic rigorous code review for features (diff against `main`/`master`) or whole projects. Spawns parallel specialist subagents, classifies findings by severity, and emits both machine-readable and human-readable reports. |
| **protobuf-lang** | Buf Protobuf lint and schema style. Governs `buf.yaml`, packages, imports, enums, messages, services, RPCs, and comments against the Buf STANDARD rule set. |
| **pytest-design** | Mandatory skill for writing, editing, running, and reviewing Python unit tests, integration tests, and pytest suites. Covers fixtures, parametrization, mocking, markers, async tests, coverage, xdist, and faker-driven test data. |
| **pytest-planner** | Generates repository-specific pytest enablement artifacts for a Python project: a test-authoring/research prompt and an iteration-ready unit-test coverage plan pinned to the exact `pytest-design` reference anchors. |
| **repo-audit** | Creates and maintains repo cards (`repos/<repo>/overview`), business-domain reports (`repos/<repo>/business`), and dependency cards (`repos/<repo>/dependencies`) in Serena memory. Supports FULL, PARTIAL, and REFRESH run modes. |
| **security-audit** | SAST workflow aligned with OWASP API Security Top 10 2023. Uses a mandatory screener to select applicable vulnerability scans and dispatches parallel detector subagents for SQLi, XSS, IDOR, SSRF, JWT, BOLA/BOPLA, misconfiguration, and others. |
| **session-inspector** | Token-cheap inspection of Kimi Code CLI session files under `~/.kimi/sessions`. Agents MUST use the provided script instead of reading raw JSONL. |
| **temporal-lang** | Guidance for Temporal durable execution across Python, TypeScript, Go, Java, .NET, and Ruby: workflow determinism, activities, signals, queries, versioning, continue-as-new, saga patterns, and troubleshooting non-determinism errors. |

### Drafts
[ref: #asr-drafts]

Skills under construction. They live in `Drafts/` and are excluded from discovery until they are promoted.

| Skill | Purpose |
|-------|---------|
| **graphify-protocol** (draft) | Converts any codebase, document set, or media collection into a persistent knowledge graph. Produces `graph.html`, `graph.json`, `GRAPH_REPORT.md`, and supports query/path/explain operations, incremental updates, and exports to Neo4j, Obsidian, GraphML, and MCP. |
| **nim-docgen** (draft) | *Description pending.* |
| **ruff-style** (draft) | Ruff rule corpus and enforcement reference for Python code style. |
| **serena-audit** (draft) | Reconciles Serena memory files against their source repositories. Audits YAML frontmatter, commit/branch freshness, naming conventions, and contradictions; produces and executes a two-phase reconciliation plan. |

## How Skills Are Discovered
[ref: #asr-discovery]

Agent runtimes that consume this registry must:

1. Locate every `SKILL.md` under the skill search paths, excluding `Drafts/*/SKILL.md`.
2. Parse the YAML frontmatter of each `SKILL.md` in a single batch pass.
3. Evaluate `triggers` against the user request and project context.
4. Load the full `SKILL.md` of every matching skill and lazily pull referenced sections as needed.
5. Evaluate the `ondemand:` manifest in `OnDemand/SKILL.md` at runtime and load `OnDemand/<name>/SKILL.md` only when an entry matches.

A skill declares its activation rules in frontmatter. Triggers may be unconditional (`always: true`), file-based, keyword-based, or compound `any`/`all` conditions.

## Justfile Integration
[ref: #asr-justfile]

This registry does not ship a `Justfile`. Skills that reference `just serena-checkpoint` or `just sync-skills-mirror` expect the consuming project to declare the recipes in its own `Justfile`. The checkpoint recipe is a persistence helper for the `.serena/` memory repository:

```just
DATETIME := `TZ=UTC date '+%Y-%m-%dT%H:%M:%SZ'`
WORKDIR := env('PWD', '')

[group('agent')]
serena-checkpoint:
    @cd "{{ WORKDIR }}/.serena" && \
        git add . && \
        git commit -m "Checkpoint at {{ DATETIME }}" 2>/dev/null || \
        true
```

## Conventions
[ref: #asr-conventions]

- **English only** for skill content, memory entries, and internal reasoning.
- **YAML frontmatter** is mandatory on every `SKILL.md`, `README.md` when required by a protocol, and every Serena memory file.
- **Lazy loading** via `[ref: #anchor]` is the default reading mode; agents must not ingest full reference trees unless the task requires it.
- **Subagent orchestration** is preferred for investigations, audits, and reviews; root agents act as routers and synthesizers.
- **Artifact paths** are deterministic: `repos/<repo>/`, `.serena/memories/`, `.reports/`, `graphify-out/`.
