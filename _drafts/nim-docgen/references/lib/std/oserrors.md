---
source_hash: acfbedac72cb0c0f
source_path: lib/std/oserrors.nim
---

# oserrors

[ref: #module-oserrors]

The std/oserrors module implements OS error reporting.

## Examples

```nim
when defined(linux):
  assert osErrorMsg(OSErrorCode(0)) == ""
  assert osErrorMsg(OSErrorCode(1)) == "Operation not permitted"
  assert osErrorMsg(OSErrorCode(2)) == "No such file or directory"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `err: OSErrorCode`

**Output:** `string`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `err1: OSErrorCode`
- `err2: OSErrorCode`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newOSError

[ref: #symbol-newoserror]

Creates a new [OSError exception](system.html#OSError).

**Input:**
- `errorCode: OSErrorCode`
- `additionalInfo:  = ""`

**Output:** `owned(ref OSError)`
**Pragmas:** `noinline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new [OSError exception](system.html#OSError).

The errorCode will determine the message, [osErrorMsg](#osErrorMsg) will be used to get this message.

The error code can be retrieved using the [osLastError](#osLastError).

If the error code is 0 or an error message could not be retrieved, the message unknown OS error will be used.

See also:

* [osErrorMsg](#osErrorMsg)
* [osLastError](#osLastError)

### osErrorMsg

[ref: #symbol-oserrormsg]

Converts an OS error code into a human readable string.

**Input:**
- `errorCode: OSErrorCode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an OS error code into a human readable string.

The error code can be retrieved using the [osLastError](#osLastError).

If conversion fails, or errorCode is 0 then "" will be returned.

See also:

* [raiseOSError](#raiseOSError)
* [osLastError](#osLastError)

### osLastError

[ref: #symbol-oslasterror]

Retrieves the last operating system error code.

**Input:**
- *(none)*

**Output:** `OSErrorCode`
**Pragmas:** `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the last operating system error code.

This procedure is useful in the event when an OS call fails. In that case this procedure will return the error code describing the reason why the OS call failed. The OSErrorMsg procedure can then be used to convert this code into a string.

**Warning:**
The behaviour of this procedure varies between Windows and POSIX systems. On Windows some OS calls can reset the error code to 0 causing this procedure to return 0. It is therefore advised to call this procedure immediately after an OS call fails. On POSIX systems this is not a problem.

See also:

* [osErrorMsg](#osErrorMsg)
* [raiseOSError](#raiseOSError)

### raiseOSError

[ref: #symbol-raiseoserror]

Raises an [OSError exception](system.html#OSError).

**Input:**
- `errorCode: OSErrorCode`
- `additionalInfo:  = ""`

**Output:** *(none)*
**Pragmas:** `noinline`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Raises an [OSError exception](system.html#OSError).

Read the description of the [newOSError](#newOSError) to learn how the exception object is created.

## Type

### OSErrorCode

[ref: #symbol-oserrorcode]

```nim
OSErrorCode = distinct int32
```

Specifies an OS Error Code.
