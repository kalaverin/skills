---
source_hash: 8558c7ca798dc203
source_path: lib/pure/uri.nim
---

# uri

[ref: #module-uri]

This module implements URI parsing as specified by RFC 3986.

A Uniform Resource Identifier (URI) provides a simple and extensible means for identifying a resource. A URI can be further classified as a locator, a name, or both. The term "Uniform Resource Locator" (URL) refers to the subset of URIs.

**Warning:**
URI parsers in this module do not perform security validation.

# [Basic usage](#basic-usage)

## [Combine URIs](#basic-usage-combine-uris)

## [Access URI item](#basic-usage-access-uri-item)

## [Data URI Base64](#basic-usage-data-uri-base64)

## Examples

```nim
import std/uri
let host = parseUri("https://nim-lang.org")
assert $host == "https://nim-lang.org"
assert $(host / "/blog.html") == "https://nim-lang.org/blog.html"
assert $(host / "blog2.html") == "https://nim-lang.org/blog2.html"
```

```nim
import std/uri
let res = parseUri("sftp://127.0.0.1:4343")
assert isAbsolute(res)
assert res.port == "4343"
```

```nim
import std/uri
assert getDataUri("Hello World", "text/plain") == "data:text/plain;charset=utf-8;base64,SGVsbG8gV29ybGQ="
assert getDataUri("Nim", "text/plain") == "data:text/plain;charset=utf-8;base64,Tmlt"
```

```nim
assert $parseUri("https://nim-lang.org") == "https://nim-lang.org"
```

```nim
let foo = parseUri("https://nim-lang.org/foo/bar") / "/baz"
assert foo.path == "/foo/bar/baz"
let bar = parseUri("https://nim-lang.org/foo/bar") / "baz"
assert bar.path == "/foo/bar/baz"
let qux = parseUri("https://nim-lang.org/foo/bar/") / "baz"
assert qux.path == "/foo/bar/baz"
```

```nim
let foo = parseUri("https://example.com") / "foo" ? {"bar": "qux"}
assert $foo == "https://example.com/foo?bar=qux"
let bar = parseUri("https://example.com/foo?existing=1") ? {"bar": "qux"}
assert $bar == "https://example.com/foo?existing=1&bar=qux"
```

```nim
let foo = combine(parseUri("https://nim-lang.org/foo/bar"), parseUri("/baz"))
assert foo.path == "/baz"
let bar = combine(parseUri("https://nim-lang.org/foo/bar"), parseUri("baz"))
assert bar.path == "/foo/baz"
let qux = combine(parseUri("https://nim-lang.org/foo/bar/"), parseUri("baz"))
assert qux.path == "/foo/bar/baz"
```

```nim
let foo = combine(parseUri("https://nim-lang.org/"), parseUri("docs/"),
    parseUri("manual.html"))
assert foo.hostname == "nim-lang.org"
assert foo.path == "/docs/manual.html"
```

```nim
assert decodeUrl("https%3A%2F%2Fnim-lang.org") == "https://nim-lang.org"
assert decodeUrl("https%3A%2F%2Fnim-lang.org%2Fthis+is+a+test") == "https://nim-lang.org/this is a test"
assert decodeUrl("https%3A%2F%2Fnim-lang.org%2Fthis%20is%20a%20test",
    false) == "https://nim-lang.org/this is a test"
assert decodeUrl("abc%xyz") == "abc%xyz"
```

```nim
assert encodeQuery({: }) == ""
assert encodeQuery({"a": "1", "b": "2"}) == "a=1&b=2"
assert encodeQuery({"a": "1", "b": ""}) == "a=1&b"
assert encodeQuery({"a": "1", "b": ""}, omitEq = false, sep = ';') == "a=1;b="
```

```nim
assert encodeUrl("https://nim-lang.org") == "https%3A%2F%2Fnim-lang.org"
assert encodeUrl("https://nim-lang.org/this is a test") == "https%3A%2F%2Fnim-lang.org%2Fthis+is+a+test"
assert encodeUrl("https://nim-lang.org/this is a test", false) == "https%3A%2F%2Fnim-lang.org%2Fthis%20is%20a%20test"
```

```nim
static: assert getDataUri("Nim", "text/plain") == "data:text/plain;charset=utf-8;base64,Tmlt"
```

```nim
var uri2 = initUri(isIpv6 = true)
uri2.scheme = "tcp"
uri2.hostname = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
uri2.port = "8080"
assert $uri2 == "tcp://[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:8080"
```

```nim
assert parseUri("https://nim-lang.org").isAbsolute
assert not parseUri("nim-lang").isAbsolute
```

```nim
let res = parseUri("ftp://Username:Password@Hostname")
assert res.username == "Username"
assert res.password == "Password"
assert res.scheme == "ftp"
```

```nim
var res = initUri()
parseUri("https://nim-lang.org/docs/manual.html", res)
assert res.scheme == "https"
assert res.hostname == "nim-lang.org"
assert res.path == "/docs/manual.html"
```

```nim
import std/sequtils
assert toSeq(decodeQuery("foo=1&bar=2=3")) == @[("foo", "1"), ("bar", "2=3")]
assert toSeq(decodeQuery("foo=1;bar=2=3", ';')) == @[("foo", "1"), ("bar", "2=3")]
assert toSeq(decodeQuery("&a&=b&=&&")) == @[("", ""), ("a", ""), ("", "b"), ("", ""), ("", "")]
```

## Iterator

### decodeQuery

[ref: #symbol-decodequery]

**Input:**
- `data: string`
- `sep:  = '&'`

**Output:** `tuple[key, value: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reads and decodes the query string data and yields the (key, value) pairs the data consists of. If compiled with -d:nimLegacyParseQueryStrict, a UriParseError is raised when there is an unencoded = character in a decoded value, which was the behavior in Nim < 1.5.1.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `u: Uri`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the string representation of the specified URI object.

### `/`

[ref: #symbol-]

Concatenates the path specified to the specified URIs path.

**Input:**
- `x: Uri`
- `path: string`

**Output:** `Uri`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates the path specified to the specified URIs path.

Contrary to the [combine func](#combine,Uri,Uri) you do not have to worry about the slashes at the beginning and end of the path and URIs path respectively.

**See also:**

* [combine func](#combine,Uri,Uri)

### `?`

[ref: #symbol-]

**Input:**
- `u: Uri`
- `query: openArray[(string, string)]`

**Output:** `Uri`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates the query parameters to the specified URI object. If the URI already has a query string, the new parameters are appended.

### combine

[ref: #symbol-combine]

Combines a base URI with a reference URI.

**Input:**
- `base: Uri`
- `reference: Uri`

**Output:** `Uri`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Combines a base URI with a reference URI.

This uses the algorithm specified in [section 5.2.2 of RFC 3986](https://tools.ietf.org/html/rfc3986#section-5.2.2).

This means that the slashes inside the base URIs path as well as reference URIs path affect the resulting URI.

**See also:**

* [/ func](#/,Uri,string) for building URIs

### combine

[ref: #symbol-combine]

Combines multiple URIs together.

**Input:**
- `uris: varargs[Uri]`

**Output:** `Uri`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Combines multiple URIs together.

**See also:**

* [/ func](#/,Uri,string) for building URIs

### decodeUrl

[ref: #symbol-decodeurl]

Decodes a URL according to RFC3986.

**Input:**
- `s: string`
- `decodePlus:  = true`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Decodes a URL according to RFC3986.

This means that any %xx (where xx denotes a hexadecimal value) are converted to the character with ordinal number xx, and every other character is carried over. If xx is not a valid hexadecimal value, it is left intact.

As a special rule, when the value of decodePlus is true, + characters are converted to a space.

**See also:**

* [encodeUrl func](#encodeUrl,string)

### encodeQuery

[ref: #symbol-encodequery]

Encodes a set of (key, value) parameters into a URL query string.

**Input:**
- `query: openArray[(string, string)]`
- `usePlus:  = true`
- `omitEq:  = true`
- `sep:  = '&'`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Encodes a set of (key, value) parameters into a URL query string.

Every (key, value) pair is URL-encoded and written as key=value. If the value is an empty string then the = is omitted, unless omitEq is false. The pairs are joined together by the sep character.

The usePlus parameter is passed down to the encodeUrl function that is used for the URL encoding of the string values.

**See also:**

* [encodeUrl func](#encodeUrl,string)

### encodeUrl

[ref: #symbol-encodeurl]

Encodes a URL according to RFC3986.

**Input:**
- `s: string`
- `usePlus:  = true`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Encodes a URL according to RFC3986.

This means that characters in the set {'a'..'z', 'A'..'Z', '0'..'9', '-', '.', '\_', '~'} are carried over to the result. All other characters are encoded as %xx where xx denotes its hexadecimal value.

As a special rule, when the value of usePlus is true, spaces are encoded as + instead of %20.

**See also:**

* [decodeUrl func](#decodeUrl,string)

### getDataUri

[ref: #symbol-getdatauri]

Convenience proc for base64.encode returns a standard Base64 Data URI (RFC-2397)

**Input:**
- `data: string`
- `mime: string`
- `encoding:  = "utf-8"`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convenience proc for base64.encode returns a standard Base64 Data URI (RFC-2397)

**See also:**

* [mimetypes](mimetypes.html) for mime argument
* <https://tools.ietf.org/html/rfc2397>
* <https://en.wikipedia.org/wiki/Data_URI_scheme>

### initUri

[ref: #symbol-inituri]

Initializes a URI with scheme, username, password, hostname, port, path, query, anchor and isIpv6.

**Input:**
- `isIpv6:  = false`

**Output:** `Uri`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes a URI with scheme, username, password, hostname, port, path, query, anchor and isIpv6.

**See also:**

* [Uri type](#Uri) for available fields in the URI type

### isAbsolute

[ref: #symbol-isabsolute]

**Input:**
- `uri: Uri`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if URI is absolute, false otherwise.

### parseUri

[ref: #symbol-parseuri]

Parses a URI. The result variable will be cleared before.

**Input:**
- `uri: string`
- `result: var Uri`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a URI. The result variable will be cleared before.

**See also:**

* [Uri type](#Uri) for available fields in the URI type
* [initUri func](#initUri) for initializing a URI

### parseUri

[ref: #symbol-parseuri]

Parses a URI and returns it.

**Input:**
- `uri: string`

**Output:** `Uri`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a URI and returns it.

**See also:**

* [Uri type](#Uri) for available fields in the URI type

### uriParseError

[ref: #symbol-uriparseerror]

**Input:**
- `msg: string`

**Output:** *(none)*
**Pragmas:** `noreturn`, `raises: [UriParseError]`, `tags: []`, `forbids: []`

**Effects:** `raises: UriParseError`, `tags: `, `forbids: `

Raises a UriParseError exception with message msg.

## Type

### Uri

[ref: #symbol-uri]

```nim
Uri = object
  scheme*, username*, password*: string
  hostname*, port*, path*, query*, anchor*: string
  opaque*: bool
  isIpv6*: bool
```

### UriParseError

[ref: #symbol-uriparseerror]

```nim
UriParseError = object of ValueError
```

### Url

[ref: #symbol-url]

```nim
Url = distinct string
```
