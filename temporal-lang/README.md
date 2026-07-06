# temporal-lang

Agent skill for building, debugging, and managing Temporal durable-execution applications.

## What this skill does

`temporal-lang` is a documentation library that provides guidance, patterns, and reference material for Temporal applications. It is consumed by coding agents as Markdown references and contains no runtime code. The skill covers:

- Workflow and activity design.
- Determinism rules and Event History replay semantics.
- Signals, queries, updates, and child workflows.
- Versioning strategies: patching, worker build IDs, and `continue-as-new`.
- Troubleshooting stuck workflows and non-determinism errors.
- Task-queue priority and fairness.
- AI patterns for durable execution.
- Developer management and operational guidance.
- Per-SDK quick starts and conventions for Python, TypeScript, Go, Java, .NET, and Ruby.
- Third-party integrations (Spring Boot, Spring AI, OpenAI Agents SDK, LangSmith, LangGraph, Google ADK).

## When to use it

Load this skill when the request involves:

- Building workflows, activities, or workers with a Temporal SDK.
- Debugging non-determinism errors, stuck workflows, or activity retries.
- Using Temporal CLI, Temporal Server, or Temporal Cloud.
- Working with durable-execution concepts such as signals, queries, heartbeats, versioning, `continue-as-new`, child workflows, or saga patterns.

## Repository layout

```text
temporal-lang/
├── references/
│   ├── core/                  # Language-agnostic Temporal concepts
│   │   ├── ai-patterns.md
│   │   ├── determinism.md
│   │   ├── dev-management.md
│   │   ├── error-reference.md
│   │   ├── gotchas.md
│   │   ├── install_cli.md
│   │   ├── interactive-workflows.md
│   │   ├── patterns.md
│   │   ├── priority-fairness.md
│   │   ├── troubleshooting.md
│   │   └── versioning.md
│   ├── dotnet/                # .NET SDK reference
│   ├── go/                    # Go SDK reference
│   ├── java/                  # Java SDK reference (with Spring integrations)
│   ├── python/                # Python SDK reference (with AI/LLM integrations)
│   ├── ruby/                  # Ruby SDK reference
│   ├── typescript/            # TypeScript SDK reference
│   └── integrations.md        # Catalog of third-party integrations
├── LICENSE
└ SKILL.md                     # Skill entry point and manifest
```

## How to use this skill

1. Open `SKILL.md` for the manifest, version, and trigger conditions.
2. Identify whether the question is language-agnostic or SDK-specific.
3. For language-agnostic topics, start with `references/core/`.
4. For SDK-specific topics, open the matching `references/{python,typescript,go,java,dotnet,ruby}/` directory.
5. Extract only the relevant section using the `[ref: #...]` anchors inside the reference files.
6. Apply the determinism rules strictly; they are the foundation of durable execution.

## Core reference index

| File | Topic |
|------|-------|
| `references/core/determinism.md` | Command/Event mapping and replay semantics |
| `references/core/patterns.md` | Signals, queries, updates, child workflows, sagas |
| `references/core/versioning.md` | Patching, worker build IDs, `continue-as-new` |
| `references/core/troubleshooting.md` | Stuck workflows and non-determinism errors |
| `references/core/error-reference.md` | Workflow status vocabulary and error codes TMPRL1100–TMPRL1103 |
| `references/core/gotchas.md` | Common pitfalls |
| `references/core/install_cli.md` | Temporal CLI installation |
| `references/core/interactive-workflows.md` | Interactive workflow patterns |
| `references/core/priority-fairness.md` | Task-queue priority and fairness |
| `references/core/dev-management.md` | Developer and team workflows |
| `references/core/ai-patterns.md` | AI patterns for durable execution |
| `references/integrations.md` | Third-party integrations |

## SDK reference index

| Directory | SDK |
|-----------|-----|
| `references/python/` | Python SDK |
| `references/typescript/` | TypeScript SDK |
| `references/go/` | Go SDK |
| `references/java/` | Java SDK |
| `references/dotnet/` | .NET SDK |
| `references/ruby/` | Ruby SDK |

## Conventions

- `SKILL.md` is the single entry point and declares the skill version (`0.4.0`).
- Reference files are grouped by SDK and by core concept.
- Examples connect to a local Temporal server (`localhost:7233`) by default.
- The skill is licensed under the MIT License; see `LICENSE`.
