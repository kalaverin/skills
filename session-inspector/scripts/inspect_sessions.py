"""Kimi Code CLI session inspector: token-cheap session listing and distillation.

Reads ~/.kimi/sessions/<project-hash>/<session-uuid>/ directories and emits
compact digests so the agent never reads raw JSONL noise (system prompts,
checkpoints, tool outputs, wire protocol) into its context.

Usage (run from the skills workspace root):
    inspect_sessions.py [--last N]           list the N most recent sessions
    inspect_sessions.py --session <id>       distilled transcript of one session
    inspect_sessions.py --session <id> --restore  context-restoration pack
    inspect_sessions.py --sessions-dir PATH  override the sessions root
"""

# ruff: noqa: INP001, T201 — CLI script, not a package; print is the interface.

import argparse
import json
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

GIST_CHARS = 220
MSG_CHARS = 300
TAIL_MESSAGES = 50
TOP_REPOS = 3
TOP_FILES = 10
TODO_CHARS = 120
SECONDS_PER_DAY = 86400
RESTORE_USER_MESSAGES = 5
RESTORE_ASSISTANT_MESSAGES = 3
RESTORE_ASSISTANT_CHARS = 1000

SYSTEM_NOISE = ("<system>", "<current_focus>", "<environment", "<system-reminder>")
PATH_RE = re.compile(r"/Users/[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+){1,5}")
MEMORY_RE = re.compile(r"(?:\.serena/memories/|mem:)[A-Za-z0-9/._-]+")
WRITE_TOOLS = ("WriteFile", "StrReplaceFile")
OPEN_TODO_STATUSES = ("pending", "in_progress")


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _text_parts(content: object) -> list[str]:
    """Extract human text parts from a message content field."""
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        return [
            p["text"]
            for p in content
            if isinstance(p, dict)
            and p.get("type") == "text"
            and isinstance(p.get("text"), str)
        ]
    return []


def _clean(text: str) -> str:
    return " ".join(text.split())


def _is_noise(text: str) -> bool:
    stripped = text.lstrip()
    return any(stripped.startswith(marker) for marker in SYSTEM_NOISE)


def _scan(
    context_file: Path,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[str]]:
    """Single streaming pass: messages, tool calls, memory refs."""
    messages: list[tuple[str, str]] = []
    tool_calls: list[tuple[str, str]] = []
    refs: set[str] = set()
    with context_file.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            refs.update(MEMORY_RE.findall(line))
            if '"role"' not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = rec.get("role")
            if role in ("user", "assistant"):
                texts = [
                    c
                    for p in _text_parts(rec.get("content"))
                    if (c := _clean(p)) and not _is_noise(c)
                ]
                if texts:
                    messages.append((role, " ".join(texts)))
            for call in rec.get("tool_calls") or []:
                function = call.get("function") or {}
                args = function.get("arguments")
                if isinstance(args, str):
                    tool_calls.append((function.get("name") or "", args))
    return messages, tool_calls, sorted(refs)


def _repo_root(path: str) -> str:
    """Resolve a path to its git repository root (longest ancestor holding .git)."""
    candidate = Path(path)
    for level in (candidate, *candidate.parents):
        if (level / ".git").exists():
            return str(level)
        if level == Path.home():
            break
    return path


def _repos(tool_calls: list[tuple[str, str]]) -> list[str]:
    """Best-effort repo detection: tool-call paths resolved to git roots."""
    counter: Counter[str] = Counter()
    for _, args in tool_calls:
        for match in PATH_RE.findall(args):
            if "/.serena" not in match and "/.kimi" not in match:
                counter[match] += 1
    roots: Counter[str] = Counter()
    for path, count in counter.most_common(20):
        roots[_repo_root(path)] += count
    return [root for root, _ in roots.most_common(TOP_REPOS)]


def _written_files(tool_calls: list[tuple[str, str]]) -> list[str]:
    out: list[str] = []
    for name, args in tool_calls:
        if name not in WRITE_TOOLS:
            continue
        try:
            path = json.loads(args).get("path")
        except json.JSONDecodeError:
            continue
        if isinstance(path, str):
            out.append(path)
    return out


def _context_files(session_dir: Path) -> list[Path]:
    """All context segments, oldest first (context_N snapshots, then the live one)."""
    numbered = sorted(
        session_dir.glob("context_*.jsonl"),
        key=lambda p: (
            int(p.stem.rsplit("_", 1)[1]) if p.stem.rsplit("_", 1)[1].isdigit() else 0
        ),
    )
    live = session_dir / "context.jsonl"
    return [*numbered, live] if live.exists() else numbered


def _session_state(session_dir: Path) -> dict:
    state_file = session_dir / "state.json"
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}
    return {}


def _status(state: dict, last_activity: float, now: float) -> str:
    if state.get("archived"):
        return "archived"
    todos = state.get("todos") or []
    open_todos = [
        t
        for t in todos
        if isinstance(t, dict) and t.get("status") in OPEN_TODO_STATUSES
    ]
    idle = now - last_activity > SECONDS_PER_DAY
    if open_todos and idle:
        return "interrupted"
    if idle:
        return "stale"
    return "active"


