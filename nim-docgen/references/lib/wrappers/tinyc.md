---
source_hash: ebacb35435ca8964
source_path: lib/wrappers/tinyc.nim
---

# tinyc

[ref: #module-tinyc]

## Const

### OutputDll

[ref: #symbol-outputdll]

```nim
OutputDll: cint = 3
```

dynamic library

### OutputExe

[ref: #symbol-outputexe]

```nim
OutputExe: cint = 2
```

executable file

### OutputMemory

[ref: #symbol-outputmemory]

```nim
OutputMemory: cint = 1
```

output will be ran in memory (no output file) (default)

### OutputObj

[ref: #symbol-outputobj]

```nim
OutputObj: cint = 4
```

object file

### OutputPreprocess

[ref: #symbol-outputpreprocess]

```nim
OutputPreprocess: cint = 5
```

preprocessed file (used internally)

## Proc

### addFile

[ref: #symbol-addfile]

**Input:**
- `s: PccState`
- `filename: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_add_file"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

add a file (either a C file, dll, an object, a library or an ld script). Return -1 if error.

### addIncludePath

[ref: #symbol-addincludepath]

**Input:**
- `s: PccState`
- `pathname: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_add_include_path"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

add include path

### addLibrary

[ref: #symbol-addlibrary]

**Input:**
- `s: PccState`
- `libraryname: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_add_library"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

the library name is the same as the argument of the '-l' option

### addLibraryPath

[ref: #symbol-addlibrarypath]

**Input:**
- `s: PccState`
- `pathname: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_add_library_path"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

equivalent to -Lpath option

### addSymbol

[ref: #symbol-addsymbol]

**Input:**
- `s: PccState`
- `name: cstring`
- `val: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_add_symbol"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

add a symbol to the compiled program

### addSysincludePath

[ref: #symbol-addsysincludepath]

**Input:**
- `s: PccState`
- `pathname: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_add_sysinclude_path"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

add in system include path

### closeCCState

[ref: #symbol-closeccstate]

**Input:**
- `s: PccState`

**Output:** *(none)*
**Pragmas:** `importc: "tcc_delete"`, `cdecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

free a TCC compilation context

### compileString

[ref: #symbol-compilestring]

**Input:**
- `s: PccState`
- `buf: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_compile_string"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

compile a string containing a C source. Return non zero if error.

### defineSymbol

[ref: #symbol-definesymbol]

**Input:**
- `s: PccState`
- `sym: cstring`
- `value: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_define_symbol"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

define preprocessor symbol 'sym'. Can put optional value

### getSymbol

[ref: #symbol-getsymbol]

**Input:**
- `s: PccState`
- `name: cstring`

**Output:** `pointer`
**Pragmas:** `cdecl`, `importc: "tcc_get_symbol"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

return symbol value or NULL if not found

### openCCState

[ref: #symbol-openccstate]

**Input:**
- *(none)*

**Output:** `PccState`
**Pragmas:** `importc: "tcc_new"`, `cdecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

create a new TCC compilation context

### outputFile

[ref: #symbol-outputfile]

**Input:**
- `s: PccState`
- `filename: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_output_file"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

output an executable, library or object file. DO NOT call tcc\_relocate() before.

### relocate

[ref: #symbol-relocate]

**Input:**
- `s: PccState`
- `p: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_relocate"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

copy code into memory passed in by the caller and do all relocations (needed before using tcc\_get\_symbol()). returns -1 on error and required size if ptr is NULL

### run

[ref: #symbol-run]

**Input:**
- `s: PccState`
- `argc: cint`
- `argv: cstringArray`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_run"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

link and run main() function and return its value. DO NOT call tcc\_relocate() before.

### setErrorFunc

[ref: #symbol-seterrorfunc]

**Input:**
- `s: PccState`
- `errorOpaque: pointer`
- `errorFun: ErrorFunc`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_set_error_func"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

set error/warning display callback

### setLibPath

[ref: #symbol-setlibpath]

**Input:**
- `s: PccState`
- `path: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_set_lib_path"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

set CONFIG\_TCCDIR at runtime

### setOptions

[ref: #symbol-setoptions]

**Input:**
- `s: PccState`
- `options: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_set_options"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

set a options

### setOutputType

[ref: #symbol-setoutputtype]

**Input:**
- `s: PccState`
- `outputType: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "tcc_set_output_type"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

set output type. MUST BE CALLED before any compilation

### undefineSymbol

[ref: #symbol-undefinesymbol]

**Input:**
- `s: PccState`
- `sym: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `importc: "tcc_undefine_symbol"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

undefine preprocess symbol 'sym'

## Type

### ErrorFunc

[ref: #symbol-errorfunc]

```nim
ErrorFunc = proc (opaque: pointer; msg: cstring) {.cdecl.}
```

### PccState

[ref: #symbol-pccstate]

```nim
PccState = ptr CcState
```
