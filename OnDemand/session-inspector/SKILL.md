---
name: session-inspector
description: "Token-cheap inspection of Kimi Code CLI session files under ~/.kimi/sessions. Use when the user asks to find, list, or identify past sessions — or to restore working context from one: 'найди сессию', 'последние сессии', 'прошлая сессия', 'сломанная/незавершённая сессия', 'какие были чаты', 'session id', 'подними контекст из сессии', 'продолжим с той сессии', 'what was that session about'. Governs the mandatory script-based extraction: the agent MUST NEVER read session JSONL files directly — the script distills titles, repos, statuses, and transcripts."
triggers:
  request: "найди сессию, последние сессии, прошлая сессия, прежняя сессия, сломанная сессия, незавершённая сессия, завершённая сессия, какие были чаты, какие были сессии, session id, найди разговор, найди чат, история сессий, what sessions, find session, previous session, broken session, подними контекст, подними контекст из сессии, продолжим с той сессии, продолжи сессию, восстанови контекст сессии, restore session context, resume that session"
  reason: "Session questions must be answered from distilled script output, never from raw JSONL reads."
runtime: true
requires:
  - mandatory-tools
version: 0.2.0
---

# SKILL: Session Inspector

Kimi Code CLI sessions live under `~/.kimi/sessions/<project-hash>/<session-uuid>/` as noisy JSONL (`context.jsonl`, `context_N.jsonl`, `wire.jsonl`) plus `state.json`/`metadata.json`. Reading those files directly floods the context with system prompts, checkpoints, tool outputs, and wire protocol. This skill owns the token-cheap way to answer session questions.

## 1. The One Rule (HARD)

[ref: #si-one-rule]

NEVER read session files (`*.jsonl`, `state.json`, `metadata.json`) directly with ReadFile/cat/rg-for-content. ALWAYS use the script; it does the parsing and emits only the distillate. The script is the only sanctioned reader of the session format.

```bash
uv run --no-project python session-inspector/scripts/inspect_sessions.py [--last N]
uv run --no-project python session-inspector/scripts/inspect_sessions.py --session <id-prefix>
uv run --no-project python session-inspector/scripts/inspect_sessions.py --session <id-prefix> --restore
```

(Subagents receive the absolute path: `<workspace>/session-inspector/scripts/inspect_sessions.py`. Run from the skills workspace root; use `--last K` to widen the window for older sessions and `--sessions-dir` to point at fixtures or another sessions root.)

## 2. Modes

[ref: #si-modes]

- **List mode (default):** the N most recent sessions (default 10, `--last K` to change), one block per session: short id, last activity (UTC), status (`active` / `archived` / `interrupted` / `stale`), title when the file carries one, working repos (absolute paths from tool calls, resolved to git roots), and the first/last real messages (the first is read from the oldest compaction segment `context_N.jsonl` when present).
- **Show mode (`--session <id-prefix>`):** the distilled transcript — user/assistant text only, noise-injected system blocks stripped, each message truncated, capped at the last 50 messages. Use it to answer "what exactly happened in that session" without touching the JSONL.
- **Restore mode (`--session <id-prefix> --restore`):** the context-restoration pack for "подними контекст из этой сессии" — NOT a transcript: OPEN todos from `state.json` in full (done ones collapse to a count), working repos, recently written files, Serena memory refs the session touched, the last user messages, and the last assistant messages at up to 1000 chars each (closing summaries carry the state).

## 3. Presenting to the User

[ref: #si-presentation]

- **The agent composes session titles itself** from the distilled first/last messages (owner ruling 2026-08-05T10:45:00Z): a short Russian one-liner per session saying what the session concretely was about, always with the short id.
- Always show the working repositories per session (the `repos:` line).
- Status vocabulary for the user: `active` = живой (активность в последние сутки), `archived` = завершён, `interrupted` = вероятно сломан/брошен (не archived, есть ОТКРЫТЫЕ todos, активность давно), `stale` = не archived, открытых todos нет, активность давно.
- If the user looks for "the broken/finished session", run list mode, name candidates with ids, and offer show mode for the chosen one.

## 4. Context Restoration Procedure

[ref: #si-restore]

When the user asks to lift/restore context from a session ("подними контекст из …", "продолжим с той сессии"):

1. Run restore mode for the given id prefix.
2. Read the memory refs the pack names — those pages are already distilled and are the sanctioned deep layer (ReadFile on `.serena/memories/...` is allowed; the JSONL is still forbidden). Read at most the 2–3 most relevant refs.
3. Present a compact Russian summary: what the session did, where it stopped (todos + last assistant message), which repos and files it touched.
4. Ask the user what to continue — never auto-resume the old task list.

## 5. Violation Protocol

[ref: #si-violation-protocol]

If you catch yourself opening a session JSONL directly, halt, discard, and rerun through the script. If the script cannot answer the question (format drift), say so and propose a script fix — do not fall back to manual digging.
