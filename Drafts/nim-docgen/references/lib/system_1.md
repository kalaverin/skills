---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

# system

[ref: #module-system]

The compiler depends on the System module to work properly and the System module depends on the compiler. Most of the routines listed here use special compiler magic.

Each module implicitly imports the System module; it must not be listed explicitly. Because of this there cannot be a user-defined module named system.

# [System module](#system-module)

The System module imports several separate modules, and their documentation is in separate files:

* [iterators](iterators.html)
* [exceptions](exceptions.html)
* [assertions](assertions.html)
* [dollars](dollars.html)
* [ctypes](ctypes.html)
* [repr\_v2](repr_v2.html)

Here is a short overview of the most commonly used functions from the system module. Function names in the tables below are clickable and will take you to the full documentation of the function.

There are many more functions available than the ones listed in this overview. Use the table of contents on the left-hand side and/or Ctrl+F to navigate through this module.

## [Strings and characters](#system-module-strings-and-characters)

| Proc | Usage |
| --- | --- |
| [len(s)](#len,string) | Return the length of a string |
| [chr(i)](#chr,range[]) | Convert an int in the range 0..255 to a character |
| [ord(c)](#ord,T) | Return int value of a character |
| [a & b](#&,string,string) | Concatenate two strings |
| [s.add(c)](#add,string,char) | Add character to the string |
| [$](dollars.html) | Convert various types to string |

**See also:**

* [strutils module](strutils.html) for common string functions
* [strformat module](strformat.html) for string interpolation and formatting
* [unicode module](unicode.html) for Unicode UTF-8 handling
* [strscans](strscans.html) for scanf and scanp macros, which offer easier substring extraction than regular expressions
* [strtabs module](strtabs.html) for efficient hash tables (dictionaries, in some programming languages) mapping from strings to strings

## [Seqs](#system-module-seqs)

| Proc | Usage |
| --- | --- |
| [newSeq](#newSeq) | Create a new sequence of a given length |
| [newSeqOfCap](#newSeqOfCap,Natural) | Create a new sequence with zero length and a given capacity |
| [setLen](#setLen,seq[T],Natural) | Set the length of a sequence |
| [len](#len,seq[T]) | Return the length of a sequence |
| [@](#@,openArray[T]) | Turn an array into a sequence |
| [add](#add,seq[T],sinkT) | Add an item to the sequence |
| [insert](#insert,seq[T],sinkT) | Insert an item at a specific position |
| [delete](#delete,seq[T],Natural) | Delete an item while preserving the order of elements (O(n) operation) |
| [del](#del,seq[T],Natural) | O(1) removal, doesn't preserve the order |
| [pop](#pop,seq[T]) | Remove and return last item of a sequence |
| [x & y](#&,seq[T],seq[T]) | Concatenate two sequences |
| [x[a .. b]](#[],openArray[T],HSlice[U: Ordinal,V: Ordinal]) | Slice of a sequence (both ends included) |
| [x[a .. ^b]](#[],openArray[T],HSlice[U: Ordinal,V: Ordinal]) | Slice of a sequence but b is a reversed index (both ends included) |
| [x[a ..< b]](#[],openArray[T],HSlice[U: Ordinal,V: Ordinal]) | Slice of a sequence (excluded upper bound) |

**See also:**

* [sequtils module](sequtils.html) for operations on container types (including strings)
* [json module](json.html) for a structure which allows heterogeneous members
* [lists module](lists.html) for linked lists

## [Sets](#system-module-sets)

Built-in bit sets.

| Proc | Usage |
| --- | --- |
| [incl](#incl,set[T],T) | Include element y in the set x |
| [excl](#excl,set[T],T) | Exclude element y from the set x |
| [card](#card,set[T]) | Return the cardinality of the set, i.e. the number of elements |
| [a \* b](#*,set[T],set[T]) | Intersection |
| [a + b](#+,set[T],set[T]) | Union |
| [a - b](#-,set[T],set[T]) | Difference |
| [contains](#contains,set[T],T) | Check if an element is in the set |
| [a < b](#<,set[T],set[T]) | Check if a is a subset of b |

**See also:**

* [setutils module](setutils.html) for bit set convenience functions
* [sets module](sets.html) for hash sets
* [intsets module](intsets.html) for efficient int sets

## [Numbers](#system-module-numbers)

| Proc | Usage | Also known as (in other languages) |
| --- | --- | --- |
| [div](#div,int,int) | Integer division | // |
| [mod](#mod,int,int) | Integer modulo (remainder) | % |
| [shl](#shl,int,SomeInteger) | Shift left | << |
| [shr](#shr,int,SomeInteger) | Shift right | >> |
| [ashr](#ashr,int,SomeInteger) | Arithmetic shift right |  |
| [and](#and,int,int) | Bitwise and | & |
| [or](#or,int,int) | Bitwise or | | |
| [xor](#xor,int,int) | Bitwise xor | ^ |
| [not](#not,int) | Bitwise not (complement) | ~ |
| [toInt](#toInt,float) | Convert floating-point number into an int |  |
| [toFloat](#toFloat,int) | Convert an integer into a float |  |

**See also:**

* [math module](math.html) for mathematical operations like trigonometric functions, logarithms, square and cubic roots, etc.
* [complex module](complex.html) for operations on complex numbers
* [rationals module](rationals.html) for rational numbers

## [Ordinals](#system-module-ordinals)

[Ordinal type](#Ordinal) includes integer, bool, character, and enumeration types, as well as their subtypes.

| Proc | Usage |
| --- | --- |
| [succ](#succ) | Successor of the value |
| [pred](#pred) | Predecessor of the value |
| [inc](#inc) | Increment the ordinal |
| [dec](#dec) | Decrement the ordinal |
| [high](#high,T) | Return the highest possible value |
| [low](#low,T) | Return the lowest possible value |
| [ord](#ord,T) | Return int value of an ordinal value |

## [Misc](#system-module-misc)

| Proc | Usage |
| --- | --- |
| [is](#is,T,S) | Check if two arguments are of the same type |
| [isnot](#isnot.t,untyped,untyped) | Negated version of is |
| [!=](#!%3D.t,untyped,untyped) | Not equals |
| [addr](#addr,T) | Take the address of a memory location |
| [T and F](#and,bool,bool) | Boolean and |
| [T or F](#or,bool,bool) | Boolean or |
| [T xor F](#xor,bool,bool) | Boolean xor (exclusive or) |
| [not T](#not,bool) | Boolean not |
| [a[^x]](#^.t,int) | Take the element at the reversed index x |
| [a .. b](#..,sinkT,sinkU) | Binary slice that constructs an interval [a, b] |
| [a ..^ b](#..^.t,untyped,untyped) | Interval [a, b] but b as reversed index |
| [a ..< b](#..<.t,untyped,untyped) | Interval [a, b) (excluded upper bound) |
| [runnableExamples](#runnableExamples,string,untyped) | Create testable documentation |

Default new string implementation used by Nim's core.Default seq implementation used by Nim's core.

Channel support for threads.

**Note**: This is part of the system module. Do not import it directly. To activate thread support compile with the --threads:on command line switch.

**Note:** Channels are designed for the Thread type. They are unstable when used with spawn

**Note:** The current implementation of message passing does not work with cyclic data structures.

**Note:** Channels cannot be passed between threads. Use globals or pass them by ptr.

# [Example](#example)

The following is a simple example of two different ways to use channels: blocking and non-blocking.

```
# Be sure to compile with --threads:on.
# The channels and threads modules are part of system and should not be
# imported.
import std/os

# Channels can either be:
#  - declared at the module level, or
#  - passed to procedures by ptr (raw pointer) -- see note on safety.
#
# For simplicity, in this example a channel is declared at module scope.
# Channels are generic, and they include support for passing objects between
# threads.
# Note that objects passed through channels will be deeply copied.
var chan: Channel[string]

# This proc will be run in another thread using the threads module.
proc firstWorker() =
  chan.send("Hello World!")

# This is another proc to run in a background thread. This proc takes a while
# to send the message since it sleeps for 2 seconds (or 2000 milliseconds).
proc secondWorker() =
  sleep(2000)
  chan.send("Another message")

# Initialize the channel.
chan.open()

# Launch the worker.
var worker1: Thread[void]
createThread(worker1, firstWorker)

# Block until the message arrives, then print it out.
echo chan.recv() # "Hello World!"

# Wait for the thread to exit before moving on to the next example.
worker1.joinThread()

# Launch the other worker.
var worker2: Thread[void]
createThread(worker2, secondWorker)
# This time, use a non-blocking approach with tryRecv.
# Since the main thread is not blocked, it could be used to perform other
# useful work while it waits for data to arrive on the channel.
while true:
  let tried = chan.tryRecv()
  if tried.dataAvailable:
    echo tried.msg # "Another message"
    break
  
  echo "Pretend I'm doing useful work..."
  # For this example, sleep in order not to flood stdout with the above
  # message.
  sleep(400)

# Wait for the second thread to exit before cleaning up the channel.
worker2.joinThread()

# Clean up the channel.
chan.close()
```

## [Sample output](#example-sample-output)

The program should output something similar to this, but keep in mind that exact results may vary in the real world:

```
Hello World!
Pretend I'm doing useful work...
Pretend I'm doing useful work...
Pretend I'm doing useful work...
Pretend I'm doing useful work...
Pretend I'm doing useful work...
Another message
```

## [Passing Channels Safely](#example-passing-channels-safely)

Note that when passing objects to procedures on another thread by pointer (for example through a thread's argument), objects created using the default allocator will use thread-local, GC-managed memory. Thus it is generally safer to store channel objects in global variables (as in the above example), in which case they will use a process-wide (thread-safe) shared heap.

However, it is possible to manually allocate shared memory for channels using e.g. system.allocShared0 and pass these pointers through thread arguments:

```
proc worker(channel: ptr Channel[string]) =
  let greeting = channel[].recv()
  echo greeting

proc localChannelExample() =
  # Use allocShared0 to allocate some shared-heap memory and zero it.
  # The usual warnings about dealing with raw pointers apply. Exercise caution.
  var channel = cast[ptr Channel[string]](
    allocShared0(sizeof(Channel[string]))
  )
  channel[].open()
  # Create a thread which will receive the channel as an argument.
  var thread: Thread[ptr Channel[string]]
  createThread(thread, worker, channel)
  channel[].send("Hello from the main thread!")
  # Clean up resources.
  thread.joinThread()
  channel[].close()
  deallocShared(channel)

localChannelExample() # "Hello from the main thread!"
```

## Examples

```nim
# Be sure to compile with --threads:on.
# The channels and threads modules are part of system and should not be
# imported.
import std/os

# Channels can either be:
#  - declared at the module level, or
#  - passed to procedures by ptr (raw pointer) -- see note on safety.
#
# For simplicity, in this example a channel is declared at module scope.
# Channels are generic, and they include support for passing objects between
# threads.
# Note that objects passed through channels will be deeply copied.
var chan: Channel[string]

# This proc will be run in another thread using the threads module.
proc firstWorker() =
  chan.send("Hello World!")

# This is another proc to run in a background thread. This proc takes a while
# to send the message since it sleeps for 2 seconds (or 2000 milliseconds).
proc secondWorker() =
  sleep(2000)
  chan.send("Another message")

# Initialize the channel.
chan.open()

# Launch the worker.
var worker1: Thread[void]
createThread(worker1, firstWorker)

# Block until the message arrives, then print it out.
echo chan.recv() # "Hello World!"

# Wait for the thread to exit before moving on to the next example.
worker1.joinThread()

# Launch the other worker.
var worker2: Thread[void]
createThread(worker2, secondWorker)
# This time, use a non-blocking approach with tryRecv.
# Since the main thread is not blocked, it could be used to perform other
# useful work while it waits for data to arrive on the channel.
while true:
  let tried = chan.tryRecv()
  if tried.dataAvailable:
    echo tried.msg # "Another message"
    break
  
  echo "Pretend I'm doing useful work..."
  # For this example, sleep in order not to flood stdout with the above
  # message.
  sleep(400)

# Wait for the second thread to exit before cleaning up the channel.
worker2.joinThread()

# Clean up the channel.
chan.close()
```

```nim
proc worker(channel: ptr Channel[string]) =
  let greeting = channel[].recv()
  echo greeting

proc localChannelExample() =
  # Use allocShared0 to allocate some shared-heap memory and zero it.
  # The usual warnings about dealing with raw pointers apply. Exercise caution.
  var channel = cast[ptr Channel[string]](
    allocShared0(sizeof(Channel[string]))
  )
  channel[].open()
  # Create a thread which will receive the channel as an argument.
  var thread: Thread[ptr Channel[string]]
  createThread(thread, worker, channel)
  channel[].send("Hello from the main thread!")
  # Clean up resources.
  thread.joinThread()
  channel[].close()
  deallocShared(channel)

localChannelExample() # "Hello from the main thread!"
```

```nim
var gOutOfMem: ref EOutOfMemory
new(gOutOfMem) # need to be allocated *before* OOM really happened!
gOutOfMem.msg = "out of memory"

proc handleOOM() =
  raise gOutOfMem

system.outOfMemHook = handleOOM
```

```nim
when (NimMajor, NimMinor, NimPatch) >= (1, 3, 1): discard
```

```nim
assert('a' & 'b' == "ab")
```

```nim
assert("ab" & "cd" == "abcd")
```

```nim
assert('a' & "bc" == "abc")
```

```nim
assert("ab" & 'c' == "abc")
```

```nim
assert(@[1, 2, 3, 4] & @[5, 6] == @[1, 2, 3, 4, 5, 6])
```

```nim
assert(@[1, 2, 3] & 4 == @[1, 2, 3, 4])
```

```nim
assert(1 & @[2, 3, 4] == @[1, 2, 3, 4])
```

```nim
var a = "abc"
a &= "de" # a <- "abcde"
```

```nim
assert {1, 2, 3} * {2, 3, 4} == {2, 3}
```

```nim
assert {1, 2, 3} + {2, 3, 4} == {1, 2, 3, 4}
```

```nim
assert {1, 2, 3} - {2, 3, 4} == {1}
```

```nim
let a = [10, 20, 30, 40, 50]
echo a[2 .. 3] # @[30, 40]
```

```nim
let a = [10, 20, 30, 40, 50]
echo a[.. 2] # @[10, 20, 30]
```

```nim
echo 7 / 5 # => 1.4
```

```nim
let
  a = 'a'
  b = 'b'
  c = 'Z'
assert a < b
assert not (a < a)
assert not (a < c)
```

```nim
let
  a = "abc"
  b = "abd"
  c = "ZZZ"
assert a < b
assert not (a < a)
assert not (a < c)
```

```nim
let
  a = {3, 5}
  b = {1, 3, 5, 7}
  c = {2}
assert a < b
assert not (a < a)
assert not (a < c)
```

```nim
let
  a = 'a'
  b = 'b'
  c = 'Z'
assert a <= b
assert a <= a
assert not (a <= c)
```

```nim
let
  a = "abc"
  b = "abd"
  c = "ZZZ"
assert a <= b
assert a <= a
assert not (a <= c)
```

```nim
let
  a = {3, 5}
  b = {1, 3, 5, 7}
  c = {2}
assert a <= b
assert a <= a
assert not (a <= c)
```

```nim
var # this is a wildly dangerous example
  a = cast[pointer](0)
  b = cast[pointer](nil)
assert a == b # true due to the special meaning of `nil`/0 as a pointer
```

```nim
type
  Enum1 = enum
    field1 = 3, field2
  Enum2 = enum
    place1, place2 = 3
var
  e1 = field1
  e2 = place2.ord.Enum1
assert e1 == e2
assert not compiles(e1 == place2) # raises error
```

```nim
assert {1, 2, 2, 3} == {1, 2, 3} # duplication in sets is ignored
```

```nim
let
  a = [1, 3, 5]
  b = "foo"

echo @a # => @[1, 3, 5]
echo @b # => @['f', 'o', 'o']
```

```nim
var a = [1, 2, 3, 4]
assert a[0..2] == @[1, 2, 3]
```

```nim
var s = "abcdef"
assert s[1..3] == "bcd"
```

```nim
var s = @[1, 2, 3, 4]
assert s[0..2] == @[1, 2, 3]
```

```nim
var a = [10, 20, 30, 40, 50]
a[1..2] = @[99, 88]
assert a == [10, 99, 88, 40, 50]
```

```nim
var s = "abcdefgh"
s[1 .. ^2] = "xyz"
assert s == "axyzh"
```

```nim
var s = @"abcdefgh"
s[1 .. ^2] = @"xyz"
assert s == @"axyzh"
```

```nim
when defined(js):
  var tmp: cstring = ""
  tmp.add(cstring("ab"))
  tmp.add(cstring("cd"))
  doAssert tmp == cstring("abcd")
```

```nim
var tmp = ""
tmp.add('a')
tmp.add('b')
assert(tmp == "ab")
```

```nim
var tmp = ""
tmp.add(cstring("ab"))
tmp.add(cstring("cd"))
doAssert tmp == "abcd"
```

```nim
var tmp = ""
tmp.add("ab")
tmp.add("cd")
assert tmp == "abcd"
```

```nim
var a = @["a1", "a2"]
a.add(["b1", "b2"])
assert a == @["a1", "a2", "b1", "b2"]
var c = @["c0", "c1", "c2", "c3"]
a.add(c.toOpenArray(1, 2))
assert a == @["a1", "a2", "b1", "b2", "c1", "c2"]
```

```nim
var tmp = ""
tmp.addQuoted(1)
tmp.add(", ")
tmp.addQuoted("string")
tmp.add(", ")
tmp.addQuoted('c')
assert(tmp == """1, "string", 'c'""")
```

```nim
var
  buf: seq[char] = @['a','b','c']
  p = buf[1].addr
echo p.repr # ref 0x7faa35c40059 --> 'b'
echo p[]    # b
```

```nim
assert (0b0011 and 0b0101) == 0b0001
assert (0b0111 and 0b1100) == 0b0100
```

```nim
assert ashr(0b0001_0000'i8, 2) == 0b0000_0100'i8
assert ashr(0b1000_0000'i8, 8) == 0b1000_0000'i8
assert ashr(0b1000_0000'i8, 1) == 0b1100_0000'i8
```

```nim
var str = newStringOfCap(cap = 42)
str.add "Nim"
assert str.capacity == 42
```

```nim
var lst = newSeqOfCap[string](cap = 42)
lst.add "Nim"
assert lst.capacity == 42
```

```nim
var a = {1, 3, 5, 7}
assert card(a) == 4
var b = {1, 3, 5, 7, 5}
assert card(b) == 4 # repeated 5 doesn't count
```

```nim
doAssert chr(65) == 'A'
doAssert chr(255) == '\255'
doAssert chr(255) == char(255)
doAssert not compiles chr(256)
doAssert not compiles char(256)
var x = 256
doAssertRaises(RangeDefect): discard chr(x)
doAssertRaises(RangeDefect): discard char(x)
```

```nim
assert (1.4).clamp(0.0, 1.0) == 1.0
assert (0.5).clamp(0.0, 1.0) == 0.5
assert 4.clamp(1, 3) == max(1, min(3, 4))
```

```nim
import std/algorithm
echo sorted(@[4, 2, 6, 5, 8, 7], cmp[int])
```

```nim
when compileOption("opt", "size") and compileOption("gc", "boehm"):
  discard "compiled with optimization for size and uses Boehm's GC"
```

```nim
static: doAssert not compileOption("floatchecks")
{.push floatChecks: on.}
static: doAssert compileOption("floatchecks")
# floating point NaN and Inf checks enabled in this scope
{.pop.}
```

```nim
when compiles(3 + 4):
  echo "'+' for integers is available"
```

```nim
var a = @[1, 3, 5]
assert a.contains(5)
assert 3 in a
assert 99 notin a
```

```nim
var s: set[range['a'..'z']] = {'a'..'c'}
assert s.contains('c')
assert 'b' in s
assert 'd' notin s
assert set['a'..'z'] is set[range['a'..'z']]
```

```nim
assert((1..3).contains(1) == true)
assert((1..3).contains(2) == true)
assert((1..3).contains(4) == false)
```

```nim
var i = 2
dec(i)
assert i == 1
dec(i, 3)
assert i == -2
```

```nim
when not declared(strutils.toUpper):
  # provide our own toUpper proc here, because strutils is
  # missing it.
```

```nim
assert (int, float).default == (0, 0.0)
type Foo = object
  a: range[2..6]
var x = Foo.default
assert x.a == 2
```

```nim
when not defined(release):
  # Do here programmer friendly expensive sanity checks.
# Put here the normal code
```

```nim
var a = @[10, 11, 12, 13, 14]
a.del(2)
assert a == @[10, 11, 14, 13]
```

```nim
var s = @[1, 2, 3, 4, 5]
s.delete(2)
doAssert s == @[1, 2, 4, 5]
```

```nim
assert (1 div 2) == 0
assert (2 div 2) == 1
assert (3 div 2) == 1
assert (7 div 3) == 2
assert (-7 div 3) == -2
assert (7 div -3) == -2
assert (-7 div -3) == 2
```

```nim
proc foo =
  var x = "Hello"
  let y = ensureMove(x)
  doAssert y == "Hello"
foo()
```

```nim
var b = {2, 3, 5, 6, 12, 54}
b.excl(5)
assert b == {2, 3, 6, 12, 54}
```

```nim
var str = "Hello world!"
high(str) # => 11
```

```nim
var arr = [1, 2, 3, 4, 5, 6, 7]
high(arr) # => 6
for i in low(arr)..high(arr):
  echo arr[i]
```

```nim
high(array[7, int]) # => 6
```

```nim
high(2) # => 9223372036854775807
```

```nim
high(int) # => 9223372036854775807
```

```nim
var s = @[1, 2, 3, 4, 5, 6, 7]
high(s) # => 6
for i in low(s)..high(s):
  echo s[i]
```

```nim
var i = 2
inc(i)
assert i == 3
inc(i, 3)
assert i == 6
```

```nim
var a = {1, 3, 5}
a.incl(2)
assert a == {1, 2, 3, 5}
a.incl(4)
assert a == {1, 2, 3, 4, 5}
```

```nim
var a = "abc"
a.insert("zz", 0) # a <- "zzabc"
```

```nim
var i = @[1, 3, 5]
i.insert(99, 0) # i <- @[99, 1, 3, 5]
```

```nim
import std/strutils

template testException(exception, code: untyped): typed =
  try:
    let pos = instantiationInfo()
    discard(code)
    echo "Test failure at $1:$2 with '$3'" % [pos.filename,
      $pos.line, astToStr(code)]
    assert false, "A test expecting failure succeeded?"
  except exception:
    discard

proc tester(pos: int): int =
  let
    a = @[1, 2, 3]
  result = a[pos]

when isMainModule:
  testException(IndexDefect, tester(30))
  testException(IndexDefect, tester(1))
  # --> Test failure at example.nim:20 with 'tester(1)'
```

```nim
assert 42 is int
assert @[1, 2] is seq

proc test[T](a: T): int =
  when (T is int):
    return a
  else:
    return 0

assert(test[int](3) == 3)
assert(test[string]("xyz") == 0)
```

```nim
var a = [1, 1, 1]
assert a.len == 3
assert array[0, float].len == 0
static: assert array[-2..2, float].len == 5
```

```nim
doAssert len(cstring"abc") == 3
doAssert len(cstring r"ab\0c") == 5 # \0 is escaped
doAssert len(cstring"ab\0c") == 5 # ditto
var a: cstring = "ab\0c"
when defined(js): doAssert a.len == 4 # len ignores \0 for js
else: doAssert a.len == 2 # \0 is a null terminator
static:
  var a2: cstring = "ab\0c"
  doAssert a2.len == 2 # \0 is a null terminator, even in js vm
```

```nim
assert "abc".len == 3
assert "".len == 0
assert string.default.len == 0
```

```nim
assert @[0, 1].len == 2
assert seq[int].default.len == 0
assert newSeq[int](3).len == 3
let s = newSeqOfCap[int](3)
assert s.len == 0
```

```nim
proc bar[T](a: openArray[T]): int = len(a)
assert bar([1,2]) == 2
assert [1,2].len == 2
```

```nim
assert((0..5).len == 6)
assert((5..2).len == 0)
```

```nim
proc testLocals() =
  var
    a = "something"
    b = 4
    c = locals()
    d = "super!"
  
  b = 1
  for name, value in fieldPairs(c):
    echo "name ", name, " with value ", value
  echo "B is ", b
# -> name a with value something
# -> name b with value 4
# -> B is 1
```

```nim
var str = "Hello world!"
low(str) # => 0
```

```nim
var arr = [1, 2, 3, 4, 5, 6, 7]
low(arr) # => 0
for i in low(arr)..high(arr):
  echo arr[i]
```

```nim
low(array[7, int]) # => 0
```

```nim
low(2) # => -9223372036854775808
```

```nim
low(int) # => -9223372036854775808
```

```nim
var s = @[1, 2, 3, 4, 5, 6, 7]
low(s) # => 0
for i in low(s)..high(s):
  echo s[i]
```

```nim
assert (7 mod 5) == 2
assert (-7 mod 5) == -2
assert (7 mod -5) == 2
assert (-7 mod -5) == -2
```

```nim
var inputStrings = newSeq[string](3)
assert len(inputStrings) == 3
inputStrings[0] = "The fourth"
inputStrings[1] = "assignment"
inputStrings[2] = "would crash"
#inputStrings[3] = "out of bounds"
```

```nim
var inputStrings: seq[string]
newSeq(inputStrings, 3)
assert len(inputStrings) == 3
inputStrings[0] = "The fourth"
inputStrings[1] = "assignment"
inputStrings[2] = "would crash"
#inputStrings[3] = "out of bounds"
```

```nim
var x = newSeqOfCap[int](5)
assert len(x) == 0
x.add(10)
assert len(x) == 1
```

```nim
var x = newSeqUninit[int](3)
assert len(x) == 3
x[0] = 10
```

```nim
var x = newSeqUninitialized[int](3)
assert len(x) == 3
x[0] = 10
```

```nim
assert not 0'u8 == 255
assert not 0'i8 == -1
assert not 1000'u16 == 64535
assert not 1000'i16 == -1001
```

```nim
type
  Base = ref object of RootObj
  Sub1 = ref object of Base
  Sub2 = ref object of Base
  Unrelated = ref object

var base: Base = Sub1() # downcast
doAssert base of Base # generates `CondTrue` (statically true)
doAssert base of Sub1
doAssert base isnot Sub1
doAssert not (base of Sub2)

base = Sub2() # re-assign
doAssert base of Sub2
doAssert Sub2(base) != nil # upcast
doAssertRaises(ObjectConversionDefect): discard Sub1(base)

var sub1 = Sub1()
doAssert sub1 of Base
doAssert sub1.Base of Sub1

doAssert not compiles(base of Unrelated)
```

```nim
assert (0b0011 or 0b0101) == 0b0111
assert (0b0111 or 0b1100) == 0b1111
```

```nim
assert ord('A') == 65
type Foo = enum
  f0 = 0, f1 = 3
assert f1.ord == 3
type Bar = distinct int
assert 3.Bar.ord == 3
```

```nim
var a = @[1, 3, 5, 7]
let b = pop(a)
assert b == 7
assert a == @[1, 3, 5]
```

```nim
assert pred(5) == 4
assert pred(5, 3) == 2
```

```nim
# 'someMethod' will be resolved fully statically:
procCall someMethod(a, b)
```

```nim
proc makeClosure(x: int): (proc(y: int): int) =
  var n = x
  result = (
    proc(y: int): int =
      n += y
      return n
  )

var
  c1 = makeClosure(10)
  e = c1.rawEnv()
  p = c1.rawProc()

if e.isNil():
  let c2 = cast[proc(y: int): int {.nimcall.}](p)
  echo c2(2)
else:
  let c3 = cast[proc(y: int; env: pointer): int {.nimcall.}](p)
  echo c3(3, e)
```

```nim
$(1 .. 5) == "1 .. 5"
```

```nim
proc timesTwo*(x: int): int =
  ## This proc doubles a number.
  runnableExamples:
    # at module scope
    const exported* = 123
    assert timesTwo(5) == 10
    block: # at block scope
      defer: echo "done"
  runnableExamples "-d:foo -b:cpp":
    import std/compilesettings
    assert querySetting(backend) == "cpp"
    assert defined(foo)
  runnableExamples "-r:off": ## this one is only compiled
     import std/browsers
     openDefaultBrowser "https://forum.nim-lang.org/"
  2 * x
```

```nim
  var stop: Atomic[bool]
  proc ctrlc() {.noconv.} =
    # Using atomics types is safe!
    stop.store(true)
  
  setControlCHook(ctrlc)
  
  while not stop.load():
    echo "Still running.."
    sleep(1000)
```

```nim
var myS = "Nim is great!!"
myS.setLen(3) # myS <- "Nim"
echo myS, " is fantastic!!"
```

```nim
var x = @[10, 20]
x.setLen(5)
x[4] = 50
assert x == @[10, 20, 0, 0, 50]
x.setLen(1)
assert x == @[10]
```

```nim
var x = @[10, 20]
x.setLenUninit(5)
x[4] = 50
assert x[4] == 50Add commentMore actions
x.setLenUninit(1)
assert x == @[10]
```

```nim
assert 1'i32 shl 4 == 0x0000_0010
assert 1'i64 shl 4 == 0x0000_0000_0000_0010
```

```nim
assert 0b0001_0000'i8 shr 2 == 0b0000_0100'i8
assert 0b0000_0001'i8 shr 1 == 0b0000_0000'i8
assert 0b1000_0000'i8 shr 4 == 0b1111_1000'i8
assert -1 shr 5 == -1
assert 1 shr 5 == 0
assert 16 shr 2 == 4
assert -16 shr 2 == -4
```

```nim
sizeof('A') # => 1
sizeof(2) # => 8
```

```nim
const buildInfo = "Revision " & staticExec("git rev-parse HEAD") &
                  "\nCompiled on " & staticExec("uname -v")
```

```nim
const stateMachine = staticExec("dfaoptimizer", "input", "0.8.0")
```

```nim
const myResource = staticRead"mydatafile.bin"
```

```nim
let a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
assert a.substr() == "abcdefgh"
assert a.toOpenArray(2, 5).substr() == "cdef"
assert a.toOpenArray(2, high(a)).substr() == "cdefgh"  # From index 2 to `high(a)`
doAssertRaises(IndexDefect): discard a.toOpenArray(5, 99).substr()
```

```nim
let a = "abcdefgh"
assert a.substr(2) == "cdefgh"    # From index 2 to string end (`high(a)`)
assert a.substr(100) == ""        # `first` out of bounds
assert a.substr(-1) == "abcdefgh" # Negative `first` clamped to 0
```

```nim
let a = "abcdefgh"
assert a.substr(2, 5) == "cdef" # Normal substring
# Invalid indexes
assert a.substr(5, 99) == "fgh" # From index 5 to `high(a)`
assert a.substr(42, 99) == ""   # `first` out of bounds
assert a.substr(100, 5) == ""   # `first > last`
assert a.substr(-1, 2) == "abc" # Negative `first` clamped to 0
```

```nim
assert succ(5) == 6
assert succ(5, 3) == 8
```

```nim
var
  a = 5
  b = 9

swap(a, b)

assert a == 9
assert b == 5
```

```nim
let
  a = 2
  b = 3.7

echo a.toFloat + b # => 5.7
```

```nim
doAssert toInt(0.49) == 0
doAssert toInt(0.5) == 1
doAssert toInt(-0.5) == -1 # rounding is symmetrical
```

```nim
proc test(x: openArray[int]) =
  doAssert x == [1, 2, 3]

let s = @[0, 1, 2, 3, 4]
s.toOpenArray(1, 3).test
```

```nim
proc myFoo(): float = 0.0
iterator myFoo(): string = yield "abc"
iterator myFoo2(): string = yield "abc"
iterator myFoo3(): string {.closure.} = yield "abc"
doAssert type(myFoo()) is string
doAssert typeof(myFoo()) is string
doAssert typeof(myFoo(), typeOfIter) is string
doAssert typeof(myFoo3) is iterator

doAssert typeof(myFoo(), typeOfProc) is float
doAssert typeof(0.0, typeOfProc) is float
doAssert typeof(myFoo3, typeOfProc) is iterator
doAssert not compiles(typeof(myFoo2(), typeOfProc))
  # this would give: Error: attempting to call routine: 'myFoo2'
  # since `typeOfProc` expects a typed expression and `myFoo2()` can
  # only be used in a `for` context.

proc varParam(x: var int;
              y: typeof(x, modifierMode = RemoveTypeModifiers);
              z: typeof(x, modifierMode = KeepTypeModifiers)) = discard
doAssert varParam is proc (x: var int; y: int; z: var int) {.nimcall.}
```

```nim
assert (0b0011 xor 0b0101) == 0b0110
assert (0b0111 xor 0b1100) == 0b1011
```

```nim
import std/sugar

let x = collect(newSeq):
  for i in 3 .. 7:
    i

assert x == @[3, 4, 5, 6, 7]
```

```nim
import std/sugar
let x = collect(newSeq):
  for i in countdown(7, 3):
    i

assert x == @[7, 6, 5, 4, 3]

let y = collect(newseq):
  for i in countdown(9, 2, 3):
    i
assert y == @[9, 6, 3]
```

```nim
import std/sugar
let x = collect(newSeq):
  for i in countup(3, 7):
    i

assert x == @[3, 4, 5, 6, 7]

let y = collect(newseq):
  for i in countup(2, 9, 3):
    i
assert y == @[2, 5, 8]
```

```nim
for i in 5 ..< 9:
  echo i # => 5; 6; 7; 8
```

```nim
let
  a = [1, 3, 5, 7, 9]
  b = "abcdefgh"

echo a[^1] # => 9
echo b[^2] # => g
```

```nim
var myClosure : proc()
# without closureScope:
for i in 0 .. 5:
  let j = i
  if j == 3:
    myClosure = proc() = echo j
myClosure() # outputs 5. `j` is changed after closure creation
# with closureScope:
for i in 0 .. 5:
  closureScope: # Everything in this scope is locked after closure creation
    let j = i
    if j == 3:
      myClosure = proc() = echo j
myClosure() # outputs 3
```

```nim
var a = {1, 3, 5, 7}
var b = {3, 4, 5}
a.excl(b) 
assert a == {1, 7}
```

```nim
assert(1 in (1..3) == true)
assert(5 in (1..3) == false)
```

```nim
var a = {1, 3, 5, 7}
var b = {4, 5, 6}
a.incl(b)
assert a == {1, 3, 4, 5, 6, 7}
```

```nim
assert 42 isnot float
assert @[1, 2] isnot enum
```

```nim
for value in inputValues:
  if likely(value <= 100):
    process(value)
  else:
    echo "Value too big!"
```

```nim
assert(1 notin (1..3) == false)
assert(5 notin (1..3) == true)
```

```nim
proc draw(t: Triangle) =
  once:
    graphicsInit()
  line(t.p1, t.p2)
  line(t.p2, t.p3)
  line(t.p3, t.p1)
```

```nim
for value in inputValues:
  if unlikely(value > 100):
    echo "Value too big!"
  else:
    process(value)
```


[Next](system_2.md)
