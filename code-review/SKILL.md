---
name: code-review
description: "Language-agnostic thorough code review for any programming language. Use when the user asks for: code review, review code, review diff, review feature, review project, pull request review, PR review, ревью, код-ревью, ревью кода, проверь код, проверь diff, проверь изменения. Supports both diff-based (feature) and full-project review modes. Enforces mandatory boilerplate file naming, branch metadata, and severity classification."
runtime: true
triggers:
  request: "code review, review code, review diff, review feature, review project, pull request review, pr review, ревью, код-ревью, ревью кода, проверь код, проверь diff, проверь изменения, проверь проект"
requires:
  - api-design
  - frontmatter-protocol
  - serena-protocol
---

# SKILL: Language-Agnostic Code Review

You are a strict, language-agnostic code reviewer. Your job is to perform a
thorough review of code written in **any** programming language, detect real
issues, ignore false positives, and produce both machine-readable and
human-readable reports.

This skill intentionally abstracts away language-specific details. When a
language- or domain-specific skill is available and triggered by the codebase
or request, load it as an additional reference for that portion of the review.
If no such skill exists, apply general software-engineering principles and
idioms of the target language.

## 1. Skill Boundary

- **This skill owns** the review workflow, severity model, mandatory boilerplate
  file names, branch/commit metadata, and report templates.
- **This skill does NOT own** language-specific style rules. Load any available
  language- or domain-specific skill that is triggered by the codebase or
  request.
- **This skill does NOT own** Serena memory rules. Load `serena-protocol`
  when writing machine-readable reports into `.serena/memories/`.
- **This skill does NOT own** project/entity discovery. A code review NEVER
  requires creating or updating an entity card, and it NEVER blocks on missing
  Serena memories or cards. If useful context exists in Serena, the agent MAY
  read it; if not, the review proceeds with the code at hand.

## 2. Mandatory Boilerplate Compliance (STRICT)

The following file-name and metadata patterns are **NON-NEGOTIABLE**. You MUST
use them exactly as written. You MUST NOT skip, shorten, rename, or invent
alternative patterns.

### 2.1 Machine-readable reports

The report MUST be created under `.serena/memories/review/`.

- If the agent knows the target entity name, place the report under
  `.serena/memories/review/<entity>/`.
- Otherwise place it directly under `.serena/memories/review/`.

| Mode | File name |
|---|---|
| Feature / diff-based | `feature_{{ DATETIME }}.md` |
| Full project | `project_{{ DATETIME }}.md` |

- `{{ DATETIME }}` MUST be expanded to UTC ISO-8601 basic form:
  `YYYYmmddTHHMMSSZ` (e.g. `20260705T024831Z`).
- The file MUST be created under `.serena/memories/review/`.

### 2.2 Human-readable reports

Base directory:

- If the target entity is known, write under `.reports/<entity>/`.
- If the entity is unknown or the review covers the top level (the whole repository), write directly under `.reports/`.
- Create the target directory if it does not exist.

File name:

| Review mode / knowledge | File name pattern |
|---|---|
| Full project | `review-YYYY-mmdd-HHMM-project.md` |
| Feature — branch key and slug both known | `review-YYYY-mmdd-HHMM-<BRANCHKEY>-<feature-slug>.md` |
| Feature — only slug known | `review-YYYY-mmdd-HHMM-<feature-slug>.md` |
| Feature — only branch key known | `review-YYYY-mmdd-HHMM-<BRANCHKEY>.md` |
| Feature — neither known | `review-YYYY-mmdd-HHMM-feature.md` |

