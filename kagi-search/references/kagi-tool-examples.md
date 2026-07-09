# Kagi Tool Examples

This file contains concrete, tested examples for every working `kagimcp` tool.
Copy and adapt the calls for real tasks.
Do not read this file in full; extract only the section you need via the anchor tags.

## [ref: #kagi-search-fetch-examples] kagi_search_fetch

Default mixed search (web, news, images, videos):

```json
{
  "query": "temporal workflow patterns",
  "limit": 5
}
```

News-only search:

```json
{
  "query": "OpenAI",
  "workflow": "news",
  "limit": 3
}
```

Filtered search by domain and recency:

```json
{
  "query": "Python 3.13 release notes",
  "include_domains": ["docs.python.org", "python.org"],
  "time_relative": "month",
  "limit": 5
}
```

Fetch full inline content for the top results:

```json
{
  "query": "Temporal workflow versioning",
  "include_domains": ["docs.temporal.io"],
  "extract_count": 2,
  "limit": 3
}
```

## [ref: #kagi-fastgpt-examples] kagi_fastgpt

Question with mandatory web search:

```json
{
  "query": "What is a neural network?",
  "web_search": true
}
```

Use this when the user asks a direct factual question and you need a synthesized answer with sources.

## [ref: #kagi-extract-examples] kagi_extract

Extract a documentation page as Markdown:

```json
{
  "url": "https://docs.temporal.io/workflows"
}
```

Use this when you already have a URL and need the complete page content, not a summary or search snippet.

## [ref: #kagi-summarizer-examples] kagi_summarizer

Bullet-point summary:

```json
{
  "url": "https://docs.temporal.io/workflows",
  "summary_type": "takeaway"
}
```

Paragraph summary:

```json
{
  "url": "https://docs.temporal.io/workflows",
  "summary_type": "summary"
}
```

Use this when the page is long and you only need the key points.
