# loki-skill
[ref: #loki-skill]

Read-only Grafana Loki log investigation through the `logcli` command-line client.

## What it does
[ref: #loki-what-it-does]

This skill lets the agent query logs, labels, series, and read-only metadata in Grafana Loki without mutating any data. It enforces a narrow-first query style: small `--limit`, short `--since`, output redirected to temporary files, and a 50 KiB size gate before anything is read into context. It also blocks destructive or expensive flags such as `--parallel-*`, `--interval`, and `--tail`.

## When it activates
[ref: #loki-when-it-activates]

The skill loads automatically when the user asks about logs, Loki, `logcli`, Grafana logs, incident investigation, or Sentry correlation.

Example prompts:

- "Посмотри логи billing на проде за последний час."
- "Найди в локи ошибки с trace_id=..."
- "Разбери инцидент: в Sentry event_id=..."
- "logcli query for api errors since 15m"

## How to run / use it
[ref: #loki-how-to-run-use-it]

What a human must ensure:

- `logcli` is installed and on `PATH`.
- `LOKI_ADDR` points at the Loki instance. If it is missing, the agent asks for it.
- For multi-tenant gateways, set `LOKI_ORG_ID` when the gateway requires `X-Scope-OrgID`.

What the agent does automatically:

- Builds only read-only commands: `query`, `instant-query`, `labels`, `series`, `stats`, `volume`, `detected-fields`.
- Redirects every `logcli query` to `.tmp/loki-skill/<utc-timestamp>_<id>.log`.
- Caps output with `--limit=30` by default and `--since=15m`.
- Runs `timeout 30s logcli ...`.
- Applies the 50 KiB gate; larger output is sliced with `rg`, `jq`, or `rtk` equivalents.
- Normalizes `--from`/`--to` to UTC `Z` suffix and sets `--timezone=UTC`.

## What it produces
[ref: #loki-what-it-produces]

- Summaries of recent logs, errors, or event correlations.
- Temporary log files under `.tmp/loki-skill/` for evidence.
- Label/series exploration results.
- Ad-hoc metric query results.

## Dependencies and why they matter
[ref: #loki-dependencies-and-why-they-matter]

| Dependency | Why it matters |
|---|---|
| `logcli` | The actual Loki CLI client; without it no query can execute. |
| `frontmatter-protocol` | Routes the lazy-loaded reference corpus. |
| `mandatory-tools` | Forces modern tools (`rg`, `jq`, `rtk`) for slicing output instead of legacy `head`/`tail`. |

## Strengths and trade-offs
[ref: #loki-strengths-and-trade-offs]

- **Strong sides:** Prevents unbounded log dumps into context, blocks write/delete commands, and encodes Loki best practices (narrow selectors, line filters before parsers, UTC timestamps).
- **Weak sides / limits:** Requires `logcli` and `LOKI_ADDR`; `--tls-skip-verify` is the default and must be disabled manually if the environment requires verified TLS; `timeout` may not be installed on macOS by default.
- **Common pitfalls / gotchas:** Do not paste raw log output into the response. Do not use `--limit=0`. Do not pass `--org-id` unless `LOKI_ORG_ID` is set. For JSON logs, search `trace_id`/`event_id` via `| json | field="..."`, not `|=` on the raw JSON string.

## Repository layout
[ref: #loki-repository-layout]

```text
loki-skill/
├── references/
│   └── logql_and_logcli.md   # LogQL syntax, logcli flags, query patterns, troubleshooting
├── README.md                 # Human overview (this file)
└── SKILL.md                  # Agent entry point: commands, flags, workflows, and routing
```

## Reference overview
[ref: #loki-reference-overview]

| File | What it covers |
|---|---|
| `references/logql_and_logcli.md` | Stream selectors, line/label filters, parsers, format expressions, metric queries, logcli commands, connection/auth, output/time flags, query patterns, and troubleshooting. |

## Important conventions / gotchas
[ref: #loki-important-conventions-and-gotchas]

- Every query output goes to a file; stdout is never read into context directly.
- The 50 KiB gate is hard: larger files are re-fetched or sliced.
- `jsonl` output is allowed only for parsing with `jq` or similar tools.
- The agent does not handle basic auth or bearer tokens; auth failures are escalated to the user.
- Temporary files are not cleaned up automatically; delete them manually when they are no longer needed.
