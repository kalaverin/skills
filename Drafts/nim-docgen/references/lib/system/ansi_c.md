---
source_hash: 64a6d1e9d702c5b4
source_path: lib/system/ansi_c.nim
---

# ansi_c

[ref: #module-ansi_c]

## Const

### SIG_DFL

[ref: #symbol-sig-dfl]

```nim
SIG_DFL = nil
```

### SIGABRT

[ref: #symbol-sigabrt]

```nim
SIGABRT = 6'i32
```

### SIGBUS

[ref: #symbol-sigbus]

```nim
SIGBUS = 10'i32
```

### SIGFPE

[ref: #symbol-sigfpe]

```nim
SIGFPE = 8'i32
```

### SIGILL

[ref: #symbol-sigill]

```nim
SIGILL = 4'i32
```

### SIGINT

[ref: #symbol-sigint]

```nim
SIGINT = 2'i32
```

### SIGPIPE

[ref: #symbol-sigpipe]

```nim
SIGPIPE = 13'i32
```

### SIGSEGV

[ref: #symbol-sigsegv]

```nim
SIGSEGV = 11'i32
```

### SIGTERM

[ref: #symbol-sigterm]

```nim
SIGTERM = 15'i32
```

## Proc

### c_abort

[ref: #symbol-c-abort]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc: "abort"`, `header: "<stdlib.h>"`, `noSideEffect`, `noreturn`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_calloc

[ref: #symbol-c-calloc]

**Input:**
- `nmemb: csize_t`
- `size: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "calloc"`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_fflush

[ref: #symbol-c-fflush]

**Input:**
- `f: CFilePtr`

**Output:** `cint`
**Pragmas:** `importc: "fflush"`, `header: "<stdio.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_fprintf

[ref: #symbol-c-fprintf]

**Input:**
- `f: CFilePtr`
- `frmt: cstring`

**Output:** `cint`
**Pragmas:** `importc: "fprintf"`, `header: "<stdio.h>"`, `varargs`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_fputc

[ref: #symbol-c-fputc]

**Input:**
- `c: char`
- `f: CFilePtr`

**Output:** `cint`
**Pragmas:** `importc: "fputc"`, `header: "<stdio.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_fputs

[ref: #symbol-c-fputs]

**Input:**
- `c: cstring`
- `f: CFilePtr`

**Output:** `cint`
**Pragmas:** `importc: "fputs"`, `header: "<stdio.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_free

[ref: #symbol-c-free]

**Input:**
- `p: pointer`

**Output:** *(none)*
**Pragmas:** `importc: "free"`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_fwrite

[ref: #symbol-c-fwrite]

**Input:**
- `buf: pointer`
- `size: csize_t`
- `n: csize_t`
- `f: CFilePtr`

**Output:** `csize_t`
**Pragmas:** `importc: "fwrite"`, `header: "<stdio.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_longjmp

[ref: #symbol-c-longjmp]

**Input:**
- `jmpb: C_JmpBuf`
- `retval: cint`

**Output:** *(none)*
**Pragmas:** `header: "<setjmp.h>"`, `importc: "_longjmp"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_malloc

[ref: #symbol-c-malloc]

**Input:**
- `size: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "malloc"`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_memchr

[ref: #symbol-c-memchr]

**Input:**
- `s: pointer`
- `c: cint`
- `n: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "memchr"`, `header: "<string.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_memcmp

[ref: #symbol-c-memcmp]

**Input:**
- `a: pointer`
- `b: pointer`
- `size: csize_t`

**Output:** `cint`
**Pragmas:** `importc: "memcmp"`, `header: "<string.h>"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_memcpy

[ref: #symbol-c-memcpy]

**Input:**
- `a: pointer`
- `b: pointer`
- `size: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "memcpy"`, `header: "<string.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_memmove

[ref: #symbol-c-memmove]

**Input:**
- `a: pointer`
- `b: pointer`
- `size: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "memmove"`, `header: "<string.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_memset

[ref: #symbol-c-memset]

**Input:**
- `p: pointer`
- `value: cint`
- `size: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "memset"`, `header: "<string.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_printf

[ref: #symbol-c-printf]

**Input:**
- `frmt: cstring`

**Output:** `cint`
**Pragmas:** `importc: "printf"`, `header: "<stdio.h>"`, `varargs`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_raise

[ref: #symbol-c-raise]

**Input:**
- `sign: cint`

**Output:** `cint`
**Pragmas:** `importc: "raise"`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_realloc

[ref: #symbol-c-realloc]

**Input:**
- `p: pointer`
- `newsize: csize_t`

**Output:** `pointer`
**Pragmas:** `importc: "realloc"`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_setjmp

[ref: #symbol-c-setjmp]

**Input:**
- `jmpb: C_JmpBuf`

**Output:** `cint`
**Pragmas:** `header: "<setjmp.h>"`, `importc: "_setjmp"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_signal

[ref: #symbol-c-signal]

**Input:**
- `sign: cint`
- `handler: CSighandlerT`

**Output:** `CSighandlerT`
**Pragmas:** `importc: "signal"`, `header: "<signal.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_snprintf

[ref: #symbol-c-snprintf]

**Input:**
- `buf: cstring`
- `n: csize_t`
- `frmt: cstring`

**Output:** `cint`
**Pragmas:** `importc: "snprintf"`, `header: "<stdio.h>"`, `varargs`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_sprintf

[ref: #symbol-c-sprintf]

**Input:**
- `buf: cstring`
- `frmt: cstring`

**Output:** `cint`
**Pragmas:** `importc: "sprintf"`, `header: "<stdio.h>"`, `varargs`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_strcmp

[ref: #symbol-c-strcmp]

**Input:**
- `a: cstring`
- `b: cstring`

**Output:** `cint`
**Pragmas:** `importc: "strcmp"`, `header: "<string.h>"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_strlen

[ref: #symbol-c-strlen]

**Input:**
- `a: cstring`

**Output:** `csize_t`
**Pragmas:** `importc: "strlen"`, `header: "<string.h>"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### c_strstr

[ref: #symbol-c-strstr]

**Input:**
- `haystack: cstring`
- `needle: cstring`

**Output:** `cstring`
**Pragmas:** `importc: "strstr"`, `header: "<string.h>"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rawWrite

[ref: #symbol-rawwrite]

**Input:**
- `f: CFilePtr`
- `s: cstring`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `nonReloadable`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rawWriteString

[ref: #symbol-rawwritestring]

**Input:**
- `f: CFilePtr`
- `s: cstring`
- `length: int`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `nonReloadable`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### C_JmpBuf

[ref: #symbol-c-jmpbuf]

```nim
C_JmpBuf {.importc: "jmp_buf", header: "<setjmp.h>".} = object
```

### CFilePtr

[ref: #symbol-cfileptr]

```nim
CFilePtr = ptr CFile
```

The type representing a file handle.

## Var

### cstderr

[ref: #symbol-cstderr]

```nim
cstderr {.importc: "__stderrp", header: "<stdio.h>".}: CFilePtr
```

### cstdin

[ref: #symbol-cstdin]

```nim
cstdin {.importc: "__stdinp", header: "<stdio.h>".}: CFilePtr
```

### cstdout

[ref: #symbol-cstdout]

```nim
cstdout {.importc: "__stdoutp", header: "<stdio.h>".}: CFilePtr
```
