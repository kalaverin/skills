---
source_hash: c0a20a33d7b828a0
source_path: lib/pure/asynchttpserver.nim
---

# asynchttpserver

[ref: #module-asynchttpserver]

This module implements a high performance asynchronous HTTP server.

This HTTP server has not been designed to be used in production, but for testing applications locally. Because of this, when deploying your application in production you should use a reverse proxy (for example nginx) instead of allowing users to connect directly to this server.

## Examples

```nim
import std/asynchttpserver
# This example will create an HTTP server on an automatically chosen port.
# It will respond to all requests with a `200 OK` response code and "Hello World"
# as the response body.
import std/asyncdispatch
proc main {.async.} =
  var server = newAsyncHttpServer()
  proc cb(req: Request) {.async.} =
    echo (req.reqMethod, req.url, req.headers)
    let headers = {"Content-type": "text/plain; charset=utf-8"}
    await req.respond(Http200, "Hello World", headers.newHttpHeaders())

  server.listen(Port(0)) # or Port(8080) to hardcode the standard HTTP port.
  let port = server.getPort
  echo "test this with: curl localhost:" & $port.uint16 & "/"
  while true:
    if server.shouldAcceptRequest():
      await server.acceptRequest(cb)
    else:
      # too many concurrent connections, `maxFDs` exceeded
      # wait 500ms for FDs to be closed
      await sleepAsync(500)

waitFor main()
```

```nim
from std/nativesockets import Port
let server = newAsyncHttpServer()
server.listen(Port(0))
assert server.getPort.uint16 > 0
server.close()
```

```nim
import std/json
proc handler(req: Request) {.async.} =
  if req.url.path == "/hello-world":
    let msg = %* {"message": "Hello World"}
    let headers = newHttpHeaders([("Content-Type","application/json")])
    await req.respond(Http200, $msg, headers)
  else:
    await req.respond(Http404, "Not Found")
```

## Const

### nimMaxDescriptorsFallback

[ref: #symbol-nimmaxdescriptorsfallback]

fallback value for

```nim
nimMaxDescriptorsFallback {.intdefine.} = 16000
```

fallback value for
when maxDescriptors is not available. This can be set on the command line during compilation via -d:nimMaxDescriptorsFallback=N

## Proc

### acceptRequest

[ref: #symbol-acceptrequest]

**Input:**
- `server: AsyncHttpServer`
- `callback: proc (request: Request): Future[void] {.closure, gcsafe.}`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError, OSError, SslError, LibraryError, KeyError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, OSError, SslError, LibraryError, KeyError`, `tags: RootEffect`, `forbids: `

Accepts a single request. Write an explicit loop around this proc so that errors can be handled properly.

### close

[ref: #symbol-close]

**Input:**
- `server: AsyncHttpServer`

**Output:** *(none)*
**Pragmas:** `raises: [LibraryError, Exception, SslError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception, SslError`, `tags: RootEffect`, `forbids: `

Terminates the async http server instance.

### getPort

[ref: #symbol-getport]

Returns the port self was bound to.

**Input:**
- `self: AsyncHttpServer`

**Output:** `Port`
**Pragmas:** `raises: [OSError, Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: `, `forbids: `

Returns the port self was bound to.

Useful for identifying what port self is bound to, if it was chosen automatically, for example via listen(Port(0)).

### listen

[ref: #symbol-listen]

**Input:**
- `server: AsyncHttpServer`
- `port: Port`
- `address:  = ""`
- `domain:  = AF_INET`

**Output:** *(none)*
**Pragmas:** `raises: [OSError, ValueError]`, `tags: [WriteIOEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: OSError, ValueError`, `tags: WriteIOEffect, ReadIOEffect`, `forbids: `

Listen to the given port and address.

### newAsyncHttpServer

[ref: #symbol-newasynchttpserver]

**Input:**
- `reuseAddr:  = true`
- `reusePort:  = false`
- `maxBody:  = 8388608`

**Output:** `AsyncHttpServer`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new AsyncHttpServer instance.

### respond

[ref: #symbol-respond]

Responds to the request with the specified HttpCode, headers and content.

**Input:**
- `req: Request`
- `code: HttpCode`
- `content: string`
- `headers: HttpHeaders = nil`

**Output:** `Future[void]`
**Pragmas:** `raises: [Exception, SslError, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, SslError, ValueError`, `tags: RootEffect`, `forbids: `

Responds to the request with the specified HttpCode, headers and content.

This procedure will **not** close the client socket.

Example:

```
import std/json
proc handler(req: Request) {.async.} =
  if req.url.path == "/hello-world":
    let msg = %* {"message": "Hello World"}
    let headers = newHttpHeaders([("Content-Type","application/json")])
    await req.respond(Http200, $msg, headers)
  else:
    await req.respond(Http404, "Not Found")
```

### sendHeaders

[ref: #symbol-sendheaders]

**Input:**
- `req: Request`
- `headers: HttpHeaders`

**Output:** `Future[void]`
**Pragmas:** `raises: [Exception, SslError, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, SslError, ValueError`, `tags: RootEffect`, `forbids: `

Sends the specified headers to the requesting client.

### serve

[ref: #symbol-serve]

Starts the process of listening for incoming HTTP connections on the specified address and port.

**Input:**
- `server: AsyncHttpServer`
- `port: Port`
- `callback: proc (request: Request): Future[void] {.closure, gcsafe.}`
- `address:  = ""`
- `assumedDescriptorsPerRequest:  = -1`
- `domain:  = AF_INET`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, OSError, ValueError, SslError, LibraryError, KeyError]`, `tags: [RootEffect, WriteIOEffect, ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: Exception, OSError, ValueError, SslError, LibraryError, KeyError`, `tags: RootEffect, WriteIOEffect, ReadIOEffect, TimeEffect`, `forbids: `

Starts the process of listening for incoming HTTP connections on the specified address and port.

When a request is made by a client the specified callback will be called.

If assumedDescriptorsPerRequest is 0 or greater the server cares about the process's maximum file descriptor limit. It then ensures that the process still has the resources for assumedDescriptorsPerRequest file descriptors before accepting a connection.

You should prefer to call acceptRequest instead with a custom server loop so that you're in control over the error handling and logging.

### shouldAcceptRequest

[ref: #symbol-shouldacceptrequest]

**Input:**
- `server: AsyncHttpServer`
- `assumedDescriptorsPerRequest:  = 5`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if the process's current number of opened file descriptors is still within the maximum limit and so it's reasonable to accept yet another request.

## Type

### AsyncHttpServer

[ref: #symbol-asynchttpserver]

```nim
AsyncHttpServer = ref object
```

### Request

[ref: #symbol-request]

```nim
Request = object
  client*: AsyncSocket
  reqMethod*: HttpMethod
  headers*: HttpHeaders
  protocol*: tuple[orig: string, major, minor: int]
  url*: Uri
  hostname*: string          ## The hostname of the client that made the request.
  body*: string
```
