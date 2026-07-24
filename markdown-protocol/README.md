# markdown-protocol

Keeps every Markdown file the agent writes machine-addressable, easy to diff, and consistently formatted.

## What it does

This skill owns two layers of Markdown discipline:

- **Authoring rules** (in `SKILL.md`): one logical line per source line, the STRICTEST UTC ISO 8601 date rule, no bare `---` in bodies, marker placement (`marker_style`), YAML quoting style, and term–description list form.
- **The "Markdown Headings as a Public API" standard** (in `references/`): headings as stable, machine-addressable identities — slugs, anchors, unique chains, the rename ban, section size limits, deprecation instead of deletion, and the `errata` conformance repair queue.

The standard applies to ANY agent-authored Markdown: Serena memory files, skill corpora, READMEs, docs, reports, plans, and standards.

## When it activates

No action needed — loaded automatically in every session.

It applies whenever the agent creates or edits any `.md` file, such as `README.md`, `SKILL.md`, reports, decisions, notes, or Serena memory pages. Chat output, code comments, and commit messages are exempt — except the date rule, which always applies.

## How to use it

Just ask the agent to write or edit Markdown content. The agent works from the compressed rule list in `SKILL.md` and lazy-loads rule sections from `references/specification.md` when a rule's application is in doubt, or `references/rationale.md` for the reasoning behind a rule.

Example prompts:

- "Write a README for this service."
- "Update the decision record in `.serena/memories/decisions/`."
- "Create a project audit report."
- "Split this section, it's over the writer limit."

## What it produces

- Markdown files where each logical line is one source line and each heading is a stable addressable identity.
- Documents that index, cite, compact, and reconcile without human intervention.
- Minimal diffs when a single word changes.
- Honest `errata:` queues instead of silently non-conformant files.

## Repository layout

```text
markdown-protocol/
├── SKILL.md                  # Agent entry point: authoring rules + compressed standard rule list
└── references/
    ├── specification.md      # The normative "Markdown Headings as a Public API" standard
    └── rationale.md          # Commentary, rejected alternatives, and evidence per section
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/specification.md` | The full normative standard: slug algorithm, anchor specification, structural and addressing rules, size limits, deprecation, errata mechanism, cross-file citation. Load sections by their `[ref: #mds-*]` anchors. |
| `references/rationale.md` | Per-section commentary: why each rule exists, which alternatives were rejected (and why), the corpus-study evidence appendix, and edition design notes. |

## Important conventions / gotchas

- Heading and anchor identities are stable forever: writers never rename headings or anchors and never delete sections — they deprecate with a dated `DEPRECATED` line.
- Pure-digit-leading heading numbers never enter slugs (they are positional, never identity); digits after the first letter are free (`RFC 2119` → `rfc-2119`).
- Section sizes use the writer limit (8192 bytes) and queue limit (16536 bytes), measured in UTF-8 bytes excluding whitespace and anchor marker lines; the terms "soft limit" and "hard limit" are forbidden.
- Deviations are never silent: they are fixed, or recorded in the document's `errata:` frontmatter list (YAML flow style).
- The standard's own corpus carries the `mds-` anchor prefix per the cross-file citation recommendation.
