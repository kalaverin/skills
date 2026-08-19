---
source_hash: 319d53cfc1304803
source_path: lib/windows/winlean.nim
---

### PROCESS_VM_READ

[ref: #symbol-process-vm-read]

```nim
PROCESS_VM_READ = 0x00000010'i32
```

### PROCESS_VM_WRITE

[ref: #symbol-process-vm-write]

```nim
PROCESS_VM_WRITE = 0x00000020'i32
```

### REALTIME_PRIORITY_CLASS

[ref: #symbol-realtime-priority-class]

```nim
REALTIME_PRIORITY_CLASS = 256'i32
```

### SECURITY_BUILTIN_DOMAIN_RID

[ref: #symbol-security-builtin-domain-rid]

```nim
SECURITY_BUILTIN_DOMAIN_RID = 32
```

### SECURITY_NT_AUTHORITY

[ref: #symbol-security-nt-authority]

```nim
SECURITY_NT_AUTHORITY = [0'u, 0'u, 0'u, 0'u, 0'u, 5'u]
```

### SIO_GET_EXTENSION_FUNCTION_POINTER

[ref: #symbol-sio-get-extension-function-pointer]

```nim
SIO_GET_EXTENSION_FUNCTION_POINTER = -939524090'i32
```

### SO_UPDATE_ACCEPT_CONTEXT

[ref: #symbol-so-update-accept-context]

```nim
SO_UPDATE_ACCEPT_CONTEXT = 0x0000700B
```

### STARTF_USESHOWWINDOW

[ref: #symbol-startf-useshowwindow]

```nim
STARTF_USESHOWWINDOW = 1'i32
```

### STARTF_USESTDHANDLES

[ref: #symbol-startf-usestdhandles]

```nim
STARTF_USESTDHANDLES = 256'i32
```

### STATUS_PENDING

[ref: #symbol-status-pending]

```nim
STATUS_PENDING = 0x00000103
```

### STD_ERROR_HANDLE

[ref: #symbol-std-error-handle]

```nim
STD_ERROR_HANDLE = -12'i32
```

### STD_INPUT_HANDLE

[ref: #symbol-std-input-handle]

```nim
STD_INPUT_HANDLE = -10'i32
```

### STD_OUTPUT_HANDLE

[ref: #symbol-std-output-handle]

```nim
STD_OUTPUT_HANDLE = -11'i32
```

### STILL_ACTIVE

[ref: #symbol-still-active]

```nim
STILL_ACTIVE = 0x00000103'i32
```

### SW_SHOWNORMAL

[ref: #symbol-sw-shownormal]

```nim
SW_SHOWNORMAL = 1'i32
```

### SYMLINK_FLAG_RELATIVE

[ref: #symbol-symlink-flag-relative]

```nim
SYMLINK_FLAG_RELATIVE = 0x00000001'i32
```

### SYNCHRONIZE

[ref: #symbol-synchronize]

```nim
SYNCHRONIZE = 0x00100000'i32
```

### WAIT_FAILED

[ref: #symbol-wait-failed]

```nim
WAIT_FAILED = 0xFFFFFFFF'i32
```

### WAIT_OBJECT_0

[ref: #symbol-wait-object-0]

```nim
WAIT_OBJECT_0 = 0'i32
```

### WAIT_TIMEOUT

[ref: #symbol-wait-timeout]

```nim
WAIT_TIMEOUT = 0x00000102'i32
```

### WSADESCRIPTION_LEN

[ref: #symbol-wsadescription-len]

```nim
WSADESCRIPTION_LEN = 256
```

### WSAEADDRINUSE

[ref: #symbol-wsaeaddrinuse]

```nim
WSAEADDRINUSE = 10048
```

### WSAECONNABORTED

[ref: #symbol-wsaeconnaborted]

```nim
WSAECONNABORTED = 10053
```

### WSAECONNRESET

[ref: #symbol-wsaeconnreset]

```nim
WSAECONNRESET = 10054
```

### WSAEDISCON

[ref: #symbol-wsaediscon]

```nim
WSAEDISCON = 10101
```

### WSAEINPROGRESS

[ref: #symbol-wsaeinprogress]

```nim
WSAEINPROGRESS = 10036
```

### WSAEINTR

[ref: #symbol-wsaeintr]

```nim
WSAEINTR = 10004
```

### WSAENETRESET

[ref: #symbol-wsaenetreset]

```nim
WSAENETRESET = 10052
```

### WSAENOTSOCK

[ref: #symbol-wsaenotsock]

```nim
WSAENOTSOCK = 10038
```

### WSAESHUTDOWN

[ref: #symbol-wsaeshutdown]

```nim
WSAESHUTDOWN = 10058
```

### WSAETIMEDOUT

[ref: #symbol-wsaetimedout]

```nim
WSAETIMEDOUT = 10060
```

### WSAEWOULDBLOCK

[ref: #symbol-wsaewouldblock]

```nim
WSAEWOULDBLOCK = 10035
```

### WSANOTINITIALISED

[ref: #symbol-wsanotinitialised]

```nim
WSANOTINITIALISED = 10093
```

### WSASYS_STATUS_LEN

[ref: #symbol-wsasys-status-len]

```nim
WSASYS_STATUS_LEN = 128
```

### WT_EXECUTEDEFAULT

[ref: #symbol-wt-executedefault]

```nim
WT_EXECUTEDEFAULT = 0x00000000'i32
```

### WT_EXECUTEINIOTHREAD

[ref: #symbol-wt-executeiniothread]

```nim
WT_EXECUTEINIOTHREAD = 0x00000001'i32
```

### WT_EXECUTEINPERSISTENTIOTHREAD

[ref: #symbol-wt-executeinpersistentiothread]

```nim
WT_EXECUTEINPERSISTENTIOTHREAD = 0x00000040'i32
```

### WT_EXECUTEINPERSISTENTTHREAD

[ref: #symbol-wt-executeinpersistentthread]

```nim
WT_EXECUTEINPERSISTENTTHREAD = 0x00000080'i32
```

### WT_EXECUTEINTIMERTHREAD

[ref: #symbol-wt-executeintimerthread]

```nim
WT_EXECUTEINTIMERTHREAD = 0x00000020'i32
```

### WT_EXECUTEINUITHREAD

[ref: #symbol-wt-executeinuithread]

```nim
WT_EXECUTEINUITHREAD = 0x00000002'i32
```

### WT_EXECUTEINWAITTHREAD

[ref: #symbol-wt-executeinwaitthread]

```nim
WT_EXECUTEINWAITTHREAD = 0x00000004'i32
```

### WT_EXECUTELONGFUNCTION

[ref: #symbol-wt-executelongfunction]

```nim
WT_EXECUTELONGFUNCTION = 0x00000010'i32
```

### WT_EXECUTEONLYONCE

[ref: #symbol-wt-executeonlyonce]

```nim
WT_EXECUTEONLYONCE = 0x00000008'i32
```

### WT_TRANSFER_IMPERSONATION

[ref: #symbol-wt-transfer-impersonation]

```nim
WT_TRANSFER_IMPERSONATION = 0x00000100'i32
```

## Proc

### `==`

[ref: #symbol-]

**Input:**
- `x: SocketHandle`
- `y: SocketHandle`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### accept

[ref: #symbol-accept]

**Input:**
- `s: SocketHandle`
- `a: ptr SockAddr`
- `addrlen: ptr SockLen`

**Output:** `SocketHandle`
**Pragmas:** `stdcall`, `importc: "accept"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### allocateAndInitializeSid

[ref: #symbol-allocateandinitializesid]

**Input:**
- `pIdentifierAuthority: ptr SID_IDENTIFIER_AUTHORITY`
- `nSubAuthorityCount: BYTE`
- `nSubAuthority0: DWORD`
- `nSubAuthority1: DWORD`
- `nSubAuthority2: DWORD`
- `nSubAuthority3: DWORD`
- `nSubAuthority4: DWORD`
- `nSubAuthority5: DWORD`
- `nSubAuthority6: DWORD`
- `nSubAuthority7: DWORD`
- `pSid: ptr PSID`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "Advapi32"`, `importc: "AllocateAndInitializeSid"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bindSocket

[ref: #symbol-bindsocket]

**Input:**
- `s: SocketHandle`
- `name: ptr SockAddr`
- `namelen: SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "bind"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### checkTokenMembership

[ref: #symbol-checktokenmembership]

**Input:**
- `tokenHandle: Handle`
- `sidToCheck: PSID`
- `isMember: PBOOL`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "Advapi32"`, `importc: "CheckTokenMembership"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### closeHandle

[ref: #symbol-closehandle]

**Input:**
- `hObject: Handle`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CloseHandle"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### closesocket

[ref: #symbol-closesocket]

**Input:**
- `s: SocketHandle`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "closesocket"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### connect

[ref: #symbol-connect]

**Input:**
- `s: SocketHandle`
- `name: ptr SockAddr`
- `namelen: SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "connect"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ConvertThreadToFiber

[ref: #symbol-convertthreadtofiber]

**Input:**
- `param: pointer`

**Output:** `pointer`
**Pragmas:** `stdcall`, `discardable`, `dynlib: "kernel32"`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ConvertThreadToFiberEx

[ref: #symbol-convertthreadtofiberex]

**Input:**
- `param: pointer`
- `flags: int32`

**Output:** `pointer`
**Pragmas:** `stdcall`, `discardable`, `dynlib: "kernel32"`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### copyFileW

[ref: #symbol-copyfilew]

**Input:**
- `lpExistingFileName: WideCString`
- `lpNewFileName: WideCString`
- `bFailIfExists: WINBOOL`

**Output:** `WINBOOL`
**Pragmas:** `importc: "CopyFileW"`, `stdcall`, `dynlib: "kernel32"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createDirectoryW

[ref: #symbol-createdirectoryw]

**Input:**
- `pathName: WideCString`
- `security: pointer = nil`

**Output:** `int32`
**Pragmas:** `importc: "CreateDirectoryW"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createEvent

[ref: #symbol-createevent]

**Input:**
- `lpEventAttributes: ptr SECURITY_ATTRIBUTES`
- `bManualReset: DWORD`
- `bInitialState: DWORD`
- `lpName: ptr Utf16Char`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateEventW"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CreateFiber

[ref: #symbol-createfiber]

**Input:**
- `stackSize: int`
- `fn: LPFIBER_START_ROUTINE`
- `param: pointer`

**Output:** `pointer`
**Pragmas:** `stdcall`, `discardable`, `dynlib: "kernel32"`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CreateFiberEx

[ref: #symbol-createfiberex]

**Input:**
- `stkCommit: int`
- `stkReserve: int`
- `flags: int32`
- `fn: LPFIBER_START_ROUTINE`
- `param: pointer`

**Output:** `pointer`
**Pragmas:** `stdcall`, `discardable`, `dynlib: "kernel32"`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createFileA

[ref: #symbol-createfilea]

**Input:**
- `lpFileName: cstring`
- `dwDesiredAccess: DWORD`
- `dwShareMode: DWORD`
- `lpSecurityAttributes: pointer`
- `dwCreationDisposition: DWORD`
- `dwFlagsAndAttributes: DWORD`
- `hTemplateFile: Handle`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateFileA"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createFileMappingW

[ref: #symbol-createfilemappingw]

**Input:**
- `hFile: Handle`
- `lpFileMappingAttributes: pointer`
- `flProtect: DWORD`
- `dwMaximumSizeHigh: DWORD`
- `dwMaximumSizeLow: DWORD`
- `lpName: pointer`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateFileMappingW"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createFileW

[ref: #symbol-createfilew]

**Input:**
- `lpFileName: WideCString`
- `dwDesiredAccess: DWORD`
- `dwShareMode: DWORD`
- `lpSecurityAttributes: pointer`
- `dwCreationDisposition: DWORD`
- `dwFlagsAndAttributes: DWORD`
- `hTemplateFile: Handle`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateFileW"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createHardLinkW

[ref: #symbol-createhardlinkw]

**Input:**
- `lpFileName: WideCString`
- `lpExistingFileName: WideCString`
- `security: pointer = nil`

**Output:** `int32`
**Pragmas:** `importc: "CreateHardLinkW"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createIoCompletionPort

[ref: #symbol-createiocompletionport]

**Input:**
- `FileHandle: Handle`
- `ExistingCompletionPort: Handle`
- `CompletionKey: ULONG_PTR`
- `NumberOfConcurrentThreads: DWORD`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateIoCompletionPort"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createNamedPipe

[ref: #symbol-createnamedpipe]

**Input:**
- `lpName: WideCString`
- `dwOpenMode: int32`
- `dwPipeMode: int32`
- `nMaxInstances: int32`
- `nOutBufferSize: int32`
- `nInBufferSize: int32`
- `nDefaultTimeOut: int32`
- `lpSecurityAttributes: ptr SECURITY_ATTRIBUTES`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateNamedPipeW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createPipe

[ref: #symbol-createpipe]

**Input:**
- `hReadPipe: var Handle`
- `hWritePipe: var Handle`
- `lpPipeAttributes: var SECURITY_ATTRIBUTES`
- `nSize: int32`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreatePipe"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createProcessW

[ref: #symbol-createprocessw]

**Input:**
- `lpApplicationName: WideCString`
- `lpCommandLine: WideCString`
- `lpProcessAttributes: ptr SECURITY_ATTRIBUTES`
- `lpThreadAttributes: ptr SECURITY_ATTRIBUTES`
- `bInheritHandles: WINBOOL`
- `dwCreationFlags: int32`
- `lpEnvironment: WideCString`
- `lpCurrentDirectory: WideCString`
- `lpStartupInfo: var STARTUPINFO`
- `lpProcessInformation: var PROCESS_INFORMATION`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "CreateProcessW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createSymbolicLinkW

[ref: #symbol-createsymboliclinkw]

**Input:**
- `lpSymlinkFileName: WideCString`
- `lpTargetFileName: WideCString`
- `flags: DWORD`

**Output:** `int32`
**Pragmas:** `importc: "CreateSymbolicLinkW"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### DeleteFiber

[ref: #symbol-deletefiber]

**Input:**
- `fiber: pointer`

**Output:** *(none)*
**Pragmas:** `stdcall`, `discardable`, `dynlib: "kernel32"`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### deleteFileA

[ref: #symbol-deletefilea]

**Input:**
- `pathName: cstring`

**Output:** `int32`
**Pragmas:** `importc: "DeleteFileA"`, `dynlib: "kernel32"`, `stdcall`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### deleteFileW

[ref: #symbol-deletefilew]

**Input:**
- `pathName: WideCString`

**Output:** `int32`
**Pragmas:** `importc: "DeleteFileW"`, `dynlib: "kernel32"`, `stdcall`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### deviceIoControl

[ref: #symbol-deviceiocontrol]

**Input:**
- `hDevice: Handle`
- `dwIoControlCode: DWORD`
- `lpInBuffer: pointer`
- `nInBufferSize: DWORD`
- `lpOutBuffer: pointer`
- `nOutBufferSize: DWORD`
- `lpBytesReturned: var DWORD`
- `lpOverlapped: pointer`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "DeviceIoControl"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### duplicateHandle

[ref: #symbol-duplicatehandle]

**Input:**
- `hSourceProcessHandle: Handle`
- `hSourceHandle: Handle`
- `hTargetProcessHandle: Handle`
- `lpTargetHandle: ptr Handle`
- `dwDesiredAccess: DWORD`
- `bInheritHandle: WINBOOL`
- `dwOptions: DWORD`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "DuplicateHandle"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_ISSET

[ref: #symbol-fd-isset]

**Input:**
- `socket: SocketHandle`
- `set: var TFdSet`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_SET

[ref: #symbol-fd-set]

**Input:**
- `socket: SocketHandle`
- `s: var TFdSet`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_ZERO

[ref: #symbol-fd-zero]

**Input:**
- `s: var TFdSet`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### findClose

[ref: #symbol-findclose]

**Input:**
- `hFindFile: Handle`

**Output:** *(none)*
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "FindClose"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### findFirstFileW

[ref: #symbol-findfirstfilew]

**Input:**
- `lpFileName: WideCString`
- `lpFindFileData: var WIN32_FIND_DATA`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "FindFirstFileW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### findNextFileW

[ref: #symbol-findnextfilew]

**Input:**
- `hFindFile: Handle`
- `lpFindFileData: var WIN32_FIND_DATA`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "FindNextFileW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### flushFileBuffers

[ref: #symbol-flushfilebuffers]

**Input:**
- `hFile: Handle`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "FlushFileBuffers"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### flushViewOfFile

[ref: #symbol-flushviewoffile]

**Input:**
- `lpBaseAddress: pointer`
- `dwNumberOfBytesToFlush: DWORD`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "FlushViewOfFile"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### formatMessageW

[ref: #symbol-formatmessagew]

**Input:**
- `dwFlags: int32`
- `lpSource: pointer`
- `dwMessageId: int32`
- `dwLanguageId: int32`
- `lpBuffer: pointer`
- `nSize: int32`
- `arguments: pointer`

**Output:** `int32`
**Pragmas:** `importc: "FormatMessageW"`, `stdcall`, `dynlib: "kernel32"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### freeAddrInfo

[ref: #symbol-freeaddrinfo]

**Input:**
- `ai: ptr AddrInfo`

**Output:** *(none)*
**Pragmas:** `stdcall`, `importc: "freeaddrinfo"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### freeEnvironmentStringsW

[ref: #symbol-freeenvironmentstringsw]

**Input:**
- `para1: WideCString`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "FreeEnvironmentStringsW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### freeSid

[ref: #symbol-freesid]

**Input:**
- `pSid: PSID`

**Output:** `PSID`
**Pragmas:** `stdcall`, `dynlib: "Advapi32"`, `importc: "FreeSid"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### get_osfhandle

[ref: #symbol-get-osfhandle]

**Input:**
- `fd: cint`

**Output:** `Handle`
**Pragmas:** `importc: "_get_osfhandle"`, `header: "<io.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getaddrinfo

[ref: #symbol-getaddrinfo]

**Input:**
- `nodename: cstring`
- `servname: cstring`
- `hints: ptr AddrInfo`
- `res: var ptr AddrInfo`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "getaddrinfo"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getCommandLineW

[ref: #symbol-getcommandlinew]

**Input:**
- *(none)*

**Output:** `WideCString`
**Pragmas:** `importc: "GetCommandLineW"`, `stdcall`, `dynlib: "kernel32"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](winlean_1.md) | [Next](winlean_3.md)
