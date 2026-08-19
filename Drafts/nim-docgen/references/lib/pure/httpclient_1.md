---
source_hash: 743132ff7529b301
source_path: lib/pure/httpclient.nim
---

# httpclient

[ref: #module-httpclient]

This module implements a simple HTTP client that can be used to retrieve webpages and other data.

**Warning:**
Validate untrusted inputs: URI parsers and getters are not detecting malicious URIs.

# [Retrieving a website](#retrieving-a-website)

This example uses HTTP GET to retrieve http://google.com:

```
import std/httpclient
var client = newHttpClient()
try:
  echo client.getContent("http://google.com")
finally:
  client.close()
```

The same action can also be performed asynchronously, simply use the AsyncHttpClient:

```
import std/[asyncdispatch, httpclient]

proc asyncProc(): Future[string] {.async.} =
  var client = newAsyncHttpClient()
  try:
    return await client.getContent("http://google.com")
  finally:
    client.close()

echo waitFor asyncProc()
```

The functionality implemented by HttpClient and AsyncHttpClient is the same, so you can use whichever one suits you best in the examples shown here.

**Note:** You need to run asynchronous examples in an async proc otherwise you will get an Undeclared identifier: 'await' error.

**Note:** An asynchronous client instance can only deal with one request at a time. To send multiple requests in parallel, use multiple client instances.

# [Using HTTP POST](#using-http-post)

This example demonstrates the usage of the W3 HTML Validator, it uses multipart/form-data as the Content-Type to send the HTML to be validated to the server.

```
import std/[httpclient]
var client = newHttpClient()
var data = newMultipartData()
data["output"] = "soap12"
data["uploaded_file"] = ("test.html", "text/html",
  "<html><head></head><body><p>test</p></body></html>")
try:
  echo client.postContent("http://validator.w3.org/check", multipart=data)
finally:
  client.close()
```

To stream files from disk when performing the request, use addFiles.

**Note:** This will allocate a new Mimetypes database every time you call it, you can pass your own via the mimeDb parameter to avoid this.

```
import std/[httpclient, mimetypes]
let mimes = newMimetypes()
var client = newHttpClient()
var data = newMultipartData()
data.addFiles({"uploaded_file": "test.html"}, mimeDb = mimes)
try:
  echo client.postContent("http://validator.w3.org/check", multipart=data)
finally:
  client.close()
```

You can also make post requests with custom headers. This example sets Content-Type to application/json and uses a json object for the body

```
import std/[httpclient, json]

let client = newHttpClient()
client.headers = newHttpHeaders({ "Content-Type": "application/json" })
let body = %*{
    "data": "some text"
}
try:
  let response = client.request("http://some.api", httpMethod = HttpPost, body = $body)
  echo response.status
finally:
  client.close()
```

# [Progress reporting](#progress-reporting)

You may specify a callback procedure to be called during an HTTP request. This callback will be executed every second with information about the progress of the HTTP request.

```
import std/[asyncdispatch, httpclient]

proc onProgressChanged(total, progress, speed: BiggestInt) {.async.} =
  echo("Downloaded ", progress, " of ", total)
  echo("Current rate: ", speed div 1000, "kb/s")

proc asyncProc() {.async.} =
  var client = newAsyncHttpClient()
  client.onProgressChanged = onProgressChanged
  try:
    discard await client.getContent("http://speedtest-ams2.digitalocean.com/100mb.test")
  finally:
    client.close()

waitFor asyncProc()
```

If you would like to remove the callback simply set it to nil.

```
client.onProgressChanged = nil
```

**Warning:**
The total reported by httpclient may be 0 in some cases.

# [SSL/TLS support](#sslslashtls-support)

This requires the OpenSSL library. Fortunately it's widely used and installed on many operating systems. httpclient will use SSL automatically if you give any of the functions a url with the https schema, for example: https://github.com/.

You will also have to compile with ssl defined like so: nim c -d:ssl ....

Certificate validation is performed by default.

A set of directories and files from the [ssl\_certs](ssl_certs.html) module are scanned to locate CA certificates.

Example of setting SSL verification parameters in a new client:

```
import std/[net, httpclient]
var client = newHttpClient(sslContext=newContext(verifyMode=CVerifyPeer))
```

There are three options for verify mode:

* CVerifyNone: certificates are not verified;
* CVerifyPeer: certificates are verified;
* CVerifyPeerUseEnvVars: certificates are verified and the optional environment variables SSL\_CERT\_FILE and SSL\_CERT\_DIR are also used to locate certificates

See [newContext](net.html#newContext.string,string,string,string) to tweak or disable certificate validation.

# [Timeouts](#timeouts)

Currently only the synchronous functions support a timeout. The timeout is measured in milliseconds, once it is set any call on a socket which may block will be susceptible to this timeout.

It may be surprising but the function as a whole can take longer than the specified timeout, only individual internal calls on the socket are affected. In practice this means that as long as the server is sending data an exception will not be raised, if however data does not reach the client within the specified timeout a TimeoutError exception will be raised.

Here is how to set a timeout when creating an HttpClient instance:

```
import std/httpclient

let client = newHttpClient(timeout = 42)
```

# [Proxy](#proxy)

A proxy can be specified as a param to any of the procedures defined in this module. To do this, use the newProxy constructor. Unfortunately, only basic authentication is supported at the moment.

Some examples on how to configure a Proxy for HttpClient:

```
import std/httpclient

let myProxy = newProxy("http://myproxy.network")
let client = newHttpClient(proxy = myProxy)
```

Use proxies with basic authentication:

```
import std/httpclient

let myProxy = newProxy("http://user:password@myproxy.network")
let client = newHttpClient(proxy = myProxy)
```

SOCKS5 proxy with proxy-side DNS resolving:

```
import std/httpclient

let myProxy = newProxy("socks5h://user:password@myproxy.network")
let client = newHttpClient(proxy = myProxy)
```

Get Proxy URL from environment variables:

```
import std/httpclient

var url = ""
try:
  if existsEnv("http_proxy"):
    url = getEnv("http_proxy")
  elif existsEnv("https_proxy"):
    url = getEnv("https_proxy")
except ValueError:
  echo "Unable to parse proxy from environment variables."

let myProxy = newProxy(url = url)
let client = newHttpClient(proxy = myProxy)
```

# [Redirects](#redirects)

The maximum redirects can be set with the maxRedirects of int type, it specifies the maximum amount of redirects to follow, it defaults to 5, you can set it to 0 to disable redirects.

Here you can see an example about how to set the maxRedirects of HttpClient:

```
import std/httpclient

let client = newHttpClient(maxRedirects = 0)
```

## Examples

```nim
import std/httpclient
var client = newHttpClient()
try:
  echo client.getContent("http://google.com")
finally:
  client.close()
```

```nim
import std/[asyncdispatch, httpclient]

proc asyncProc(): Future[string] {.async.} =
  var client = newAsyncHttpClient()
  try:
    return await client.getContent("http://google.com")
  finally:
    client.close()

echo waitFor asyncProc()
```

```nim
import std/[httpclient]
var client = newHttpClient()
var data = newMultipartData()
data["output"] = "soap12"
data["uploaded_file"] = ("test.html", "text/html",
  "<html><head></head><body><p>test</p></body></html>")
try:
  echo client.postContent("http://validator.w3.org/check", multipart=data)
finally:
  client.close()
```

```nim
import std/[httpclient, mimetypes]
let mimes = newMimetypes()
var client = newHttpClient()
var data = newMultipartData()
data.addFiles({"uploaded_file": "test.html"}, mimeDb = mimes)
try:
  echo client.postContent("http://validator.w3.org/check", multipart=data)
finally:
  client.close()
```

```nim
import std/[httpclient, json]

let client = newHttpClient()
client.headers = newHttpHeaders({ "Content-Type": "application/json" })
let body = %*{
    "data": "some text"
}
try:
  let response = client.request("http://some.api", httpMethod = HttpPost, body = $body)
  echo response.status
finally:
  client.close()
```

```nim
import std/[asyncdispatch, httpclient]

proc onProgressChanged(total, progress, speed: BiggestInt) {.async.} =
  echo("Downloaded ", progress, " of ", total)
  echo("Current rate: ", speed div 1000, "kb/s")

proc asyncProc() {.async.} =
  var client = newAsyncHttpClient()
  client.onProgressChanged = onProgressChanged
  try:
    discard await client.getContent("http://speedtest-ams2.digitalocean.com/100mb.test")
  finally:
    client.close()

waitFor asyncProc()
```

```nim
client.onProgressChanged = nil
```

```nim
import std/[net, httpclient]
var client = newHttpClient(sslContext=newContext(verifyMode=CVerifyPeer))
```

```nim
import std/httpclient

let client = newHttpClient(timeout = 42)
```

```nim
import std/httpclient

let myProxy = newProxy("http://myproxy.network")
let client = newHttpClient(proxy = myProxy)
```

```nim
import std/httpclient

let myProxy = newProxy("http://user:password@myproxy.network")
let client = newHttpClient(proxy = myProxy)
```

```nim
import std/httpclient

let myProxy = newProxy("socks5h://user:password@myproxy.network")
let client = newHttpClient(proxy = myProxy)
```

```nim
import std/httpclient

var url = ""
try:
  if existsEnv("http_proxy"):
    url = getEnv("http_proxy")
  elif existsEnv("https_proxy"):
    url = getEnv("https_proxy")
except ValueError:
  echo "Unable to parse proxy from environment variables."

let myProxy = newProxy(url = url)
let client = newHttpClient(proxy = myProxy)
```

```nim
import std/httpclient

let client = newHttpClient(maxRedirects = 0)
```

```nim
data["username"] = "NimUser"
```

```nim
data["uploaded_file"] = ("test.html", "text/html",
  "<html><head></head><body><p>test</p></body></html>")
```

```nim
data.add({"action": "login", "format": "json"})
```

```nim
data.addFiles({"uploaded_file": "public/test.html"})
```

```nim
if client.connected:
  echo client.getSocket.getLocalAddr
  echo client.getSocket.getPeerAddr
```

```nim
import std/[asyncdispatch, strutils]

proc asyncProc(): Future[string] {.async.} =
  let client = newAsyncHttpClient()
  result = await client.getContent("http://example.com")

let exampleHtml = waitFor asyncProc()
assert "Example Domain" in exampleHtml
assert "Pizza" notin exampleHtml
```

```nim
import std/strutils

let exampleHtml = newHttpClient().getContent("http://example.com")
assert "Example Domain" in exampleHtml
assert "Pizza" notin exampleHtml
```

```nim
var data = newMultipartData({"action": "login", "format": "json"})
```

## Const

### defUserAgent

[ref: #symbol-defuseragent]

```nim
defUserAgent = "Nim-httpclient/2.2.11"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `data: MultipartData`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

convert MultipartData to string so it's human readable when echo see <https://github.com/nim-lang/Nim/issues/11863>

### `[]=`

[ref: #symbol-]

Add a multipart entry to the multipart data p. The value is added without a filename and without a content type.

**Input:**
- `p: MultipartData`
- `name: string`
- `content: string`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Add a multipart entry to the multipart data p. The value is added without a filename and without a content type.

```
data["username"] = "NimUser"
```

### `[]=`

[ref: #symbol-]

Add a file to the multipart data p, specifying filename, contentType and content manually.

**Input:**
- `p: MultipartData`
- `name: string`
- `file: tuple[name, contentType, content: string]`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Add a file to the multipart data p, specifying filename, contentType and content manually.

```
data["uploaded_file"] = ("test.html", "text/html",
  "<html><head></head><body><p>test</p></body></html>")
```

### add

[ref: #symbol-add]

Add a value to the multipart data.

**Input:**
- `p: MultipartData`
- `name: string`
- `content: string`
- `filename: string = ""`
- `contentType: string = ""`
- `useStream:  = true`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Add a value to the multipart data.

When useStream is false, the file will be read into memory.

Raises a ValueError exception if name, filename or contentType contain newline characters.

### add

[ref: #symbol-add]

Add a list of multipart entries to the multipart data p. All values are added without a filename and without a content type.

**Input:**
- `p: MultipartData`
- `xs: MultipartEntries`

**Output:** `MultipartData`
**Pragmas:** `discardable`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Add a list of multipart entries to the multipart data p. All values are added without a filename and without a content type.

```
data.add({"action": "login", "format": "json"})
```

### addFiles

[ref: #symbol-addfiles]

Add files to a multipart data object. The files will be streamed from disk when the request is being made. When stream is false, the files are instead read into memory, but beware this is very memory ineffecient even for small files. The MIME types will automatically be determined. Raises an IOError if the file cannot be opened or reading fails. To manually specify file content, filename and MIME type, use []= instead.

**Input:**
- `p: MultipartData`
- `xs: openArray[tuple[name, file: string]]`
- `mimeDb:  = newMimetypes()`
- `useStream:  = true`

**Output:** `MultipartData`
**Pragmas:** `discardable`, `raises: [IOError, ValueError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, ValueError`, `tags: ReadIOEffect`, `forbids: `

Add files to a multipart data object. The files will be streamed from disk when the request is being made. When stream is false, the files are instead read into memory, but beware this is very memory ineffecient even for small files. The MIME types will automatically be determined. Raises an IOError if the file cannot be opened or reading fails. To manually specify file content, filename and MIME type, use []= instead.

```
data.addFiles({"uploaded_file": "public/test.html"})
```

### auth

[ref: #symbol-auth]

**Input:**
- `p: Proxy`

**Output:** `string`
**Pragmas:** `deprecated: "Get auth from p.url.username and p.url.password"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### body

[ref: #symbol-body]

Retrieves the specified response's body.

**Input:**
- `response: Response`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Retrieves the specified response's body.

The response's body stream is read synchronously.

### body

[ref: #symbol-body]

**Input:**
- `response: AsyncResponse`

**Output:** `Future[string]`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Reads the response's body and caches it. The read is performed only once.

### close

[ref: #symbol-close]

**Input:**
- `client: HttpClient | AsyncHttpClient`

**Output:** *(none)*
**Generic parameters:** `client:type`

Closes any connections held by the HTTP client.

### code

[ref: #symbol-code]

Retrieves the specified response's HttpCode.

**Input:**
- `response: Response | AsyncResponse`

**Output:** `HttpCode`
**Generic parameters:** `response:type`

**Pragmas:** `raises: [ValueError, OverflowDefect]`

**Effects:** `raises: ValueError, OverflowDefect`

Retrieves the specified response's HttpCode.

Raises a ValueError if the response's status does not have a corresponding HttpCode.

### contentLength

[ref: #symbol-contentlength]

Retrieves the specified response's content length.

**Input:**
- `response: Response | AsyncResponse`

**Output:** `int`
**Generic parameters:** `response:type`

Retrieves the specified response's content length.

This is effectively the value of the "Content-Length" header.

A ValueError exception will be raised if the value is not an integer. If the Content-Length header is not set in the response, ContentLength is set to the value -1.

### contentType

[ref: #symbol-contenttype]

Retrieves the specified response's content type.

**Input:**
- `response: Response | AsyncResponse`

**Output:** `string`
**Generic parameters:** `response:type`

**Pragmas:** `inline`

Retrieves the specified response's content type.

This is effectively the value of the "Content-Type" header.

### delete

[ref: #symbol-delete]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a DELETE request. This procedure uses httpClient values such as client.maxRedirects.

### delete

[ref: #symbol-delete]

**Input:**
- `client: HttpClient`
- `url: Uri | string`

**Output:** `Response`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and performs a DELETE request. This procedure uses httpClient values such as client.maxRedirects.

### deleteContent

[ref: #symbol-deletecontent]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`

**Output:** `Future[string]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and returns the content of a DELETE request.

### deleteContent

[ref: #symbol-deletecontent]

**Input:**
- `client: HttpClient`
- `url: Uri | string`

**Output:** `string`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and returns the content of a DELETE request.

### downloadFile

[ref: #symbol-downloadfile]

**Input:**
- `client: HttpClient`
- `url: Uri | string`
- `filename: string`

**Output:** *(none)*
**Generic parameters:** `url:type`

Downloads url and saves it to filename.

### downloadFile

[ref: #symbol-downloadfile]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`
- `filename: string`

**Output:** `Future[void]`
**Generic parameters:** `url:type`

### get

[ref: #symbol-get]

Connects to the hostname specified by the URL and performs a GET request.

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a GET request.

This procedure uses httpClient values such as client.maxRedirects.

### get

[ref: #symbol-get]

Connects to the hostname specified by the URL and performs a GET request.

**Input:**
- `client: HttpClient`
- `url: Uri | string`

**Output:** `Response`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and performs a GET request.

This procedure uses httpClient values such as client.maxRedirects.

### getContent

[ref: #symbol-getcontent]

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`

**Output:** `Future[string]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and returns the content of a GET request.

### getContent

[ref: #symbol-getcontent]

**Input:**
- `client: HttpClient`
- `url: Uri | string`

**Output:** `string`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and returns the content of a GET request.

### getSocket

[ref: #symbol-getsocket]

Get network socket, useful if you want to find out more details about the connection.

**Input:**
- `client: HttpClient`

**Output:** `Socket`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get network socket, useful if you want to find out more details about the connection.

This example shows info about local and remote endpoints:

```
if client.connected:
  echo client.getSocket.getLocalAddr
  echo client.getSocket.getPeerAddr
```

### getSocket

[ref: #symbol-getsocket]

**Input:**
- `client: AsyncHttpClient`

**Output:** `AsyncSocket`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### head

[ref: #symbol-head]

Connects to the hostname specified by the URL and performs a HEAD request.

**Input:**
- `client: AsyncHttpClient`
- `url: Uri | string`

**Output:** `Future[AsyncResponse]`
**Generic parameters:** `url:type`

**Pragmas:** `stackTrace: false`

Connects to the hostname specified by the URL and performs a HEAD request.

This procedure uses httpClient values such as client.maxRedirects.

### head

[ref: #symbol-head]

Connects to the hostname specified by the URL and performs a HEAD request.

**Input:**
- `client: HttpClient`
- `url: Uri | string`

**Output:** `Response`
**Generic parameters:** `url:type`

Connects to the hostname specified by the URL and performs a HEAD request.

This procedure uses httpClient values such as client.maxRedirects.

### lastModified

[ref: #symbol-lastmodified]

Retrieves the specified response's last modified time.

**Input:**
- `response: Response | AsyncResponse`

**Output:** `DateTime`
**Generic parameters:** `response:type`

Retrieves the specified response's last modified time.

This is effectively the value of the "Last-Modified" header.

Raises a ValueError if the parsing fails or the value is not a correctly formatted time.

### newAsyncHttpClient

[ref: #symbol-newasynchttpclient]

Creates a new AsyncHttpClient instance.

**Input:**
- `userAgent:  = defUserAgent`
- `maxRedirects:  = 5`
- `sslContext:  = getDefaultSSL()`
- `proxy: Proxy = nil`
- `headers:  = newHttpHeaders()`

**Output:** `AsyncHttpClient`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new AsyncHttpClient instance.

userAgent specifies the user agent that will be used when making requests.

maxRedirects specifies the maximum amount of redirects to follow, default is 5.

sslContext specifies the SSL context to use for HTTPS requests.

proxy specifies an HTTP proxy to use for this HTTP client's connections.

headers specifies the HTTP Headers.

### newHttpClient

[ref: #symbol-newhttpclient]

Creates a new HttpClient instance.

**Input:**
- `userAgent:  = defUserAgent`
- `maxRedirects:  = 5`
- `sslContext:  = getDefaultSSL()`
- `proxy: Proxy = nil`
- `timeout:  = -1`
- `headers:  = newHttpHeaders()`

**Output:** `HttpClient`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new HttpClient instance.

userAgent specifies the user agent that will be used when making requests.

maxRedirects specifies the maximum amount of redirects to follow, default is 5.

sslContext specifies the SSL context to use for HTTPS requests. See [SSL/TLS support](#sslslashtls-support)

proxy specifies an HTTP proxy to use for this HTTP client's connections.

timeout specifies the number of milliseconds to allow before a TimeoutError is raised.

headers specifies the HTTP Headers.

### newMultipartData

[ref: #symbol-newmultipartdata]

**Input:**
- *(none)*

**Output:** `MultipartData`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructs a new MultipartData object.


[Next](httpclient_2.md)
