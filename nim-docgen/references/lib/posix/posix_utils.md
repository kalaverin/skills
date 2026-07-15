---
source_hash: 33721aecce967d38
source_path: lib/posix/posix_utils.nim
---

# posix_utils

[ref: #module-posix_utils]

A set of helpers for the POSIX module. Raw interfaces are in the other posix\*.nim files.

## Examples

```nim
memoryLockAll(MCL_CURRENT or MCL_FUTURE)
```

```nim
import std/parsecfg
when defined(linux):
  let data = osReleaseFile()
  echo "OS name: ", data.getSectionValue("", "NAME") ## the data is up to each distro.
```

```nim
echo uname().nodename, uname().release, uname().version
doAssert uname().sysname.len != 0
```

## Proc

### fsync

[ref: #symbol-fsync]

**Input:**
- `fd: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

synchronize a file's buffer cache to the storage device

### memoryLock

[ref: #symbol-memorylock]

**Input:**
- `a1: pointer`
- `a2: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Locks pages starting from a1 for a1 bytes and prevent them from being swapped.

### memoryLockAll

[ref: #symbol-memorylockall]

Locks all memory for the running process to prevent swapping.

**Input:**
- `flags: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Locks all memory for the running process to prevent swapping.

example:

```
memoryLockAll(MCL_CURRENT or MCL_FUTURE)
```

### memoryUnlock

[ref: #symbol-memoryunlock]

**Input:**
- `a1: pointer`
- `a2: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Unlock pages starting from a1 for a1 bytes and allow them to be swapped.

### memoryUnlockAll

[ref: #symbol-memoryunlockall]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Unlocks all memory for the running process to allow swapping.

### mkdtemp

[ref: #symbol-mkdtemp]

**Input:**
- `prefix: string`

**Output:** `string`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a unique temporary directory from a prefix string. Adds a six chars suffix. The directory is created with permissions 0700. Returns the directory name.

### mkstemp

[ref: #symbol-mkstemp]

**Input:**
- `prefix: string`
- `suffix:  = ""`

**Output:** `(string, File)`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a unique temporary file from a prefix string. A six-character string will be added. If suffix is provided it will be added to the string The file is created with perms 0600. Returns the filename and a file opened in r/w mode.

### osReleaseFile

[ref: #symbol-osreleasefile]

Gets system identification from os-release file and returns it as a parsecfg.Config. You also need to import the parsecfg module to gain access to this object. The os-release file is an official Freedesktop.org open standard. Available in Linux and BSD distributions, except Android and Android-based Linux. os-release file is not available on Windows and OS X by design.

**Input:**
- *(none)*

**Output:** `Config`
**Pragmas:** `raises: [IOError, OSError, ValueError, KeyError]`, `tags: [ReadDirEffect, ReadIOEffect, WriteIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, KeyError`, `tags: ReadDirEffect, ReadIOEffect, WriteIOEffect, RootEffect`, `forbids: `

Gets system identification from os-release file and returns it as a parsecfg.Config. You also need to import the parsecfg module to gain access to this object. The os-release file is an official Freedesktop.org open standard. Available in Linux and BSD distributions, except Android and Android-based Linux. os-release file is not available on Windows and OS X by design.

* <https://www.freedesktop.org/software/systemd/man/os-release.html>

### sendSignal

[ref: #symbol-sendsignal]

**Input:**
- `pid: Pid`
- `signal: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Sends a signal to a running process by calling kill. Raise exception in case of failure e.g. process not running.

### stat

[ref: #symbol-stat]

**Input:**
- `path: string`

**Output:** `Stat`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns file status in a Stat structure

### uname

[ref: #symbol-uname]

**Input:**
- *(none)*

**Output:** `Uname`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Provides system information in a Uname struct with sysname, nodename, release, version and machine attributes.

## Type

### Uname

[ref: #symbol-uname]

```nim
Uname = object
  sysname*, nodename*, release*, version*, machine*: string
```
