---
source_hash: 30126b07c38d2f7b
source_path: lib/posix/termios.nim
---

# termios

[ref: #module-termios]

## Const

### NCCS

[ref: #symbol-nccs]

```nim
NCCS = 20
```

## Proc

### cfGetIspeed

[ref: #symbol-cfgetispeed]

**Input:**
- `termios: ptr Termios`

**Output:** `Speed`
**Pragmas:** `importc: "cfgetispeed"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cfGetOspeed

[ref: #symbol-cfgetospeed]

**Input:**
- `termios: ptr Termios`

**Output:** `Speed`
**Pragmas:** `importc: "cfgetospeed"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cfSetIspeed

[ref: #symbol-cfsetispeed]

**Input:**
- `termios: ptr Termios`
- `speed: Speed`

**Output:** `cint`
**Pragmas:** `importc: "cfsetispeed"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cfSetOspeed

[ref: #symbol-cfsetospeed]

**Input:**
- `termios: ptr Termios`
- `speed: Speed`

**Output:** `cint`
**Pragmas:** `importc: "cfsetospeed"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ioctl

[ref: #symbol-ioctl]

**Input:**
- `fd: cint`
- `request: culong`
- `reply: ptr IOctl_WinSize`

**Output:** `int`
**Pragmas:** `importc: "ioctl"`, `header: "<stdio.h>"`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcDrain

[ref: #symbol-tcdrain]

**Input:**
- `fd: cint`

**Output:** `cint`
**Pragmas:** `importc: "tcdrain"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcFlow

[ref: #symbol-tcflow]

**Input:**
- `fd: cint`
- `action: cint`

**Output:** `cint`
**Pragmas:** `importc: "tcflow"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcFlush

[ref: #symbol-tcflush]

**Input:**
- `fd: cint`
- `queue_selector: cint`

**Output:** `cint`
**Pragmas:** `importc: "tcflush"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcGetAttr

[ref: #symbol-tcgetattr]

**Input:**
- `fd: cint`
- `termios: ptr Termios`

**Output:** `cint`
**Pragmas:** `importc: "tcgetattr"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcSendBreak

[ref: #symbol-tcsendbreak]

**Input:**
- `fd: cint`
- `duration: cint`

**Output:** `cint`
**Pragmas:** `importc: "tcsendbreak"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcSetAttr

[ref: #symbol-tcsetattr]

**Input:**
- `fd: cint`
- `optional_actions: cint`
- `termios: ptr Termios`

**Output:** `cint`
**Pragmas:** `importc: "tcsetattr"`, `header: "<termios.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### cceq

[ref: #symbol-cceq]

**Input:**
- `val: `
- `c: `

**Output:** `untyped`
## Type

### Cflag

[ref: #symbol-cflag]

```nim
Cflag = cuint
```

### IOctl_WinSize

[ref: #symbol-ioctl-winsize]

```nim
IOctl_WinSize = object
  ws_row*, ws_col*, ws_xpixel*, ws_ypixel*: cushort
```

### Speed

[ref: #symbol-speed]

```nim
Speed = cuint
```

### Termios

[ref: #symbol-termios]

```nim
Termios {.importc: "struct termios", header: "<termios.h>".} = object
  c_iflag*: Cflag
  c_oflag*: Cflag
  c_cflag*: Cflag
  c_lflag*: Cflag
  c_cc*: array[NCCS, cuchar]
```

## Var

### B0

[ref: #symbol-b0]

```nim
B0 {.importc, header: "<termios.h>".}: Speed
```

### B1000000

[ref: #symbol-b1000000]

```nim
B1000000 {.importc, header: "<termios.h>".}: Speed
```

### B110

[ref: #symbol-b110]

```nim
B110 {.importc, header: "<termios.h>".}: Speed
```

### B115200

[ref: #symbol-b115200]

```nim
B115200 {.importc, header: "<termios.h>".}: Speed
```

### B1152000

[ref: #symbol-b1152000]

```nim
B1152000 {.importc, header: "<termios.h>".}: Speed
```

### B1200

[ref: #symbol-b1200]

```nim
B1200 {.importc, header: "<termios.h>".}: Speed
```

### B134

[ref: #symbol-b134]

```nim
B134 {.importc, header: "<termios.h>".}: Speed
```

### B150

[ref: #symbol-b150]

```nim
B150 {.importc, header: "<termios.h>".}: Speed
```

### B1500000

[ref: #symbol-b1500000]

```nim
B1500000 {.importc, header: "<termios.h>".}: Speed
```

### B1800

[ref: #symbol-b1800]

```nim
B1800 {.importc, header: "<termios.h>".}: Speed
```

### B19200

[ref: #symbol-b19200]

```nim
B19200 {.importc, header: "<termios.h>".}: Speed
```

### B200

[ref: #symbol-b200]

```nim
B200 {.importc, header: "<termios.h>".}: Speed
```

### B2000000

[ref: #symbol-b2000000]

```nim
B2000000 {.importc, header: "<termios.h>".}: Speed
```

### B230400

[ref: #symbol-b230400]

```nim
B230400 {.importc, header: "<termios.h>".}: Speed
```

### B2400

[ref: #symbol-b2400]

```nim
B2400 {.importc, header: "<termios.h>".}: Speed
```

### B2500000

[ref: #symbol-b2500000]

```nim
B2500000 {.importc, header: "<termios.h>".}: Speed
```

### B300

[ref: #symbol-b300]

```nim
B300 {.importc, header: "<termios.h>".}: Speed
```

### B3000000

[ref: #symbol-b3000000]

```nim
B3000000 {.importc, header: "<termios.h>".}: Speed
```

### B3500000

[ref: #symbol-b3500000]

```nim
B3500000 {.importc, header: "<termios.h>".}: Speed
```

### B38400

[ref: #symbol-b38400]

```nim
B38400 {.importc, header: "<termios.h>".}: Speed
```

### B4000000

[ref: #symbol-b4000000]

```nim
B4000000 {.importc, header: "<termios.h>".}: Speed
```

### B460800

[ref: #symbol-b460800]

```nim
B460800 {.importc, header: "<termios.h>".}: Speed
```

### B4800

[ref: #symbol-b4800]

```nim
B4800 {.importc, header: "<termios.h>".}: Speed
```

### B50

[ref: #symbol-b50]

```nim
B50 {.importc, header: "<termios.h>".}: Speed
```

### B500000

[ref: #symbol-b500000]

```nim
B500000 {.importc, header: "<termios.h>".}: Speed
```

### B57600

[ref: #symbol-b57600]

```nim
B57600 {.importc, header: "<termios.h>".}: Speed
```

### B576000

[ref: #symbol-b576000]

```nim
B576000 {.importc, header: "<termios.h>".}: Speed
```

### B600

[ref: #symbol-b600]

```nim
B600 {.importc, header: "<termios.h>".}: Speed
```

### B75

[ref: #symbol-b75]

```nim
B75 {.importc, header: "<termios.h>".}: Speed
```

### B921600

[ref: #symbol-b921600]

```nim
B921600 {.importc, header: "<termios.h>".}: Speed
```

### B9600

[ref: #symbol-b9600]

```nim
B9600 {.importc, header: "<termios.h>".}: Speed
```

### BRKINT

[ref: #symbol-brkint]

```nim
BRKINT {.importc, header: "<termios.h>".}: Cflag
```

### BS0

[ref: #symbol-bs0]

```nim
BS0 {.importc, header: "<termios.h>".}: Cflag
```

### BS1

[ref: #symbol-bs1]

```nim
BS1 {.importc, header: "<termios.h>".}: Cflag
```

### BSDLY

[ref: #symbol-bsdly]

```nim
BSDLY {.importc, header: "<termios.h>".}: Cflag
```

### CLOCAL

[ref: #symbol-clocal]

```nim
CLOCAL {.importc, header: "<termios.h>".}: Cflag
```

### CR0

[ref: #symbol-cr0]

```nim
CR0 {.importc, header: "<termios.h>".}: Cflag
```

### CR1

[ref: #symbol-cr1]

```nim
CR1 {.importc, header: "<termios.h>".}: Cflag
```

### CR2

[ref: #symbol-cr2]

```nim
CR2 {.importc, header: "<termios.h>".}: Cflag
```

### CR3

[ref: #symbol-cr3]

```nim
CR3 {.importc, header: "<termios.h>".}: Cflag
```

### CRDLY

[ref: #symbol-crdly]

```nim
CRDLY {.importc, header: "<termios.h>".}: Cflag
```

### CREAD

[ref: #symbol-cread]

```nim
CREAD {.importc, header: "<termios.h>".}: Cflag
```

### CS5

[ref: #symbol-cs5]

```nim
CS5 {.importc, header: "<termios.h>".}: Cflag
```

### CS6

[ref: #symbol-cs6]

```nim
CS6 {.importc, header: "<termios.h>".}: Cflag
```

### CS7

[ref: #symbol-cs7]

```nim
CS7 {.importc, header: "<termios.h>".}: Cflag
```

### CS8

[ref: #symbol-cs8]

```nim
CS8 {.importc, header: "<termios.h>".}: Cflag
```

### CSIZE

[ref: #symbol-csize]

```nim
CSIZE {.importc, header: "<termios.h>".}: Cflag
```

### CSTOPB

[ref: #symbol-cstopb]

```nim
CSTOPB {.importc, header: "<termios.h>".}: Cflag
```

### ECHO

[ref: #symbol-echo]

```nim
ECHO {.importc, header: "<termios.h>".}: Cflag
```

### ECHOE

[ref: #symbol-echoe]

```nim
ECHOE {.importc, header: "<termios.h>".}: Cflag
```

### ECHOK

[ref: #symbol-echok]

```nim
ECHOK {.importc, header: "<termios.h>".}: Cflag
```

### ECHONL

[ref: #symbol-echonl]

```nim
ECHONL {.importc, header: "<termios.h>".}: Cflag
```

### EXTA

[ref: #symbol-exta]

```nim
EXTA {.importc, header: "<termios.h>".}: Speed
```

### EXTB

[ref: #symbol-extb]

```nim
EXTB {.importc, header: "<termios.h>".}: Speed
```

### FF0

[ref: #symbol-ff0]

```nim
FF0 {.importc, header: "<termios.h>".}: Cflag
```

### FF1

[ref: #symbol-ff1]

```nim
FF1 {.importc, header: "<termios.h>".}: Cflag
```

### FFDLY

[ref: #symbol-ffdly]

```nim
FFDLY {.importc, header: "<termios.h>".}: Cflag
```

### HUPCL

[ref: #symbol-hupcl]

```nim
HUPCL {.importc, header: "<termios.h>".}: Cflag
```

### ICANON

[ref: #symbol-icanon]

```nim
ICANON {.importc, header: "<termios.h>".}: Cflag
```

### ICRNL

[ref: #symbol-icrnl]

```nim
ICRNL {.importc, header: "<termios.h>".}: Cflag
```

### IEXTEN

[ref: #symbol-iexten]

```nim
IEXTEN {.importc, header: "<termios.h>".}: Cflag
```

### IGNBRK

[ref: #symbol-ignbrk]

```nim
IGNBRK {.importc, header: "<termios.h>".}: Cflag
```

### IGNCR

[ref: #symbol-igncr]

```nim
IGNCR {.importc, header: "<termios.h>".}: Cflag
```

### IGNPAR

[ref: #symbol-ignpar]

```nim
IGNPAR {.importc, header: "<termios.h>".}: Cflag
```

### INLCR

[ref: #symbol-inlcr]

```nim
INLCR {.importc, header: "<termios.h>".}: Cflag
```

### INPCK

[ref: #symbol-inpck]

```nim
INPCK {.importc, header: "<termios.h>".}: Cflag
```

### ISIG

[ref: #symbol-isig]

```nim
ISIG {.importc, header: "<termios.h>".}: Cflag
```

### ISTRIP

[ref: #symbol-istrip]

```nim
ISTRIP {.importc, header: "<termios.h>".}: Cflag
```

### IUCLC

[ref: #symbol-iuclc]

```nim
IUCLC {.importc, header: "<termios.h>".}: Cflag
```

### IXANY

[ref: #symbol-ixany]

```nim
IXANY {.importc, header: "<termios.h>".}: Cflag
```

### IXOFF

[ref: #symbol-ixoff]

```nim
IXOFF {.importc, header: "<termios.h>".}: Cflag
```

### IXON

[ref: #symbol-ixon]

```nim
IXON {.importc, header: "<termios.h>".}: Cflag
```

### NL0

[ref: #symbol-nl0]

```nim
NL0 {.importc, header: "<termios.h>".}: Cflag
```

### NL1

[ref: #symbol-nl1]

```nim
NL1 {.importc, header: "<termios.h>".}: Cflag
```

### NLDLY

[ref: #symbol-nldly]

```nim
NLDLY {.importc, header: "<termios.h>".}: Cflag
```

### NOFLSH

[ref: #symbol-noflsh]

```nim
NOFLSH {.importc, header: "<termios.h>".}: Cflag
```

### OCRNL

[ref: #symbol-ocrnl]

```nim
OCRNL {.importc, header: "<termios.h>".}: Cflag
```

### OFDEL

[ref: #symbol-ofdel]

```nim
OFDEL {.importc, header: "<termios.h>".}: Cflag
```

### OFILL

[ref: #symbol-ofill]

```nim
OFILL {.importc, header: "<termios.h>".}: Cflag
```

### ONLCR

[ref: #symbol-onlcr]

```nim
ONLCR {.importc, header: "<termios.h>".}: Cflag
```

### ONLRET

[ref: #symbol-onlret]

```nim
ONLRET {.importc, header: "<termios.h>".}: Cflag
```

### ONOCR

[ref: #symbol-onocr]

```nim
ONOCR {.importc, header: "<termios.h>".}: Cflag
```

### OPOST

[ref: #symbol-opost]

```nim
OPOST {.importc, header: "<termios.h>".}: Cflag
```

### PARENB

[ref: #symbol-parenb]

```nim
PARENB {.importc, header: "<termios.h>".}: Cflag
```

### PARMRK

[ref: #symbol-parmrk]

```nim
PARMRK {.importc, header: "<termios.h>".}: Cflag
```

### PARODD

[ref: #symbol-parodd]

```nim
PARODD {.importc, header: "<termios.h>".}: Cflag
```

### TAB0

[ref: #symbol-tab0]

```nim
TAB0 {.importc, header: "<termios.h>".}: Cflag
```

### TAB1

[ref: #symbol-tab1]

```nim
TAB1 {.importc, header: "<termios.h>".}: Cflag
```

### TAB2

[ref: #symbol-tab2]

```nim
TAB2 {.importc, header: "<termios.h>".}: Cflag
```

### TAB3

[ref: #symbol-tab3]

```nim
TAB3 {.importc, header: "<termios.h>".}: Cflag
```

### TABDLY

[ref: #symbol-tabdly]

```nim
TABDLY {.importc, header: "<termios.h>".}: Cflag
```

### TCIFLUSH

[ref: #symbol-tciflush]

```nim
TCIFLUSH {.importc, header: "<termios.h>".}: cint
```

### TCIOFF

[ref: #symbol-tcioff]

```nim
TCIOFF {.importc, header: "<termios.h>".}: cint
```

### TCIOFLUSH

[ref: #symbol-tcioflush]

```nim
TCIOFLUSH {.importc, header: "<termios.h>".}: cint
```

### TCION

[ref: #symbol-tcion]

```nim
TCION {.importc, header: "<termios.h>".}: cint
```

### TCOFLUSH

[ref: #symbol-tcoflush]

```nim
TCOFLUSH {.importc, header: "<termios.h>".}: cint
```

### TCOOFF

[ref: #symbol-tcooff]

```nim
TCOOFF {.importc, header: "<termios.h>".}: cint
```


[Next](termios_2.md)
