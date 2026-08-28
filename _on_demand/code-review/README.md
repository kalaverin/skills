# code-review
[ref: #cr-intro]

Runs a thorough, language-agnostic review of your code or pull request.

## What it does
[ref: #cr-what]

This skill delegates code inspection to five parallel specialist subagents, each focused on a narrow domain: security and configuration, correctness and concurrency, resilience and observability, architecture and maintainability, and the adversarial "existence inquisition." It supports two review modes: a diff-based review for feature branches and a full-project review for audits. Every finding is classified into one of five severity levels and recorded in both a machine-readable Serena memory entry and a human-readable report. The workflow also includes a mandatory Google AIP design review and an optional CodeRabbit cross-validation pass.

## When it activates
[ref: #cr-when]

Activates when you ask for a code review, PR review, diff review, or project review in English or Russian.

Examples:

- "Review this pull request"
- "Check this diff for bugs"
- "Audit the whole project"
- "Review feature branch user-auth against main"
- "Проверь код"
- "Ревью проекта"

## How to run / use it
[ref: #cr-how]

Ask the agent to review your code.
For a feature review, make sure your branch has commits and a base branch exists; the agent will use `git diff` to determine scope and may launch CodeRabbit in the background.
For a full-project review, the agent will inspect the entire source tree.
The agent auto-detects language- and domain-specific skills triggered by the codebase and applies them during the review.
If you are on a branch other than `main` or `master`, the agent will ask you to choose the review mode.
Tests are skipped unless you explicitly ask to review them.

## What it produces
[ref: #cr-produces]

- A machine-readable report under `.serena/memories/review/` named `feature_YYYYMMDDTHHMMSSZ.md` or `project_YYYYMMDDTHHMMSSZ.md`.
- A human-readable report under `.reports/` (or `.reports/<entity>/` when the entity is known) named per `SKILL.md` Section 2.2: `review-YYYY-mmdd-HHMM-project.md`, or `review-YYYY-mmdd-HHMM-feature.md` with optional branch-key / feature-slug forms such as `review-YYYY-mmdd-HHMM-WGNBCK4176-rate-limiting.md`.
- Findings grouped by severity, with dedicated sections for architecture, API design (AIP), security, resilience, observability, data privacy, and the existence inquisition.
- Optional CodeRabbit cross-validation in feature mode.

## Dependencies and why they matter
[ref: #cr-deps]

- `api-design` — supplies the Google AIP corpus used in the mandatory architectural design review.
- `discuss-first` — owns the existence-review standard applied by the fifth specialist subagent.
- `frontmatter-protocol` — governs tracking fields and lazy-load routing used when reading reference files.
- `serena-protocol` — provides the memory-mutation rules for writing machine-readable reports into `.serena/memories/`.

## Strengths and trade-offs
[ref: #cr-tradeoffs]

### Strong sides
[ref: #cr-strong]

- Language-agnostic: works for any programming language and adapts to language-specific skills when available.
- Parallel specialist review gives broad coverage without the agent trying to be an expert in every domain at once.
- Mandatory AIP and existence-inquisition passes catch design overreach and unnecessary code that simpler reviews miss.
- Severity-based classification makes it easy to prioritize follow-ups.

### Weak sides / limits
[ref: #cr-weak]

- Higher token and wall-clock cost than a single-pass review because of the five subagents and optional CodeRabbit run.
- The agent does not patch code; it only reports findings.
- Feature mode requires a known base branch and an explicit mode decision on non-main branches.
- CodeRabbit is advisory and may refuse large diffs.

### Common pitfalls / gotchas
[ref: #cr-pitfalls]

- On a non-`main`/`master` branch the agent must ask for the review mode; do not expect it to guess.
- Boilerplate file names and metadata are mandatory; the agent will not invent alternative patterns.
- The human-readable report is written in Russian; the machine-readable memory entry is in English.
- Every finding must map to a real line in the reviewed files; hallucinated entries are dropped.

## Repository layout
[ref: #cr-layout]

```text
_on_demand/code-review/
├── references/           # Checklist, report templates, and specialist subagent prompts
│   ├── checklist.md
│   ├── report-templates.md
│   ├── subagent-architecture-and-maintainability.md
│   ├── subagent-correctness-concurrency-performance.md
│   ├── subagent-existence-inquisition.md
│   ├── subagent-resilience-and-observability.md
│   └── subagent-security-and-configuration.md
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview
[ref: #cr-refs]

| File | What it covers |
|------|----------------|
| `references/checklist.md` | Language-agnostic review checklist |
| `references/report-templates.md` | Machine-readable and human-readable report templates |
| `references/subagent-security-and-configuration.md` | Security, privacy, and configuration specialist prompt |
| `references/subagent-correctness-concurrency-performance.md` | Correctness, concurrency, and performance specialist prompt |
| `references/subagent-resilience-and-observability.md` | Resilience, observability, and logging specialist prompt |
| `references/subagent-architecture-and-maintainability.md` | Architecture and maintainability specialist prompt |
| `references/subagent-existence-inquisition.md` | Adversarial existence-review specialist prompt |

## Important conventions / gotchas
[ref: #cr-conventions]

- Requires `serena-protocol` when writing machine-readable reports into `.serena/memories/`.
- Language-specific style rules come from sibling skills such as `python-lang` or `protobuf-lang`.
- The agent uses the repository default branch as the comparison base; confirm if it is not `main` or `master`.
- Tests are skipped unless you explicitly ask to review them.
- Machine-readable reports are in English; human-readable reports are in Russian.
- A `CRITICAL` finding must include a clear explanation of why production will break.
