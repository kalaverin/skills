# todo-protocol

Keeps the agent's multi-step work visible and correctly ordered through the `SetTodoList` tool.

## What it does

This skill owns the agent's todo list.
It makes sure non-trivial or multi-step work is broken into milestones, that completed items are marked done promptly, and that the list is not deleted or rewritten while work is still in progress.
The result is a transparent, step-by-step view of what the agent is doing and what remains.

## When it activates

No action needed — loaded automatically in every session.
It also activates for non-trivial implementation tasks, multi-step requests, or when you ask for ordered, step-by-step work.

Examples of prompts that trigger it:

- "Break this task into steps."
- "Create a todo list for adding OAuth."
- "Show me the current todos."

## How to use it

Ask the agent to break a task into steps or simply start a multi-step request.
The agent creates a todo list with high-level milestones and updates it as work finishes.
You can ask "What is on the todo list?" at any time to see the current state.
You do not edit any files.

## What it produces

- A conversation-visible todo list with items in `pending`, `in_progress`, or `done` states.
- No files or memory entries; the list lives in the session and is the single source of truth for work state.

## Repository layout

```text
todo-protocol/
└── SKILL.md              # Agent entry point: creation, update, and immutability rules
```

## Reference overview

| File | What it covers |
|------|----------------|
| `SKILL.md` | When to create a todo list, how to update it, and the immutability rules |

## Important conventions / gotchas

- No prerequisites.
- Do not use it for trivial single-step tasks.
- Once a list exists, the agent must not delete, overwrite, clear, shrink, or recreate it while any item remains unfinished.
- Newly discovered work is inserted at the current active position, not appended to the end.
- Mark an item `done` only after the work it represents is actually complete.
