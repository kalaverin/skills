---
name: markdown-protocol
description: "MANDATORY skill for Markdown authoring rules and the Markdown Headings as a Public API standard. Always active. Governs how the agent writes and edits any Markdown file: line discipline, date format, frontmatter pairing, markers and anchors, heading identity (slugs, renames, uniqueness), section shape and size, deprecation, and the errata conformance queue. The full normative standard lives in references/specification.md with rationale in references/rationale.md."
triggers:
  always: true
  reason: "Markdown is used for all documentation, skills, and Serena memories; every authored document must be machine-addressable."
version: 0.1.0
---

# SKILL: Markdown Authoring Protocol & Headings-as-API Standard

This skill owns how the agent produces Markdown content. The complete normative standard lives in `references/specification.md` (load rule sections by their `[ref: #mds-*]` anchors per the pointers below); commentary, rejected alternatives, and evidence live in `references/rationale.md`. The compressed list in §4 summarizes the writer-side rules — the specification is authoritative: always read the pointed section when a rule's application is in doubt.

**Skill addendum (lazyload):** paths in this skill are skill-root-relative; the corpus anchor prefix is `mds-` (domain prefix per the cross-file citation recommendation).

## 1. Date and Language (STRICTEST)

[ref: #mds-date-and-language]

**STRICTEST RULE: ALL dates and times MUST use UTC ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ` — NO exceptions, NEVER local time, NEVER omit the `Z` suffix, NEVER any other format. Example: `2026-05-23T11:25:54Z`.**

All document content (bodies, comments, memory entries) is technical English only.

## 2. Application (HARDEST)

[ref: #mds-application]

Every Markdown FILE you write or edit — memory files, skill corpora, READMEs, docs, reports, plans, standards — MUST conform to this skill and to `references/specification.md`. NO exceptions, no partial conformance. Chat output, code comments, and commit messages are exempt EXCEPT the date rule, which always applies.

The only legal outs:

1. Fix the deviation before finishing.
2. Record it in the document's `errata:` list (tracked documents).
3. A waiver recorded in `agent/allowed_violations`.

When in doubt — STOP and ASK the user.

## 3. Authoring Rules

[ref: #mds-authoring-rules]

- **One logical line = one source line (MUST NOT wrap):** never break a single sentence or logical line across source lines (no soft wrapping, no YAML `>` folds for visual narrowing); breaks only between paragraphs, list items, and block structures.
- **No bare `---` (MUST NOT):** a line containing only `---` never appears in a document body outside fenced code blocks; separate sections with headings, use `***` when a break is unavoidable. Never substitute `~~~`.
- **Marker placement (`marker_style`, default `tight`):** a `[ref: #<anchor>]` marker sits at column 0 on its own line directly under the section heading, with one blank line below it; one form per skill, declared when non-default; inline heading markers are legacy and MUST NOT be introduced.
- **YAML quoting (MUST):** double-quoted YAML strings for quoted frontmatter values; nested quotations use single quotes — never escaped double quotes (`\"`).
- **Term–description lists (MUST):** single-line inline colon form `- \`term\`: description`; never split the description onto an indented continuation line.

## 4. Headings-as-API Rule List

[ref: #mds-headings-api-rule-list]

Summary of the writer-side rules of `references/specification.md` (authoritative):

- **Scope:** applies to ANY agent-authored Markdown FILE. → `[ref: #mds-scope-and-conformance-classes]`
- **Conformance model:** repair, never rejection — tooling indexes everything parseable and marks violations via `errata`. → `[ref: #mds-conformance-model]`
- **Slugs:** NFC → lowercase → strip punctuation and symbols (P*/S*, backticks included) → whitespace to dash → collapse → strip edges → strip leading digits until the first letter (`3.5 Parser` → `parser`, `RFC 2119` → `rfc-2119`, `2fa` → `fa`); leading numbers are positional and never identity, so sections differing only in numbers collide as `dup_chain` — name sections meaningfully. Writers Latin-only, tooling Unicode-liberal; uniqueness judged post-slugging. → `[ref: #mds-slug-specification]`
- **Anchors:** `[ref: #<id>]` at column 0 under the heading, one blank line below; kebab-case, unique per document; H1+H2 required, H3+ optional; ids stable forever, never reused (tombstones), never positional. → `[ref: #mds-anchor-specification]`
- **Single H1 (MUST):** exactly one H1 immediately after frontmatter, matching `title` exactly. → `[ref: #mds-single-h1-matching-title]`
- **ATX only (MUST):** `#`–`######` forms only; setext forbidden. → `[ref: #mds-atx-headings-only]`
- **No skipped levels (MUST):** no H1→H3 jumps. → `[ref: #mds-no-skipped-levels]`
- **Depth unlimited (INFO):** H5/H6 legitimate; anchors required only at H1/H2. → `[ref: #mds-depth-unlimited]`
- **Preamble (MUST):** no semantic content before the first H2 — only meta-remarks about the document; flat H1-only documents are legal. → `[ref: #mds-preamble-discipline]`
- **Unique chain (MUST):** slugged heading chain unique per document. → `[ref: #mds-unique-heading-chain]`
- **Cosmetic differences (INFO):** case/punctuation/emphasis differences are not regulated (slugging erases them). → `[ref: #mds-cosmetic-differences-unregulated]`
- **Renames forbidden (MUST NOT):** NEVER rename a heading or the title — new thought = new heading; obsolete heading = DEPRECATION (the only path). Closed exemption list: cosmetic (slug-erased) edits; typo fixes with Damerau–Levenshtein distance ≤ 2 AND ≤ 20% of string length; repository-recorded waivers (`agent/allowed_violations`). Anything else = STOP and ask the user. → `[ref: #mds-heading-renames-forbidden]`
- **Anchors on H1/H2 (MUST).** → `[ref: #mds-anchors-on-h1-h2]`
- **Plain-text headings (MUST):** no bold/italic/links in heading text; code identifiers MUST be backticked; pure-symbol headings forbidden. → `[ref: #mds-plain-text-headings]`
- **One section = one thought (SHOULD):** no minimum size, no merging. → `[ref: #mds-one-section-one-thought]`
- **Writer limit (MUST):** own body above 8192 UTF-8 bytes excluding whitespace → the writer splits into subsections; **queue limit (MUST NOT exceed):** any subtree above 16536 bytes (same count, anchor marker lines excluded) → `errata: over_cap`, indexed whole, never mechanically split. The terms soft/hard limit are forbidden — limits trigger repair, never rejection. → `[ref: #mds-size-limits]`
- **Deprecation (MUST):** never delete or rename — deprecate with `> **DEPRECATED <YYYY-MM-DDTHH:MM:SSZ>:** <reason>. See [ref: #<replacement>]` placed after the anchor marker with one blank line. → `[ref: #mds-deprecation-instead-of-deletion]`
- **Fence-aware parsing (MUST, tooling):** heading-lookalikes inside fences are content. → `[ref: #mds-fence-aware-parsing]`
- **Frontmatter stripping (MUST, tooling):** strip YAML before heading detection; frontmatter is never chunked or hashed. → `[ref: #mds-frontmatter-stripping]`
- **Errata mechanism (MUST):** authors MUST fix violations they author; encountering an unflagged violation → fix it or flag it in `errata:` (silence is non-conformant); already-flagged docs carry no remediation obligation, but your own writing MUST conform. Writers self-report known deviations and remove a reason ONLY after a complete fix of ALL its instances; unknown reasons are never touched; flow style `errata: [a, b]` is required. → `[ref: #mds-the-errata-mechanism]`
- **Cross-file citation (SHOULD):** anchor ids globally unique per domain; name the owner when citing across files; domain prefixes (`entity-`, `ra-`, `fm-`, `serena-`, `mds-`). → `[ref: #mds-cross-file-citation]`

## 5. Pre-Write Checklist (MANDATORY)

[ref: #mds-pre-write-checklist]

Before writing or editing ANY Markdown file, verify:

- [ ] Exactly one H1 matching `title` (where frontmatter is present).
- [ ] ATX headings only; no skipped levels.
- [ ] Anchors on every H1 and H2 heading, correct form and placement.
- [ ] No heading renames (cosmetic edits and the closed exemption list aside).
- [ ] Plain-text headings; code identifiers backticked.
- [ ] Sections within the writer limit (UTF-8 bytes excluding whitespace).
- [ ] Dates in UTC ISO 8601 with `Z`.
- [ ] No bare `---` in the body; no manual line wrapping.

## 6. Reviewer Role (MANDATORY)

[ref: #mds-reviewer-role]

Any agent acting as a Markdown reviewer, rewriter, or validator MUST first load the specification's full frontmatter card index into context and route through it before working. Bounded section extraction uses ONLY the canonical one-liner from `frontmatter-protocol` core §7 (`[ref: #lazy-load-routing]`) — the exact command lives there and is never restated here.

## 7. Scope and Exemptions

[ref: #mds-scope-and-exemptions]

- **Bound:** Markdown FILES — memory files, skill corpora, READMEs, docs, reports, plans, standards.
- **Exempt:** chat output, code comments, commit messages — EXCEPT the date rule, which always applies.
- **Waivers:** permitted deviations live ONLY in the `agent/allowed_violations` Serena memory (format: date, rule being waived, scope, rationale); verify it before assuming a rule applies in full force. A custom anchor id (non-slug form) requires a recorded reason.
- **Repository waivers** never weaken the `errata` recording duty: a permitted deviation is still recorded when it exists.

## 8. Relationship to Other Standards

[ref: #mds-relationship-to-other-standards]

- `frontmatter-protocol` (tracking extension) owns the tracking field set; `errata` is registered there as an optional top-level field activating by presence alone, with semantics pointing to `references/specification.md`.
- `frontmatter-protocol` (lazyload extension) owns `[ref: #…]` marker usage for reference corpora — same notation as this standard's anchors, one mental model.
- Details: `[ref: #mds-relationship-to-other-standards]` in `references/specification.md`.

## 9. Violation Protocol

[ref: #mds-violation-protocol]

If you produce Markdown violating this skill (wrapped lines, bare `---`, renamed headings, markup in headings, missing anchors on H1/H2, lost `errata`, silence about a known deviation), halt immediately, discard the offending output, reload the pointed rule section from `references/specification.md`, and redo correctly. Deviations you cannot fix now MUST be recorded in the document's `errata:` list; deviations you are unsure about MUST be asked about — record permitted ones in `agent/allowed_violations` per its protocol.
