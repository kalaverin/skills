---
name: loki-skill
description: "Query logs and service state in Grafana Loki via the logcli terminal client. Use for investigating service problems, exploring labels and series, and incident response. The agent is read-only: no mutations, no writes, no deletes."
triggers:
  request: "logcli, loki, grafana logs, посмотри логи, найди в логах, посмотри логи на стейдже, посмотри логи на проде, проверь в локи, посмотри в графане, расследование инцидентов, разбор инцидента, разбор проблем, sentry, логи sentry, incident"
  reason: "User needs to query logs or service state through Grafana Loki."
runtime: true
requires:
  - mandatory-tools
version: 0.3.0
---

# SKILL: Grafana Loki via logcli

[ref: #loki-skill-intro]

This skill governs how the agent uses the `logcli` command-line client to query Grafana Loki. The agent acts as a read-only investigator: it may query logs, labels, series, and read-only metadata, but it must never mutate Loki state, write data, or run destructive commands. The skill is atomic: everything — rules, workflows, and the LogQL/logcli reference — lives in this file.

## 1. Allowed commands

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

## 2. Connection and auth

[ref: #loki-connection-auth]

- `LOKI_ADDR` is read from the environment. If it is not set, the agent asks the user.
- The agent does not pass `--addr` on the command line.
- `--tls-skip-verify` is used by default (§16 documents the internal-CA symptom it solves).
- **Project default org (HARD):** `LOKI_ORG_ID` MUST hold the project's default tenant. If `LOKI_ORG_ID` is empty, the agent STOPS before the first query and asks the user to set the project's default org. One Loki endpoint commonly serves several tenants per business scope, so an unset org silently queries the wrong tenant or fails with 401/403.
- **Non-default scope (HARD):** when the investigation targets a scope outside the project's default org, the agent passes `--org-id` explicitly on those queries (flags override the environment) and states which org was used in the summary.
- The agent does not handle basic auth, bearer tokens, or any other credentials. If Loki rejects the connection for authentication reasons, escalate to the user.
- No credentials, hostnames, org ids, or tenant names are hardcoded in examples or transcripts.

## 3. Hard parameter rules

[ref: #loki-hard-parameter-rules]

| Parameter | Rule |
|---|---|
| `--limit` | Always set. Never `0`. Default is `30`. Exploration: `10–50`. Deep investigation: `100–200`. Need more — ask the user. |
| `--since` | Prefer narrow windows: `5m`, `15m`, `1h`. |
| `--from` / `--to` | RFC3339Nano with explicit timezone suffix, always `Z` for UTC, e.g. `2026-08-18T10:00:00Z`. Combine with `--timezone=UTC`. |
| `--output` | Always `jsonl`, always paired with `--output-timestamp-format=rfc3339nano`, and always piped through `unjsonl` before the output reaches a file or the context. `raw` is forbidden. |
| `--parallel-*` | Forbidden. Removed from the skill. |
| `--interval` | Forbidden. Removed from the skill. |
| `--tail` | Forbidden. Removed from the skill. |

## 4. Workflows

[ref: #loki-workflows]

### 4.1 Query recent logs

[ref: #loki-workflow-query-recent]

1. Create the output directory: `mkdir -p .tmp/loki-skill`.
2. Start narrow (the default org comes from `LOKI_ORG_ID`; pass `--org-id` only for a non-default scope):
   ```bash
   timeout 30s logcli query \
     --tls-skip-verify --timezone=UTC --since=15m --output=jsonl \
     --output-timestamp-format=rfc3339nano --quiet --limit=30 \
     '{app="example", env="dev"}' \
     | unjsonl > ".tmp/loki-skill/$(date -u +%Y%m%dT%H%M%S)_$$.log"
   ```
3. Adjust `--since` and `--limit` based on results.
4. Add a LogQL filter: `... '{app="example", env="dev"} |= "error"'`.
5. Summarize findings; do not paste raw output into the response.

### 4.2 Explore labels and series

[ref: #loki-workflow-explore]

1. List labels: `logcli labels`.
2. List values for a label: `logcli labels <label_name>`.
3. List series for a selector: `logcli series '{app="example"}'`.
4. Use tight selectors and narrow time windows; ask before broad selectors.

### 4.3 Deep investigation

[ref: #loki-workflow-deep]

1. Start from a known anchor: trace id, request id, error message, or Sentry event id.
2. Query with a tight filter on that anchor.
3. Widen time window only if the anchor is not found.
4. Cross-reference with related services only after the first hit.

## 5. Context protection

[ref: #loki-context-protection]

1. **Create the output directory.** Run `mkdir -p .tmp/loki-skill` before the first query.
2. **Every query goes to a file.** The agent always pipes `logcli query` output through `unjsonl` into a temporary file under `.tmp/loki-skill/<utc-timestamp>_<short-query-id>.log`. Stdout is never read into context directly.
3. **Size gate: 50 KiB.** Check the file size with `rtk wc -c <path>`. If the file is 50 KiB or less, read and summarize it. If it is larger, either re-fetch with a narrower query, or slice the file with `rg`, `jq`, or `rtk` equivalents.
4. **Start narrow.** First query uses `--since=15m --limit=30`, or an exact event-based query such as a trace id or Sentry event id.
5. **Filter first.** Always apply a LogQL filter (`|=`, `|~`, `!=`, `!~`) before broadening the query.
6. **Output format.** Always `--output=jsonl` with `--output-timestamp-format=rfc3339nano`, piped through `unjsonl`. Raw jsonl never enters the context unprocessed.
7. **Abort on hang.** Run `timeout 30s logcli ...`. On timeout, suggest narrowing the query.
8. **All bulk-producing commands go to a file.** Apply the temporary-file, timeout, and size-gate rules to `logcli query`, `instant-query`, `stats`, `volume`, and `detected-fields`.
9. **No credentials in examples.** Mask hosts, org ids, and tenant names in transcripts and summaries.

## 6. Pipeline

[ref: #loki-pipeline]

Forward flow:

1. User mentions `logcli`, Loki, Grafana logs, looking at logs on stage/prod, checking Loki, investigating an incident, or Sentry problem analysis.
2. Runtime trigger activates `loki-skill`; the agent reads `SKILL.md`.
3. Agent detects intent: query recent logs, explore labels/series, deep investigation, or event-based query.
4. Agent checks environment: `LOKI_ADDR`, `LOKI_ORG_ID` (project default org).
5. Agent builds command from allowed commands, connection flags, hard parameter rules, and context protection rules.
6. Agent executes `timeout 30s logcli ... --output=jsonl --output-timestamp-format=rfc3339nano ... | unjsonl > .tmp/loki-skill/...`.
7. Agent applies the 50 KiB size gate.
8. Agent summarizes and responds.

Error routes:

- Missing `LOKI_ADDR` → ask the user.
- Missing `LOKI_ORG_ID` → ask the user to set the project's default org before any query.
- Investigation targets a non-default scope → pass `--org-id` explicitly and name the org in the summary.
- Loki requires authentication (basic auth, bearer token, etc.) → escalate to the user.
- `logcli: command not found` → hard stop; ask the user to install `logcli` (prefer the Homebrew build on macOS).
- `unjsonl: command not found` → hard stop; ask the user to install `unjsonl`.
- Timeout → suggest narrowing.
- Output > 50 KiB → re-fetch or slice with `rg`, `jq`, or `rtk` equivalents.
- No results → suggest widening the window or changing the filter.

## 7. Violation protocol

[ref: #loki-violation-protocol]

If the agent is about to run a forbidden command, omit `--limit`, use `--limit=0`, pull raw multi-line logs into the response, or bypass the temporary-file rule: stop, discard the command, and rebuild it according to this skill.

## 8. Loki architecture

[ref: #loki-ref-architecture]

Loki is a horizontally scalable log aggregation system inspired by Prometheus. It groups incoming log lines into streams identified by a unique set of labels. Loki indexes only the label set and the timestamp; the full log line is compressed and stored in chunks inside an object store such as S3, GCS, or Azure Blob Storage.

Key components:

- **Distributor** receives push requests and hashes streams to ingesters.
- **Ingester** buffers streams in memory and writes chunks to storage.
- **Query frontend** splits queries and merges results.
- **Querier** fetches data from ingesters and object storage.
- **Ruler** evaluates alerting and recording rules.

Storage format:

- **Index** is a table of contents mapping label sets to chunks. TSDB is the recommended index format.
- **Chunk** contains log entries for one stream over a time range, compressed.

Multi-tenancy:

- Loki partitions data by tenant id.
- The `X-Scope-OrgID` header carries the tenant.
- Single-tenant deployments ignore the header and use tenant id `fake`.

Because only labels are indexed, query performance depends heavily on choosing low-cardinality, high-selectivity labels in the stream selector.

## 9. Labels and streams

[ref: #loki-ref-labels-streams]

A **log stream** is the set of log lines that share exactly the same label set. Loki stores one chunk per stream per time window, so the number of streams directly impacts storage efficiency and query speed.

Good labels are static and bounded:

- `namespace`, `app`, `service_name`, `env`, `cluster`, `host`.

Bad labels are dynamic or unbounded:

- `trace_id`, `request_id`, `user_id`, `order_id`.

Cardinality guidance:

- Keep a single tenant under roughly 100,000 active streams.
- Prefer fewer streams with larger chunks over many streams with tiny chunks.
- Use line filters such as `|= "trace_id=abc"` for high-cardinality values only when the raw line literally contains that form (for example logfmt). For JSON logs parse first: `{app="api"} | json | trace_id="abc"`.

Structured metadata allows attaching non-indexed key-value pairs to log lines at ingestion time. These values can be extracted at query time with parsers but do not explode the index.

## 10. LogQL syntax overview

[ref: #loki-ref-logql-syntax]

Every LogQL query has the form:

```logql
{ log stream selector } | pipeline stage | pipeline stage | ...
```

The log stream selector is mandatory. The pipeline is optional.

Pipeline stages are evaluated left to right:

1. **Line filters** narrow by substring or regex in the raw line.
2. **Parsers** extract structured fields as labels.
3. **Label filters** filter on extracted or existing labels.
4. **Format expressions** reshape output for display.

A query can end as a log query, returning lines, or as a metric query, wrapping the pipeline in a range vector and aggregation function.

Examples:

```logql
{app="api", env="prod"} |= "error"
{app="api"} | json | status >= 500
{app="api"} | json | line_format "{{.method}} {{.path}} -> {{.status}}"
```

## 11. Stream selectors

[ref: #loki-ref-stream-selectors]

The stream selector chooses which log streams to process. It uses label matchers inside curly braces.

Operators:

- `=` exact equality.
- `!=` inequality.
- `=~` regex match.
- `!~` negative regex match.

Multiple matchers inside one selector are AND-ed together.

Examples:

```logql
{app="billing", env="prod"}
{namespace=~"team-.*", service_name="wallet"}
{app!="debug-app"}
```

Best practice: use the most specific label first. If `app_name` selects a smaller subset than `namespace`, prefer `{app_name="wallet"}` alone.

## 12. Line filters

[ref: #loki-ref-line-filters]

Line filters operate on the raw log line text. They are the cheapest filter type and should be placed as early as possible.

Operators:

- `|=` line contains string.
- `!=` line does not contain string.
- `|~` line matches regex.
- `!~` line does not match regex.

Performance order:

1. `|=` and `!=` are fastest.
2. `|~` and `!~` are slower.
3. Parsers are slower than line filters.

Examples:

```logql
{app="api"} |= "timeout"
{app="api"} != "healthcheck"
{app="api"} |~ "(error|fatal)"
```

Pattern match filters `|>` and `!>` (Loki 3.x+) match the whole line against a pattern where `<_>` matches arbitrary text. They are faster than regex for lines with a predictable shape. Do not confuse them with the `| pattern` parser.

```logql
{app="api"} |> "<_> level=error <_>"
```

## 13. Label filters

[ref: #loki-ref-label-filters]

Label filters operate on labels that already exist or were extracted by a parser. They are written after parsers or directly after the selector.

Operators:

- `==` or `=` equality.
- `!=` inequality.
- `>`, `>=`, `<`, `<=` numeric comparison.
- `and` and `or` boolean chaining.

Examples:

```logql
{app="api"} | json | status >= 500
{app="api"} | json | method="POST" and status >= 400
{app="api"} | logfmt | duration > 1.5
```

Pipeline errors from parsers produce a system label `__error__`. Filter it explicitly:

```logql
{app="api"} | json | __error__=""
```

## 14. Parsers

[ref: #loki-ref-parsers]

Parsers extract structured data from log lines and create temporary labels for the rest of the pipeline.

Available parsers:

- `json` parses JSON log lines.
- `logfmt` parses `key=value` or `key="value"` pairs.
- `pattern` extracts fields via a lightweight wildcard pattern.
- `regexp` extracts fields via a regular expression with named capture groups.
- `unpack` extracts labels from structured metadata in the log line.

JSON parser examples:

```logql
{app="api"} | json
{app="api"} | json | status="500"
{app="api"} | json method, status
```

The last example extracts only `method` and `status` as labels. The parser also supports explicit mappings such as `json method="http_method", status="http_status"`.

Logfmt parser example:

```logql
{app="api"} | logfmt | level="error"
```

Pattern parser example:

```logql
{app="api"} | pattern "<_> caller=<caller> level=<level> msg=<msg>"
```

Regexp parser example:

```logql
{app="api"} | regexp "(?P<method>\w+) (?P<path>\S+) HTTP/(?P<version>\d\.\d)"
```

Use a single backslash inside the regex; LogQL passes it directly to the Go regex engine.

Parser errors populate `__error__`. Always handle errors when parser reliability is uncertain.

## 15. Format expressions

[ref: #loki-ref-format-expressions]

Format expressions change how results are displayed. They do not modify stored data.

`line_format` rewrites the log line using Go templates:

```logql
{app="api"} | json | line_format "{{.method}} {{.path}} -> {{.status}}"
```

`label_format` creates or rewrites labels:

```logql
{app="api"} | json | label_format severity="{{.level | upper}}"
```

Common template helpers include `upper`, `lower`, and `trim`. Keep formatting late in the pipeline, after all filtering and parsing.

## 16. Metric queries

[ref: #loki-ref-metric-queries]

Metric queries convert log streams into numeric time series. They wrap a log pipeline in a range vector `[duration]` and apply an aggregation function.

Common functions:

- `rate({selector} |= "error" [1m])` entries per second.
- `count_over_time({selector} [5m])` total entries in range.
- `sum by (status) (rate({selector} | json | status >= 500 [5m]))` grouped error rate.
- `quantile_over_time(0.99, {selector} | json | unwrap latency_ms [5m])` percentile.

Range vector durations:

- Use `[1m]`, `[5m]`, `[1h]` depending on granularity.
- The range must be longer than or equal to the query step.
- Always pass `--step` explicitly when running metric queries with `logcli` to control sampling density and server load.

Aggregation modifiers:

- `by (label1, label2)` keeps listed labels in result.
- `without (label1)` drops listed labels from result.

Binary operators (`+`, `-`, `*`, `/`, `%`, `^`) and comparison operators (`==`, `!=`, `>`, `<`) work on vectors and scalars. Use `bool` after comparison to keep zeros and ones instead of filtering.

## 17. logcli commands reference

[ref: #loki-ref-logcli-commands]

`logcli` is the command-line client for Loki. Read-only commands useful for agent work:

- `logcli query <logql>` returns log lines or metric results.
- `logcli instant-query <logql>` evaluates a metric query at a single point in time.
- `logcli labels [label]` lists label names or values.
- `logcli series <matcher>` lists streams matching a selector.
- `logcli stats <query>` returns index statistics for a selector.
- `logcli volume <query>` returns aggregate log volume for a selector.
- `logcli detected-fields <query>` reports fields detected by parsers.

Forbidden commands for read-only agent use:

- `delete` and all its subcommands.
- Any write, push, or ingest operation.

## 18. Connection reference

[ref: #loki-ref-logcli-connection]

Connection settings can come from environment variables or command-line flags. Command-line flags override environment variables; environment variables provide defaults.

Important environment variables and flags:

- `LOKI_ADDR` / `--addr` — Loki server URL.
- `LOKI_ORG_ID` / `--org-id` — tenant id added as `X-Scope-OrgID`.
- `LOKI_USERNAME` / `--username` and `LOKI_PASSWORD` / `--password` — HTTP basic auth.
- `LOKI_BEARER_TOKEN` / `--bearer-token` — bearer token for Authorization header.
- `LOKI_TLS_SKIP_VERIFY` / `--tls-skip-verify` — skip TLS verification.
- `LOKI_CA_CERT_PATH` / `--ca-cert` — custom CA certificate.
- `LOKI_CLIENT_CERT_PATH` / `--cert` and `LOKI_CLIENT_KEY_PATH` / `--key` — mutual TLS.

One endpoint frequently serves several business scopes as different tenants (for example `loki-gw.prod.internal.example-corp.net` with org id `10` for custodial wallet logs and `30` for payment-core logs, the dev gateway carrying its own id). The prescriptive rules live in §2.

## 19. Output and time flags reference

[ref: #loki-ref-logcli-output-time]

Output flags:

- `-o default` / `--output=default` — timestamp, labels, and line.
- `-o raw` / `--output=raw` — line content only (forbidden for agent use, see §3).
- `-o jsonl` / `--output=jsonl` — one JSON object per returned log line with `labels`, `line`, and `timestamp` fields.
- `--output-timestamp-format=rfc3339nano` — nanosecond RFC3339 timestamps.
- `--timezone=UTC` — format timestamps in UTC.
- `-q` / `--quiet` — suppress query metadata.

Time flags:

- `--since=15m` — relative lookback window.
- `--from=2026-08-18T10:00:00Z` — absolute start, RFC3339Nano with explicit `Z` UTC suffix.
- `--to=2026-08-18T11:00:00Z` — absolute end, RFC3339Nano with explicit `Z` UTC suffix.
- `--timezone=UTC` — format output timestamps in UTC and interpret bounds without an offset as UTC.

Limit flag:

- `--limit=30` — cap returned entries. Never set to `0`.

Agent defaults:

- `--output=jsonl --output-timestamp-format=rfc3339nano --quiet --timezone=UTC --limit=30 --since=15m`, piped through `unjsonl` before the output reaches a file or the context.

## 20. Query patterns

[ref: #loki-ref-query-patterns]

All bash examples below are simplified. In agent use, wrap every `logcli query` in `timeout 30s`, pipe output through `unjsonl` into `.tmp/loki-skill/<timestamp>_<id>.log`, and apply the 50 KiB size gate.

Internal label convention: selectors are typically `{namespace=..., service_name=...}` where `service_name` is the workload name.

### Recent errors for a service

```bash
mkdir -p .tmp/loki-skill
timeout 30s logcli query \
  --tls-skip-verify --timezone=UTC --since=15m --output=jsonl \
  --output-timestamp-format=rfc3339nano --quiet --limit=30 \
  '{app="billing", env="prod"} |= "error"' \
  | unjsonl > ".tmp/loki-skill/$(date -u +%Y%m%dT%H%M%S)_$$.log"
```

### Trace id search

For logfmt or literal `trace_id=...` lines:

```bash
timeout 30s logcli query --tls-skip-verify --timezone=UTC --since=1h --output=jsonl \
  --output-timestamp-format=rfc3339nano --quiet --limit=100 \
  '{app=~"api|worker"} |= "trace_id=7a98025445386b1feef1402bb13362e5"' | unjsonl
```

For JSON logs use a parser:

```logql
{app=~"api|worker"} | json | trace_id="7a98025445386b1feef1402bb13362e5"
```

### HTTP 5xx with JSON logs

```logql
{app="api"} | json | status >= 500
```

### Error rate per service

```logql
sum by (app) (rate({app=~"api|worker"} |= "error" [5m]))
```

For `logcli`, add `--step=1m` (or smaller than the range) when running metric queries.

### Sentry event correlation

Given a Sentry event id, search raw logs for that literal token only if the line contains it literally:

```logql
{app=~"api|worker"} |= "event_id=6d9ab75c00ac479f98a629f07ad253e7"
```

For JSON logs parse the field first:

```logql
{app=~"api|worker"} | json | event_id="6d9ab75c00ac479f98a629f07ad253e7"
```

### Business identifier search

Three canonical anchors inside one service: URL path, workflow/trace UUID, business `key=value` parameter (identifiers below are fictional):

```logql
{namespace="payments", service_name="gateway-api"} |= "/api/v2/webhook"
{namespace="payments", service_name="gateway-api"} |= "a1b2c3d4-1111-4222-8333-abcdef012345"
{namespace="payments", service_name="gateway-api"} |= "client_id=42"
```

## 21. Troubleshooting

[ref: #loki-ref-troubleshooting]

| Symptom | Likely cause | Remedy |
|---|---|---|
| Empty results | Time range too narrow or selector too strict | Widen `--since`, relax selectors, check labels with `logcli labels`. |
| Timeout or slow query | Time range too wide, low-selectivity selector, or heavy parser | Narrow time, add <code>&#124;=</code> filter first, avoid regex. |
| 401/403 | `LOKI_ORG_ID` unset or wrong tenant for the scope | Set `LOKI_ORG_ID` to the project default org; pass explicit `--org-id` for non-default scopes. |
| macOS cannot resolve an internal host (`*.internal.*`) | `mise`-installed `logcli` is built with the `netgo` tag and bypasses the macOS system resolver | Use the Homebrew build (`/opt/homebrew/bin/logcli --version`) or another cgo-resolver build. |
| `tls: failed to verify certificate: ... not standards compliant` | Go rejects some internal CA certificates as non-compliant | Keep `--tls-skip-verify`; it is the intended default, not a misconfiguration. |
| `unjsonl: command not found` | `unjsonl` missing from PATH | Hard stop; ask the user to install `unjsonl`. |
| `__error__` labels | Parser failed on some lines | Add <code>&#124; __error__=""</code> or <code>&#124; __error__!=""</code> depending on intent. |
| Huge output file | No filter or `--limit=0` | Refetch with filter and limit; slice with `rg`, `jq`, or `rtk` equivalents. |
| Out-of-order lines with parallel flags | `--parallel-*` splits range into parts | Avoid parallel flags; use narrow sequential queries. |
