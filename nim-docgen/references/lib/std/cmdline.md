---
source_hash: 906782d23c69bdaf
source_path: lib/std/cmdline.nim
---

# cmdline

[ref: #module-cmdline]

This module contains system facilities for reading command line parameters.**See also:**

* [parseopt module](parseopt.html) for command-line parser beyond [parseCmdLine](#parseCmdLine)

## Examples

```nim
when declared(commandLineParams):
  # Use commandLineParams() here
else:
  # Do something else!
```

```nim
when declared(paramCount):
  # Use paramCount() here
else:
  # Do something else!
```

```nim
when declared(paramStr):
  # Use paramStr() here
else:
  # Do something else!
```

## Proc

### commandLineParams

[ref: #symbol-commandlineparams]

Convenience proc which returns the command line parameters.

**Input:**
- *(none)*

**Output:** `seq[string]`
**Pragmas:** `raises: []`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadIOEffect`, `forbids: `

Convenience proc which returns the command line parameters.

This returns **only** the parameters. If you want to get the application executable filename, call [getAppFilename()](os.html#getAppFilename).

**Availability**: On Posix there is no portable way to get the command line from a DLL and thus the proc isn't defined in this environment. You can test for its availability with [declared()](system.html#declared,untyped).

See also:

* [parseopt module](parseopt.html)
* [parseCmdLine](#parseCmdLine)
* [paramCount](#paramCount)
* [paramStr](#paramStr)
* [getAppFilename proc](os.html#getAppFilename)

**Examples:**

```
when declared(commandLineParams):
  # Use commandLineParams() here
else:
  # Do something else!
```

### paramCount

[ref: #symbol-paramcount]

Returns the number of command line arguments given to the application.

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Returns the number of command line arguments given to the application.

Unlike argc in C, if your binary was called without parameters this will return zero. You can query each individual parameter with [paramStr](#paramStr) or retrieve all of them in one go with [commandLineParams](#commandLineParams).

**Availability**: When generating a dynamic library (see --app:lib) on Posix this proc is not defined. Test for availability using [declared()](system.html#declared,untyped).

See also:

* [parseopt module](parseopt.html)
* [parseCmdLine](#parseCmdLine)
* [paramStr](#paramStr)
* [commandLineParams](#commandLineParams)

**Examples:**

```
when declared(paramCount):
  # Use paramCount() here
else:
  # Do something else!
```

### paramStr

[ref: #symbol-paramstr]

Returns the i-th command line argument given to the application.

**Input:**
- `i: int`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Returns the i-th command line argument given to the application.

i should be in the range 1..paramCount(), the IndexDefect exception will be raised for invalid values. Instead of iterating over [paramCount](#paramCount) with this proc you can call the convenience [commandLineParams](#commandLineParams).

Similarly to argv in C, it is possible to call paramStr(0) but this will return OS specific contents (usually the name of the invoked executable). You should avoid this and call [getAppFilename()](os.html#getAppFilename) instead.

**Availability**: When generating a dynamic library (see --app:lib) on Posix this proc is not defined. Test for availability using [declared()](system.html#declared,untyped).

See also:

* [parseopt module](parseopt.html)
* [parseCmdLine](#parseCmdLine)
* [paramCount](#paramCount)
* [commandLineParams](#commandLineParams)
* [getAppFilename proc](os.html#getAppFilename)

**Examples:**

```
when declared(paramStr):
  # Use paramStr() here
else:
  # Do something else!
```

### parseCmdLine

[ref: #symbol-parsecmdline]

Splits a command line into several components.

**Input:**
- `c: string`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a command line into several components.

**Note**: This proc is only occasionally useful, better use the [parseopt module](parseopt.html).

On Windows, it uses the [following parsing rules](https://msdn.microsoft.com/en-us/library/17w5ykft.aspx):

* Arguments are delimited by white space, which is either a space or a tab.
* The caret character (^) is not recognized as an escape character or delimiter. The character is handled completely by the command-line parser in the operating system before being passed to the argv array in the program.
* A string surrounded by double quotation marks ("string") is interpreted as a single argument, regardless of white space contained within. A quoted string can be embedded in an argument.
* A double quotation mark preceded by a backslash (") is interpreted as a literal double quotation mark character (").
* Backslashes are interpreted literally, unless they immediately precede a double quotation mark.
* If an even number of backslashes is followed by a double quotation mark, one backslash is placed in the argv array for every pair of backslashes, and the double quotation mark is interpreted as a string delimiter.
* If an odd number of backslashes is followed by a double quotation mark, one backslash is placed in the argv array for every pair of backslashes, and the double quotation mark is "escaped" by the remaining backslash, causing a literal double quotation mark (") to be placed in argv.

On Posix systems, it uses the following parsing rules: Components are separated by whitespace unless the whitespace occurs within " or ' quotes.

See also:

* [parseopt module](parseopt.html)
* [paramCount](#paramCount)
* [paramStr](#paramStr)
* [commandLineParams](#commandLineParams)
