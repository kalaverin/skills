---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### newSeq

[ref: #symbol-newseq]

Creates a new sequence of type seq[T] with length len.

**Input:**
- `len:  = 0.Natural`

**Output:** `seq[T]`
**Generic parameters:** `T`

Creates a new sequence of type seq[T] with length len.

Note that the sequence will be filled with zeroed entries. After the creation of the sequence you should assign entries to the sequence instead of adding them.

```
var inputStrings = newSeq[string](3)
assert len(inputStrings) == 3
inputStrings[0] = "The fourth"
inputStrings[1] = "assignment"
inputStrings[2] = "would crash"
#inputStrings[3] = "out of bounds"
```

See also:

* [newSeqOfCap](#newSeqOfCap,Natural)
* [newSeqUninit](#newSeqUninit,Natural)

### newSeqOfCap

[ref: #symbol-newseqofcap]

Creates a new sequence of type seq[T] with length zero and capacity cap. Example:

**Input:**
- `cap: Natural`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "NewSeqOfCap"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new sequence of type seq[T] with length zero and capacity cap. Example:

```
var x = newSeqOfCap[int](5)
assert len(x) == 0
x.add(10)
assert len(x) == 1
```

### newSeqUninit

[ref: #symbol-newsequninit]

Creates a new sequence of type seq[T] with length len.

**Input:**
- `len: Natural`

**Output:** `seq[T]`
**Generic parameters:** `T`

Creates a new sequence of type seq[T] with length len.

Only available for types, which don't contain managed memory or have destructors. Note that the sequence will be uninitialized. After the creation of the sequence you should assign entries to the sequence instead of adding them.

### newSeqUninitialized

[ref: #symbol-newsequninitialized]

Creates a new sequence of type seq[T] with length len.

**Input:**
- `len: Natural`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `deprecated: "Use `newSeqUninit` instead"`

Creates a new sequence of type seq[T] with length len.

Only available for numbers types. Note that the sequence will be uninitialized. After the creation of the sequence you should assign entries to the sequence instead of adding them. Example:

```
var x = newSeqUninitialized[int](3)
assert len(x) == 3
x[0] = 10
```

### newString

[ref: #symbol-newstring]

Returns a new string of length len. One needs to fill the string character after character with the index operator s[i].

**Input:**
- `len: Natural`

**Output:** `string`
**Pragmas:** `magic: "NewString"`, `importc: "mnewString"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string of length len. One needs to fill the string character after character with the index operator s[i].

This procedure exists only for optimization purposes; the same effect can be achieved with the & operator or with add.

### newStringOfCap

[ref: #symbol-newstringofcap]

Returns a new string of length 0 but with capacity cap.

**Input:**
- `cap: Natural`

**Output:** `string`
**Pragmas:** `magic: "NewStringOfCap"`, `importc: "rawNewString"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string of length 0 but with capacity cap.

This procedure exists only for optimization purposes; the same effect can be achieved with the & operator or with add.

### newStringUninit

[ref: #symbol-newstringuninit]

Returns a new string of length len but with uninitialized content. One needs to fill the string character after character with the index operator s[i].

**Input:**
- `len: Natural`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string of length len but with uninitialized content. One needs to fill the string character after character with the index operator s[i].

This procedure exists only for optimization purposes; the same effect can be achieved with the & operator or with add.

### nimCStrLen

[ref: #symbol-nimcstrlen]

**Input:**
- `a: cstring`

**Output:** `int`
**Pragmas:** `compilerproc`, `nonReloadable`, `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### onThreadDestruction

[ref: #symbol-onthreaddestruction]

Registers a *thread local* handler that is called at the thread's destruction.

**Input:**
- `handler: proc () {.closure, gcsafe, raises: [].}`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Registers a *thread local* handler that is called at the thread's destruction.

A thread is destructed when the .thread proc returns normally or when it raises an exception. Note that unhandled exceptions in a thread nevertheless cause the whole process to die.

### open

[ref: #symbol-open]

Opens a channel c for inter thread communication.

**Input:**
- `c: var Channel[TMsg]`
- `maxItems: int = 0`

**Output:** *(none)*
**Generic parameters:** `TMsg`

**Pragmas:** `raises: []`, `gcsafe`

**Effects:** `raises: `

Opens a channel c for inter thread communication.

The send operation will block until number of unprocessed items is less than maxItems.

For unlimited queue set maxItems to 0.

### ord

[ref: #symbol-ord]

**Input:**
- `x: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "Ord"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the internal int value of x, including for enum with holes and distinct ordinal types.

### peek

[ref: #symbol-peek]

Returns the current number of messages in the channel c.

**Input:**
- `c: var Channel[TMsg]`

**Output:** `int`
**Generic parameters:** `TMsg`

**Pragmas:** `raises: []`, `gcsafe`

**Effects:** `raises: `

Returns the current number of messages in the channel c.

Returns -1 if the channel has been closed.

**Note**: This is dangerous to use as it encourages races. It's much better to use [tryRecv proc](#tryRecv,Channel[TMsg]) instead.

### pop

[ref: #symbol-pop]

Returns the last item of s and decreases s.len by one. This treats s as a stack and implements the common *pop* operation.

**Input:**
- `s: var seq[T]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `noSideEffect`

Returns the last item of s and decreases s.len by one. This treats s as a stack and implements the common *pop* operation.

Raises IndexDefect if s is empty.

### pred

[ref: #symbol-pred]

Returns the y-th predecessor (default: 1) of the value x.

**Input:**
- `x: T`
- `y: V = 1`

**Output:** `T`
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Pred"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the y-th predecessor (default: 1) of the value x.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs.

### prepareMutation

[ref: #symbol-preparemutation]

**Input:**
- `s: var string`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### procCall

[ref: #symbol-proccall]

Special magic to prohibit dynamic binding for method calls. This is similar to super in ordinary OO languages.

**Input:**
- `x: untyped`

**Output:** *(none)*
**Pragmas:** `magic: "ProcCall"`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special magic to prohibit dynamic binding for method calls. This is similar to super in ordinary OO languages.

```
# 'someMethod' will be resolved fully statically:
procCall someMethod(a, b)
```

### protect

[ref: #symbol-protect]

**Input:**
- `x: pointer`

**Output:** `ForeignCell`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### quit

[ref: #symbol-quit]

Stops the program immediately with an exit code.

**Input:**
- `errorcode: int = QuitSuccess`

**Output:** *(none)*
**Pragmas:** `magic: "Exit"`, `noreturn`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Stops the program immediately with an exit code.

Before stopping the program the "exit procedures" are called in the opposite order they were added with [addExitProc](exitprocs.html#addExitProc,proc)).

The proc quit(QuitSuccess) is called implicitly when your nim program finishes without incident for platforms where this is the expected behavior. A raised unhandled exception is equivalent to calling quit(QuitFailure).

Note that this is a *runtime* call and using quit inside a macro won't have any compile time effect. If you need to stop the compiler inside a macro, use the [error](manual.html#pragmas-error-pragma) or [fatal](manual.html#pragmas-fatal-pragma) pragmas.

**Warning:**
errorcode gets saturated when it exceeds the valid range on the specific platform. On Posix, the valid range is low(int8)..high(int8). On Windows, the valid range is low(int32)..high(int32). For instance, quit(int(0x100000000)) is equal to quit(127) on Linux.

**Danger:**
In almost all cases, in particular in library code, prefer alternatives, e.g. raiseAssert or raise a Defect. quit bypasses regular control flow in particular defer, try, catch, finally and destructors, and exceptions that may have been raised by an addExitProc proc, as well as cleanup code in other threads. It does *not* call the garbage collector to free all the memory, unless an addExitProc proc calls [GC\_fullCollect](#GC_fullCollect).

### quit

[ref: #symbol-quit]

**Input:**
- `errormsg: string`
- `errorcode:  = QuitFailure`

**Output:** *(none)*
**Pragmas:** `noreturn`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A shorthand for echo(errormsg); quit(errorcode).

### rawEnv

[ref: #symbol-rawenv]

**Input:**
- `x: T`

**Output:** `pointer`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `inline`

Retrieves the raw environment pointer of the closure x. See also rawProc. This is not available for the JS target.

### rawProc

[ref: #symbol-rawproc]

**Input:**
- `x: T`

**Output:** `pointer`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `inline`

Retrieves the raw proc pointer of the closure x. This is useful for interfacing closures with C/C++, hash computations, etc. If rawEnv(x) returns nil, the proc which the result points to takes as many parameters as x, but with {.nimcall.} as its calling convention instead of {.closure.}, otherwise it takes one more parameter which is a pointer, and it still has {.nimcall.} as its calling convention. To invoke the resulted proc, what this returns has to be casted into a proc, not a ptr proc, and, in a case where rawEnv(x) returns non-nil, the last and additional argument has to be the result of rawEnv(x). This is not available for the JS target.

### ready

[ref: #symbol-ready]

**Input:**
- `c: var Channel[TMsg]`

**Output:** `bool`
**Generic parameters:** `TMsg`

**Pragmas:** `raises: []`, `gcsafe`

**Effects:** `raises: `

Returns true if some thread is waiting on the channel c for new messages.

### realloc0Impl

[ref: #symbol-realloc0impl]

**Input:**
- `p: pointer`
- `oldSize: Natural`
- `newSize: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### reallocImpl

[ref: #symbol-reallocimpl]

**Input:**
- `p: pointer`
- `newSize: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### reallocShared0Impl

[ref: #symbol-reallocshared0impl]

**Input:**
- `p: pointer`
- `oldSize: Natural`
- `newSize: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### reallocSharedImpl

[ref: #symbol-reallocsharedimpl]

**Input:**
- `p: pointer`
- `newSize: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### recv

[ref: #symbol-recv]

Receives a message from the channel c.

**Input:**
- `c: var Channel[TMsg]`

**Output:** `TMsg`
**Generic parameters:** `TMsg`

**Pragmas:** `raises: []`, `gcsafe`

**Effects:** `raises: `

Receives a message from the channel c.

This blocks until a message has arrived! You may use [peek proc](#peek,Channel[TMsg]) to avoid the blocking.

### repr

[ref: #symbol-repr]

Generic repr operator for slices that is lifted from the components of x. Example:

**Input:**
- `x: HSlice[T, U]`

**Output:** `string`
**Generic parameters:** `T`, `U`

Generic repr operator for slices that is lifted from the components of x. Example:

```
$(1 .. 5) == "1 .. 5"
```

### reset

[ref: #symbol-reset]

**Input:**
- `obj: var T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Resets an object obj to its default value.

### resize

[ref: #symbol-resize]

Grows or shrinks a given memory block.

**Input:**
- `p: ptr T`
- `newSize: Natural`

**Output:** `ptr T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `gcsafe`, `raises: []`

**Effects:** `raises: `

Grows or shrinks a given memory block.

If p is **nil** then a new memory block is returned. In either way the block has at least T.sizeof \* newSize bytes. If newSize == 0 and p is not **nil** resize calls dealloc(p). In other cases the block has to be freed with free.

The allocated memory belongs to its allocating thread! Use [resizeShared](#resizeShared,ptr.T,Natural) to reallocate from a shared heap.

### resizeShared

[ref: #symbol-resizeshared]

Grows or shrinks a given memory block on the heap.

**Input:**
- `p: ptr T`
- `newSize: Natural`

**Output:** `ptr T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `raises: []`

**Effects:** `raises: `

Grows or shrinks a given memory block on the heap.

If p is **nil** then a new memory block is returned. In either way the block has at least T.sizeof \* newSize bytes. If newSize == 0 and p is not **nil** resizeShared calls freeShared(p). In other cases the block has to be freed with [freeShared](#freeShared,ptr.T).

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

### send

[ref: #symbol-send]

**Input:**
- `c: var Channel[TMsg]`
- `msg: sink TMsg`

**Output:** *(none)*
**Generic parameters:** `TMsg`

**Pragmas:** `inline`, `raises: []`, `gcsafe`

**Effects:** `raises: `

Sends a message to a thread.

### setControlCHook

[ref: #symbol-setcontrolchook]

Allows you to override the behaviour of your application when CTRL+C is pressed. Only one such hook is supported.

**Input:**
- `hook: proc () {.noconv.}`

**Output:** *(none)*
**Pragmas:** `raises: []`, `gcsafe`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Allows you to override the behaviour of your application when CTRL+C is pressed. Only one such hook is supported.

The handler runs inside a C signal handler and comes with similar limitations.

Allocating memory and interacting with most system calls, including using echo, string, seq, raising or catching exceptions etc is undefined behavior and will likely lead to application crashes.

The OS may call the ctrl-c handler from any thread, including threads that were not created by Nim, such as happens on Windows.

## [Example:](#system-module-examplecolon)

```
  var stop: Atomic[bool]
  proc ctrlc() {.noconv.} =
    # Using atomics types is safe!
    stop.store(true)
  
  setControlCHook(ctrlc)
  
  while not stop.load():
    echo "Still running.."
    sleep(1000)
```

### setCurrentException

[ref: #symbol-setcurrentexception]

Sets the current exception.

**Input:**
- `exc: ref Exception`

**Output:** *(none)*
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the current exception.

**Warning:**
Only use this if you know what you are doing.

### setFrame

[ref: #symbol-setframe]

**Input:**
- `s: PFrame`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setFrameState

[ref: #symbol-setframestate]

**Input:**
- `state: FrameState`

**Output:** *(none)*
**Pragmas:** `compilerproc`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setLen

[ref: #symbol-setlen]

Sets the length of seq s to newlen. T may be any sequence type.

**Input:**
- `s: var seq[T]`
- `newlen: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "SetLengthSeq"`, `noSideEffect`, `nodestroy`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the length of seq s to newlen. T may be any sequence type.

If the current length is greater than the new length, s will be truncated.

```
var x = @[10, 20]
x.setLen(5)
x[4] = 50
assert x == @[10, 20, 0, 0, 50]
x.setLen(1)
assert x == @[10]
```

### setLen

[ref: #symbol-setlen]

Sets the length of string s to newlen.

**Input:**
- `s: var string`
- `newlen: Natural`

**Output:** *(none)*
**Pragmas:** `magic: "SetLengthStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the length of string s to newlen.

If the current length is greater than the new length, s will be truncated.

```
var myS = "Nim is great!!"
myS.setLen(3) # myS <- "Nim"
echo myS, " is fantastic!!"
```

### setLenUninit

[ref: #symbol-setlenuninit]

Sets the length of seq s to newlen. T may be any sequence type. New slots will not be initialized.

**Input:**
- `s: var seq[T]`
- `newlen: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "SetLengthSeqUninit"`, `nodestroy`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the length of seq s to newlen. T may be any sequence type. New slots will not be initialized.

If the current length is greater than the new length, s will be truncated.

```
var x = @[10, 20]
x.setLenUninit(5)
x[4] = 50
assert x[4] == 50Add commentMore actions
x.setLenUninit(1)
assert x == @[10]
```

### setLenUninit

[ref: #symbol-setlenuninit]

Sets the length of string s to newlen. New slots will not be initialized.

**Input:**
- `s: var string`
- `newlen: Natural`

**Output:** *(none)*
**Pragmas:** `nodestroy`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the length of string s to newlen. New slots will not be initialized.

If the new length is smaller than the new length, s will be truncated.

### shrink

[ref: #symbol-shrink]

**Input:**
- `x: var seq[T]`
- `newLen: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `tags: []`, `raises: []`

**Effects:** `tags: `, `raises: `

### sizeof

[ref: #symbol-sizeof]

Returns the size of x in bytes.

**Input:**
- `x: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "SizeOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the size of x in bytes.

Since this is a low-level proc, its usage is discouraged - using [new](#new,ref.T,proc(ref.T)) for the most cases suffices that one never needs to know x's size.

As a special semantic rule, x may also be a type identifier (sizeof(int) is valid).

Limitations: If used for types that are imported from C or C++, sizeof should fallback to the sizeof in the C compiler. The result isn't available for the Nim compiler and therefore can't be used inside of macros.

```
sizeof('A') # => 1
sizeof(2) # => 8
```

### sizeof

[ref: #symbol-sizeof]

**Input:**
- `x: typedesc`

**Output:** `int`
**Generic parameters:** `x:type`

**Pragmas:** `magic: "SizeOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### slurp

[ref: #symbol-slurp]

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `magic: "Slurp"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is an alias for [staticRead](#staticRead,string).

### stackTraceAvailable

[ref: #symbol-stacktraceavailable]

**Input:**
- *(none)*

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

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

### substr

[ref: #symbol-substr]

Returns a new string, copying contents of a.

**Input:**
- `a: openArray[char]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string, copying contents of a.

**Warning:**
As opposed to other substr overloads, no additional input validation and clamping is performed!

This proc does not prevent raising an IndexDefect when a is being passed using a toOpenArray call with out-of-bounds indexes:

* doAssertRaises(IndexDefect): discard "abc".toOpenArray(-9, 9).substr()

If clamping is required, consider using [substr(s: string; first, last: int)](#substr,string,int,int):

* doAssert "abc".substr(-9, 9) == "abc"

### substr

[ref: #symbol-substr]

Returns a new string containing a substring (slice) of s, copying characters from index first to index last inclusive.

**Input:**
- `s: string`
- `first: int`
- `last: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string containing a substring (slice) of s, copying characters from index first to index last inclusive.

Index values are validated and capped:

* Negative first is clamped to 0
* If last >= s.len, it is clamped to high(s)
* If last < first, returns an empty string

This means substr can also be used to cut or limit a string's length.

**Note:**
If index values are ensured to be in-bounds, for performance critical cases consider using a non-clamping overload [substr(a: openArray[char])](#substr,openArray[char])


[Prev](system_9.md) | [Next](system_11.md)
