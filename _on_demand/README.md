# _on_demand
[ref: #ondemand-readme-intro]

On-demand skills are rarely used capabilities stored outside the always-loaded skill set. They are discovered from a compressed manifest in `_on_demand/SKILL.md` and loaded only when their triggers match the current request.

## What on-demand skills are
[ref: #ondemand-readme-what]

- Optional skills that do not need to be parsed at every session start.
- Each skill lives in its own directory under `_on_demand/<skill>/`.
- The manifest keeps the agent startup cheap by holding only headers, not full skill bodies.

## How the manifest is used
[ref: #ondemand-readme-usage]

- At bootstrap, `_on_demand/SKILL.md` is discovered and its frontmatter is batch-extracted like any skill header.
- Entries marked `runtime: true` are re-evaluated after every new user message or path touch.
- When a manifest entry matches, the agent reads `_on_demand/<skill>/SKILL.md` and resolves its `requires`.
- Entries without `runtime: true` are evaluated once at bootstrap and never re-evaluated mid-session.

## On-demand skill index
[ref: #ondemand-readme-index]

| Skill | Runtime | Short description | Path |
|---|---|---|---|
| `atlassian-skill` | yes | Read-only Atlassian Jira and Confluence access via MCP. | `_on_demand/atlassian-skill/` |
| `bobplus-api` | yes | Bobplus Payments API integration knowledge for Africa payments. | `_on_demand/bobplus-api/` |
| `code-review` | yes | Language-agnostic diff-based and full-project code review. | `_on_demand/code-review/` |
| `loki-skill` | yes | Grafana Loki log investigation through `logcli`. | `_on_demand/loki-skill/` |
| `protobuf-lang` | yes | Buf Protobuf lint and schema style. | `_on_demand/protobuf-lang/` |
| `pytest-design` | yes | Python unit, integration, and pytest suite work. | `_on_demand/pytest-design/` |
| `pytest-planner` | no | Repository-specific pytest enablement and coverage plans. | `_on_demand/pytest-planner/` |
| `repo-audit` | no | Full repository audits, entity cards, and dependency maps. | `_on_demand/repo-audit/` |
| `security-audit` | no | OWASP API Security Top 10 aligned SAST workflow. | `_on_demand/security-audit/` |
| `session-inspector` | yes | Token-cheap inspection of Kimi Code CLI session files. | `_on_demand/session-inspector/` |
| `temporal-lang` | yes | Temporal workflows, activities, workers, and operations. | `_on_demand/temporal-lang/` |

## How to add a new on-demand skill
[ref: #ondemand-readme-add]

1. Create `_on_demand/<skill>/SKILL.md` with a valid frontmatter header, triggers, and `runtime: true` if it should re-evaluate mid-session.
2. Add an entry to `_on_demand/SKILL.md` frontmatter `ondemand:` block, copying `description`, `triggers`, and `runtime` exactly.
3. Add a mapping row to the `## Mapping` table in `_on_demand/SKILL.md`.
4. Add a row to the index table in `_on_demand/README.md`.

## Repository layout
[ref: #ondemand-readme-layout]

```text
_on_demand/
├── README.md              # Human overview (this file)
├── SKILL.md               # Runtime manifest and mapping table
├── atlassian-skill/       # Jira and Confluence read-only integration
├── bobplus-api/           # Bobplus Payments API integration
├── code-review/           # Language-agnostic code review
├── loki-skill/            # Grafana Loki log investigation
├── protobuf-lang/         # Buf Protobuf lint and schema style
├── pytest-design/         # Python test authoring and review
├── pytest-planner/        # Pytest enablement and coverage plans
├── repo-audit/            # Repository audit and business-domain reports
├── security-audit/        # Security assessment workflow
├── session-inspector/     # Kimi session inspection tools
└── temporal-lang/         # Temporal application development
```

## Dependencies
[ref: #ondemand-readme-deps]

- `frontmatter-protocol` — defines the skill header schema, trigger grammar, and discovery algorithm that consume this manifest.
