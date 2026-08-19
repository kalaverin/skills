---
source_hash: d5b5ba92859bf29e
source_path: lib/pure/net.nim
---

# net

[ref: #module-net]

This module implements a high-level cross-platform sockets interface. The procedures implemented in this module are primarily for blocking sockets. For asynchronous non-blocking sockets use the asyncnet module together with the asyncdispatch module.

The first thing you will always need to do in order to start using sockets, is to create a new instance of the Socket type using the newSocket procedure.

# [SSL](#ssl)

In order to use the SSL procedures defined in this module, you will need to compile your application with the -d:ssl flag. See the [newContext](net.html#newContext%2Cstring%2Cstring%2Cstring%2Cstring) procedure for additional details.

# [SSL on Windows](#ssl-on-windows)

On Windows the SSL library checks for valid certificates. It uses the cacert.pem file for this purpose which was extracted from https://curl.se/ca/cacert.pem. Besides the OpenSSL DLLs (e.g. libssl-1\_1-x64.dll, libcrypto-1\_1-x64.dll) you also need to ship cacert.pem with your .exe file.

# [Examples](#examples)

## [Connecting to a server](#examples-connecting-to-a-server)

After you create a socket with the newSocket procedure, you can easily connect it to a server running at a known hostname (or IP address) and port. To do so over TCP, use the example below.

For SSL, use the following example:UDP is a connectionless protocol, so UDP sockets don't have to explicitly call the [connect](net.html#connect%2CSocket%2Cstring) procedure. They can simply start sending data immediately.

## [Creating a server](#examples-creating-a-server)

After you create a socket with the newSocket procedure, you can create a TCP server by calling the bindAddr and listen procedures.

## Examples

```nim
import std/net
let socket = newSocket()
socket.connect("google.com", Port(80))
```

```nim
import std/net
let socket = newSocket()
let ctx = newContext()
wrapSocket(ctx, socket)
socket.connect("google.com", Port(443))
```

```nim
import std/net
let socket = newSocket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
socket.sendTo("192.168.0.1", Port(27960), "status\n")
```

```nim
import std/net
let socket = newSocket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
let ip = parseIpAddress("192.168.0.1")
doAssert socket.sendTo(ip, Port(27960), "status\c\l") == 8
```

```nim
import std/net
let socket = newSocket()
socket.bindAddr(Port(1234))
socket.listen()

# You can then begin accepting connections using the `accept` procedure.
var client: Socket
var address = ""
while true:
  socket.acceptAddr(client, address)
  echo "Client connected from: ", address
```

```nim
echo getPrimaryIPAddr() # "192.168.1.2"
```

```nim
let socket = newSocket()
socket.setSockOpt(OptReusePort, true)
socket.setSockOpt(OptNoDelay, true, level = IPPROTO_TCP.cint)
```

## Const

### BufferSize

[ref: #symbol-buffersize]

```nim
BufferSize: int = 4000
```

size of a buffered socket's buffer

### MaxLineLength

[ref: #symbol-maxlinelength]

```nim
MaxLineLength = 1000000
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `address: IpAddress`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an IpAddress into the textual representation

### `==`

[ref: #symbol-]

**Input:**
- `lhs: IpAddress`
- `rhs: IpAddress`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two IpAddresses for Equality. Returns true if the addresses are equal

### accept

[ref: #symbol-accept]

Equivalent to acceptAddr but doesn't return the address, only the socket.

**Input:**
- `server: Socket`
- `client: var owned(Socket)`
- `flags:  = {SafeDisconn}`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError, IOError, SslError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError, IOError, SslError`, `forbids: `

Equivalent to acceptAddr but doesn't return the address, only the socket.

The SocketHandle associated with the resulting client will not be inheritable by child processes by default. This can be changed via the inheritable parameter.

The accept call may result in an error if the connecting socket disconnects during the duration of the accept. If the SafeDisconn flag is specified then this error will not be raised and instead accept will be called again.

### acceptAddr

[ref: #symbol-acceptaddr]

Blocks until a connection is being made from a client. When a connection is made sets client to the client socket and address to the address of the connecting client. This function will raise OSError if an error occurs.

**Input:**
- `server: Socket`
- `client: var owned(Socket)`
- `address: var string`
- `flags:  = {SafeDisconn}`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [OSError, IOError, SslError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError, IOError, SslError`, `forbids: `

Blocks until a connection is being made from a client. When a connection is made sets client to the client socket and address to the address of the connecting client. This function will raise OSError if an error occurs.

The resulting client will inherit any properties of the server socket. For example: whether the socket is buffered or not.

The SocketHandle associated with the resulting client will not be inheritable by child processes by default. This can be changed via the inheritable parameter.

The accept call may result in an error if the connecting socket disconnects during the duration of the accept. If the SafeDisconn flag is specified then this error will not be raised and instead accept will be called again.

### bindAddr

[ref: #symbol-bindaddr]

Binds address:port to the socket.

**Input:**
- `socket: Socket`
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
- `socket: Socket`
- `path: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binds Unix socket to path. This only works on Unix-style systems: Mac OS X, BSD and Linux

### clientGetPskFunc

[ref: #symbol-clientgetpskfunc]

**Input:**
- `ctx: SslContext`

**Output:** `SslClientGetPskFunc`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clientGetPskFunc=

[ref: #symbol-clientgetpskfunc]

Sets function that returns the client identity and the PSK based on identity hint from the server.

**Input:**
- `ctx: SslContext`
- `fun: SslClientGetPskFunc`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets function that returns the client identity and the PSK based on identity hint from the server.

Only used in PSK ciphersuites.

### close

[ref: #symbol-close]

Closes a socket.

**Input:**
- `socket: Socket`
- `flags:  = {SafeDisconn}`

**Output:** *(none)*
**Pragmas:** `raises: [LibraryError, Exception, OSError, SslError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception, OSError, SslError, OSError`, `tags: RootEffect`, `forbids: `

Closes a socket.

If socket is an SSL/TLS socket, this proc will also send a closure notification to the peer. If SafeDisconn is in flags, failure to do so due to disconnections will be ignored. This is generally safe in practice. See [here](https://security.stackexchange.com/a/82044) for more details.

### connect

[ref: #symbol-connect]

Connects socket to address:port. Address can be an IP address or a host name. If address is a host name, this function will try each IP of that host name. htons is already performed on port so you must not do it.

**Input:**
- `socket: Socket`
- `address: string`
- `port:  = Port(0)`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect, RootEffect]`, `raises: [OSError, SslError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, RootEffect`, `raises: OSError, SslError`, `forbids: `

Connects socket to address:port. Address can be an IP address or a host name. If address is a host name, this function will try each IP of that host name. htons is already performed on port so you must not do it.

If socket is an SSL socket a handshake will be automatically performed.

### connect

[ref: #symbol-connect]

Connects to server as specified by address on port specified by port.

**Input:**
- `socket: Socket`
- `address: string`
- `port:  = Port(0)`
- `timeout: int`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect, WriteIOEffect, RootEffect]`, `raises: [OSError, TimeoutError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, WriteIOEffect, RootEffect`, `raises: OSError, TimeoutError`, `forbids: `

Connects to server as specified by address on port specified by port.

The timeout parameter specifies the time in milliseconds to allow for the connection to the server to be made.

### connectUnix

[ref: #symbol-connectunix]

**Input:**
- `socket: Socket`
- `path: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Connects to Unix socket on path. This only works on Unix-style systems: Mac OS X, BSD and Linux

### destroyContext

[ref: #symbol-destroycontext]

**Input:**
- `ctx: SslContext`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Free memory referenced by SslContext.

### dial

[ref: #symbol-dial]

**Input:**
- `address: string`
- `port: Port`
- `protocol:  = IPPROTO_TCP`
- `buffered:  = true`

**Output:** `owned(Socket)`
**Pragmas:** `tags: [ReadIOEffect, WriteIOEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, WriteIOEffect`, `raises: OSError, IOError`, `forbids: `

Establishes connection to the specified address:port pair via the specified protocol. The procedure iterates through possible resolutions of the address until it succeeds, meaning that it seamlessly works with both IPv4 and IPv6. Returns Socket ready to send or receive data.

### fromSockAddr

[ref: #symbol-fromsockaddr]

**Input:**
- `sa: Sockaddr_storage | SockAddr | Sockaddr_in | Sockaddr_in6`
- `sl: SockLen`
- `address: var IpAddress`
- `port: var Port`

**Output:** *(none)*
**Generic parameters:** `sa:type`

**Pragmas:** `inline`

Converts SockAddr and SockLen to IpAddress and Port. Raises ObjectConversionDefect in case of invalid sa and sl arguments.

### getExtraData

[ref: #symbol-getextradata]

**Input:**
- `ctx: SslContext`
- `index: int`

**Output:** `RootRef`
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Retrieves arbitrary data stored inside SslContext.

### getFd

[ref: #symbol-getfd]

**Input:**
- `socket: Socket`

**Output:** `SocketHandle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the socket's file descriptor

### getLocalAddr

[ref: #symbol-getlocaladdr]

Get the socket's local address and port number.

**Input:**
- `socket: Socket`

**Output:** `(string, Port)`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Get the socket's local address and port number.

This is high-level interface for getsockname.

### getPeerAddr

[ref: #symbol-getpeeraddr]

Get the socket's peer address and port number.

**Input:**
- `socket: Socket`

**Output:** `(string, Port)`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Get the socket's peer address and port number.

This is high-level interface for getpeername.

### getPeerCertificates

[ref: #symbol-getpeercertificates]

**Input:**
- `sslHandle: SslPtr`

**Output:** `seq[Certificate]`
**Pragmas:** `raises: [Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception`, `tags: `, `forbids: `

Returns the certificate chain received by the peer we are connected to through the OpenSSL connection represented by sslHandle. The handshake must have been completed and the certificate chain must have been verified successfully or else an empty sequence is returned. The chain is ordered from leaf certificate to root certificate.

### getPeerCertificates

[ref: #symbol-getpeercertificates]

**Input:**
- `socket: Socket`

**Output:** `seq[Certificate]`
**Pragmas:** `raises: [Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception`, `tags: `, `forbids: `

Returns the certificate chain received by the peer we are connected to through the given socket. The handshake must have been completed and the certificate chain must have been verified successfully or else an empty sequence is returned. The chain is ordered from leaf certificate to root certificate.

### getPrimaryIPAddr

[ref: #symbol-getprimaryipaddr]

Finds the local IP address, usually assigned to eth0 on LAN or wlan0 on WiFi, used to reach an external address. Useful to run local services.

**Input:**
- `dest:  = parseIpAddress("8.8.8.8")`

**Output:** `IpAddress`
**Pragmas:** `raises: [OSError, OSError, SslError, ValueError, Exception, LibraryError]`, `tags: [ReadIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: OSError, OSError, SslError, ValueError, Exception, LibraryError`, `tags: ReadIOEffect, RootEffect`, `forbids: `

Finds the local IP address, usually assigned to eth0 on LAN or wlan0 on WiFi, used to reach an external address. Useful to run local services.

No traffic is sent.

Supports IPv4 and v6. Raises OSError if external networking is not set up.

### getPskIdentity

[ref: #symbol-getpskidentity]

**Input:**
- `socket: Socket`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the PSK identity provided by the client.

### getSocketError

[ref: #symbol-getsocketerror]

**Input:**
- `socket: Socket`

**Output:** `OSErrorCode`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Checks osLastError for a valid error. If it has been reset it uses the last error stored in the socket object.

### getSockOpt

[ref: #symbol-getsockopt]

**Input:**
- `socket: Socket`
- `opt: SOBool`
- `level:  = SOL_SOCKET`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Retrieves option opt as a boolean value.

### gotHandshake

[ref: #symbol-gothandshake]

Determines whether a handshake has occurred between a client (socket) and the server that socket is connected to.

**Input:**
- `socket: Socket`

**Output:** `bool`
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Determines whether a handshake has occurred between a client (socket) and the server that socket is connected to.

Throws SslError if socket is not an SSL socket.

### hasDataBuffered

[ref: #symbol-hasdatabuffered]

**Input:**
- `s: Socket`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether a socket has data buffered.

### IPv4_any

[ref: #symbol-ipv4-any]

**Input:**
- *(none)*

**Output:** `IpAddress`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the IPv4 any address, which can be used to listen on all available network adapters

### IPv4_broadcast

[ref: #symbol-ipv4-broadcast]

**Input:**
- *(none)*

**Output:** `IpAddress`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the IPv4 broadcast address (255.255.255.255)

### IPv4_loopback

[ref: #symbol-ipv4-loopback]

**Input:**
- *(none)*

**Output:** `IpAddress`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the IPv4 loopback address (127.0.0.1)

### IPv6_any

[ref: #symbol-ipv6-any]

**Input:**
- *(none)*

**Output:** `IpAddress`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the IPv6 any address (::0), which can be used to listen on all available network adapters

### IPv6_loopback

[ref: #symbol-ipv6-loopback]

**Input:**
- *(none)*

**Output:** `IpAddress`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the IPv6 loopback address (::1)

### isDisconnectionError

[ref: #symbol-isdisconnectionerror]

**Input:**
- `flags: set[SocketFlag]`
- `lastError: OSErrorCode`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether lastError is a disconnection error. Only does this if flags contains SafeDisconn.

### isIpAddress

[ref: #symbol-isipaddress]

**Input:**
- `addressStr: string`

**Output:** `bool`
**Pragmas:** `tags: []`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Checks if a string is an IP address Returns true if it is, false otherwise

### isSsl

[ref: #symbol-isssl]

**Input:**
- `socket: Socket`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether socket is a SSL socket.

### listen

[ref: #symbol-listen]

Marks socket as accepting connections. Backlog specifies the maximum length of the queue of pending connections.

**Input:**
- `socket: Socket`
- `backlog:  = SOMAXCONN`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Marks socket as accepting connections. Backlog specifies the maximum length of the queue of pending connections.

Raises an OSError error upon failure.

### newContext

[ref: #symbol-newcontext]

Creates an SSL context.

**Input:**
- `protVersion:  = protSSLv23`
- `verifyMode:  = CVerifyPeer`
- `certFile:  = ""`
- `keyFile:  = ""`
- `cipherList:  = CiphersIntermediate`
- `caDir:  = ""`
- `caFile:  = ""`
- `ciphersuites:  = CiphersModern`

**Output:** `SslContext`
**Pragmas:** `raises: [LibraryError, SslError, Exception, IOError]`, `tags: [RootEffect, ReadDirEffect, ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, SslError, Exception, IOError`, `tags: RootEffect, ReadDirEffect, ReadEnvEffect`, `forbids: `

Creates an SSL context.

Protocol version is currently ignored by default and TLS is used. With -d:openssl10, only SSLv23 and TLSv1 may be used.

There are three options for verify mode: CVerifyNone: certificates are not verified; CVerifyPeer: certificates are verified; CVerifyPeerUseEnvVars: certificates are verified and the optional environment variables SSL\_CERT\_FILE and SSL\_CERT\_DIR are also used to locate certificates

The nimDisableCertificateValidation define overrides verifyMode and disables certificate verification globally!

CA certificates will be loaded, in the following order, from:

* caFile, caDir, parameters, if set
* if verifyMode is set to CVerifyPeerUseEnvVars, the SSL\_CERT\_FILE and SSL\_CERT\_DIR environment variables are used
* a set of files and directories from the [ssl\_certs](ssl_certs.html) file.

The last two parameters specify the certificate file path and the key file path, a server socket will most likely not work without these.

Certificates can be generated using the following command:

* openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout mykey.pem -out mycert.pem

or using ECDSA:

* openssl ecparam -out mykey.pem -name secp256k1 -genkey
* openssl req -new -key mykey.pem -x509 -nodes -days 365 -out mycert.pem

### newSocket

[ref: #symbol-newsocket]

**Input:**
- `fd: SocketHandle`
- `domain: Domain = AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`
- `buffered:  = true`

**Output:** `owned(Socket)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new socket as specified by the params.

### newSocket

[ref: #symbol-newsocket]

Creates a new socket.

**Input:**
- `domain: cint`
- `sockType: cint`
- `protocol: cint`
- `buffered:  = true`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(Socket)`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a new socket.

The SocketHandle associated with the resulting Socket will not be inheritable by child processes by default. This can be changed via the inheritable parameter.

If an error occurs OSError will be raised.

### newSocket

[ref: #symbol-newsocket]

Creates a new socket.

**Input:**
- `domain: Domain = AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`
- `buffered:  = true`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(Socket)`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a new socket.

The SocketHandle associated with the resulting Socket will not be inheritable by child processes by default. This can be changed via the inheritable parameter.

If an error occurs OSError will be raised.

### parseIpAddress

[ref: #symbol-parseipaddress]

Parses an IP address

**Input:**
- `addressStr: string`

**Output:** `IpAddress`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an IP address

Raises ValueError on error.

For IPv4 addresses, only the strict form as defined in RFC 6943 is considered valid, see <https://datatracker.ietf.org/doc/html/rfc6943#section-3.1.1>.

### pskIdentityHint=

[ref: #symbol-pskidentityhint]

Sets the identity hint passed to server.

**Input:**
- `ctx: SslContext`
- `hint: string`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Sets the identity hint passed to server.

Only used in PSK ciphersuites.

### raiseSSLError

[ref: #symbol-raisesslerror]

**Input:**
- `s:  = ""`

**Output:** *(none)*
**Pragmas:** `raises: [SslError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SslError`, `tags: `, `forbids: `

Raises a new SSL error.

### readLine

[ref: #symbol-readline]

Reads a line of data from socket.

**Input:**
- `socket: Socket`
- `line: var string`
- `timeout:  = -1`
- `flags:  = {SafeDisconn}`
- `maxLength:  = MaxLineLength`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect, TimeEffect]`, `raises: [TimeoutError, OSError, SslError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, TimeEffect`, `raises: TimeoutError, OSError, SslError`, `forbids: `

Reads a line of data from socket.

If a full line is read \r\L is not added to line, however if solely \r\L is read then line will be set to it.

If the socket is disconnected, line will be set to "".

An OSError exception will be raised in the case of a socket error.

A timeout can be specified in milliseconds, if data is not received within the specified time a TimeoutError exception will be raised.

The maxLength parameter determines the maximum amount of characters that can be read. The result is truncated after that.

**Warning:**
Only the SafeDisconn flag is currently supported.

### recv

[ref: #symbol-recv]

Receives data from a socket.

**Input:**
- `socket: Socket`
- `data: pointer`
- `size: int`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Receives data from a socket.

**Note**: This is a low-level function, you may be interested in the higher level versions of this function which are also named recv.

### recv

[ref: #symbol-recv]

**Input:**
- `socket: Socket`
- `data: pointer`
- `size: int`
- `timeout: int`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect, TimeEffect]`, `raises: [TimeoutError, OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, TimeEffect`, `raises: TimeoutError, OSError`, `forbids: `

overload with a timeout parameter in milliseconds.

### recv

[ref: #symbol-recv]

Higher-level version of recv.

**Input:**
- `socket: Socket`
- `data: var string`
- `size: int`
- `timeout:  = -1`
- `flags:  = {SafeDisconn}`

**Output:** `int`
**Pragmas:** `raises: [TimeoutError, OSError, SslError]`, `tags: [ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: TimeoutError, OSError, SslError`, `tags: ReadIOEffect, TimeEffect`, `forbids: `

Higher-level version of recv.

Reads **up to** size bytes from socket into data.

For buffered sockets this function will attempt to read all the requested data. It will read this data in BufferSize chunks.

For unbuffered sockets this function makes no effort to read all the data requested. It will return as much data as the operating system gives it.

When 0 is returned the socket's connection has been closed.

This function will throw an OSError exception when an error occurs. A value lower than 0 is never returned.

A timeout may be specified in milliseconds, if enough data is not received within the time specified a TimeoutError exception will be raised.

**Warning:**
Only the SafeDisconn flag is currently supported.


[Next](net_2.md)
