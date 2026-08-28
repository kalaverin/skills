---
source_hash: 19598ef80290012e
source_path: lib/pure/strformat.nim
---

# strformat

[ref: #module-strformat]

String interpolation / format inspired by Python's f-strings.

# [fmt vs. &](#nimfmt-vsdot-nimamp)

You can use either fmt or the unary & operator for formatting. The difference between them is subtle but important.

The fmt"{expr}" syntax is more aesthetically pleasing, but it hides a small gotcha. The string is a [generalized raw string literal](manual.html#lexical-analysis-generalized-raw-string-literals). This has some surprising effects:

Because the literal is a raw string literal, the \n is not interpreted as an escape sequence.

There are multiple ways to get around this, including the use of the & operator:

The choice of style is up to you.

# [Formatting strings](#formatting-strings)

# [Formatting floats](#formatting-floats)

# [Expressions](#expressions)

# [Debugging strings](#debugging-strings)

fmt"{expr=}" expands to fmt"expr={expr}" namely the text of the expression, an equal sign and the results of evaluated expression.

Note that it is space sensitive:

# [Implementation details](#implementation-details)

An expression like &"{key} is {value:arg} {{z}}" is transformed into:

```
var temp = newStringOfCap(educatedCapGuess)
temp.formatValue(key, "")
temp.add(" is ")
temp.formatValue(value, arg)
temp.add(" {z}")
temp
```

Parts of the string that are enclosed in the curly braces are interpreted as Nim code. To escape a { or }, double it.

Within a curly expression, however, {, }, must be escaped with a backslash.

To enable evaluating Nim expressions within curlies, colons inside parentheses do not need to be escaped.

& delegates most of the work to an open overloaded set of formatValue procs. The required signature for a type T that supports formatting is usually proc formatValue(result: var string; x: T; specifier: string).

The subexpression after the colon (arg in &"{key} is {value:arg} {{z}}") is optional. It will be passed as the last argument to formatValue. When the colon with the subexpression it is left out, an empty string will be taken instead.

For strings and numeric types the optional argument is a so-called "standard format specifier".

# [Standard format specifiers for strings, integers and floats](#standard-format-specifiers-for-strings-integers-and-floats)

The general form of a standard format specifier is:

```
[[fill]align][sign][#][0][minimumwidth][.precision][type]
```

The square brackets [] indicate an optional element.

The optional align flag can be one of the following:

<
:   Forces the field to be left-aligned within the available space. (This is the default for strings.)

>
:   Forces the field to be right-aligned within the available space. (This is the default for numbers.)

^
:   Forces the field to be centered within the available space.

Note that unless a minimum field width is defined, the field width will always be the same size as the data to fill it, so that the alignment option has no meaning in this case.

The optional fill character defines the character to be used to pad the field to the minimum width. The fill character, if present, must be followed by an alignment flag.

The sign option is only valid for numeric types, and can be one of the following:

| Sign | Meaning |
| --- | --- |
| + | Indicates that a sign should be used for both positive as well as negative numbers. |
| - | Indicates that a sign should be used only for negative numbers (this is the default behavior). |
| (space) | Indicates that a leading space should be used on positive numbers. |

If the # character is present, integers use the 'alternate form' for formatting. This means that binary, octal and hexadecimal output will be prefixed with 0b, 0o and 0x, respectively.

width is a decimal integer defining the minimum field width. If not specified, then the field width will be determined by the content.

If the width field is preceded by a zero (0) character, this enables zero-padding.

The precision is a decimal number indicating how many digits should be displayed after the decimal point in a floating point conversion. For non-numeric types the field indicates the maximum field size - in other words, how many characters will be used from the field content. The precision is ignored for integer conversions.

Finally, the type determines how the data should be presented.

The available integer presentation types are:

| Type | Result |
| --- | --- |
| b | Binary. Outputs the number in base 2. |
| d | Decimal Integer. Outputs the number in base 10. |
| o | Octal format. Outputs the number in base 8. |
| x | Hex format. Outputs the number in base 16, using lower-case letters for the digits above 9. |
| X | Hex format. Outputs the number in base 16, using uppercase letters for the digits above 9. |
| (None) | The same as d. |

The available floating point presentation types are:

| Type | Result |
| --- | --- |
| e | Exponent notation. Prints the number in scientific notation using the letter e to indicate the exponent. |
| E | Exponent notation. Same as e except it converts the number to uppercase. |
| f | Fixed point. Displays the number as a fixed-point number. |
| F | Fixed point. Same as f except it converts the number to uppercase. |
| g | General format. This prints the number as a fixed-point number, unless the number is too large, in which case it switches to e exponent notation. |
| G | General format. Same as g except it switches to E if the number gets to large. |
| i | Complex General format. This is only supported for complex numbers, which it prints using the mathematical (RE+IMj) format. The real and imaginary parts are printed using the general format g by default, but it is possible to combine this format with one of the other formats (e.g jf). |
| (None) | Similar to g, except that it prints at least one digit after the decimal point. |

# [Limitations](#limitations)

Because of the well defined order how templates and macros are expanded, strformat cannot expand template arguments:

```
template myTemplate(arg: untyped): untyped =
  echo "arg is: ", arg
  echo &"--- {arg} ---"

let x = "abc"
myTemplate(x)
```

First the template myTemplate is expanded, where every identifier arg is substituted with its argument. The arg inside the format string is not seen by this process, because it is part of a quoted string literal. It is not an identifier yet. Then the strformat macro creates the arg identifier from the string literal, an identifier that cannot be resolved anymore.

The workaround for this is to bind the template argument to a new local variable.

```
template myTemplate(arg: untyped): untyped =
  block:
    let arg1 {.inject.} = arg
    echo "arg is: ", arg1
    echo &"--- {arg1} ---"
```

The use of {.inject.} here is necessary again because of template expansion order and hygienic templates. But since we generally want to keep the hygiene of myTemplate, and we do not want arg1 to be injected into the context where myTemplate is expanded, everything is wrapped in a block.

# [Future directions](#future-directions)

A curly expression with commas in it like {x, argA, argB} could be transformed to formatValue(result, x, argA, argB) in order to support formatters that do not need to parse a custom language within a custom language but instead prefer to use Nim's existing syntax. This would also help with readability, since there is only so much you can cram into single letter DSLs.

## Examples

```nim
import std/strformat
let msg = "hello"
assert fmt"{msg}\n" == "hello\\n"
```

```nim
import std/strformat
let msg = "hello"

assert &"{msg}\n" == "hello\n"

assert fmt"{msg}{'\n'}" == "hello\n"
assert fmt("{msg}\n") == "hello\n"
assert "{msg}\n".fmt == "hello\n"
```

```nim
import std/strformat
assert &"""{"abc":>4}""" == " abc"
assert &"""{"abc":<4}""" == "abc "
```

```nim
import std/strformat
assert fmt"{-12345:08}" == "-0012345"
assert fmt"{-1:3}" == " -1"
assert fmt"{-1:03}" == "-01"
assert fmt"{16:#X}" == "0x10"

assert fmt"{123.456}" == "123.456"
assert fmt"{123.456:>9.3f}" == "  123.456"
assert fmt"{123.456:9.3f}" == "  123.456"
assert fmt"{123.456:9.4f}" == " 123.4560"
assert fmt"{123.456:>9.0f}" == "     123."
assert fmt"{123.456:<9.4f}" == "123.4560 "

assert fmt"{123.456:e}" == "1.234560e+02"
assert fmt"{123.456:>13e}" == " 1.234560e+02"
assert fmt"{123.456:13e}" == " 1.234560e+02"
```

```nim
import std/strformat
let x = 3.14
assert fmt"{(if x!=0: 1.0/x else: 0):.5}" == "0.31847"
assert fmt"""{(block:
    var res: string
    for i in 1..15:
      res.add (if i mod 15 == 0: "FizzBuzz"
        elif i mod 5 == 0: "Buzz"
        elif i mod 3 == 0: "Fizz"
        else: $i) & " "
    res)}""" == "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz "
```

```nim
import std/strformat
assert fmt"{123.456=}" == "123.456=123.456"
assert fmt"{123.456=:>9.3f}" == "123.456=  123.456"

let x = "hello"
assert fmt"{x=}" == "x=hello"
assert fmt"{x =}" == "x =hello"

let y = 3.1415926
assert fmt"{y=:.2f}" == fmt"y={y:.2f}"
assert fmt"{y=}" == fmt"y={y}"
assert fmt"{y = : <8}" == fmt"y = 3.14159 "

proc hello(a: string, b: float): int = 12
assert fmt"{hello(x, y) = }" == "hello(x, y) = 12"
assert fmt"{x.hello(y) = }" == "x.hello(y) = 12"
assert fmt"{hello x, y = }" == "hello x, y = 12"
```

```nim
import std/strformat
let x = "12"
assert fmt"{x=}" == "x=12"
assert fmt"{x =:}" == "x =12"
assert fmt"{x =}" == "x =12"
assert fmt"{x= :}" == "x= 12"
assert fmt"{x= }" == "x= 12"
assert fmt"{x = :}" == "x = 12"
assert fmt"{x = }" == "x = 12"
assert fmt"{x   =  :}" == "x   =  12"
assert fmt"{x   =  }" == "x   =  12"
```

```nim
var temp = newStringOfCap(educatedCapGuess)
temp.formatValue(key, "")
temp.add(" is ")
temp.formatValue(value, arg)
temp.add(" {z}")
temp
```

```nim
import std/strformat
let x = "hello"
assert fmt"""{ "\{(" & x & ")\}" }""" == "{(hello)}"
assert fmt"""{{({ x })}}""" == "{(hello)}"
assert fmt"""{ $(\{x:1,"world":2\}) }""" == """[("hello", 1), ("world", 2)]"""
```

```nim
template myTemplate(arg: untyped): untyped =
  echo "arg is: ", arg
  echo &"--- {arg} ---"

let x = "abc"
myTemplate(x)
```

```nim
template myTemplate(arg: untyped): untyped =
  block:
    let arg1 {.inject.} = arg
    echo "arg is: ", arg1
    echo &"--- {arg1} ---"
```

```nim
let x = 7
assert &"{x}\n" == "7\n" # regular string literal
assert &"{x}\n" == "{x}\n".fmt # `fmt` can be used instead
assert &"{x}\n" != fmt"{x}\n" # see `fmt` docs, this would use a raw string literal
```

```nim
let x = 7
assert "var is {x * 2}".fmt == "var is 14"
assert "var is {{x}}".fmt == "var is {x}" # escape via doubling
const s = "foo: {x}"
assert s.fmt == "foo: 7" # also works with const strings

assert fmt"\n" == r"\n" # raw string literal
assert "\n".fmt == "\n" # regular literal (likewise with `fmt("\n")` or `fmt "\n"`)
```

```nim
# custom `openChar`, `closeChar`
let x = 7
assert "<x>".fmt('<', '>') == "7"
assert "<<<x>>>".fmt('<', '>') == "<7>"
assert "`x`".fmt('`', '`') == "7"
```

## Proc

### alignString

[ref: #symbol-alignstring]

**Input:**
- `s: string`
- `minimumWidth: int`
- `align:  = '\x00'`
- `fill:  = ' '`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Aligns s using the fill char. This is only of interest if you want to write a custom format proc that should support the standard format specifiers.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: T`
- `specifier: static string`

**Output:** *(none)*
**Generic parameters:** `T`, `specifier:type`

Standard format implementation for SomeInteger. It makes little sense to call this directly, but it is required to exist by the & macro.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: T`
- `specifier: string`

**Output:** *(none)*
**Generic parameters:** `T`

Standard format implementation for SomeInteger. It makes little sense to call this directly, but it is required to exist by the & macro.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: SomeFloat`
- `specifier: static string`

**Output:** *(none)*
**Generic parameters:** `SomeFloat`, `specifier:type`

Standard format implementation for SomeFloat. It makes little sense to call this directly, but it is required to exist by the & macro.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: SomeFloat`
- `specifier: string`

**Output:** *(none)*
**Generic parameters:** `SomeFloat`

Standard format implementation for SomeFloat. It makes little sense to call this directly, but it is required to exist by the & macro.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: string`
- `specifier: static string`

**Output:** *(none)*
**Generic parameters:** `specifier:type`

Standard format implementation for string. It makes little sense to call this directly, but it is required to exist by the & macro.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: string`
- `specifier: string`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Standard format implementation for string. It makes little sense to call this directly, but it is required to exist by the & macro.

### parseStandardFormatSpecifier

[ref: #symbol-parsestandardformatspecifier]

An exported helper proc that parses the "standard format specifiers", as specified by the grammar:

**Input:**
- `s: string`
- `start:  = 0`
- `ignoreUnknownSuffix:  = false`

**Output:** `StandardFormatSpecifier`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

An exported helper proc that parses the "standard format specifiers", as specified by the grammar:

```
[[fill]align][sign][#][0][minimumwidth][.precision][type]
```

This is only of interest if you want to write a custom format proc that should support the standard format specifiers. If ignoreUnknownSuffix is true, an unknown suffix after the type field is not an error.

## Template

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `pattern: string{lit}`

**Output:** `string`
**Pragmas:** `callsite`

&pattern is the same as pattern.fmt. For a specification of the & macro, see the module level documentation.

### fmt

[ref: #symbol-fmt]

**Input:**
- `pattern: static string`
- `openChar: static char`
- `closeChar: static char`

**Output:** `string`
**Generic parameters:** `pattern:type`, `openChar:type`, `closeChar:type`

**Pragmas:** `callsite`

Interpolates pattern using symbols in scope.

### fmt

[ref: #symbol-fmt]

**Input:**
- `pattern: static string`

**Output:** `untyped`
**Generic parameters:** `pattern:type`

**Pragmas:** `callsite`

Alias for fmt(pattern, '{', '}').

## Type

### StandardFormatSpecifier

[ref: #symbol-standardformatspecifier]

```nim
StandardFormatSpecifier = object
  fill*, align*: char        ## Desired fill and alignment.
  sign*: char                ## Desired sign.
  alternateForm*: bool       ## Whether to prefix binary, octal and hex numbers
                             ## with `0b`, `0o`, `0x`.
  padWithZero*: bool         ## Whether to pad with zeros rather than spaces.
  minimumWidth*, precision*: int ## Desired minimum width and precision.
  typ*: char                 ## Type like 'f', 'g' or 'd'.
  endPosition*: int          ## End position in the format specifier after
                             ## `parseStandardFormatSpecifier` returned.
```

Type that describes "standard format specifiers".
