---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### globalRaiseHook

[ref: #symbol-globalraisehook]

With this hook you can influence exception handling on a global level. If not nil, every 'raise' statement ends up calling this hook.

```nim
globalRaiseHook: proc (e: ref Exception): bool {.nimcall, gcsafe.}
```

With this hook you can influence exception handling on a global level. If not nil, every 'raise' statement ends up calling this hook.

**Warning:**
Ordinary application code should never set this hook! You better know what you do when setting this.

If globalRaiseHook returns false, the exception is caught and does not propagate further through the call stack.

### localRaiseHook

[ref: #symbol-localraisehook]

With this hook you can influence exception handling on a thread local level. If not nil, every 'raise' statement ends up calling this hook.

```nim
localRaiseHook {.threadvar.}: proc (e: ref Exception): bool {.nimcall, gcsafe.}
```

With this hook you can influence exception handling on a thread local level. If not nil, every 'raise' statement ends up calling this hook.

**Warning:**
Ordinary application code should never set this hook! You better know what you do when setting this.

If localRaiseHook returns false, the exception is caught and does not propagate further through the call stack.

### nimThreadDestructionHandlers

[ref: #symbol-nimthreaddestructionhandlers]

```nim
nimThreadDestructionHandlers {.threadvar.}: seq[
    proc () {.closure, gcsafe, raises: [].}]
```

### onUnhandledException

[ref: #symbol-onunhandledexception]

Set this error

```nim
onUnhandledException: (proc (errorMsg: string) {.nimcall, gcsafe.})
```

Set this error
handler to override the existing behaviour on an unhandled exception.

The default is to write a stacktrace to stderr and then call quit(1). Unstable API.

### outOfMemHook

[ref: #symbol-outofmemhook]

Set this variable to provide a procedure that should be called in case of an out of memory event. The standard handler writes an error message and terminates the program.

```nim
outOfMemHook: proc () {.nimcall, tags: [], gcsafe, raises: [].}
```

Set this variable to provide a procedure that should be called in case of an out of memory event. The standard handler writes an error message and terminates the program.

outOfMemHook can be used to raise an exception in case of OOM like so:

```
var gOutOfMem: ref EOutOfMemory
new(gOutOfMem) # need to be allocated *before* OOM really happened!
gOutOfMem.msg = "out of memory"

proc handleOOM() =
  raise gOutOfMem

system.outOfMemHook = handleOOM
```

If the handler does not raise an exception, ordinary control flow continues and the program is terminated.

### programResult

[ref: #symbol-programresult]

```nim
programResult {.compilerproc, exportc: "nim_program_result".}: int
```

deprecated, prefer quit or exitprocs.getProgramResult, exitprocs.setProgramResult.

### unhandledExceptionHook

[ref: #symbol-unhandledexceptionhook]

```nim
unhandledExceptionHook: proc (e: ref Exception) {.nimcall, tags: [], gcsafe,
    raises: [].}
```

Set this variable to provide a procedure that should be called in case of an unhandle exception event. The standard handler writes an error message and terminates the program, except when using --os:any

[Prev](system_12.md)