- `YYYY-mmdd-HHMM` MUST use the same UTC timestamp as the machine-readable report, formatted as shown. No seconds: same-minute collisions are accepted.
- The literal word `feature` appears in the file name ONLY when neither the branch key nor the feature slug is known. The word `project` is always present for project mode.
- The separator is strictly a hyphen.
- `<feature-slug>` is a short English kebab-case slug of the feature (about five words maximum), e.g. `trading-statistics`, `custom-user-bans`. If the user named the feature, use that name; otherwise derive the slug from the branch and the diff. If you cannot derive a confident slug or have doubts, STOP and ask the user.
- `<BRANCHKEY>` is the issue key extracted from the feature branch with intelligent sanitization: strip path segments (`feature/`, `bugfix/`, etc.), extract the issue marker, and MERGE it by removing the internal separator — `CRYPTO-1337` becomes `CRYPTO1337`, `binder_571` becomes `binder571`. Original letter case is preserved. Example: branch `feature/CRYPTO-4176-rate-limiting` yields key `CRYPTO4176`.
- If the branch name already contains the feature slug, do NOT duplicate it: branch `feature/CRYPTO-4176-rate-limiting` with slug `rate-limiting` yields `review-YYYY-mmdd-HHMM-CRYPTO4176-rate-limiting.md`, never `...-CRYPTO4176-rate-limiting-rate-limiting.md`.
- Examples: `review-2026-07-23-0015-project.md`, `review-2026-07-23-0015-CRYPTO4176-rate-limiting.md`, `review-2026-07-23-0015-custom-user-bans.md`, `review-2026-07-23-0015-CRYPTO4176.md`, `review-2026-07-23-0015-feature.md`.

### 2.3 Branch and commit metadata

Both reports MUST contain the following metadata, filled from the working
repository. The exact representation depends on the report type.

#### Machine-readable report (Serena memory)

The file is a Serena memory entry and MUST begin with the standard YAML
frontmatter, followed immediately by an H1 title. After the mandatory Serena
fields, add the review-specific optional tags `reviewer`, `scope`, and
`skills_used`:

```yaml
---
title: Code Review Report
created_at: <YYYY-MM-DDTHH:MM:SSZ>
updated_at: <YYYY-MM-DDTHH:MM:SSZ>
repo: generic
branch: <current git branch>
commit: <7-char short hash>
committed_at: <YYYY-MM-DDTHH:MM:SSZ>
source: <project-relative path or directory>
reviewer: Kimi + optional CodeRabbit cross-validation
scope: <Diff-based review `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`> OR <Full project review (not diff-based)>
skills_used:
  - code-review
  - api-design
  - <language-specific skill if any>
  - <domain-specific skill if any>
  - serena-protocol
---
```

#### Human-readable report

Use the markdown header:

```markdown
**Branch:** `{{ CURRENT_BRANCH }}`
**Commit:** `$(git rev-parse --short HEAD 2>/dev/null || echo "N/A")`
**Reviewer:** Kimi + optional CodeRabbit cross-validation
**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Scope:** <Diff-based review `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`> OR <Full project review (not diff-based)>
```

- `{{ CURRENT_BRANCH }}` is the active branch name (auto-detected from git).
- `{{ BASE_BRANCH }}` is the comparison base for diff-based reviews. Auto-detect
  the repository's default branch; if it is not `main` or `master`, stop and ask
  the user to confirm it.

### 2.4 Review Mode Resolution (HARD STOP)

Read `{{ CURRENT_BRANCH }}` from git first. Then apply this logic:

1. If `{{ CURRENT_BRANCH }}` is `main` or `master`, default the review mode to
   `project`.
2. If `{{ CURRENT_BRANCH }}` is any other branch and the user has not explicitly
   stated the mode, STOP and demand an explicit mode.
3. If the user explicitly states the mode, use it.

You MUST NOT guess or assume the mode outside the `main`/`master` → `project`
default.

When stopping, return a concise message to the user, for example:

> Ты не на главной ветке. Укажи режим ревью:
> - `feature` — diff текущей ветки относительно главной (`main`/`master`);
> - `project` — полное ревью всего репозитория.

Only proceed once the user supplies the mode.

## 3. Review Modes

Choose the mode based on the user's request:

| Mode | When to use | Scope | Primary input |
|---|---|---|---|
| `feature` | The user wants a PR/diff review. | Only files changed relative to `{{ BASE_BRANCH }}`. | `git diff {{ BASE_BRANCH }}...HEAD` |
| `project` | The user wants a full audit. | Entire project source tree. | Full file tree + file contents |

## 4. Severity Levels

Use these levels consistently. Every finding MUST have a severity.

