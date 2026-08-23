---
subject: "Dash MCP tool examples; `list_installed_docsets`, `search_documentation`, `enable_docset_fts`, `load_documentation_page`, result interpretation, empty results, common result types across Python, Rust, Go, and cheatsheet docsets; docset identifiers, symbol lookup, multi-docset search, guide pages, sample pages, error handling, full text search activation."
index:
  - anchor: dash-ex-list-docsets
    what: "Initial inventory call that enumerates installed docsets and their capabilities."
    problem: "Agent lacks local docset identifiers before searching; guessing identifiers produces empty results or pulls wrong docset; docset inventory, available sets, identifiers, installed documentation, local docs, docset discovery, dash catalog, full text search status."
    use_when: "Starting a documentation task; the target identifier is unknown; verifying whether a specific docset is installed."
    avoid_when: "The identifier is already known from a previous call or project context."
    expected: "A list of records with `identifier`, `name`, `platform`, and FTS capability flags."
  - anchor: dash-ex-search-symbol
    what: "Named API entry lookup in one docset, returning typed results with a `load_url`."
    problem: "Agent needs signature or behavior of known API symbol; web search returns stale or mismatched version; symbol lookup, API reference, function signature, method docs, callable entry, official docs, exact match, version correctness, language standard."
    use_when: "The symbol name is known and the docset identifier is available; you need the official page reference."
    avoid_when: "The query is vague or exploratory; prefer broad topic search."
    expected: "One or more results pointing to the symbol's documentation page."
  - anchor: dash-ex-search-multi
    what: "Cross-docset search for concepts that exist in several languages, using identifiers from `list_installed_docsets`."
    problem: "Same concept lives in multiple docsets and agent must compare language-specific docs; cross-language lookup, polyglot search, compare APIs, multi-docset query, comma-separated identifiers, language comparison, API parity, concept mapping, runtime differences, standard library equivalents."
    use_when: "Querying a concept such as `map`, `filter`, or `error handling` across Python, Rust, and Go."
    avoid_when: "Only one language is relevant; single-docset search reduces noise."
    expected: "Mixed results from each selected docset, tagged by `platform` and `docset`."
  - anchor: dash-ex-search-topic
    what: "Topic-oriented search returning explanatory chapters and sections rather than single symbols."
    problem: "Agent needs conceptual explanation rather than function signature; broad query returns guides, book chapters, and narrative sections; how-to, guide, tutorial, concept, pattern, explanatory prose, task-oriented docs, learning material, design rationale."
    use_when: "The query names a concept or task like `error handling` or `list comprehensions`."
    avoid_when: "Looking for a specific class or function; use symbol lookup instead."
    expected: "Guide or section results with page-level `load_url`."
  - anchor: dash-ex-search-cheatsheet
    what: "Search in a quick-reference docset to retrieve command snippets and recipes."
    problem: "Agent needs terse command or recipe rather than full prose documentation; cheatsheet docset stores terse reference cards with copy-paste snippets; command cheat sheet, quick reference, snippet, CLI recipe, workflow reminder, terminal commands."
    use_when: "The installed docset has `platform: cheatsheet` and the query names a command or workflow."
    avoid_when: "Needing detailed behavior explanation; load the full page from a narrative docset instead."
    expected: "`Entry`-typed results with command snippets ready to copy."
  - anchor: dash-ex-search-empty
    what: "Handling a result list with zero entries when the symbol or topic is absent."
    problem: "Search returns zero hits; agent must decide whether query phrase was wrong, docset is missing, or term is not indexed; empty result, no matches, troubleshooting, search failure, query reformulation, identifier check, vocabulary mismatch, result absence, query tuning."
    use_when: "A query returned `[]`; rephrasing the query or checking installed docsets."
    avoid_when: "Results are non-empty; proceed to `load_documentation_page`."
    expected: "Clear next step: rephrase query, check identifiers, or fall back."
  - anchor: dash-ex-enable-fts
    what: "Activation call that enables body-text matching in FTS-capable docsets."
    problem: "Broad queries in some docsets return only index entries and miss body text; FTS activation unlocks full-text matches inside articles; full text search, index expansion, body search, broader recall, deep matching."
    use_when: "A docset's `full_text_search` is `enabled` and a broad query returns too few matches."
    avoid_when: "The docset reports `not supported`; the query already returns good index matches."
    expected: "`true` when activation succeeds; subsequent searches include full-text hits."
  - anchor: dash-ex-load-function
    what: "Loading a symbol page from a `Function` or `Method` result to read signature and behavior."
    problem: "Search gives only title and URL; agent needs full prose, parameters, and examples for callable symbol; full page, signature, parameters, argument list, return value, code samples, member details, overload variants."
    use_when: "A search result of type `Function`, `Method`, or `Class` has a `load_url`."
    avoid_when: "Only the result title is needed; loading wastes tokens."
    expected: "Markdown page with the symbol's full documentation."
  - anchor: dash-ex-load-guide
    what: "Loading narrative sections and cheatsheet pages from `Guide`, `Section`, or `Entry` results."
    problem: "Conceptual or recipe results require full context; partial snippets from search are insufficient for answering how or why; tutorial, recipe, command reference, explanatory chapter, narrative guide, step-by-step instructions, background rationale, usage examples."
    use_when: "The result type is `Guide`, `Section`, or `Entry` and the user needs surrounding content."
    avoid_when: "A short snippet already answers the question."
    expected: "Complete Markdown of the result page."
  - anchor: dash-ex-load-not-found
    what: "Error handling when a `load_url` points to a missing or malformed local path."
    problem: "Stale bookmark or invalid URL yields no content; agent must detect failure and retry with corrected search; missing page, broken link, page not found, stale reference, local docset gap, fallback decision, retry strategy."
    use_when: "`load_documentation_page` returned empty `content` and a non-null `error`."
    avoid_when: "The page loaded successfully."
    expected: "Agent reports the failure and either re-searches or falls back."
  - anchor: dash-ex-result-types
    what: "Catalog of common `type` values returned by `search_documentation` and their meaning."
    problem: "Agent misinterprets result types and loads wrong kind of page; confusing `Function` with `Guide` wastes tokens and yields irrelevant content; type semantics, result taxonomy, result classification, entry kind, content shape, label meaning."
    use_when: "Parsing search results to decide which `load_url` to follow."
    avoid_when: "No search results are present."
    expected: "Correct mapping from `type` label to expected page structure."
