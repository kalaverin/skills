# kagi-search

Routes all web search and page enrichment through the Kagi MCP tools.

## What it does

This skill makes the agent use Kagi for every external lookup.
It covers general web search, news search, AI-generated answers with citations, full-page extraction, and page summarization.
It also defines efficiency rules and the narrow raw-fetch exception.

## When it activates

No action needed — loaded automatically in every session.

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

## How to use it

Ask the agent to look something up online.
The skill chooses the right Kagi tool for the job:

- `kagi_search_fetch` for general search and discovery.
- `kagi_fastgpt` for a synthesized, cited answer.
- `kagi_extract` when you already have a URL and need the full page.
- `kagi_summarizer` when you need a short summary of a long page.

If you need exact bytes from a specific URL, such as downloading a binary or raw config file, the agent may use a raw CLI fetch instead.

## What it produces

- Search results and inline page content.
- Synthesized answers with citations.
- Full-page Markdown extractions.
- Condensed page summaries.

## Repository layout

```text
kagi-search/
├── references/
│   └── kagi-tool-examples.md   # Concrete examples for each Kagi tool
└── SKILL.md                    # Agent entry point: rules, tool selection, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/kagi-tool-examples.md` | Tested examples for `kagi_search_fetch`, `kagi_fastgpt`, `kagi_extract`, and `kagi_summarizer` |

## Important conventions / gotchas

- The `kagimcp` MCP skill group must be available in the environment.
- The agent prefers the narrowest query and the lowest result limit to save tokens.
- Raw CLI fetches are allowed only for exact-byte retrieval, not for search or summarization.
- Subagents cannot use Kagi tools; the main agent performs searches and passes distilled results to them.