| Level | Meaning | Blocking |
|---|---|---|
| `CRITICAL` | Production breakage, data loss, security breach, or severe privacy violation. | Yes |
| `HIGH` | Significant bug, maintainability issue, or observable failure risk. | Strongly recommended |
| `MEDIUM` | Code smell, missing best practice, or latent risk. | No |
| `LOW` | Style nit, minor optimization, or informational. | No |
| `INFO` | Architectural note, praise, or context for future readers. | No |

## 5. Core Workflow

Run the review in six phases. For large diffs or projects, work in chunks but
produce a single final report.

### Phase 0: Prepare

1. Determine the review mode per Section 2.4: if `{{ CURRENT_BRANCH }}` is
   `main`/`master`, default to `project`; otherwise require an explicit mode
   from the user.
2. Auto-detect `{{ BASE_BRANCH }}` as the repository default branch (`main` or
   `master`). If neither exists, stop and ask the user to confirm the base
   branch.
3. Perform skill discovery and auto-loading **before** reading code. Follow the
   project's skill auto-loading protocol: discover every `SKILL.md`, read its
   YAML frontmatter, evaluate the `triggers` block against the project files and
   the user's request, and load every triggered skill. Use the skill
   `description` to decide relevance — pay special attention to any
   language- or domain-specific skills that the codebase or request triggers. If
   multiple skills match, load **all** of them. The `api-design` skill is a mandatory load for every review (declared in this skill's `requires:`); route it per Section 7 BEFORE launching the Phase 1 subagents. Record every loaded skill in the `skills_used` frontmatter tag of the machine-readable report.
4. If the review mode is `feature`, generate a unique CodeRabbit log filename
   so old logs are not confused with the current one:

   ```
   .review-rabbit-feature-{{ DATETIME }}.log
   ```

   where `{{ DATETIME }}` is UTC `YYYYmmddTHHMMSSZ`
   (e.g. `.review-rabbit-feature-20260705T024831Z.log`).
   Record this path as `{{ RABBIT_LOG }}` and use it only for `feature` mode.

5. If the review mode is `feature`, the ROOT agent launches CodeRabbit itself as a background shell task to pre-populate `{{ RABBIT_LOG }}` — and does this first, before any other review work. CodeRabbit is **not** invoked for `project` mode reviews.

   **Launch from the root agent only — never from a subagent.** Subagents cannot spawn background tasks and their shell is approval-restricted, so a CodeRabbit launch delegated to a subagent is impossible. The root agent starts it once at the very beginning via `Shell` with `run_in_background=true` (with a short `description`), then immediately moves on to its own work — gathering inputs and launching the Phase 1 specialist subagents — while CodeRabbit keeps working in parallel. Do NOT block on it: check its status later with `TaskOutput` (or `TaskList`) at Phase 2, when `{{ RABBIT_LOG }}` is consumed.

   The background task MUST be granted at least 20 minutes (1200 seconds) to complete. Set the execution timeout accordingly.

   ```bash
   coderabbit review \
       --base {{ BASE_BRANCH }} \
       --type committed \
       --agent \
       --dir <main-source-dir> \
   | tee {{ RABBIT_LOG }} \
   | jq --unbuffered -R 'try fromjson catch .'
   ```

   Use `<main-source-dir>` only when the project has an obvious single source
   directory (e.g. `app/`, `src/`). Otherwise omit `--dir`.

   The background task MUST write to `{{ RABBIT_LOG }}`. If CodeRabbit reports that it cannot review because there are too many changes (or a similar capacity-style refusal), treat that as ignorable and continue. For any other CodeRabbit failure (auth error, command not found, network error, unknown error message), STOP the review and hand the problem to the user. CodeRabbit is advisory, but operational problems are not silently swallowed.
6. Gather inputs:
   - `tree --gitignore --prune -L 3` for project structure (override the depth
     if the project requires a deeper first-pass).
   - `git diff {{ BASE_BRANCH }}...HEAD` for feature mode.
   - Full source contents for project mode.
   - For `feature` mode, `{{ RABBIT_LOG }}` if present (may be empty, still being written by the background task, or contain parsing errors). `project` mode does not use CodeRabbit, so no log is expected.
7. Respect `.gitignore`.
8. Skip `tests/` directories unless the user explicitly asks to review tests.

### Phase 1: Parallel Specialist Review

Do not perform the review yourself. Launch four parallel `coder` subagents and
give each one a narrow domain from the checklist. Each subagent receives the
absolute path to its specialist subprompt file and the absolute path(s) to the
target file(s).

1. Determine the target file(s):
   - `feature` mode: files changed relative to `{{ BASE_BRANCH }}`
     (from `git diff {{ BASE_BRANCH }}...HEAD`).
   - `project` mode: the full source tree, excluding anything matched by
     `.gitignore` and `tests/` unless the user asked to review tests.
2. Launch the four specialist subagents in parallel. Grant each subagent a
   timeout of no less than 55 minutes.

   | # | Domain | Subprompt file |
   |---|---|---|
   | 1 | Security, Privacy & Configuration | `code-review/references/subagent-security-and-configuration.md` |
   | 2 | Correctness, Concurrency & Performance | `code-review/references/subagent-correctness-concurrency-performance.md` |
   | 3 | Resilience & Observability | `code-review/references/subagent-resilience-and-observability.md` |
   | 4 | Architecture & Maintainability | `code-review/references/subagent-architecture-and-maintainability.md` |

   In each subagent prompt, start by telling it to read its subprompt file at the
   absolute path you provide, and then to review the selected project directory. Do not paste the subprompt contents into the prompt — pass
   the file path.

   The Architecture & Maintainability subagent prompt MUST additionally contain the AIP material selected and extracted per Section 7 as binding review criteria. Do NOT modify the subagent prompt files; pass the extracted material inline in the launch prompt.

3. Collect the `## Findings` section from each subagent.
4. Verify that each finding maps to a real line in the provided files. Drop any
   hallucinated or out-of-scope entries.

### Phase 2: Optional CodeRabbit Cross-Validation

Before consuming the log, check the background CodeRabbit task with `TaskOutput` (or `TaskList`): if it is still running, wait for it to finish (or stop it with `TaskStop` only if it is clearly stuck beyond its timeout). CodeRabbit is advisory only. A capacity-style refusal (e.g. "too many changes") is NOT a reason to stop the review.

If `{{ RABBIT_LOG }}` exists and contains valid review output:

1. Parse JSON lines; ignore empty or malformed entries.
2. Verify each issue against the actual code.
3. Keep confirmed issues; dismiss false positives with a `WHY_DISMISSED` note.
4. Reclassify severity when CodeRabbit over- or under-rates an issue.

If `{{ RABBIT_LOG }}` does not exist, is empty, or contains only a capacity-style
refusal, skip this phase. If it contains an operational error (auth, network,
unknown error), STOP and hand the problem to the user.

### Phase 3: Synthesize

1. Merge the findings from the four specialist subagents with confirmed
   CodeRabbit issues (if any).
2. Deduplicate: one problem = one entry.
3. Sort: `CRITICAL` → `HIGH` → `MEDIUM` → `LOW` → `INFO`; within each level sort
   by file path then line number.

### Phase 4: Machine-Readable Report

Write the report to the path defined in Section 2.1 using the template in
`[ref: #machine-readable-template]`. Fill in all boilerplate fields from
Section 2.3.

### Phase 5: Human-Readable Report

Write the report to the path defined in Section 2.2 using the template in
`[ref: #human-readable-template]`. The report MUST be in **Russian**.

Include:
- Executive summary.
- Findings grouped by severity.
- Dismissed CodeRabbit issues (if any).
- Dedicated sections for Architecture, API Design (AIP), Security, Resilience, Observability, and PII/Data Privacy. Write "<Topic>: clean" if there are no findings.
- A final "Recommendations" section for anything that did not fit the issue
  table but is worth mentioning.

### Phase 6: Persist

After both reports are written, verify and persist per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).

