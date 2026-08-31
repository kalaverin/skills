# discuss-first
[ref: #df-intro]

Co-implementation mode: plan the implementation top-down and get your approval before any code is written.

## What it does
[ref: #df-what]

This skill switches the agent into discuss-first mode for non-trivial work. Instead of immediately editing files, the agent studies the task, walks you through the implementation one abstraction layer at a time, and collects your explicit approval for each part and for the final blueprint. Only after the master approval does the agent write code, and every line must match the approved contract. The mode also applies a mandatory existence-review standard (the always-loaded `existence-bible` skill, rule ids A1–K4) to every keep/revert/delete decision.

## When it activates
[ref: #df-when]

Activates when you ask for co-implementation, step-by-step planning, or explicitly say the agent should not write code without you in English or Russian.

Examples:

- "Пишем код вместе"
- "Ты не пишешь без меня"
- "Step-by-step"
- "Обсудим реализацию"

It also activates proactively before non-trivial code work: new features, refactoring, behavior-changing bugfixes, or any new function, method, class, or abstraction.

## How to run / use it
[ref: #df-how]

Once active, the agent will:

1. Study the task and existing code.
2. Present a top-down plan: abstractions, signatures with pseudocode bodies, data flow.
3. Ask for per-part approval.
4. Request master approval of the final blueprint.
5. Write code only after master approval.

Interrupt or correct the agent at any step. If you want to exit discuss-first mode for the rest of the session, say so explicitly.

## What it produces
[ref: #df-produces]

- A written implementation blueprint with full signatures and pseudocode.
- Per-part and final approvals captured in the conversation.
- Code written strictly according to the approved blueprint.
- A Solutions Journal in Serena memory (`solutions/<repo>/<subject>/`): one card per approval round, plus the final `solution.md` and `decisions.md` (see `SKILL.md` §13).

## Dependencies and why they matter
[ref: #df-deps]

- `serena-protocol` — governs the mandatory decision-card recording in Phase 3.
- `frontmatter-protocol` and `markdown-protocol` — provide the document conventions used by the blueprint and review notes.

## Strengths and trade-offs
[ref: #df-tradeoffs]

### Strong sides
[ref: #df-strong]

- Prevents mismatched expectations and wasted implementation effort.
- Forces explicit architecture decisions before code exists.
- Existence-review standard catches unnecessary code and keeps the tree clean.

### Weak sides / limits
[ref: #df-weak]

- Slower for trivial changes; use it only for non-trivial work.
- Requires active user engagement; not suitable for fire-and-forget tasks.
- The mode is session-scoped and does not persist.

### Common pitfalls / gotchas
[ref: #df-pitfalls]

- Code is written only after the final master approval.
- The existence-review standard is applied when deciding what to keep, revert, or delete.
- If the user changes requirements mid-plan, restart the affected layer rather than silently adapting.

## Repository layout
[ref: #df-layout]

```text
discuss-first/
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: mode rules, approval flow, blueprint format, and the Solutions Journal (§13); the Existence Bible lives in the `existence-bible` skill
```

## Reference overview
[ref: #df-refs]

| File | What it covers |
|------|----------------|
| `existence-bible` skill | Rules A1–K4 for keep/revert/delete decisions |

## Important conventions / gotchas
[ref: #df-conventions]

- Mode is session-scoped; a new session starts without it.
- Code is written only after master approval.
- Every keep/revert/delete decision follows the Existence Bible (`existence-bible` skill).
- The agent must explain each abstraction and signature before asking for approval.
