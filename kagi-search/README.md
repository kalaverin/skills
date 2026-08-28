# kagi-search
[ref: #kagi-search]

Routes all web search and page enrichment through the Kagi MCP tools.

## What it does
[ref: #kagi-what-it-does]

This skill makes the agent use Kagi for every external information lookup. It selects the right tool for the job — general search, AI-generated answers with citations, full-page extraction, or page summarization — and enforces efficiency rules such as narrow queries and low result limits. It also defines the narrow raw-fetch exception for exact-byte downloads.

## When it activates
[ref: #kagi-when-it-activates]

No action is needed — it is loaded automatically in every session.

It applies whenever you ask the agent to:

- search the web or "google" something
- find documentation, tutorials, or news online
- answer a factual question that needs current sources
- fetch or summarize a known URL

Example prompts:

- "Search the web for the latest Python release notes."
- "What is Temporal workflow versioning?"
- "Summarize this article: https://example.com/post"
- "Find the official docs for the OpenAI Python SDK."

## How to run / use it
[ref: #kagi-how-to-run-use-it]

What a human must ensure:

- The `kagimcp` MCP skill group is available in the environment. If it is not, web lookups will fail.

What the agent does automatically:

- Chooses the right Kagi tool for the request:
  - `kagi_search_fetch` for general search and discovery.
  - `kagi_fastgpt` for a synthesized, cited answer.
  - `kagi_extract` when you already have a URL and need the full page.
  - `kagi_summarizer` when you need a short summary of a long page.
- Starts with the narrowest query and the lowest practical `limit`.
- Uses `include_domains`, `exclude_domains`, and `time_relative` to keep results focused.

Raw CLI fetches (`curl`, `wget`) are limited to exact-byte retrieval, such as downloading a binary or saving an RFC unchanged.

## What it produces
[ref: #kagi-what-it-produces]

- Search results with optional inline page content.
- Synthesized answers with numbered citations and source URLs.
- Full-page Markdown extractions.
- Condensed page summaries.

## Dependencies and why they matter
[ref: #kagi-dependencies-and-why-they-matter]

| Dependency | Why it matters |
|---|---|
| `kagimcp` MCP tools | The skill owns web search and enrichment; it cannot function without these MCP tools. |

No project skills are required, but this skill is mandatory whenever external lookup is needed.

## Strengths and trade-offs
[ref: #kagi-strengths-and-trade-offs]

- **Strong sides:** Prevents hallucination by requiring live sources, reduces token usage compared to raw page fetches, and funnels all web work through a single authoritative provider.
- **Weak sides / limits:** Requires Kagi MCP to be configured; subagents cannot call Kagi tools directly; not suitable for downloading exact binary bytes.
- **Common pitfalls / gotchas:** `curl` is not used for discovery, reading, or summarization. Training data and general knowledge are not used when a Kagi search could verify the fact. When a subagent needs web data, the main agent fetches and distills it first.

## Repository layout
[ref: #kagi-repository-layout]

```text
kagi-search/
├── references/
│   └── kagi-tool-examples.md   # Concrete examples for each Kagi tool
├── README.md                # Human overview (this file)
└── SKILL.md                    # Agent entry point: rules, tool selection, and routing index
```

## Reference overview
[ref: #kagi-reference-overview]

| File | What it covers |
|---|---|
| `references/kagi-tool-examples.md` | Tested examples for `kagi_search_fetch`, `kagi_fastgpt`, `kagi_extract`, and `kagi_summarizer` |

## Important conventions / gotchas
[ref: #kagi-important-conventions-and-gotchas]

- Kagi is the exclusive search mechanism; other search APIs or raw CLI searches are not used except for the narrow raw-fetch exception.
- Prefer the narrowest query and the lowest result limit to save tokens.
- Use `include_domains` to restrict to authoritative sources and `time_relative` for time-sensitive topics.
- Subagents cannot use Kagi tools; the main agent performs searches and passes distilled results to them.
- Repeated bypasses of this protocol are recorded in Serena memory under `bugs/<entity>/kagi-search-bypass` or `notes/agent/kagi-search-bypass`.
