---
name: markdown-protocol
description: MANDATORY skill for Markdown authoring rules. Always active. Governs how the agent writes and edits Markdown files, including Serena memory entries, skill documents, and README files.
triggers:
  always: true
  reason: "Markdown is used for all documentation, skills, and Serena memories."
---

# SKILL: Markdown Authoring Protocol

**STRICTEST RULE: ALL dates and times MUST use UTC ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ` — NO exceptions, NEVER local time, NEVER omit the `Z` suffix, NEVER any other format. Example: `2026-05-23T11:25:54Z`.**

This skill owns how the agent produces Markdown content. It applies to every `.md` file the agent creates or edits, including but not limited to:

- `SKILL.md` files and their YAML frontmatter.
- `README.md` files.
- Serena memory entries under `.serena/memories/` and at serena MCP calls.
- Reports, proposals, decisions, and notes.

## 1. No Manual Line Wrapping Inside a Line (HARD RULE)

When a sentence, phrase, or logical line is conceptually a single line of text, you MUST write it as a single continuous line. Do NOT insert manual line breaks (soft wrapping) in the source Markdown to make the file look narrower.

### 1.1 What is forbidden

Breaking a single sentence or clause across source lines like this:

```markdown
---
description: >
  Canonical skill discovery and auto-loading protocol. Always active. Governs how
  the agent discovers skill directories, parses SKILL.md frontmatter, evaluates
  triggers, resolves transitive dependencies via `requires:`, and lazily loads
  reference sections. This skill is the loader for all other skills.
---

- Inside code blocks, tables, and other block-level structures where newlines
are semantically required.
- Between distinct sentences when you intentionally want one sentence per source
line for diff readability (optional, but never inside a sentence).
```

Although YAML `>` folds newlines into spaces, the source still contains manual breaks inside what is logically one string. This is forbidden.

### 1.2 Correct form

Write the same content as one continuous source line:

```markdown
---
description: "Canonical skill discovery and auto-loading protocol. Always active. Governs how the agent discovers skill directories, parses SKILL.md frontmatter, evaluates triggers, resolves transitive dependencies via `requires:`, and lazily loads reference sections. This skill is the loader for all other skills."
---
```

### 1.3 When line breaks are allowed

- Between paragraphs.
- Between list items.
- Inside code blocks, tables, and other block-level structures where newlines are semantically required.
- Between distinct sentences when you intentionally want one sentence per source line for diff readability (optional, but never inside a sentence).

### 1.4 Applies to Serena memory too

Serena memory files are Markdown. The same rule applies to their YAML frontmatter and body: do not wrap a single sentence across multiple source lines.

## 2. Rationale

- **Consistent rendering:** Manual wrapping behaves differently across Markdown parsers and YAML folded-block implementations.
- **Clean diffs:** Adding or removing a word in a wrapped paragraph reshuffles many lines; a single-line paragraph produces a minimal diff.
- **Predictability:** One logical line = one source line. There is no ambiguity about whether a newline is a paragraph break or just wrapping.

## 3. No Bare `---` Thematic Breaks (HARD RULE)

A line containing only `---` (a Markdown thematic break / horizontal rule) MUST NOT appear in a document body outside fenced code blocks. Separate sections with headings; if a visual break is truly unavoidable, use `***` instead.

### 3.1 Rationale

Documents in this ecosystem carry YAML frontmatter delimited by `---` lines and are machine-parsed: frontmatter extraction tooling keys on anchored delimiter lines (`^---[ \t]*$` in awk), so a bare body `---` is indistinguishable from a delimiter and falsifies splitter assumptions. Inside fenced code blocks `---` is content, not markup, and remains allowed.

## 5. Anchor Marker Placement (`marker_style`)

For `[ref: #<anchor>]` lazy-load markers (mechanics: `frontmatter-protocol` lazyload extension), two placement forms exist:

- **`tight` (DEFAULT):** the marker sits at column 0 on its own line directly under the section heading, with one blank line below it.
- **`separate`:** the marker additionally has a blank line above it (blank lines on both sides).

A skill MUST choose **one** form and apply it uniformly across its corpus; a non-default choice is declared in that skill's addendum. Extraction tooling MUST NOT depend on a blank line above the marker. Inline heading markers (`## Heading [ref: #x]`) are a legacy form and MUST NOT be introduced.

## 6. Title and H1

Every frontmatter-carrying document has exactly **one** H1, placed immediately after the frontmatter block. When the frontmatter carries a `title` field (e.g. Serena memories), the H1 text MUST match `title` exactly.

## 7. Hard Rules

- **NEVER** wrap a single sentence or logical line across multiple source lines.
- **NEVER** use YAML `>` folded blocks just to split a long string over several lines for visual narrowing.
- **NEVER** place a bare `---` thematic break in a document body outside fenced code blocks; use headings, or `***` when a break is unavoidable.
- **ALWAYS** write term–description list items in the single-line inline colon form `- `term`: description`; **NEVER** split the description onto an indented continuation line (the HTML-style description-list form).
- **ALWAYS** prefer a single continuous source line unless a line break carries real structural meaning (new paragraph, list item, code block, etc.).
- **ALWAYS** place `[ref: #anchor]` markers per `marker_style` (default `tight`: own line directly under the heading, one blank line below); **NEVER** mix forms in one skill or introduce inline heading markers.
- **ALWAYS** keep exactly one H1 immediately after the frontmatter, matching the `title` field when one exists.
- **ALWAYS** use YAML double-quoted style for quoted frontmatter values; **NEVER** place escaped double quotes (`\"`) inside them — nested quotations use single quotes.

## 8. Quoting Inside YAML Frontmatter Strings (HARD RULE)

When a frontmatter value must be quoted (it contains `: `, starts with an indicator character, or the owning standard requires quoted style), you MUST use YAML double-quoted style. Inside a double-quoted YAML string, every nested quotation MUST be written with single quotes — NEVER as escaped double quotes (`\"`). Escaped quotes are visual noise, rot quickly under editing, and signal that the author did not control the quoting style.

Forbidden:

```yaml
description: "... the user asks for: business rules, \"domain events\", ..."
```

Correct:

```yaml
description: "... the user asks for: business rules, 'domain events', ..."
```

Corollary: when authoring prose destined for a double-quoted YAML string, write inner quotations as single quotes from the start. Do not write `"..."` and escape it afterwards.
