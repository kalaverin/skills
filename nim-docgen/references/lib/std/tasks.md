---
source_hash: 7480a869f2f25a2a
source_path: lib/std/tasks.nim
---

# tasks

[ref: #module-tasks]

This module provides basic primitives for creating parallel programs. A Task should be only owned by a single Thread, it cannot be shared by threads.

## Examples

```nim
import std/tasks
block:
  var num = 0
  proc hello(a: int) = inc num, a

  let b = toTask hello(13)
  b.invoke()
  assert num == 13
  # A task can be invoked multiple times
  b.invoke()
  assert num == 26

block:
  type
    Runnable = ref object
      data: int

  var data: int
  proc hello(a: Runnable) {.nimcall.} =
    a.data += 2
    data = a.data


  when false:
    # the parameters of call must be isolated.
    let x = Runnable(data: 12)
    let b = toTask hello(x) # error ----> expression cannot be isolated: x
    b.invoke()

  let b = toTask(hello(Runnable(data: 12)))
  b.invoke()
  assert data == 14
  b.invoke()
  assert data == 16
```

```nim
proc hello(a: int) = echo a

let b = toTask hello(13)
assert b is Task
```

## Macro

### toTask

[ref: #symbol-totask]

**Input:**
- `e: typed{nkCall | nkInfix | nkPrefix | nkPostfix | nkCommand | nkCallStrLit}`

**Output:** `Task`
Converts the call and its arguments to Task.

## Proc

### `=copy`

[ref: #symbol-copy]

**Input:**
- `x: var Task`
- `y: Task`

**Output:** *(none)*
**Pragmas:** `error`

### `=destroy`

[ref: #symbol-destroy]

**Input:**
- `t: Task`

**Output:** *(none)*
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Frees the resources allocated for a Task.

### invoke

[ref: #symbol-invoke]

**Input:**
- `task: Task`
- `res: pointer = nil`

**Output:** *(none)*
**Pragmas:** `inline`, `gcsafe`, `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Invokes the task.

## Type

### Task

[ref: #symbol-task]

```nim
Task = object
```

Task contains the callback and its arguments.
