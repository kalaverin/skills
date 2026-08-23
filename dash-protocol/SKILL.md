---
name: dash-protocol
description: "Mandatory protocol for the Dash MCP documentation layer. Governs installed docset enumeration, documentation search, full-text search enablement, and page loading through local Dash docsets."
triggers:
  always: true
  reason: "The agent must be able to reach for local Dash docsets both when the user asks for documentation/man/spec and when the agent's own reasoning identifies a documentation gap."
requires:
  - frontmatter-protocol
  - markdown-protocol
version: 0.1.0
---

# SKILL: Dash Documentation Protocol
[ref: #dash-protocol]

This skill governs every use of the Dash MCP tools.
When this skill is active, you MUST use Dash MCP tools for any local documentation lookup, API reference query, or docset search.
No other local documentation mechanism is permitted.

## Absolute Rule
[ref: #dash-absolute-rule]

Whenever the current task requires information that is available in local Dash docsets, you MUST use a Dash MCP tool to obtain it.
You MUST NOT guess, assume, or hallucinate API signatures, behavior, or version details that can be verified against a local docset.
When the relevant docset is not installed or Dash search returns no useful result, fall back to `kagi-search` before using training data.

## When to Use Dash
[ref: #dash-when-to-use]

Use Dash whenever a question can be answered from locally installed documentation, including:

- The user asks to read, search, or check documentation: `look it up in the docs`, `check the man page`, `read the spec`, `search the documentation`.
- Russian user phrases: `почитай в документации`, `поищи в доке`, `посмотри в мане`, `посмотри в мануале`, `глянь в спеке`, `глянь в спецификации`.
- The agent's own reasoning surfaces a need for an API signature, behavior, version detail, or code example that may exist in a local docset.

## MCP Group Declaration
[ref: #dash-mcp-declaration]

This task requires the `dash` MCP skill group.
All local documentation lookup, docset enumeration, search, and page loading MUST go through the tools listed below.

## Tool Inventory
[ref: #dash-tool-inventory]

| Tool | Purpose |
|---|---|
| `list_installed_docsets` | List all documentation sets installed in Dash. |
| `search_documentation` | Search across selected docsets by query. |
| `enable_docset_fts` | Enable full-text search for a specific docset. |
| `load_documentation_page` | Load the full content of a documentation page by its `load_url`. |

## Tool Selection Guide
[ref: #dash-tool-selection]

| Situation | Tool |
|---|---|
| You need to know which docsets are available. | `list_installed_docsets` |
| You need to find a symbol, function, class, or topic. | `search_documentation` |
| Broad search in a docset returns only index entries or too few matches. | `enable_docset_fts` |
| You have a `load_url` from search results and need the full page. | `load_documentation_page` |

## Choosing the Right Search Result
[ref: #dash-choose-result]

A `search_documentation` call may return several entries for the same name.
Pick the result using this order:

1. **Exact name match** — prefer the result whose `name` equals the queried symbol.
2. **API questions** — prefer `Function`, `Method`, `Class`, `Type`, or `Constant`.
3. **Conceptual questions** — prefer `Guide` or `Section`.
4. **Command recipes** — prefer `Entry` from a `cheatsheet` docset.
5. **Code examples** — prefer `Sample` when the user asks for a runnable example.

If no result matches the intent, rephrase the query or fall back to `kagi-search`.

## Listing Installed Docsets
[ref: #dash-list-docsets]

Call `list_installed_docsets` with no arguments.
The result is a list of docset records.
Use the `identifier` value as the `docset_identifiers` argument for `search_documentation`.

Example:

```json
{}
```

Returned identifiers are opaque strings such as `wfenxqwf` for Python or `urmpmslc` for Rust; pass them verbatim.
The `platform` and `name` fields tell you which language or library each docset covers.
If `docsets` is empty, no documentation sets are installed and local Dash lookup cannot proceed; fall back to `kagi-search` or ask the user to install the needed docset.

## Searching Documentation
[ref: #dash-search-docs]

Use `search_documentation` to find symbols and topics across one or more docsets.

Parameters:

- `query` (string, required): the search string.
- `docset_identifiers` (string, required): comma-separated list of identifiers from `list_installed_docsets`.
- `search_snippets` (boolean, optional, default `true`): request code snippets in results.
- `max_results` (integer, optional, default `100`): cap the result count.

Example:

```json
{
  "query": "os.path.join",
  "docset_identifiers": "wfenxqwf",
  "max_results": 3
}
```

Interpret the result list; each item carries a `type`, a `name`, and a `load_url` that can be passed to `load_documentation_page`.
The `search_snippets` flag is forwarded to the underlying docset; in the tested docsets it does not add a separate snippet field to the result object.
Load the page to see the matching content and code examples.

## Enabling Full-Text Search
[ref: #dash-enable-fts]

Some docsets require explicit full-text search activation.
Call `enable_docset_fts` with the docset identifier.

Parameters:

- `identifier` (string, required): the docset identifier.

Example:

```json
{
  "identifier": "wfenxqwf"
}
```

The call returns `true` for docsets that support FTS and `false` for docsets that do not support it or for unknown identifiers.
If the docset already shows `full_text_search: enabled`, the call is idempotent and still returns `true`.
After enabling, re-run `search_documentation` with broader queries; results of type `Full-Text Search` may now appear alongside index entries.

## Loading a Documentation Page
[ref: #dash-load-page]

When `search_documentation` returns a `load_url`, pass it to `load_documentation_page` to retrieve the page content as Markdown.

Parameters:

- `load_url` (string, required): the opaque URL from a search result.

Example:

```json
{
  "load_url": "http://127.0.0.1:49879/Dash/ydhmyixk/doc/library/os.path.html#//apple_ref/Function/os.path.join"
}
```

The returned Markdown contains the whole page, even when the `load_url` includes an anchor.
Anchors identify the matching symbol but do not restrict the returned content.
Documentation pages can be large; if the returned content exceeds the available context budget, refine the query to a more specific symbol before loading.
Do not construct `load_url` values by hand; always use the URLs returned by `search_documentation`.
An invalid or stale `load_url` returns empty `content` and an `error` such as `Documentation page not found.`.

## Examples and Result Catalog
[ref: #dash-examples]

Concrete payloads for every tool, a catalog of common `search_documentation` result types, and error-handling patterns live in `references/dash-tool-examples.md`.
Load only the sections you need using the lazy-load routing rules from `frontmatter-protocol`.

## Master Execution Workflow
[ref: #dash-workflow]

0. Before answering any code, API, or configuration question, consider whether a local Dash docset has the answer.
1. Identify the documentation need.
2. Call `list_installed_docsets` if the available docsets are unknown.
3. Call `search_documentation` with the appropriate docset identifiers.
4. If search returns only index entries or too few matches, call `enable_docset_fts` and search again.
5. Choose the best result using the result-selection criteria.
6. Call `load_documentation_page` on the relevant `load_url`.
7. Distill the result and answer the user.
8. If Dash cannot answer, fall back to `kagi-search`.

## Violation Protocol
[ref: #dash-violation]

If you use training data, web search, or any non-Dash mechanism when a Dash MCP tool is appropriate, halt immediately, discard the offending output, perform the required Dash lookup, and continue from the result.
Systemic or repeated violations MUST be recorded in Serena memory under `bugs/project/dash-protocol-bypass`.
