---
source_hash: 319d53cfc1304803
source_path: lib/windows/winlean.nim
---

# winlean

[ref: #module-winlean]

This module implements a small wrapper for some needed Win API procedures, so that the Nim compiler does not depend on the huge Windows module.

## Const

### AF_INET

[ref: #symbol-af-inet]

```nim
AF_INET = 2
```

### AF_INET6

[ref: #symbol-af-inet6]

```nim
AF_INET6 = 23
```

### AF_UNSPEC

[ref: #symbol-af-unspec]

```nim
AF_UNSPEC = 0
```

### AI_V4MAPPED

[ref: #symbol-ai-v4mapped]

```nim
AI_V4MAPPED = 0x00000008
```

### CREATE_ALWAYS

[ref: #symbol-create-always]

```nim
CREATE_ALWAYS = 2'i32
```

### CREATE_NEW

[ref: #symbol-create-new]

```nim
CREATE_NEW = 1'i32
```

### CREATE_NO_WINDOW

[ref: #symbol-create-no-window]

```nim
CREATE_NO_WINDOW = 0x08000000'i32
```

### CREATE_UNICODE_ENVIRONMENT

[ref: #symbol-create-unicode-environment]

```nim
CREATE_UNICODE_ENVIRONMENT = 1024'i32
```

### DETACHED_PROCESS

[ref: #symbol-detached-process]

```nim
DETACHED_PROCESS = 8'i32
```

### DOMAIN_ALIAS_RID_ADMINS

[ref: #symbol-domain-alias-rid-admins]

```nim
DOMAIN_ALIAS_RID_ADMINS = 544
```

### DUPLICATE_SAME_ACCESS

[ref: #symbol-duplicate-same-access]

```nim
DUPLICATE_SAME_ACCESS = 2
```

### ERROR_ACCESS_DENIED

[ref: #symbol-error-access-denied]

```nim
ERROR_ACCESS_DENIED = 5
```

### ERROR_BAD_ARGUMENTS

[ref: #symbol-error-bad-arguments]

```nim
ERROR_BAD_ARGUMENTS = 165
```

### ERROR_FILE_EXISTS

[ref: #symbol-error-file-exists]

```nim
ERROR_FILE_EXISTS = 80
```

### ERROR_FILE_NOT_FOUND

[ref: #symbol-error-file-not-found]

```nim
ERROR_FILE_NOT_FOUND = 2
```

<https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499>-

### ERROR_HANDLE_EOF

[ref: #symbol-error-handle-eof]

```nim
ERROR_HANDLE_EOF = 38
```

### ERROR_IO_PENDING

[ref: #symbol-error-io-pending]

```nim
ERROR_IO_PENDING = 997
```

### ERROR_LOCK_VIOLATION

[ref: #symbol-error-lock-violation]

```nim
ERROR_LOCK_VIOLATION = 33
```

### ERROR_NETNAME_DELETED

[ref: #symbol-error-netname-deleted]

```nim
ERROR_NETNAME_DELETED = 64
```

### ERROR_NO_MORE_FILES

[ref: #symbol-error-no-more-files]

```nim
ERROR_NO_MORE_FILES = 18
```

### ERROR_PATH_NOT_FOUND

[ref: #symbol-error-path-not-found]

```nim
ERROR_PATH_NOT_FOUND = 3
```

### FD_ACCEPT

[ref: #symbol-fd-accept]

```nim
FD_ACCEPT = 0x00000008'i32
```

### FD_ADDRESS_LIST_CHANGE

[ref: #symbol-fd-address-list-change]

```nim
FD_ADDRESS_LIST_CHANGE = 0x00000200'i32
```

### FD_ALL_EVENTS

[ref: #symbol-fd-all-events]

```nim
FD_ALL_EVENTS = 0x000003FF'i32
```

### FD_CLOSE

[ref: #symbol-fd-close]

```nim
FD_CLOSE = 0x00000020'i32
```

### FD_CONNECT

[ref: #symbol-fd-connect]

```nim
FD_CONNECT = 0x00000010'i32
```

### FD_GROUP_QQS

[ref: #symbol-fd-group-qqs]

```nim
FD_GROUP_QQS = 0x00000080'i32
```

### FD_OOB

[ref: #symbol-fd-oob]

```nim
FD_OOB = 0x00000004'i32
```

### FD_QQS

[ref: #symbol-fd-qqs]

```nim
FD_QQS = 0x00000040'i32
```

### FD_READ

[ref: #symbol-fd-read]

```nim
FD_READ = 0x00000001'i32
```

### FD_ROUTING_INTERFACE_CHANGE

[ref: #symbol-fd-routing-interface-change]

```nim
FD_ROUTING_INTERFACE_CHANGE = 0x00000100'i32
```

### FD_SETSIZE

[ref: #symbol-fd-setsize]

```nim
FD_SETSIZE = 64
```

### FD_WRITE

[ref: #symbol-fd-write]

```nim
FD_WRITE = 0x00000002'i32
```

### FIBER_FLAG_FLOAT_SWITCH

[ref: #symbol-fiber-flag-float-switch]

```nim
FIBER_FLAG_FLOAT_SWITCH = 0x00000001
```

### FILE_ATTRIBUTE_ARCHIVE

[ref: #symbol-file-attribute-archive]

```nim
FILE_ATTRIBUTE_ARCHIVE = 0x00000020'i32
```

### FILE_ATTRIBUTE_COMPRESSED

[ref: #symbol-file-attribute-compressed]

```nim
FILE_ATTRIBUTE_COMPRESSED = 0x00000800'i32
```

### FILE_ATTRIBUTE_DEVICE

[ref: #symbol-file-attribute-device]

```nim
FILE_ATTRIBUTE_DEVICE = 0x00000040'i32
```

### FILE_ATTRIBUTE_DIRECTORY

[ref: #symbol-file-attribute-directory]

```nim
FILE_ATTRIBUTE_DIRECTORY = 0x00000010'i32
```

### FILE_ATTRIBUTE_HIDDEN

[ref: #symbol-file-attribute-hidden]

```nim
FILE_ATTRIBUTE_HIDDEN = 0x00000002'i32
```

### FILE_ATTRIBUTE_NORMAL

[ref: #symbol-file-attribute-normal]

```nim
FILE_ATTRIBUTE_NORMAL = 0x00000080'i32
```

### FILE_ATTRIBUTE_NOT_CONTENT_INDEXED

[ref: #symbol-file-attribute-not-content-indexed]

```nim
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x00002000'i32
```

### FILE_ATTRIBUTE_OFFLINE

[ref: #symbol-file-attribute-offline]

```nim
FILE_ATTRIBUTE_OFFLINE = 0x00001000'i32
```

### FILE_ATTRIBUTE_READONLY

[ref: #symbol-file-attribute-readonly]

```nim
FILE_ATTRIBUTE_READONLY = 0x00000001'i32
```

### FILE_ATTRIBUTE_REPARSE_POINT

[ref: #symbol-file-attribute-reparse-point]

```nim
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400'i32
```

### FILE_ATTRIBUTE_SPARSE_FILE

[ref: #symbol-file-attribute-sparse-file]

```nim
FILE_ATTRIBUTE_SPARSE_FILE = 0x00000200'i32
```

### FILE_ATTRIBUTE_SYSTEM

[ref: #symbol-file-attribute-system]

```nim
FILE_ATTRIBUTE_SYSTEM = 0x00000004'i32
```

### FILE_ATTRIBUTE_TEMPORARY

[ref: #symbol-file-attribute-temporary]

```nim
FILE_ATTRIBUTE_TEMPORARY = 0x00000100'i32
```

### FILE_BEGIN

[ref: #symbol-file-begin]

```nim
FILE_BEGIN = 0'i32
```

### FILE_FLAG_BACKUP_SEMANTICS

[ref: #symbol-file-flag-backup-semantics]

```nim
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000'i32
```

### FILE_FLAG_DELETE_ON_CLOSE

[ref: #symbol-file-flag-delete-on-close]

```nim
FILE_FLAG_DELETE_ON_CLOSE = 0x04000000'i32
```

### FILE_FLAG_FIRST_PIPE_INSTANCE

[ref: #symbol-file-flag-first-pipe-instance]

```nim
FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000'i32
```

### FILE_FLAG_NO_BUFFERING

[ref: #symbol-file-flag-no-buffering]

```nim
FILE_FLAG_NO_BUFFERING = 0x20000000'i32
```

### FILE_FLAG_OPEN_NO_RECALL

[ref: #symbol-file-flag-open-no-recall]

```nim
FILE_FLAG_OPEN_NO_RECALL = 0x00100000'i32
```

### FILE_FLAG_OPEN_REPARSE_POINT

[ref: #symbol-file-flag-open-reparse-point]

```nim
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000'i32
```

### FILE_FLAG_OVERLAPPED

[ref: #symbol-file-flag-overlapped]

```nim
FILE_FLAG_OVERLAPPED = 0x40000000'i32
```

### FILE_FLAG_POSIX_SEMANTICS

[ref: #symbol-file-flag-posix-semantics]

```nim
FILE_FLAG_POSIX_SEMANTICS = 0x01000000'i32
```

### FILE_FLAG_RANDOM_ACCESS

[ref: #symbol-file-flag-random-access]

```nim
FILE_FLAG_RANDOM_ACCESS = 0x10000000'i32
```

### FILE_FLAG_SEQUENTIAL_SCAN

[ref: #symbol-file-flag-sequential-scan]

```nim
FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000'i32
```

### FILE_FLAG_WRITE_THROUGH

[ref: #symbol-file-flag-write-through]

```nim
FILE_FLAG_WRITE_THROUGH = 0x80000000'i32
```

### FILE_MAP_READ

[ref: #symbol-file-map-read]

```nim
FILE_MAP_READ = 4'i32
```

### FILE_MAP_WRITE

[ref: #symbol-file-map-write]

```nim
FILE_MAP_WRITE = 2'i32
```

### FILE_READ_DATA

[ref: #symbol-file-read-data]

```nim
FILE_READ_DATA = 0x00000001
```

### FILE_SHARE_DELETE

[ref: #symbol-file-share-delete]

```nim
FILE_SHARE_DELETE = 4'i32
```

### FILE_SHARE_READ

[ref: #symbol-file-share-read]

```nim
FILE_SHARE_READ = 1'i32
```

### FILE_SHARE_WRITE

[ref: #symbol-file-share-write]

```nim
FILE_SHARE_WRITE = 2'i32
```

### FILE_WRITE_DATA

[ref: #symbol-file-write-data]

```nim
FILE_WRITE_DATA = 0x00000002
```

### FSCTL_GET_REPARSE_POINT

[ref: #symbol-fsctl-get-reparse-point]

```nim
FSCTL_GET_REPARSE_POINT = 0x000900A8'i32
```

### GENERIC_ALL

[ref: #symbol-generic-all]

```nim
GENERIC_ALL = 0x10000000'i32
```

### GENERIC_READ

[ref: #symbol-generic-read]

```nim
GENERIC_READ = 0x80000000'i32
```

### GENERIC_WRITE

[ref: #symbol-generic-write]

```nim
GENERIC_WRITE = 0x40000000'i32
```

### HANDLE_FLAG_INHERIT

[ref: #symbol-handle-flag-inherit]

```nim
HANDLE_FLAG_INHERIT = 0x00000001'i32
```

### HIGH_PRIORITY_CLASS

[ref: #symbol-high-priority-class]

```nim
HIGH_PRIORITY_CLASS = 128'i32
```

### IDLE_PRIORITY_CLASS

[ref: #symbol-idle-priority-class]

```nim
IDLE_PRIORITY_CLASS = 64'i32
```

### INADDR_ANY

[ref: #symbol-inaddr-any]

```nim
INADDR_ANY = 0'u32
```

### INADDR_BROADCAST

[ref: #symbol-inaddr-broadcast]

```nim
INADDR_BROADCAST = -1
```

### INADDR_LOOPBACK

[ref: #symbol-inaddr-loopback]

```nim
INADDR_LOOPBACK = 0x7F000001
```

### INADDR_NONE

[ref: #symbol-inaddr-none]

```nim
INADDR_NONE = -1
```

### INFINITE

[ref: #symbol-infinite]

```nim
INFINITE = -1'i32
```

### INVALID_FILE_SIZE

[ref: #symbol-invalid-file-size]

```nim
INVALID_FILE_SIZE = -1'i32
```

### INVALID_HANDLE_VALUE

[ref: #symbol-invalid-handle-value]

```nim
INVALID_HANDLE_VALUE = -1
```

### INVALID_SET_FILE_POINTER

[ref: #symbol-invalid-set-file-pointer]

```nim
INVALID_SET_FILE_POINTER = -1'i32
```

### IO_REPARSE_TAG_MOUNT_POINT

[ref: #symbol-io-reparse-tag-mount-point]

```nim
IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003'i32
```

### IO_REPARSE_TAG_SYMLINK

[ref: #symbol-io-reparse-tag-symlink]

```nim
IO_REPARSE_TAG_SYMLINK = 0xA000000C'i32
```

### IOC_IN

[ref: #symbol-ioc-in]

```nim
IOC_IN = 0x80000000'i32
```

### IOC_INOUT

[ref: #symbol-ioc-inout]

```nim
IOC_INOUT = -1073741824'i32
```

### IOC_OUT

[ref: #symbol-ioc-out]

```nim
IOC_OUT = 0x40000000'i32
```

### IOC_WS2

[ref: #symbol-ioc-ws2]

```nim
IOC_WS2 = 0x08000000'i32
```

### MAX_PATH

[ref: #symbol-max-path]

```nim
MAX_PATH = 260
```

### MAXIMUM_REPARSE_DATA_BUFFER_SIZE

[ref: #symbol-maximum-reparse-data-buffer-size]

```nim
MAXIMUM_REPARSE_DATA_BUFFER_SIZE = 16384
```

### MAXIMUM_WAIT_OBJECTS

[ref: #symbol-maximum-wait-objects]

```nim
MAXIMUM_WAIT_OBJECTS = 0x00000040
```

### MOVEFILE_COPY_ALLOWED

[ref: #symbol-movefile-copy-allowed]

```nim
MOVEFILE_COPY_ALLOWED = 0x00000002'i32
```

### MOVEFILE_CREATE_HARDLINK

[ref: #symbol-movefile-create-hardlink]

```nim
MOVEFILE_CREATE_HARDLINK = 0x00000010'i32
```

### MOVEFILE_DELAY_UNTIL_REBOOT

[ref: #symbol-movefile-delay-until-reboot]

```nim
MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004'i32
```

### MOVEFILE_FAIL_IF_NOT_TRACKABLE

[ref: #symbol-movefile-fail-if-not-trackable]

```nim
MOVEFILE_FAIL_IF_NOT_TRACKABLE = 0x00000020'i32
```

### MOVEFILE_REPLACE_EXISTING

[ref: #symbol-movefile-replace-existing]

```nim
MOVEFILE_REPLACE_EXISTING = 0x00000001'i32
```

### MOVEFILE_WRITE_THROUGH

[ref: #symbol-movefile-write-through]

```nim
MOVEFILE_WRITE_THROUGH = 0x00000008'i32
```

### MSG_PEEK

[ref: #symbol-msg-peek]

```nim
MSG_PEEK = 2
```

### NO_ERROR

[ref: #symbol-no-error]

```nim
NO_ERROR = 0'i32
```

### NORMAL_PRIORITY_CLASS

[ref: #symbol-normal-priority-class]

```nim
NORMAL_PRIORITY_CLASS = 32'i32
```

### OPEN_ALWAYS

[ref: #symbol-open-always]

```nim
OPEN_ALWAYS = 4'i32
```

### OPEN_EXISTING

[ref: #symbol-open-existing]

```nim
OPEN_EXISTING = 3'i32
```

### PAGE_EXECUTE

[ref: #symbol-page-execute]

```nim
PAGE_EXECUTE = 0x00000010'i32
```

### PAGE_EXECUTE_READ

[ref: #symbol-page-execute-read]

```nim
PAGE_EXECUTE_READ = 0x00000020'i32
```

### PAGE_EXECUTE_READWRITE

[ref: #symbol-page-execute-readwrite]

```nim
PAGE_EXECUTE_READWRITE = 0x00000040'i32
```

### PAGE_NOACCESS

[ref: #symbol-page-noaccess]

```nim
PAGE_NOACCESS = 0x00000001'i32
```

### PAGE_READONLY

[ref: #symbol-page-readonly]

```nim
PAGE_READONLY = 2'i32
```

### PAGE_READWRITE

[ref: #symbol-page-readwrite]

```nim
PAGE_READWRITE = 4'i32
```

### PIPE_ACCESS_DUPLEX

[ref: #symbol-pipe-access-duplex]

```nim
PIPE_ACCESS_DUPLEX = 0x00000003'i32
```

### PIPE_ACCESS_INBOUND

[ref: #symbol-pipe-access-inbound]

```nim
PIPE_ACCESS_INBOUND = 1'i32
```

### PIPE_ACCESS_OUTBOUND

[ref: #symbol-pipe-access-outbound]

```nim
PIPE_ACCESS_OUTBOUND = 2'i32
```

### PIPE_NOWAIT

[ref: #symbol-pipe-nowait]

```nim
PIPE_NOWAIT = 0x00000001'i32
```

### PROCESS_CREATE_PROCESS

[ref: #symbol-process-create-process]

```nim
PROCESS_CREATE_PROCESS = 0x00000080'i32
```

### PROCESS_CREATE_THREAD

[ref: #symbol-process-create-thread]

```nim
PROCESS_CREATE_THREAD = 0x00000002'i32
```

### PROCESS_DUP_HANDLE

[ref: #symbol-process-dup-handle]

```nim
PROCESS_DUP_HANDLE = 0x00000040'i32
```

### PROCESS_QUERY_INFORMATION

[ref: #symbol-process-query-information]

```nim
PROCESS_QUERY_INFORMATION = 0x00000400'i32
```

### PROCESS_QUERY_LIMITED_INFORMATION

[ref: #symbol-process-query-limited-information]

```nim
PROCESS_QUERY_LIMITED_INFORMATION = 0x00001000'i32
```

### PROCESS_SET_INFORMATION

[ref: #symbol-process-set-information]

```nim
PROCESS_SET_INFORMATION = 0x00000200'i32
```

### PROCESS_SET_LIMITED_INFORMATION

[ref: #symbol-process-set-limited-information]

```nim
PROCESS_SET_LIMITED_INFORMATION = 0x00002000'i32
```

### PROCESS_SET_QUOTA

[ref: #symbol-process-set-quota]

```nim
PROCESS_SET_QUOTA = 0x00000100'i32
```

### PROCESS_SET_SESSIONID

[ref: #symbol-process-set-sessionid]

```nim
PROCESS_SET_SESSIONID = 0x00000004'i32
```

### PROCESS_SUSPEND_RESUME

[ref: #symbol-process-suspend-resume]

```nim
PROCESS_SUSPEND_RESUME = 0x00000800'i32
```

### PROCESS_TERMINATE

[ref: #symbol-process-terminate]

```nim
PROCESS_TERMINATE = 0x00000001'i32
```

### PROCESS_VM_OPERATION

[ref: #symbol-process-vm-operation]

```nim
PROCESS_VM_OPERATION = 0x00000008'i32
```


[Next](winlean_2.md)
