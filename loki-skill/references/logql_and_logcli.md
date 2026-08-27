---
subject: "LogQL query syntax and `logcli` invocation rules for Grafana Loki; covers stream selectors, line filters, label filters, parsers, formatters, metric queries, aggregation functions, connection flags, output modes, label cardinality, storage architecture, and troubleshooting common errors."
index:
  - anchor: loki-ref-architecture
    what: "Reference section describing Loki distributed architecture, storage layout with index and chunks, write path, read path, and multi-tenancy model."
    problem: "Agent needs background on how Loki stores and retrieves logs; missing mental model leads to slow queries, wrong assumptions about indexing, and confusion over tenant isolation; architecture, storage, chunks, index, streams, tenants."
    use_when: "Reasoning about query performance, explaining why labels matter, or diagnosing storage-level behavior."
    avoid_when: "Only constructing a simple LogQL filter without needing internals."
    expected: "Agent understands index-only-labels, chunk-based storage, and tenant isolation via `X-Scope-OrgID`."
  - anchor: loki-ref-labels-streams
    what: "Reference section defining labels, log streams, cardinality, structured metadata, and label best practices for efficient queries."
    problem: "Agent must decide whether values belong in labels or line filters; poor label hygiene causes excessive stream counts, tiny chunks, and slow queries across cluster; cardinality, streams, labels, metadata extraction, bounded values."
    use_when: "Designing selectors, advising on label usage, or diagnosing cardinality-related slowdowns."
    avoid_when: "Querying logs from a system where label schema is already fixed and correct."
    expected: "Agent picks low-cardinality static labels for selectors and defers high-cardinality values to line filters."
  - anchor: loki-ref-logql-syntax
    what: "Reference section introducing LogQL query structure: mandatory log stream selector plus optional pipeline of filters, parsers, and formatters."
    problem: "Agent needs to compose valid LogQL for every investigation; malformed selector or wrong pipeline order produces empty results, parser errors, wasted round trips, and operator misuse; query syntax, pipeline, selector, LogQL, stages."
    use_when: "Writing or reviewing any LogQL query."
    avoid_when: "Only looking up a specific function signature."
    expected: "Agent produces syntactically valid `{selector} | stage | stage` queries."
  - anchor: loki-ref-stream-selectors
    what: "Reference section listing label matcher operators `=`, `!=`, `=~`, `!~` and rules for combining multiple matchers."
    problem: "Agent must narrow log streams precisely before applying filters; wrong selector operator or matcher combination returns too many streams, none at all, or silently wrong data for label sets; equality, regex, exclusion, operators, combinations, constraints."
    use_when: "Picking streams by application, environment, namespace, or other static labels."
    avoid_when: "Filtering log line content; line filters handle that case."
    expected: "Agent writes exact or regex label selectors without escaping mistakes."
  - anchor: loki-ref-line-filters
    what: "Reference section detailing line filter operators `|=`, `!=`, `|~`, `!~` and their performance ordering relative to parsers."
    problem: "Agent needs substring or regex filtering inside raw log lines; incorrect operator choice or pipeline placement degrades query performance and returns irrelevant or misleading rows during investigation; contains, regex, exclusion, brute force, placement, ordering."
    use_when: "Searching for error strings, trace ids, request paths, or other inline tokens."
    avoid_when: "Filtering on structured fields already extracted as labels."
    expected: "Agent prefers `|=` and `!=` over regex and places filters before parsers."
  - anchor: loki-ref-label-filters
    what: "Reference section covering label filter operators `==`, `!=`, `>`, `>=`, `<`, `<=`, plus `and`/`or` chaining and `__error__` handling."
    problem: "Agent must filter on extracted or existing labels numerically or logically; wrong operator precedence or comparison type yields incorrect or misleading results and hides matching events from analysis; number filters, boolean logic, pipeline errors, precedence."
    use_when: "Filtering parsed JSON fields, logfmt keys, or metadata labels by value."
    avoid_when: "Only matching raw substrings in log text; line filters are faster."
    expected: "Agent writes correct label comparisons and chains them with `and`/`or`."
  - anchor: loki-ref-parsers
    what: "Reference section explaining `json`, `logfmt`, `pattern`, `regexp`, and `unpack` parsers and when each is appropriate."
    problem: "Agent needs to extract fields from structured or semi-structured log lines; parser choice affects query speed, memory use, and correctness of downstream filters and output shape; json, logfmt, pattern, regexp, unpack, structured parsing."
    use_when: "Logs contain JSON, key=value pairs, predictable patterns, or structured metadata that needs extraction."
    avoid_when: "Simple substring search suffices without structured field retrieval."
    expected: "Agent selects parser matching log shape and handles parser errors via `__error__`."
  - anchor: loki-ref-format-expressions
    what: "Reference section for `line_format` and `label_format` template functions that reshape output without changing stored data."
    problem: "Agent must reshape displayed log lines or synthesize temporary labels for readable summaries; template mistakes produce unreadable output and break downstream filters and temporary fields; display formatting, Go templates, output rewriting, presentation."
    use_when: "Formatting log lines for summaries, correlating fields, or creating temporary display labels."
    avoid_when: "Filtering or aggregating data; formatting is purely presentational."
    expected: "Agent uses Go-template syntax correctly inside `line_format` and `label_format`."
  - anchor: loki-ref-metric-queries
    what: "Reference section describing metric queries built from log ranges, aggregation functions such as `rate`, `count_over_time`, `sum`, `avg`, and `quantile_over_time`."
    problem: "Agent must turn log streams into numeric time series for dashboards or alerts; wrong range duration, aggregation function, or grouping yields misleading counts and hidden spikes across services; range vectors, aggregation, quantiles, grouping, histograms."
    use_when: "Counting errors per minute, computing latency percentiles, or building ad-hoc dashboards from logs."
    avoid_when: "Retrieving raw log lines; metric queries return matrices, not text."
    expected: "Agent writes valid range-vector expressions and groups results with `by` or `without`."
  - anchor: loki-ref-logcli-commands
    what: "Reference section enumerating `logcli` subcommands `query`, `instant-query`, `labels`, `series`, `stats`, `volume`, and read-only use cases."
    problem: "Agent must map each investigation goal to correct `logcli` subcommand; choosing `query` for label enumeration or `series` for raw log lines returns unusable output and wastes round trips; command selection, subcommands, CLI verbs, read-only verbs."
    use_when: "Deciding which `logcli` subcommand matches the investigation goal."
    avoid_when: "Only looking up flag syntax for a command already chosen."
    expected: "Agent maps task to `query`, `labels`, `series`, or other read-only command."
  - anchor: loki-ref-logcli-connection
    what: "Reference section covering `LOKI_ADDR`, `--tls-skip-verify`, `--org-id`, basic auth, bearer tokens, and tenant header behavior."
    problem: "Agent must reach Loki instance and identify correct tenant before every query; missing address, wrong tenant identifier, or leaked secrets produce connection failures, security incidents, and credential hygiene problems; authentication, tenant, TLS, credentials, gateway."
    use_when: "Constructing any `logcli` invocation that touches a Loki instance."
    avoid_when: "Internal documentation about LogQL syntax unrelated to CLI invocation."
    expected: "Agent passes connection flags without exposing secrets and handles unknown tenant gracefully."
  - anchor: loki-ref-logcli-output-time
    what: "Reference section detailing `--output`, `--output-timestamp-format`, `--timezone`, `--since`, `--from`, `--to`, `--limit`, and `--quiet`."
    problem: "Agent must control how `logcli` renders rows and which interval it scans for each request; wrong rendering mode or timestamp bounds return unreadable rows or flood context with data; rendering, timestamps, intervals, caps, formatting."
    use_when: "Formatting `logcli` output or narrowing the queried time range."
    avoid_when: "Writing LogQL queries for Grafana Explore instead of CLI."
    expected: "Agent selects appropriate rendering mode and caps the queried UTC window."
  - anchor: loki-ref-query-patterns
    what: "Reference section providing reusable query recipes for sudden error surges, trace id search, Sentry event correlation, and namespace filtering."
    problem: "Agent repeatedly reconstructs common investigation shapes from scratch during active incidents; ad-hoc queries ignore best practices and return noisy or incomplete result sets and wasted effort; recipes, incidents, trace correlation, failure bursts, investigation templates."
    use_when: "Starting an incident investigation or correlating logs with an external signal."
    avoid_when: "Exploring unknown label schema; use `labels` command first."
    expected: "Agent adapts a known-safe query pattern to the concrete incident."
  - anchor: loki-ref-troubleshooting
    what: "Reference section cataloging common failures such as timeouts, 401/403 tenant issues, absence of matching lines, parser errors, and oversized output."
    problem: "Agent hits opaque `logcli` failures and wastes time guessing instead of diagnosing root cause; systematic symptom-to-cause mapping shortens incident response and prevents repeated mistakes across outages; errors, timeouts, auth failures, no-match cases."
    use_when: "A `logcli` call returns an error, no results, or unexpected volume."
    avoid_when: "Query succeeds and only interpretation of log content is needed."
    expected: "Agent maps symptom to cause and applies narrow time, better filter, correct org id, or parser error handling."
