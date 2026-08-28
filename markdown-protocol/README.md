# markdown-protocol
[ref: #markdown-protocol]

Keeps every Markdown file the agent writes machine-addressable, easy to diff, and consistently formatted.

## What it does
[ref: #markdown-protocol-purpose]

This skill owns two layers of Markdown discipline:

- **Authoring rules** (in `SKILL.md`): one logical line per source line, the strict UTC ISO 8601 date rule, no bare `---` in bodies, `[ref: #<anchor>]` marker placement, YAML quoting style, and term–description list form.
- **The "Markdown Headings as a Public API" standard** (in `references/`): stable, machine-addressable heading identities — slugs, anchors, unique chains, the rename ban, section size limits, deprecation instead of deletion, and the `errata` conformance repair queue.

The standard applies to any agent-authored Markdown file: Serena memory files, skill corpora, READMEs, docs, reports, plans, and standards.

## When it activates
[ref: #markdown-protocol-activation]

Always active.
It applies whenever the agent creates or edits any `.md` file, such as `README.md`, `SKILL.md`, reports, decisions, notes, or Serena memory pages.
Chat output, code comments, and commit messages are exempt — except the date rule, which always applies.

## How to run / use it
[ref: #markdown-protocol-usage]

1. Ask the agent to write or edit Markdown content.
2. The agent consults the compressed rule list in `SKILL.md` and lazy-loads rule sections from `references/specification.md` when a rule's application is in doubt.
3. For reasoning behind a rule, consult `references/rationale.md`.
4. If a file cannot be made fully conformant, record the deviation in its `errata:` frontmatter list instead of staying silent.

Example prompts:

- "Write a README for this service."
- "Update the decision record in `.serena/memories/decisions/`."
- "Create a project audit report."
- "Split this section, it is over the writer limit."

## What it produces
[ref: #markdown-protocol-artifacts]

- Markdown files where each logical line is one source line and each heading is a stable addressable identity.
- Documents that index, cite, compact, and reconcile without human intervention.
- Minimal diffs when a single word changes.
- Honest `errata:` queues instead of silently non-conformant files.

## Dependencies and why they matter
[ref: #markdown-protocol-dependencies]

- None declared in the skill header.
- The skill is consumed automatically because it is `always: true`. It works alongside `frontmatter-protocol` (YAML envelope rules for frontmatter-carrying files) and `read-for-comments` (RFC 2119 normative keywords used in standards prose).

## Strengths and trade-offs
[ref: #markdown-protocol-tradeoffs]

- Strong sides: headings become durable API endpoints for citations; one-line-per-logical-line minimizes diff noise; the `errata` queue keeps non-conformance visible rather than hidden.
- Weak sides / limits: strict rules can feel heavy for one-off notes; every H1 and H2 must carry an anchor marker; the writer limit (8192 bytes) and queue limit (16536 bytes) require section splitting.
- Common pitfalls / gotchas: headings and anchor IDs are not renamed or reused — obsolete ones are deprecated instead; leading numbers are positional and do not enter slugs; bare `---` lines are not used in the body (use `***` for unavoidable breaks); dates use UTC ISO 8601 with a `Z` suffix.

## Repository layout
[ref: #markdown-protocol-layout]

```text
markdown-protocol/
├── README.md                  # Human overview (this file)
├── SKILL.md                   # Agent entry point: authoring rules + compressed standard rule list
└── references/
    ├── specification.md       # The normative "Markdown Headings as a Public API" standard
    └── rationale.md           # Commentary, rejected alternatives, and evidence per section
```

## Reference overview
[ref: #markdown-protocol-references]

| File | What it covers |
|------|----------------|
| `references/specification.md` | The full normative standard: slug algorithm, anchor specification, structural and addressing rules, size limits, deprecation, errata mechanism, and cross-file citation. Load sections by their `[ref: #mds-*]` anchors. |
| `references/rationale.md` | Per-section commentary: why each rule exists, which alternatives were rejected and why, the corpus-study evidence appendix, and edition design notes. |

## Important conventions / gotchas
[ref: #markdown-protocol-gotchas]

- Heading and anchor identities are stable: headings and anchors are not renamed or deleted — obsolete ones are deprecated with a dated `DEPRECATED` line.
- Pure-digit-leading heading numbers never enter slugs (they are positional, never identity); digits after the first letter are free (`RFC 2119` → `rfc-2119`).
- Section sizes use the writer limit (8192 bytes) and queue limit (16536 bytes), measured in UTF-8 bytes excluding whitespace and anchor marker lines; the terms "soft limit" and "hard limit" are not used.
- Deviations are fixed or recorded in the document's `errata:` frontmatter list in YAML flow style.
- The standard's own corpus carries the `mds-` anchor prefix per the cross-file citation recommendation.
