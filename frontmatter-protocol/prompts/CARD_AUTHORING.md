# Prompt: Author a Reference Card (any topic, any skill)

Use this prompt to produce a **reference card** that conforms to the lazyload standard of `frontmatter-protocol` (`frontmatter-protocol/references/lazyload.md`). This prompt is ONLY the operational skeleton: it says WHICH standard sections to load and in what order to apply them. Every rule about cards, frontmatter, body, and anchors lives in the standard — never restated here. If anything here conflicts with the standard, the standard wins.

**MANDATORY pre-work:** before generating, extract and apply these standard sections (per the canonical loader mechanics, `[ref: #lazy-load-routing]`):

- `[ref: #lazyload-file-layout]` — filename and anchor-prefix conventions.
- `[ref: #lazyload-frontmatter-schema]` — top-level fields and the `subject` firm style.
- `[ref: #lazyload-cards]` — the six card keys and per-field rules.
- `[ref: #lazyload-problem-style]` — the `problem` firm style.
- `[ref: #lazyload-dedup]` — cross-field dedup and convergence.
- `[ref: #lazyload-body-skeleton]` — body structure rules.
- `[ref: #lazyload-anchors]` — marker placement and id format.
- The host skill's addendum (if any) for tier, terminator, title-style, and code-idiom conventions.

Copy everything from `<BEGIN PROMPT>` to `<END PROMPT>` and fill the `{{...}}` inputs.

***

<BEGIN PROMPT>

You are authoring a **reference card** — a lazy-loaded recipe file consumed in two stages: (1) an agent reads only the YAML frontmatter to decide which sections apply, then (2) loads only those `[ref: #<anchor>]` body sections. Your card MUST be routable from the frontmatter alone and MUST contain only HOW in the body. Apply the standard sections listed in the pre-work literally; do not rely on memory of the rules.

## Inputs (fill before generating)

- `{{TOPIC}}` — the subject area of the card (e.g., "Capturing stdout/stderr/logs in tests", "Rate limiting with token buckets").
- `{{FILENAME}}` — `<topic_slug>.md`, lowercase, words separated by underscores.
- `{{ANCHOR_PREFIX}}` — the filename slug with underscores → hyphens, or a shorter semantic prefix used consistently for every anchor.
- `{{TIER_NOTE}}` — optional taxonomy note from the host skill's addendum (e.g. "goes to `references/optional/`"); omit for flat corpora. Tier markers never leak into frontmatter text.
- `{{TERMINATOR_NOTE}}` — optional per-section terminator convention from the host skill's addendum; omit when the skill defines none.
- `{{DOMAIN_IDIOMS}}` — the language/framework conventions for code examples per the host skill's addendum.
- `{{LIBRARIES}}` — optional list of related packages (lowercase; keep significant pins and extras).
- `{{EXTRA_KEYS}}` — optional skill-declared extra top-level keys (e.g. `aips`) with their values; only keys documented in the host skill's `SKILL.md`.

## Output

Produce exactly one Markdown file at the host skill's reference location: frontmatter, then body. No other files. No README, no changelog.

## Part A — Frontmatter (routing index)

Apply the loaded standard sections literally: top-level fields and `subject` per `lazyload-frontmatter-schema`; each card per `lazyload-cards`, `lazyload-problem-style`, and `lazyload-dedup`; convergence by anchor repetition per `lazyload-dedup`.

Template (fill per the loaded rules):

```yaml
---
subject: "<Short essence of {{TOPIC}}; <comma-separated keyword/API cloud of EVERY section area>>"
index:
  - anchor: {{ANCHOR_PREFIX}}-<section-slug>
    what: "<The entity under the anchor, concisely, framed as applied to `problem`.>"
    problem: "<Situation + stake; <naïve path> → <what breaks>; <concept/synonym keyword cloud>>"
    use_when: "<Criterion clause; criterion clause; criterion clause.>"
    avoid_when: "<Criterion clause; criterion clause.>"
    expected: "<Attainability criterion: what holds after applying the section.>"
  - anchor: {{ANCHOR_PREFIX}}-<section-slug>      # MAY repeat a prior anchor (convergence)
    what: "..."
    problem: "..."
    use_when: "..."
    avoid_when: "..."
    expected: "..."
libraries:                                        # optional; omit if none
  - package-name
---
```

## Part B — Body (pure HOW)

Per `lazyload-body-skeleton` and `lazyload-anchors`: exactly one H1 immediately after the frontmatter, optional one-line intro, `##` sections aligned 1:1 with the cards, one marker per routable section in the host skill's placement form, pure HOW content, no cross-section routing/decision tables. Code examples follow `{{DOMAIN_IDIOMS}}`.

## Procedure (follow in order)

1. **Decompose** `{{TOPIC}}` into sections (one rule / recipe / technique / decision each). Each section → one body `##` → one or more cards.
2. **Name** the file (`{{FILENAME}}`), choose `{{ANCHOR_PREFIX}}`, and draft each section's anchor slug per `lazyload-file-layout` and `lazyload-anchors`.
3. **Write the cards first**, fully self-contained per `lazyload-cards` + `lazyload-problem-style` + `lazyload-dedup`. Put every WHEN/WHY/decision here.
4. **Write `subject`** per `lazyload-frontmatter-schema`; add `libraries` and `{{EXTRA_KEYS}}` if any.
5. **Write the body** per `lazyload-body-skeleton`: lead prose → code → labeled contrasts → terminator per `{{TERMINATOR_NOTE}}`.
6. **Verify anchor equality** per `lazyload-anchors`: every card `anchor` has exactly one matching `[ref: #<anchor>]`; every body marker has a declaring card.
7. **Validate** per `lazyload-conformance`: run `uv run --no-project --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py <file>` and fix every failure before finishing.

<END PROMPT>
