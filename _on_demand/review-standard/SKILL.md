---
name: review-standard
description: "Evaluate an ongoing or completed code review against the Google eng-practices code review standard: reviewer comments, speed, tone, coverage, conflict handling, emergency exceptions. Authoritative corpus: the archived gep standard. Use when assessing review quality, not when performing a review."
triggers:
  request: review-standard, review standard, стандарт ревью, оцени ревью, оценка код-ревью, оцени код-ревью, качество ревью, насколько хорошо ревью, google review standard, google eng-practices review, оцени ревьюера, ревьюер прав/неправ, разбор ревью, review assessment/evaluation, evaluate code review
  reason: Review evaluation must be grounded in the archived Google eng-practices standard, not in training-data notions of good review.
runtime: true
requires:
  - frontmatter-protocol
  - read-for-comments
version: 0.2.0
---

# Review Standard

## Mission & Authority

[ref: #mission-authority]

This skill **evaluates** code reviews against the Google eng-practices review standard. It answers questions like "was this review done well?", "is the reviewer right?", "did the author handle comments correctly?". It never performs a review itself — execution requests redirect to the `code-review` skill.

Authority order, highest first:

1. The archived `gep` corpus (Serena scope `standard/gep/`, pin 2026-09-13) — the sole source of verdicts. See [ref: #sources-corpus-map] and [ref: #sources-provenance-pin] in `references/sources.md`.
2. This SKILL.md — the full actionable distillate (§ The Standard in One Pass) plus workflow and verdict format.
3. Background material (Google styleguide, SWE book ch.3) — context only, never overrides the corpus. External documents (e.g. Chromium cr_respect) are non-authoritative. See [ref: #sources-background].

Before any web fetch, the `read-for-comments` Lookup Gate applies: the archive is the corpus; the live site is consulted only for re-verification.

## The Standard in One Pass

[ref: #standard-distillate]

Every rule of the corpus, compressed to one actionable line each. This section is sufficient to assess a review; open the anchored section only when a verdict needs the exact letter of the standard.

### Principles — the bar (`references/principles.md`)

- **Senior principle:** approve a CL once it definitely improves overall code health, even if imperfect; there is no "perfect" code, only better code — seek continuous improvement, never delay an improvement over polish [ref: #principles-core-standard].
- Non-critical suggestions and purely educational comments are welcome but MUST be prefixed `Nit:` (or otherwise marked non-mandatory) [ref: #principles-core-standard] [ref: #principles-mentoring].
- Nothing justifies checking in code that worsens code health — except a qualified emergency [ref: #principles-core-standard] [ref: #conflicts-emergency-definition].
- **Dispute hierarchy:** technical facts and data overrule opinions → style guide is absolute on style → design is weighed on engineering principles (author's preference wins among demonstrably equal options) → consistency with the existing codebase [ref: #principles-technical-facts].
- **Conflict ladder:** consensus from the documents → face-to-face/video (record results as a CL comment) → escalate to team, Technical Lead, maintainer, or Eng Manager; never let a CL sit blocked [ref: #principles-resolving-conflicts].

### Coverage — what must be checked (`references/coverage.md`)

- **Design** first: interactions make sense, the change belongs in this codebase, integrates with the system, now is the right time [ref: #coverage-design].
- **Functionality:** does what the developer intended and is good for users; think edge cases and concurrency; UI changes validated by demo or patching [ref: #coverage-functionality].
- **Complexity:** no more than needed at line/function/class level; call out over-engineering for speculative future needs [ref: #coverage-complexity].
- **Tests:** appropriate unit/integration/e2e tests in the same CL, verified correct, sensible, useful, and maintainable by a human [ref: #coverage-tests].
- **Naming:** long enough to fully communicate, short enough to stay readable [ref: #coverage-naming].
- **Code comments:** explain why, not what; unclear code is simplified instead of commented; pre-existing TODOs reconsidered [ref: #coverage-comments].
- **Style:** the style guide is the authority; anything outside it is `Nit:` and never blocks; reformatting never mixes with functional change [ref: #coverage-style].
- **Consistency:** guide requirements win over existing code; recommendations are judgment calls biased toward the guide; otherwise match the codebase — and file a bug + TODO for cleanup [ref: #coverage-consistency].
- **Documentation:** build/test/usage/release changes update docs; deleted or deprecated code deletes docs; missing docs are requested [ref: #coverage-documentation].
- **Every line:** read everything assigned, no skimming human-written code; scope splits declared in a comment; unreadable code goes back for clarification [ref: #coverage-every-line].
- **Context:** whole file and whole system, not the diff hunk; never accept code-health degradation, even in small increments [ref: #coverage-context].
- **Good things:** praise what was done well — encouragement mentors better than criticism [ref: #coverage-good-things].
- Completeness check against the standard's own closing checklist [ref: #coverage-summary].

### Process — navigation and speed (`references/process.md`)

- **Pass structure:** sense-check the change's existence → main parts first, major design comments immediately → the rest in sequence, missing nothing [ref: #process-summary] [ref: #process-broad-view] [ref: #process-main-parts] [ref: #process-sequence].
- **Speed rationale:** team velocity outranks individual velocity; slow reviews breed process complaints and degrade code health [ref: #process-why-fast].
- **Latency ceiling:** review shortly after arrival; one business day maximum per response; multiple rounds should fit a single day [ref: #process-how-fast].
- **Interruption exception:** never break a focused task for review — answer at the next break point [ref: #process-interruption].
- **Response priority:** per-response speed matters more than total duration; when busy, send a quick ack with timing, alternative reviewers, or broad comments [ref: #process-fast-responses].
- **Time zones:** answer while the author can still respond that working day, or finish before their next morning [ref: #process-time-zones].
- **LGTM with comments:** approve with open comments when the author will address them, they are optional, or they are minor — and specify which case applies [ref: #process-lgtm-with-comments].
- **Large CLs:** ask for a split into smaller dependent CLs; if impossible, give design comments and return — always unblock quickly without sacrificing health [ref: #process-large-cls].
- **Trajectory:** strict fast reviews accelerate over time; never trade standards or quality for imagined velocity [ref: #process-improvements].

### Comments — how reviewer remarks are written (`references/comments.md`)

- Headline duties: be kind, explain reasoning, balance explicit direction with author autonomy, push simplification over explanation [ref: #comments-summary].
- **Courtesy:** comment on the code, never on the developer — mandatory for anything potentially upsetting or contentious [ref: #comments-courtesy].
- **Explain why:** non-trivial remarks carry intent, the best practice followed, or the code-health improvement [ref: #comments-explain-why].
- **Guidance balance:** fixing the CL is the author's responsibility, not the reviewer's; balance pointing out problems against direct instructions; praise what is done well [ref: #comments-guidance].
- **Severity labels:** `Nit:` / `Optional` (`Consider`) / `FYI:` — so authors prioritize and don't read every remark as mandatory [ref: #comments-severity].
- **Accepting explanations:** unclear code is answered by rewriting the code (occasionally a code comment); explanations living only in the review tool are lost to future readers [ref: #comments-accepting-explanations].

### Conflicts and emergencies (`references/conflicts.md`)

- **Who is right:** consider the developer right first (they are closer to the code); if the suggestion improves code health, keep advocating politely in explanations that show the reply was heard [ref: #conflicts-who-is-right].
- **Upsetting:** polite insistence rarely upsets anyone; friction comes from how comments are written, not from insisting on quality [ref: #conflicts-upsetting].
- **Cleanup later:** refuse it — deferred cleanups almost never happen; new complexity is cleaned before submission; exposed surrounding problems get a bug filed and assigned to the author (optional TODO) [ref: #conflicts-cleanup-later].
- **Strictness complaints:** loud but temporary when moving from lax to strict; faster reviews dissolve them [ref: #conflicts-strictness-complaints].
- **Emergency:** a small CL that unblocks a major launch, fixes a production bug significantly affecting users, handles a pressing legal issue, or closes a major security hole; only speed and correctness matter, top priority, thorough re-review afterwards [ref: #conflicts-emergency-definition].
- **Not emergencies:** launch-this-week preference, long feature work, reviewer timezones, Friday evening, manager's soft deadline, rollback of test-failing CLs [ref: #conflicts-non-emergency].
- **Hard deadline:** only when missing it is disastrous (contractual obligation, marketplace failure, annual hardware window); soft deadlines never justify sacrificing code health [ref: #conflicts-hard-deadline].

### Author side (`references/author_side.md`)

- **Description first line:** short imperative complete sentence that stands alone in version-control history, blank line after [ref: #author-side-first-line].
- **Description body:** the problem, why this approach, shortcomings, bug numbers, benchmark results, design-doc links with enough inline context [ref: #author-side-body].
- **Description examples:** bad one-liners vs good functionality/refactoring/contextual descriptions; tags limited in the first line; generated CLs follow the same rules; re-check the description before submitting [ref: #author-side-description-examples].
- **Why small:** faster and more thorough review, fewer bugs, less wasted work, easier merge/design/rollback; the reviewer may reject outright for size alone [ref: #author-side-why-small].
- **What is small:** one self-contained change with related tests, understandable, system keeps working; ~100 lines fine, ~1000 too large [ref: #author-side-what-small].
- **Large CL exceptions:** whole-file deletions; output of trusted auto-refactoring tools [ref: #author-side-large-okay].
- **Splitting:** stack dependent CLs; split by files, horizontally by layers, vertically by features, or as a grid of standalone CLs [ref: #author-side-splitting].
- **Hygiene:** refactorings go in separate CLs from features/fixes; related tests live in the same CL; stacked CLs never break the build [ref: #author-side-refactor-tests-build].
- **Not personal:** critique targets the code; never respond in anger — walk away, then reply politely [ref: #author-side-not-personal].
- **Fix the code:** comprehension questions are answered by clarifying the code, not by thread explanations [ref: #author-side-fix-code].
- **Collaborate:** disagree with weighed pros/cons and tradeoffs, not flat refusal; consensus comes from technical facts [ref: #author-side-collaborate].

### Sources and provenance (`references/sources.md`)

- Ten canonical pages mapped to the six content files; archived attested copies under Serena scope `standard/gep/` [ref: #sources-corpus-map].
- Pin: scraped and attested **2026-09-13**; every verdict names this pin [ref: #sources-provenance-pin].
- Background: Google styleguide + SWE book ch.3 (context only); Chromium `cr_respect.md` is external and non-authoritative [ref: #sources-background].

## Corpus & Routing Index

[ref: #corpus-routing]

The distillate above is sufficient for assessment; the reference files hold the full verbatim-detailed texts (each section ending with `Sources:` full URLs) for deepening a topic or quoting the exact letter of the standard.

| Question about the review | Reference file | Key anchors |
|---|---|---|
| Is the reviewer applying the right bar? (quality, no perfection, progress) | `references/principles.md` | [ref: #principles-core-standard], [ref: #principles-mentoring] |
| Did the reviewer check everything? (design, functionality, tests, naming, docs…) | `references/coverage.md` | 12 coverage zones, [ref: #coverage-functionality], [ref: #coverage-tests] |
| Was the review process right? (navigation, speed, response time) | `references/process.md` | [ref: #process-why-fast], [ref: #process-fast-responses] |
| Are comments well-written? (tone, courtesy, clarity, nits) | `references/comments.md` | [ref: #comments-courtesy], [ref: #comments-guidance] |
| Conflict, pushback, emergency claims | `references/conflicts.md` | [ref: #conflicts-who-is-right], [ref: #conflicts-emergency-definition] |
| Author behavior (description, CL size, replies to comments) | `references/author_side.md` | [ref: #author-side-what-small], [ref: #author-side-fix-code] |
| Where does a rule come from? Provenance, freshness | `references/sources.md` | [ref: #sources-corpus-map], [ref: #sources-provenance-pin] |

## Evaluation Workflow

[ref: #evaluation-workflow]

Input: a review artifact — PR/MR/CL link or pasted thread, plus the user's question.

1. **CLASSIFY.** Determine what is being assessed: reviewer behavior, author behavior, process (speed/coverage), a specific conflict, or the whole review. If the user actually wants a review *performed*, stop and redirect to `code-review`.
2. **ROUTE.** Assess from The Standard in One Pass; load only the reference sections whose anchors the verdict will cite (table above). Every claim about the standard must resolve to a `[ref: #anchor]` in a reference file.
3. **ASSESS.** Compare observed behavior against the distillate and, where contested, the verbatim text. Quote the standard where a verdict hinges on it. If the standard is silent on the point, say so explicitly — never invent rules.
4. **REPORT.** Emit the Verdict Format below.

Hard rules:

- **Corpus only.** Verdicts come from the archived gep text, not from training-data notions of good review.
- **Silent standard → say so.** "The standard does not address X" is a valid finding.
- **Quote on dispute.** Any contested verdict includes the verbatim quote it rests on.
- **No execution.** Never review the code itself; assess the review.

## Verdict Format

[ref: #verdict-format]

```markdown
## Review Assessment

**Scope:** <what was assessed — reviewer / author / process / conflict>
**Standard pin:** gep @ 2026-09-13

**Verdict:** <1–3 sentences, overall judgment>

### Findings

| # | Aspect | Standard says | Observed | Verdict |
|---|--------|---------------|----------|---------|
| 1 | <aspect> | <rule> [ref: #anchor] | <what happened> | OK / VIOLATION / N/A |

### Deviations

- <rule violated> — "<quote from standard>" — severity: Nit / Optional / FYI / **blocking**

### Recommendations

- <actionable fix per deviation, grounded in the standard>
```

Severity labels come from the standard's own vocabulary: `Nit:` for nits ([ref: #comments-severity]), optional/preference for non-mandatory guidance, FYI for informational comments, **blocking** where the standard demands refusal or fix-before-approval.

## Violation Protocol

[ref: #violation-protocol]

- If asked to **perform** a review → halt, redirect to `code-review`.
- If asked to judge something the corpus does not cover → state the gap, do not extrapolate.
- If the corpus pin is questioned or upstream drift is suspected → propose re-verification via `read-for-comments` archival pipeline; do not silently fetch and mix versions.
- If a reference file and the archive card disagree → the archive card wins; report the drift.
