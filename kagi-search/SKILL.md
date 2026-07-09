---
name: kagi-search
description: Mandatory protocol for all Kagi web search and enrichment operations. Governs tool selection across kagi_search_fetch, kagi_fastgpt, kagi_extract, and kagi_summarizer, with examples and efficiency guidance. Always active.
triggers:
  always: true
  reason: "Web search and page enrichment may be needed in any session."
---

# SKILL: Kagi Search & Enrichment Protocol

This skill governs every use of the `kagimcp` MCP tools.
When this skill is active, you MUST use Kagi tools for any web search or page enrichment instead of raw CLI alternatives.

## 1. MCP Group Declaration

This task requires the `kagimcp` MCP skill group.
All web search, news retrieval, page extraction, and summarization MUST go through the tools listed below.

## 2. Lazy-Load Protocol (CRITICAL)

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

## 3. Tool Selection Guide

| Tool | Best for | When to use |
|---|---|---|
| `kagi_search_fetch` | General web/news/video/image/podcast search. | Default first choice for almost any search. Use for discovery, finding documentation, news, tutorials, and source verification. |
| `kagi_fastgpt` | AI-generated answers with citations. | When the user asks a direct question and a synthesized, cited answer is more valuable than a list of links. |
| `kagi_extract` | Full-page Markdown extraction. | When you already have a URL and need the complete page content, not a summary. |
| `kagi_summarizer` | Condensed page summary. | When you have a long page and only need the key takeaways or a short paragraph. |

## 4. kagi_search_fetch

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

## 5. kagi_fastgpt

Use this when the user asks a direct question such as "What is X?", "How does Y work?", or "Compare A and B.".
Always set `web_search: true` unless you are asking a purely internal question.

The output is a synthesized answer with numbered citations and source URLs.
Summarize the answer for the user; do not dump raw output unless requested.

## 6. kagi_extract

Use this when:

- You have a specific documentation page and need the full text.
- Search snippets are insufficient and you need detailed procedures or code examples.
- You need to quote exact passages from a page.

## 7. kagi_summarizer

Use this when:

- The page is long and you only need the gist.
- You want bullet points for quick scanning (`summary_type: "takeaway"`).
- You want a concise paragraph (`summary_type: "summary"`).

## 8. Efficiency Rules

- Start with the narrowest query and lowest `limit`.
- Use `include_domains` to restrict to authoritative sources.
- Use `time_relative` for time-sensitive topics.
- Do not call multiple tools in parallel unless the queries are independent.
- Distill web results before passing them to subagents or users.

## 9. Interaction with Subagents

Subagents do NOT have access to `kagimcp` tools.
If a subagent needs web data, the main agent MUST perform the Kagi call and pass distilled results in the subagent prompt.

## 10. Master Execution Workflow

1. **Analyze Task:** Determine whether the user needs search, a synthesized answer, full-page content, or a summary.
2. **Tool Selection:** Choose the tool from Section 3.
3. **Example Lookup:** If you need an example payload, use the Lazy-Load Protocol in Section 2.
4. **Execute:** Call the selected Kagi tool with the minimum necessary parameters.
5. **Distill:** Summarize or extract the relevant facts for the user or subagent.
6. **Verify:** Confirm you did not use a raw CLI search tool when a Kagi tool was appropriate.

## 11. Violation Protocol

If you use a raw CLI search tool (for example `curl` to a search engine or `grep` over downloaded pages) when a Kagi MCP tool is appropriate, halt immediately and retry with the correct Kagi tool.
