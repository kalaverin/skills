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
uv run --no-project python session-inspector/scripts/inspect_sessions.py [--last N]
uv run --no-project python session-inspector/scripts/inspect_sessions.py --session <id-prefix>
uv run --no-project python session-inspector/scripts/inspect_sessions.py --session <id-prefix> --restore
```

You do not need to open `~/.kimi/sessions/` yourself; the script is the only sanctioned reader of the session format.

## What it produces
[ref: #si-produces]

- A list of recent sessions with short ids, last activity (UTC), status, composed title, working repos, and first/last messages.
- A distilled transcript for a chosen session, capped at the last 50 messages.
- A context-restoration pack with open todos, working repos, recently written files, Serena memory refs, and closing messages.

## Dependencies and why they matter
[ref: #si-deps]

- `mandatory-tools` — governs CLI execution and the script invocation pattern.
- `uv` and Python — needed to run `inspect_sessions.py`.

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

## Repository layout
[ref: #si-layout]

```text
session-inspector/
├── scripts/              # Session parsing and distillation script
│   └── inspect_sessions.py
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: modes, presentation rules, and violation protocol
```

## Important conventions / gotchas
[ref: #si-conventions]

- The script is the only sanctioned reader of the session format.
- List mode defaults to the 10 most recent sessions; use `--last K` to widen the window.
- Show mode truncates each message and caps at the last 50 messages.
- Restore mode reads at most the 2–3 most relevant Serena memory refs.
- The agent composes session titles itself from the distillate.
