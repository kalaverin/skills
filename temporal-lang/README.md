# temporal-lang

Provides guidance, patterns, and SDK-specific recipes for building reliable Temporal durable-execution applications.

## What it does

This skill is a documentation library for Temporal.
It helps the agent design workflows and activities, keep workflow code deterministic, use signals/queries/updates/child workflows, version running workflows, troubleshoot stuck workflows and non-determinism errors, and apply task-queue priority and fairness.
It includes per-SDK guidance for Python, TypeScript, Go, Java, .NET, and Ruby, plus a catalog of third-party integrations.

## When it activates

Activates when the project contains Temporal SDK code or when you ask about Temporal concepts.

Typical triggers:

- The repo imports a Temporal SDK such as `@temporalio`, `temporalio`, or `go.temporal.io`.
- You mention workflows, activities, workers, signals, queries, heartbeats, versioning, `continue-as-new`, child workflows, or saga patterns.
- You ask about Temporal CLI, Temporal Server, or Temporal Cloud.

Example prompts:

- "Add a new workflow that calls an activity."
- "Why is my workflow failing with a non-determinism error?"
- "Show me how to query a running workflow."
- "Set up a Python Temporal worker."
- "How do I version this workflow safely?"

## How to use it

Ask the agent to build, review, or debug your Temporal code.
The agent reads the language-agnostic `references/core/` guides first and then pulls in the relevant SDK-specific reference.
If you want to run a local Temporal server, install the Temporal CLI; the skill points to `references/core/install_cli.md` for instructions.

## What it produces

- Workflow, activity, and worker code.
- Determinism checks and replay guidance.
- Debugging steps for stuck workflows or non-determinism errors.
- Versioning, signal, query, and update patterns.
- CLI and operational recommendations.

## Repository layout

```text
temporal-lang/
├── references/
│   ├── core/               # Language-agnostic Temporal concepts
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
│   ├── dotnet/             # .NET SDK reference
│   ├── go/                 # Go SDK reference
│   ├── java/               # Java SDK reference (with Spring integrations)
│   ├── python/             # Python SDK reference (with AI/LLM integrations)
│   ├── ruby/               # Ruby SDK reference
│   ├── typescript/         # TypeScript SDK reference
│   └── integrations.md     # Catalog of third-party integrations
├── LICENSE
└── SKILL.md                # Agent entry point: manifest, version, and routing index
```

## Reference overview

| File / Directory | What it covers |
|------------------|----------------|
| `references/core/determinism.md` | Why determinism matters and replay mechanics |
| `references/core/patterns.md` | Signals, queries, updates, child workflows, and sagas |
| `references/core/versioning.md` | Patching, worker build IDs, and `continue-as-new` |
| `references/core/troubleshooting.md` | Stuck workflows and non-determinism errors |
| `references/core/error-reference.md` | Workflow status vocabulary and error codes |
| `references/core/gotchas.md` | Common pitfalls |
| `references/core/install_cli.md` | Temporal CLI installation |
| `references/core/interactive-workflows.md` | Interactive workflow patterns |
| `references/core/priority-fairness.md` | Task-queue priority and fairness |
| `references/core/dev-management.md` | Developer and team workflows |
| `references/core/ai-patterns.md` | AI patterns for durable execution |
| `references/integrations.md` | Third-party integrations catalog |
| `references/python/` | Python SDK guidance |
| `references/typescript/` | TypeScript SDK guidance |
| `references/go/` | Go SDK guidance |
| `references/java/` | Java SDK guidance |
| `references/dotnet/` | .NET SDK guidance |
| `references/ruby/` | Ruby SDK guidance |

## Important conventions / gotchas

- This skill contains guidance, not runtime code or SDK replacements.
- Install the Temporal CLI before running a local development server.
- Determinism rules are the foundation of durable execution; the agent applies them strictly.
- SDK examples connect to `localhost:7233` by default.
