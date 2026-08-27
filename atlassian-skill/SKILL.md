---
name: atlassian-skill
description: "Read-only access to Atlassian Jira and Confluence via MCP. Use for reading Jira issues/tickets and Confluence pages/documentation, including daily page diffs. Triggers on mentions of Jira, Confluence, Atlassian, Jira issue, Jira ticket, Confluence page, Confluence space, daily doc sync, page diff, or page history."
triggers:
  request: "jira, confluence, atlassian, issue, ticket, epic, jira issue, jira task, confluence page, confluence space, confluence doc, daily doc sync, page diff, page history, джира, жира, задача в джира, тикет, конфла, конфлюенс, страница конфлюенс"
  reason: "User needs to read Jira issues or Confluence pages."
runtime: true
version: 0.1.0
---

# SKILL: Atlassian Reader (Jira + Confluence)

Read-only skill for Atlassian Cloud and Data Center. Covers Jira issue search/reading and Confluence page search/reading, including daily diff/history sync. Never writes or mutates Atlassian data.

## Allowed tools

[ref: #atlassian-allowed-tools]

This skill is read-only. Use only the tools listed below. Never call any tool that creates, updates, transitions, deletes, or writes Atlassian data. If the user asks for a read operation not listed here, confirm before using another read-only tool.

### Jira

- `jira_search` — search issues via JQL.
- `jira_get_issue` — read one issue with comments, worklogs, and links.
- `jira_get_project_issues` — list issues in a project.
- `jira_get_all_projects` / `jira_search_projects` — find projects.
- `jira_get_user_profile` — resolve a Jira user.

### Confluence

- `confluence_search` — CQL or text search for pages.
- `confluence_get_page` — read a page by ID or title+space.
- `confluence_get_page_children` — child pages and folders.
- `confluence_get_space_page_tree` — full space hierarchy.
- `confluence_get_page_history` — previous versions.
- `confluence_get_page_diff` — diff between two versions.
- `confluence_search_user` — resolve a Confluence user.

## Hard parameter rules

[ref: #atlassian-hard-parameter-rules]

### Confluence

| Parameter | Rule |
|---|---|
| `convert_to_markdown` | **Always `true`.** Returning storage-XHTML kills the session. Hard rule. |
| `include_content` | **Always `false`** for `confluence_get_page_children` and `confluence_get_space_page_tree`. Bodies are not needed for navigation. |
| `include_metadata` | **Default `false`** for `confluence_get_page` when only page text is needed. |
| `limit` | Search — `3–5`; children — `5–10`; space tree — `10–20`. |
| `spaces_filter` | Use when the space key is known. |

### Jira

| Parameter | Rule |
|---|---|
| `fields` | **Always pass** a concrete list like `summary,status,assignee,labels`. Never `*all`. |
| `comment_limit` | For `jira_get_issue`: **default `0`**. Read comments only if the user explicitly asks. |
| `limit` | Search — `3–5`, max `10`; project issues — `5–10`. |
| `expand` | **`renderedFields` is forbidden in any form.** HTML in responses is not allowed. |
| `include` | Never use `include=all`. Request only explicitly needed sections. |
| `use_display_names` | Default `false`; `true` inflates the response. |

### Jira issue key format

[ref: #atlassian-jira-issue-key-format]

Jira issue keys are **always uppercase**.

- Normalize any user-supplied key to uppercase before calling Jira tools.
- Valid format: `[A-Z][A-Z0-9_]+-\d+` (for example `PROJECT-123`, `TEAM42-7`, `MY_PROJECT-99`).
- Never pass a mixed-case or lowercase key such as `Crypto-5314`; convert it to `CRYPTO-5314` first.
- This rule is hard: a lowercase key fails validation before the tool call.

### Pagination

Use `start`/`start_at`/`page_token` instead of pulling large lists at once.

## Workflows

[ref: #atlassian-workflows]

If a search returns several equally plausible results, ask the user which one to read instead of fetching multiple pages or issues.

### Read a Jira issue

1. If you have the issue key, normalize it to uppercase (`Crypto-5314` → `CRYPTO-5314`), then call `jira_get_issue` with `fields="summary,status,assignee,labels,description"` and `comment_limit=0`.
2. If not, call `jira_search` with JQL and `limit=5`.
3. Summarize: summary, status, assignee, description, labels. Omit comments unless asked.

### Read project tasks

1. Use `jira_search_projects` or `jira_get_all_projects` to find the project key.
2. Use `jira_get_project_issues` or `jira_search` with `project = KEY`, limited `fields`, and `limit`.

### Read Confluence documentation

1. Use `confluence_search` with a narrow CQL query and `limit=3–5`.
2. Use `confluence_get_page(page_id=..., include_metadata=false)` for the most relevant page.
3. For navigation, use `confluence_get_page_children(..., include_content=false, limit=5–10)` or `confluence_get_space_page_tree(..., limit=10–20)`.

### Daily documentation sync

1. Identify target pages via `confluence_search` or known page IDs.
2. Call `confluence_get_page_history(page_id=..., limit=...)` to list recent versions.
3. From the history, identify the two version numbers that bound the last 24 hours, then call `confluence_get_page_diff(page_id=..., from_version=older, to_version=newer)`.
4. Summarize changes and append to local notes or memory.

## Oversized response hard stop

[ref: #atlassian-oversized-response-hard-stop]

When you receive an MCP tool result, check its character length before processing. If it exceeds ~100 000 characters or consumes most of the available context:

1. **Hard stop.** Do not read further, summarize, save, or continue.
2. Report to the user: the tool called, the arguments used, and the approximate response size.
3. Wait for user instructions.

The raw response is already in context — any continuation makes it worse.

## Error handling

[ref: #atlassian-error-handling]

| Error | Meaning | Action |
|---|---|---|
| `401 Unauthorized` / `403 Forbidden` | Credentials or permissions problem. | **Hard stop.** Ask the user to check credentials. No retries. |
| `404 Not Found` | Issue or page does not exist, or wrong key/ID. | Check the key case and normalize to uppercase; verify the key/ID/space with the user or the source. Do not retry until corrected. |
| Empty search results | Query too narrow or wrong space/project. | Check CQL/JQL and filters. |
| `Confluence client not available` / `Jira client not available` | MCP server did not initialize the client. | Hard stop, report to the user. |
| Oversized response | Response >~100K characters. | See `## Oversized response hard stop`. |

## Context protection

[ref: #atlassian-context-protection]

- Always start with `confluence_search` / `jira_search` with a tight `limit`.
- `convert_to_markdown=true`; `include_content=false` always for children and space tree; `include_metadata=false` by default for page reads.
- Never download attachments or images unless explicitly asked.
- Never request HTML; `renderedFields` and `convert_to_markdown=false` are forbidden.
- For Jira, always pass `fields` and `comment_limit=0` by default.
- Do not keep raw JSON in context: summarize relevant facts and discard the original response.
- Do not pull several large pages/issues into the same turn.
- Daily sync: read diffs, not full pages.