---

# LogQL and logcli reference

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

## Labels and streams

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

## LogQL syntax overview

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

## Stream selectors

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

## Line filters

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

## Label filters

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

## Parsers

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

## Format expressions

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

## Metric queries

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

## logcli commands

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

## logcli connection and authentication

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

Agent rule:

- Prefer `LOKI_ADDR` from environment.
- Use `--tls-skip-verify` by default.
- Pass `--org-id` explicitly only when `LOKI_ORG_ID` is set; otherwise try without it first. If the gateway returns 401/403, ask the user to set `LOKI_ORG_ID` and retry.
- The agent does not handle basic auth, bearer tokens, or any other credentials. If Loki rejects the connection for authentication reasons, escalate to the user.
- Never expose credentials in examples or transcripts.

## logcli output and time flags

[ref: #loki-ref-logcli-output-time]

Output flags:

- `-o default` / `--output=default` — timestamp, labels, and line.
- `-o raw` / `--output=raw` — line content only.
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

- `--output=raw --quiet --timezone=UTC --limit=30 --since=15m`.

## Query patterns

[ref: #loki-ref-query-patterns]

All bash examples below are simplified. In agent use, wrap every `logcli query` in `timeout 30s`, redirect output to `.tmp/loki-skill/<timestamp>_<id>.log`, and apply the 50 KiB size gate.

### Recent errors for a service

```bash
mkdir -p .tmp/loki-skill
timeout 30s logcli query \
  --tls-skip-verify --timezone=UTC --since=15m --output=raw --quiet --limit=30 \
  '{app="billing", env="prod"} |= "error"' \
  > ".tmp/loki-skill/$(date -u +%Y%m%dT%H%M%S)_$$.log"
```

### Trace id search

For logfmt or literal `trace_id=...` lines:

```bash
timeout 30s logcli query --tls-skip-verify --timezone=UTC --since=1h --output=raw --quiet --limit=100 \
  '{app=~"api|worker"} |= "trace_id=7a98025445386b1feef1402bb13362e5"'
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

## Troubleshooting

[ref: #loki-ref-troubleshooting]

| Symptom | Likely cause | Remedy |
|---|---|---|
| Empty results | Time range too narrow or selector too strict | Widen `--since`, relax selectors, check labels with `logcli labels`. |
| Timeout or slow query | Time range too wide, low-selectivity selector, or heavy parser | Narrow time, add <code>&#124;=</code> filter first, avoid regex. |
| 401/403 | Missing or wrong `--org-id` | Try without `--org-id`; if it fails, ask user to set `LOKI_ORG_ID`. |
| `__error__` labels | Parser failed on some lines | Add <code>&#124; __error__=""</code> or <code>&#124; __error__!=""</code> depending on intent. |
| Huge output file | No filter or `--limit=0` | Refetch with filter and limit; slice with `rg`, `jq`, or `rtk` equivalents. |
| Labels missing in output | `--output=raw` strips labels | Use `default` output or include labels explicitly. |
| Out-of-order lines with parallel flags | `--parallel-*` splits range into parts | Avoid parallel flags; use narrow sequential queries. |
