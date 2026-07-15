---
source_hash: 2228c5889cba3df5
source_path: lib/pure/osproc.nim
---

# osproc

[ref: #module-osproc]

This module implements an advanced facility for executing OS processes and process communication.

**See also:**

* [os module](os.html)
* [streams module](streams.html)
* [memfiles module](memfiles.html)

## Examples

```nim
let errC = execCmd("nim c -r mytestfile.nim")
```

```nim
var result = execCmdEx("nim r --hints:off -", options = {}, input = "echo 3*4")
import std/[strutils, strtabs]
stripLineEnd(result[0]) ## portable way to remove trailing newline, if any
doAssert result == ("12", 0)
doAssert execCmdEx("ls --nonexistent").exitCode != 0
when defined(posix):
  assert execCmdEx("echo $FO", env = newStringTable({"FO": "B"})) == ("B\n", 0)
  assert execCmdEx("echo $PWD", workingDir = "/") == ("/\n", 0)
```

```nim
let outp = execProcess("nim", args=["c", "-r", "mytestfile.nim"], options={poUsePath})
let outp_shell = execProcess("nim c -r mytestfile.nim")
# Note: outp may have an interleave of text from the nim compile
# and any output from mytestfile when it runs
```

```nim
const opts = {poUsePath, poDaemon, poStdErrToStdOut}
var ps: seq[Process]
for prog in ["a", "b"]: # run 2 progs in parallel
  ps.add startProcess("nim", "", ["r", prog], nil, opts)
for p in ps:
  let (lines, exCode) = p.readLines
  if exCode != 0:
    for line in lines: echo line
  p.close
```

```nim
const opts = {poUsePath, poDaemon, poStdErrToStdOut}
var ps: seq[Process]
for prog in ["a", "b"]: # run 2 progs in parallel
  ps.add startProcess("nim", "", ["r", prog], nil, opts)
for p in ps:
  var i = 0
  for line in p.lines:
    echo line
    i.inc
    if i > 100: break
  p.close
```

## Iterator

### lines

[ref: #symbol-lines]

Convenience iterator for working with startProcess to read data from a background process.

**Input:**
- `p: Process`
- `keepNewLines:  = false`

**Output:** `string`
**Pragmas:** `raises: [OSError, IOError, ValueError]`, `tags: [ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError, ValueError`, `tags: ReadIOEffect, TimeEffect`, `forbids: `

Convenience iterator for working with startProcess to read data from a background process.

See also:

* [readLines proc](#readLines,Process)

Example:

```
const opts = {poUsePath, poDaemon, poStdErrToStdOut}
var ps: seq[Process]
for prog in ["a", "b"]: # run 2 progs in parallel
  ps.add startProcess("nim", "", ["r", prog], nil, opts)
for p in ps:
  var i = 0
  for line in p.lines:
    echo line
    i.inc
    if i > 100: break
  p.close
```

## Proc

### close

[ref: #symbol-close]

When the process has finished executing, cleanup related handles.

**Input:**
- `p: Process`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

When the process has finished executing, cleanup related handles.

**Warning:**
If the process has not finished executing, this will forcibly terminate the process. Doing so may result in zombie processes and [pty leaks](https://stackoverflow.com/questions/27021641/how-to-fix-request-failed-on-channel-0).

### countProcessors

[ref: #symbol-countprocessors]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of the processors/cores the machine has. Returns 0 if it cannot be detected. It is implemented just calling cpuinfo.countProcessors.

### errorHandle

[ref: #symbol-errorhandle]

Returns p's error file handle for reading from.

**Input:**
- `p: Process`

**Output:** `FileHandle`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns p's error file handle for reading from.

**Warning:**
The returned FileHandle should not be closed manually as it is closed when closing the Process p.

See also:

* [inputHandle proc](#inputHandle,Process)
* [outputHandle proc](#outputHandle,Process)

### errorStream

[ref: #symbol-errorstream]

Returns p's error stream for reading from.

**Input:**
- `p: Process`

**Output:** `Stream`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Returns p's error stream for reading from.

You cannot perform peek/write/setOption operations to this stream. Use [peekableErrorStream proc](#peekableErrorStream,Process) if you need to peek stream.

**Warning:**
The returned Stream should not be closed manually as it is closed when closing the Process p.

See also:

* [inputStream proc](#inputStream,Process)
* [outputStream proc](#outputStream,Process)

### execCmd

[ref: #symbol-execcmd]

Executes command and returns its error code.

**Input:**
- `command: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: [ExecIOEffect, ReadIOEffect, RootEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ExecIOEffect, ReadIOEffect, RootEffect`, `raises: `, `forbids: `

Executes command and returns its error code.

Standard input, output, error streams are inherited from the calling process. This operation is also often called system.

See also:

* [execCmdEx proc](#execCmdEx,string,set[ProcessOption],StringTableRef,string,string)
* [startProcess proc](#startProcess,string,string,openArray[string],StringTableRef,set[ProcessOption])
* [execProcess proc](#execProcess,string,string,openArray[string],StringTableRef,set[ProcessOption])

Example:

```
let errC = execCmd("nim c -r mytestfile.nim")
```

### execCmdEx

[ref: #symbol-execcmdex]

A convenience proc that runs the command, and returns its output and exitCode. env and workingDir params behave as for startProcess. If input.len > 0, it is passed as stdin.

**Input:**
- `command: string`
- `options: set[ProcessOption] = {poStdErrToStdOut, poUsePath}`
- `env: StringTableRef = nil`
- `workingDir:  = ""`
- `input:  = ""`

**Output:** `tuple[output: string, exitCode: int]`
**Pragmas:** `raises: [OSError, IOError]`, `tags: [ExecIOEffect, ReadIOEffect, RootEffect]`, `gcsafe`, `forbids: []`

**Effects:** `raises: OSError, IOError`, `tags: ExecIOEffect, ReadIOEffect, RootEffect`, `forbids: `

A convenience proc that runs the command, and returns its output and exitCode. env and workingDir params behave as for startProcess. If input.len > 0, it is passed as stdin.

Note: this could block if input.len is greater than your OS's maximum pipe buffer size.

See also:

* [execCmd proc](#execCmd,string)
* [startProcess proc](#startProcess,string,string,openArray[string],StringTableRef,set[ProcessOption])
* [execProcess proc](#execProcess,string,string,openArray[string],StringTableRef,set[ProcessOption])

Example:

```
var result = execCmdEx("nim r --hints:off -", options = {}, input = "echo 3*4")
import std/[strutils, strtabs]
stripLineEnd(result[0]) ## portable way to remove trailing newline, if any
doAssert result == ("12", 0)
doAssert execCmdEx("ls --nonexistent").exitCode != 0
when defined(posix):
  assert execCmdEx("echo $FO", env = newStringTable({"FO": "B"})) == ("B\n", 0)
  assert execCmdEx("echo $PWD", workingDir = "/") == ("/\n", 0)
```

### execProcess

[ref: #symbol-execprocess]

A convenience procedure that executes command with startProcess and returns its output as a string.

**Input:**
- `command: string`
- `workingDir: string = ""`
- `args: openArray[string] = []`
- `env: StringTableRef = nil`
- `options: set[ProcessOption] = {poStdErrToStdOut, poUsePath, poEvalCommand}`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [OSError, IOError]`, `tags: [ExecIOEffect, ReadIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError`, `tags: ExecIOEffect, ReadIOEffect, RootEffect`, `forbids: `

A convenience procedure that executes command with startProcess and returns its output as a string.

**Warning:**
This function uses poEvalCommand by default for backwards compatibility. Make sure to pass options explicitly.

See also:

* [startProcess proc](#startProcess,string,string,openArray[string],StringTableRef,set[ProcessOption])
* [execProcesses proc](#execProcesses,openArray[string],proc(int),proc(int,Process))
* [execCmd proc](#execCmd,string)

Example:

```
let outp = execProcess("nim", args=["c", "-r", "mytestfile.nim"], options={poUsePath})
let outp_shell = execProcess("nim c -r mytestfile.nim")
# Note: outp may have an interleave of text from the nim compile
# and any output from mytestfile when it runs
```

### execProcesses

[ref: #symbol-execprocesses]

Executes the commands cmds in parallel. Creates n processes that execute in parallel.

**Input:**
- `cmds: openArray[string]`
- `options:  = {poStdErrToStdOut, poParentStreams}`
- `n:  = countProcessors()`
- `beforeRunEvent: proc (idx: int) = nil`
- `afterRunEvent: proc (idx: int; p: Process) = nil`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [ValueError, OSError, IOError]`, `tags: [ExecIOEffect, TimeEffect, ReadEnvEffect, RootEffect]`, `effectsOf: [beforeRunEvent, afterRunEvent]`, `forbids: []`

**Effects:** `raises: ValueError, OSError, IOError`, `tags: ExecIOEffect, TimeEffect, ReadEnvEffect, RootEffect`, `forbids: `

Executes the commands cmds in parallel. Creates n processes that execute in parallel.

The highest (absolute) return value of all processes is returned. Runs beforeRunEvent before running each command.

### hasData

[ref: #symbol-hasdata]

**Input:**
- `p: Process`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inputHandle

[ref: #symbol-inputhandle]

Returns p's input file handle for writing to.

**Input:**
- `p: Process`

**Output:** `FileHandle`
**Pragmas:** `gcsafe`, `raises: []`, `extern: "nosp$1"`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns p's input file handle for writing to.

**Warning:**
The returned FileHandle should not be closed manually as it is closed when closing the Process p.

See also:

* [outputHandle proc](#outputHandle,Process)
* [errorHandle proc](#errorHandle,Process)

### inputStream

[ref: #symbol-inputstream]

Returns p's input stream for writing to.

**Input:**
- `p: Process`

**Output:** `Stream`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Returns p's input stream for writing to.

**Warning:**
The returned Stream should not be closed manually as it is closed when closing the Process p.

See also:

* [outputStream proc](#outputStream,Process)
* [errorStream proc](#errorStream,Process)

### kill

[ref: #symbol-kill]

Kill the process p.

**Input:**
- `p: Process`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Kill the process p.

On Posix OSes the procedure sends SIGKILL to the process. On Windows kill is simply an alias for [terminate()](#terminate,Process).

See also:

* [suspend proc](#suspend,Process)
* [resume proc](#resume,Process)
* [terminate proc](#terminate,Process)
* [posix\_utils.sendSignal(pid: Pid, signal: int)](posix_utils.html#sendSignal,Pid,int)

### outputHandle

[ref: #symbol-outputhandle]

Returns p's output file handle for reading from.

**Input:**
- `p: Process`

**Output:** `FileHandle`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns p's output file handle for reading from.

**Warning:**
The returned FileHandle should not be closed manually as it is closed when closing the Process p.

See also:

* [inputHandle proc](#inputHandle,Process)
* [errorHandle proc](#errorHandle,Process)

### outputStream

[ref: #symbol-outputstream]

Returns p's output stream for reading from.

**Input:**
- `p: Process`

**Output:** `Stream`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

Returns p's output stream for reading from.

You cannot perform peek/write/setOption operations to this stream. Use [peekableOutputStream proc](#peekableOutputStream,Process) if you need to peek stream.

**Warning:**
The returned Stream should not be closed manually as it is closed when closing the Process p.

See also:

* [inputStream proc](#inputStream,Process)
* [errorStream proc](#errorStream,Process)

### peekableErrorStream

[ref: #symbol-peekableerrorstream]

Returns p's error stream for reading from.

**Input:**
- `p: Process`

**Output:** `Stream`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Returns p's error stream for reading from.

You can run peek operation to returned stream.

**Warning:**
The returned Stream should not be closed manually as it is closed when closing the Process p.

See also:

* [errorStream proc](#errorStream,Process)
* [peekableOutputStream proc](#peekableOutputStream,Process)

### peekableOutputStream

[ref: #symbol-peekableoutputstream]

Returns p's output stream for reading from.

**Input:**
- `p: Process`

**Output:** `Stream`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Returns p's output stream for reading from.

You can peek returned stream.

**Warning:**
The returned Stream should not be closed manually as it is closed when closing the Process p.

See also:

* [outputStream proc](#outputStream,Process)
* [peekableErrorStream proc](#peekableErrorStream,Process)

### peekExitCode

[ref: #symbol-peekexitcode]

Return -1 if the process is still running. Otherwise the process' exit code.

**Input:**
- `p: Process`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Return -1 if the process is still running. Otherwise the process' exit code.

On posix, if the process has exited because of a signal, 128 + signal number will be returned.

### processID

[ref: #symbol-processid]

Returns p's process ID.

**Input:**
- `p: Process`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns p's process ID.

See also:

* [os.getCurrentProcessId proc](os.html#getCurrentProcessId)

### readLines

[ref: #symbol-readlines]

Convenience function for working with startProcess to read data from a background process.

**Input:**
- `p: Process`

**Output:** `(seq[string], int)`
**Pragmas:** `raises: [OSError, IOError, ValueError]`, `tags: [ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError, ValueError`, `tags: ReadIOEffect, TimeEffect`, `forbids: `

Convenience function for working with startProcess to read data from a background process.

See also:

* [lines iterator](#lines.i,Process)

Example:

```
const opts = {poUsePath, poDaemon, poStdErrToStdOut}
var ps: seq[Process]
for prog in ["a", "b"]: # run 2 progs in parallel
  ps.add startProcess("nim", "", ["r", prog], nil, opts)
for p in ps:
  let (lines, exCode) = p.readLines
  if exCode != 0:
    for line in lines: echo line
  p.close
```

### resume

[ref: #symbol-resume]

Resumes the process p.

**Input:**
- `p: Process`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Resumes the process p.

See also:

* [suspend proc](#suspend,Process)
* [terminate proc](#terminate,Process)
* [kill proc](#kill,Process)

### running

[ref: #symbol-running]

**Input:**
- `p: Process`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns true if the process p is still running. Returns immediately.

### startProcess

[ref: #symbol-startprocess]

Starts a process. Command is the executable file, workingDir is the process's working directory. If workingDir == "" the current directory is used (default). args are the command line arguments that are passed to the process. On many operating systems, the first command line argument is the name of the executable. args should *not* contain this argument! env is the environment that will be passed to the process. If env == nil (default) the environment is inherited of the parent process. options are additional flags that may be passed to startProcess. See the documentation of [ProcessOption](#ProcessOption) for the meaning of these flags.

**Input:**
- `command: string`
- `workingDir: string = ""`
- `args: openArray[string] = []`
- `env: StringTableRef = nil`
- `options: set[ProcessOption] = {poStdErrToStdOut}`

**Output:** `owned(Process)`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [OSError, IOError]`, `tags: [ExecIOEffect, ReadEnvEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError`, `tags: ExecIOEffect, ReadEnvEffect, RootEffect`, `forbids: `

Starts a process. Command is the executable file, workingDir is the process's working directory. If workingDir == "" the current directory is used (default). args are the command line arguments that are passed to the process. On many operating systems, the first command line argument is the name of the executable. args should *not* contain this argument! env is the environment that will be passed to the process. If env == nil (default) the environment is inherited of the parent process. options are additional flags that may be passed to startProcess. See the documentation of [ProcessOption](#ProcessOption) for the meaning of these flags.

You need to [close](#close,Process) the process when done.

Note that you can't pass any args if you use the option poEvalCommand, which invokes the system shell to run the specified command. In this situation you have to concatenate manually the contents of args to command carefully escaping/quoting any special characters, since it will be passed *as is* to the system shell. Each system/shell may feature different escaping rules, so try to avoid this kind of shell invocation if possible as it leads to non portable software.

Return value: The newly created process object. Nil is never returned, but OSError is raised in case of an error.

See also:

* [execProcesses proc](#execProcesses,openArray[string],proc(int),proc(int,Process))
* [execProcess proc](#execProcess,string,string,openArray[string],StringTableRef,set[ProcessOption])
* [execCmd proc](#execCmd,string)

### suspend

[ref: #symbol-suspend]

Suspends the process p.

**Input:**
- `p: Process`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Suspends the process p.

See also:

* [resume proc](#resume,Process)
* [terminate proc](#terminate,Process)
* [kill proc](#kill,Process)

### terminate

[ref: #symbol-terminate]

Stop the process p.

**Input:**
- `p: Process`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Stop the process p.

On Posix OSes the procedure sends SIGTERM to the process. On Windows the Win32 API function TerminateProcess() is called to stop the process.

See also:

* [suspend proc](#suspend,Process)
* [resume proc](#resume,Process)
* [kill proc](#kill,Process)
* [posix\_utils.sendSignal(pid: Pid, signal: int)](posix_utils.html#sendSignal,Pid,int)

### waitForExit

[ref: #symbol-waitforexit]

Waits for the process to finish and returns p's error code.

**Input:**
- `p: Process`
- `timeout: int = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nosp$1"`, `raises: [OSError, ValueError]`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: OSError, ValueError`, `tags: TimeEffect`, `forbids: `

Waits for the process to finish and returns p's error code.

**Warning:**
Be careful when using waitForExit for processes created without poParentStreams because they may fill output buffers, causing deadlock.

On posix, if the process has exited because of a signal, 128 + signal number will be returned.

**Warning:**
When working with timeout parameters, remember that the value is typically expressed in milliseconds, and ensure that the correct unit of time is used to avoid unexpected behavior.

## Type

### Process

[ref: #symbol-process]

```nim
Process = ref ProcessObj
```

Represents an operating system process.

### ProcessOption

[ref: #symbol-processoption]

```nim
ProcessOption = enum
  poEchoCmd,                ## Echo the command before execution.
  poUsePath, ## Asks system to search for executable using PATH environment
              ## variable.
              ## On Windows, this is the default.
  poEvalCommand, ## Pass `command` directly to the shell, without quoting.
                  ## Use it only if `command` comes from trusted source.
  poStdErrToStdOut,         ## Merge stdout and stderr to the stdout stream.
  poParentStreams,          ## Use the parent's streams.
  poInteractive, ## Optimize the buffer handling for responsiveness for
                  ## UI applications. Currently this only affects
                  ## Windows: Named pipes are used so that you can peek
                  ## at the process' output streams.
  poDaemon                   ## Windows: The program creates no Window.
                             ## Unix: Start the program as a daemon. This is still
                             ## work in progress!
```

Options that can be passed to [startProcess proc](#startProcess,string,string,openArray[string],StringTableRef,set[ProcessOption]).
