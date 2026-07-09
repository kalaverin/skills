---
name: markdown-protocol
description: MANDATORY skill for Markdown authoring rules. Always active. Governs how the agent writes and edits Markdown files, including Serena memory entries, skill documents, and README files.
triggers:
  always: true
  reason: "Markdown is used for all documentation, skills, and Serena memories."
---

# SKILL: Markdown Authoring Protocol

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
description: Canonical skill discovery and auto-loading protocol. Always active. Governs how the agent discovers skill directories, parses SKILL.md frontmatter, evaluates triggers, resolves transitive dependencies via `requires:`, and lazily loads reference sections. This skill is the loader for all other skills.
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

## 3. Hard Rules

- **NEVER** wrap a single sentence or logical line across multiple source lines.
- **NEVER** use YAML `>` folded blocks just to split a long string over several lines for visual narrowing.
- **ALWAYS** prefer a single continuous source line unless a line break carries real structural meaning (new paragraph, list item, code block, etc.).
