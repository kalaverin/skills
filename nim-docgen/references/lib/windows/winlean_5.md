---
source_hash: 319d53cfc1304803
source_path: lib/windows/winlean.nim
---

### SO_USELOOPBACK

[ref: #symbol-so-useloopback]

```nim
SO_USELOOPBACK {.importc, header: "winsock2.h".}: cint
```

### SOL_SOCKET

[ref: #symbol-sol-socket]

```nim
SOL_SOCKET {.importc, header: "winsock2.h".}: cint
```

### SOMAXCONN

[ref: #symbol-somaxconn]

```nim
SOMAXCONN {.importc, header: "winsock2.h".}: cint
```

### TCP_NODELAY

[ref: #symbol-tcp-nodelay]

```nim
TCP_NODELAY {.importc, header: "winsock2.h".}: cint
```

### WSAID_ACCEPTEX

[ref: #symbol-wsaid-acceptex]

```nim
WSAID_ACCEPTEX: GUID = GUID(D1: 0xB5367DF1'i32, D2: 0xCBAC'i16, D3: 0x000011CF, D4: [
    0x95'i8, 0xCA'i8, 0x00'i8, 0x80'i8, 0x5F'i8, 0x48'i8, 0xA1'i8, 0x92'i8])
```

### WSAID_CONNECTEX

[ref: #symbol-wsaid-connectex]

```nim
WSAID_CONNECTEX: GUID = GUID(D1: 0x25A207B9, D2: 0xDDF3'i16, D3: 0x00004660, D4: [
    0x8E'i8, 0xE9'i8, 0x76'i8, 0xE5'i8, 0x8C'i8, 0x74'i8, 0x06'i8, 0x3E'i8])
```

### WSAID_GETACCEPTEXSOCKADDRS

[ref: #symbol-wsaid-getacceptexsockaddrs]

```nim
WSAID_GETACCEPTEXSOCKADDRS: GUID = GUID(D1: 0xB5367DF2'i32, D2: 0xCBAC'i16,
                                        D3: 0x000011CF, D4: [0x95'i8, 0xCA'i8,
    0x00'i8, 0x80'i8, 0x5F'i8, 0x48'i8, 0xA1'i8, 0x92'i8])
```

[Prev](winlean_4.md)
