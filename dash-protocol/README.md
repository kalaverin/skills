# dash-protocol
[ref: #dash-protocol-readme]

Governs every lookup the agent performs through the local Dash documentation layer.

## What it does
[ref: #dash-protocol-readme-purpose]

This skill owns the Dash MCP layer:

- **Installed docset inventory** (`list_installed_docsets`): discover which local docsets exist and what identifiers they use.
- **Documentation search** (`search_documentation`): find symbols, functions, methods, types, guides, and full-text matches across one or more docsets.
- **Full-text search enablement** (`enable_docset_fts`): activate FTS for docsets that support it when index-only results are too shallow.
- **Page loading** (`load_documentation_page`): fetch the full content behind a search result `load_url` and distill the answer.

The protocol sits above the raw tools: it tells the agent when to use Dash, how to pick the right result, and what the fallback chain is when local docs cannot answer.

## When it activates
[ref: #dash-protocol-readme-activation]

Always active.
It applies whenever the user asks about a documented API, language, library, tool, spec, error, or configuration, and whenever the agent's own reasoning identifies a documentation gap that local docsets can close.

## How to run / use it
[ref: #dash-protocol-readme-usage]

1. The agent checks whether the question can be answered from a local Dash docset.
2. If docset identifiers are unknown, it calls `list_installed_docsets` first.
3. It calls `search_documentation` with the right identifiers and query.
4. If results are only index entries or too few, it enables FTS and retries.
5. It selects the best result and calls `load_documentation_page` on the relevant `load_url`.
6. It answers from the loaded page, citing the source docset.
7. If Dash cannot answer, it falls back to `kagi-search`; it never fabricates signatures or behavior from training data.

Example prompts:

- "What does `std::mem::replace` do in Rust?"
- "Show me the Python `pathlib.Path` API for resolving symlinks."
- "Look up the Go `context` package cancellation rules."
- "What does this Git command flag do?"

## What it produces
[ref: #dash-protocol-readme-artifacts]

- Direct, verifiable answers grounded in local documentation.
- Correct source citations including docset name and loaded page.
- Empty-result handling: the agent reports what it searched and why nothing matched, then offers a web-search fallback.

## Dependencies and why they matter
[ref: #dash-protocol-readme-dependencies]

- `frontmatter-protocol`: both `SKILL.md` and `references/dash-tool-examples.md` carry YAML frontmatter; the lazy-load router consumes their `subject`/`index`.
- `markdown-protocol`: the skill files follow the Markdown Headings as a Public API conventions (anchors, one logical line per source line, stable heading identities).
- `kagi-search`: the mandated fallback when Dash returns no useful result.

## Strengths and trade-offs
[ref: #dash-protocol-readme-tradeoffs]

- Strong sides: answers are verifiable against installed docs; works offline; no hallucinated API signatures; fast local search.
- Weak sides / limits: answers are limited to installed docsets; Dash identifiers are opaque strings, not language names; `load_documentation_page` can return very large pages; some docsets do not support FTS.
- Common pitfalls / gotchas: do not guess docset identifiers — list them first; `load_url` anchors identify the symbol but the full page is still returned; `enable_docset_fts` returns `false` for unsupported docsets; result `type` values are docset-specific.

## Repository layout
[ref: #dash-protocol-readme-layout]

```text
dash-protocol/
├── README.md                     # Human overview (this file)
├── SKILL.md                      # Agent entry point: rules, tool inventory, workflow, violation protocol
└── references/
    └── dash-tool-examples.md     # Lazy-load corpus: concrete tool calls and result interpretation
```

## Reference overview
[ref: #dash-protocol-readme-references]

| File | What it covers |
|------|----------------|
| `SKILL.md` | The agent entry point: absolute rule, tool inventory, selection guide, result-choosing criteria, per-tool sections, master workflow, and violation protocol. |
| `references/dash-tool-examples.md` | Eleven lazy-load cards covering live examples for listing docsets, symbol search, multi-docset search, cheatsheet lookup, empty results, FTS enablement, and page loading. Load sections by their `[ref: #dash-ex-*]` anchors. |

## Important conventions / gotchas
[ref: #dash-protocol-readme-gotchas]

- Docset identifiers are opaque strings (for example, `wfenxqwf` for Python); use the `name`/`platform` fields from `list_installed_docsets` for human-readable labels.
- Always prefer Dash for verifiable facts about installed libraries and languages; never invent API signatures or version behavior.
- `enable_docset_fts` is safe to call repeatedly and returns `true` only for FTS-capable docsets.
- `load_documentation_page` returns the whole page even when the `load_url` contains an anchor.
- The fallback chain is fixed: Dash → Kagi web search → never training data.
