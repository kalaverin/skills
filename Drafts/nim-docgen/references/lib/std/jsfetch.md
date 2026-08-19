---
source_hash: b9b640144fafe814
source_path: lib/std/jsfetch.nim
---

# jsfetch

[ref: #module-jsfetch]

* Fetch for the JavaScript target: <https://developer.mozilla.org/docs/Web/API/Fetch_API>

## Examples

```nim
import std/jsfetch
import std/[asyncjs, jsconsole, jsformdata, jsheaders]
from std/httpcore import HttpMethod
from std/jsffi import JsObject
from std/sugar import `=>`

block:
  let options0: FetchOptions = unsafeNewFetchOptions(
    metod = "POST".cstring,
    body = """{"key": "value"}""".cstring,
    mode = "no-cors".cstring,
    credentials = "omit".cstring,
    cache = "no-cache".cstring,
    referrerPolicy = "no-referrer".cstring,
    keepalive = false,
    redirect = "follow".cstring,
    referrer = "client".cstring,
    integrity = "".cstring,
    headers = newHeaders()
  )
  assert options0.keepalive == false
  assert options0.metod == "POST".cstring
  assert options0.body == """{"key": "value"}""".cstring
  assert options0.mode == "no-cors".cstring
  assert options0.credentials == "omit".cstring
  assert options0.cache == "no-cache".cstring
  assert options0.referrerPolicy == "no-referrer".cstring
  assert options0.redirect == "follow".cstring
  assert options0.referrer == "client".cstring
  assert options0.integrity == "".cstring
  assert options0.headers.len == 0

block:
  let options1: FetchOptions = newFetchOptions(
    metod =  HttpPost,
    body = """{"key": "value"}""".cstring,
    mode = fmNoCors,
    credentials = fcOmit,
    cache = fchNoCache,
    referrerPolicy = frpNoReferrer,
    keepalive = false,
    redirect = frFollow,
    referrer = "client".cstring,
    integrity = "".cstring,
    headers = newHeaders()
  )
  assert options1.keepalive == false
  assert options1.metod == $HttpPost
  assert options1.body == """{"key": "value"}""".cstring
  assert options1.mode == $fmNoCors
  assert options1.credentials == $fcOmit
  assert options1.cache == $fchNoCache
  assert options1.referrerPolicy == $frpNoReferrer
  assert options1.redirect == $frFollow
  assert options1.referrer == "client".cstring
  assert options1.integrity == "".cstring
  assert options1.headers.len == 0

block:
  let response: Response = newResponse(body = "-. .. --".cstring)
  let request: Request = newRequest(url = "http://nim-lang.org".cstring)

if not defined(nodejs):
  block:
    proc doFetch(): Future[Response] {.async.} =
      fetch "https://httpbin.org/get".cstring

    proc example() {.async.} =
      let response: Response = await doFetch()
      assert response.ok
      assert response.status == 200.cint
      assert response.headers is Headers
      assert response.body is cstring

    discard example()

  block:
    proc example2 {.async.} =
      await fetch("https://api.github.com/users/torvalds".cstring)
        .then((response: Response) => response.json())
        .then((json: JsObject) => console.log(json))
        .catch((err: Error) => console.log("Request Failed", err))

    discard example2()
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `self: Request | Response | FetchOptions`

**Output:** `string`
**Generic parameters:** `self:type`

### clone

[ref: #symbol-clone]

**Input:**
- `self: Response | Request`

**Output:** `Response`
**Generic parameters:** `self:type`

**Pragmas:** `importjs: "#.$1()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Response/clone>

### fetch

[ref: #symbol-fetch]

**Input:**
- `url: cstring | Request`

**Output:** `Future[Response]`
**Generic parameters:** `url:type`

**Pragmas:** `importjs: "$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

fetch() API, simple GET only, returns a Future[Response].

### fetch

[ref: #symbol-fetch]

**Input:**
- `url: cstring | Request`
- `options: FetchOptions`

**Output:** `Future[Response]`
**Generic parameters:** `url:type`

**Pragmas:** `importjs: "$1(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

fetch() API that takes a FetchOptions, returns a Future[Response].

### formData

[ref: #symbol-formdata]

**Input:**
- `self: Response`

**Output:** `Future[FormData]`
**Pragmas:** `importjs: "#.$1()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Response/formData>

### json

[ref: #symbol-json]

**Input:**
- `self: Response`

**Output:** `Future[JsObject]`
**Pragmas:** `importjs: "#.$1()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Response/json>

### newfetchOptions

[ref: #symbol-newfetchoptions]

**Input:**
- `metod:  = HttpGet`
- `body: cstring = nil`
- `mode:  = fmCors`
- `credentials:  = fcSameOrigin`
- `cache:  = fchDefault`
- `referrerPolicy:  = frpNoReferrerWhenDowngrade`
- `keepalive:  = false`
- `redirect:  = frFollow`
- `referrer:  = "client".cstring`
- `integrity:  = "".cstring`
- `headers: Headers = newHeaders()`

**Output:** `FetchOptions`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for FetchOptions.

### newRequest

[ref: #symbol-newrequest]

**Input:**
- `url: cstring`

**Output:** `Request`
**Pragmas:** `importjs: "(new Request(#))"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for Request. This does *not* call fetch(). Same as new Request().

### newRequest

[ref: #symbol-newrequest]

**Input:**
- `url: cstring`
- `fetchOptions: FetchOptions`

**Output:** `Request`
**Pragmas:** `importjs: "(new Request(#, #))"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for Request with fetchOptions. Same as fetch(url, fetchOptions).

### newResponse

[ref: #symbol-newresponse]

**Input:**
- `body: cstring | FormData`

**Output:** `Response`
**Generic parameters:** `body:type`

**Pragmas:** `importjs: "(new Response(#))"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for Response. This does *not* call fetch(). Same as new Response().

### text

[ref: #symbol-text]

**Input:**
- `self: Response`

**Output:** `Future[cstring]`
**Pragmas:** `importjs: "#.$1()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Response/text>

### toCstring

[ref: #symbol-tocstring]

**Input:**
- `self: Request | Response | FetchOptions`

**Output:** `cstring`
**Generic parameters:** `self:type`

**Pragmas:** `importjs: "JSON.stringify(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### unsafeNewFetchOptions

[ref: #symbol-unsafenewfetchoptions]

**Warning:**

**Input:**
- `metod: cstring`
- `body: cstring`
- `mode: cstring`
- `credentials: cstring`
- `cache: cstring`
- `referrerPolicy: cstring`
- `keepalive: bool`
- `redirect:  = "follow".cstring`
- `referrer:  = "client".cstring`
- `integrity:  = "".cstring`
- `headers: Headers = newHeaders()`

**Output:** `FetchOptions`
**Pragmas:** `importjs: "{method: #, body: #, mode: #, credentials: #, cache: #, referrerPolicy: #, keepalive: #, redirect: #, referrer: #, integrity: #, headers: #}"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

**Warning:**
Unsafe newfetchOptions.

## Type

### FetchCaches

[ref: #symbol-fetchcaches]

```nim
FetchCaches = enum
  fchDefault = "default", fchNoStore = "no-store", fchReload = "reload",
  fchNoCache = "no-cache", fchForceCache = "force-cache"
```

<https://developer.mozilla.org/docs/Web/API/Request/cache>

### FetchCredentials

[ref: #symbol-fetchcredentials]

```nim
FetchCredentials = enum
  fcInclude = "include", fcSameOrigin = "same-origin", fcOmit = "omit"
```

Credential options. See <https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials>

### FetchModes

[ref: #symbol-fetchmodes]

```nim
FetchModes = enum
  fmCors = "cors", fmNoCors = "no-cors", fmSameOrigin = "same-origin"
```

Mode options.

### FetchOptions

[ref: #symbol-fetchoptions]

```nim
FetchOptions = ref object of JsRoot
  keepalive*: bool
  metod* {.importjs: "method".}: cstring
  body*, integrity*, referrer*, mode*, credentials*, cache*, redirect*,
  referrerPolicy*: cstring
  headers*: Headers
```

Options for Fetch API.

### FetchRedirects

[ref: #symbol-fetchredirects]

```nim
FetchRedirects = enum
  frFollow = "follow", frError = "error", frManual = "manual"
```

Redirects options.

### FetchReferrerPolicies

[ref: #symbol-fetchreferrerpolicies]

```nim
FetchReferrerPolicies = enum
  frpNoReferrer = "no-referrer",
  frpNoReferrerWhenDowngrade = "no-referrer-when-downgrade",
  frpOrigin = "origin", frpOriginWhenCrossOrigin = "origin-when-cross-origin",
  frpUnsafeUrl = "unsafe-url"
```

Referrer Policy options.

### Request

[ref: #symbol-request]

```nim
Request = ref object of JsRoot
  bodyUsed*, ok*, redirected*: bool
  typ* {.importjs: "type".}: cstring
  url*, statusText*: cstring
  status*: cint
  headers*: Headers
  body*: cstring
```

<https://developer.mozilla.org/en-US/docs/Web/API/Request>

### Response

[ref: #symbol-response]

```nim
Response = ref object of JsRoot
  bodyUsed*, ok*, redirected*: bool
  typ* {.importjs: "type".}: cstring
  url*, statusText*: cstring
  status*: cint
  headers*: Headers
  body*: cstring
```

<https://developer.mozilla.org/en-US/docs/Web/API/Response>
