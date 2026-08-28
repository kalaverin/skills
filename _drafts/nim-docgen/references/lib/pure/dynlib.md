---
source_hash: a54c9b37ff80983b
source_path: lib/pure/dynlib.nim
---

# dynlib

[ref: #module-dynlib]

This module implements the ability to access symbols from shared libraries. On POSIX this uses the dlsym mechanism, on Windows LoadLibrary.

# [Examples](#examples)

## [Loading a simple C function](#examples-loading-a-simple-c-function)

The following example demonstrates loading a function called greet from a library that is determined at runtime based upon a language choice. If the library fails to load or the function greet is not found, it quits with a failure error code.

## Examples

```nim
import std/dynlib
type
  GreetFunction = proc (): cstring {.gcsafe, stdcall.}

proc loadGreet(lang: string) =
  let lib =
    case lang
    of "french":
      loadLib("french.dll")
    else:
      loadLib("english.dll")
  assert lib != nil, "Error loading library"

  let greet = cast[GreetFunction](lib.symAddr("greet"))
  assert greet != nil, "Error loading 'greet' function from library"

  echo greet()

  unloadLib(lib)
```

## Proc

### checkedSymAddr

[ref: #symbol-checkedsymaddr]

**Input:**
- `lib: LibHandle`
- `name: cstring`

**Output:** `pointer`
**Pragmas:** `raises: [Exception, LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, LibraryError`, `tags: RootEffect`, `forbids: `

Retrieves the address of a procedure/variable from lib. Raises LibraryError if the symbol could not be found.

### libCandidates

[ref: #symbol-libcandidates]

**Input:**
- `s: string`
- `dest: var seq[string]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Given a library name pattern s, write possible library names to dest.

### loadLib

[ref: #symbol-loadlib]

**Input:**
- `path: string`
- `globalSymbols:  = false`

**Output:** `LibHandle`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Loads a library from path. Returns nil if the library could not be loaded.

### loadLib

[ref: #symbol-loadlib]

**Input:**
- *(none)*

**Output:** `LibHandle`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the handle from the current executable. Returns nil if the library could not be loaded.

### loadLibPattern

[ref: #symbol-loadlibpattern]

Loads a library with name matching pattern, similar to what the dynlib pragma does. Returns nil if the library could not be loaded.

**Input:**
- `pattern: string`
- `globalSymbols:  = false`

**Output:** `LibHandle`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Loads a library with name matching pattern, similar to what the dynlib pragma does. Returns nil if the library could not be loaded.

**Warning:**
this proc uses the GC and so cannot be used to load the GC.

### raiseInvalidLibrary

[ref: #symbol-raiseinvalidlibrary]

**Input:**
- `name: cstring`

**Output:** *(none)*
**Pragmas:** `noinline`, `noreturn`, `raises: [LibraryError]`, `tags: []`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: `, `forbids: `

Raises a LibraryError exception.

### symAddr

[ref: #symbol-symaddr]

**Input:**
- `lib: LibHandle`
- `name: cstring`

**Output:** `pointer`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the address of a procedure/variable from lib. Returns nil if the symbol could not be found.

### unloadLib

[ref: #symbol-unloadlib]

**Input:**
- `lib: LibHandle`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unloads the library lib.

## Type

### LibHandle

[ref: #symbol-libhandle]

```nim
LibHandle = pointer
```

A handle to a dynamically loaded library.
