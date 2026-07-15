---
source_hash: d2759de8fae52109
source_path: lib/pure/asyncmacro.nim
---

# asyncmacro

[ref: #module-asyncmacro]

Implements the async and multisync macros for asyncdispatch.

## Macro

### async

[ref: #symbol-async]

**Input:**
- `prc: untyped`

**Output:** `untyped`
Macro which processes async procedures into the appropriate iterators and yield statements.

### multisync

[ref: #symbol-multisync]

Macro which processes async procedures into both asynchronous and synchronous procedures.

**Input:**
- `prc: untyped`

**Output:** `untyped`
Macro which processes async procedures into both asynchronous and synchronous procedures.

The generated async procedures use the async macro, whereas the generated synchronous procedures simply strip off the await calls.

## Template

### await

[ref: #symbol-await]

**Input:**
- `f: typed`

**Output:** `untyped`
**Pragmas:** `used`

### await

[ref: #symbol-await]

**Input:**
- `f: Future[T]`

**Output:** `auto`
**Generic parameters:** `T`

**Pragmas:** `used`
