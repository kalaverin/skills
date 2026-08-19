---
source_hash: db9f268cef143e33
source_path: lib/pure/unittest.nim
---

# unittest

[ref: #module-unittest]

|  |  |
| --- | --- |
| Author: | Zahary Karadjov |

This module implements boilerplate to make unit testing easy.

The test status and name is printed after any output or traceback.

Tests can be nested, however failure of a nested test will not mark the parent test as failed. Setup and teardown are inherited. Setup can be overridden locally.

Compiled test files as well as nim c -r <testfile.nim> exit with 0 for success (no failed tests) or 1 for failure.

# [Testament](#testament)

Instead of unittest, please consider using [the Testament tool](testament.html) which offers process isolation for your tests.

Alternatively using when isMainModule: doAssert conditionHere is usually a much simpler solution for testing purposes.

# [Running a single test](#running-a-single-test)

Specify the test name as a command line argument.

```
nim c -r test "my test name" "another test"
```

Multiple arguments can be used.

# [Running a single test suite](#running-a-single-test-suite)

Specify the suite name delimited by "::".

```
nim c -r test "my test name::"
```

# [Selecting tests by pattern](#selecting-tests-by-pattern)

A single "\*" can be used for globbing.

Delimit the end of a suite name with "::".

Tests matching **any** of the arguments are executed.

```
nim c -r test fast_suite::mytest1 fast_suite::mytest2
nim c -r test "fast_suite::mytest*"
nim c -r test "auth*::" "crypto::hashing*"
# Run suites starting with 'bug #' and standalone tests starting with '#'
nim c -r test 'bug #*::' '::#*'
```

# [Examples](#examples)

```
suite "description for this stuff":
  echo "suite setup: run once before the tests"
  
  setup:
    echo "run before each test"
  
  teardown:
    echo "run after each test"
  
  test "essential truths":
    # give up and stop if this fails
    require(true)
  
  test "slightly less obvious stuff":
    # print a nasty message and move on, skipping
    # the remainder of this block
    check(1 != 1)
    check("asd"[2] == 'd')
  
  test "out of bounds error is thrown on bad access":
    let v = @[1, 2, 3]  # you can do initialization here
    expect(IndexDefect):
      discard v[4]
  
  echo "suite teardown: run once after the tests"
```

# [Limitations/Bugs](#limitationsslashbugs)

Since check will rewrite some expressions for supporting checkpoints (namely assigns expressions to variables), some type conversions are not supported. For example check 4.0 == 2 + 2 won't work. But doAssert 4.0 == 2 + 2 works. Make sure both sides of the operator (such as ==, >= and so on) have the same type.

## Examples

```nim
nim c -r test "my test name" "another test"
```

```nim
nim c -r test "my test name::"
```

```nim
nim c -r test fast_suite::mytest1 fast_suite::mytest2
nim c -r test "fast_suite::mytest*"
nim c -r test "auth*::" "crypto::hashing*"
# Run suites starting with 'bug #' and standalone tests starting with '#'
nim c -r test 'bug #*::' '::#*'
```

```nim
suite "description for this stuff":
  echo "suite setup: run once before the tests"
  
  setup:
    echo "run before each test"
  
  teardown:
    echo "run after each test"
  
  test "essential truths":
    # give up and stop if this fails
    require(true)
  
  test "slightly less obvious stuff":
    # print a nasty message and move on, skipping
    # the remainder of this block
    check(1 != 1)
    check("asd"[2] == 'd')
  
  test "out of bounds error is thrown on bad access":
    let v = @[1, 2, 3]  # you can do initialization here
    expect(IndexDefect):
      discard v[4]
  
  echo "suite teardown: run once after the tests"
```

```nim
checkpoint("Checkpoint A")
check((42, "the Answer to life and everything") == (1, "a"))
checkpoint("Checkpoint B")
```

```nim
import std/strutils

check("AKB48".toLowerAscii() == "akb48")

let teams = {'A', 'K', 'B', '4', '8'}

check:
  "AKB48".toLowerAscii() == "akb48"
  'C' notin teams
```

```nim
import std/[math, random, strutils]
proc defectiveRobot() =
  randomize()
  case rand(1..4)
  of 1: raise newException(OSError, "CANNOT COMPUTE!")
  of 2: discard parseInt("Hello World!")
  of 3: raise newException(IOError, "I can't do that Dave.")
  else: assert 2 + 2 == 5

expect IOError, OSError, ValueError, AssertionDefect:
  defectiveRobot()
```

```nim
checkpoint("Checkpoint A")
complicatedProcInThread()
fail()
```

```nim
if not isGLContextCreated():
  skip()
```

```nim
suite "test suite for addition":
  setup:
    let result = 4
  
  test "2 + 2 = 4":
    check(2+2 == result)
  
  test "(2 + -2) != 4":
    check(2 + -2 != result)
  
  # No teardown needed
```

```nim
test "roses are red":
  let roses = "red"
  check(roses == "red")
```

## Macro

### check

[ref: #symbol-check]

**Input:**
- `conditions: untyped`

**Output:** `untyped`
Verify if a statement or a list of statements is true. A helpful error message and set checkpoints are printed out on failure (if outputLevel is not PRINT\_NONE).

### expect

[ref: #symbol-expect]

**Input:**
- `exceptions: varargs[typed]`
- `body: untyped`

**Output:** `untyped`
Test if body raises an exception found in the passed exceptions. The test passes if the raised exception is part of the acceptable exceptions. Otherwise, it fails.

## Proc

### addOutputFormatter

[ref: #symbol-addoutputformatter]

**Input:**
- `formatter: OutputFormatter`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### checkpoint

[ref: #symbol-checkpoint]

Set a checkpoint identified by msg. Upon test failure all checkpoints encountered so far are printed out. Example:

**Input:**
- `msg: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set a checkpoint identified by msg. Upon test failure all checkpoints encountered so far are printed out. Example:

```
checkpoint("Checkpoint A")
check((42, "the Answer to life and everything") == (1, "a"))
checkpoint("Checkpoint B")
```

outputs "Checkpoint A" once it fails.

### close

[ref: #symbol-close]

**Input:**
- `formatter: JUnitOutputFormatter`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Completes the report and closes the underlying stream.

### defaultConsoleFormatter

[ref: #symbol-defaultconsoleformatter]

**Input:**
- *(none)*

**Output:** `ConsoleOutputFormatter`
**Pragmas:** `raises: [ValueError]`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: ReadEnvEffect`, `forbids: `

### delOutputFormatter

[ref: #symbol-deloutputformatter]

**Input:**
- `formatter: OutputFormatter`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### disableParamFiltering

[ref: #symbol-disableparamfiltering]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

disables filtering tests with the command line params

### newConsoleOutputFormatter

[ref: #symbol-newconsoleoutputformatter]

**Input:**
- `outputLevel: OutputLevel = outputLevelDefault`
- `colorOutput:  = true`

**Output:** `ConsoleOutputFormatter`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newJUnitOutputFormatter

[ref: #symbol-newjunitoutputformatter]

**Input:**
- `stream: Stream`

**Output:** `JUnitOutputFormatter`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Creates a formatter that writes report to the specified stream in JUnit format. The stream is NOT closed automatically when the test are finished, because the formatter has no way to know when all tests are finished. You should invoke formatter.close() to finalize the report.

### resetOutputFormatters

[ref: #symbol-resetoutputformatters]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### fail

[ref: #symbol-fail]

Print out the checkpoints encountered so far and quit if abortOnError is true. Otherwise, erase the checkpoints and indicate the test has failed (change exit code and test status). This template is useful for debugging, but is otherwise mostly used internally. Example:

**Input:**
- *(none)*

**Output:** *(none)*
Print out the checkpoints encountered so far and quit if abortOnError is true. Otherwise, erase the checkpoints and indicate the test has failed (change exit code and test status). This template is useful for debugging, but is otherwise mostly used internally. Example:

```
checkpoint("Checkpoint A")
complicatedProcInThread()
fail()
```

outputs "Checkpoint A" before quitting.

### require

[ref: #symbol-require]

**Input:**
- `conditions: untyped`

**Output:** *(none)*
Same as check except any failed test causes the program to quit immediately. Any teardown statements are not executed and the failed test output is not generated.

### skip

[ref: #symbol-skip]

Mark the test as skipped. Should be used directly in case when it is not possible to perform test for reasons depending on outer environment, or certain application logic conditions or configurations. The test code is still executed.

**Input:**
- *(none)*

**Output:** *(none)*
Mark the test as skipped. Should be used directly in case when it is not possible to perform test for reasons depending on outer environment, or certain application logic conditions or configurations. The test code is still executed.

```
if not isGLContextCreated():
  skip()
```

### suite

[ref: #symbol-suite]

Declare a test suite identified by name with optional setup and/or teardown section.

**Input:**
- `name: `
- `body: `

**Output:** *(none)*
**Pragmas:** `dirty`

Declare a test suite identified by name with optional setup and/or teardown section.

A test suite is a series of one or more related tests sharing a common fixture (setup, teardown). The fixture is executed for EACH test.

```
suite "test suite for addition":
  setup:
    let result = 4
  
  test "2 + 2 = 4":
    check(2+2 == result)
  
  test "(2 + -2) != 4":
    check(2 + -2 != result)
  
  # No teardown needed
```

The suite will run the individual test cases in the order in which they were listed. With default global settings the above code prints:

```
[Suite] test suite for addition
  [OK] 2 + 2 = 4
  [OK] (2 + -2) != 4
```

### test

[ref: #symbol-test]

Define a single test case identified by name.

**Input:**
- `name: `
- `body: `

**Output:** *(none)*
**Pragmas:** `dirty`

Define a single test case identified by name.

```
test "roses are red":
  let roses = "red"
  check(roses == "red")
```

The above code outputs:

```
[OK] roses are red
```

## Type

### ConsoleOutputFormatter

[ref: #symbol-consoleoutputformatter]

```nim
ConsoleOutputFormatter = ref object of OutputFormatter
```

### JUnitOutputFormatter

[ref: #symbol-junitoutputformatter]

```nim
JUnitOutputFormatter = ref object of OutputFormatter
```

### OutputFormatter

[ref: #symbol-outputformatter]

```nim
OutputFormatter = ref object of RootObj
```

### OutputLevel

[ref: #symbol-outputlevel]

```nim
OutputLevel = enum
  PRINT_ALL,                ## Print as much as possible.
  PRINT_FAILURES,           ## Print only the failed tests.
  PRINT_NONE                 ## Print nothing.
```

The output verbosity of the tests.

### TestResult

[ref: #symbol-testresult]

```nim
TestResult = object
  suiteName*: string ## Name of the test suite that contains this test case.
                     ## Can be ``nil`` if the test case is not in a suite.
  testName*: string          ## Name of the test case
  status*: TestStatus
```

### TestStatus

[ref: #symbol-teststatus]

```nim
TestStatus = enum
  OK, FAILED, SKIPPED
```

The status of a test when it is done.

## Var

### abortOnError

[ref: #symbol-abortonerror]

Set to true in order to quit immediately on fail. Default is false, or override with -d:nimUnittestAbortOnError:on|off.

```nim
abortOnError {.threadvar.}: bool
```

Set to true in order to quit immediately on fail. Default is false, or override with -d:nimUnittestAbortOnError:on|off.

Deprecated: can also override depending on whether NIMTEST\_ABORT\_ON\_ERROR environment variable is set.
