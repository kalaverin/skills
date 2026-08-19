---
source_hash: bffe575f764e3235
source_path: lib/pure/httpcore.nim
---

# httpcore

[ref: #module-httpcore]

Contains functionality shared between the httpclient and asynchttpserver modules.

Unstable API.

## Examples

```nim
doAssert($Http404 == "404 Not Found")
```

```nim
doAssert is1xx(HttpCode(103))
```

## Const

### headerLimit

[ref: #symbol-headerlimit]

```nim
headerLimit = 10000
```

### Http100

[ref: #symbol-http100]

```nim
Http100 = 100
```

### Http101

[ref: #symbol-http101]

```nim
Http101 = 101
```

### Http102

[ref: #symbol-http102]

```nim
Http102 = 102
```

<https://tools.ietf.org/html/rfc2518.html> WebDAV

### Http103

[ref: #symbol-http103]

```nim
Http103 = 103
```

<https://tools.ietf.org/html/rfc8297.html> Early hints

### Http200

[ref: #symbol-http200]

```nim
Http200 = 200
```

### Http201

[ref: #symbol-http201]

```nim
Http201 = 201
```

### Http202

[ref: #symbol-http202]

```nim
Http202 = 202
```

### Http203

[ref: #symbol-http203]

```nim
Http203 = 203
```

### Http204

[ref: #symbol-http204]

```nim
Http204 = 204
```

### Http205

[ref: #symbol-http205]

```nim
Http205 = 205
```

### Http206

[ref: #symbol-http206]

```nim
Http206 = 206
```

### Http207

[ref: #symbol-http207]

```nim
Http207 = 207
```

<https://tools.ietf.org/html/rfc4918.html> WebDAV

### Http208

[ref: #symbol-http208]

```nim
Http208 = 208
```

<https://tools.ietf.org/html/rfc5842.html> WebDAV, Section 7.1

### Http226

[ref: #symbol-http226]

```nim
Http226 = 226
```

<https://tools.ietf.org/html/rfc3229.html> Delta encoding, Section 10.4.1

### Http300

[ref: #symbol-http300]

```nim
Http300 = 300
```

### Http301

[ref: #symbol-http301]

```nim
Http301 = 301
```

### Http302

[ref: #symbol-http302]

```nim
Http302 = 302
```

### Http303

[ref: #symbol-http303]

```nim
Http303 = 303
```

### Http304

[ref: #symbol-http304]

```nim
Http304 = 304
```

### Http305

[ref: #symbol-http305]

```nim
Http305 = 305
```

### Http307

[ref: #symbol-http307]

```nim
Http307 = 307
```

### Http308

[ref: #symbol-http308]

```nim
Http308 = 308
```

### Http400

[ref: #symbol-http400]

```nim
Http400 = 400
```

### Http401

[ref: #symbol-http401]

```nim
Http401 = 401
```

### Http402

[ref: #symbol-http402]

```nim
Http402 = 402
```

<https://tools.ietf.org/html/rfc7231.html> Payment required, Section 6.5.2

### Http403

[ref: #symbol-http403]

```nim
Http403 = 403
```

### Http404

[ref: #symbol-http404]

```nim
Http404 = 404
```

### Http405

[ref: #symbol-http405]

```nim
Http405 = 405
```

### Http406

[ref: #symbol-http406]

```nim
Http406 = 406
```

### Http407

[ref: #symbol-http407]

```nim
Http407 = 407
```

### Http408

[ref: #symbol-http408]

```nim
Http408 = 408
```

### Http409

[ref: #symbol-http409]

```nim
Http409 = 409
```

### Http410

[ref: #symbol-http410]

```nim
Http410 = 410
```

### Http411

[ref: #symbol-http411]

```nim
Http411 = 411
```

### Http412

[ref: #symbol-http412]

```nim
Http412 = 412
```

### Http413

[ref: #symbol-http413]

```nim
Http413 = 413
```

### Http414

[ref: #symbol-http414]

```nim
Http414 = 414
```

### Http415

[ref: #symbol-http415]

```nim
Http415 = 415
```

### Http416

[ref: #symbol-http416]

```nim
Http416 = 416
```

### Http417

[ref: #symbol-http417]

```nim
Http417 = 417
```

### Http418

[ref: #symbol-http418]

```nim
Http418 = 418
```

### Http421

[ref: #symbol-http421]

```nim
Http421 = 421
```

### Http422

[ref: #symbol-http422]

```nim
Http422 = 422
```

### Http423

[ref: #symbol-http423]

```nim
Http423 = 423
```

<https://tools.ietf.org/html/rfc4918.html> WebDAV, Section 11.3

### Http424

[ref: #symbol-http424]

```nim
Http424 = 424
```

<https://tools.ietf.org/html/rfc4918.html> WebDAV, Section 11.3

### Http425

[ref: #symbol-http425]

```nim
Http425 = 425
```

<https://tools.ietf.org/html/rfc8470.html> Early data

### Http426

[ref: #symbol-http426]

```nim
Http426 = 426
```

### Http428

[ref: #symbol-http428]

```nim
Http428 = 428
```

### Http429

[ref: #symbol-http429]

```nim
Http429 = 429
```

### Http431

[ref: #symbol-http431]

```nim
Http431 = 431
```

### Http451

[ref: #symbol-http451]

```nim
Http451 = 451
```

### Http500

[ref: #symbol-http500]

```nim
Http500 = 500
```

### Http501

[ref: #symbol-http501]

```nim
Http501 = 501
```

### Http502

[ref: #symbol-http502]

```nim
Http502 = 502
```

### Http503

[ref: #symbol-http503]

```nim
Http503 = 503
```

### Http504

[ref: #symbol-http504]

```nim
Http504 = 504
```

### Http505

[ref: #symbol-http505]

```nim
Http505 = 505
```

### Http506

[ref: #symbol-http506]

```nim
Http506 = 506
```

<https://tools.ietf.org/html/rfc2295.html> Content negotiation, Section 8.1

### Http507

[ref: #symbol-http507]

```nim
Http507 = 507
```

<https://tools.ietf.org/html/rfc4918.html> WebDAV, Section 11.5

### Http508

[ref: #symbol-http508]

```nim
Http508 = 508
```

<https://tools.ietf.org/html/rfc5842.html> WebDAV, Section 7.2

### Http510

[ref: #symbol-http510]

```nim
Http510 = 510
```

<https://tools.ietf.org/html/rfc2774.html> Extension framework, Section 7

### Http511

[ref: #symbol-http511]

```nim
Http511 = 511
```

<https://tools.ietf.org/html/rfc6585.html> Additional status code, Section 6

### httpNewLine

[ref: #symbol-httpnewline]

```nim
httpNewLine = "\r\n"
```

## Iterator

### pairs

[ref: #symbol-pairs]

**Input:**
- `headers: HttpHeaders`

**Output:** `tuple[key, value: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields each key, value pair.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `headers: HttpHeaders`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `code: HttpCode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the specified HttpCode into a HTTP status.

### `==`

[ref: #symbol-]

**Input:**
- `protocol: tuple[orig: string, major, minor: int]`
- `ver: HttpVersion`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `a: HttpCode`
- `b: HttpCode`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]=`

[ref: #symbol-]

**Input:**
- `headers: HttpHeaders`
- `key: string`
- `value: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the header entries associated with key to the specified value. Replaces any existing values.

### `[]=`

[ref: #symbol-]

**Input:**
- `headers: HttpHeaders`
- `key: string`
- `value: seq[string]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the header entries associated with key to the specified list of values. Replaces any existing values. If value is empty, deletes the header entries associated with key.

### `[]`

[ref: #symbol-]

Returns the values associated with the given key. If the returned values are passed to a procedure expecting a string, the first value is automatically picked. If there are no values associated with the key, an exception is raised.

**Input:**
- `headers: HttpHeaders`
- `key: string`

**Output:** `HttpHeaderValues`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Returns the values associated with the given key. If the returned values are passed to a procedure expecting a string, the first value is automatically picked. If there are no values associated with the key, an exception is raised.

To access multiple values of a key, use the overloaded [] below or to get all of them access the table field directly.

### `[]`

[ref: #symbol-]

**Input:**
- `headers: HttpHeaders`
- `key: string`
- `i: int`

**Output:** `string`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Returns the i'th value associated with the given key. If there are no values associated with the key or the i'th value doesn't exist, an exception is raised.

### add

[ref: #symbol-add]

**Input:**
- `headers: HttpHeaders`
- `key: string`
- `value: string`

**Output:** *(none)*
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Adds the specified value to the specified key. Appends to any existing values associated with the key.

### clear

[ref: #symbol-clear]

**Input:**
- `headers: HttpHeaders`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `values: HttpHeaderValues`
- `value: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines if value is one of the values inside values. Comparison is performed without case sensitivity.

### contains

[ref: #symbol-contains]

**Input:**
- `methods: set[HttpMethod]`
- `x: string`

**Output:** `bool`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### del

[ref: #symbol-del]

**Input:**
- `headers: HttpHeaders`
- `key: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes the header entries associated with key

### getOrDefault

[ref: #symbol-getordefault]

**Input:**
- `headers: HttpHeaders`
- `key: string`
- `default:  = @[""].HttpHeaderValues`

**Output:** `HttpHeaderValues`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Returns the values associated with the given key. If there are no values associated with the key, then default is returned.

### hasKey

[ref: #symbol-haskey]

**Input:**
- `headers: HttpHeaders`
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### is1xx

[ref: #symbol-is1xx]

**Input:**
- `code: HttpCode`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether code is a 1xx HTTP status code.

### is2xx

[ref: #symbol-is2xx]

**Input:**
- `code: HttpCode`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether code is a 2xx HTTP status code.

### is3xx

[ref: #symbol-is3xx]

**Input:**
- `code: HttpCode`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether code is a 3xx HTTP status code.

### is4xx

[ref: #symbol-is4xx]

**Input:**
- `code: HttpCode`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether code is a 4xx HTTP status code.

### is5xx

[ref: #symbol-is5xx]

**Input:**
- `code: HttpCode`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether code is a 5xx HTTP status code.

### len

[ref: #symbol-len]

**Input:**
- `headers: HttpHeaders`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newHttpHeaders

[ref: #symbol-newhttpheaders]

**Input:**
- `titleCase:  = false`

**Output:** `HttpHeaders`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new HttpHeaders object. if titleCase is set to true, headers are passed to the server in title case (e.g. "Content-Length")

### newHttpHeaders

[ref: #symbol-newhttpheaders]

**Input:**
- `keyValuePairs: openArray[tuple[key: string, val: string]]`
- `titleCase:  = false`

**Output:** `HttpHeaders`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Returns a new HttpHeaders object from an array. if titleCase is set to true, headers are passed to the server in title case (e.g. "Content-Length")

### parseHeader

[ref: #symbol-parseheader]

Parses a single raw header HTTP line into key value pairs.

**Input:**
- `line: string`

**Output:** `tuple[key: string, value: seq[string]]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a single raw header HTTP line into key value pairs.

Used by asynchttpserver and httpclient internally and should not be used by you.

### toCaseInsensitive

[ref: #symbol-tocaseinsensitive]

**Input:**
- `headers: HttpHeaders`
- `s: string`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

For internal usage only. Do not use.

## Type

### HttpCode

[ref: #symbol-httpcode]

```nim
HttpCode = distinct range[0 .. 599]
```

### HttpHeaders

[ref: #symbol-httpheaders]

```nim
HttpHeaders = ref object
  table*: TableRef[string, seq[string]]
```

### HttpHeaderValues

[ref: #symbol-httpheadervalues]

```nim
HttpHeaderValues = distinct seq[string]
```


[Next](httpcore_2.md)
