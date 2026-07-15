---
source_hash: 3dfa13653a8cbe07
source_path: lib/std/monotimes.nim
---

# monotimes

[ref: #module-monotimes]

The std/monotimes module implements monotonic timestamps. A monotonic timestamp represents the time that has passed since some system defined point in time. The monotonic timestamps are guaranteed not to decrease, meaning that that the following is guaranteed to work:

This is not guaranteed for the times.Time type! This means that the MonoTime should be used when measuring durations of time with high precision.

However, since MonoTime represents the time that has passed since some unknown time origin, it cannot be converted to a human readable timestamp. If this is required, the times.Time type should be used instead.

The MonoTime type stores the timestamp in nanosecond resolution, but note that the actual supported time resolution differs for different systems.

# [See also](#see-also)

* [times module](times.html)

## Examples

```nim
import std/monotimes
let a = getMonoTime()
let b = getMonoTime()
assert a <= b
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `t: MonoTime`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `a: MonoTime`
- `b: MonoTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a happened before b or if they happened simultaneous.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `a: MonoTime`
- `b: MonoTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a happened before b.

### `+`

[ref: #symbol-]

**Input:**
- `a: MonoTime`
- `b: Duration`

**Output:** `MonoTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Increases a by b.

### `-`

[ref: #symbol-]

**Input:**
- `a: MonoTime`
- `b: MonoTime`

**Output:** `Duration`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the difference between two MonoTime timestamps as a Duration.

### `-`

[ref: #symbol-]

**Input:**
- `a: MonoTime`
- `b: Duration`

**Output:** `MonoTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reduces a by b.

### `==`

[ref: #symbol-]

**Input:**
- `a: MonoTime`
- `b: MonoTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a and b happened simultaneous.

### getMonoTime

[ref: #symbol-getmonotime]

Returns the current MonoTime timestamp.

**Input:**
- *(none)*

**Output:** `MonoTime`
**Pragmas:** `tags: [TimeEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Returns the current MonoTime timestamp.

When compiled with the JS backend and executed in a browser, this proc calls window.performance.now(). See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now) for more information.

### high

[ref: #symbol-high]

**Input:**
- `typ: typedesc[MonoTime]`

**Output:** `MonoTime`
**Generic parameters:** `typ:type`

Returns the highest representable MonoTime.

### low

[ref: #symbol-low]

**Input:**
- `typ: typedesc[MonoTime]`

**Output:** `MonoTime`
**Generic parameters:** `typ:type`

Returns the lowest representable MonoTime.

### ticks

[ref: #symbol-ticks]

**Input:**
- `t: MonoTime`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the raw ticks value from a MonoTime. This value always uses nanosecond time resolution.

## Type

### MonoTime

[ref: #symbol-monotime]

```nim
MonoTime = object
```

Represents a monotonic timestamp.
