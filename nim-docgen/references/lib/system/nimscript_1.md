---
source_hash: f89aa0a386027073
source_path: lib/system/nimscript.nim
---

# nimscript

[ref: #module-nimscript]

To learn about scripting in Nim see [NimScript](nims.html)

## Examples

```nim
patchFile("stdlib", "asyncdispatch", "patches/replacement")
```

```nim
--path:somePath # same as switch("path", "somePath")
--path:"someOtherPath" # same as switch("path", "someOtherPath")
--hint:"[Conf]:off" # same as switch("hint", "[Conf]:off")
```

```nim
--listCmd # same as switch("listCmd")
```

```nim
task build, "default build is via the C backend":
  setCommand "c"
```

```nim
task foo, "foo":        # > nim foo
  echo "Running foo"    # Running foo

task bar, "bar":        # > nim bar
  echo "Running bar"    # Running bar
  fooTask()             # Running foo
```

```nim
# inside /some/path/
withDir "foo":
  # move to /some/path/foo/
# back in /some/path/
```

## Const

### buildCPU

[ref: #symbol-buildcpu]

```nim
buildCPU {.magic: "BuildCPU".}: string = ""
```

The CPU this build is running on. Can be different from system.hostCPU for cross compilations.

### buildOS

[ref: #symbol-buildos]

```nim
buildOS {.magic: "BuildOS".}: string = ""
```

The OS this build is running on. Can be different from system.hostOS for cross compilations.

## Proc

### cd

[ref: #symbol-cd]

Changes the current directory.

**Input:**
- `dir: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Changes the current directory.

The change is permanent for the rest of the execution, since this is just a shortcut for [os.setCurrentDir()](os.html#setCurrentDir,string) . Use the [withDir()](#withDir.t,string,untyped) template if you want to perform a temporary change only.

### cmpic

[ref: #symbol-cmpic]

**Input:**
- `a: string`
- `b: string`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares a and b ignoring case.

### cpDir

[ref: #symbol-cpdir]

**Input:**
- `from: string`
- `to: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Copies the dir from to to.

### cpFile

[ref: #symbol-cpfile]

**Input:**
- `from: string`
- `to: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Copies the file from to to.

### cppDefine

[ref: #symbol-cppdefine]

**Input:**
- `define: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

tell Nim that define is a C preprocessor #define and so always needs to be mangled.

### delEnv

[ref: #symbol-delenv]

**Input:**
- `key: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

Deletes the environment variable named key.

### dirExists

[ref: #symbol-direxists]

**Input:**
- `dir: string`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Checks if the directory dir exists.

### exec

[ref: #symbol-exec]

Executes an external process. If the external process terminates with a non-zero exit code, an OSError exception is raised. The command is executed relative to the current source path.

**Input:**
- `command: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ExecIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ExecIOEffect, WriteIOEffect`, `forbids: `

Executes an external process. If the external process terminates with a non-zero exit code, an OSError exception is raised. The command is executed relative to the current source path.

**Note:**
If you need a version of exec that returns the exit code and text output of the command, you can use [system.gorgeEx](system.html#gorgeEx,string,string,string).

### exec

[ref: #symbol-exec]

Executes an external process. If the external process terminates with a non-zero exit code, an OSError exception is raised.

**Input:**
- `command: string`
- `input: string`
- `cache:  = ""`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ExecIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ExecIOEffect, WriteIOEffect`, `forbids: `

Executes an external process. If the external process terminates with a non-zero exit code, an OSError exception is raised.

**Warning:**
This version of exec is executed relative to the nimscript module path, which affects how the command resolves relative paths. Thus it is generally better to use gorgeEx directly when you need more control over the execution environment or when working with commands that deal with relative paths.

### exists

[ref: #symbol-exists]

**Input:**
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for the existence of a configuration 'key' like 'gcc.options.always'.

### existsEnv

[ref: #symbol-existsenv]

**Input:**
- `key: string`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Checks for the existence of an environment variable named key.

### fileExists

[ref: #symbol-fileexists]

**Input:**
- `filename: string`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Checks if the file exists.

### findExe

[ref: #symbol-findexe]

**Input:**
- `bin: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for bin in the current working directory and then in directories listed in the PATH environment variable. Returns "" if the exe cannot be found.

### get

[ref: #symbol-get]

**Input:**
- `key: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves a configuration 'key' like 'gcc.options.always'.

### getCommand

[ref: #symbol-getcommand]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the Nim command that the compiler has been invoked with, for example "c", "js", "build", "help".

### getCurrentDir

[ref: #symbol-getcurrentdir]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the current working directory.

### getEnv

[ref: #symbol-getenv]

**Input:**
- `key: string`
- `default:  = ""`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Retrieves the environment variable of name key.

### hint

[ref: #symbol-hint]

**Input:**
- `name: string`
- `val: bool`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Disables or enables a specific hint.

### listDirs

[ref: #symbol-listdirs]

**Input:**
- `dir: string`

**Output:** `seq[string]`
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect`, `forbids: `

Lists all the subdirectories (non-recursively) in the directory dir.

### listFiles

[ref: #symbol-listfiles]

**Input:**
- `dir: string`

**Output:** `seq[string]`
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect`, `forbids: `

Lists all the files (non-recursively) in the directory dir.

### mkDir

[ref: #symbol-mkdir]

**Input:**
- `dir: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: WriteIOEffect`, `forbids: `

Creates the directory dir including all necessary subdirectories. If the directory already exists, no error is raised.

### mvDir

[ref: #symbol-mvdir]

**Input:**
- `from: string`
- `to: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Moves the dir from to to.

### mvFile

[ref: #symbol-mvfile]

**Input:**
- `from: string`
- `to: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Moves the file from to to.

### nimcacheDir

[ref: #symbol-nimcachedir]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the location of 'nimcache'.

### paramCount

[ref: #symbol-paramcount]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the number of command line parameters.

### paramStr

[ref: #symbol-paramstr]

**Input:**
- `i: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the i'th command line parameter.

### patchFile

[ref: #symbol-patchfile]

Overrides the location of a given file belonging to the passed package. If the replacement is not an absolute path, the path is interpreted to be local to the Nimscript file that contains the call to patchFile, Nim's --path is not used at all to resolve the filename! The compiler also performs [path substitution](nimc.html#compiler-usage-commandminusline-switches) on replacement.

**Input:**
- `package: string`
- `filename: string`
- `replacement: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Overrides the location of a given file belonging to the passed package. If the replacement is not an absolute path, the path is interpreted to be local to the Nimscript file that contains the call to patchFile, Nim's --path is not used at all to resolve the filename! The compiler also performs [path substitution](nimc.html#compiler-usage-commandminusline-switches) on replacement.

Example:

```
patchFile("stdlib", "asyncdispatch", "patches/replacement")
```

### projectDir

[ref: #symbol-projectdir]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the absolute directory of the current project

### projectName

[ref: #symbol-projectname]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the name of the current project

### projectPath

[ref: #symbol-projectpath]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the absolute path of the current project

### put

[ref: #symbol-put]

**Input:**
- `key: string`
- `value: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets a configuration 'key' like 'gcc.options.always' to its value.

### putEnv

[ref: #symbol-putenv]

**Input:**
- `key: string`
- `val: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

Sets the value of the environment variable named key to val.

### readAllFromStdin

[ref: #symbol-readallfromstdin]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: [IOError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect`, `forbids: `

Reads all data from stdin - blocks until EOF which happens when stdin is closed

### readLineFromStdin

[ref: #symbol-readlinefromstdin]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: [IOError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect`, `forbids: `

Reads a line of data from stdin - blocks until n or EOF which happens when stdin is closed

### requires

[ref: #symbol-requires]

**Input:**
- `deps: varargs[string]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Nimble support: Call this to set the list of requirements of your Nimble package.

### rmDir

[ref: #symbol-rmdir]

**Input:**
- `dir: string`
- `checkDir:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Removes the directory dir.

### rmFile

[ref: #symbol-rmfile]

**Input:**
- `file: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Removes the file.

### selfExe

[ref: #symbol-selfexe]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `deprecated: "Deprecated since v1.7; Use getCurrentCompilerExe"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the currently running nim or nimble executable.

### selfExec

[ref: #symbol-selfexec]

**Input:**
- `command: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [ExecIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ExecIOEffect, WriteIOEffect`, `forbids: `

Executes an external command with the current nim/nimble executable. Command must not contain the "nim " part.

### setCommand

[ref: #symbol-setcommand]

**Input:**
- `cmd: string`
- `project:  = ""`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the Nim command that should be continued with after this Nimscript has finished.

### switch

[ref: #symbol-switch]

**Input:**
- `key: string`
- `val:  = ""`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets a Nim compiler command line switch, for example switch("checks", "on").

### thisDir

[ref: #symbol-thisdir]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the directory of the current nims script file. Its path is obtained via currentSourcePath (although, currently, currentSourcePath resolves symlinks, unlike thisDir).

### toDll

[ref: #symbol-todll]

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

On Windows adds ".dll" to filename, on Posix produces "lib$filename.so".

### toExe

[ref: #symbol-toexe]

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

On Windows adds ".exe" to filename, else returns filename unmodified.

### warning

[ref: #symbol-warning]

**Input:**
- `name: string`
- `val: bool`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Disables or enables a specific warning.

## Template

### `--`

[ref: #symbol-]

A shortcut for [switch](#switch,string,string) Example:

**Input:**
- `key: untyped`
- `val: untyped`

**Output:** *(none)*
A shortcut for [switch](#switch,string,string) Example:

```
--path:somePath # same as switch("path", "somePath")
--path:"someOtherPath" # same as switch("path", "someOtherPath")
--hint:"[Conf]:off" # same as switch("hint", "[Conf]:off")
```

### `--`

[ref: #symbol-]

A shortcut for [switch](#switch,string,string) Example:

**Input:**
- `key: untyped`

**Output:** *(none)*
A shortcut for [switch](#switch,string,string) Example:

```
--listCmd # same as switch("listCmd")
```

### task

[ref: #symbol-task]

Defines a task. Hidden tasks are supported via an empty description.

**Input:**
- `name: untyped`
- `description: string`
- `body: untyped`

**Output:** `untyped`
Defines a task. Hidden tasks are supported via an empty description.

Example:

```
task build, "default build is via the C backend":
  setCommand "c"
```

For a task named foo, this template generates a proc named fooTask. This is useful if you need to call one task in another in your Nimscript.

Example:

```
task foo, "foo":        # > nim foo
  echo "Running foo"    # Running foo

task bar, "bar":        # > nim bar
  echo "Running bar"    # Running bar
  fooTask()             # Running foo
```

### withDir

[ref: #symbol-withdir]

Changes the current directory temporarily.

**Input:**
- `dir: string`
- `body: untyped`

**Output:** `untyped`
Changes the current directory temporarily.

If you need a permanent change, use the [cd()](#cd,string) proc. Usage example:

```
# inside /some/path/
withDir "foo":
  # move to /some/path/foo/
# back in /some/path/
```

## Type

### ScriptMode

[ref: #symbol-scriptmode]

```nim
ScriptMode {.pure.} = enum
  Silent,                   ## Be silent.
  Verbose,                  ## Be verbose.
  Whatif                     ## Do not run commands, instead just echo what
                             ## would have been done.
```

Controls the behaviour of the script.

## Var

### author

[ref: #symbol-author]

```nim
author: string
```

Nimble support: The package's author.

### backend

[ref: #symbol-backend]

```nim
backend: string
```

Nimble support: The package's backend.

### bin

[ref: #symbol-bin]

```nim
bin: seq[string] = @[]
```

### binDir

[ref: #symbol-bindir]

```nim
binDir: string
```

Nimble support: The package's binary directory.

### description

[ref: #symbol-description]

```nim
description: string
```

Nimble support: The package's description.

### installDirs

[ref: #symbol-installdirs]

```nim
installDirs: seq[string] = @[]
```

### installExt

[ref: #symbol-installext]

```nim
installExt: seq[string] = @[]
```

### installFiles

[ref: #symbol-installfiles]

```nim
installFiles: seq[string] = @[]
```

### license

[ref: #symbol-license]

```nim
license: string
```

Nimble support: The package's license.

### mode

[ref: #symbol-mode]

```nim
mode: ScriptMode
```

Set this to influence how mkDir, rmDir, rmFile etc. behave

### packageName

[ref: #symbol-packagename]

```nim
packageName = ""
```

Nimble support: Set this to the package name. It is usually not required to do that, nims' filename is the default.

### requiresData

[ref: #symbol-requiresdata]

```nim
requiresData: seq[string] = @[]
```

Exposes the list of requirements for read and write accesses.

### skipDirs

[ref: #symbol-skipdirs]

```nim
skipDirs: seq[string] = @[]
```

### skipExt

[ref: #symbol-skipext]

```nim
skipExt: seq[string] = @[]
```

### skipFiles

[ref: #symbol-skipfiles]

```nim
skipFiles: seq[string] = @[]
```

### srcDir

[ref: #symbol-srcdir]

```nim
srcDir: string
```

Nimble support: The package's source directory.


[Next](nimscript_2.md)
