---
source_hash: 471e16e8d89073d0
source_path: lib/std/socketstreams.nim
---

# socketstreams

[ref: #module-socketstreams]

This module provides an implementation of the streams interface for sockets. It contains two separate implementations, a [ReadSocketStream](#ReadSocketStream) and a [WriteSocketStream](#WriteSocketStream).

The ReadSocketStream only supports reading, peeking, and seeking. It reads into a buffer, so even by seeking backwards it will only read the same position a single time from the underlying socket. To clear the buffer and free the data read into it you can call resetStream, this will also reset the position back to 0 but won't do anything to the underlying socket.

The WriteSocketStream allows both reading and writing, but it performs the reads on the internal buffer. So by writing to the buffer you can then read back what was written but without receiving anything from the socket. You can also set the position and overwrite parts of the buffer, and to send anything over the socket you need to call flush at which point you can't write anything to the buffer before the point of the flush (but it can still be read). Again to empty the underlying buffer you need to call resetStream.

# [Examples](#examples)

```
import std/socketstreams

var
  socket = newSocket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
  stream = newReadSocketStream(socket)
socket.sendTo("127.0.0.1", Port(12345), "SOME REQUEST")
echo stream.readLine() # Will call `recv`
stream.setPosition(0)
echo stream.readLine() # Will return the read line from the buffer
stream.resetStream() # Buffer is now empty, position is 0
echo stream.readLine() # Will call `recv` again
stream.close() # Closes the socket
```

```
import std/socketstreams

var socket = newSocket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
socket.connect("127.0.0.1", Port(12345))
var sendStream = newWriteSocketStream(socket)
sendStream.write "NOM"
sendStream.setPosition(1)
echo sendStream.peekStr(2) # OM
sendStream.write "I"
sendStream.setPosition(0)
echo sendStream.readStr(3) # NIM
echo sendStream.getPosition() # 3
sendStream.flush() # This actually performs the writing to the socket
sendStream.setPosition(1)
sendStream.write "I" # Throws an error as we can't write into an already sent buffer
```

## Examples

```nim
import std/socketstreams

var
  socket = newSocket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
  stream = newReadSocketStream(socket)
socket.sendTo("127.0.0.1", Port(12345), "SOME REQUEST")
echo stream.readLine() # Will call `recv`
stream.setPosition(0)
echo stream.readLine() # Will return the read line from the buffer
stream.resetStream() # Buffer is now empty, position is 0
echo stream.readLine() # Will call `recv` again
stream.close() # Closes the socket
```

```nim
import std/socketstreams

var socket = newSocket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
socket.connect("127.0.0.1", Port(12345))
var sendStream = newWriteSocketStream(socket)
sendStream.write "NOM"
sendStream.setPosition(1)
echo sendStream.peekStr(2) # OM
sendStream.write "I"
sendStream.setPosition(0)
echo sendStream.readStr(3) # NIM
echo sendStream.getPosition() # 3
sendStream.flush() # This actually performs the writing to the socket
sendStream.setPosition(1)
sendStream.write "I" # Throws an error as we can't write into an already sent buffer
```

## Proc

### newReadSocketStream

[ref: #symbol-newreadsocketstream]

**Input:**
- `s: Socket`

**Output:** `owned ReadSocketStream`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newWriteSocketStream

[ref: #symbol-newwritesocketstream]

**Input:**
- `s: Socket`

**Output:** `owned WriteSocketStream`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### resetStream

[ref: #symbol-resetstream]

**Input:**
- `s: ReadSocketStream`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### resetStream

[ref: #symbol-resetstream]

**Input:**
- `s: WriteSocketStream`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### ReadSocketStream

[ref: #symbol-readsocketstream]

```nim
ReadSocketStream = ref ReadSocketStreamObj
```

### ReadSocketStreamObj

[ref: #symbol-readsocketstreamobj]

```nim
ReadSocketStreamObj = object of StreamObj
```

### WriteSocketStream

[ref: #symbol-writesocketstream]

```nim
WriteSocketStream = ref WriteSocketStreamObj
```

### WriteSocketStreamObj

[ref: #symbol-writesocketstreamobj]

```nim
WriteSocketStreamObj = object of ReadSocketStreamObj
```
