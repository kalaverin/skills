---
source_hash: 0d7ceb967b1553c5
source_path: lib/js/jsffi.nim
---

# jsffi

[ref: #module-jsffi]

This Module implements types and macros to facilitate the wrapping of, and interaction with JavaScript libraries. Using the provided types JsObject and JsAssoc together with the provided macros allows for smoother interfacing with JavaScript, allowing for example quick and easy imports of JavaScript variables:

## Examples

```nim
import std/jsffi
# Here, we are using jQuery for just a few calls and do not want to wrap the
# whole library:

# import the document object and the console
var document {.importc, nodecl.}: JsObject
var console {.importc, nodecl.}: JsObject
# import the "$" function
proc jq(selector: JsObject): JsObject {.importjs: "$$(#)".}

# Use jQuery to make the following code run, after the document is ready.
# This uses an experimental `.()` operator for `JsObject`, to emit
# JavaScript calls, when no corresponding proc exists for `JsObject`.
proc main =
  jq(document).ready(proc() =
    console.log("Hello JavaScript!")
  )
```

```nim
let obj = newJsObject()
obj.a = 20
assert obj.a.to(int) == 20
```

```nim
# Let's get back to the console example:
var console {.importc, nodecl.}: JsObject
let res = console.log("I return undefined!")
console.log(res) # This prints undefined, as console.log always returns
                 # undefined. Thus one has to be careful, when using
                 # JsObject calls.
```

```nim
var obj = {a: 10};
obj.someMethod = function() {
  return this.a + 42;
};
```

```nim
let obj = JsObject{ a: 10 }
proc someMethodImpl(that: JsObject): int =
  that.a.to(int) + 42
obj.someMethod = bindMethod someMethodImpl

# Alternatively:
obj.someMethod = bindMethod
  proc(that: JsObject): int = that.a.to(int) + 42
```

```nim
# Let's say we have a type with a ton of fields, where some fields do not
# need to be set, and we do not want those fields to be set to `nil`:
type
  ExtremelyHugeType = ref object
    a, b, c, d, e, f, g: int
    h, i, j, k, l: cstring
    # And even more fields ...

let obj = ExtremelyHugeType{ a: 1, k: "foo".cstring, d: 42 }

# This generates roughly the same JavaScript as:
{.emit: "var obj = {a: 1, k: "foo", d: 42};".}
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `obj: JsObject`

**Output:** `JsObject`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields the values of each field in a JsObject, wrapped into a JsObject.

### items

[ref: #symbol-items]

**Input:**
- `assoc: JsAssoc[K, V]`

**Output:** `V`
**Generic parameters:** `K`, `V`

Yields the values in a JsAssoc.

### keys

[ref: #symbol-keys]

**Input:**
- `obj: JsObject`

**Output:** `cstring`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields the names of each field in a JsObject.

### keys

[ref: #symbol-keys]

**Input:**
- `assoc: JsAssoc[K, V]`

**Output:** `K`
**Generic parameters:** `K`, `V`

Yields the keys in a JsAssoc.

### pairs

[ref: #symbol-pairs]

**Input:**
- `obj: JsObject`

**Output:** `(cstring, JsObject)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields tuples of type (cstring, JsObject), with the first entry being the name of a fields in the JsObject and the second being its value wrapped into a JsObject.

### pairs

[ref: #symbol-pairs]

**Input:**
- `assoc: JsAssoc[K, V]`

**Output:** `(K, V)`
**Generic parameters:** `K`, `V`

Yields tuples of type (K, V), with the first entry being a key in the JsAssoc and the second being its corresponding value.

## Macro

### `.()`

[ref: #symbol-]

Experimental "method call" operator for type JsObject. Takes the name of a method of the JavaScript object (field) and calls it with args as arguments, returning a JsObject (which may be discarded, and may be undefined, if the method does not return anything, so be careful when using this.)

**Input:**
- `obj: JsObject`
- `field: untyped`
- `args: varargs[JsObject, jsFromAst]`

**Output:** `JsObject`
Experimental "method call" operator for type JsObject. Takes the name of a method of the JavaScript object (field) and calls it with args as arguments, returning a JsObject (which may be discarded, and may be undefined, if the method does not return anything, so be careful when using this.)

Example:

```
# Let's get back to the console example:
var console {.importc, nodecl.}: JsObject
let res = console.log("I return undefined!")
console.log(res) # This prints undefined, as console.log always returns
                 # undefined. Thus one has to be careful, when using
                 # JsObject calls.
```

### `.()`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[K, V]`
- `field: untyped`
- `args: varargs[untyped]`

**Output:** `auto`
**Generic parameters:** `K`, `V`

Experimental "method call" operator for type JsAssoc. Takes the name of a method of the JavaScript object (field) and calls it with args as arguments. Here, everything is typechecked, so you do not have to worry about undefined return values.

### `.=`

[ref: #symbol-]

**Input:**
- `obj: JsObject`
- `field: untyped`
- `value: untyped`

**Output:** `untyped`
Experimental dot accessor (set) for type JsObject. Sets the value of a property of name field in a JsObject x to value.

### `.=`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[K, V]`
- `field: untyped`
- `value: V`

**Output:** `untyped`
**Generic parameters:** `K`, `V`

Experimental dot accessor (set) for type JsAssoc. Sets the value of a property of name field in a JsObject x to value.

### `.`

[ref: #symbol-]

**Input:**
- `obj: JsObject`
- `field: untyped`

**Output:** `JsObject`
Experimental dot accessor (get) for type JsObject. Returns the value of a property of name field from a JsObject x.

### `.`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[K, V]`
- `field: untyped`

**Output:** `V`
**Generic parameters:** `K`, `V`

Experimental dot accessor (get) for type JsAssoc. Returns the value of a property of name field from a JsObject x.

### `{}`

[ref: #symbol-]

Takes a typedesc as its first argument, and a series of expressions of type key: value, and returns a value of the specified type with each field key set to value, as specified in the arguments of {}.

**Input:**
- `typ: typedesc`
- `xs: varargs[untyped]`

**Output:** `auto`
**Generic parameters:** `typ:type`

Takes a typedesc as its first argument, and a series of expressions of type key: value, and returns a value of the specified type with each field key set to value, as specified in the arguments of {}.

Example:

```
# Let's say we have a type with a ton of fields, where some fields do not
# need to be set, and we do not want those fields to be set to `nil`:
type
  ExtremelyHugeType = ref object
    a, b, c, d, e, f, g: int
    h, i, j, k, l: cstring
    # And even more fields ...

let obj = ExtremelyHugeType{ a: 1, k: "foo".cstring, d: 42 }

# This generates roughly the same JavaScript as:
{.emit: "var obj = {a: 1, k: "foo", d: 42};".}
```

### bindMethod

[ref: #symbol-bindmethod]

Takes the name of a procedure and wraps it into a lambda missing the first argument, which passes the JavaScript builtin this as the first argument to the procedure. Returns the resulting lambda.

**Input:**
- `procedure: typed`

**Output:** `auto`
**Pragmas:** `deprecated: "Don\'t use it with closures"`

Takes the name of a procedure and wraps it into a lambda missing the first argument, which passes the JavaScript builtin this as the first argument to the procedure. Returns the resulting lambda.

Example:

We want to generate roughly this JavaScript:

```
var obj = {a: 10};
obj.someMethod = function() {
  return this.a + 42;
};
```

We can achieve this using the bindMethod macro:

```
let obj = JsObject{ a: 10 }
proc someMethodImpl(that: JsObject): int =
  that.a.to(int) + 42
obj.someMethod = bindMethod someMethodImpl

# Alternatively:
obj.someMethod = bindMethod
  proc(that: JsObject): int = that.a.to(int) + 42
```

### jsFromAst

[ref: #symbol-jsfromast]

**Input:**
- `n: untyped`

**Output:** `untyped`
## Proc

### `%=`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# %= #)"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# % #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `a: cstring`
- `b: cstring`

**Output:** `cstring`
**Pragmas:** `importjs: "(# + #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenation operator for JavaScript strings.

### `&gt;=`

[ref: #symbol-gt]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# >= #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&gt;`

[ref: #symbol-gt]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# > #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# <= #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# < #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `**`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "((#) ** #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*=`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# *= #)"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# * #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `++`

[ref: #symbol-]

**Input:**
- `x: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(++#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# += #)"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# + #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `--`

[ref: #symbol-]

**Input:**
- `x: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(--#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# -= #)"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# - #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/=`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# /= #)"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/`

[ref: #symbol-]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# / #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: JsRoot`
- `y: JsRoot`

**Output:** `bool`
**Pragmas:** `importjs: "(# === #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two JsObjects or JsAssocs. Be careful though, as this is comparison like in JavaScript, so if your JsObjects are in fact JavaScript Objects, and not strings or numbers, this is a *comparison of references*.

### `[]=`

[ref: #symbol-]

**Input:**
- `obj: JsObject`
- `field: cstring`
- `val: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importjs: "#[#] = #"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the value of a property of name field in a JsObject obj to v.

### `[]=`

[ref: #symbol-]

**Input:**
- `obj: JsObject`
- `field: int`
- `val: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importjs: "#[#] = #"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the value of a property of name field in a JsObject obj to v.

### `[]=`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[K, V]`
- `field: K`
- `val: V`

**Output:** *(none)*
**Generic parameters:** `K`, `V`

**Pragmas:** `importjs: "#[#] = #"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the value of a property of name field in a JsAssoc obj to v.

### `[]=`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[cstring, V]`
- `field: string`
- `val: V`

**Output:** *(none)*
**Generic parameters:** `V`

### `[]`

[ref: #symbol-]

**Input:**
- `obj: JsObject`
- `field: cstring`

**Output:** `JsObject`
**Pragmas:** `importjs: "#[#]"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the value of a property of name field from a JsObject obj.

### `[]`

[ref: #symbol-]

**Input:**
- `obj: JsObject`
- `field: int`

**Output:** `JsObject`
**Pragmas:** `importjs: "#[#]"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the value of a property of name field from a JsObject obj.

### `[]`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[K, V]`
- `field: K`

**Output:** `V`
**Generic parameters:** `K`, `V`

**Pragmas:** `importjs: "#[#]"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the value of a property of name field from a JsAssoc obj.

### `[]`

[ref: #symbol-]

**Input:**
- `obj: JsAssoc[cstring, V]`
- `field: string`

**Output:** `V`
**Generic parameters:** `V`

### `and`

[ref: #symbol-and]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# && #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `in`

[ref: #symbol-in]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# in #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(!#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: JsObject`
- `y: JsObject`

**Output:** `JsObject`
**Pragmas:** `importjs: "(# || #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hasOwnProperty

[ref: #symbol-hasownproperty]

**Input:**
- `x: JsObject`
- `prop: cstring`

**Output:** `bool`
**Pragmas:** `importjs: "#.hasOwnProperty(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks, whether x has a property of name prop.

### isNull

[ref: #symbol-isnull]

**Input:**
- `x: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `importjs: "(# === null)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if a value is exactly null.

### isUndefined

[ref: #symbol-isundefined]

**Input:**
- `x: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `importjs: "(# === undefined)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if a value is exactly undefined.

### jsDelete

[ref: #symbol-jsdelete]

**Input:**
- `x: auto`

**Output:** `JsObject`
**Generic parameters:** `x:type`

**Pragmas:** `importjs: "(delete #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

JavaScript's delete operator.

### jsNew

[ref: #symbol-jsnew]

**Input:**
- `x: auto`

**Output:** `JsObject`
**Generic parameters:** `x:type`

**Pragmas:** `importjs: "(new #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Turns a regular function call into an invocation of the JavaScript's new operator.

### jsTypeOf

[ref: #symbol-jstypeof]

**Input:**
- `x: JsObject`

**Output:** `cstring`
**Pragmas:** `importjs: "typeof(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the name of the JsObject's JavaScript type as a cstring.

### newJsAssoc

[ref: #symbol-newjsassoc]

**Input:**
- *(none)*

**Output:** `JsAssoc[K, V]`
**Generic parameters:** `K`, `V`

**Pragmas:** `importjs: "{@}"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new empty JsAssoc with key type K and value type V.

### newJsObject

[ref: #symbol-newjsobject]

**Input:**
- *(none)*

**Output:** `JsObject`
**Pragmas:** `importjs: "{@}"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new empty JsObject.

### require

[ref: #symbol-require]

**Input:**
- `module: cstring`

**Output:** `JsObject`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

JavaScript's require function.

### to

[ref: #symbol-to]

**Input:**
- `x: JsObject`
- `T: typedesc`

**Output:** `T:type`
**Generic parameters:** `T:type`

**Pragmas:** `importjs: "(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a JsObject x to type T.

### toJs

[ref: #symbol-tojs]

**Input:**
- `val: T`

**Output:** `JsObject`
**Generic parameters:** `T`

**Pragmas:** `importjs: "(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a value of any type to type JsObject.

### toJsKey

[ref: #symbol-tojskey]

**Input:**
- `text: cstring`
- `t: type T`

**Output:** `T`
**Generic parameters:** `T`, `t:type`

**Pragmas:** `importjs: "parseInt(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toJsKey

[ref: #symbol-tojskey]

**Input:**
- `text: cstring`
- `t: type T`

**Output:** `T`
**Generic parameters:** `T`, `t:type`

### toJsKey

[ref: #symbol-tojskey]

**Input:**
- `text: cstring`
- `t: type cstring`

**Output:** `cstring`
**Generic parameters:** `t:type`

### toJsKey

[ref: #symbol-tojskey]

**Input:**
- `text: cstring`
- `t: type T`

**Output:** `T`
**Generic parameters:** `T`, `t:type`

**Pragmas:** `importjs: "parseFloat(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### toJs

[ref: #symbol-tojs]

**Input:**
- `s: string`

**Output:** `JsObject`
## Type

### js

[ref: #symbol-js]

```nim
js = JsObject
```


[Next](jsffi_2.md)
