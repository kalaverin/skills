---
source_hash: 5076e0f317804c90
source_path: lib/system/compilation.nim
---

# compilation

[ref: #module-compilation]

## Const

### CompileDate

[ref: #symbol-compiledate]

```nim
CompileDate {.magic: "CompileDate".}: string = "0000-00-00"
```

The date (in UTC) of compilation as a string of the form YYYY-MM-DD. This works thanks to compiler magic.

### CompileTime

[ref: #symbol-compiletime]

```nim
CompileTime {.magic: "CompileTime".}: string = "00:00:00"
```

The time (in UTC) of compilation as a string of the form HH:MM:SS. This works thanks to compiler magic.

### isMainModule

[ref: #symbol-ismainmodule]

```nim
isMainModule {.magic: "IsMainModule".}: bool = false
```

True only when accessed in the main module. This works thanks to compiler magic. It is useful to embed testing code in a module.

### NimMajor

[ref: #symbol-nimmajor]

is the major number of Nim's version. Example:

```nim
NimMajor {.intdefine.}: int = 2
```

is the major number of Nim's version. Example:

```
when (NimMajor, NimMinor, NimPatch) >= (1, 3, 1): discard
```

### NimMinor

[ref: #symbol-nimminor]

```nim
NimMinor {.intdefine.}: int = 2
```

is the minor number of Nim's version. Odd for devel, even for releases.

### NimPatch

[ref: #symbol-nimpatch]

```nim
NimPatch {.intdefine.}: int = 11
```

is the patch number of Nim's version. Odd for devel, even for releases.

## Let

### nimvm

[ref: #symbol-nimvm]

```nim
nimvm {.magic: "Nimvm", compileTime.}: bool = false
```

May be used only in when expression. It is true in Nim VM context and false otherwise.

## Proc

### astToStr

[ref: #symbol-asttostr]

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

**Pragmas:** `magic: "AstToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the AST of x into a string representation. This is very useful for debugging.

### compileOption

[ref: #symbol-compileoption]

Can be used to determine an on|off compile-time option.

**Input:**
- `option: string`

**Output:** `bool`
**Pragmas:** `magic: "CompileOption"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Can be used to determine an on|off compile-time option.

See also:

* [compileOption](#compileOption,string,string) for enum options
* [defined](#defined,untyped)
* [std/compilesettings module](compilesettings.html)

### compileOption

[ref: #symbol-compileoption]

Can be used to determine an enum compile-time option.

**Input:**
- `option: string`
- `arg: string`

**Output:** `bool`
**Pragmas:** `magic: "CompileOptionArg"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Can be used to determine an enum compile-time option.

See also:

* [compileOption](#compileOption,string) for on|off options
* [defined](#defined,untyped)
* [std/compilesettings module](compilesettings.html)

### compiles

[ref: #symbol-compiles]

Special compile-time procedure that checks whether x can be compiled without any semantic error. This can be used to check whether a type supports some operation:

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "Compiles"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x can be compiled without any semantic error. This can be used to check whether a type supports some operation:

```
when compiles(3 + 4):
  echo "'+' for integers is available"
```

### declared

[ref: #symbol-declared]

Special compile-time procedure that checks whether x is declared. x has to be an identifier or a qualified identifier.

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "Declared"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x is declared. x has to be an identifier or a qualified identifier.

This can be used to check whether a library provides a certain feature or not:

```
when not declared(strutils.toUpper):
  # provide our own toUpper proc here, because strutils is
  # missing it.
```

See also:

* [declaredInScope](#declaredInScope,untyped)

### declaredInScope

[ref: #symbol-declaredinscope]

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "DeclaredInScope"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x is declared in the current scope. x has to be an identifier.

### defined

[ref: #symbol-defined]

Special compile-time procedure that checks whether x is defined.

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "Defined"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x is defined.

x is an external symbol introduced through the compiler's [-d:x switch](nimc.html#compiler-usage-compileminustime-symbols) to enable build time conditionals:

```
when not defined(release):
  # Do here programmer friendly expensive sanity checks.
# Put here the normal code
```

See also:

* [compileOption](#compileOption,string) for on|off options
* [compileOption](#compileOption,string,string) for enum options
* [define pragmas](manual.html#implementation-specific-pragmas-compileminustime-define-pragmas)

### gorge

[ref: #symbol-gorge]

**Input:**
- `command: string`
- `input:  = ""`
- `cache:  = ""`

**Output:** `string`
**Pragmas:** `magic: "StaticExec"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is an alias for [staticExec](#staticExec,string,string,string).

### gorgeEx

[ref: #symbol-gorgeex]

**Input:**
- `command: string`
- `input:  = ""`
- `cache:  = ""`

**Output:** `tuple[output: string, exitCode: int]`
**Pragmas:** `noinit`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Similar to [gorge](#gorge,string,string,string) but also returns the precious exit code.

### runnableExamples

[ref: #symbol-runnableexamples]

A section you should use to mark runnable example code with.

**Input:**
- `rdoccmd:  = ""`
- `body: untyped`

**Output:** *(none)*
**Pragmas:** `magic: "RunnableExamples"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A section you should use to mark runnable example code with.

* In normal debug and release builds code within a runnableExamples section is ignored.
* The documentation generator is aware of these examples and considers them part of the ## doc comment. As the last step of documentation generation each runnableExample is put in its own file $file\_examples$i.nim, compiled and tested. The collected examples are put into their own module to ensure the examples do not refer to non-exported symbols.

### slurp

[ref: #symbol-slurp]

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `magic: "Slurp"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is an alias for [staticRead](#staticRead,string).

### staticExec

[ref: #symbol-staticexec]

Executes an external process at compile-time and returns its text output (stdout + stderr).

**Input:**
- `command: string`
- `input:  = ""`
- `cache:  = ""`

**Output:** `string`
**Pragmas:** `magic: "StaticExec"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Executes an external process at compile-time and returns its text output (stdout + stderr).

If input is not an empty string, it will be passed as a standard input to the executed program.

```
const buildInfo = "Revision " & staticExec("git rev-parse HEAD") &
                  "\nCompiled on " & staticExec("uname -v")
```

[gorge](#gorge,string,string,string) is an alias for staticExec.

Note that you can use this proc inside a pragma like [passc](manual.html#implementation-specific-pragmas-passc-pragma) or [passl](manual.html#implementation-specific-pragmas-passl-pragma).

If cache is not empty, the results of staticExec are cached within the nimcache directory. Use --forceBuild to get rid of this caching behaviour then. command & input & cache (the concatenated string) is used to determine whether the entry in the cache is still valid. You can use versioning information for cache:

```
const stateMachine = staticExec("dfaoptimizer", "input", "0.8.0")
```

### staticRead

[ref: #symbol-staticread]

Compile-time [readFile](syncio.html#readFile,string) proc for easy resource embedding:

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `magic: "Slurp"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compile-time [readFile](syncio.html#readFile,string) proc for easy resource embedding:

The maximum file size limit that staticRead and slurp can read is near or equal to the *free* memory of the device you are using to compile.

```
const myResource = staticRead"mydatafile.bin"
```

[slurp](#slurp,string) is an alias for staticRead.

## Template

### currentSourcePath

[ref: #symbol-currentsourcepath]

Returns the full file-system path of the current source.

**Input:**
- *(none)*

**Output:** `string`
Returns the full file-system path of the current source.

To get the directory containing the current source, use it with [ospaths2.parentDir()](ospaths2.html#parentDir%2Cstring) as currentSourcePath.parentDir().

The path returned by this template is set at compile time.

See the docstring of [macros.getProjectPath()](macros.html#getProjectPath) for an example to see the distinction between the currentSourcePath() and getProjectPath().

See also:

* [ospaths2.getCurrentDir() proc](ospaths2.html#getCurrentDir)
