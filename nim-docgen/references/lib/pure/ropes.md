---
source_hash: fdc77c9ea3278430
source_path: lib/pure/ropes.nim
---

# ropes

[ref: #module-ropes]

This module contains support for a rope data type. Ropes can represent very long strings efficiently; in particular, concatenation is done in O(1) instead of O(n). They are essentially concatenation trees that are only flattened when converting to a native Nim string. The empty string is represented by nil. Ropes are immutable and subtrees can be shared without copying. Leaves can be cached for better memory efficiency at the cost of runtime efficiency.

## Examples

```nim
let r1 = "$1 $2 $3" % [rope("Nim"), rope("is"), rope("a great language")]
doAssert $r1 == "Nim is a great language"

let r2 = "$# $# $#" % [rope("Nim"), rope("is"), rope("a great language")]
doAssert $r2 == "Nim is a great language"

let r3 = "${1} ${2} ${3}" % [rope("Nim"), rope("is"), rope("a great language")]
doAssert $r3 == "Nim is a great language"
```

```nim
let r = rope("Hello, ") & rope("Nim!")
doAssert $r == "Hello, Nim!"
```

```nim
let r = &[rope("Hello, "), rope("Nim"), rope("!")]
doAssert $r == "Hello, Nim!"
```

```nim
let r = rope("Hello, ") & "Nim!"
doAssert $r == "Hello, Nim!"
```

```nim
let r = "Hello, " & rope("Nim!")
doAssert $r == "Hello, Nim!"
```

```nim
let r = rope("Hello, Nim!")

doAssert r[0] == 'H'
doAssert r[7] == 'N'
doAssert r[22] == '\0'
```

```nim
var r = rope("Hello, ")
r.add(rope("Nim!"))
doAssert $r == "Hello, Nim!"
```

```nim
var r = rope("Hello, ")
r.add("Nim!")
doAssert $r == "Hello, Nim!"
```

```nim
var r = rope("Dash: ")
r.addf "$1 $2 $3", [rope("Nim"), rope("is"), rope("a great language")]
doAssert $r == "Dash: Nim is a great language"
```

```nim
let r = rope(4.29)
doAssert $r == "4.29"
```

```nim
let r = rope(429)
doAssert $r == "429"
```

```nim
let r = rope("I'm a rope")
doAssert $r == "I'm a rope"
```

```nim
let r = rope("Hello") & rope(", Nim!")
let s = ["Hello", ", Nim!"]
var index = 0
for leave in r.leaves:
  doAssert leave == s[index]
  inc(index)
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `r: Rope`

**Output:** `char`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over any character in the rope r.

### leaves

[ref: #symbol-leaves]

**Input:**
- `r: Rope`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over any leaf string in the rope r.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `r: Rope`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nroToString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a rope back to a string.

### `%`

[ref: #symbol-]

**Input:**
- `frmt: string`
- `args: openArray[Rope]`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nroFormat"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

% substitution operator for ropes. Does not support the $identifier nor ${identifier} notations.

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `a: Rope`
- `b: Rope`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nroConcRopeRope"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The concatenation operator for ropes.

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `a: Rope`
- `b: string`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nroConcRopeStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The concatenation operator for ropes.

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `a: string`
- `b: Rope`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nroConcStrRope"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The concatenation operator for ropes.

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `a: openArray[Rope]`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nroConcOpenArray"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The concatenation operator for an openArray of ropes.

### `[]`

[ref: #symbol-]

**Input:**
- `r: Rope`
- `i: int`

**Output:** `char`
**Pragmas:** `gcsafe`, `extern: "nroCharAt"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the character at position i in the rope r. This is quite expensive! Worst-case: O(n). If i >= r.len or i < 0, \0 is returned.

### add

[ref: #symbol-add]

**Input:**
- `a: var Rope`
- `b: Rope`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nro$1Rope"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds b to the rope a.

### add

[ref: #symbol-add]

**Input:**
- `a: var Rope`
- `b: string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nro$1Str"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds b to the rope a.

### addf

[ref: #symbol-addf]

**Input:**
- `c: var Rope`
- `frmt: string`
- `args: openArray[Rope]`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nro$1"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Shortcut for add(c, frmt % args).

### disableCache

[ref: #symbol-disablecache]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nro$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The cache is discarded and disabled. The GC will reuse its used memory.

### enableCache

[ref: #symbol-enablecache]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nro$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Enables the caching of leaves. This reduces the memory footprint at the cost of runtime efficiency.

### equalsFile

[ref: #symbol-equalsfile]

**Input:**
- `r: Rope`
- `f: File`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nro$1File"`, `raises: [IOError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect`, `forbids: `

Returns true if the contents of the file f equal r.

### equalsFile

[ref: #symbol-equalsfile]

**Input:**
- `r: Rope`
- `filename: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nro$1Str"`, `raises: [IOError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect`, `forbids: `

Returns true if the contents of the file f equal r. If f does not exist, false is returned.

### len

[ref: #symbol-len]

**Input:**
- `a: Rope`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nro$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The rope's length.

### rope

[ref: #symbol-rope]

**Input:**
- `s: string = ""`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nro$1Str"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a string to a rope.

### rope

[ref: #symbol-rope]

**Input:**
- `i: BiggestInt`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nro$1BiggestInt"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an int to a rope.

### rope

[ref: #symbol-rope]

**Input:**
- `f: BiggestFloat`

**Output:** `Rope`
**Pragmas:** `gcsafe`, `extern: "nro$1BiggestFloat"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a float to a rope.

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `r: Rope`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nro$1"`, `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Writes a rope to a file.

### write

[ref: #symbol-write]

**Input:**
- `s: Stream`
- `r: Rope`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nroWriteStream"`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes a rope to a stream.

## Type

### Rope

[ref: #symbol-rope]

```nim
Rope {.acyclic.} = ref object
```

A rope data type. The empty rope is represented by nil.
