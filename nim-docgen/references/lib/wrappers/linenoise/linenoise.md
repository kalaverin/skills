---
source_hash: 59a36621216a0e78
source_path: lib/wrappers/linenoise/linenoise.nim
---

# linenoise

[ref: #module-linenoise]

## Examples

```nim
var ret: ReadLineResult
while true:
  readLineStatus("name: ", ret) # ctrl-D will exit, ctrl-C will go to next prompt
  if ret.line.len > 0: echo ret.line
  if ret.status == lnCtrlD: break
echo "exiting"
```

## Proc

### addCompletion

[ref: #symbol-addcompletion]

**Input:**
- `a2: ptr Completions`
- `a3: cstring`

**Output:** *(none)*
**Pragmas:** `importc: "linenoiseAddCompletion"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clearScreen

[ref: #symbol-clearscreen]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc: "linenoiseClearScreen"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### free

[ref: #symbol-free]

**Input:**
- `s: cstring`

**Output:** *(none)*
**Pragmas:** `importc: "free"`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### historyAdd

[ref: #symbol-historyadd]

**Input:**
- `line: cstring`

**Output:** `cint`
**Pragmas:** `importc: "linenoiseHistoryAdd"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### historyLoad

[ref: #symbol-historyload]

**Input:**
- `filename: cstring`

**Output:** `cint`
**Pragmas:** `importc: "linenoiseHistoryLoad"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### historySave

[ref: #symbol-historysave]

**Input:**
- `filename: cstring`

**Output:** `cint`
**Pragmas:** `importc: "linenoiseHistorySave"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### historySetMaxLen

[ref: #symbol-historysetmaxlen]

**Input:**
- `len: cint`

**Output:** `cint`
**Pragmas:** `importc: "linenoiseHistorySetMaxLen"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### printKeyCodes

[ref: #symbol-printkeycodes]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc: "linenoisePrintKeyCodes"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readLine

[ref: #symbol-readline]

**Input:**
- `prompt: cstring`

**Output:** `cstring`
**Pragmas:** `importc: "linenoise"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readLineStatus

[ref: #symbol-readlinestatus]

**Input:**
- `prompt: string`
- `result: var ReadLineResult`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

line editing API that allows returning the line entered and an indicator of which control key was entered, allowing user to distinguish between for example ctrl-C vs ctrl-D.

### setCompletionCallback

[ref: #symbol-setcompletioncallback]

**Input:**
- `a2: CompletionCallback`

**Output:** *(none)*
**Pragmas:** `importc: "linenoiseSetCompletionCallback"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setMultiLine

[ref: #symbol-setmultiline]

**Input:**
- `ml: cint`

**Output:** *(none)*
**Pragmas:** `importc: "linenoiseSetMultiLine"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### CompletionCallback

[ref: #symbol-completioncallback]

```nim
CompletionCallback = proc (a2: cstring; a3: ptr Completions) {.cdecl.}
```

### Completions

[ref: #symbol-completions]

```nim
Completions = object
  len*: csize_t
  cvec*: cstringArray
```

### LinenoiseData

[ref: #symbol-linenoisedata]

```nim
LinenoiseData = object
```

### ReadLineResult

[ref: #symbol-readlineresult]

```nim
ReadLineResult = object
  line*: string
  status*: Status
```

### Status

[ref: #symbol-status]

```nim
Status = enum
  lnCtrlUnkown, lnCtrlC, lnCtrlD
```
