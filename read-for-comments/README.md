# read-for-comments

Keeps frequently referenced technical standards close at hand so the agent consults local copies before searching the web.

## What it does

This skill hosts local copies of technical standards such as RFCs.
It gives the agent a fast, offline-first lookup for requirement-level keywords and common specifications.
It reduces redundant web searches and keeps interpretations consistent across sessions.
When a requested standard is not stored locally, the agent falls back to web search and can save the result for future reuse.

## When it activates

No action needed — loaded automatically in every session.
It also activates when you ask about RFCs, OWASP guidelines, STDs, PEPs, or requirement words such as MUST, SHOULD, and MAY.

Examples of prompts that trigger it:

- "What does RFC 2119 say about MUST?"
- "Explain the OWASP API Security Top 10."
- "When is lowercase 'should' still binding?"

## How to use it

You do not need to configure anything.
When you ask about a standard, the agent checks the local `references/` directory first.
If the standard is missing, the agent searches the web and may store the fetched text under Serena memory `standard/<kind>/<id>` for next time.
You can add new local standards by placing Markdown or text files in `read-for-comments/references/` with predictable names such as `rfc<id>.md`, `owasp<id>.md`, `std<id>.md`, or `pep<id>.md`.

## What it produces

- Local answers from `references/` when a standard is already on disk.
- Serena memory entries under `standard/` when a newly fetched standard is saved for reuse.
- No changes to project source code.

## Repository layout

```text
read-for-comments/
├── references/           # Local copies of technical standards
│   ├── rfc2119.md        # Key words for use in RFCs to Indicate Requirement Levels
│   └── rfc8174.md        # Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words
└── SKILL.md              # Agent entry point: manifest, triggers, and lookup protocol
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/rfc2119.md` | RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels |
| `references/rfc8174.md` | RFC 8174 — Ambiguity of uppercase vs lowercase in RFC 2119 key words |

## Important conventions / gotchas

- No prerequisites.
- Only standards present in `references/` are served locally; absent standards still require a web search.
- The skill prefers local copies, so adding a file here makes future lookups faster and more consistent.
- Saved web standards land in Serena memory, not in this directory.