---

# Dash MCP Tool Examples
[ref: #dash-ex-list-docsets]

Call `list_installed_docsets` with no arguments to discover what is available.

```json
{}
```

A trimmed response looks like this:

```json
{
  "docsets": [
    {
      "name": "Python 3.14.6",
      "identifier": "wfenxqwf",
      "platform": "python",
      "full_text_search": "enabled",
      "notice": null
    },
    {
      "name": "Rust 1.97.1",
      "identifier": "urmpmslc",
      "platform": "rust",
      "full_text_search": "enabled",
      "notice": null
    }
  ],
  "error": null
}
```

Use the `identifier` value in subsequent `search_documentation` calls.

## Searching for a symbol in one docset
[ref: #dash-ex-search-symbol]

Query a known function or method in a single docset.

```json
{
  "query": "os.path.join",
  "docset_identifiers": "wfenxqwf",
  "max_results": 3
}
```

Response:

```json
{
  "results": [
    {
      "name": "join",
      "type": "Function",
      "platform": "python",
      "load_url": "http://127.0.0.1:49879/Dash/ydhmyixk/doc/library/os.path.html#//apple_ref/Function/os.path.join",
      "docset": "Python",
      "description": "os.path",
      "language": null,
      "tags": null
    }
  ],
  "error": null
}
```

## Searching across multiple docsets
[ref: #dash-ex-search-multi]

Pass comma-separated identifiers to compare the same concept in several languages.

```json
{
  "query": "map",
  "docset_identifiers": "wfenxqwf,urmpmslc,zopnyeol",
  "max_results": 5
}
```

The result mixes entries from Python, Rust, and Go, each tagged with its own `platform` and `docset`.

## Searching for a guide or topic
[ref: #dash-ex-search-topic]

Use broad, conceptual queries when you need an explanation rather than a single API entry.

```json
{
  "query": "error handling",
  "docset_identifiers": "urmpmslc",
  "max_results": 3
}
```

Result types include `Guide` and `Section`, and the `load_url` points to a chapter or page rather than an anchor.

## Searching a cheatsheet docset
[ref: #dash-ex-search-cheatsheet]

Cheatsheet docsets return `Entry` results with command snippets.

```json
{
  "query": "clone",
  "docset_identifiers": "vaypjksk",
  "max_results": 3
}
```

Response:

```json
{
  "results": [
    {
      "name": "Clone an existing repository",
      "type": "Entry",
      "platform": "cheatsheet",
      "load_url": "http://127.0.0.1:49879/Dash/oqugypzb/index.html#//dash_ref_Create/Entry/Clone%20an%20existing%20repository/0",
      "docset": "Git",
      "description": null,
      "language": null,
      "tags": null
    }
  ],
  "error": null
}
```

## Handling empty search results
[ref: #dash-ex-search-empty]

A missing symbol returns an empty result list.

```json
{
  "query": "nonexistent_xyz_123",
  "docset_identifiers": "wfenxqwf",
  "max_results": 3
}
```

Response:

```json
{
  "results": [],
  "error": null
}
```

When this happens, rephrase the query, confirm the docset identifier, or fall back to web search.

## Enabling full-text search
[ref: #dash-ex-enable-fts]

Call `enable_docset_fts` before broad queries that return only index matches.

```json
{
  "identifier": "wfenxqwf"
}
```

A supported docset returns `true`.
A docset that does not support FTS, or a non-existent identifier, returns `false`.

## Loading a function or method page
[ref: #dash-ex-load-function]

Pass the `load_url` from a `Function` or `Method` result to `load_documentation_page`.

```json
{
  "load_url": "http://127.0.0.1:49879/Dash/ydhmyixk/doc/library/os.path.html#//apple_ref/Function/os.path.join"
}
```

The returned Markdown contains the whole page, including the symbol signature, parameter list, and examples.
The anchor in the URL identifies the symbol but does not restrict the returned content.

## Loading a guide or cheatsheet page
[ref: #dash-ex-load-guide]

For `Guide`, `Section`, or `Entry` results, load the full page to get surrounding context.

```json
{
  "load_url": "http://127.0.0.1:49879/Dash/pmsfruit/doc.rust-lang.org/1.97.1/book/ch09-00-error-handling.html"
}
```

A cheatsheet `load_url` returns the entire cheatsheet page, which includes all sections:

```json
{
  "load_url": "http://127.0.0.1:49879/Dash/oqugypzb/index.html#//dash_ref_Create/Entry/Clone%20an%20existing%20repository/0"
}
```

## Handling a missing page
[ref: #dash-ex-load-not-found]

An invalid or stale `load_url` returns an error instead of content.

```json
{
  "load_url": "http://127.0.0.1:49879/Dash/invalid/url.html"
}
```

Response:

```json
{
  "content": "",
  "load_url": "http://127.0.0.1:49879/Dash/invalid/url.html",
  "error": "Documentation page not found."
}
```

## Common result types
[ref: #dash-ex-result-types]

`search_documentation` returns a `type` field that hints at the result shape:

| Type | Meaning |
|---|---|
| `Function` | A function or callable. |
| `Method` | A method on a type or class. |
| `Class` | A class or struct definition. |
| `_Struct` / `Struct` | A struct type, common in Rust docsets; `_Struct` is a docset-specific artifact and should be treated like `Struct`. |
| `Type` | A type alias or type definition. |
| `Constant` | A constant value. |
| `Guide` | A book chapter or explanatory guide. |
| `Section` | A section within a larger page. |
| `Entry` | A cheatsheet entry with a snippet. |
| `Sample` | A code example, common in Go docsets. |
| `Full-Text Search` | A page-level hit found by full-text search. |

Treat the type as a hint for which `load_url` to follow and how much context to load.
