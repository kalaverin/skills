---
source_hash: b1e2e794bf3e90ea
source_path: lib/pure/nativesockets.nim
---

# nativesockets

[ref: #module-nativesockets]

This module implements a low-level cross-platform sockets interface. Look at the net module for the higher-level version.

## Const

### FIONBIO

[ref: #symbol-fionbio]

```nim
FIONBIO = -2147195266'i32
```

### IOC_IN

[ref: #symbol-ioc-in]

```nim
IOC_IN = -2147483648
```

### IOCPARM_MASK

[ref: #symbol-iocparm-mask]

```nim
IOCPARM_MASK = 127
```

### IPPROTO_NONE

[ref: #symbol-ipproto-none]

```nim
IPPROTO_NONE = IPPROTO_IP
```

Use this if your socket type requires a protocol value of zero (e.g. Unix sockets).

## Let

### osInvalidSocket

[ref: #symbol-osinvalidsocket]

```nim
osInvalidSocket = INVALID_SOCKET
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `p: Port`

**Output:** `string`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the port number as a string

### `==`

[ref: #symbol-]

**Input:**
- `a: Port`
- `b: Port`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

== for ports.

### accept

[ref: #symbol-accept]

Accepts a new client connection.

**Input:**
- `fd: SocketHandle`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `(SocketHandle, string)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Accepts a new client connection.

inheritable decides if the resulting SocketHandle can be inherited by child processes.

Returns (osInvalidSocket, "") if an error occurred.

### bindAddr

[ref: #symbol-bindaddr]

**Input:**
- `socket: SocketHandle`
- `name: ptr SockAddr`
- `namelen: SockLen`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### close

[ref: #symbol-close]

**Input:**
- `socket: SocketHandle`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Closes a socket.

### createNativeSocket

[ref: #symbol-createnativesocket]

Creates a new socket; returns osInvalidSocket if an error occurs.

**Input:**
- `domain: cint`
- `sockType: cint`
- `protocol: cint`
- `inheritable: bool = defined(nimInheritHandles)`

**Output:** `SocketHandle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new socket; returns osInvalidSocket if an error occurs.

inheritable decides if the resulting SocketHandle can be inherited by child processes.

Use this overload if one of the enums specified above does not contain what you need.

### createNativeSocket

[ref: #symbol-createnativesocket]

Creates a new socket; returns osInvalidSocket if an error occurs.

**Input:**
- `domain: Domain = AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`
- `inheritable: bool = defined(nimInheritHandles)`

**Output:** `SocketHandle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new socket; returns osInvalidSocket if an error occurs.

inheritable decides if the resulting SocketHandle can be inherited by child processes.

### getAddrInfo

[ref: #symbol-getaddrinfo]

**Warning:**

**Input:**
- `address: string`
- `port: Port`
- `hints: AddrInfo`

**Output:** `ptr AddrInfo`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

**Warning:**
The resulting ptr AddrInfo must be freed using freeAddrInfo!

### getAddrInfo

[ref: #symbol-getaddrinfo]

**Warning:**

**Input:**
- `address: string`
- `port: Port`
- `domain: Domain = AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`

**Output:** `ptr AddrInfo`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

**Warning:**
The resulting ptr AddrInfo must be freed using freeAddrInfo!

### getAddrString

[ref: #symbol-getaddrstring]

**Input:**
- `sockAddr: ptr SockAddr`

**Output:** `string`
**Pragmas:** `raises: [Exception, OSError, IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception, OSError, IOError`, `tags: `, `forbids: `

Returns the string representation of address within sockAddr

### getAddrString

[ref: #symbol-getaddrstring]

Stores in strAddress the string representation of the address inside sockAddr

**Input:**
- `sockAddr: ptr SockAddr`
- `strAddress: var string`

**Output:** *(none)*
**Pragmas:** `raises: [Exception, OSError, IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception, OSError, IOError`, `tags: `, `forbids: `

Stores in strAddress the string representation of the address inside sockAddr

**Note**

* strAddress must be initialized to 46 in length.

### getHostByAddr

[ref: #symbol-gethostbyaddr]

**Input:**
- `ip: string`

**Output:** `Hostent`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError, IOError, Exception]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError, IOError, Exception`, `forbids: `

This function will lookup the hostname of an IP Address.

### getHostByName

[ref: #symbol-gethostbyname]

**Input:**
- `name: string`

**Output:** `Hostent`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

This function will lookup the IP address of a hostname.

### getHostname

[ref: #symbol-gethostname]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Returns the local hostname (not the FQDN)

### getLocalAddr

[ref: #symbol-getlocaladdr]

Returns the socket's local address and port number.

**Input:**
- `socket: SocketHandle`
- `domain: Domain`

**Output:** `(string, Port)`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Returns the socket's local address and port number.

Similar to POSIX's getsockname.

### getPeerAddr

[ref: #symbol-getpeeraddr]

Returns the socket's peer address and port number.

**Input:**
- `socket: SocketHandle`
- `domain: Domain`

**Output:** `(string, Port)`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Returns the socket's peer address and port number.

Similar to POSIX's getpeername

### getProtoByName

[ref: #symbol-getprotobyname]

**Input:**
- `name: string`

**Output:** `int`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns a protocol code from the database that matches the protocol name.

### getServByName

[ref: #symbol-getservbyname]

Searches the database from the beginning and finds the first entry for which the service name specified by name matches the s\_name member and the protocol name specified by proto matches the s\_proto member.

**Input:**
- `name: string`
- `proto: string`

**Output:** `Servent`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Searches the database from the beginning and finds the first entry for which the service name specified by name matches the s\_name member and the protocol name specified by proto matches the s\_proto member.

On posix this will search through the /etc/services file.

### getServByPort

[ref: #symbol-getservbyport]

Searches the database from the beginning and finds the first entry for which the port specified by port matches the s\_port member and the protocol name specified by proto matches the s\_proto member.

**Input:**
- `port: Port`
- `proto: string`

**Output:** `Servent`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Searches the database from the beginning and finds the first entry for which the port specified by port matches the s\_port member and the protocol name specified by proto matches the s\_proto member.

On posix this will search through the /etc/services file.

### getSockDomain

[ref: #symbol-getsockdomain]

**Input:**
- `socket: SocketHandle`

**Output:** `Domain`
**Pragmas:** `raises: [OSError, IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, IOError`, `tags: `, `forbids: `

Returns the socket's domain (AF\_INET or AF\_INET6).

### getSockName

[ref: #symbol-getsockname]

**Input:**
- `socket: SocketHandle`

**Output:** `Port`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the socket's associated port number.

### getSockOptInt

[ref: #symbol-getsockoptint]

**Input:**
- `socket: SocketHandle`
- `level: int`
- `optname: int`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

getsockopt for integer options.

### ioctlsocket

[ref: #symbol-ioctlsocket]

**Input:**
- `s: SocketHandle`
- `cmd: clong`
- `argptr: ptr clong`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "ioctlsocket"`, `dynlib: "ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### listen

[ref: #symbol-listen]

**Input:**
- `socket: SocketHandle`
- `backlog:  = SOMAXCONN`

**Output:** `cint`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Marks socket as accepting connections. Backlog specifies the maximum length of the queue of pending connections.

### ntohl

[ref: #symbol-ntohl]

**Input:**
- `x: uint32`

**Output:** `uint32`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts 32-bit unsigned integers from network to host byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 4-byte swap operation.

### ntohs

[ref: #symbol-ntohs]

**Input:**
- `x: uint16`

**Output:** `uint16`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts 16-bit unsigned integers from network to host byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 2-byte swap operation.

### selectRead

[ref: #symbol-selectread]

When a socket in readfds is ready to be read from then a non-zero value will be returned specifying the count of the sockets which can be read from. The sockets which cannot be read from will also be removed from readfds.

**Input:**
- `readfds: var seq[SocketHandle]`
- `timeout:  = 500`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

When a socket in readfds is ready to be read from then a non-zero value will be returned specifying the count of the sockets which can be read from. The sockets which cannot be read from will also be removed from readfds.

timeout is specified in milliseconds and -1 can be specified for an unlimited time.

### selectWrite

[ref: #symbol-selectwrite]

When a socket in writefds is ready to be written to then a non-zero value will be returned specifying the count of the sockets which can be written to. The sockets which cannot be written to will also be removed from writefds.

**Input:**
- `writefds: var seq[SocketHandle]`
- `timeout:  = 500`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

When a socket in writefds is ready to be written to then a non-zero value will be returned specifying the count of the sockets which can be written to. The sockets which cannot be written to will also be removed from writefds.

timeout is specified in milliseconds and -1 can be specified for an unlimited time.

### setBlocking

[ref: #symbol-setblocking]

Sets blocking mode on socket.

**Input:**
- `s: SocketHandle`
- `blocking: bool`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Sets blocking mode on socket.

Raises OSError on error.

### setInheritable

[ref: #symbol-setinheritable]

Set whether a socket is inheritable by child processes. Returns true on success.

**Input:**
- `s: SocketHandle`
- `inheritable: bool`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set whether a socket is inheritable by child processes. Returns true on success.

This function is not implemented on all platform, test for availability with declared() <system.html#declared,untyped>.

### setSockOptInt

[ref: #symbol-setsockoptint]

**Input:**
- `socket: SocketHandle`
- `level: int`
- `optname: int`
- `optval: int`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: OSError`, `forbids: `

setsockopt for integer options.

### toInt

[ref: #symbol-toint]

**Input:**
- `domain: Domain`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the Domain enum to a platform-dependent cint.

### toInt

[ref: #symbol-toint]

**Input:**
- `typ: SockType`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the SockType enum to a platform-dependent cint.

### toInt

[ref: #symbol-toint]

**Input:**
- `p: Protocol`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the Protocol enum to a platform-dependent cint.

### toKnownDomain

[ref: #symbol-toknowndomain]

**Input:**
- `family: cint`

**Output:** `Option[Domain]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the platform-dependent cint to the Domain or none(), if the cint is not known.

### toSockType

[ref: #symbol-tosocktype]

**Input:**
- `protocol: Protocol`

**Output:** `SockType`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### htonl

[ref: #symbol-htonl]

**Input:**
- `x: uint32`

**Output:** `untyped`
Converts 32-bit unsigned integers from host to network byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 4-byte swap operation.

### htons

[ref: #symbol-htons]

**Input:**
- `x: uint16`

**Output:** `untyped`
Converts 16-bit unsigned integers from host to network byte order. On machines where the host byte order is the same as network byte order, this is a no-op; otherwise, it performs a 2-byte swap operation.

## Type

### Domain

[ref: #symbol-domain]

```nim
Domain = enum
  AF_UNSPEC = 0, ## unspecified domain (can be detected automatically by
                  ## some procedures, such as getaddrinfo)
  AF_UNIX = 1,              ## for local socket (using a file). Unsupported on Windows.
  AF_INET = 2,              ## for network protocol IPv4 or
  AF_INET6 = 30
```

domain, which specifies the protocol family of the created socket. Other domains than those that are listed here are unsupported.

### Hostent

[ref: #symbol-hostent]

```nim
Hostent = object
  name*: string
  aliases*: seq[string]
  addrtype*: Domain
  length*: int
  addrList*: seq[string]
```

information about a given host

### Port

[ref: #symbol-port]

```nim
Port = distinct uint16
```

port type

### Protocol

[ref: #symbol-protocol]

```nim
Protocol = enum
  IPPROTO_TCP = 6,          ## Transmission control protocol.
  IPPROTO_UDP = 17,         ## User datagram protocol.
  IPPROTO_IP,               ## Internet protocol.
  IPPROTO_IPV6,             ## Internet Protocol Version 6.
  IPPROTO_RAW,              ## Raw IP Packets Protocol. Unsupported on Windows.
  IPPROTO_ICMP,             ## Internet Control message protocol.
  IPPROTO_ICMPV6             ## Internet Control message protocol for IPv6.
```

third argument to socket proc

### Servent

[ref: #symbol-servent]

```nim
Servent = object
  name*: string
  aliases*: seq[string]
  port*: Port
  proto*: string
```

information about a service

### SockType

[ref: #symbol-socktype]

```nim
SockType = enum
  SOCK_STREAM = 1,          ## reliable stream-oriented service or Stream Sockets
  SOCK_DGRAM = 2,           ## datagram service or Datagram Sockets
  SOCK_RAW = 3,             ## raw protocols atop the network layer.
  SOCK_SEQPACKET = 5         ## reliable sequenced packet service
```

second argument to socket proc