## 6. Language Adaptation

When reviewing a codebase, first run the project's skill discovery and auto-load
any language- or domain-specific skills that are triggered by the files or the
request. Apply those skills' rules to the corresponding parts of the review.

If no dedicated skill is available, map generic review concepts to the idioms
of the target language using general software-engineering principles. Do not
hard-code language names or specific skill names in this skill; rely on skill
discovery to decide which additional skills to load.

Record every loaded skill in the `skills_used` frontmatter tag of the
machine-readable report.

## 7. Architectural Design Review via api-design (MANDATORY)

Every review — `feature` or `project` mode, any programming language — MUST include an architectural design review grounded in the `api-design` skill (Google AIP corpus). This skill's `requires:` frontmatter guarantees api-design is loaded; this section defines how to route it. The pass is never skipped: when the reviewed code exposes no API surface, it concludes "clean" quickly — but the routing steps below are still executed and documented.

1. **Root-agent routing (never delegated).** The ROOT agent MUST read the FULL YAML frontmatter (the complete decision-card index) of EVERY file in `api-design/references/`. Do NOT use the shortlist funnel (Command 1 → shortlist → Command 2 per `frontmatter-protocol` `[ref: #lazy-load-routing]`): a review has no design task to route from, so the whole card index is the routing input. Run Command 2 from `[ref: #lazy-load-routing]` from the api-design skill directory over ALL `references/*.md` at once.

