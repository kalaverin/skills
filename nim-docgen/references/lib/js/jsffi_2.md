---
source_hash: 0d7ceb967b1553c5
source_path: lib/js/jsffi.nim
---

### JsAssoc

[ref: #symbol-jsassoc]

```nim
JsAssoc[K; V] = ref object of JsRoot
```

Statically typed wrapper around a JavaScript object.

### JsError

[ref: #symbol-jserror]

```nim
JsError {.importc: "Error".} = object of JsRoot
  message*: cstring
```

### JsEvalError

[ref: #symbol-jsevalerror]

```nim
JsEvalError {.importc: "EvalError".} = object of JsError
```

### JsKey

[ref: #symbol-jskey]

```nim
JsKey = concept atypeof(T)
    cstring.toJsKey(T) is T
```

### JsObject

[ref: #symbol-jsobject]

```nim
JsObject = ref object of JsRoot
```

Dynamically typed wrapper around a JavaScript object.

### JsRangeError

[ref: #symbol-jsrangeerror]

```nim
JsRangeError {.importc: "RangeError".} = object of JsError
```

### JsReferenceError

[ref: #symbol-jsreferenceerror]

```nim
JsReferenceError {.importc: "ReferenceError".} = object of JsError
```

### JsSyntaxError

[ref: #symbol-jssyntaxerror]

```nim
JsSyntaxError {.importc: "SyntaxError".} = object of JsError
```

### JsTypeError

[ref: #symbol-jstypeerror]

```nim
JsTypeError {.importc: "TypeError".} = object of JsError
```

### JsURIError

[ref: #symbol-jsurierror]

```nim
JsURIError {.importc: "URIError".} = object of JsError
```

## Var

### jsArguments

[ref: #symbol-jsarguments]

```nim
jsArguments {.importc: "arguments", nodecl.}: JsObject
```

JavaScript's arguments pseudo-variable.

### jsDirname

[ref: #symbol-jsdirname]

```nim
jsDirname {.importc: "__dirname", nodecl.}: cstring
```

JavaScript's \_\_dirname pseudo-variable.

### jsFilename

[ref: #symbol-jsfilename]

```nim
jsFilename {.importc: "__filename", nodecl.}: cstring
```

JavaScript's \_\_filename pseudo-variable.

### jsNull

[ref: #symbol-jsnull]

```nim
jsNull {.importc: "null", nodecl.}: JsObject
```

JavaScript's null literal.

### jsUndefined

[ref: #symbol-jsundefined]

```nim
jsUndefined {.importc: "undefined", nodecl.}: JsObject
```

JavaScript's undefined literal.

[Prev](jsffi_1.md)
