---
source_hash: e4e878e2859d0df3
source_path: lib/posix/linux.nim
---

# linux

[ref: #module-linux]

Flags of clone syscall. See [clone syscall manual](https://man7.org/linux/man-pages/man2/clone.2.html) for more information.

## Const

### CLONE_CHILD_CLEARTID

[ref: #symbol-clone-child-cleartid]

```nim
CLONE_CHILD_CLEARTID = 0x00200000'i32
```

### CLONE_CHILD_SETTID

[ref: #symbol-clone-child-settid]

```nim
CLONE_CHILD_SETTID = 0x01000000'i32
```

### CLONE_DETACHED

[ref: #symbol-clone-detached]

```nim
CLONE_DETACHED = 0x00400000'i32
```

### CLONE_FILES

[ref: #symbol-clone-files]

```nim
CLONE_FILES = 0x00000400'i32
```

### CLONE_FS

[ref: #symbol-clone-fs]

```nim
CLONE_FS = 0x00000200'i32
```

### CLONE_IO

[ref: #symbol-clone-io]

```nim
CLONE_IO = 0x80000000'i32
```

### CLONE_NEWCGROUP

[ref: #symbol-clone-newcgroup]

```nim
CLONE_NEWCGROUP = 0x02000000'i32
```

### CLONE_NEWIPC

[ref: #symbol-clone-newipc]

```nim
CLONE_NEWIPC = 0x08000000'i32
```

### CLONE_NEWNET

[ref: #symbol-clone-newnet]

```nim
CLONE_NEWNET = 0x40000000'i32
```

### CLONE_NEWNS

[ref: #symbol-clone-newns]

```nim
CLONE_NEWNS = 0x00020000'i32
```

### CLONE_NEWPID

[ref: #symbol-clone-newpid]

```nim
CLONE_NEWPID = 0x20000000'i32
```

### CLONE_NEWUSER

[ref: #symbol-clone-newuser]

```nim
CLONE_NEWUSER = 0x10000000'i32
```

### CLONE_NEWUTS

[ref: #symbol-clone-newuts]

```nim
CLONE_NEWUTS = 0x04000000'i32
```

### CLONE_PARENT

[ref: #symbol-clone-parent]

```nim
CLONE_PARENT = 0x00008000'i32
```

### CLONE_PARENT_SETTID

[ref: #symbol-clone-parent-settid]

```nim
CLONE_PARENT_SETTID = 0x00100000'i32
```

### CLONE_PIDFD

[ref: #symbol-clone-pidfd]

```nim
CLONE_PIDFD = 0x00001000'i32
```

### CLONE_PTRACE

[ref: #symbol-clone-ptrace]

```nim
CLONE_PTRACE = 0x00002000'i32
```

### CLONE_SETTLS

[ref: #symbol-clone-settls]

```nim
CLONE_SETTLS = 0x00080000'i32
```

### CLONE_SIGHAND

[ref: #symbol-clone-sighand]

```nim
CLONE_SIGHAND = 0x00000800'i32
```

### CLONE_SYSVSEM

[ref: #symbol-clone-sysvsem]

```nim
CLONE_SYSVSEM = 0x00040000'i32
```

### CLONE_THREAD

[ref: #symbol-clone-thread]

```nim
CLONE_THREAD = 0x00010000'i32
```

### CLONE_UNTRACED

[ref: #symbol-clone-untraced]

```nim
CLONE_UNTRACED = 0x00800000'i32
```

### CLONE_VFORK

[ref: #symbol-clone-vfork]

```nim
CLONE_VFORK = 0x00004000'i32
```

### CLONE_VM

[ref: #symbol-clone-vm]

```nim
CLONE_VM = 0x00000100'i32
```

### CSIGNAL

[ref: #symbol-csignal]

```nim
CSIGNAL = 0x000000FF'i32
```

## Proc

### clone

[ref: #symbol-clone]

**Input:**
- `fn: pointer`
- `child_stack: pointer`
- `flags: cint`
- `arg: pointer`
- `ptid: ptr Pid`
- `tls: pointer`
- `ctid: ptr Pid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pipe2

[ref: #symbol-pipe2]

**Input:**
- `a: array[0 .. 1, cint]`
- `flags: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
