---
source_hash: 743132ff7529b301
source_path: lib/pure/httpclient.nim
---

### newMultipartData

[ref: #symbol-newmultipartdata]

Create a new multipart data object and fill it with the entries xs directly.

**Input:**
- `xs: MultipartEntries`

**Output:** `MultipartData`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Create a new multipart data object and fill it with the entries xs directly.

```
var data = newMultipartData({"action": "login", "format": "json"})
```

### newProxy

[ref: #symbol-newproxy]

**Input:**
- `url: Uri`

**Output:** `Proxy`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructs a new TProxy object.

### newProxy

[ref: #symbol-newproxy]

**Input:**
- `url: string`

**Output:** `Proxy`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructs a new TProxy object.

### newProxy

[ref: #symbol-newproxy]

**Input:**
- `url: Uri`
- `auth: string`

**Output:** `Proxy`
**Pragmas:** `deprecated: "Provide auth in url instead"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### newProxy

[ref: #symbol-newproxy]

**Input:**
- `url: string`
- `auth: string`

**Output:** `Proxy`
**Pragmas:** `deprecated: "Provide auth in url instead"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### patch

[ref: #symbol-patch]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a PATCH request. This procedure uses httpClient values such as client.maxRedirects.

### patch

[ref: #symbol-patch]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Response`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and performs a PATCH request. This procedure uses httpClient values such as client.maxRedirects.

### patchContent

[ref: #symbol-patchcontent]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Future[string]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and returns the content of a PATCH request.

### patchContent

[ref: #symbol-patchcontent]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `string`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and returns the content of a PATCH request.

### post

[ref: #symbol-post]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a POST request. This procedure uses httpClient values such as client.maxRedirects.

### post

[ref: #symbol-post]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Response`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and performs a POST request. This procedure uses httpClient values such as client.maxRedirects.

### postContent

[ref: #symbol-postcontent]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Future[string]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and returns the content of a POST request.

### postContent

[ref: #symbol-postcontent]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `string`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and returns the content of a POST request.

### put

[ref: #symbol-put]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a PUT request. This procedure uses httpClient values such as client.maxRedirects.

### put

[ref: #symbol-put]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Response`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and performs a PUT request. This procedure uses httpClient values such as client.maxRedirects.

### putContent

[ref: #symbol-putcontent]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `Future[string]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL andreturns the content of a PUT request.

### putContent

[ref: #symbol-putcontent]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `body:  = ""`
- `multipart: MultipartData = nil`

**Output:** `string`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL andreturns the content of a PUT request.

### request

[ref: #symbol-request]

Connects to the hostname specified by the URL and performs a request using the custom method string specified by httpMethod.

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `httpMethod: HttpMethod | string = HttpGet`
- `body:  = ""`
- `headers: HttpHeaders = nil`
- `multipart: MultipartData = nil`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`, `httpMethod:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a request using the custom method string specified by httpMethod.

Connection will be kept alive. Further requests on the same client to the same hostname will not require a new connection to be made. The connection can be closed by using the close procedure.

This procedure will follow redirects up to a maximum number of redirects specified in client.maxRedirects.

You need to make sure that the url doesn't contain any newline characters. Failing to do so will raise AssertionDefect.

headers are HTTP headers that override the client.headers for this specific request only and will not be persisted.

**Deprecated since v1.5**: use HttpMethod enum instead; string parameter httpMethod is deprecated

### request

[ref: #symbol-request]

Connects to the hostname specified by the URL and performs a request using the custom method string specified by httpMethod.

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `httpMethod: HttpMethod | string = HttpGet`
- `body:  = ""`
- `headers: HttpHeaders = nil`
- `multipart: MultipartData = nil`

**Output:** `Response`
**Generic parameters:** `url:type`, `httpMethod:type`

Connects to the hostname specified by the URL and performs a request using the custom method string specified by httpMethod.

Connection will be kept alive. Further requests on the same client to the same hostname will not require a new connection to be made. The connection can be closed by using the close procedure.

This procedure will follow redirects up to a maximum number of redirects specified in client.maxRedirects.

You need to make sure that the url doesn't contain any newline characters. Failing to do so will raise AssertionDefect.

headers are HTTP headers that override the client.headers for this specific request only and will not be persisted.

**Deprecated since v1.5**: use HttpMethod enum instead; string parameter httpMethod is deprecated

## Type

### AsyncHttpClient

[ref: #symbol-asynchttpclient]

```nim
AsyncHttpClient = HttpClientBase[AsyncSocket]
```

### AsyncResponse

[ref: #symbol-asyncresponse]

```nim
AsyncResponse = ref object
  version*: string
  status*: string
  headers*: HttpHeaders
  bodyStream*: FutureStream[string]
```

### HttpClient

[ref: #symbol-httpclient]

```nim
HttpClient = HttpClientBase[Socket]
```

### HttpClientBase

[ref: #symbol-httpclientbase]

```nim
HttpClientBase[SocketType] = ref object
  headers*: HttpHeaders      ## Headers to send in requests.
  timeout*: int              ## Only used for blocking HttpClient for now.
  when SocketType is Socket:
    onProgressChanged*: ProgressChangedProc[void]
  else:
    onProgressChanged*: ProgressChangedProc[Future[void]]
  when defined(ssl):
  when SocketType is AsyncSocket:
  else:
```

### HttpRequestError

[ref: #symbol-httprequesterror]

```nim
HttpRequestError = object of IOError
```

Thrown in the getContent proc and postContent proc, when the server returns an error

### MultipartData

[ref: #symbol-multipartdata]

```nim
MultipartData = ref object
```

### MultipartEntries

[ref: #symbol-multipartentries]

```nim
MultipartEntries = openArray[tuple[name, content: string]]
```

### ProgressChangedProc

[ref: #symbol-progresschangedproc]

```nim
ProgressChangedProc[ReturnType] = proc (total, progress, speed: BiggestInt): ReturnType {.
    closure, gcsafe.}
```

### ProtocolError

[ref: #symbol-protocolerror]

```nim
ProtocolError = object of IOError
```

exception that is raised when server does not conform to the implemented protocol

### Proxy

[ref: #symbol-proxy]

```nim
Proxy = ref object
  url*: Uri
```

### Response

[ref: #symbol-response]

```nim
Response = ref object
  version*: string
  status*: string
  headers*: HttpHeaders
  bodyStream*: Stream
```

[Prev](httpclient_1.md)
