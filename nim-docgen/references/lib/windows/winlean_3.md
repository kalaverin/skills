---
source_hash: 319d53cfc1304803
source_path: lib/windows/winlean.nim
---

### getCurrentDirectoryW

[ref: #symbol-getcurrentdirectoryw]

**Input:**
- `nBufferLength: int32`
- `lpBuffer: WideCString`

**Output:** `int32`
**Pragmas:** `importc: "GetCurrentDirectoryW"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### GetCurrentFiber

[ref: #symbol-getcurrentfiber]

**Input:**
- *(none)*

**Output:** `pointer`
**Pragmas:** `stdcall`, `importc`, `header: "windows.h"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getCurrentProcess

[ref: #symbol-getcurrentprocess]

**Input:**
- *(none)*

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetCurrentProcess"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getEnvironmentStringsW

[ref: #symbol-getenvironmentstringsw]

**Input:**
- *(none)*

**Output:** `WideCString`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetEnvironmentStringsW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getExitCodeProcess

[ref: #symbol-getexitcodeprocess]

**Input:**
- `hProcess: Handle`
- `lpExitCode: var int32`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetExitCodeProcess"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFileAttributesW

[ref: #symbol-getfileattributesw]

**Input:**
- `lpFileName: WideCString`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetFileAttributesW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFileInformationByHandle

[ref: #symbol-getfileinformationbyhandle]

**Input:**
- `hFile: Handle`
- `lpFileInformation: ptr BY_HANDLE_FILE_INFORMATION`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetFileInformationByHandle"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFileSize

[ref: #symbol-getfilesize]

**Input:**
- `hFile: Handle`
- `lpFileSizeHigh: ptr DWORD`

**Output:** `DWORD`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetFileSize"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFullPathNameW

[ref: #symbol-getfullpathnamew]

**Input:**
- `lpFileName: WideCString`
- `nBufferLength: int32`
- `lpBuffer: WideCString`
- `lpFilePart: var WideCString`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetFullPathNameW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getHandleInformation

[ref: #symbol-gethandleinformation]

**Input:**
- `hObject: Handle`
- `lpdwFlags: ptr DWORD`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetHandleInformation"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostbyaddr

[ref: #symbol-gethostbyaddr]

**Input:**
- `ip: ptr InAddr`
- `len: cuint`
- `theType: cint`

**Output:** `ptr Hostent`
**Pragmas:** `stdcall`, `importc: "gethostbyaddr"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostbyname

[ref: #symbol-gethostbyname]

**Input:**
- `name: cstring`

**Output:** `ptr Hostent`
**Pragmas:** `stdcall`, `importc: "gethostbyname"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostname

[ref: #symbol-gethostname]

**Input:**
- `hostname: cstring`
- `len: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "gethostname"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getLastError

[ref: #symbol-getlasterror]

**Input:**
- *(none)*

**Output:** `int32`
**Pragmas:** `importc: "GetLastError"`, `stdcall`, `dynlib: "kernel32"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getModuleFileNameW

[ref: #symbol-getmodulefilenamew]

**Input:**
- `handle: Handle`
- `buf: WideCString`
- `size: int32`

**Output:** `int32`
**Pragmas:** `importc: "GetModuleFileNameW"`, `dynlib: "kernel32"`, `stdcall`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getnameinfo

[ref: #symbol-getnameinfo]

**Input:**
- `a1: ptr SockAddr`
- `a2: SockLen`
- `a3: cstring`
- `a4: SockLen`
- `a5: cstring`
- `a6: SockLen`
- `a7: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "getnameinfo"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getOverlappedResult

[ref: #symbol-getoverlappedresult]

**Input:**
- `hFile: Handle`
- `lpOverlapped: POVERLAPPED`
- `lpNumberOfBytesTransferred: var DWORD`
- `bWait: WINBOOL`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetOverlappedResult"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpeername

[ref: #symbol-getpeername]

**Input:**
- `s: SocketHandle`
- `name: ptr SockAddr`
- `namelen: ptr SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getProcessTimes

[ref: #symbol-getprocesstimes]

**Input:**
- `hProcess: Handle`
- `lpCreationTime: var FILETIME`
- `lpExitTime: var FILETIME`
- `lpKernelTime: var FILETIME`
- `lpUserTime: var FILETIME`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetProcessTimes"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getprotobyname

[ref: #symbol-getprotobyname]

**Input:**
- `name: cstring`

**Output:** `ptr Protoent`
**Pragmas:** `stdcall`, `importc: "getprotobyname"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getprotobynumber

[ref: #symbol-getprotobynumber]

**Input:**
- `proto: cint`

**Output:** `ptr Protoent`
**Pragmas:** `stdcall`, `importc: "getprotobynumber"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getQueuedCompletionStatus

[ref: #symbol-getqueuedcompletionstatus]

**Input:**
- `CompletionPort: Handle`
- `lpNumberOfBytesTransferred: PDWORD`
- `lpCompletionKey: PULONG_PTR`
- `lpOverlapped: ptr POVERLAPPED`
- `dwMilliseconds: DWORD`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetQueuedCompletionStatus"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getservbyname

[ref: #symbol-getservbyname]

**Input:**
- `name: cstring`
- `proto: cstring`

**Output:** `ptr Servent`
**Pragmas:** `stdcall`, `importc: "getservbyname"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getservbyport

[ref: #symbol-getservbyport]

**Input:**
- `port: cint`
- `proto: cstring`

**Output:** `ptr Servent`
**Pragmas:** `stdcall`, `importc: "getservbyport"`, `dynlib: ws2dll`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getsockname

[ref: #symbol-getsockname]

**Input:**
- `s: SocketHandle`
- `name: ptr SockAddr`
- `namelen: ptr SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "getsockname"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getsockopt

[ref: #symbol-getsockopt]

**Input:**
- `s: SocketHandle`
- `level: cint`
- `optname: cint`
- `optval: pointer`
- `optlen: ptr SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "getsockopt"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getStdHandle

[ref: #symbol-getstdhandle]

**Input:**
- `nStdHandle: int32`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetStdHandle"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getSystemTimeAsFileTime

[ref: #symbol-getsystemtimeasfiletime]

**Input:**
- `lpSystemTimeAsFileTime: var FILETIME`

**Output:** *(none)*
**Pragmas:** `importc: "GetSystemTimeAsFileTime"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getSystemTimePreciseAsFileTime

[ref: #symbol-getsystemtimepreciseasfiletime]

**Input:**
- `lpSystemTimeAsFileTime: var FILETIME`

**Output:** *(none)*
**Pragmas:** `importc: "GetSystemTimePreciseAsFileTime"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getSystemTimes

[ref: #symbol-getsystemtimes]

**Input:**
- `lpIdleTime: var FILETIME`
- `lpKernelTime: var FILETIME`
- `lpUserTime: var FILETIME`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetSystemTimes"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getVersion

[ref: #symbol-getversion]

**Input:**
- *(none)*

**Output:** `DWORD`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetVersion"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getVersionExA

[ref: #symbol-getversionexa]

**Input:**
- `lpVersionInfo: ptr OSVERSIONINFO`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetVersionExA"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getVersionExW

[ref: #symbol-getversionexw]

**Input:**
- `lpVersionInfo: ptr OSVERSIONINFO`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetVersionExW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_addr

[ref: #symbol-inet-addr]

**Input:**
- `cp: cstring`

**Output:** `uint32`
**Pragmas:** `stdcall`, `importc: "inet_addr"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_ntoa

[ref: #symbol-inet-ntoa]

**Input:**
- `i: InAddr`

**Output:** `cstring`
**Pragmas:** `stdcall`, `importc`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_ntop

[ref: #symbol-inet-ntop]

**Input:**
- `family: cint`
- `paddr: pointer`
- `pStringBuffer: cstring`
- `stringBufSize: int32`

**Output:** `cstring`
**Pragmas:** `stdcall`, `raises: [Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception`, `tags: `, `forbids: `

### isSuccess

[ref: #symbol-issuccess]

**Input:**
- `a: WINBOOL`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a != 0. Windows uses a different convention than POSIX, where a == 0 is commonly used on success.

### listen

[ref: #symbol-listen]

**Input:**
- `s: SocketHandle`
- `backlog: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "listen"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### localFree

[ref: #symbol-localfree]

**Input:**
- `p: pointer`

**Output:** *(none)*
**Pragmas:** `importc: "LocalFree"`, `stdcall`, `dynlib: "kernel32"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mapViewOfFileEx

[ref: #symbol-mapviewoffileex]

**Input:**
- `hFileMappingObject: Handle`
- `dwDesiredAccess: DWORD`
- `dwFileOffsetHigh: DWORD`
- `dwFileOffsetLow: DWORD`
- `dwNumberOfBytesToMap: WinSizeT`
- `lpBaseAddress: pointer`

**Output:** `pointer`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "MapViewOfFileEx"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### moveFileExW

[ref: #symbol-movefileexw]

**Input:**
- `lpExistingFileName: WideCString`
- `lpNewFileName: WideCString`
- `flags: DWORD`

**Output:** `WINBOOL`
**Pragmas:** `importc: "MoveFileExW"`, `stdcall`, `dynlib: "kernel32"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### moveFileW

[ref: #symbol-movefilew]

**Input:**
- `lpExistingFileName: WideCString`
- `lpNewFileName: WideCString`

**Output:** `WINBOOL`
**Pragmas:** `importc: "MoveFileW"`, `stdcall`, `dynlib: "kernel32"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### openProcess

[ref: #symbol-openprocess]

**Input:**
- `dwDesiredAccess: DWORD`
- `bInheritHandle: WINBOOL`
- `dwProcessId: DWORD`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "OpenProcess"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### peekNamedPipe

[ref: #symbol-peeknamedpipe]

**Input:**
- `hNamedPipe: Handle`
- `lpBuffer: pointer = nil`
- `nBufferSize: int32 = 0`
- `lpBytesRead: ptr int32 = nil`
- `lpTotalBytesAvail: ptr int32 = nil`
- `lpBytesLeftThisMessage: ptr int32 = nil`

**Output:** `bool`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "PeekNamedPipe"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### postQueuedCompletionStatus

[ref: #symbol-postqueuedcompletionstatus]

**Input:**
- `CompletionPort: Handle`
- `dwNumberOfBytesTransferred: DWORD`
- `dwCompletionKey: ULONG_PTR`
- `lpOverlapped: pointer`

**Output:** `bool`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "PostQueuedCompletionStatus"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rdFileSize

[ref: #symbol-rdfilesize]

**Input:**
- `f: WIN32_FIND_DATA`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rdFileTime

[ref: #symbol-rdfiletime]

**Input:**
- `f: FILETIME`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readConsoleInput

[ref: #symbol-readconsoleinput]

**Input:**
- `hConsoleInput: Handle`
- `lpBuffer: pointer`
- `nLength: cint`
- `lpNumberOfEventsRead: ptr cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "ReadConsoleInputW"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readFile

[ref: #symbol-readfile]

**Input:**
- `hFile: Handle`
- `buffer: pointer`
- `nNumberOfBytesToRead: int32`
- `lpNumberOfBytesRead: ptr int32`
- `lpOverlapped: pointer`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "ReadFile"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### recv

[ref: #symbol-recv]

**Input:**
- `s: SocketHandle`
- `buf: pointer`
- `len: cint`
- `flags: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "recv"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### recvfrom

[ref: #symbol-recvfrom]

**Input:**
- `s: SocketHandle`
- `buf: cstring`
- `len: cint`
- `flags: cint`
- `fromm: ptr SockAddr`
- `fromlen: ptr SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "recvfrom"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### registerWaitForSingleObject

[ref: #symbol-registerwaitforsingleobject]

**Input:**
- `phNewWaitObject: ptr Handle`
- `hObject: Handle`
- `Callback: WAITORTIMERCALLBACK`
- `Context: pointer`
- `dwMilliseconds: ULONG`
- `dwFlags: ULONG`

**Output:** `bool`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "RegisterWaitForSingleObject"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeDirectoryW

[ref: #symbol-removedirectoryw]

**Input:**
- `lpPathName: WideCString`

**Output:** `int32`
**Pragmas:** `importc: "RemoveDirectoryW"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### resumeThread

[ref: #symbol-resumethread]

**Input:**
- `hThread: Handle`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "ResumeThread"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### select

[ref: #symbol-select]

**Input:**
- `nfds: cint`
- `readfds: ptr TFdSet`
- `writefds: ptr TFdSet`
- `exceptfds: ptr TFdSet`
- `timeout: ptr Timeval`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "select"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### send

[ref: #symbol-send]

**Input:**
- `s: SocketHandle`
- `buf: pointer`
- `len: cint`
- `flags: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "send"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sendto

[ref: #symbol-sendto]

**Input:**
- `s: SocketHandle`
- `buf: pointer`
- `len: cint`
- `flags: cint`
- `to: ptr SockAddr`
- `tolen: SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "sendto"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setCurrentDirectoryW

[ref: #symbol-setcurrentdirectoryw]

**Input:**
- `lpPathName: WideCString`

**Output:** `int32`
**Pragmas:** `importc: "SetCurrentDirectoryW"`, `dynlib: "kernel32"`, `stdcall`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setEndOfFile

[ref: #symbol-setendoffile]

**Input:**
- `hFile: Handle`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetEndOfFile"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setEnvironmentVariableW

[ref: #symbol-setenvironmentvariablew]

**Input:**
- `lpName: WideCString`
- `lpValue: WideCString`

**Output:** `int32`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetEnvironmentVariableW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setEvent

[ref: #symbol-setevent]

**Input:**
- `hEvent: Handle`

**Output:** `cint`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetEvent"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setFileAttributesW

[ref: #symbol-setfileattributesw]

**Input:**
- `lpFileName: WideCString`
- `dwFileAttributes: int32`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetFileAttributesW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setFilePointer

[ref: #symbol-setfilepointer]

**Input:**
- `hFile: Handle`
- `lDistanceToMove: LONG`
- `lpDistanceToMoveHigh: ptr LONG`
- `dwMoveMethod: DWORD`

**Output:** `DWORD`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetFilePointer"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setFileTime

[ref: #symbol-setfiletime]

**Input:**
- `hFile: Handle`
- `lpCreationTime: LPFILETIME`
- `lpLastAccessTime: LPFILETIME`
- `lpLastWriteTime: LPFILETIME`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetFileTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setHandleInformation

[ref: #symbol-sethandleinformation]

**Input:**
- `hObject: Handle`
- `dwMask: DWORD`
- `dwFlags: DWORD`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetHandleInformation"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setLastError

[ref: #symbol-setlasterror]

**Input:**
- `error: int32`

**Output:** *(none)*
**Pragmas:** `importc: "SetLastError"`, `stdcall`, `dynlib: "kernel32"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setsockopt

[ref: #symbol-setsockopt]

**Input:**
- `s: SocketHandle`
- `level: cint`
- `optname: cint`
- `optval: pointer`
- `optlen: SockLen`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "setsockopt"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setStdHandle

[ref: #symbol-setstdhandle]

**Input:**
- `nStdHandle: int32`
- `hHandle: Handle`

**Output:** `WINBOOL`
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "SetStdHandle"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### shellExecuteW

[ref: #symbol-shellexecutew]

**Input:**
- `hwnd: Handle`
- `lpOperation: WideCString`
- `lpFile: WideCString`
- `lpParameters: WideCString`
- `lpDirectory: WideCString`
- `nShowCmd: int32`

**Output:** `Handle`
**Pragmas:** `stdcall`, `dynlib: "shell32.dll"`, `importc: "ShellExecuteW"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### shutdown

[ref: #symbol-shutdown]

**Input:**
- `s: SocketHandle`
- `how: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `importc: "shutdown"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sleep

[ref: #symbol-sleep]

**Input:**
- `dwMilliseconds: int32`

**Output:** *(none)*
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "Sleep"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### socket

[ref: #symbol-socket]

**Input:**
- `af: cint`
- `typ: cint`
- `protocol: cint`

**Output:** `SocketHandle`
**Pragmas:** `stdcall`, `importc: "socket"`, `dynlib: ws2dll`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](winlean_2.md) | [Next](winlean_4.md)
