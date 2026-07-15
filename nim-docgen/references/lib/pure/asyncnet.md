---
source_hash: f654ddf53f3dfe1b
source_path: lib/pure/asyncnet.nim
---

# asyncnet

[ref: #module-asyncnet]

This module implements a high-level asynchronous sockets API based on the asynchronous dispatcher defined in the asyncdispatch module.

# [Asynchronous IO in Nim](#asynchronous-io-in-nim)

Async IO in Nim consists of multiple layers (from highest to lowest):

* asyncnet module
* Async await
* asyncdispatch module (event loop)
* selectors module

Each builds on top of the layers below it. The selectors module is an abstraction for the various system select() mechanisms such as epoll or kqueue. If you wish you can use it directly, and some people have done so [successfully](https://goran.krampe.se/2014/10/25/nim-socketserver/). But you must be aware that on Windows it only supports select().

The async dispatcher implements the proactor pattern and also has an implementation of IOCP. It implements the proactor pattern for other OS' via the selectors module. Futures are also implemented here, and indeed all the procedures return a future.

The final layer is the async await transformation. This allows you to write asynchronous code in a synchronous style and works similar to C#'s await. The transformation works by converting any async procedures into an iterator.

This is all single threaded, fully non-blocking and does give you a lot of control. In theory you should be able to work with any of these layers interchangeably (as long as you only care about non-Windows platforms).

For most applications using asyncnet is the way to go as it builds over all the layers, providing some extra features such as buffering.

# [SSL](#ssl)

SSL can be enabled by compiling with the -d:ssl flag.

You must create a new SSL context with the newContext function defined in the net module. You may then call wrapSocket on your socket using the newly created SSL context to get an SSL socket.

# [Examples](#examples)

## [Chat server](#examples-chat-server)

The following example demonstrates a simple chat server.

```
import std/[asyncnet, asyncdispatch]

var clients {.threadvar.}: seq[AsyncSocket]

proc processClient(client: AsyncSocket) {.async.} =
  while true:
    let line = await client.recvLine()
    if line.len == 0: break
    for c in clients:
      await c.send(line & "\c\L")

proc serve() {.async.} =
  clients = @[]
  var server = newAsyncSocket()
  server.setSockOpt(OptReuseAddr, true)
  server.bindAddr(Port(12345))
  server.listen()
  
  while true:
    let client = await server.accept()
    clients.add client
    
    asyncCheck processClient(client)

asyncCheck serve()
runForever()
```

## Examples

```nim
import std/[asyncnet, asyncdispatch]

var clients {.threadvar.}: seq[AsyncSocket]

proc processClient(client: AsyncSocket) {.async.} =
  while true:
    let line = await client.recvLine()
    if line.len == 0: break
    for c in clients:
      await c.send(line & "\c\L")

proc serve() {.async.} =
  clients = @[]
  var server = newAsyncSocket()
  server.setSockOpt(OptReuseAddr, true)
  server.bindAddr(Port(12345))
  server.listen()
  
  while true:
    let client = await server.accept()
    clients.add client
    
    asyncCheck processClient(client)

asyncCheck serve()
runForever()
```

## Proc

### accept

[ref: #symbol-accept]

**Input:**
- `socket: AsyncSocket`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[AsyncSocket])`
**Pragmas:** `raises: [ValueError, OSError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError, Exception`, `tags: RootEffect`, `forbids: `

Accepts a new connection. Returns a future containing the client socket corresponding to that connection. If inheritable is false (the default), the resulting client socket will not be inheritable by child processes. The future will complete when the connection is successfully accepted.

### acceptAddr

[ref: #symbol-acceptaddr]

Accepts a new connection. Returns a future containing the client socket corresponding to that connection and the remote address of the client.

**Input:**
- `socket: AsyncSocket`
- `flags:  = {SafeDisconn}`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(Future[tuple[address: string, client: AsyncSocket]])`
**Pragmas:** `raises: [ValueError, OSError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError, Exception`, `tags: RootEffect`, `forbids: `

Accepts a new connection. Returns a future containing the client socket corresponding to that connection and the remote address of the client.

If inheritable is false (the default), the resulting client socket will not be inheritable by child processes.

The future will complete when the connection is successfully accepted.

### bindAddr

[ref: #symbol-bindaddr]

Binds address:port to the socket.

**Input:**
- `socket: AsyncSocket`
- `port:  = Port(0)`
- `address:  = ""`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [ValueError, OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: ValueError, OSError`, `forbids: `

Binds address:port to the socket.

If address is "" then ADDR\_ANY will be bound.

### bindUnix

[ref: #symbol-bindunix]

**Input:**
- `socket: AsyncSocket`
- `path: string`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Binds Unix socket to path. This only works on Unix-style systems: Mac OS X, BSD and Linux

### close

[ref: #symbol-close]

**Input:**
- `socket: AsyncSocket`

**Output:** *(none)*
**Pragmas:** `raises: [LibraryError, Exception, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception, SslError`, `tags: RootEffect`, `forbids: `

Closes the socket.

### connect

[ref: #symbol-connect]

Connects socket to server at address:port.

**Input:**
- `socket: AsyncSocket`
- `address: string`
- `port: Port`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, OSError, IOError, ValueError, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, OSError, IOError, ValueError, SslError`, `tags: RootEffect`, `forbids: `

Connects socket to server at address:port.

Returns a Future which will complete when the connection succeeds or an error occurs.

### connectUnix

[ref: #symbol-connectunix]

**Input:**
- `socket: AsyncSocket`
- `path: string`

**Output:** `owned(Future[void])`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binds Unix socket to path. This only works on Unix-style systems: Mac OS X, BSD and Linux

### dial

[ref: #symbol-dial]

**Input:**
- `address: string`
- `port: Port`
- `protocol:  = IPPROTO_TCP`
- `buffered:  = true`

**Output:** `owned(Future[AsyncSocket])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError, OSError, IOError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, OSError, IOError`, `tags: RootEffect`, `forbids: `

Establishes connection to the specified address:port pair via the specified protocol. The procedure iterates through possible resolutions of the address until it succeeds, meaning that it seamlessly works with both IPv4 and IPv6. Returns AsyncSocket ready to send or receive data.

### getFd

[ref: #symbol-getfd]

**Input:**
- `socket: AsyncSocket`

**Output:** `SocketHandle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the socket's file descriptor.

### getLocalAddr

[ref: #symbol-getlocaladdr]

Get the socket's local address and port number.

**Input:**
- `socket: AsyncSocket`

**Output:** `(string, Port)`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Get the socket's local address and port number.

This is high-level interface for getsockname.

### getPeerAddr

[ref: #symbol-getpeeraddr]

Get the socket's peer address and port number.

**Input:**
- `socket: AsyncSocket`

**Output:** `(string, Port)`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Get the socket's peer address and port number.

This is high-level interface for getpeername.

### getPeerCertificates

[ref: #symbol-getpeercertificates]

**Input:**
- `socket: AsyncSocket`

**Output:** `seq[Certificate]`
**Pragmas:** `raises: [Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception`, `tags: `, `forbids: `

Returns the certificate chain received by the peer we are connected to through the given socket. The handshake must have been completed and the certificate chain must have been verified successfully or else an empty sequence is returned. The chain is ordered from leaf certificate to root certificate.

### getSockOpt

[ref: #symbol-getsockopt]

**Input:**
- `socket: AsyncSocket`
- `opt: SOBool`
- `level:  = SOL_SOCKET`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Retrieves option opt as a boolean value.

### hasDataBuffered

[ref: #symbol-hasdatabuffered]

**Input:**
- `s: AsyncSocket`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether an AsyncSocket has data buffered.

### isClosed

[ref: #symbol-isclosed]

**Input:**
- `socket: AsyncSocket`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether the socket has been closed.

### isSsl

[ref: #symbol-isssl]

**Input:**
- `socket: AsyncSocket`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether socket is a SSL socket.

### listen

[ref: #symbol-listen]

Marks socket as accepting connections. Backlog specifies the maximum length of the queue of pending connections.

**Input:**
- `socket: AsyncSocket`
- `backlog:  = SOMAXCONN`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Marks socket as accepting connections. Backlog specifies the maximum length of the queue of pending connections.

Raises an OSError error upon failure.

### newAsyncSocket

[ref: #symbol-newasyncsocket]

Creates a new AsyncSocket based on the supplied params.

**Input:**
- `fd: AsyncFD`
- `domain: Domain = AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`
- `buffered:  = true`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(AsyncSocket)`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a new AsyncSocket based on the supplied params.

The supplied fd's non-blocking state will be enabled implicitly.

If inheritable is false (the default), the supplied fd will not be inheritable by child processes.

**Note**: This procedure will **NOT** register fd with the global async dispatcher. You need to do this manually. If you have used newAsyncNativeSocket to create fd then it's already registered.

### newAsyncSocket

[ref: #symbol-newasyncsocket]

Creates a new asynchronous socket.

**Input:**
- `domain: Domain = AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`
- `buffered:  = true`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(AsyncSocket)`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a new asynchronous socket.

This procedure will also create a brand new file descriptor for this socket.

If inheritable is false (the default), the new file descriptor will not be inheritable by child processes.

### newAsyncSocket

[ref: #symbol-newasyncsocket]

Creates a new asynchronous socket.

**Input:**
- `domain: cint`
- `sockType: cint`
- `protocol: cint`
- `buffered:  = true`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(AsyncSocket)`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a new asynchronous socket.

This procedure will also create a brand new file descriptor for this socket.

If inheritable is false (the default), the new file descriptor will not be inheritable by child processes.

### recv

[ref: #symbol-recv]

Reads **up to** size bytes from socket.

**Input:**
- `socket: AsyncSocket`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[string])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, SslError`, `tags: RootEffect`, `forbids: `

Reads **up to** size bytes from socket.

For buffered sockets this function will attempt to read all the requested data. It will read this data in BufferSize chunks.

For unbuffered sockets this function makes no effort to read all the data requested. It will return as much data as the operating system gives it.

If socket is disconnected during the recv operation then the future may complete with only a part of the requested data.

If socket is disconnected and no data is available to be read then the future will complete with a value of "".

### recvFrom

[ref: #symbol-recvfrom]

Receives a datagram data from socket into data, which must be at least of size size. The address and port of datagram's sender will be stored into address and port, respectively. Returned future will complete once one datagram has been received, and will return size of packet received.

**Input:**
- `socket: AsyncSocket`
- `data: FutureVar[string]`
- `size: int`
- `address: FutureVar[string]`
- `port: FutureVar[Port]`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[int])`
**Pragmas:** `stackTrace: false`, `raises: [ValueError, Exception, OSError, IOError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception, OSError, IOError`, `tags: RootEffect`, `forbids: `

Receives a datagram data from socket into data, which must be at least of size size. The address and port of datagram's sender will be stored into address and port, respectively. Returned future will complete once one datagram has been received, and will return size of packet received.

If an error occurs an OSError exception will be raised.

This proc is normally used with connectionless sockets (UDP sockets).

**Notes**

* data must be initialized to the length of size.
* address must be initialized to 46 in length.

### recvFrom

[ref: #symbol-recvfrom]

Receives a datagram data from socket, which must be at least of size size. Returned future will complete once one datagram has been received and will return tuple with: data of packet received; and address and port of datagram's sender.

**Input:**
- `socket: AsyncSocket`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[tuple[data: string, address: string, port: Port]])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError, OSError, IOError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, OSError, IOError`, `tags: RootEffect`, `forbids: `

Receives a datagram data from socket, which must be at least of size size. Returned future will complete once one datagram has been received and will return tuple with: data of packet received; and address and port of datagram's sender.

If an error occurs an OSError exception will be raised.

This proc is normally used with connectionless sockets (UDP sockets).

### recvInto

[ref: #symbol-recvinto]

Reads **up to** size bytes from socket into buf.

**Input:**
- `socket: AsyncSocket`
- `buf: pointer`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[int])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, SslError`, `tags: RootEffect`, `forbids: `

Reads **up to** size bytes from socket into buf.

For buffered sockets this function will attempt to read all the requested data. It will read this data in BufferSize chunks.

For unbuffered sockets this function makes no effort to read all the data requested. It will return as much data as the operating system gives it.

If socket is disconnected during the recv operation then the future may complete with only a part of the requested data.

If socket is disconnected and no data is available to be read then the future will complete with a value of 0.

### recvLine

[ref: #symbol-recvline]

Reads a line of data from socket. Returned future will complete once a full line is read or an error occurs.

**Input:**
- `socket: AsyncSocket`
- `flags:  = {SafeDisconn}`
- `maxLength:  = MaxLineLength`

**Output:** `owned(Future[string])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, SslError`, `tags: RootEffect`, `forbids: `

Reads a line of data from socket. Returned future will complete once a full line is read or an error occurs.

If a full line is read \r\L is not added to line, however if solely \r\L is read then line will be set to it.

If the socket is disconnected, line will be set to "".

If the socket is disconnected in the middle of a line (before \r\L is read) then line will be set to "". The partial line **will be lost**.

The maxLength parameter determines the maximum amount of characters that can be read. The result is truncated after that.

**Warning:**
The Peek flag is not yet implemented.

**Warning:**
recvLine on unbuffered sockets assumes that the protocol uses \r\L to delimit a new line.

### recvLineInto

[ref: #symbol-recvlineinto]

Reads a line of data from socket into resString.

**Input:**
- `socket: AsyncSocket`
- `resString: FutureVar[string]`
- `flags:  = {SafeDisconn}`
- `maxLength:  = MaxLineLength`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [ValueError, Exception, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception, SslError`, `tags: RootEffect`, `forbids: `

Reads a line of data from socket into resString.

If a full line is read \r\L is not added to line, however if solely \r\L is read then line will be set to it.

If the socket is disconnected, line will be set to "".

If the socket is disconnected in the middle of a line (before \r\L is read) then line will be set to "". The partial line **will be lost**.

The maxLength parameter determines the maximum amount of characters that can be read. resString will be truncated after that.

**Warning:**
The Peek flag is not yet implemented.

**Warning:**
recvLineInto on unbuffered sockets assumes that the protocol uses \r\L to delimit a new line.

### send

[ref: #symbol-send]

**Input:**
- `socket: AsyncSocket`
- `buf: pointer`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, SslError, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, SslError, ValueError`, `tags: RootEffect`, `forbids: `

Sends size bytes from buf to socket. The returned future will complete once all data has been sent.

### send

[ref: #symbol-send]

**Input:**
- `socket: AsyncSocket`
- `data: string`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, SslError, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, SslError, ValueError`, `tags: RootEffect`, `forbids: `

Sends data to socket. The returned future will complete once all data has been sent.

### sendTo

[ref: #symbol-sendto]

This proc sends data to the specified address, which may be an IP address or a hostname. If a hostname is specified this function will try each IP of that hostname. The returned future will complete once all data has been sent.

**Input:**
- `socket: AsyncSocket`
- `address: string`
- `port: Port`
- `data: string`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, OSError, ValueError, IOError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, OSError, ValueError, IOError`, `tags: RootEffect`, `forbids: `

This proc sends data to the specified address, which may be an IP address or a hostname. If a hostname is specified this function will try each IP of that hostname. The returned future will complete once all data has been sent.

If an error occurs an OSError exception will be raised.

This proc is normally used with connectionless sockets (UDP sockets).

### setSockOpt

[ref: #symbol-setsockopt]

**Input:**
- `socket: AsyncSocket`
- `opt: SOBool`
- `value: bool`
- `level:  = SOL_SOCKET`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: OSError`, `forbids: `

Sets option opt to a boolean value specified by value.

### sslHandle

[ref: #symbol-sslhandle]

**Input:**
- `self: AsyncSocket`

**Output:** `SslPtr`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieve the ssl pointer of socket. Useful for interfacing with openssl.

### wrapConnectedSocket

[ref: #symbol-wrapconnectedsocket]

Wraps a connected socket in an SSL context. This function effectively turns socket into an SSL socket. hostname should be specified so that the client knows which hostname the server certificate should be validated against.

**Input:**
- `ctx: SslContext`
- `socket: AsyncSocket`
- `handshake: SslHandshakeType`
- `hostname: string = ""`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Wraps a connected socket in an SSL context. This function effectively turns socket into an SSL socket. hostname should be specified so that the client knows which hostname the server certificate should be validated against.

This should be called on a connected socket, and will perform an SSL handshake immediately.

**Disclaimer**: This code is not well tested, may be very unsafe and prone to security vulnerabilities.

### wrapSocket

[ref: #symbol-wrapsocket]

Wraps a socket in an SSL context. This function effectively turns socket into an SSL socket.

**Input:**
- `ctx: SslContext`
- `socket: AsyncSocket`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Wraps a socket in an SSL context. This function effectively turns socket into an SSL socket.

**Disclaimer**: This code is not well tested, may be very unsafe and prone to security vulnerabilities.

## Type

### AsyncSocket

[ref: #symbol-asyncsocket]

```nim
AsyncSocket = ref AsyncSocketDesc
```
