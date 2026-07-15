---
source_hash: a8e736d27ea6eac7
source_path: lib/std/private/gitutils.nim
---

# gitutils

[ref: #module-gitutils]

internal API for now, API subject to change

## Examples

```nim
let a = "ok1\nok2\nok3\n"
let b = "ok1\nok2 alt\nok3\nok4\n"
let (c, same) = diffStrings(a, b)
doAssert not same
let (c2, same2) = diffStrings(a, a)
doAssert same2
```

```nim
let a = "ok1\nok2\nok3\n"
let b = "ok1\nok2 alt\nok3\nok4\n"
echo diffStrings(a, b).output
```

```nim
doAssert not retryCall(maxRetry = 2, backoffDuration = 0.1, false)
var i = 0
doAssert: retryCall(maxRetry = 3, backoffDuration = 0.1, (i.inc; i >= 3))
doAssert retryCall(call = true)
```

## Const

### commitHead

[ref: #symbol-commithead]

```nim
commitHead = "HEAD"
```

## Proc

### diffFiles

[ref: #symbol-difffiles]

**Input:**
- `path1: string`
- `path2: string`

**Output:** `tuple[output: string, same: bool]`
**Pragmas:** `raises: [OSError, IOError, ValueError]`, `tags: [ExecIOEffect, ReadIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError, ValueError`, `tags: ExecIOEffect, ReadIOEffect, RootEffect`, `forbids: `

Returns a human readable diff of files path1, path2, the exact form of which is implementation defined.

### diffStrings

[ref: #symbol-diffstrings]

**Input:**
- `a: string`
- `b: string`

**Output:** `tuple[output: string, same: bool]`
**Pragmas:** `raises: [IOError, OSError, ValueError]`, `tags: [ReadEnvEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect, ExecIOEffect,
       RootEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError`, `tags: ReadEnvEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect, ExecIOEffect, RootEffect`, `forbids: `

Returns a human readable diff of a, b, the exact form of which is implementation defined. See also experimental.diff.

### isGitRepo

[ref: #symbol-isgitrepo]

**Input:**
- `dir: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: [ReadDirEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadDirEffect`, `forbids: `

Avoid calling git since it depends on /bin/sh existing and fails in Nix.

## Template

### retryCall

[ref: #symbol-retrycall]

**Input:**
- `maxRetry:  = 3`
- `backoffDuration:  = 1.0`
- `call: untyped`

**Output:** `bool`
Retry call up to maxRetry times with exponential backoff and initial duraton of backoffDuration seconds. This is in particular useful for network commands that can fail.
