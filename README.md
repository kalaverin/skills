# Agent Skills Registry

A curated collection of execution skills for Kimi Code CLI and compatible agentic runtimes. Each skill is a self-contained directory with a `SKILL.md` entry point and a `references/` folder containing routing tables, subagent prompts, checklists, and rulebooks.

Skills are not libraries. They are operational protocols: they define when the agent must activate, which tools it must use, which subagents it must spawn, and where artifacts must be written. Every skill follows the same layout so an agent can discover, load, and route against it deterministically.

## Repository Layout

```
.
├── AGENTS.md                    # Runtime-wide startup gate and MCP usage contract
├── <skill-name>/
│   ├── SKILL.md                 # Entry point: frontmatter, triggers, routing index
│   └── references/              # Lazy-loaded sections referenced by [ref: #...] anchors
└── README.md                    # This file
```

A skill is active when its trigger matches the user request or project context. The agent then loads `SKILL.md`, resolves the relevant `[ref: #...]` anchors, and executes the referenced section only.

## Skill Catalog

### Runtime Protocols

Skills that govern the agent itself, its tool selection, and its startup behavior.

| Skill | Purpose |
|-------|---------|
| **preflight-checklist** | A compliance gate loaded in every session. Verifies that `shell-protocol` and `serena-protocol` have been discovered and loaded before any user-facing output. |
| **shell-protocol** | Mandates modern CLI tooling for filesystem, search, and Python operations: `lsd`, `fd`, `rg`, `ruplacer`, `uv`, `ruff`. Replaces legacy `ls`, `find`, `grep`, `sed`, `pip`, `black`, `flake8`, etc. |
| **serena-protocol** | Defines the Serena MCP contract: memory namespaces, YAML frontmatter schema, entity-card prerequisites, mutation rules, and the `just agent-memory-commit` persistence ritual. |

### Languages & API Design

Skills that enforce language-specific and API-specific rules.

| Skill | Purpose |
|-------|---------|
| **api-design** | Enforces Google AIP compliance for resource-oriented APIs: resource naming, standard methods, custom methods, pagination, filtering, planes, compatibility guarantees, and HTTP/gRPC transcoding. |
| **protobuf-lang** | Buf Protobuf lint and schema style. Governs `buf.yaml`, packages, imports, enums, messages, services, RPCs, and comments against the Buf STANDARD rule set. |
| **python-lang** | Mandatory Google Python Style Guide enforcement plus a Ruff self-linting protocol. Covers imports, mutability, exceptions, type hints, comprehensions, decorators, docstrings, and formatting. |
| **temporal-lang** | Guidance for Temporal durable execution across Python, TypeScript, Go, Java, .NET, and Ruby: workflow determinism, activities, signals, queries, versioning, continue-as-new, saga patterns, and troubleshooting non-determinism errors. |

### Knowledge & Architecture

Skills that extract, structure, and navigate project knowledge.

| Skill | Purpose |
|-------|---------|
| **graphify-protocol** | Converts any codebase, document set, or media collection into a persistent knowledge graph. Produces `graph.html`, `graph.json`, `GRAPH_REPORT.md`, and supports query/path/explain operations, incremental updates, and exports to Neo4j, Obsidian, GraphML, and MCP. |
| **project-audit** | Creates and maintains Serena entity cards (`entities/<entity>`) for services, libraries, repositories, and infrastructure components. Orchestrates a read-only explorer subagent and writes scoped findings to `bugs/`, `notes/`, `decisions/`, `style/`, `todo/`. |

### Audits & Reviews

Skills that inspect code, dependencies, business logic, and memory state.

| Skill | Purpose |
|-------|---------|
| **business-audit** | Extracts the business layer from source code for a single entity: domain entities, processes, rules, invariants, actors, integrations, and risks. Requires an existing entity card and project glossary. |
| **code-review** | Language-agnostic rigorous code review for features (diff against `main`/`master`) or whole projects. Spawns parallel specialist subagents, classifies findings by severity, and emits both machine-readable and human-readable reports. |
| **dependencies-audit** | Builds exhaustive per-service dependency cards (`logic/<entity>/dependencies.md`): public interfaces, downstream calls, databases, external integrations, libraries, infrastructure, and mandatory Mermaid diagrams. |
| **security-audit** | SAST workflow aligned with OWASP API Security Top 10 2023. Uses a mandatory screener to select applicable vulnerability scans and dispatches parallel detector subagents for SQLi, XSS, IDOR, SSRF, JWT, BOLA/BOPLA, misconfiguration, and others. |
| **serena-audit** | Reconciles Serena memory files against their source repositories. Audits YAML frontmatter, commit/branch freshness, naming conventions, and contradictions; produces and executes a two-phase reconciliation plan. |

## How Skills Are Discovered

Agent runtimes that consume this registry must:

1. Locate every `SKILL.md` under the skill search paths.
2. Parse the YAML frontmatter of each `SKILL.md` in a single batch pass.
3. Evaluate `triggers` against the user request and project context.
4. Load the full `SKILL.md` of every matching skill and lazily pull referenced sections as needed.

A skill declares its activation rules in frontmatter. Triggers may be unconditional (`always: true`), file-based, keyword-based, or compound `any`/`all` conditions.

## Conventions

- **English only** for skill content, memory entries, and internal reasoning.
- **YAML frontmatter** is mandatory on every `SKILL.md` and every Serena memory file.
- **Lazy loading** via `[ref: #anchor]` is the default reading mode; agents must not ingest full reference trees unless the task requires it.
- **Subagent orchestration** is preferred for investigations, audits, and reviews; root agents act as routers and synthesizers.
- **Artifact paths** are deterministic: `entities/<entity>`, `logic/<entity>/`, `.serena/memories/`, `.reports/`, `graphify-out/`.
