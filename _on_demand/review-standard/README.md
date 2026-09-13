# review-standard
[ref: #rs-intro]

Evaluate a code review against the Google eng-practices review standard.

## What it does
[ref: #rs-what]

Answers "was this review done well?" — reviewer bar and thoroughness, comment tone
and clarity, review speed and process, conflict and pushback handling, emergency
exceptions, and author behavior (CL descriptions, CL size, replies to comments).

Assessment, not execution: this skill never performs a review. To have code
reviewed, use the `code-review` skill.

## Corpus
[ref: #rs-corpus]

The sole authority is the archived Google eng-practices review standard
(10 pages, Serena scope `standard/gep/`, pin **2026-09-13**). Full verbatim-detailed
texts live in `references/`, one file per topic, each section ending with the full
source URL. `SKILL.md` carries the full actionable distillate (**The Standard in One Pass**) with `[ref: #anchor]` links into those files — sufficient to assess a review on its own; references deepen any topic in full.

| Reference file | Source pages |
|---|---|
| `references/principles.md` | The Standard of Code Review |
| `references/coverage.md` | What to Look For (12 zones + summary) |
| `references/process.md` | Navigating a CL, Speed of Reviews |
| `references/comments.md` | How to Write Comments |
| `references/conflicts.md` | Handling Pushback, Emergencies |
| `references/author_side.md` | CL Descriptions, Small CLs, Handling Comments |
| `references/sources.md` | URL map, provenance pin, background material |

## Output
[ref: #rs-output]

Every run produces a `## Review Assessment` verdict: scope, standard pin,
overall judgment, findings table with `[ref: #anchor]` citations, deviations with
severity labels taken from the standard itself (Nit / Optional / FYI / blocking),
and grounded recommendations.

## Usage
[ref: #rs-usage]

Ask in chat: «оцени ревью», «стандарт ревью», "evaluate this code review",
"review standard" — or invoke `review-standard` directly with a PR/MR/CL link or
a pasted review thread.
