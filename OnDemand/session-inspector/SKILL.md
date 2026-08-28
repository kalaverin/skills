---
name: session-inspector
description: "Token-cheap inspection of Kimi Code CLI session files under ~/.kimi/sessions. Use when the user asks to find, list, or identify past sessions — or to restore working context from one: 'найди сессию', 'последние сессии', 'прошлая сессия', 'сломанная/незавершённая сессия', 'какие были чаты', 'какие были сессии', 'session id', 'подними контекст из сессии', 'продолжим с той сессии', 'what was that session about'. Governs the mandatory script-based extraction: the agent MUST NEVER read session JSONL files directly — the script distills titles, repos, statuses, and transcripts."
triggers:
  request: "найди сессию, последние сессии, прошлая сессия, прежняя сессия, сломанная сессия, незавершённая сессия, завершённая сессия, какие были чаты, какие были сессии, session id, найди разговор, найди чат, история сессий, what sessions, find session, previous session, broken session, подними контекст, подними контекст из сессии, продолжим с той сессии, продолжи сессию, восстанови контекст сессии, restore session context, resume that session, трекай сессию, следи за сессией, мониторинг сессии, track session, session counters, сколько токенов, контекст заполнен, счётчики сессии"
  reason: "Session questions must be answered from distilled script output, never from raw JSONL reads."
runtime: true
requires:
  - mandatory-tools
version: 0.3.0
---

# SKILL: Session Inspector

Kimi Code CLI sessions live under `~/.kimi/sessions/<project-hash>/<session-uuid>/` as noisy JSONL (`context.jsonl`, `context_N.jsonl`, `wire.jsonl`) plus `state.json`/`metadata.json`. Reading those files directly floods the context with system prompts, checkpoints, tool outputs, and wire protocol. This skill owns the token-cheap way to answer session questions.

## 1. The One Rule (HARD)

