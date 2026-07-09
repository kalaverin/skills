---
name: kagi-search
description: Mandatory and exclusive protocol for all web search and page enrichment. Applies whenever the user mentions internet search, asks to 'google' something (including the Russian verb 'погуглить'), 'find online', 'search the web', or any equivalent. The agent MUST use Kagi MCP tools for any external information lookup; no other search mechanism is permitted. Governs kagi_search_fetch, kagi_fastgpt, kagi_extract, and kagi_summarizer with examples and efficiency guidance. Always active.
triggers:
  always: true
  reason: "Web search and page enrichment may be needed in any session, and this skill mandates exclusive use of Kagi."
---

# SKILL: Kagi Search & Enrichment Protocol

This skill governs every use of the `kagimcp` MCP tools.
When this skill is active, you MUST use Kagi tools for any web search, news retrieval, page extraction, or summarization.
No other search mechanism is permitted.

Any user request phrased as "погугли", "поищи в интернете", "search the web", "google it", "find online", or any similar phrase MUST be handled through this skill and therefore through Kagi tools.

## 1. Absolute Search Rule (HARD RULE)

Whenever the current task requires information that is not already present in the project context, Serena memory, or the current conversation, you MUST use a Kagi tool to obtain it.

You MUST NOT:

- Use your training data or general knowledge as a substitute for a live web search.
- Use any CLI tool to perform a web search (for example `curl`, `wget`, `lynx`, `w3m`, `python requests`, or `grep` over downloaded pages).
- Use any non-Kagi search API or service.
- Guess, assume, or hallucinate facts that could be verified with a Kagi search.

If the answer matters, search for it with Kagi.

The only exception is the raw-fetch case described in Section 1.1.

## 1.1 When Raw Fetch is Permitted

You MAY use a raw CLI fetch tool (for example `curl` or `wget`) ONLY when the explicit goal is to obtain the exact bytes returned by a specific URL, with no transformation, summarization, or search.

Permitted cases include:

- Downloading a source file, binary, archive, or asset exactly as the server serves it.
- Fetching an RFC, standard, or specification to save it to Serena memory or disk unchanged.
- Retrieving a raw config, schema, or data file for direct storage or checksum verification.

In all other cases — discovery, reading, summarizing, searching, comparing, or answering questions about web content — you MUST use Kagi tools.
Kagi tools are strongly preferred because they minimize token usage.

## 2. MCP Group Declaration

This task requires the `kagimcp` MCP skill group.
All web search, news retrieval, page extraction, and summarization MUST go through the tools listed below.

## 3. Lazy-Load Protocol (CRITICAL)

You MUST NOT read `references/kagi-tool-examples.md` in its entirety.
Use the Routing Index below to extract only the section you need.

**Extraction Execution:**
1. Match your task to a "Trigger / Situation" in the Routing Index below.
2. Copy the corresponding `[ref: ...]` tag.
3. Use `rg` to extract ONLY the relevant section.
   *Example CLI command:* `rg -A 30 "\\[ref: #kagi-search-fetch-examples\\]" references/kagi-tool-examples.md`
4. Apply the extracted example strictly.

### Routing Index

| Trigger / Situation | Target Section | Anchor |
|---|---|---|
| Writing or adapting a `kagi_search_fetch` call. | Search examples | `[ref: #kagi-search-fetch-examples]` |
| Writing or adapting a `kagi_fastgpt` call. | FastGPT examples | `[ref: #kagi-fastgpt-examples]` |
| Writing or adapting a `kagi_extract` call. | Extract examples | `[ref: #kagi-extract-examples]` |
| Writing or adapting a `kagi_summarizer` call. | Summarizer examples | `[ref: #kagi-summarizer-examples]` |

## 4. Tool Selection Guide

| Tool | Best for | When to use |
|---|---|---|
| `kagi_search_fetch` | General web/news/video/image/podcast search. | Default first choice for almost any search. Use for discovery, finding documentation, news, tutorials, and source verification. |
| `kagi_fastgpt` | AI-generated answers with citations. | When the user asks a direct question and a synthesized, cited answer is more valuable than a list of links. |
| `kagi_extract` | Full-page Markdown extraction. | When you already have a URL and need the complete page content, not a summary. |
| `kagi_summarizer` | Condensed page summary. | When you have a long page and only need the key takeaways or a short paragraph. |

## 5. kagi_search_fetch

This is the workhorse tool.

Use it for:

- Finding documentation, libraries, or APIs.
- News search (`workflow: "news"`).
- Video, podcast, or image search (`workflow: "videos"`, `"podcasts"`, `"images"`).
- Domain-restricted searches (`include_domains`, `exclude_domains`).
- Time-bounded searches (`after`, `before`, `time_relative`).
- Fetching full inline content for top results (`extract_count`).

Prefer a low `limit` (3–5) to save tokens.
Only increase `limit` when the first page is insufficient.

### Example patterns

Find official docs only:

```json
{
  "query": "Temporal workflow versioning",
  "include_domains": ["docs.temporal.io"],
  "limit": 3
}
```

Recent news:

```json
{
  "query": "OpenAI",
  "workflow": "news",
  "time_relative": "week",
  "limit": 5
}
```

## 6. kagi_fastgpt

Use this when the user asks a direct question such as "What is X?", "How does Y work?", or "Compare A and B.".
Always set `web_search: true` unless you are asking a purely internal question.

The output is a synthesized answer with numbered citations and source URLs.
Summarize the answer for the user; do not dump raw output unless requested.

## 7. kagi_extract

Use this when:

- You have a specific documentation page and need the full text.
- Search snippets are insufficient and you need detailed procedures or code examples.
- You need to quote exact passages from a page.

## 8. kagi_summarizer

Use this when:

- The page is long and you only need the gist.
- You want bullet points for quick scanning (`summary_type: "takeaway"`).
- You want a concise paragraph (`summary_type: "summary"`).

## 9. Efficiency Rules

- Start with the narrowest query and lowest `limit`.
- Use `include_domains` to restrict to authoritative sources.
- Use `time_relative` for time-sensitive topics.
- Do not call multiple tools in parallel unless the queries are independent.
- Distill web results before passing them to subagents or users.

## 10. Interaction with Subagents

Subagents do NOT have access to `kagimcp` tools.
If a subagent needs web data, the main agent MUST perform the Kagi call and pass distilled results in the subagent prompt.

## 11. Master Execution Workflow

1. **Analyze Task:** Determine whether the user needs search, a synthesized answer, full-page content, or a summary.
2. **Check Need:** If the information is not already in context, memory, or conversation, you MUST use Kagi, unless the task is a raw-fetch case under Section 1.1.
3. **Tool Selection:** Choose the tool from Section 4.
4. **Example Lookup:** If you need an example payload, use the Lazy-Load Protocol in Section 3.
5. **Execute:** Call the selected Kagi tool with the minimum necessary parameters.
6. **Distill:** Summarize or extract the relevant facts for the user or subagent.
7. **Verify:** Confirm you did not use training data, a raw CLI tool, or any non-Kagi search mechanism.

## 12. Violation Protocol

If you use training data, a raw CLI search tool, or any non-Kagi mechanism when a Kagi tool is appropriate, halt immediately, discard the offending output, perform the required Kagi search, and continue from the Kagi results.
Raw CLI fetches are allowed only under the narrow exception in Section 1.1; any other raw fetch is a violation.
Repeated violations MUST be recorded in Serena memory under `bugs/<entity>/kagi-search-bypass` or `notes/agent/kagi-search-bypass`.
