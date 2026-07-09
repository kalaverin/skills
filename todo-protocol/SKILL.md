---
name: todo-protocol
description: Mandatory protocol for using the SetTodoList tool. Governs when to create a todo list, how to update it without violating immutability rules, how to synchronize item status after every tool call, and the forbidden mutations. Always active.
triggers:
  always: true
  reason: "Todo list management is required for any non-trivial or multi-step task."
---

# SKILL: Todo List Protocol

This skill owns the `SetTodoList` tool.
It applies to every task that involves multiple subtasks, milestones, sequential steps, or any situation where the user asks for a todo list, ordered execution, or step-by-step work.
When this skill is active, its rules override any casual or heuristic use of the todo list.

## 1. When to Use SetTodoList

You MUST use `SetTodoList` for:

- Non-trivial implementation tasks (new features, architectural changes, multi-file modifications, unclear requirements).
- Tasks with more than one step.
- Any request where the user asks for a todo list, sequential execution, ordered actions, or step-by-step work.

You MAY stop using the todo list mid-session if you started it and then realized the task is trivial enough to complete without it.
You MUST NOT use the todo list for trivial single-step tasks or for tracking steps that are too small to justify the overhead.

## 2. Creating the Todo List

If no todo list exists, create one immediately when the task qualifies under Section 1.
The initial list should contain the high-level milestones or subtasks needed to complete the request.

## 3. Updating the Todo List

`SetTodoList` operates in three modes:

- **Update mode:** pass `todos` to replace the entire list. Use this only when the rules below allow it.
- **Query mode:** omit `todos` to retrieve the current list without changes.
- **Clear mode:** pass an empty array `[]` to clear all todos. Allowed only when every item is already finished or the task is truly complete.

## 4. Todo List Immutability Rule (HARD RULE)

Once a todo list exists, you MUST NOT delete, overwrite, clear, shrink, or recreate it while any item remains unfinished.

Allowed mutations are:

- Marking an item as `done`.
- Inserting new items at the current active position.

You MUST NOT remove unfinished items, reorder them to hide progress, or replace the list with a shorter one while work remains.

## 5. Status Synchronization Rule (HARD RULE)

After every tool call that completes a task, you MUST evaluate whether the active todo item is now factually complete.

- If yes, update it to `done` via `SetTodoList` BEFORE any subsequent action.
- Under no circumstances may you leave an item as `pending` or `in_progress` after the corresponding work is already done.

The todo list is the single source of truth for work state.

## 6. Inserting New Items

If new work is discovered after the list was created, insert new items at the current active position.
Do not append new items to the end if that would place them after already-completed work unless they are genuinely follow-up tasks.

## 7. Forbidden Patterns

You MUST NOT:

- Call `SetTodoList` repeatedly without making real progress between calls.
- Create a todo list and then ignore it.
- Mark an item done before the work it represents is actually finished.
- Leave an item as `in_progress` after the work is complete.
- Delete or overwrite a list to erase unfinished work.

## 8. Interaction with Other Skills

This skill is always active and works alongside other protocols.
When a subtask involves another skill (for example, writing a memory entry or delegating to a subagent), the active todo item should reflect the higher-level goal, and you must still synchronize its status after the underlying tool call completes.

## 9. Violation Protocol

If you violate any rule in this skill, halt immediately, restore the correct todo list state, and resume from the last valid state before continuing.