[ref: #si-one-rule]

NEVER read session files (`*.jsonl`, `state.json`, `metadata.json`) directly with ReadFile/cat/rg-for-content. ALWAYS use the script; it does the parsing and emits only the distillate. The script is the only sanctioned reader of the session format.

```bash
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py [--last N]
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py --no-cwd [--last N]
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py --query "some phrase" [--last N]
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py --query "some phrase" --exact [--last N]
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py --session <session-uuid>
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py --session <session-uuid> --restore
uv run --no-project python OnDemand/session-inspector/scripts/inspect_sessions.py --sessions-dir PATH
```

(Subagents receive the absolute path: `<workspace>/session-inspector/scripts/inspect_sessions.py`. Run from the skills workspace root.)

## 2. Flags and Arguments

[ref: #si-flags]

| Flag | Default | Description |
|---|---|---|
| `--last N` | 10 | How many recent sessions to list. Increase this when the target session is older than the default window. |
| `--no-cwd` | false | Disable the current-working-directory filter and search sessions from all known projects. |
| `--query PHRASE` | — | Filter sessions whose messages match `PHRASE`. Fuzzy by default; use `--exact` for a case-insensitive substring match. |
| `--exact` | false | Switch `--query` from fuzzy matching to exact case-insensitive substring matching. |
| `--session UUID` | — | Switch to show/restore mode. A full UUID or a short unambiguous prefix is accepted; it must match exactly one session directory. |
| `--restore` | false | Use only with `--session`: emit a context-restoration pack instead of a transcript. |
| `--sessions-dir PATH` | `~/.kimi/sessions` | Override the sessions root (useful for tests, fixtures, or non-standard Kimi layouts). |

Combinations and constraints:

- `--exact` is only meaningful together with `--query`.
- `--query` can be combined with `--no-cwd` to search across all projects.
- `--restore` is invalid without `--session`.
- `--last` affects list mode only (the default). Show/restore mode always targets one session.

## 3. Modes

[ref: #si-modes]

- **List mode (default):** the N most recent sessions (default 10, `--last K` to change), one block per session: full UUID, last activity (UTC), status (`active` / `archived` / `interrupted` / `stale`), title when the file carries one, working repos (absolute paths from tool calls, resolved to git roots), and the first/last real messages (the first is read from the oldest compaction segment `context_N.jsonl` when present).
- **Show mode (`--session <session-uuid>`):** the distilled transcript — user/assistant text only, noise-injected system blocks stripped, each message truncated, capped at the last 50 messages. Use it to answer "what exactly happened in that session" without touching the JSONL.
- **Restore mode (`--session <session-uuid> --restore`):** the context-restoration pack for "подними контекст из этой сессии" — NOT a transcript: OPEN todos from `state.json` in full (done ones collapse to a count), working repos, recently written files, Serena memory refs the session touched, the last user messages, and the last assistant messages at up to 1000 chars each. Additionally, the full session is converted to TOON format and written to `.tmp/session-inspector/<session-uuid>.toon`; the pack reports the file path, turn count, and line count. The on-screen `toon_preview` shows the first/last 5 user→assistant turns and skips `role: tool` results to keep the preview compact; the written TOON file still contains the full conversation including tool results. If `toon` is not installed, ask the user to install `@toon-format/cli` themselves; the agent MUST NOT run `npm install -g @toon-format/cli` for the user.

## 4. Presenting to the User

[ref: #si-presentation]

- **The agent composes session titles itself** from the distilled first/last messages (owner ruling 2026-08-05T10:45:00Z): a short Russian one-liner per session saying what the session concretely was about, always with the full UUID.
- Always show the working repositories per session (the `repos:` line).
- Status vocabulary for the user: `active` = живой (активность в последние сутки), `archived` = завершён, `interrupted` = вероятно сломан/брошен (не archived, есть ОТКРЫТЫЕ todos, активность давно), `stale` = не archived, открытых todos нет, активность давно.
- If the user looks for "the broken/finished session", run list mode, name candidates with ids, and offer show mode for the chosen one.

## 5. Context Restoration Procedure

[ref: #si-restore]

When the user asks to lift/restore context from a session ("подними контекст из …", "продолжим с той сессии"):

1. Run restore mode for the given UUID.
2. Read the memory refs the pack names — those pages are already distilled and are the sanctioned deep layer (ReadFile on `.serena/memories/...` is allowed; the JSONL is still forbidden). Read at most the 2–3 most relevant refs.
3. Present a compact Russian summary: what the session did, where it stopped (todos + last assistant message), which repos and files it touched.
4. The pack ends with `toon_file:`, `toon_turns:`, and `toon_lines:` lines. The TOON file contains the **entire** session and can be huge. The agent MUST NOT load it whole into the chat or save it to Serena memory. Default handling: read the first ~100 lines with `rtk head -n 100 <toon_file>`, then read more or slice with `rtk tail` / `rg` / `rtk` as needed.
5. Ask the user what to continue — never auto-resume the old task list.

## 6. Violation Protocol

[ref: #si-violation-protocol]

If you catch yourself opening a session JSONL directly, halt, discard, and rerun through the script. If the script cannot answer the question (format drift), say so and propose a script fix — do not fall back to manual digging.

## 7. Session Tracking

[ref: #si-session-tracking]

When the user asks to track the live session ("трекай сессию", "сколько токенов", "контекст заполнен", "track session", "session counters"), use `track_session.py`. This is the only sanctioned reader of `wire.jsonl`; the agent MUST NOT read it directly.

### 7.1 One-shot on-demand flow

[ref: #si-tracking-flow]

The agent cannot start work on its own between user messages, so tracking is on-demand: one user request produces one snapshot of counters.

```text
if a real session_id is already known in this conversation:
    uv run --no-project python OnDemand/session-inspector/scripts/track_session.py <session_id>
else:
    probe = python -c "import uuid; print(uuid.uuid4())"
    uv run --no-project python OnDemand/session-inspector/scripts/track_session.py <probe>
    remember the returned session_id for subsequent calls
show the counters to the user
```

### 7.2 Interpreting the output

[ref: #si-tracking-output]

The script emits one JSON line:

```json
{
  "session_id": "84c2da47-f01a-41b6-9921-6e4e94bbae75",
  "found_by": "probe",
  "status": {
    "context_tokens": 9057,
    "context_usage": 0.0345,
    "max_context_tokens": 262144,
    "token_usage": {
      "input_other": 353,
      "output": 87,
      "input_cache_read": 8704,
      "input_cache_creation": 0
    },
    "message_id": "chatcmpl-...",
    "plan_mode": false,
    "mcp_status": null
  },
  "error": null
}
```

Presentation rules:

- Show `context_tokens / max_context_tokens` and the percentage from `context_usage`.
- Show `token_usage.input_cache_read`, `input_other`, and `output`.
- Mention `plan_mode: true` if the session is currently in plan mode.
- If `status` is `null` but `session_id` is present, the session was found but no `StatusUpdate` has arrived yet.
- If `found_by` is `"not_found"`, the probe has not yet been flushed to disk. Tell the user to repeat the request in a few seconds.
- If `error` is non-null, report the error and stop.

### 7.3 Generating the probe UUID

[ref: #si-probe-uuid]

Use a one-liner with the system Python interpreter:

```bash
python -c "import uuid; print(uuid.uuid4())"
```

The probe UUID is passed to `track_session.py`. The script discovers the real session directory because the tool invocation containing the probe is recorded in the session's own JSONL files.
