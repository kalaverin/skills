---
source_hash: 8542f545a88c4df5
source_path: lib/pure/streamwrapper.nim
---

# streamwrapper

[ref: #module-streamwrapper]

This module implements stream wrapper.

**Since** version 1.2.

## Examples

```nim
import std/[osproc, streamwrapper]
var
  p = startProcess(exePath)
  outStream = p.outputStream().newPipeOutStream()
echo outStream.peekChar
p.close()
```

## Proc

### newPipeOutStream

[ref: #symbol-newpipeoutstream]

Wrap pipe for reading with PipeOutStream so that you can use peek\* procs and generate runtime error when setPosition/getPosition is called or write operation is performed.

**Input:**
- `s: sink (ref T)`

**Output:** `owned PipeOutStream[T]`
**Generic parameters:** `T`

Wrap pipe for reading with PipeOutStream so that you can use peek\* procs and generate runtime error when setPosition/getPosition is called or write operation is performed.

Example:

```
import std/[osproc, streamwrapper]
var
  p = startProcess(exePath)
  outStream = p.outputStream().newPipeOutStream()
echo outStream.peekChar
p.close()
```

## Type

### PipeOutStream

[ref: #symbol-pipeoutstream]

```nim
PipeOutStream[T] = ref object of T
```
