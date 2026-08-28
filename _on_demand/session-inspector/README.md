# session-inspector
[ref: #si-intro]

Inspects Kimi Code CLI session files without reading raw JSONL.

## What it does
[ref: #si-what]

This skill provides a token-cheap way to answer questions about past Kimi Code CLI sessions. Sessions are stored as noisy JSONL files under `~/.kimi/sessions/<project-hash>/<session-uuid>/` and can flood context if read directly. The skill mandates using a dedicated script that parses the session format and emits only a distillate: titles, repos, statuses, and transcripts.

## When it activates
[ref: #si-when]

Activates when you ask to find, list, identify, or restore past sessions in Russian or English.

Examples:

- "Найди сессию"
- "Последние сессии"
- "Подними контекст из сессии"
- "What was that session about?"
- "Restore session context"

## How to run / use it
[ref: #si-how]

The agent runs the script from the skills workspace root.
Use list mode for the most recent sessions, show mode for a distilled transcript, or restore mode for a context-restoration pack.

```bash
uv run --no-project python _on_demand/session-inspector/scripts/inspect_sessions.py [--last N]
uv run --no-project python _on_demand/session-inspector/scripts/inspect_sessions.py --session <session-uuid>
uv run --no-project python _on_demand/session-inspector/scripts/inspect_sessions.py --session <session-uuid> --restore
```

You do not need to open `~/.kimi/sessions/` yourself; the script is the only sanctioned reader of the session format.

### Session tracking

To track the live counters of the current session, use `track_session.py`. First call uses a probe UUID; the script discovers the real session id and returns the latest `StatusUpdate` counters. Subsequent calls use that real id directly.

```bash
# first call: discover session with a probe UUID
uv run --no-project python _on_demand/session-inspector/scripts/track_session.py <probe-uuid>

# later calls: use the real session id
uv run --no-project python _on_demand/session-inspector/scripts/track_session.py <session-id>
```

Example output:

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

## What it produces
[ref: #si-produces]

- A list of recent sessions with full UUIDs, last activity (UTC), status, composed title, working repos, and first/last messages.
- A distilled transcript for a chosen session, capped at the last 50 messages.
- A context-restoration pack with open todos, working repos, recently written files, Serena memory refs, closing messages, and the path to a TOON file that contains the **entire** session.

## Dependencies and why they matter
[ref: #si-deps]

- `mandatory-tools` — governs CLI execution and the script invocation pattern.
- `uv` + Python 3.12+ — for running both scripts.
- `rapidfuzz` — optional; `inspect_sessions.py` falls back to `difflib` if it is missing.
- `rg` (ripgrep) — required by `track_session.py` to discover a session from a probe UUID.
- `jq` — required by `track_session.py` to extract the latest `StatusUpdate` from `wire.jsonl`, and by `inspect_sessions.py` restore mode to filter context JSONL.
- `toon` (the `@toon-format/cli` tool) — required by `inspect_sessions.py` restore mode to convert the full session to a compact agent-readable format.
  - Install (user-side only): `npm install -g @toon-format/cli`
  - Repo / spec: https://github.com/toon-format/toon
  - Note: MCP agents are typically proxied through https://github.com/chaindead/tooner
  - The agent must **not** run this install command for the user; it is a one-time user setup step.

## Strengths and trade-offs
[ref: #si-tradeoffs]

### Strong sides
[ref: #si-strong]

- Avoids flooding context with raw JSONL, system prompts, and wire protocol noise.
- Composes human-readable session titles from the distillate.
- Restore mode gives a compact state summary without replaying the whole conversation.

### Weak sides / limits
[ref: #si-weak]

- Depends on the script keeping up with session format changes in Kimi Code CLI.
- Restore mode does not auto-resume tasks; it only presents state and asks what to continue.
- Can only inspect sessions that still exist on disk.

### Common pitfalls / gotchas
[ref: #si-pitfalls]

- NEVER read session `*.jsonl`, `state.json`, or `metadata.json` directly with ReadFile, cat, or grep-for-content.
- If the script cannot answer the question due to format drift, propose a script fix instead of manual digging.
- Status vocabulary for users: `active` = живой, `archived` = завершён, `interrupted` = вероятно сломан/брошен, `stale` = открытых todos нет, активность давно.
- Restore mode writes the **entire** session as a TOON file to `.tmp/session-inspector/<session-uuid>.toon`. Do not load it whole into context; use `rtk head -n 100 <file>` by default and slice further as needed.

## Repository layout
[ref: #si-layout]

```text
_on_demand/session-inspector/
├── scripts/              # Session parsing and distillation scripts
│   ├── inspect_sessions.py
│   └── track_session.py
├── README.md             # Human overview (this file)
└── SKILL.md              # Agent entry point: modes, presentation rules, and violation protocol
```

## Important conventions / gotchas
[ref: #si-conventions]

- The script is the only sanctioned reader of the session format.
- List mode defaults to the 10 most recent sessions; use `--last K` to widen the window.
- Show mode truncates each message and caps at the last 50 messages.
- Restore mode reads at most the 2–3 most relevant Serena memory refs.
- The agent composes session titles itself from the distillate.
