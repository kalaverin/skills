[ref: #report-templates]

# Report Templates

These templates are mandatory. Use the exact file names defined in
`SKILL.md` Section 2.1.

[ref: #machine-readable-template]

## Machine-Readable Template

Target path follows `SKILL.md` Section 2.1: use the `<entity>/` sub-directory
only when the target entity is known; otherwise write directly under
`.serena/memories/review/`.

This report is stored as a Serena memory entry and MUST begin with the Serena
metadata frontmatter. The `reviewer` and `scope` tags are additional optional
fields placed after the mandatory fields. The `skills_used` tag records which
skills the agent loaded while producing the report.

```markdown
---
title: Code Review Report
created_at: <YYYY-MM-DDTHH:MM:SSZ>
updated_at: <YYYY-MM-DDTHH:MM:SSZ>
repo: project
branch: <current git branch>
commit: <7-char short hash>
committed_at: <YYYY-MM-DDTHH:MM:SSZ>
source: <project-relative path or directory>
reviewer: Kimi + optional CodeRabbit cross-validation
scope: <Diff-based review `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`> OR <Full project review (not diff-based)>
skills_used:
  - code-review
  - <language-specific skill if any>
  - <domain-specific skill if any>
  - serena-protocol
---

# Code Review Report

## Executive Summary

[2-3 sentences: what is being reviewed and overall risk level.]

## Critical Issues [BLOCKING]

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | `path/to/file.ext:12-15` | CRITICAL | [one-line summary] | [concrete fix] |

## High Priority [SHOULD FIX]

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | `path/to/file.ext:22` | HIGH | [one-line summary] | [concrete fix] |

## Medium Priority [COULD FIX]

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | `path/to/file.ext:31` | MEDIUM | [one-line summary] | [concrete fix] |

## Low Priority / INFO [NICE TO HAVE]

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | `path/to/file.ext:40` | LOW / INFO | [one-line summary] | [optional fix or note] |

## Dismissed CodeRabbit Issues [FALSE POSITIVES]

- **[Severity from CodeRabbit]** `file.ext:line` — [summary] — **WHY_DISMISSED:** [reason]

## Architecture Observations

[Problems at the architectural level: coupling, cohesion, boundary violations,
or "Architecture: clean" if there are none.]

## Security Notes

[Security findings or "Security: clean".]

## Resilience & Fault Tolerance Notes

[Resilience findings or "Resilience: clean".]

## Observability & Logging Notes

[Observability findings or "Observability: clean".]

## PII & Data Privacy Notes

[Privacy findings or "PII: clean".]
```

[ref: #human-readable-template]

## Human-Readable Template

Target: `.reports/review-YYYY-mmdd-HHMM-feature.md` or
`.reports/review-YYYY-mmdd-HHMM-project.md`.

The report MUST be written in **Russian**.

```markdown
# Code Review Report

**Branch:** `{{ CURRENT_BRANCH }}`
**Commit:** `<git rev-parse HEAD>`
**Reviewer:** Kimi + optional CodeRabbit cross-validation
**Date:** `<YYYY-MM-DDTHH:MM:SSZ>`
**Scope:** <Diff-based review `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`> OR <Full project review (not diff-based)>

## Executive Summary

[2-3 sentences in Russian describing the scope and overall risk.]

## [CRITICAL] <Title>

Created: `<YYYY-MM-DDTHH:MM:SSZ>`
File: `path/to/file.ext:line-range`
Next step: [concrete next action]

Context:
  [Background needed to understand the issue.]

Summary: |
  [Detailed explanation of the problem, impact, and attack scenario if applicable.]

Notes: |
  [Additional context, expected behavior, and how to reproduce if relevant.]

---

## [HIGH] <Title>

[Same structure as CRITICAL.]

---

## [MEDIUM] <Title>

[Same structure as CRITICAL, may be shorter.]

---

## [LOW] / [INFO] <Title>

[Same structure, optional fix.]

---

## Dismissed CodeRabbit Issues

- **[Severity]** `file.ext:line` — [summary] — **WHY_DISMISSED:** [reason]

## Architecture Observations

[Architectural findings or "Architecture: clean".]

## Security Notes

[Security findings or "Security: clean".]

## Resilience & Fault Tolerance Notes

[Resilience findings or "Resilience: clean".]

## Observability & Logging Notes

[Observability findings or "Observability: clean".]

## PII & Data Privacy Notes

[Privacy findings or "PII: clean".]

## Recommendations

[General recommendations, style advice, refactoring ideas, test improvements,
performance optimizations, or any other thoughts that did not fit the issue
list but can help developers improve the project.]

---

**Methodology:** Independent review + optional CodeRabbit cross-validation,
severity reclassified based on project context.
```
