---
source_hash: 58d2d4b1a3815683
source_path: lib/pure/parsecfg.nim
---

# parsecfg

[ref: #module-parsecfg]

The parsecfg module implements a high performance configuration file parser. The configuration file's syntax is similar to the Windows .ini format, but much more powerful, as it is not a line based parser. String literals, raw string literals and triple quoted string literals are supported as in the Nim programming language.

Example of how a configuration file may look like:

```
# This is a comment.
; this too.

[Common]
cc=gcc     # '=' and ':' are the same
--foo="bar"   # '--cc' and 'cc' are the same, 'bar' and '"bar"' are the same (except for '#')
macrosym: "#"  # Note that '#' is interpreted as a comment without the quotation
--verbose

[Windows]
isConsoleApplication=False ; another comment

[Posix]
isConsoleApplication=True

key1: "in this string backslash escapes are interpreted\n"
key2: r"in this string not"
key3: """triple quotes strings
are also supported. They may span
multiple lines."""

--"long option with spaces": r"c:\myfiles\test.txt"
```

Here is an example of how to use the configuration file parser:

## [Configuration file example](#configuration-file-example)

```
charset = "utf-8"
[Package]
name = "hello"
--threads:on
[Author]
name = "nim-lang"
website = "nim-lang.org"
```

## [Creating a configuration file](#creating-a-configuration-file)

## [Reading a configuration file](#reading-a-configuration-file)

## [Modifying a configuration file](#modifying-a-configuration-file)

## [Deleting a section key in a configuration file](#deleting-a-section-key-in-a-configuration-file)

## [Supported INI File structure](#supported-ini-file-structure)

## Examples

```nim
import std/parsecfg
import std/[strutils, streams]

let configFile = "example.ini"
var f = newFileStream(configFile, fmRead)
assert f != nil, "cannot open " & configFile
var p: CfgParser
open(p, f, configFile)
while true:
  var e = next(p)
  case e.kind
  of cfgEof: break
  of cfgSectionStart:   ## a `[section]` has been parsed
    echo "new section: " & e.section
  of cfgKeyValuePair:
    echo "key-value-pair: " & e.key & ": " & e.value
  of cfgOption:
    echo "command: " & e.key & ": " & e.value
  of cfgError:
    echo e.msg
close(p)
```

```nim
charset = "utf-8"
[Package]
name = "hello"
--threads:on
[Author]
name = "nim-lang"
website = "nim-lang.org"
```

```nim
import std/parsecfg
var dict = newConfig()
dict.setSectionKey("","charset", "utf-8")
dict.setSectionKey("Package", "name", "hello")
dict.setSectionKey("Package", "--threads", "on")
dict.setSectionKey("Author", "name", "nim-lang")
dict.setSectionKey("Author", "website", "nim-lang.org")
assert $dict == """
charset=utf-8
[Package]
name=hello
--threads:on
[Author]
name=nim-lang
website=nim-lang.org
"""
```

```nim
import std/parsecfg
let dict = loadConfig("config.ini")
let charset = dict.getSectionValue("","charset")
let threads = dict.getSectionValue("Package","--threads")
let pname = dict.getSectionValue("Package","name")
let name = dict.getSectionValue("Author","name")
let website = dict.getSectionValue("Author","website")
echo pname & "\n" & name & "\n" & website
```

```nim
import std/parsecfg
var dict = loadConfig("config.ini")
dict.setSectionKey("Author", "name", "nim-lang")
dict.writeConfig("config.ini")
```

```nim
import std/parsecfg
var dict = loadConfig("config.ini")
dict.delSectionKey("Author", "website")
dict.writeConfig("config.ini")
```

```nim
import std/parsecfg
import std/streams

var dict = loadConfig(newStringStream("""[Simple Values]
    key=value
    spaces in keys=allowed
    spaces in values=allowed as well
    spaces around the delimiter = obviously
    you can also use : to delimit keys from values
    [All Values Are Strings]
    values like this: 19990429
    or this: 3.14159265359
    are they treated as numbers : no
    integers floats and booleans are held as: strings
    can use the API to get converted values directly: true
    [No Values]
    key_without_value
    # empty string value is not allowed =
    [ Seletion A   ]
    space around section name will be ignored
    [You can use comments]
    # like this
    ; or this
    # By default only in an empty line.
    # Inline comments can be harmful because they prevent users
    # from using the delimiting characters as parts of values.
    # That being said, this can be customized.
        [Sections Can Be Indented]
            can_values_be_as_well = True
            does_that_mean_anything_special = False
            purpose = formatting for readability
            # Did I mention we can indent comments, too?
    """)
)

let section1 = "Simple Values"
assert dict.getSectionValue(section1, "key") == "value"
assert dict.getSectionValue(section1, "spaces in keys") == "allowed"
assert dict.getSectionValue(section1, "spaces in values") == "allowed as well"
assert dict.getSectionValue(section1, "spaces around the delimiter") == "obviously"
assert dict.getSectionValue(section1, "you can also use") == "to delimit keys from values"

let section2 = "All Values Are Strings"
assert dict.getSectionValue(section2, "values like this") == "19990429"
assert dict.getSectionValue(section2, "or this") == "3.14159265359"
assert dict.getSectionValue(section2, "are they treated as numbers") == "no"
assert dict.getSectionValue(section2, "integers floats and booleans are held as") == "strings"
assert dict.getSectionValue(section2, "can use the API to get converted values directly") == "true"

let section3 = "Seletion A"
assert dict.getSectionValue(section3, 
  "space around section name will be ignored", "not an empty value") == ""

let section4 = "Sections Can Be Indented"
assert dict.getSectionValue(section4, "can_values_be_as_well") == "True"
assert dict.getSectionValue(section4, "does_that_mean_anything_special") == "False"
assert dict.getSectionValue(section4, "purpose") == "formatting for readability"
```

## Iterator

### sections

[ref: #symbol-sections]

**Input:**
- `dict: Config`

**Output:** `lent string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates through the sections in the dict.

## Proc

### `$`

[ref: #symbol-]

Writes the contents of the table to string.

**Input:**
- `dict: Config`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes the contents of the table to string.

**Note:**
Comment statement will be ignored.

### close

[ref: #symbol-close]

**Input:**
- `c: var CfgParser`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Closes the parser c and its associated input stream.

### delSection

[ref: #symbol-delsection]

**Input:**
- `dict: var Config`
- `section: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes the specified section and all of its sub keys.

### delSectionKey

[ref: #symbol-delsectionkey]

**Input:**
- `dict: var Config`
- `section: string`
- `key: string`

**Output:** *(none)*
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Deletes the key of the specified section.

### errorStr

[ref: #symbol-errorstr]

**Input:**
- `c: CfgParser`
- `msg: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a properly formatted error message containing current line and column information.

### getColumn

[ref: #symbol-getcolumn]

**Input:**
- `c: CfgParser`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the current column the parser has arrived at.

### getFilename

[ref: #symbol-getfilename]

**Input:**
- `c: CfgParser`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the filename of the file that the parser processes.

### getLine

[ref: #symbol-getline]

**Input:**
- `c: CfgParser`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the current line the parser has arrived at.

### getSectionValue

[ref: #symbol-getsectionvalue]

**Input:**
- `dict: Config`
- `section: string`
- `key: string`
- `defaultVal:  = ""`

**Output:** `string`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Gets the key value of the specified Section. Returns the specified default value if the specified key does not exist.

### ignoreMsg

[ref: #symbol-ignoremsg]

**Input:**
- `c: CfgParser`
- `e: CfgEvent`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a properly formatted warning message containing that an entry is ignored.

### loadConfig

[ref: #symbol-loadconfig]

**Input:**
- `stream: Stream`
- `filename: string = "[stream]"`

**Output:** `Config`
**Pragmas:** `raises: [IOError, OSError, ValueError, KeyError]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, KeyError`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Loads the specified configuration from stream into a new Config instance. filename parameter is only used for nicer error messages.

### loadConfig

[ref: #symbol-loadconfig]

**Input:**
- `filename: string`

**Output:** `Config`
**Pragmas:** `raises: [IOError, OSError, ValueError, KeyError]`, `tags: [ReadIOEffect, WriteIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, KeyError`, `tags: ReadIOEffect, WriteIOEffect, RootEffect`, `forbids: `

Loads the specified configuration file into a new Config instance.

### newConfig

[ref: #symbol-newconfig]

**Input:**
- *(none)*

**Output:** `Config`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new configuration table. Useful when wanting to create a configuration file.

### next

[ref: #symbol-next]

**Input:**
- `c: var CfgParser`

**Output:** `CfgEvent`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: [ValueError, OSError, IOError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError, IOError`, `tags: ReadIOEffect`, `forbids: `

Retrieves the first/next event. This controls the parser.

### open

[ref: #symbol-open]

**Input:**
- `c: var CfgParser`
- `input: Stream`
- `filename: string`
- `lineOffset:  = 0`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: [IOError, OSError, ValueError]`, `tags: [ReadIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError`, `tags: ReadIOEffect, RootEffect`, `forbids: `

Initializes the parser with an input stream. Filename is only used for nice error messages. lineOffset can be used to influence the line number information in the generated error messages.

### setSectionKey

[ref: #symbol-setsectionkey]

**Input:**
- `dict: var Config`
- `section: string`
- `key: string`
- `value: string`

**Output:** *(none)*
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Sets the Key value of the specified Section.

### warningStr

[ref: #symbol-warningstr]

**Input:**
- `c: CfgParser`
- `msg: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a properly formatted warning message containing current line and column information.

### writeConfig

[ref: #symbol-writeconfig]

Writes the contents of the table to the specified stream.

**Input:**
- `dict: Config`
- `stream: Stream`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes the contents of the table to the specified stream.

**Note:**
Comment statement will be ignored.

### writeConfig

[ref: #symbol-writeconfig]

Writes the contents of the table to the specified configuration file.

**Input:**
- `dict: Config`
- `filename: string`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes the contents of the table to the specified configuration file.

**Note:**
Comment statement will be ignored.

## Type

### CfgEvent

[ref: #symbol-cfgevent]

```nim
CfgEvent = object of RootObj
  case kind*: CfgEventKind   ## the kind of the event
  of cfgEof:
    nil
  of cfgSectionStart:
    section*: string         ## `section` contains the name of the
                             ## parsed section start (syntax: `[section]`)
  of cfgKeyValuePair, cfgOption:
    key*, value*: string     ## contains the (key, value) pair if an option
                             ## of the form `--key: value` or an ordinary
                             ## `key= value` pair has been parsed.
                             ## `value==""` if it was not specified in the
                             ## configuration file.
  of cfgError:              ## the parser encountered an error: `msg`
    msg*: string             ## contains the error message. No exceptions
                             ## are thrown if a parse error occurs.
```

describes a parsing event

### CfgEventKind

[ref: #symbol-cfgeventkind]

```nim
CfgEventKind = enum
  cfgEof,                   ## end of file reached
  cfgSectionStart,          ## a `[section]` has been parsed
  cfgKeyValuePair,          ## a `key=value` pair has been detected
  cfgOption,                ## a `--key=value` command line option
  cfgError                   ## an error occurred during parsing
```

enumeration of all events that may occur when parsing

### CfgParser

[ref: #symbol-cfgparser]

```nim
CfgParser = object of BaseLexer
```

the parser object.

### Config

[ref: #symbol-config]

```nim
Config = OrderedTableRef[string, OrderedTableRef[string, string]]
```
