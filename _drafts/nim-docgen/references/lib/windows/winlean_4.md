---
source_hash: 319d53cfc1304803
source_path: lib/windows/winlean.nim
---

### suspendThread

[ref: #symbol-suspendthread]

**Input:**
- `hThread: Handle`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SuspendThread"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SwitchToFiber

[ref: #symbol-switchtofiber]

**Input:**
- `fiber: pointer`

**Output:** *(none)*
**Pragmas:** `stdcall`, `discardable`, `dynlib: "kernel32"`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### terminateProcess

[ref: #symbol-terminateprocess]

**Input:**
- `hProcess: Handle`
- `uExitCode: int`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "TerminateProcess"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toFILETIME

[ref: #symbol-tofiletime]

**Input:**
- `t: int64`

**Output:** `FILETIME`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convert the Windows file time timestamp t to FILETIME.

### unmapViewOfFile

[ref: #symbol-unmapviewoffile]

**Input:**
- `lpBaseAddress: pointer`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "UnmapViewOfFile"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### unregisterWait

[ref: #symbol-unregisterwait]

**Input:**
- `WaitHandle: Handle`

**Output:** `DWORD`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "UnregisterWait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### waitForMultipleObjects

[ref: #symbol-waitformultipleobjects]

**Input:**
- `nCount: DWORD`
- `lpHandles: PWOHandleArray`
- `bWaitAll: WINBOOL`
- `dwMilliseconds: DWORD`

**Output:** `DWORD`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "WaitForMultipleObjects"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### waitForSingleObject

[ref: #symbol-waitforsingleobject]

**Input:**
- `hHandle: Handle`
- `dwMilliseconds: int32`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "WaitForSingleObject"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### writeFile

[ref: #symbol-writefile]

**Input:**
- `hFile: Handle`
- `buffer: pointer`
- `nNumberOfBytesToWrite: int32`
- `lpNumberOfBytesWritten: ptr int32`
- `lpOverlapped: pointer`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "WriteFile"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wsaCloseEvent

[ref: #symbol-wsacloseevent]

**Input:**
- `hEvent: Handle`

**Output:** `bool`
**Pragmas:** `stdcall`, `importc: "WSACloseEvent"`, `dynlib: "ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wsaCreateEvent

[ref: #symbol-wsacreateevent]

**Input:**
- *(none)*

**Output:** `Handle`
**Pragmas:** `stdcall`, `importc: "WSACreateEvent"`, `dynlib: "ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wsaEventSelect

[ref: #symbol-wsaeventselect]

**Input:**
- `s: SocketHandle`
- `hEventObject: Handle`
- `lNetworkEvents: clong`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSAEventSelect"`, `dynlib: "ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wsaGetLastError

[ref: #symbol-wsagetlasterror]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc: "WSAGetLastError"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WSAIoctl

[ref: #symbol-wsaioctl]

**Input:**
- `s: SocketHandle`
- `dwIoControlCode: DWORD`
- `lpvInBuffer: pointer`
- `cbInBuffer: DWORD`
- `lpvOutBuffer: pointer`
- `cbOutBuffer: DWORD`
- `lpcbBytesReturned: PDWORD`
- `lpOverlapped: POVERLAPPED`
- `lpCompletionRoutine: POVERLAPPED_COMPLETION_ROUTINE`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSAIoctl"`, `dynlib: "Ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WSARecv

[ref: #symbol-wsarecv]

**Input:**
- `s: SocketHandle`
- `buf: ptr TWSABuf`
- `bufCount: DWORD`
- `bytesReceived: PDWORD`
- `flags: PDWORD`
- `lpOverlapped: POVERLAPPED`
- `completionProc: POVERLAPPED_COMPLETION_ROUTINE`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSARecv"`, `dynlib: "Ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WSARecvFrom

[ref: #symbol-wsarecvfrom]

**Input:**
- `s: SocketHandle`
- `buf: ptr TWSABuf`
- `bufCount: DWORD`
- `bytesReceived: PDWORD`
- `flags: PDWORD`
- `name: ptr SockAddr`
- `namelen: ptr cint`
- `lpOverlapped: POVERLAPPED`
- `completionProc: POVERLAPPED_COMPLETION_ROUTINE`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSARecvFrom"`, `dynlib: "Ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wsaResetEvent

[ref: #symbol-wsaresetevent]

**Input:**
- `hEvent: Handle`

**Output:** `bool`
**Pragmas:** `stdcall`, `importc: "WSAResetEvent"`, `dynlib: "ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WSASend

[ref: #symbol-wsasend]

**Input:**
- `s: SocketHandle`
- `buf: ptr TWSABuf`
- `bufCount: DWORD`
- `bytesSent: PDWORD`
- `flags: DWORD`
- `lpOverlapped: POVERLAPPED`
- `completionProc: POVERLAPPED_COMPLETION_ROUTINE`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSASend"`, `dynlib: "Ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WSASendTo

[ref: #symbol-wsasendto]

**Input:**
- `s: SocketHandle`
- `buf: ptr TWSABuf`
- `bufCount: DWORD`
- `bytesSent: PDWORD`
- `flags: DWORD`
- `name: ptr SockAddr`
- `namelen: cint`
- `lpOverlapped: POVERLAPPED`
- `completionProc: POVERLAPPED_COMPLETION_ROUTINE`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSASendTo"`, `dynlib: "Ws2_32.dll"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wsaStartup

[ref: #symbol-wsastartup]

**Input:**
- `wVersionRequired: int16`
- `WSData: ptr WSAData`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "WSAStartup"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### hasOverlappedIoCompleted

[ref: #symbol-hasoverlappediocompleted]

**Input:**
- `lpOverlapped: `

**Output:** `bool`
### WSAIORW

[ref: #symbol-wsaiorw]

**Input:**
- `x: `
- `y: `

**Output:** `untyped`
## Type

### AddrInfo

[ref: #symbol-addrinfo]

```nim
AddrInfo {.importc: "ADDRINFOA", header: "ws2tcpip.h".} = object
  ai_flags*: cint            ## Input flags.
  ai_family*: cint           ## Address family of socket.
  ai_socktype*: cint         ## Socket type.
  ai_protocol*: cint         ## Protocol of socket.
  ai_addrlen*: csize_t       ## Length of socket address.
  ai_canonname*: cstring     ## Canonical name of service location.
  ai_addr*: ptr SockAddr     ## Socket address of socket.
  ai_next*: ptr AddrInfo     ## Pointer to next in list.
```

### BY_HANDLE_FILE_INFORMATION

[ref: #symbol-by-handle-file-information]

```nim
BY_HANDLE_FILE_INFORMATION = object
  dwFileAttributes*: DWORD
  ftCreationTime*: FILETIME
  ftLastAccessTime*: FILETIME
  ftLastWriteTime*: FILETIME
  dwVolumeSerialNumber*: DWORD
  nFileSizeHigh*: DWORD
  nFileSizeLow*: DWORD
  nNumberOfLinks*: DWORD
  nFileIndexHigh*: DWORD
  nFileIndexLow*: DWORD
```

### BYTE

[ref: #symbol-byte]

```nim
BYTE = uint8
```

### DWORD

[ref: #symbol-dword]

```nim
DWORD = int32
```

### FILETIME

[ref: #symbol-filetime]

```nim
FILETIME = object
  dwLowDateTime*: DWORD
  dwHighDateTime*: DWORD
```

CANNOT BE int64 BECAUSE OF ALIGNMENT

### GUID

[ref: #symbol-guid]

```nim
GUID = object
  D1*: int32
  D2*: int16
  D3*: int16
  D4*: array[0 .. 7, int8]
```

### Handle

[ref: #symbol-handle]

```nim
Handle = int
```

### HDC

[ref: #symbol-hdc]

```nim
HDC = Handle
```

### HGLRC

[ref: #symbol-hglrc]

```nim
HGLRC = Handle
```

### Hostent

[ref: #symbol-hostent]

```nim
Hostent = object
  h_name*: cstring
  h_aliases*: cstringArray
  h_addrtype*: int16
  h_length*: int16
  h_addr_list*: cstringArray
```

### In6_addr

[ref: #symbol-in6-addr]

```nim
In6_addr {.importc: "IN6_ADDR", header: "winsock2.h".} = object
  bytes* {.importc: "u.Byte".}: array[0 .. 15, char]
```

### InAddr

[ref: #symbol-inaddr]

```nim
InAddr {.importc: "IN_ADDR", header: "winsock2.h", union.} = object
  s_addr*: uint32
```

### KEY_EVENT_RECORD

[ref: #symbol-key-event-record]

```nim
KEY_EVENT_RECORD = object
  eventType*: int16
  bKeyDown*: WINBOOL
  wRepeatCount*: int16
  wVirtualKeyCode*: int16
  wVirtualScanCode*: int16
  uChar*: int16
  dwControlKeyState*: DWORD
```

### LONG

[ref: #symbol-long]

```nim
LONG = int32
```

### LPFIBER_START_ROUTINE

[ref: #symbol-lpfiber-start-routine]

```nim
LPFIBER_START_ROUTINE = proc (param: pointer) {.stdcall.}
```

### LPFILETIME

[ref: #symbol-lpfiletime]

```nim
LPFILETIME = ptr FILETIME
```

### LPINT

[ref: #symbol-lpint]

```nim
LPINT = ptr int32
```

### OSVERSIONINFO

[ref: #symbol-osversioninfo]

```nim
OSVERSIONINFO = object
  dwOSVersionInfoSize*: DWORD
  dwMajorVersion*: DWORD
  dwMinorVersion*: DWORD
  dwBuildNumber*: DWORD
  dwPlatformId*: DWORD
  szCSDVersion*: array[0 .. 127, WinChar]
```

### OVERLAPPED

[ref: #symbol-overlapped]

```nim
OVERLAPPED {.pure, inheritable.} = object
  internal*: PULONG
  internalHigh*: PULONG
  offset*: DWORD
  offsetHigh*: DWORD
  hEvent*: Handle
```

### PBOOL

[ref: #symbol-pbool]

```nim
PBOOL = ptr WINBOOL
```

### PDWORD

[ref: #symbol-pdword]

```nim
PDWORD = ptr DWORD
```

### POVERLAPPED

[ref: #symbol-poverlapped]

```nim
POVERLAPPED = ptr OVERLAPPED
```

### POVERLAPPED_COMPLETION_ROUTINE

[ref: #symbol-poverlapped-completion-routine]

```nim
POVERLAPPED_COMPLETION_ROUTINE = proc (para1: DWORD; para2: DWORD;
                                       para3: POVERLAPPED) {.stdcall.}
```

### PROCESS_INFORMATION

[ref: #symbol-process-information]

```nim
PROCESS_INFORMATION = object
  hProcess*: Handle
  hThread*: Handle
  dwProcessId*: int32
  dwThreadId*: int32
```

### Protoent

[ref: #symbol-protoent]

```nim
Protoent = object
  p_name*: cstring
  p_aliases*: cstringArray
  p_proto*: cshort
```

### PSID

[ref: #symbol-psid]

```nim
PSID = ptr SID
```

### PULONG

[ref: #symbol-pulong]

```nim
PULONG = ptr int
```

### PULONG_PTR

[ref: #symbol-pulong-ptr]

```nim
PULONG_PTR = ptr uint
```

### PWOHandleArray

[ref: #symbol-pwohandlearray]

```nim
PWOHandleArray = ptr WOHandleArray
```

### SECURITY_ATTRIBUTES

[ref: #symbol-security-attributes]

```nim
SECURITY_ATTRIBUTES = object
  nLength*: int32
  lpSecurityDescriptor*: pointer
  bInheritHandle*: WINBOOL
```

### Servent

[ref: #symbol-servent]

```nim
Servent = object
  s_name*: cstring
  s_aliases*: cstringArray
  when defined(cpu64):
    s_proto*: cstring
    s_port*: int16
  else:
    s_port*: int16
    s_proto*: cstring
```

### SID

[ref: #symbol-sid]

```nim
SID {.importc, header: "<windows.h>".} = object
```

### SID_IDENTIFIER_AUTHORITY

[ref: #symbol-sid-identifier-authority]

```nim
SID_IDENTIFIER_AUTHORITY {.importc, header: "<windows.h>".} = object
  value* {.importc: "Value".}: array[6, BYTE]
```

### SockAddr

[ref: #symbol-sockaddr]

```nim
SockAddr {.importc: "SOCKADDR", header: "winsock2.h".} = object
  sa_family*: uint16
  sa_data*: array[0 .. 13, char]
```

### Sockaddr_in

[ref: #symbol-sockaddr-in]

```nim
Sockaddr_in {.importc: "SOCKADDR_IN", header: "winsock2.h".} = object
  sin_family*: uint16
  sin_port*: uint16
  sin_addr*: InAddr
  sin_zero*: array[0 .. 7, char]
```

### Sockaddr_in6

[ref: #symbol-sockaddr-in6]

```nim
Sockaddr_in6 {.importc: "SOCKADDR_IN6", header: "ws2tcpip.h".} = object
  sin6_family*: uint16
  sin6_port*: uint16
  sin6_flowinfo*: int32
  sin6_addr*: In6_addr
  sin6_scope_id*: int32
```

### Sockaddr_storage

[ref: #symbol-sockaddr-storage]

```nim
Sockaddr_storage {.importc: "SOCKADDR_STORAGE", header: "winsock2.h".} = object
  ss_family*: uint16
```

### SocketHandle

[ref: #symbol-sockethandle]

```nim
SocketHandle = distinct int
```

### SockLen

[ref: #symbol-socklen]

```nim
SockLen = cuint
```

### STARTUPINFO

[ref: #symbol-startupinfo]

```nim
STARTUPINFO = object
  cb*: int32
  lpReserved*: cstring
  lpDesktop*: cstring
  lpTitle*: cstring
  dwX*: int32
  dwY*: int32
  dwXSize*: int32
  dwYSize*: int32
  dwXCountChars*: int32
  dwYCountChars*: int32
  dwFillAttribute*: int32
  dwFlags*: int32
  wShowWindow*: int16
  cbReserved2*: int16
  lpReserved2*: pointer
  hStdInput*: Handle
  hStdOutput*: Handle
  hStdError*: Handle
```

### TFdSet

[ref: #symbol-tfdset]

```nim
TFdSet = object
  fd_count*: cint
  fd_array*: array[0 .. 64 - 1, SocketHandle]
```

### Timeval

[ref: #symbol-timeval]

```nim
Timeval {.importc: "struct timeval", header: "<time.h>".} = object
  tv_sec*, tv_usec*: int32
```

### TWSABuf

[ref: #symbol-twsabuf]

```nim
TWSABuf {.importc: "WSABUF", header: "winsock2.h".} = object
  len*: ULONG
  buf*: cstring
```

### ULONG

[ref: #symbol-ulong]

```nim
ULONG = int32
```

### ULONG_PTR

[ref: #symbol-ulong-ptr]

```nim
ULONG_PTR = uint
```

### WAITORTIMERCALLBACK

[ref: #symbol-waitortimercallback]

```nim
WAITORTIMERCALLBACK = proc (para1: pointer; para2: int32) {.stdcall.}
```

### WIN32_FIND_DATA

[ref: #symbol-win32-find-data]

```nim
WIN32_FIND_DATA {.pure.} = object
  dwFileAttributes*: int32
  ftCreationTime*: FILETIME
  ftLastAccessTime*: FILETIME
  ftLastWriteTime*: FILETIME
  nFileSizeHigh*: int32
  nFileSizeLow*: int32
  cFileName*: array[0 .. 260 - 1, WinChar]
  cAlternateFileName*: array[0 .. 13, WinChar]
```

### WINBOOL

[ref: #symbol-winbool]

```nim
WINBOOL = int32
```

WINBOOL uses opposite convention as posix, !=0 meaning success.

### WinChar

[ref: #symbol-winchar]

```nim
WinChar = Utf16Char
```

### WinSizeT

[ref: #symbol-winsizet]

```nim
WinSizeT = uint64
```

### WOHandleArray

[ref: #symbol-wohandlearray]

```nim
WOHandleArray = array[0 .. 0x00000040 - 1, Handle]
```

### WSAData

[ref: #symbol-wsadata]

```nim
WSAData {.importc: "WSADATA", header: "winsock2.h".} = object
```

### WSAPROC_ACCEPTEX

[ref: #symbol-wsaproc-acceptex]

```nim
WSAPROC_ACCEPTEX = proc (sListenSocket: SocketHandle;
                         sAcceptSocket: SocketHandle; lpOutputBuffer: pointer;
                         dwReceiveDataLength: DWORD;
                         dwLocalAddressLength: DWORD;
                         dwRemoteAddressLength: DWORD;
                         lpdwBytesReceived: ptr DWORD; lpOverlapped: POVERLAPPED): bool {.
    stdcall, gcsafe, raises: [].}
```

### WSAPROC_CONNECTEX

[ref: #symbol-wsaproc-connectex]

```nim
WSAPROC_CONNECTEX = proc (s: SocketHandle; name: ptr SockAddr; namelen: cint;
                          lpSendBuffer: pointer; dwSendDataLength: DWORD;
                          lpdwBytesSent: ptr DWORD; lpOverlapped: POVERLAPPED): bool {.
    stdcall, gcsafe, raises: [].}
```

### WSAPROC_GETACCEPTEXSOCKADDRS

[ref: #symbol-wsaproc-getacceptexsockaddrs]

```nim
WSAPROC_GETACCEPTEXSOCKADDRS = proc (lpOutputBuffer: pointer;
                                     dwReceiveDataLength: DWORD;
                                     dwLocalAddressLength: DWORD;
                                     dwRemoteAddressLength: DWORD;
                                     LocalSockaddr: ptr PSockAddr;
                                     LocalSockaddrLength: ptr cint;
                                     RemoteSockaddr: ptr PSockAddr;
                                     RemoteSockaddrLength: ptr cint) {.stdcall,
    gcsafe, raises: [].}
```

## Var

### INVALID_SOCKET

[ref: #symbol-invalid-socket]

```nim
INVALID_SOCKET {.importc, header: "winsock2.h".}: SocketHandle
```

### SO_ACCEPTCONN

[ref: #symbol-so-acceptconn]

```nim
SO_ACCEPTCONN {.importc, header: "winsock2.h".}: cint
```

### SO_BROADCAST

[ref: #symbol-so-broadcast]

```nim
SO_BROADCAST {.importc, header: "winsock2.h".}: cint
```

### SO_DEBUG

[ref: #symbol-so-debug]

```nim
SO_DEBUG {.importc, header: "winsock2.h".}: cint
```

turn on debugging info recording

### SO_DONTLINGER

[ref: #symbol-so-dontlinger]

```nim
SO_DONTLINGER {.importc, header: "winsock2.h".}: cint
```

### SO_DONTROUTE

[ref: #symbol-so-dontroute]

```nim
SO_DONTROUTE {.importc, header: "winsock2.h".}: cint
```

### SO_ERROR

[ref: #symbol-so-error]

```nim
SO_ERROR {.importc, header: "winsock2.h".}: cint
```

### SO_EXCLUSIVEADDRUSE

[ref: #symbol-so-exclusiveaddruse]

```nim
SO_EXCLUSIVEADDRUSE {.importc, header: "winsock2.h".}: cint
```

### SO_KEEPALIVE

[ref: #symbol-so-keepalive]

```nim
SO_KEEPALIVE {.importc, header: "winsock2.h".}: cint
```

### SO_LINGER

[ref: #symbol-so-linger]

```nim
SO_LINGER {.importc, header: "winsock2.h".}: cint
```

### SO_OOBINLINE

[ref: #symbol-so-oobinline]

```nim
SO_OOBINLINE {.importc, header: "winsock2.h".}: cint
```

### SO_REUSEADDR

[ref: #symbol-so-reuseaddr]

```nim
SO_REUSEADDR {.importc, header: "winsock2.h".}: cint
```

### SO_REUSEPORT

[ref: #symbol-so-reuseport]

```nim
SO_REUSEPORT {.importc: "SO_REUSEADDR", header: "winsock2.h".}: cint
```


[Prev](winlean_3.md) | [Next](winlean_5.md)
