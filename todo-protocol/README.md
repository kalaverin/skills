# todo-protocol
[ref: #todo-protocol]

Keeps the agent's multi-step work visible and correctly ordered through the `SetTodoList` tool.

## What it does
[ref: #todo-protocol-purpose]

This skill owns the agent's todo list.
It makes sure non-trivial or multi-step work is broken into milestones, that completed items are marked done promptly, and that the list is not deleted, overwritten, or shrunk while work is still in progress.
The result is a transparent, step-by-step view of what the agent is doing and what remains.

## When it activates
[ref: #todo-protocol-activation]

Always active.
It also activates for non-trivial implementation tasks, multi-step requests, or whenever you ask for ordered, step-by-step work.

Example prompts:

- "Break this task into steps."
- "Create a todo list for adding OAuth."
- "Show me the current todos."

## How to run / use it
[ref: #todo-protocol-usage]

1. Start a multi-step request or ask the agent to break a task into steps.
2. The agent creates a todo list with high-level milestones.
3. As work completes, the agent marks each item `done` before moving on.
4. If new work is discovered, the agent inserts new items at the current active position rather than appending them after completed work.
5. Ask "What is on the todo list?" at any time to see the current state.

## What it produces
[ref: #todo-protocol-artifacts]

- A conversation-visible todo list with items in `pending`, `in_progress`, or `done` states.
- No files or memory entries; the list lives in the session and is the single source of truth for work state.

## Dependencies and why they matter
[ref: #todo-protocol-dependencies]

- None declared in the skill header.
- This skill is always active and works alongside any other protocol that produces multi-step work.

## Strengths and trade-offs
[ref: #todo-protocol-tradeoffs]

- Strong sides: makes agent progress explicit and inspectable; prevents silent abandonment of unfinished work; synchronizes state after every completed tool call.
- Weak sides / limits: adds overhead that is not justified for trivial single-step tasks; the list is session-local and disappears when the session ends.
- Common pitfalls / gotchas: once a list exists, the agent must not delete, overwrite, clear, shrink, or recreate it while any item remains unfinished; new items are inserted at the current active position, not appended to the end; mark an item done only after the work it represents is actually complete.

## Repository layout
[ref: #todo-protocol-layout]

```text
todo-protocol/
├── README.md   # Human overview (this file)
└── SKILL.md    # Agent entry point: creation, update, and immutability rules
```

## Important conventions / gotchas
[ref: #todo-protocol-gotchas]

- Use `SetTodoList` for non-trivial, multi-step, or user-requested ordered work; skip it for trivial single-step tasks.
- Allowed mutations are marking items done and inserting new items at the current active position.
- Forbidden mutations while work remains: deleting, overwriting, clearing, shrinking, or recreating the list.
- The todo list is the single source of truth for work state; status must be synchronized after every tool call that completes a task.
