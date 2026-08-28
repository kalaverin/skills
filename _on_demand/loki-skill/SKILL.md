---
name: loki-skill
description: "Query logs and service state in Grafana Loki via the logcli terminal client. Use for investigating service problems, exploring labels and series, and incident response. The agent is read-only: no mutations, no writes, no deletes."
triggers:
  request: "logcli, loki, grafana logs, посмотри логи, найди в логах, посмотри логи на стейдже, посмотри логи на проде, проверь в локи, посмотри в графане, расследование инцидентов, разбор инцидента, разбор проблем, sentry, логи sentry, incident"
  reason: "User needs to query logs or service state through Grafana Loki."
runtime: true
requires:
  - frontmatter-protocol
  - mandatory-tools
version: 0.1.0
---

# SKILL: Grafana Loki via logcli

[ref: #loki-skill-intro]

This skill governs how the agent uses the `logcli` command-line client to query Grafana Loki. The agent acts as a read-only investigator: it may query logs, labels, series, and read-only metadata, but it must never mutate Loki state, write data, or run destructive commands.

## 1. Reference corpus

[ref: #loki-reference-corpus]

The `references/` directory holds detailed reference material. Do not read the whole file; route through the lazy-load funnel in `frontmatter-protocol` `[ref: #lazy-load-routing]` from the skill directory:

1. Extract the subject map from `references/logql_and_logcli.md`.
2. Read its frontmatter `index` cards.
3. Load only the body sections whose cards match the current question.

File inventory:

- `references/logql_and_logcli.md` — LogQL syntax, `logcli` flags, query patterns, and troubleshooting; anchors `loki-ref-*`.

## 2. Allowed commands

[ref: #loki-allowed-commands]

The agent may use only these read-only `logcli` commands:

- `logcli query` — main command for log lines.
- `logcli instant-query` — evaluate a metric query at a single point in time.
- `logcli labels` — list available label names or values.
- `logcli series` — list series matching a selector.
- `logcli stats` — index statistics for a selector.
- `logcli volume` — aggregate log volume for a selector.
- `logcli detected-fields` — fields detected by parsers.

Any other subcommand is forbidden. The agent must never use `delete`, `push`, or any write-oriented command.

## 3. Connection and auth

[ref: #loki-connection-auth]

- `LOKI_ADDR` is read from the environment. If it is not set, the agent asks the user.
- The agent does not pass `--addr` on the command line.
- `--tls-skip-verify` is used by default.
- `--org-id` is never passed unless the `LOKI_ORG_ID` environment variable is set. The agent first tries the call without `--org-id`. If the gateway requires `X-Scope-OrgID` and returns 401/403, the agent asks the user to set `LOKI_ORG_ID` and retry.
- The agent does not handle basic auth, bearer tokens, or any other credentials. If Loki rejects the connection for authentication reasons, escalate to the user.
- No credentials, hostnames, org ids, or tenant names are hardcoded in examples or transcripts.

## 4. Hard parameter rules

[ref: #loki-hard-parameter-rules]

| Parameter | Rule |
|---|---|
| `--limit` | Always set. Never `0`. Default is `30`. Exploration: `10–50`. Deep investigation: `100–200`. Need more — ask the user. |
| `--since` | Prefer narrow windows: `5m`, `15m`, `1h`. |
| `--from` / `--to` | RFC3339Nano with explicit timezone suffix, always `Z` for UTC, e.g. `2026-08-18T10:00:00Z`. Combine with `--timezone=UTC`. |
| `--output` | Default is `raw`. `jsonl` is allowed only when the output is piped to `jq` or saved to a file for parsing. Avoid `jsonl` on huge ranges. |
| `--parallel-*` | Forbidden. Removed from the skill. |
| `--interval` | Forbidden. Removed from the skill. |
| `--tail` | Forbidden. Removed from the skill. |

## 5. Workflows

[ref: #loki-workflows]

### 5.1 Query recent logs

[ref: #loki-workflow-query-recent]

1. Create the output directory: `mkdir -p .tmp/loki-skill`.
2. Start narrow (do not pass `--org-id` unless `LOKI_ORG_ID` is set):
   ```bash
   timeout 30s logcli query \
     --tls-skip-verify --timezone=UTC --since=15m --output=raw --quiet --limit=30 \
     '{app="example", env="dev"}' \
     > ".tmp/loki-skill/$(date -u +%Y%m%dT%H%M%S)_$$.log"
   ```
3. Adjust `--since` and `--limit` based on results.
4. Add a LogQL filter: `... '{app="example", env="dev"} |= "error"'`.
5. Summarize findings; do not paste raw output into the response.

### 5.2 Explore labels and series

[ref: #loki-workflow-explore]

1. List labels: `logcli labels`.
2. List values for a label: `logcli labels <label_name>`.
3. List series for a selector: `logcli series '{app="example"}'`.
4. Use tight selectors and narrow time windows; ask before broad selectors.

### 5.3 Deep investigation

[ref: #loki-workflow-deep]

1. Start from a known anchor: trace id, request id, error message, or Sentry event id.
2. Query with a tight filter on that anchor.
3. Widen time window only if the anchor is not found.
4. Cross-reference with related services only after the first hit.

## 6. Context protection

[ref: #loki-context-protection]

1. **Create the output directory.** Run `mkdir -p .tmp/loki-skill` before the first query.
2. **Every query goes to a file.** The agent always redirects `logcli query` output to a temporary file under `.tmp/loki-skill/<utc-timestamp>_<short-query-id>.log`. Stdout is never read into context directly.
3. **Size gate: 50 KiB.** Check the file size with `rtk wc -c <path>`. If the file is 50 KiB or less, read and summarize it. If it is larger, either re-fetch with a narrower query, or slice the file with `rg`, `jq`, or `rtk` equivalents.
4. **Start narrow.** First query uses `--since=15m --limit=30`, or an exact event-based query such as a trace id or Sentry event id.
5. **Filter first.** Always apply a LogQL filter (`|=`, `|~`, `!=`, `!~`) before broadening the query.
6. **Output format.** Default is `raw`. Use `jsonl` only when the output is piped to a parser.
7. **Abort on hang.** Run `timeout 30s logcli ...`. On timeout, suggest narrowing the query.
8. **All bulk-producing commands go to a file.** Apply the temporary-file, timeout, and size-gate rules to `logcli query`, `instant-query`, `stats`, `volume`, and `detected-fields`.
9. **No credentials in examples.** Mask hosts, org ids, and tenant names in transcripts and summaries.

## 7. Pipeline

[ref: #loki-pipeline]

Forward flow:

1. User mentions `logcli`, Loki, Grafana logs, looking at logs on stage/prod, checking Loki, investigating an incident, or Sentry problem analysis.
2. Runtime trigger activates `loki-skill`; the agent reads `SKILL.md`.
3. Agent detects intent: query recent logs, explore labels/series, deep investigation, or event-based query.
4. Agent checks environment: `LOKI_ADDR`, org id.
5. Agent builds command from allowed commands, connection flags, hard parameter rules, and context protection rules.
6. Agent executes `timeout 30s logcli ... > .tmp/loki-skill/...`.
7. Agent applies the 50 KiB size gate.
8. Agent summarizes and responds.

Error routes:

- Missing `LOKI_ADDR` → ask the user.
- Gateway requires org id → ask the user to set `LOKI_ORG_ID` and retry.
- Loki requires authentication (basic auth, bearer token, etc.) → escalate to the user.
- `logcli: command not found` → hard stop; ask the user to install `logcli`.
- Timeout → suggest narrowing.
- Output > 50 KiB → re-fetch or slice with `rg`, `jq`, or `rtk` equivalents.
- No results → suggest widening the window or changing the filter.

## 8. Violation protocol

[ref: #loki-violation-protocol]

If the agent is about to run a forbidden command, omit `--limit`, use `--limit=0`, pull raw multi-line logs into the response, or bypass the temporary-file rule: stop, discard the command, and rebuild it according to this skill.
