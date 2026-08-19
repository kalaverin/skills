---
source_hash: d640e6dc83860c91
source_path: lib/std/assertions.nim
---

# assertions

[ref: #module-assertions]

This module implements assertion handling.

## Examples

```nim
assert 1 == 1
```

```nim
assert 1 == 2 # no code generated, no failure here
```

```nim
assert 1 == 2 # ditto
```

```nim
doAssert 1 == 1 # generates code even when built with `-d:danger` or `--assertions:off`
```

```nim
doAssertRaises(ValueError): raise newException(ValueError, "Hello World")
doAssertRaises(CatchableError): raise newException(ValueError, "Hello World")
doAssertRaises(AssertionDefect): doAssert false
```

```nim
type MyError = object of CatchableError
  lineinfo: tuple[filename: string, line: int, column: int]
# block-wide policy to change the failed assert exception type in order to
# include a lineinfo
onFailedAssert(msg):
  raise (ref MyError)(msg: msg, lineinfo: instantiationInfo(-2))
doAssertRaises(MyError): doAssert false
```

## Proc

### failedAssertImpl

[ref: #symbol-failedassertimpl]

**Input:**
- `msg: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Raises an AssertionDefect with msg, but this is hidden from the effect system. Called when an assertion failed.

### raiseAssert

[ref: #symbol-raiseassert]

**Input:**
- `msg: string`

**Output:** *(none)*
**Pragmas:** `noinline`, `noreturn`, `nosinks`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Raises an AssertionDefect with msg.

## Template

### assert

[ref: #symbol-assert]

Raises AssertionDefect with msg if cond is false. Note that AssertionDefect is hidden from the effect system, so it doesn't produce {.raises: [AssertionDefect].}. This exception is only supposed to be caught by unit testing frameworks.

**Input:**
- `cond: untyped`
- `msg:  = ""`

**Output:** *(none)*
Raises AssertionDefect with msg if cond is false. Note that AssertionDefect is hidden from the effect system, so it doesn't produce {.raises: [AssertionDefect].}. This exception is only supposed to be caught by unit testing frameworks.

No code will be generated for assert when passing -d:danger (implied by --assertions:off). See [command line switches](nimc.html#compiler-usage-commandminusline-switches).

### doAssert

[ref: #symbol-doassert]

**Input:**
- `cond: untyped`
- `msg:  = ""`

**Output:** *(none)*
Similar to [assert](#assert.t,untyped,string) but is always turned on regardless of --assertions.

### doAssertRaises

[ref: #symbol-doassertraises]

**Input:**
- `exception: typedesc`
- `code: untyped`

**Output:** *(none)*
**Generic parameters:** `exception:type`

Raises AssertionDefect if specified code does not raise exception.

### onFailedAssert

[ref: #symbol-onfailedassert]

**Input:**
- `msg: untyped`
- `code: untyped`

**Output:** `untyped`
**Pragmas:** `dirty`

Sets an assertion failure handler that will intercept any assert statements following onFailedAssert in the current scope.
