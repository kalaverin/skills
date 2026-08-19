---
source_hash: 0b1e7c301b97daad
source_path: lib/nimhcr.nim
---

# nimhcr

[ref: #module-nimhcr]

## Proc

### hcrAddEventHandler

[ref: #symbol-hcraddeventhandler]

**Input:**
- `isBefore: bool`
- `cb: proc () {.nimcall.}`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### hcrAddModule

[ref: #symbol-hcraddmodule]

**Input:**
- `module: cstring`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hcrGeneration

[ref: #symbol-hcrgeneration]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hcrGetGlobal

[ref: #symbol-hcrgetglobal]

**Input:**
- `module: cstring`
- `name: cstring`

**Output:** `pointer`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### hcrGetProc

[ref: #symbol-hcrgetproc]

**Input:**
- `module: cstring`
- `name: cstring`

**Output:** `pointer`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### hcrHasModuleChanged

[ref: #symbol-hcrhasmodulechanged]

**Input:**
- `moduleHash: string`

**Output:** `bool`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### hcrInit

[ref: #symbol-hcrinit]

**Input:**
- `moduleList: ptr pointer`
- `main: cstring`
- `sys: cstring`
- `datInit: HcrModuleInitializer`
- `handle: pointer`
- `gpa: HcrProcGetter`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError, Exception, LibraryError]`, `tags: [ReadDirEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: KeyError, Exception, LibraryError`, `tags: ReadDirEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect, RootEffect`, `forbids: `

### hcrMarkGlobals

[ref: #symbol-hcrmarkglobals]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `nimcall`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

### hcrPerformCodeReload

[ref: #symbol-hcrperformcodereload]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError, Exception, LibraryError]`, `tags: [RootEffect, ReadDirEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect]`, `forbids: []`

**Effects:** `raises: KeyError, Exception, LibraryError`, `tags: RootEffect, ReadDirEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect`, `forbids: `

### hcrRegisterGlobal

[ref: #symbol-hcrregisterglobal]

**Input:**
- `module: cstring`
- `name: cstring`
- `size: Natural`
- `gcMarker: HcrGcMarkerProc`
- `outPtr: ptr pointer`

**Output:** `bool`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### hcrRegisterProc

[ref: #symbol-hcrregisterproc]

**Input:**
- `module: cstring`
- `name: cstring`
- `fn: pointer`

**Output:** `pointer`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError, OSError`, `tags: `, `forbids: `

### hcrReloadNeeded

[ref: #symbol-hcrreloadneeded]

**Input:**
- *(none)*

**Output:** `bool`
**Pragmas:** `compilerproc`, `exportc`, `dynlib`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

## Type

### HcrModuleInitializer

[ref: #symbol-hcrmoduleinitializer]

```nim
HcrModuleInitializer = proc () {.nimcall.}
```

### HcrProcGetter

[ref: #symbol-hcrprocgetter]

```nim
HcrProcGetter = proc (libHandle: pointer; procName: cstring): pointer {.nimcall.}
```
