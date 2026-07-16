# code-review

Runs a thorough, language-agnostic review of your code or pull request.

## What it does

This skill performs repeatable code reviews by delegating inspection work to specialist subagents.
It supports two modes: a feature/diff-based review for pull requests, and a full-project review for audits.
Findings are classified into five severity levels from `INFO` to `CRITICAL` and written into both a machine-readable Serena memory report and a human-readable report.

## When it activates

Activates when you ask for a code review, PR review, diff review, or project review.
Examples:
- "Review this pull request"
- "Check this diff for bugs"
- "Audit the whole project"
- "Review feature branch user-auth against main"

## How to use it

Ask the agent to review your code.
For a feature review, make sure your branch has commits and a base branch exists; the agent will use `git diff` to determine scope.
For a full-project review, the agent will inspect the entire source tree.
The agent auto-detects language- and domain-specific skills triggered by the codebase and applies them during the review.
If you are on a branch other than `main` or `master`, the agent will ask you to choose the review mode.

## What it produces

- A machine-readable report under `.serena/memories/review/` named `feature_YYYYMMDDTHHMMSSZ.md` or `project_YYYYMMDDTHHMMSSZ.md`.
- A human-readable report under `.reports/` named `review-YYYY-mmdd-HHMM-feature.md` or `review-YYYY-mmdd-HHMM-project.md`.
- Findings grouped by severity, with sections for architecture, security, resilience, observability, and data privacy.
- Optional CodeRabbit cross-validation in feature mode.

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
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/checklist.md` | Language-agnostic review checklist |
| `references/report-templates.md` | Machine-readable and human-readable report templates |
| `references/subagent-security-and-configuration.md` | Security, privacy, and configuration specialist prompt |
| `references/subagent-correctness-concurrency-performance.md` | Correctness, concurrency, and performance specialist prompt |
| `references/subagent-resilience-and-observability.md` | Resilience, observability, and logging specialist prompt |
| `references/subagent-architecture-and-maintainability.md` | Architecture and maintainability specialist prompt |

## Important conventions / gotchas

- Requires `serena-protocol` when writing machine-readable reports into `.serena/memories/`.
- Language-specific style rules come from sibling skills such as `python-lang` or `protobuf-lang`.
- The agent uses the repository default branch as the comparison base; confirm if it is not `main` or `master`.
- Tests are skipped unless you explicitly ask to review them.
- Machine-readable reports are in English; human-readable reports are in Russian.