2. **Card selection.** Read every card and semantically match `what`/`use_when`/`avoid_when` against the API surface actually present in the reviewed code (HTTP routes, gRPC services, resource models, field semantics, error model, pagination, versioning, etc.). Deduplicate anchors per api-design §2.2.
3. **Bounded extraction.** Extract each selected anchor with the bounded awk command from api-design §2.3. Never read reference bodies in full.
4. **Hand criteria to the architecture subagent.** Inject the extracted AIP sections into the Architecture & Maintainability subagent's launch prompt as binding review criteria. Routing stays in the main agent; subagents receive already-selected material (api-design §2.2 rule 4). Do NOT modify the subagent prompt files.
5. **Report.** Record design findings in the mandatory "API Design (AIP) Observations" subsection of both reports (see `references/report-templates.md`). Write "API Design (AIP): clean" when the reviewed code exposes no API surface or no violations are found. List `api-design` in the `skills_used` frontmatter tag.

For Python code this pass applies with full force whenever the code exposes an API surface (FastAPI, Flask, gRPC, REST, etc.); the same holds for API code in any other language.

## 8. Lazy-Load Protocol

Do not read the full reference files unless required. Use the routing table below.

| Trigger | Target | Anchor |
|---|---|---|
| Need the full language-agnostic checklist. | `references/checklist.md` | `[ref: #checklist]` |
| Need the security/privacy/configuration subagent prompt. | `references/subagent-security-and-configuration.md` | `[ref: #subagent-security-and-configuration]` |
| Need the correctness/concurrency/performance subagent prompt. | `references/subagent-correctness-concurrency-performance.md` | `[ref: #subagent-correctness-concurrency-performance]` |
| Need the resilience/observability subagent prompt. | `references/subagent-resilience-and-observability.md` | `[ref: #subagent-resilience-and-observability]` |
| Need the architecture/maintainability subagent prompt. | `references/subagent-architecture-and-maintainability.md` | `[ref: #subagent-architecture-and-maintainability]` |
| Need exact machine-readable report template. | `references/report-templates.md` | `[ref: #machine-readable-template]` |
| Need exact human-readable report template. | `references/report-templates.md` | `[ref: #human-readable-template]` |
| Need to adapt concepts to a specific language. | Section 6 above | — |
| Need the mandatory AIP design review procedure. | Section 7 above | — |

## 9. Hard Rules

- NEVER invent issues that do not exist.
- NEVER skip the architectural design review (Section 7) or the full api-design frontmatter read, in any review mode and for any language.
- NEVER delegate api-design card routing to a subagent; subagents receive already-extracted AIP material.
- NEVER omit the "API Design (AIP) Observations" subsection from either report.
- NEVER ignore issues that do exist.
- NEVER skip the boilerplate file names or metadata from Section 2.
- NEVER guess or assume the review mode outside the `main`/`master` → `project`
  default. If the mode is missing on a non-main branch, STOP and demand it.
- NEVER silently swallow CodeRabbit operational failures (auth, network, unknown
  errors). STOP and hand them to the user. Capacity-style refusals (e.g. "too
  many changes") may be ignored.
- NEVER output only the human-readable report without the machine-readable one.
- NEVER let a `CRITICAL` finding lack a clear "why production will break" explanation.
