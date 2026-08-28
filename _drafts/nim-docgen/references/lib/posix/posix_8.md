---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### Lconv

[ref: #symbol-lconv]

```nim
Lconv {.importc: "struct lconv", header: "<locale.h>", final, pure.} = object
  currency_symbol*: cstring
  decimal_point*: cstring
  frac_digits*: char
  grouping*: cstring
  int_curr_symbol*: cstring
  int_frac_digits*: char
  int_n_cs_precedes*: char
  int_n_sep_by_space*: char
  int_n_sign_posn*: char
  int_p_cs_precedes*: char
  int_p_sep_by_space*: char
  int_p_sign_posn*: char
  mon_decimal_point*: cstring
  mon_grouping*: cstring
  mon_thousands_sep*: cstring
  negative_sign*: cstring
  n_cs_precedes*: char
  n_sep_by_space*: char
  n_sign_posn*: char
  positive_sign*: cstring
  p_cs_precedes*: char
  p_sep_by_space*: char
  p_sign_posn*: char
  thousands_sep*: cstring
```

### Mcontext

[ref: #symbol-mcontext]

```nim
Mcontext {.importc: "mcontext_t", header: "<ucontext.h>", final, pure.} = object
```

### Mode

[ref: #symbol-mode]

```nim
Mode {.importc: "mode_t", header: "<sys/types.h>".} = (when false or false:
  uint32
 else:
  uint16)
```

### Nl_catd

[ref: #symbol-nl-catd]

```nim
Nl_catd {.importc: "nl_catd", header: "<nl_types.h>".} = cint
```

### Nl_item

[ref: #symbol-nl-item]

```nim
Nl_item {.importc: "nl_item", header: "<nl_types.h>".} = cint
```

### Nlink

[ref: #symbol-nlink]

```nim
Nlink {.importc: "nlink_t", header: "<sys/types.h>".} = uint16
```

### Off

[ref: #symbol-off]

```nim
Off {.importc: "off_t", header: "<sys/types.h>".} = int64
```

### Passwd

[ref: #symbol-passwd]

```nim
Passwd {.importc: "struct passwd", header: "<pwd.h>", final, pure.} = object
  pw_name*: cstring          ## User's login name.
  pw_uid*: Uid               ## Numerical user ID.
  pw_gid*: Gid               ## Numerical group ID.
  pw_dir*: cstring           ## Initial working directory.
  pw_shell*: cstring         ## Program to use as shell.
```

struct passwd

### Pid

[ref: #symbol-pid]

```nim
Pid {.importc: "pid_t", header: "<sys/types.h>".} = int32
```

### Posix_typed_mem_info

[ref: #symbol-posix-typed-mem-info]

```nim
Posix_typed_mem_info {.importc: "struct posix_typed_mem_info",
                       header: "<sys/mman.h>", final, pure.} = object
  posix_tmi_length*: int
```

### Protoent

[ref: #symbol-protoent]

```nim
Protoent {.importc: "struct protoent", pure, final, header: "<netdb.h>".} = object
  p_name*: cstring           ## Official name of the protocol.
  p_aliases*: cstringArray   ## A pointer to an array of pointers to
                             ## alternative protocol names, terminated by
                             ## a null pointer.
  p_proto*: cint             ## The protocol number.
```

struct protoent

### Pthread

[ref: #symbol-pthread]

```nim
Pthread {.importc: "pthread_t", header: "<sys/types.h>".} = int
```

### Pthread_attr

[ref: #symbol-pthread-attr]

```nim
Pthread_attr {.importc: "pthread_attr_t", header: "<sys/types.h>".} = int
```

### Pthread_barrier

[ref: #symbol-pthread-barrier]

```nim
Pthread_barrier {.importc: "pthread_barrier_t", header: "<sys/types.h>".} = int
```

### Pthread_barrierattr

[ref: #symbol-pthread-barrierattr]

```nim
Pthread_barrierattr {.importc: "pthread_barrierattr_t", header: "<sys/types.h>".} = int
```

### Pthread_cond

[ref: #symbol-pthread-cond]

```nim
Pthread_cond {.importc: "pthread_cond_t", header: "<sys/types.h>".} = int
```

### Pthread_condattr

[ref: #symbol-pthread-condattr]

```nim
Pthread_condattr {.importc: "pthread_condattr_t", header: "<sys/types.h>".} = int
```

### Pthread_key

[ref: #symbol-pthread-key]

```nim
Pthread_key {.importc: "pthread_key_t", header: "<sys/types.h>".} = int
```

### Pthread_mutex

[ref: #symbol-pthread-mutex]

```nim
Pthread_mutex {.importc: "pthread_mutex_t", header: "<sys/types.h>".} = int
```

### Pthread_mutexattr

[ref: #symbol-pthread-mutexattr]

```nim
Pthread_mutexattr {.importc: "pthread_mutexattr_t", header: "<sys/types.h>".} = int
```

### Pthread_once

[ref: #symbol-pthread-once]

```nim
Pthread_once {.importc: "pthread_once_t", header: "<sys/types.h>".} = int
```

### Pthread_rwlock

[ref: #symbol-pthread-rwlock]

```nim
Pthread_rwlock {.importc: "pthread_rwlock_t", header: "<sys/types.h>".} = int
```

### Pthread_rwlockattr

[ref: #symbol-pthread-rwlockattr]

```nim
Pthread_rwlockattr {.importc: "pthread_rwlockattr_t", header: "<sys/types.h>".} = int
```

### Pthread_spinlock

[ref: #symbol-pthread-spinlock]

```nim
Pthread_spinlock {.importc: "pthread_spinlock_t", header: "<sys/types.h>".} = int
```

### RLimit

[ref: #symbol-rlimit]

```nim
RLimit {.importc: "struct rlimit", header: "<sys/resource.h>", pure, final.} = object
  rlim_cur*: int
  rlim_max*: int
```

### Rusage

[ref: #symbol-rusage]

```nim
Rusage {.importc: "struct rusage", header: "<sys/resource.h>", bycopy.} = object
  ru_utime*, ru_stime*: Timeval
  ru_maxrss*, ru_ixrss*, ru_idrss*, ru_isrss*, ru_minflt*, ru_majflt*,
  ru_nswap*, ru_inblock*, ru_oublock*, ru_msgsnd*, ru_msgrcv*, ru_nsignals*,
  ru_nvcsw*, ru_nivcsw*: clong
```

### Sched_param

[ref: #symbol-sched-param]

```nim
Sched_param {.importc: "struct sched_param", header: "<sched.h>", final, pure.} = object
  sched_priority*: cint
  sched_ss_low_priority*: cint ## Low scheduling priority for
                               ## sporadic server.
  sched_ss_repl_period*: Timespec ## Replenishment period for
                                  ## sporadic server.
  sched_ss_init_budget*: Timespec ## Initial budget for sporadic server.
  sched_ss_max_repl*: cint   ## Maximum pending replenishments for
                             ## sporadic server.
```

struct sched\_param

### Sem

[ref: #symbol-sem]

```nim
Sem {.importc: "sem_t", header: "<semaphore.h>", final, pure.} = object
```

### Servent

[ref: #symbol-servent]

```nim
Servent {.importc: "struct servent", pure, final, header: "<netdb.h>".} = object
  s_name*: cstring           ## Official name of the service.
  s_aliases*: cstringArray   ## A pointer to an array of pointers to
                             ## alternative service names, terminated by
                             ## a null pointer.
  s_port*: cint              ## The port number at which the service
                             ## resides, in network byte order.
  s_proto*: cstring          ## The name of the protocol to use when
                             ## contacting the service.
```

struct servent

### Sig_atomic

[ref: #symbol-sig-atomic]

```nim
Sig_atomic {.importc: "sig_atomic_t", header: "<signal.h>".} = cint
```

Possibly volatile-qualified integer type of an object that can be accessed as an atomic entity, even in the presence of asynchronous interrupts.

### Sigaction

[ref: #symbol-sigaction]

```nim
Sigaction {.importc: "struct sigaction", header: "<signal.h>", final, pure.} = object
  sa_handler*: proc (x: cint) {.noconv.} ## Pointer to a signal-catching
                                         ## function or one of the macros
                                         ## SIG_IGN or SIG_DFL.
  sa_mask*: Sigset           ## Set of signals to be blocked during execution of
                             ## the signal handling function.
  sa_flags*: cint            ## Special flags.
  sa_sigaction*: proc (x: cint; y: ptr SigInfo; z: pointer) {.noconv.}
```

struct sigaction

### SigEvent

[ref: #symbol-sigevent]

```nim
SigEvent {.importc: "struct sigevent", header: "<signal.h>", final, pure.} = object
  sigev_notify*: cint        ## Notification type.
  sigev_signo*: cint         ## Signal number.
  sigev_value*: SigVal       ## Signal value.
  sigev_notify_function*: proc (x: SigVal) {.noconv.} ## Notification func.
  sigev_notify_attributes*: ptr Pthread_attr ## Notification attributes.
```

struct sigevent

### SigInfo

[ref: #symbol-siginfo]

```nim
SigInfo {.importc: "siginfo_t", header: "<signal.h>", final, pure.} = object
  si_signo*: cint            ## Signal number.
  si_code*: cint             ## Signal code.
  si_errno*: cint            ## If non-zero, an errno value associated with
                             ## this signal, as defined in <errno.h>.
  si_pid*: Pid               ## Sending process ID.
  si_uid*: Uid               ## Real user ID of sending process.
  si_addr*: pointer          ## Address of faulting instruction.
  si_status*: cint           ## Exit value or signal.
  si_band*: int              ## Band event for SIGPOLL.
  si_value*: SigVal          ## Signal value.
```

siginfo\_t

### Sigset

[ref: #symbol-sigset]

```nim
Sigset {.importc: "sigset_t", header: "<signal.h>", final, pure.} = object
```

### SigStack

[ref: #symbol-sigstack]

```nim
SigStack {.importc: "struct sigstack", header: "<signal.h>", final, pure.} = object
  ss_onstack*: cint          ## Non-zero when signal stack is in use.
  ss_sp*: pointer            ## Signal stack pointer.
```

struct sigstack

### SigVal

[ref: #symbol-sigval]

```nim
SigVal {.importc: "union sigval", header: "<signal.h>", final, pure.} = object
  sival_ptr*: pointer        ## pointer signal value;
                             ## integer signal value not defined!
```

struct sigval

### SockAddr

[ref: #symbol-sockaddr]

```nim
SockAddr {.importc: "struct sockaddr", header: "<sys/socket.h>", pure, final.} = object
  sa_family*: TSa_Family     ## Address family.
  sa_data*: array[0 .. 255, char] ## Socket address (variable-length data).
```

struct sockaddr

### Sockaddr_in

[ref: #symbol-sockaddr-in]

```nim
Sockaddr_in {.importc: "struct sockaddr_in", pure, final,
              header: "<netinet/in.h>".} = object
  sin_family*: TSa_Family    ## AF_INET.
  sin_port*: InPort          ## Port number.
  sin_addr*: InAddr          ## IP address.
```

struct sockaddr\_in

### Sockaddr_in6

[ref: #symbol-sockaddr-in6]

```nim
Sockaddr_in6 {.importc: "struct sockaddr_in6", pure, final,
               header: "<netinet/in.h>".} = object
  sin6_family*: TSa_Family   ## AF_INET6.
  sin6_port*: InPort         ## Port number.
  sin6_flowinfo*: uint32     ## IPv6 traffic class and flow information.
  sin6_addr*: In6Addr        ## IPv6 address.
  sin6_scope_id*: uint32     ## Set of interfaces for a scope.
```

struct sockaddr\_in6

### Sockaddr_storage

[ref: #symbol-sockaddr-storage]

```nim
Sockaddr_storage {.importc: "struct sockaddr_storage", header: "<sys/socket.h>",
                   pure, final.} = object
  ss_family*: TSa_Family     ## Address family.
```

struct sockaddr\_storage

### Sockaddr_un

[ref: #symbol-sockaddr-un]

```nim
Sockaddr_un {.importc: "struct sockaddr_un", header: "<sys/un.h>", pure, final.} = object
  sun_family*: TSa_Family    ## Address family.
  sun_path*: array[0 .. 92 - 1, char] ## Socket path
```

struct sockaddr\_un

### SocketHandle

[ref: #symbol-sockethandle]

```nim
SocketHandle = distinct cint
```

### SockLen

[ref: #symbol-socklen]

```nim
SockLen {.importc: "socklen_t", header: "<sys/socket.h>".} = cuint
```

### Stack

[ref: #symbol-stack]

```nim
Stack {.importc: "stack_t", header: "<signal.h>", final, pure.} = object
  ss_sp*: pointer            ## Stack base or pointer.
  ss_size*: int              ## Stack size.
  ss_flags*: cint            ## Flags.
```

stack\_t

### Stat

[ref: #symbol-stat]

```nim
Stat {.importc: "struct stat", header: "<sys/stat.h>", final, pure.} = object
  st_dev*: Dev               ## Device ID of device containing file.
  st_ino*: Ino               ## File serial number.
  st_mode*: Mode             ## Mode of file (see below).
  st_nlink*: Nlink           ## Number of hard links to the file.
  st_uid*: Uid               ## User ID of file.
  st_gid*: Gid               ## Group ID of file.
  st_rdev*: Dev              ## Device ID (if file is character or block special).
  st_size*: Off              ## For regular files, the file size in bytes.
                             ## For symbolic links, the length in bytes of the
                             ## pathname contained in the symbolic link.
                             ## For a shared memory object, the length in bytes.
                             ## For a typed memory object, the length in bytes.
                             ## For other file types, the use of this field is
                             ## unspecified.
  when defined(osx):
    st_atim* {.importc: "st_atimespec".}: Timespec ## Time of last access.
    st_mtim* {.importc: "st_mtimespec".}: Timespec ## Time of last data modification.
    st_ctim* {.importc: "st_ctimespec".}: Timespec ## Time of last status change.
  elif StatHasNanoseconds:
    st_atim*: Timespec       ## Time of last access.
    st_mtim*: Timespec       ## Time of last data modification.
    st_ctim*: Timespec       ## Time of last status change.
  else:
    st_atime*: Time          ## Time of last access.
    st_mtime*: Time          ## Time of last data modification.
    st_ctime*: Time          ## Time of last status change.
  st_blksize*: Blksize       ## A file system-specific preferred I/O block size
                             ## for this object. In some file system types, this
                             ## may vary from file to file.
  st_blocks*: Blkcnt         ## Number of blocks allocated for this object.
```

struct stat

### Statvfs

[ref: #symbol-statvfs]

```nim
Statvfs {.importc: "struct statvfs", header: "<sys/statvfs.h>", final, pure.} = object
  f_bsize*: int              ## File system block size.
  f_frsize*: int             ## Fundamental file system block size.
  f_blocks*: Fsblkcnt        ## Total number of blocks on file system
                             ## in units of f_frsize.
  f_bfree*: Fsblkcnt         ## Total number of free blocks.
  f_bavail*: Fsblkcnt        ## Number of free blocks available to
                             ## non-privileged process.
  f_files*: Fsfilcnt         ## Total number of file serial numbers.
  f_ffree*: Fsfilcnt         ## Total number of free file serial numbers.
  f_favail*: Fsfilcnt        ## Number of file serial numbers available to
                             ## non-privileged process.
  f_fsid*: int               ## File system ID.
  f_flag*: int               ## Bit mask of f_flag values.
  f_namemax*: int            ## Maximum filename length.
```

struct statvfs

### Suseconds

[ref: #symbol-suseconds]

```nim
Suseconds {.importc: "suseconds_t", header: "<sys/types.h>".} = int32
```

### Tcmsghdr

[ref: #symbol-tcmsghdr]

```nim
Tcmsghdr {.importc: "struct cmsghdr", pure, final, header: "<sys/socket.h>".} = object
  cmsg_len*: SockLen         ## Data byte count, including the cmsghdr.
  cmsg_level*: cint          ## Originating protocol.
  cmsg_type*: cint           ## Protocol-specific type.
```

struct cmsghdr

### TFdSet

[ref: #symbol-tfdset]

```nim
TFdSet {.importc: "fd_set", header: "<sys/select.h>", final, pure.} = object
```

### Tflock

[ref: #symbol-tflock]

```nim
Tflock {.importc: "struct flock", final, pure, header: "<fcntl.h>".} = object
  l_type*: cshort            ## Type of lock; F_RDLCK, F_WRLCK, F_UNLCK.
  l_whence*: cshort          ## Flag for starting offset.
  l_start*: Off              ## Relative offset in bytes.
  l_len*: Off                ## Size; if 0 then until EOF.
  l_pid*: Pid                ## Process ID of the process holding the lock;
                             ## returned with F_GETLK.
```

flock type

### Tif_nameindex

[ref: #symbol-tif-nameindex]

```nim
Tif_nameindex {.importc: "struct if_nameindex", final, pure,
                header: "<net/if.h>".} = object
  if_index*: cint            ## Numeric index of the interface.
  if_name*: cstring          ## Null-terminated name of the interface.
```

struct if\_nameindex

### Time

[ref: #symbol-time]

```nim
Time {.importc: "time_t", header: "<time.h>".} = distinct clong
```

### Timer

[ref: #symbol-timer]

```nim
Timer {.importc: "timer_t", header: "<sys/types.h>".} = int
```

### Timespec

[ref: #symbol-timespec]

```nim
Timespec {.importc: "struct timespec", header: "<time.h>", final, pure.} = object
  tv_sec*: Time              ## Seconds.
  tv_nsec*: int              ## Nanoseconds.
```

struct timespec

### Timeval

[ref: #symbol-timeval]

```nim
Timeval {.importc: "struct timeval", header: "<sys/select.h>", final, pure.} = object
  tv_sec*: Time              ## Seconds.
  tv_usec*: Suseconds        ## Microseconds.
```

struct timeval

### Tipv6_mreq

[ref: #symbol-tipv6-mreq]

```nim
Tipv6_mreq {.importc: "struct ipv6_mreq", pure, final, header: "<netinet/in.h>".} = object
  ipv6mr_multiaddr*: In6Addr ## IPv6 multicast address.
  ipv6mr_interface*: cint    ## Interface index.
```

struct ipv6\_mreq

### TLinger

[ref: #symbol-tlinger]

```nim
TLinger {.importc: "struct linger", pure, final, header: "<sys/socket.h>".} = object
  l_onoff*: cint             ## Indicates whether linger option is enabled.
  l_linger*: cint            ## Linger time, in seconds.
```

struct linger

### Tm

[ref: #symbol-tm]

```nim
Tm {.importc: "struct tm", header: "<time.h>", final, pure.} = object
  tm_sec*: cint              ## Seconds [0,60].
  tm_min*: cint              ## Minutes [0,59].
  tm_hour*: cint             ## Hour [0,23].
  tm_mday*: cint             ## Day of month [1,31].
  tm_mon*: cint              ## Month of year [0,11].
  tm_year*: cint             ## Years since 1900.
  tm_wday*: cint             ## Day of week [0,6] (Sunday =0).
  tm_yday*: cint             ## Day of year [0,365].
  tm_isdst*: cint            ## Daylight Savings flag.
```

struct tm

### Tmsghdr

[ref: #symbol-tmsghdr]

```nim
Tmsghdr {.importc: "struct msghdr", pure, final, header: "<sys/socket.h>".} = object
  msg_name*: pointer         ## Optional address.
  msg_namelen*: SockLen      ## Size of address.
  msg_iov*: ptr IOVec        ## Scatter/gather array.
  msg_iovlen*: cint          ## Members in msg_iov.
  msg_control*: pointer      ## Ancillary data; see below.
  msg_controllen*: SockLen   ## Ancillary data buffer len.
  msg_flags*: cint           ## Flags on received message.
```

struct msghdr

### Tnetent

[ref: #symbol-tnetent]

```nim
Tnetent {.importc: "struct netent", pure, final, header: "<netdb.h>".} = object
  n_name*: cstring           ## Official, fully-qualified (including the
                             ## domain) name of the host.
  n_aliases*: cstringArray   ## A pointer to an array of pointers to
                             ## alternative network names, terminated by a
                             ## null pointer.
  n_addrtype*: cint          ## The address type of the network.
  n_net*: uint32             ## The network number, in host byte order.
```

struct netent

### Tnfds

[ref: #symbol-tnfds]

```nim
Tnfds {.importc: "nfds_t", header: "<poll.h>".} = cuint
```

### TPollfd

[ref: #symbol-tpollfd]

```nim
TPollfd {.importc: "struct pollfd", pure, final, header: "<poll.h>".} = object
  fd*: cint                  ## The following descriptor being polled.
  events*: cshort            ## The input event flags (see below).
  revents*: cshort           ## The output event flags (see below).
```

struct pollfd

### Tposix_spawn_file_actions

[ref: #symbol-tposix-spawn-file-actions]

```nim
Tposix_spawn_file_actions {.importc: "posix_spawn_file_actions_t",
                            header: "<spawn.h>", final, pure.} = object
```

### Tposix_spawnattr

[ref: #symbol-tposix-spawnattr]

```nim
Tposix_spawnattr {.importc: "posix_spawnattr_t", header: "<spawn.h>", final,
                   pure.} = object
```

### Trace_attr

[ref: #symbol-trace-attr]

```nim
Trace_attr {.importc: "trace_attr_t", header: "<sys/types.h>".} = int
```

### Trace_event_id

[ref: #symbol-trace-event-id]

```nim
Trace_event_id {.importc: "trace_event_id_t", header: "<sys/types.h>".} = int
```

### Trace_event_set

[ref: #symbol-trace-event-set]

```nim
Trace_event_set {.importc: "trace_event_set_t", header: "<sys/types.h>".} = int
```

### Trace_id

[ref: #symbol-trace-id]

```nim
Trace_id {.importc: "trace_id_t", header: "<sys/types.h>".} = int
```

### TSa_Family

[ref: #symbol-tsa-family]

```nim
TSa_Family {.importc: "sa_family_t", header: "<sys/socket.h>".} = uint8
```

### Ucontext

[ref: #symbol-ucontext]

```nim
Ucontext {.importc: "ucontext_t", header: "<ucontext.h>", final, pure.} = object
  uc_link*: ptr Ucontext     ## Pointer to the context that is resumed
                             ## when this context returns.
  uc_sigmask*: Sigset        ## The set of signals that are blocked when this
                             ## context is active.
  uc_stack*: Stack           ## The stack used by this context.
  uc_mcontext*: Mcontext     ## A machine-specific representation of the saved
                             ## context.
```

ucontext\_t

### Uid

[ref: #symbol-uid]

```nim
Uid {.importc: "uid_t", header: "<sys/types.h>".} = uint32
```

### Useconds

[ref: #symbol-useconds]

```nim
Useconds {.importc: "useconds_t", header: "<sys/types.h>".} = int
```

### Utsname

[ref: #symbol-utsname]

```nim
Utsname {.importc: "struct utsname", header: "<sys/utsname.h>", final, pure.} = object
  sysname*,                 ## Name of the hardware type on which the
                             ## system is running.
  ## Name of this implementation of the operating system.
  nodename*,                ## Name of this node within the communications
                             ## network to which this node is attached, if any.
  release*,                 ## Current release level of this implementation.
  version*,                 ## Current version level of this release.
  machine*: array[0 .. 255, char]
```

struct utsname

## Var

### ABDAY_1

[ref: #symbol-abday-1]

```nim
ABDAY_1 {.importc: "ABDAY_1", header: "<langinfo.h>".}: cint
```

### ABDAY_2

[ref: #symbol-abday-2]

```nim
ABDAY_2 {.importc: "ABDAY_2", header: "<langinfo.h>".}: cint
```

### ABDAY_3

[ref: #symbol-abday-3]

```nim
ABDAY_3 {.importc: "ABDAY_3", header: "<langinfo.h>".}: cint
```

### ABDAY_4

[ref: #symbol-abday-4]

```nim
ABDAY_4 {.importc: "ABDAY_4", header: "<langinfo.h>".}: cint
```

### ABDAY_5

[ref: #symbol-abday-5]

```nim
ABDAY_5 {.importc: "ABDAY_5", header: "<langinfo.h>".}: cint
```

### ABDAY_6

[ref: #symbol-abday-6]

```nim
ABDAY_6 {.importc: "ABDAY_6", header: "<langinfo.h>".}: cint
```

### ABDAY_7

[ref: #symbol-abday-7]

```nim
ABDAY_7 {.importc: "ABDAY_7", header: "<langinfo.h>".}: cint
```

### ABMON_1

[ref: #symbol-abmon-1]

```nim
ABMON_1 {.importc: "ABMON_1", header: "<langinfo.h>".}: cint
```

### ABMON_10

[ref: #symbol-abmon-10]

```nim
ABMON_10 {.importc: "ABMON_10", header: "<langinfo.h>".}: cint
```

### ABMON_11

[ref: #symbol-abmon-11]

```nim
ABMON_11 {.importc: "ABMON_11", header: "<langinfo.h>".}: cint
```

### ABMON_12

[ref: #symbol-abmon-12]

```nim
ABMON_12 {.importc: "ABMON_12", header: "<langinfo.h>".}: cint
```

### ABMON_2

[ref: #symbol-abmon-2]

```nim
ABMON_2 {.importc: "ABMON_2", header: "<langinfo.h>".}: cint
```

### ABMON_3

[ref: #symbol-abmon-3]

```nim
ABMON_3 {.importc: "ABMON_3", header: "<langinfo.h>".}: cint
```

### ABMON_4

[ref: #symbol-abmon-4]

```nim
ABMON_4 {.importc: "ABMON_4", header: "<langinfo.h>".}: cint
```

### ABMON_5

[ref: #symbol-abmon-5]

```nim
ABMON_5 {.importc: "ABMON_5", header: "<langinfo.h>".}: cint
```

### ABMON_6

[ref: #symbol-abmon-6]

```nim
ABMON_6 {.importc: "ABMON_6", header: "<langinfo.h>".}: cint
```


[Prev](posix_7.md) | [Next](posix_9.md)