def _iter_sessions(root: Path) -> list[tuple[float, Path]]:
    sessions = []
    for session_dir in root.glob("*/*/"):
        if (
            not _context_files(session_dir)
            and not (session_dir / "state.json").exists()
        ):
            continue
        last = max(f.stat().st_mtime for f in session_dir.iterdir() if f.is_file())
        sessions.append((last, session_dir))
    sessions.sort(reverse=True)
    return sessions


def cmd_list(root: Path, last: int) -> None:
    now = datetime.now(UTC).timestamp()
    for last_activity, session_dir in _iter_sessions(root)[:last]:
        state = _session_state(session_dir)
        segments = _context_files(session_dir)
        first = ""
        if segments:
            oldest_messages, _, _ = _scan(segments[0])
            first = next((t for r, t in oldest_messages if r == "user"), "")
        latest = ""
        repos: list[str] = []
        if segments:
            messages, tool_calls, _ = _scan(segments[-1])
            latest = messages[-1][1] if messages else ""
            repos = _repos(tool_calls)
        status = _status(state, last_activity, now)
        print(f"{session_dir.name[:8]}  {_iso(last_activity)}  {status}")
        if state.get("custom_title"):
            print(f"  title: {state['custom_title']}")
        if repos:
            print(f"  repos: {', '.join(repos)}")
        if first:
            print(f"  first: {first[:GIST_CHARS]}")
        if latest and latest != first:
            print(f"  last:  {latest[:GIST_CHARS]}")
        print()


def cmd_show(session_dir: Path) -> None:
    segments = _context_files(session_dir)
    if not segments:
        sys.exit(f"no context segments in {session_dir}")
    messages, _, _ = _scan(segments[-1])
    for role, text in messages[-TAIL_MESSAGES:]:
        print(f"[{role}] {text[:MSG_CHARS]}")
        print()


def _print_todos(state: dict) -> None:
    todos = [t for t in (state.get("todos") or []) if isinstance(t, dict)]
    if not todos:
        return
    open_todos = [t for t in todos if t.get("status") in OPEN_TODO_STATUSES]
    done_count = len(todos) - len(open_todos)
    print("todos:")
    for todo in open_todos:
        print(
            f"  [{todo.get('status', '?')}] {str(todo.get('title', ''))[:TODO_CHARS]}",
        )
    if done_count:
        print(f"  ({done_count} done)")
    print()


def cmd_restore(session_dir: Path) -> None:
    """Emit a context-restoration pack: where the session stopped, what it touched."""
    segments = _context_files(session_dir)
    state = _session_state(session_dir)
    if state.get("custom_title"):
        print(f"title: {state['custom_title']}")
    _print_todos(state)
    if not segments:
        return
    messages, tool_calls, refs = _scan(segments[-1])
    repos = _repos(tool_calls)
    if repos:
        print(f"repos: {', '.join(repos)}")
    written = _written_files(tool_calls)
    if written:
        print("files written (recent):")
        for path in list(dict.fromkeys(written))[-TOP_FILES:]:
            print(f"  {path}")
        print()
    if refs:
        print("memory refs:")
        for ref in refs[:TOP_FILES]:
            print(f"  {ref}")
        print()
    users = [t for r, t in messages if r == "user"][-RESTORE_USER_MESSAGES:]
    assistants = [t for r, t in messages if r == "assistant"][
        -RESTORE_ASSISTANT_MESSAGES:
    ]
    print("last user messages:")
    for text in users:
        print(f"  - {text[:MSG_CHARS]}")
    print()
    print("last assistant messages (up to 1000 chars — closing summaries carry state):")
    for text in assistants:
        print(f"  ---\n  {text[:RESTORE_ASSISTANT_CHARS]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--last",
        type=int,
        default=10,
        help="how many recent sessions to list",
    )
    parser.add_argument("--session", help="session id (unique prefix) to distill")
    parser.add_argument(
        "--restore",
        action="store_true",
        help="context-restoration pack instead of transcript",
    )
    parser.add_argument(
        "--sessions-dir",
        type=Path,
        default=Path.home() / ".kimi" / "sessions",
    )
    args = parser.parse_args()

    root = args.sessions_dir
    if not root.is_dir():
        sys.exit(f"sessions dir not found: {root}")
    if args.last < 1:
        parser.error("--last must be a positive number")
    if args.restore and not args.session:
        parser.error("--restore requires --session <id-prefix>")

    if args.session:
        matches = [
            d for _, d in _iter_sessions(root) if d.name.startswith(args.session)
        ]
        if len(matches) != 1:
            candidates = ", ".join(d.name for d in matches) or "none"
            sys.exit(
                f"prefix {args.session!r} matches {len(matches)} dirs: {candidates}",
            )
        if args.restore:
            cmd_restore(matches[0])
        else:
            cmd_show(matches[0])
    else:
        cmd_list(root, args.last)


if __name__ == "__main__":
    main()
