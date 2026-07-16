# markdown-protocol

Keeps every Markdown file the agent writes easy to diff and consistently formatted.

## What it does

This skill defines how the agent authors Markdown.
It requires one logical sentence or clause per source line and forbids manual wrapping just to make a file look narrower.
The same rule applies to YAML frontmatter and Markdown bodies, including Serena memory entries.

## When it activates

No action needed — loaded automatically in every session.

It applies whenever the agent creates or edits any `.md` file, such as `README.md`, `SKILL.md`, reports, decisions, notes, or Serena memory pages.

## How to use it

Just ask the agent to write or edit Markdown content.
It will keep each sentence on its own source line and avoid YAML `>` folded blocks that hide line breaks inside a long string.

Example prompts:

- "Write a README for this service."
- "Update the decision record in `.serena/memories/decisions/`."
- "Create a project audit report."

## What it produces

- Markdown files where each logical line is one source line.
- Minimal diffs when a single word changes.
- YAML frontmatter without folded blocks used for visual narrowing.

## Repository layout

```text
markdown-protocol/
└── SKILL.md              # Agent entry point: authoring rules and rationale
```

## Reference overview

This skill has no reference files; all rules live in `SKILL.md`.

## Important conventions / gotchas

- Line breaks are allowed between paragraphs, between list items, inside code blocks and tables, and optionally between distinct sentences for diff readability.
- The rule applies to Serena memory YAML frontmatter and body content too.
- It governs Markdown style, not the correctness of non-Markdown content.
