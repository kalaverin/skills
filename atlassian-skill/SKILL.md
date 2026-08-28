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
| `include_metadata` | **Default `false`** for `confluence_get_page` when only page text is needed. Set `true` when reading version or `history.lastUpdated` for actualization. |
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
- Never pass a mixed-case or lowercase key such as `Wgnbck-5314`; convert it to `WGNBCK-5314` first.
- This rule is hard: a lowercase key fails validation before the tool call.

### External source versioning

[ref: #atlassian-external-source-versioning]

When the agent saves a local copy of an Atlassian artifact, it adds an `external_source` block to the frontmatter. Later "update" / "actualize" requests use this block to fetch only the delta instead of pulling the whole document.

```yaml
external_source:
  atlassian:
    kind: confluence   # or jira
    id: 1501236        # Confluence page ID or uppercase Jira issue key
    version: 41        # Confluence page version; omit for Jira
    updated_at: 2025-06-17T00:00:00Z   # Jira issue updated timestamp; omit for Confluence
    last_sync_at: 2025-06-17T00:00:00Z
```

- `id` — for Confluence the numeric page ID; for Jira the uppercase issue key.
- `version` — Confluence page version number from `history`.
- `updated_at` — Jira issue `updated` field; used instead of `version`.
- `last_sync_at` — UTC timestamp of the last successful sync of this local copy.

If the block is missing or incomplete, fall back to a full read.

### Pagination

Use `start`/`start_at`/`page_token` instead of pulling large lists at once.

## Workflows

[ref: #atlassian-workflows]

If a search returns several equally plausible results, ask the user which one to read instead of fetching multiple pages or issues.

### Read a Jira issue

1. If you have the issue key, normalize it to uppercase (`Wgnbck-5314` → `WGNBCK-5314`).
2. If a tracked local copy exists with `external_source.atlassian.kind=jira` and a matching `id`, compare its `updated_at` with the issue. If they match, return the local summary.
3. Otherwise call `jira_get_issue` with `fields="summary,status,assignee,labels,description,updated"` and `comment_limit=0`.
4. Summarize: summary, status, assignee, description, labels. Omit comments unless asked.
5. When saving a local copy, stamp `external_source.atlassian.kind=jira`, `id`, `updated_at`, and `last_sync_at`.

### Actualize a Jira issue

[ref: #atlassian-workflow-actualize-jira]

1. Load the local copy and read `external_source.atlassian.id` and `external_source.atlassian.updated_at`. Require `kind=jira`.
2. If missing, fall back to **Read a Jira issue**.
3. Normalize the key to uppercase.
4. Call `jira_get_issue(issue_key=..., fields="summary,status,assignee,labels,description,updated", comment_limit=0)`.
5. If returned `updated` equals recorded `updated_at`, report "no changes" and stop.
6. Summarize changes, update the local copy, and bump `external_source.atlassian.updated_at` and `external_source.atlassian.last_sync_at`.

### Read project tasks

1. Use `jira_search_projects` or `jira_get_all_projects` to find the project key.
2. Use `jira_get_project_issues` or `jira_search` with `project = KEY`, limited `fields`, and `limit`.

### Read Confluence documentation

1. If a tracked local copy exists with `external_source.atlassian.kind=confluence`, read its `id` and `version`; otherwise use `confluence_search` with a narrow CQL query and `limit=3–5` to find the page.
2. Use `confluence_get_page(page_id=..., include_metadata=false)` to read the page body.
3. When saving a local copy, stamp `external_source.atlassian.kind=confluence`, `id`, `version`, and `last_sync_at` from `history`.
4. For navigation, use `confluence_get_page_children(..., include_content=false, limit=5–10)` or `confluence_get_space_page_tree(..., limit=10–20)`.

### Actualize a Confluence page

[ref: #atlassian-workflow-actualize-confluence]

1. Load the local copy and read `external_source.atlassian.id` and `external_source.atlassian.version`. Require `kind=confluence`.
2. If missing, fall back to **Read Confluence documentation**.
3. Call `confluence_get_page(page_id=..., include_metadata=true)` to read current version and `history.lastUpdated`.
4. If current version equals recorded `version`, report "no changes" and stop.
5. Call `confluence_get_page_diff(page_id=..., from_version=recorded, to_version=current)`.
6. Summarize the diff, update the local copy, and bump `external_source.atlassian.version` and `external_source.atlassian.last_sync_at`.

### Daily documentation sync

1. For each tracked page, read `external_source.atlassian.id` and `external_source.atlassian.version`.
2. Call `confluence_get_page_history(page_id=..., limit=...)` to list versions newer than the recorded one.
3. If no newer versions exist, skip the page.
4. Otherwise call `confluence_get_page_diff(page_id=..., from_version=recorded, to_version=newest)`.
5. Summarize changes, update the local copy, and bump `external_source.atlassian.version` and `external_source.atlassian.last_sync_at`.
6. For pages without a tracked version, fall back to diffing the last 24 hours.

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
- `convert_to_markdown=true`; `include_content=false` always for children and space tree; `include_metadata=false` by default for page reads; set `true` when actualizing to read `version` and `history.lastUpdated`.
- Never download attachments or images unless explicitly asked.
- Never request HTML; `renderedFields` and `convert_to_markdown=false` are forbidden.
- For Jira, always pass `fields` and `comment_limit=0` by default.
- Do not keep raw JSON in context: summarize relevant facts and discard the original response.
- Do not pull several large pages/issues into the same turn.
- Daily sync: read diffs, not full pages.
