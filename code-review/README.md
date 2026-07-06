# code-review

Language-agnostic code-review protocol for Kimi agents.

## What this skill does

`code-review` defines a repeatable, multi-phase code-review workflow that delegates inspection work to specialist subagents. It contains no runtime service; it is consumed as Markdown documentation and subagent prompts. The skill covers:

- Two review modes:
  - **Feature / diff-based review** — reviews changes between a base branch and `HEAD`.
  - **Full-project review** — reviews the entire codebase.
- A five-level severity taxonomy.
- Mandatory report boilerplate and file naming.
- A six-phase workflow:
  1. Scope and skill selection.
  2. Architecture reconnaissance.
  3. Parallel specialist inspection.
  4. Finding validation.
  5. Consolidation.
  6. Persistence.
- Four specialist subagent prompts:
  - Security and configuration.
  - Correctness, concurrency, and performance.
  - Resilience and observability.
  - Architecture and maintainability.

## When to use it

Use this skill when the request involves:

- Code review, PR review, or diff review.
- Reviewing a feature, project, or repository.
- Checking correctness, security, performance, concurrency, resilience, observability, or architecture.

The skill responds to prompts such as "code review", "review code", "PR review", "ревью", "код-ревью", and "проверь код".

## Repository layout

```text
code-review/
├── references/           # Checklist, report templates, and specialist subagent prompts
│   ├── checklist.md
│   ├── report-templates.md
│   ├── subagent-architecture-and-maintainability.md
│   ├── subagent-correctness-concurrency-performance.md
│   ├── subagent-resilience-and-observability.md
│   └── subagent-security-and-configuration.md
└── SKILL.md              # Skill entry point with workflow and routing
```

## How to use this skill

1. Open `SKILL.md` and determine the review mode (feature or full-project).
2. For feature mode, gather the diff with `git diff {{ BASE_BRANCH }}...HEAD`.
3. Load `references/checklist.md` for the language-agnostic review checklist.
4. Load `references/report-templates.md` for the mandatory report skeleton.
5. Dispatch the four specialist subagents in parallel using the prompts under `references/subagent-*.md`.
6. Validate findings and write the consolidated report using the template.
7. Persist the machine-readable report as a Serena memory entry with the required YAML frontmatter.

## Reference index

| File | Purpose |
|------|---------|
| `references/checklist.md` | Language-agnostic review checklist |
| `references/report-templates.md` | Machine-readable and human-readable report templates |
| `references/subagent-security-and-configuration.md` | Security and configuration specialist prompt |
| `references/subagent-correctness-concurrency-performance.md` | Correctness, concurrency, and performance specialist prompt |
| `references/subagent-resilience-and-observability.md` | Resilience and observability specialist prompt |
| `references/subagent-architecture-and-maintainability.md` | Architecture and maintainability specialist prompt |

## Conventions

- `SKILL.md` is the single entry point.
- Reports must begin with the standard Serena YAML frontmatter.
- Machine-readable reports are written in English; human-readable reports are written in Russian.
- Timestamps use UTC ISO 8601 format.
- Severity follows the five-level taxonomy defined in `SKILL.md`.
- Feature-mode reviews use the base branch diff as the primary scope.
- Four specialist subagents run in parallel during the inspection phase.

## Optional cross-validation

Feature-mode reviews may use the CodeRabbit CLI (`coderabbit review`) for advisory cross-validation when it is available.
