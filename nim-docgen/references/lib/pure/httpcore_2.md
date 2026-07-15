---
source_hash: bffe575f764e3235
source_path: lib/pure/httpcore.nim
---

### HttpMethod

[ref: #symbol-httpmethod]

```nim
HttpMethod = enum
  HttpHead = "HEAD",        ## Asks for the response identical to the one that
                             ## would correspond to a GET request, but without
                             ## the response body.
  HttpGet = "GET",          ## Retrieves the specified resource.
  HttpPost = "POST",        ## Submits data to be processed to the identified
                             ## resource. The data is included in the body of
                             ## the request.
  HttpPut = "PUT",          ## Uploads a representation of the specified
                             ## resource.
  HttpDelete = "DELETE",    ## Deletes the specified resource.
  HttpTrace = "TRACE",      ## Echoes back the received request, so that a
                             ## client
                             ## can see what intermediate servers are adding or
                             ## changing in the request.
  HttpOptions = "OPTIONS",  ## Returns the HTTP methods that the server
                             ## supports for specified address.
  HttpConnect = "CONNECT",  ## Converts the request connection to a transparent
                             ## TCP/IP tunnel, usually used for proxies.
  HttpPatch = "PATCH"        ## Applies partial modifications to a resource.
```

the requested HttpMethod

### HttpVersion

[ref: #symbol-httpversion]

```nim
HttpVersion = enum
  HttpVer11, HttpVer10
```

[Prev](httpcore_1.md)
