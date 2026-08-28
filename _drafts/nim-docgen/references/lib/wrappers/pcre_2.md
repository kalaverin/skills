---
source_hash: ace26bbf795b20ce
source_path: lib/wrappers/pcre.nim
---

### PCRE_DATE

[ref: #symbol-pcre-date]

```nim
PCRE_DATE = "2014-09-26"
```

### PCRE_MAJOR

[ref: #symbol-pcre-major]

```nim
PCRE_MAJOR = 8
```

### PCRE_MINOR

[ref: #symbol-pcre-minor]

```nim
PCRE_MINOR = 36
```

### PCRE_PRERELEASE

[ref: #symbol-pcre-prerelease]

```nim
PCRE_PRERELEASE = true
```

### STUDY_EXTRA_NEEDED

[ref: #symbol-study-extra-needed]

```nim
STUDY_EXTRA_NEEDED = 0x00000008
```

### STUDY_JIT_COMPILE

[ref: #symbol-study-jit-compile]

```nim
STUDY_JIT_COMPILE = 0x00000001
```

### STUDY_JIT_PARTIAL_HARD_COMPILE

[ref: #symbol-study-jit-partial-hard-compile]

```nim
STUDY_JIT_PARTIAL_HARD_COMPILE = 0x00000004
```

### STUDY_JIT_PARTIAL_SOFT_COMPILE

[ref: #symbol-study-jit-partial-soft-compile]

```nim
STUDY_JIT_PARTIAL_SOFT_COMPILE = 0x00000002
```

### UCP

[ref: #symbol-ucp]

```nim
UCP = 0x20000000
```

### UNGREEDY

[ref: #symbol-ungreedy]

```nim
UNGREEDY = 0x00000200
```

### UTF16

[ref: #symbol-utf16]

```nim
UTF16 = 0x00000800
```

### UTF16_ERR0

[ref: #symbol-utf16-err0]

```nim
UTF16_ERR0 = 0
```

### UTF16_ERR1

[ref: #symbol-utf16-err1]

```nim
UTF16_ERR1 = 1
```

### UTF16_ERR2

[ref: #symbol-utf16-err2]

```nim
UTF16_ERR2 = 2
```

### UTF16_ERR3

[ref: #symbol-utf16-err3]

```nim
UTF16_ERR3 = 3
```

### UTF16_ERR4

[ref: #symbol-utf16-err4]

```nim
UTF16_ERR4 = 4
```

### UTF32

[ref: #symbol-utf32]

```nim
UTF32 = 0x00000800
```

### UTF32_ERR0

[ref: #symbol-utf32-err0]

```nim
UTF32_ERR0 = 0
```

### UTF32_ERR1

[ref: #symbol-utf32-err1]

```nim
UTF32_ERR1 = 1
```

### UTF32_ERR2

[ref: #symbol-utf32-err2]

```nim
UTF32_ERR2 = 2
```

### UTF32_ERR3

[ref: #symbol-utf32-err3]

```nim
UTF32_ERR3 = 3
```

### UTF8

[ref: #symbol-utf8]

```nim
UTF8 = 0x00000800
```

### UTF8_ERR0

[ref: #symbol-utf8-err0]

```nim
UTF8_ERR0 = 0
```

### UTF8_ERR1

[ref: #symbol-utf8-err1]

```nim
UTF8_ERR1 = 1
```

### UTF8_ERR10

[ref: #symbol-utf8-err10]

```nim
UTF8_ERR10 = 10
```

### UTF8_ERR11

[ref: #symbol-utf8-err11]

```nim
UTF8_ERR11 = 11
```

### UTF8_ERR12

[ref: #symbol-utf8-err12]

```nim
UTF8_ERR12 = 12
```

### UTF8_ERR13

[ref: #symbol-utf8-err13]

```nim
UTF8_ERR13 = 13
```

### UTF8_ERR14

[ref: #symbol-utf8-err14]

```nim
UTF8_ERR14 = 14
```

### UTF8_ERR15

[ref: #symbol-utf8-err15]

```nim
UTF8_ERR15 = 15
```

### UTF8_ERR16

[ref: #symbol-utf8-err16]

```nim
UTF8_ERR16 = 16
```

### UTF8_ERR17

[ref: #symbol-utf8-err17]

```nim
UTF8_ERR17 = 17
```

### UTF8_ERR18

[ref: #symbol-utf8-err18]

```nim
UTF8_ERR18 = 18
```

### UTF8_ERR19

[ref: #symbol-utf8-err19]

```nim
UTF8_ERR19 = 19
```

### UTF8_ERR2

[ref: #symbol-utf8-err2]

```nim
UTF8_ERR2 = 2
```

### UTF8_ERR20

[ref: #symbol-utf8-err20]

```nim
UTF8_ERR20 = 20
```

### UTF8_ERR21

[ref: #symbol-utf8-err21]

```nim
UTF8_ERR21 = 21
```

### UTF8_ERR22

[ref: #symbol-utf8-err22]

```nim
UTF8_ERR22 = 22
```

### UTF8_ERR3

[ref: #symbol-utf8-err3]

```nim
UTF8_ERR3 = 3
```

### UTF8_ERR4

[ref: #symbol-utf8-err4]

```nim
UTF8_ERR4 = 4
```

### UTF8_ERR5

[ref: #symbol-utf8-err5]

```nim
UTF8_ERR5 = 5
```

### UTF8_ERR6

[ref: #symbol-utf8-err6]

```nim
UTF8_ERR6 = 6
```

### UTF8_ERR7

[ref: #symbol-utf8-err7]

```nim
UTF8_ERR7 = 7
```

### UTF8_ERR8

[ref: #symbol-utf8-err8]

```nim
UTF8_ERR8 = 8
```

### UTF8_ERR9

[ref: #symbol-utf8-err9]

```nim
UTF8_ERR9 = 9
```

## Proc

### assign_jit_stack

[ref: #symbol-assign-jit-stack]

**Input:**
- `extra: ptr ExtraData`
- `callback: JitCallback`
- `data: pointer`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### compile

[ref: #symbol-compile]

**Input:**
- `pattern: cstring`
- `options: cint`
- `errptr: ptr cstring`
- `erroffset: ptr cint`
- `tableptr: pointer`

**Output:** `ptr Pcre`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### compile2

[ref: #symbol-compile2]

**Input:**
- `pattern: cstring`
- `options: cint`
- `errorcodeptr: ptr cint`
- `errptr: ptr cstring`
- `erroffset: ptr cint`
- `tableptr: pointer`

**Output:** `ptr Pcre`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### config

[ref: #symbol-config]

**Input:**
- `what: cint`
- `where: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### copy_named_substring

[ref: #symbol-copy-named-substring]

**Input:**
- `code: ptr Pcre`
- `subject: cstring`
- `ovector: ptr cint`
- `stringcount: cint`
- `stringname: cstring`
- `buffer: cstring`
- `buffersize: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### copy_substring

[ref: #symbol-copy-substring]

**Input:**
- `subject: cstring`
- `ovector: ptr cint`
- `stringcount: cint`
- `stringnumber: cint`
- `buffer: cstring`
- `buffersize: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dfa_exec

[ref: #symbol-dfa-exec]

**Input:**
- `code: ptr Pcre`
- `extra: ptr ExtraData`
- `subject: cstring`
- `length: cint`
- `startoffset: cint`
- `options: cint`
- `ovector: ptr cint`
- `ovecsize: cint`
- `workspace: ptr cint`
- `wscount: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### exec

[ref: #symbol-exec]

**Input:**
- `code: ptr Pcre`
- `extra: ptr ExtraData`
- `subject: cstring`
- `length: cint`
- `startoffset: cint`
- `options: cint`
- `ovector: ptr cint`
- `ovecsize: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### free_study

[ref: #symbol-free-study]

**Input:**
- `extra: ptr ExtraData`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### free_substring

[ref: #symbol-free-substring]

**Input:**
- `stringptr: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### free_substring_list

[ref: #symbol-free-substring-list]

**Input:**
- `stringptr: cstringArray`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fullinfo

[ref: #symbol-fullinfo]

**Input:**
- `code: ptr Pcre`
- `extra: ptr ExtraData`
- `what: cint`
- `where: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### get_named_substring

[ref: #symbol-get-named-substring]

**Input:**
- `code: ptr Pcre`
- `subject: cstring`
- `ovector: ptr cint`
- `stringcount: cint`
- `stringname: cstring`
- `stringptr: cstringArray`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### get_stringnumber

[ref: #symbol-get-stringnumber]

**Input:**
- `code: ptr Pcre`
- `name: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### get_stringtable_entries

[ref: #symbol-get-stringtable-entries]

**Input:**
- `code: ptr Pcre`
- `name: cstring`
- `first: cstringArray`
- `last: cstringArray`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### get_substring

[ref: #symbol-get-substring]

**Input:**
- `subject: cstring`
- `ovector: ptr cint`
- `stringcount: cint`
- `stringnumber: cint`
- `stringptr: cstringArray`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### get_substring_list

[ref: #symbol-get-substring-list]

**Input:**
- `subject: cstring`
- `ovector: ptr cint`
- `stringcount: cint`
- `listptr: ptr cstringArray`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### jit_exec

[ref: #symbol-jit-exec]

**Input:**
- `code: ptr Pcre`
- `extra: ptr ExtraData`
- `subject: cstring`
- `length: cint`
- `startoffset: cint`
- `options: cint`
- `ovector: ptr cint`
- `ovecsize: cint`
- `jstack: ptr JitStack`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### jit_free_unused_memory

[ref: #symbol-jit-free-unused-memory]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### jit_stack_alloc

[ref: #symbol-jit-stack-alloc]

**Input:**
- `startsize: cint`
- `maxsize: cint`

**Output:** `ptr JitStack`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### jit_stack_free

[ref: #symbol-jit-stack-free]

**Input:**
- `stack: ptr JitStack`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### maketables

[ref: #symbol-maketables]

**Input:**
- *(none)*

**Output:** `pointer`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pattern_to_host_byte_order

[ref: #symbol-pattern-to-host-byte-order]

**Input:**
- `code: ptr Pcre`
- `extra: ptr ExtraData`
- `tables: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### refcount

[ref: #symbol-refcount]

**Input:**
- `code: ptr Pcre`
- `adjust: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### study

[ref: #symbol-study]

**Input:**
- `code: ptr Pcre`
- `options: cint`
- `errptr: ptr cstring`

**Output:** `ptr ExtraData`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### study

[ref: #symbol-study]

**Input:**
- `code: ptr Pcre`
- `options: cint`
- `errptr: var cstring`

**Output:** `ptr ExtraData`
**Pragmas:** `deprecated`, `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### version

[ref: #symbol-version]

**Input:**
- *(none)*

**Output:** `cstring`
**Pragmas:** `cdecl`, `importc: "pcre_$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### CalloutBlock

[ref: #symbol-calloutblock]

```nim
CalloutBlock = object
  version*: cint             ## Identifies version of block
  callout_number*: cint      ## Number compiled into pattern
  offset_vector*: ptr cint   ## The offset vector
  subject*: cstring          ## The subject being matched
  subject_length*: cint      ## The length of the subject
  start_match*: cint         ## Offset to start of this match attempt
  current_position*: cint    ## Where we currently are in the subject
  capture_top*: cint         ## Max current capture
  capture_last*: cint        ## Most recently closed capture
  callout_data*: pointer     ## Data passed in with the call
  pattern_position*: cint    ## Offset to next item in the pattern
  next_item_length*: cint    ## Length of next item in the pattern
  mark*: pointer             ## Pointer to current mark or NULL
```

### ExtraData

[ref: #symbol-extradata]

```nim
ExtraData = object
  flags*: clong              ## Bits for which fields are set
  study_data*: pointer       ## Opaque data from pcre_study()
  match_limit*: clong        ## Maximum number of calls to match()
  callout_data*: pointer     ## Data passed back in callouts
  tables*: pointer           ## Pointer to character tables
  match_limit_recursion*: clong ## Max recursive calls to match()
  mark*: pointer             ## For passing back a mark pointer
  executable_jit*: pointer   ## Contains a pointer to a compiled jit code
```

### JitCallback

[ref: #symbol-jitcallback]

```nim
JitCallback = proc (a: pointer): ptr JitStack {.cdecl.}
```

### JitStack

[ref: #symbol-jitstack]

```nim
JitStack = object
```

### JitStack16

[ref: #symbol-jitstack16]

```nim
JitStack16 = object
```

### JitStack32

[ref: #symbol-jitstack32]

```nim
JitStack32 = object
```

### Pcre

[ref: #symbol-pcre]

```nim
Pcre = object
```

### Pcre16

[ref: #symbol-pcre16]

```nim
Pcre16 = object
```

### Pcre32

[ref: #symbol-pcre32]

```nim
Pcre32 = object
```

### PJitStack

[ref: #symbol-pjitstack]

```nim
PJitStack {.deprecated.} = ptr JitStack
```

### PPcre

[ref: #symbol-ppcre]

```nim
PPcre {.deprecated.} = ptr Pcre
```

[Prev](pcre_1.md)
