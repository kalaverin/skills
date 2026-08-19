---
source_hash: cf862a7a8ed347ee
source_path: lib/js/jsconsole.nim
---

# jsconsole

[ref: #module-jsconsole]

Wrapper for the console object for the [JavaScript backend](backends.html#backends-the-javascript-target).

# [Styled Messages](#styled-messages)

CSS-styled messages in the browser are useful for debugging purposes. To use them, prefix the message with one or more %c, and provide the CSS style as the last argument. The amount of %c's must match the amount of CSS-styled strings.

## Examples

```nim
import std/jsconsole
console.log "%c My Debug Message", "color: red" # Notice the "%c"
console.log "%c My Debug %c Message", "color: red", "font-size: 2em"
```

```nim
console.jsAssert(42 == 42) # OK
console.jsAssert(42 != 42) # Fail, prints "Assertion failed" and continues
console.jsAssert('`' == '\n' and '\t' == '\0') # Message correctly formatted
assert 42 == 42  # Normal assertions keep working
```

## Proc

### clear

[ref: #symbol-clear]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/clear>

### count

[ref: #symbol-count]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/count>

### countReset

[ref: #symbol-countreset]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/countReset>

### debug

[ref: #symbol-debug]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/debug>

### dir

[ref: #symbol-dir]

**Input:**
- `console: Console`
- `obj: auto`

**Output:** *(none)*
**Generic parameters:** `obj:type`

**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Console/dir>

### dirxml

[ref: #symbol-dirxml]

**Input:**
- `console: Console`
- `obj: auto`

**Output:** *(none)*
**Generic parameters:** `obj:type`

**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Console/dirxml>

### error

[ref: #symbol-error]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/error>

### group

[ref: #symbol-group]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/group>

### groupCollapsed

[ref: #symbol-groupcollapsed]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Console/groupCollapsed>

### groupEnd

[ref: #symbol-groupend]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/groupEnd>

### info

[ref: #symbol-info]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/info>

### log

[ref: #symbol-log]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/log>

### table

[ref: #symbol-table]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/table>

### time

[ref: #symbol-time]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/time>

### timeEnd

[ref: #symbol-timeend]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/timeEnd>

### timeLog

[ref: #symbol-timelog]

**Input:**
- `console: Console`
- `label:  = "".cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/timeLog>

### timeStamp

[ref: #symbol-timestamp]

<https://developer.mozilla.org/en-US/docs/Web/API/Console/timeStamp>

**Input:**
- `console: Console`
- `label: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Console/timeStamp>

..warning:: non-standard

### trace

[ref: #symbol-trace]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/trace>

### warn

[ref: #symbol-warn]

**Input:**
- `console: Console`

**Output:** *(none)*
**Pragmas:** `importcpp`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/docs/Web/API/Console/warn>

## Template

### exception

[ref: #symbol-exception]

**Input:**
- `console: Console`
- `args: varargs[untyped]`

**Output:** *(none)*
Alias for console.error().

### jsAssert

[ref: #symbol-jsassert]

**Input:**
- `console: Console`
- `assertion: `

**Output:** *(none)*
JavaScript console.assert, for NodeJS this prints to stderr, assert failure just prints to console and do not quit the program, this is not meant to be better or even equal than normal assertions, is just for when you need faster performance *and* assertions, otherwise use the normal assertions for better user experience. <https://developer.mozilla.org/en-US/docs/Web/API/Console/assert>

## Type

### Console

[ref: #symbol-console]

```nim
Console = ref object of JsRoot
```

## Var

### console

[ref: #symbol-console]

```nim
console {.importc, nodecl.}: Console
```
