# atlassian-skill
[ref: #atlassian-skill]

Read-only access to Atlassian Jira and Confluence through the Atlassian MCP tools.

## What it does
[ref: #atlassian-what-it-does]

This skill lets the agent read Jira issues, search tickets, list project issues, and read Confluence pages, page histories, and diffs. It is strictly read-only: it never creates, updates, transitions, or deletes Atlassian data.

## When it activates
[ref: #atlassian-when-it-activates]

The skill loads automatically when the user mentions Jira, Confluence, Atlassian, issues, tickets, pages, spaces, daily doc sync, page diffs, or page history.

Example prompts:

- "Посмотри задачу WGNBCK-5314."
- "Найди в джира тикеты про billing."
- "Прочитай страницу On-call в Confluence."
- "Какие изменения были в доке за последние сутки?"

## How to run / use it
[ref: #atlassian-how-to-run-use-it]

What a human must ensure:

- The Atlassian MCP server is configured with credentials and permissions for the target Jira/Confluence instance.
- Jira issue keys are supplied in uppercase. The skill normalizes keys automatically, but `WGNBCK-5314` is the canonical form.

What the agent does automatically:

- Uses only read-only Jira tools: `jira_search`, `jira_get_issue`, `jira_get_project_issues`, `jira_get_all_projects`, `jira_search_projects`, `jira_get_user_profile`.
- Uses only read-only Confluence tools: `confluence_search`, `confluence_get_page`, `confluence_get_page_children`, `confluence_get_space_page_tree`, `confluence_get_page_history`, `confluence_get_page_diff`, `confluence_search_user`.
- Requests concrete `fields` lists and defaults `comment_limit=0`.
- Sets `convert_to_markdown=true` for every page read.
- Keeps limits tight (`3–5` for searches, `5–10` for children/space tree).
- Normalizes Jira issue keys to uppercase before calling tools.

## What it produces
[ref: #atlassian-what-it-produces]

- Summaries of Jira issues (summary, status, assignee, description, labels).
- Search result overviews with links.
- Confluence page content in Markdown.
- Daily diff summaries from page history.
- Updated local copies with `external_source.atlassian` stamps when actualizing.

## Dependencies and why they matter
[ref: #atlassian-dependencies-and-why-they-matter]

| Dependency | Why it matters |
|---|---|
| Atlassian MCP tools | `jira_*` and `confluence_*` MCP tools are the only way to reach Jira/Confluence; the skill cannot function without them. |

## Strengths and trade-offs
[ref: #atlassian-strengths-and-trade-offs]

- **Strong sides:** Centralizes read-only Atlassian access, prevents accidental writes, enforces tight response limits, and keeps page content in Markdown rather than storage-XHTML.
- **Weak sides / limits:** Cannot modify Atlassian data; requires MCP server credentials; does not download attachments or images by default.
- **Common pitfalls / gotchas:** Jira keys must be uppercase (`WGNBCK-5314`, not `Wgnbck-5314`). Never pass `*all` or `include=all`. Never request `renderedFields`. For daily sync, read diffs, not full pages.

## Repository layout
[ref: #atlassian-repository-layout]

```text
atlassian-skill/
├── README.md   # Human overview (this file)
└── SKILL.md    # Agent entry point: allowed tools, parameter rules, workflows
```

## Important conventions / gotchas
[ref: #atlassian-important-conventions-and-gotchas]

- Issue keys are normalized to uppercase before any Jira call.
- `convert_to_markdown=true` is mandatory for Confluence page reads.
- `renderedFields` and `convert_to_markdown=false` are forbidden.
- Start searches with `limit=3–5`; widen only if needed.
- The agent hard-stops on `401`/`403` and asks the user to check credentials.
- Local copies carry an `external_source.atlassian` block (`kind`, `id`, `version`/`updated_at`, `last_sync_at`). On "actualize" the agent reads only the diff or compares timestamps instead of pulling the whole artifact.
