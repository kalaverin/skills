---
source_hash: d5b5ba92859bf29e
source_path: lib/pure/net.nim
---

### recv

[ref: #symbol-recv]

Higher-level version of recv which returns a string.

**Input:**
- `socket: Socket`
- `size: int`
- `timeout:  = -1`
- `flags:  = {SafeDisconn}`

**Output:** `string`
**Pragmas:** `inline`, `raises: [TimeoutError, OSError, SslError]`, `tags: [ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: TimeoutError, OSError, SslError`, `tags: ReadIOEffect, TimeEffect`, `forbids: `

Higher-level version of recv which returns a string.

Reads **up to** size bytes from socket into the result.

For buffered sockets this function will attempt to read all the requested data. It will read this data in BufferSize chunks.

For unbuffered sockets this function makes no effort to read all the data requested. It will return as much data as the operating system gives it.

When "" is returned the socket's connection has been closed.

This function will throw an OSError exception when an error occurs.

A timeout may be specified in milliseconds, if enough data is not received within the time specified a TimeoutError exception will be raised.

**Warning:**
Only the SafeDisconn flag is currently supported.

### recvFrom

[ref: #symbol-recvfrom]

Receives data from socket. This function should normally be used with connection-less sockets (UDP sockets). The source address of the data packet is stored in the address argument as either a string or an IpAddress.

**Input:**
- `socket: Socket`
- `data: var string`
- `length: int`
- `address: var T`
- `port: var Port`
- `flags:  = 0'i32`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `tags: [ReadIOEffect]`

**Effects:** `tags: ReadIOEffect`

Receives data from socket. This function should normally be used with connection-less sockets (UDP sockets). The source address of the data packet is stored in the address argument as either a string or an IpAddress.

If an error occurs an OSError exception will be raised. Otherwise the return value will be the length of data received.

**Warning:**
This function does not yet have a buffered implementation, so when socket is buffered the non-buffered implementation will be used. Therefore if socket contains something in its buffer this function will make no effort to return it.

### recvLine

[ref: #symbol-recvline]

Reads a line of data from socket.

**Input:**
- `socket: Socket`
- `timeout:  = -1`
- `flags:  = {SafeDisconn}`
- `maxLength:  = MaxLineLength`

**Output:** `string`
**Pragmas:** `raises: [TimeoutError, OSError, SslError]`, `tags: [ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: TimeoutError, OSError, SslError`, `tags: ReadIOEffect, TimeEffect`, `forbids: `

Reads a line of data from socket.

If a full line is read \r\L is not added to the result, however if solely \r\L is read then the result will be set to it.

If the socket is disconnected, the result will be set to "".

An OSError exception will be raised in the case of a socket error.

A timeout can be specified in milliseconds, if data is not received within the specified time a TimeoutError exception will be raised.

The maxLength parameter determines the maximum amount of characters that can be read. The result is truncated after that.

**Warning:**
Only the SafeDisconn flag is currently supported.

### send

[ref: #symbol-send]

Sends data to a socket.

**Input:**
- `socket: Socket`
- `data: pointer`
- `size: int`

**Output:** `int`
**Pragmas:** `tags: [WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

Sends data to a socket.

**Note**: This is a low-level version of send. You likely should use the version below.

### send

[ref: #symbol-send]

**Input:**
- `socket: Socket`
- `data: string`
- `flags:  = {SafeDisconn}`
- `maxRetries:  = 100`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: [SslError, OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: SslError, OSError`, `forbids: `

Sends data to a socket. Will try to send all the data by handling interrupts and incomplete writes up to maxRetries.

### sendTo

[ref: #symbol-sendto]

This proc sends data to the specified address, which may be an IP address or a hostname, if a hostname is specified this function will try each IP of that hostname. This function should normally be used with connection-less sockets (UDP sockets).

**Input:**
- `socket: Socket`
- `address: string`
- `port: Port`
- `data: pointer`
- `size: int`
- `af: Domain = AF_INET`
- `flags:  = 0'i32`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: OSError`, `forbids: `

This proc sends data to the specified address, which may be an IP address or a hostname, if a hostname is specified this function will try each IP of that hostname. This function should normally be used with connection-less sockets (UDP sockets).

If an error occurs an OSError exception will be raised.

**Note:** You may wish to use the high-level version of this function which is defined below.

**Note:** This proc is not available for SSL sockets.

### sendTo

[ref: #symbol-sendto]

This proc sends data to the specified address, which may be an IP address or a hostname, if a hostname is specified this function will try each IP of that hostname.

**Input:**
- `socket: Socket`
- `address: string`
- `port: Port`
- `data: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: OSError`, `forbids: `

This proc sends data to the specified address, which may be an IP address or a hostname, if a hostname is specified this function will try each IP of that hostname.

Generally for use with connection-less (UDP) sockets.

If an error occurs an OSError exception will be raised.

This is the high-level version of the above sendTo function.

### sendTo

[ref: #symbol-sendto]

This proc sends data to the specified IpAddress and returns the number of bytes written.

**Input:**
- `socket: Socket`
- `address: IpAddress`
- `port: Port`
- `data: string`
- `flags:  = 0'i32`

**Output:** `int`
**Pragmas:** `discardable`, `tags: [WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: OSError`, `forbids: `

This proc sends data to the specified IpAddress and returns the number of bytes written.

Generally for use with connection-less (UDP) sockets.

If an error occurs an OSError exception will be raised.

This is the high-level version of the above sendTo function.

### serverGetPskFunc

[ref: #symbol-servergetpskfunc]

**Input:**
- `ctx: SslContext`

**Output:** `SslServerGetPskFunc`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### serverGetPskFunc=

[ref: #symbol-servergetpskfunc]

Sets function that returns PSK based on the client identity.

**Input:**
- `ctx: SslContext`
- `fun: SslServerGetPskFunc`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets function that returns PSK based on the client identity.

Only used in PSK ciphersuites.

### sessionIdContext=

[ref: #symbol-sessionidcontext]

Sets the session id context in which a session can be reused. Used for permitting clients to reuse a session id instead of doing a new handshake.

**Input:**
- `ctx: SslContext`
- `sidCtx: string`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Sets the session id context in which a session can be reused. Used for permitting clients to reuse a session id instead of doing a new handshake.

TLS clients might attempt to resume a session using the session id context, thus it must be set if verifyMode is set to CVerifyPeer or CVerifyPeerUseEnvVars, otherwise the connection will fail and SslError will be raised if resumption occurs.

* Only useful if set server-side.
* Should be unique per-application to prevent clients from malfunctioning.
* sidCtx must be at most 32 characters in length.

### setExtraData

[ref: #symbol-setextradata]

**Input:**
- `ctx: SslContext`
- `index: int`
- `data: RootRef`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Stores arbitrary data inside SslContext. The unique index should be retrieved using getSslContextExtraDataIndex.

### setSockOpt

[ref: #symbol-setsockopt]

**Input:**
- `socket: Socket`
- `opt: SOBool`
- `value: bool`
- `level:  = SOL_SOCKET`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: OSError`, `forbids: `

Sets option opt to a boolean value specified by value.

### skip

[ref: #symbol-skip]

Skips size amount of bytes.

**Input:**
- `socket: Socket`
- `size: int`
- `timeout:  = -1`

**Output:** *(none)*
**Pragmas:** `raises: [TimeoutError, OSError]`, `tags: [TimeEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: TimeoutError, OSError`, `tags: TimeEffect, ReadIOEffect`, `forbids: `

Skips size amount of bytes.

An optional timeout can be specified in milliseconds, if skipping the bytes takes longer than specified a TimeoutError exception will be raised.

Returns the number of skipped bytes.

### socketError

[ref: #symbol-socketerror]

**Input:**
- `socket: Socket`
- `err: int = -1`
- `async:  = false`
- `lastError:  = -1.OSErrorCode`
- `flags: set[SocketFlag] = {}`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `raises: [SslError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError, OSError`, `tags: `, `forbids: `

### sslHandle

[ref: #symbol-sslhandle]

**Input:**
- `self: Socket`

**Output:** `SslPtr`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieve the ssl pointer of socket. Useful for interfacing with openssl.

### toCInt

[ref: #symbol-tocint]

**Input:**
- `opt: SOBool`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a SOBool into its Socket Option cint representation.

### toOSFlags

[ref: #symbol-toosflags]

**Input:**
- `socketFlags: set[SocketFlag]`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the flags into the underlying OS representation.

### toSockAddr

[ref: #symbol-tosockaddr]

**Input:**
- `address: IpAddress`
- `port: Port`
- `sa: var Sockaddr_storage`
- `sl: var SockLen`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts IpAddress and Port to SockAddr and SockLen

### trySend

[ref: #symbol-trysend]

**Input:**
- `socket: Socket`
- `data: string`

**Output:** `bool`
**Pragmas:** `tags: [WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

Safe alternative to send. Does not raise an OSError when an error occurs, and instead returns false on failure.

### wrapConnectedSocket

[ref: #symbol-wrapconnectedsocket]

Wraps a connected socket in an SSL context. This function effectively turns socket into an SSL socket. hostname should be specified so that the client knows which hostname the server certificate should be validated against.

**Input:**
- `ctx: SslContext`
- `socket: Socket`
- `handshake: SslHandshakeType`
- `hostname: string = ""`

**Output:** *(none)*
**Pragmas:** `raises: [SslError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: SslError, Exception`, `tags: RootEffect`, `forbids: `

Wraps a connected socket in an SSL context. This function effectively turns socket into an SSL socket. hostname should be specified so that the client knows which hostname the server certificate should be validated against.

This should be called on a connected socket, and will perform an SSL handshake immediately.

FIXME: **Disclaimer**: This code is not well tested, may be very unsafe and prone to security vulnerabilities.

### wrapSocket

[ref: #symbol-wrapsocket]

Wraps a socket in an SSL context. This function effectively turns socket into an SSL socket.

**Input:**
- `ctx: SslContext`
- `socket: Socket`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Wraps a socket in an SSL context. This function effectively turns socket into an SSL socket.

This must be called on an unconnected socket; an SSL session will be started when the socket is connected.

FIXME: **Disclaimer**: This code is not well tested, may be very unsafe and prone to security vulnerabilities.

## Template

### `&amp;=`

[ref: #symbol-amp]

**Input:**
- `socket: Socket`
- `data: typed`

**Output:** *(none)*
an alias for 'send'.

## Type

### Certificate

[ref: #symbol-certificate]

```nim
Certificate = string
```

DER encoded certificate

### IpAddress

[ref: #symbol-ipaddress]

```nim
IpAddress = object
  case family*: IpAddressFamily ## the type of the IP address (IPv4 or IPv6)
  of IpAddressFamily.IPv6:
    address_v6*: array[0 .. 15, uint8] ## Contains the IP address in bytes in
                                       ## case of IPv6
  of IpAddressFamily.IPv4:
    address_v4*: array[0 .. 3, uint8] ## Contains the IP address in bytes in
                                      ## case of IPv4
```

stores an arbitrary IP address

### IpAddressFamily

[ref: #symbol-ipaddressfamily]

```nim
IpAddressFamily {.pure.} = enum
  IPv6,                     ## IPv6 address
  IPv4                       ## IPv4 address
```

Describes the type of an IP address

### ReadLineResult

[ref: #symbol-readlineresult]

```nim
ReadLineResult = enum
  ReadFullLine, ReadPartialLine, ReadDisconnected, ReadNone
```

result for readLineAsync

### SOBool

[ref: #symbol-sobool]

```nim
SOBool = enum
  OptAcceptConn, OptBroadcast, OptDebug, OptDontRoute, OptKeepAlive,
  OptOOBInline, OptReuseAddr, OptReusePort, OptNoDelay
```

Boolean socket options.

### Socket

[ref: #symbol-socket]

```nim
Socket = ref SocketImpl
```

### SocketFlag

[ref: #symbol-socketflag]

```nim
SocketFlag {.pure.} = enum
  Peek, SafeDisconn          ## Ensures disconnection exceptions (ECONNRESET, EPIPE etc) are not thrown.
```

### SocketImpl

[ref: #symbol-socketimpl]

```nim
SocketImpl = object
  when defineSsl:
```

socket type

### SslAcceptResult

[ref: #symbol-sslacceptresult]

```nim
SslAcceptResult = enum
  AcceptNoClient = 0, AcceptNoHandshake, AcceptSuccess
```

### SslClientGetPskFunc

[ref: #symbol-sslclientgetpskfunc]

```nim
SslClientGetPskFunc = proc (hint: string): tuple[identity: string, psk: string]
```

### SslContext

[ref: #symbol-sslcontext]

```nim
SslContext = ref object
  context*: SslCtx
```

### SslCVerifyMode

[ref: #symbol-sslcverifymode]

```nim
SslCVerifyMode = enum
  CVerifyNone, CVerifyPeer, CVerifyPeerUseEnvVars
```

### SslError

[ref: #symbol-sslerror]

```nim
SslError = object of CatchableError
```

### SslHandshakeType

[ref: #symbol-sslhandshaketype]

```nim
SslHandshakeType = enum
  handshakeAsClient, handshakeAsServer
```

### SslProtVersion

[ref: #symbol-sslprotversion]

```nim
SslProtVersion = enum
  protSSLv2, protSSLv3, protTLSv1, protSSLv23
```

### SslServerGetPskFunc

[ref: #symbol-sslservergetpskfunc]

```nim
SslServerGetPskFunc = proc (identity: string): string
```

### TimeoutError

[ref: #symbol-timeouterror]

```nim
TimeoutError = object of CatchableError
```

[Prev](net_1.md)
