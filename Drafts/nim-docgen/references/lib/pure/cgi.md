---
source_hash: 24bffc0f6ab54a43
source_path: lib/pure/cgi.nim
---

# cgi

[ref: #module-cgi]

This module implements helper procs for CGI applications. Example:

```
import std/[strtabs, cgi]

# Fill the values when debugging:
when debug:
  setTestData("name", "Klaus", "password", "123456")
# read the data into `myData`
var myData = readData()
# check that the data's variable names are "name" or "password"
validateData(myData, "name", "password")
# start generating content:
writeContentType()
# generate content:
write(stdout, "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\">\n")
write(stdout, "<html><head><title>Test</title></head><body>\n")
writeLine(stdout, "your name: " & myData["name"])
writeLine(stdout, "your password: " & myData["password"])
writeLine(stdout, "</body></html>")
```

## Examples

```nim
import std/[strtabs, cgi]

# Fill the values when debugging:
when debug:
  setTestData("name", "Klaus", "password", "123456")
# read the data into `myData`
var myData = readData()
# check that the data's variable names are "name" or "password"
validateData(myData, "name", "password")
# start generating content:
writeContentType()
# generate content:
write(stdout, "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\">\n")
write(stdout, "<html><head><title>Test</title></head><body>\n")
writeLine(stdout, "your name: " & myData["name"])
writeLine(stdout, "your password: " & myData["password"])
writeLine(stdout, "</body></html>")
```

```nim
setTestData("name", "Hanz", "password", "12345")
```

```nim
write(stdout, "Content-type: text/html\n\n")
```

## Iterator

### decodeData

[ref: #symbol-decodedata]

**Input:**
- `data: string`

**Output:** `tuple[key, value: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reads and decodes CGI data and yields the (name, value) pairs the data consists of.

### decodeData

[ref: #symbol-decodedata]

**Input:**
- `allowedMethods: set[RequestMethod] = {methodNone, methodPost, methodGet}`

**Output:** `tuple[key, value: string]`
**Pragmas:** `raises: [CgiError, ValueError, IOError]`, `tags: [ReadEnvEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: CgiError, ValueError, IOError`, `tags: ReadEnvEffect, ReadIOEffect`, `forbids: `

Reads and decodes CGI data and yields the (name, value) pairs the data consists of. If the client does not use a method listed in the allowedMethods set, a CgiError exception is raised.

## Proc

### cgiError

[ref: #symbol-cgierror]

**Input:**
- `msg: string`

**Output:** *(none)*
**Pragmas:** `noreturn`, `raises: [CgiError]`, `tags: []`, `forbids: []`

**Effects:** `raises: CgiError`, `tags: `, `forbids: `

Raises a CgiError exception with message msg.

### existsCookie

[ref: #symbol-existscookie]

**Input:**
- `name: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Checks if a cookie of name exists.

### getContentLength

[ref: #symbol-getcontentlength]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the CONTENT\_LENGTH environment variable.

### getContentType

[ref: #symbol-getcontenttype]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the CONTENT\_TYPE environment variable.

### getCookie

[ref: #symbol-getcookie]

**Input:**
- `name: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Gets a cookie. If no cookie of name exists, "" is returned.

### getDocumentRoot

[ref: #symbol-getdocumentroot]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the DOCUMENT\_ROOT environment variable.

### getGatewayInterface

[ref: #symbol-getgatewayinterface]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the GATEWAY\_INTERFACE environment variable.

### getHttpAccept

[ref: #symbol-gethttpaccept]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_ACCEPT environment variable.

### getHttpAcceptCharset

[ref: #symbol-gethttpacceptcharset]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_ACCEPT\_CHARSET environment variable.

### getHttpAcceptEncoding

[ref: #symbol-gethttpacceptencoding]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_ACCEPT\_ENCODING environment variable.

### getHttpAcceptLanguage

[ref: #symbol-gethttpacceptlanguage]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_ACCEPT\_LANGUAGE environment variable.

### getHttpConnection

[ref: #symbol-gethttpconnection]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_CONNECTION environment variable.

### getHttpCookie

[ref: #symbol-gethttpcookie]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_COOKIE environment variable.

### getHttpHost

[ref: #symbol-gethttphost]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_HOST environment variable.

### getHttpReferer

[ref: #symbol-gethttpreferer]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_REFERER environment variable.

### getHttpUserAgent

[ref: #symbol-gethttpuseragent]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the HTTP\_USER\_AGENT environment variable.

### getPathInfo

[ref: #symbol-getpathinfo]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the PATH\_INFO environment variable.

### getPathTranslated

[ref: #symbol-getpathtranslated]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the PATH\_TRANSLATED environment variable.

### getQueryString

[ref: #symbol-getquerystring]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the QUERY\_STRING environment variable.

### getRemoteAddr

[ref: #symbol-getremoteaddr]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REMOTE\_ADDR environment variable.

### getRemoteHost

[ref: #symbol-getremotehost]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REMOTE\_HOST environment variable.

### getRemoteIdent

[ref: #symbol-getremoteident]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REMOTE\_IDENT environment variable.

### getRemotePort

[ref: #symbol-getremoteport]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REMOTE\_PORT environment variable.

### getRemoteUser

[ref: #symbol-getremoteuser]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REMOTE\_USER environment variable.

### getRequestMethod

[ref: #symbol-getrequestmethod]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REQUEST\_METHOD environment variable.

### getRequestURI

[ref: #symbol-getrequesturi]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the REQUEST\_URI environment variable.

### getScriptFilename

[ref: #symbol-getscriptfilename]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SCRIPT\_FILENAME environment variable.

### getScriptName

[ref: #symbol-getscriptname]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SCRIPT\_NAME environment variable.

### getServerAddr

[ref: #symbol-getserveraddr]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_ADDR environment variable.

### getServerAdmin

[ref: #symbol-getserveradmin]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_ADMIN environment variable.

### getServerName

[ref: #symbol-getservername]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_NAME environment variable.

### getServerPort

[ref: #symbol-getserverport]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_PORT environment variable.

### getServerProtocol

[ref: #symbol-getserverprotocol]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_PROTOCOL environment variable.

### getServerSignature

[ref: #symbol-getserversignature]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_SIGNATURE environment variable.

### getServerSoftware

[ref: #symbol-getserversoftware]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns contents of the SERVER\_SOFTWARE environment variable.

### readData

[ref: #symbol-readdata]

**Input:**
- `allowedMethods: set[RequestMethod] = {methodNone, methodPost, methodGet}`

**Output:** `StringTableRef`
**Pragmas:** `raises: [CgiError, ValueError, IOError]`, `tags: [ReadEnvEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: CgiError, ValueError, IOError`, `tags: ReadEnvEffect, ReadIOEffect`, `forbids: `

Reads CGI data. If the client does not use a method listed in the allowedMethods set, a CgiError exception is raised.

### readData

[ref: #symbol-readdata]

**Input:**
- `data: string`

**Output:** `StringTableRef`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reads CGI data from a string.

### setCookie

[ref: #symbol-setcookie]

**Input:**
- `name: string`
- `value: string`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Sets a cookie.

### setStackTraceStdout

[ref: #symbol-setstacktracestdout]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Makes Nim output stacktraces to stdout, instead of server log.

### setTestData

[ref: #symbol-settestdata]

Fills the appropriate environment variables to test your CGI application. This can only simulate the 'GET' request method. keysvalues should provide embedded (name, value)-pairs. Example:

**Input:**
- `keysvalues: varargs[string]`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: [WriteEnvEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: WriteEnvEffect`, `forbids: `

Fills the appropriate environment variables to test your CGI application. This can only simulate the 'GET' request method. keysvalues should provide embedded (name, value)-pairs. Example:

```
setTestData("name", "Hanz", "password", "12345")
```

### validateData

[ref: #symbol-validatedata]

**Input:**
- `data: StringTableRef`
- `validKeys: varargs[string]`

**Output:** *(none)*
**Pragmas:** `raises: [CgiError]`, `tags: []`, `forbids: []`

**Effects:** `raises: CgiError`, `tags: `, `forbids: `

Validates data; raises CgiError if this fails. This checks that each variable name of the CGI data occurs in the validKeys array.

### writeContentType

[ref: #symbol-writecontenttype]

Calls this before starting to send your HTML data to stdout. This implements this part of the CGI protocol:

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Calls this before starting to send your HTML data to stdout. This implements this part of the CGI protocol:

```
write(stdout, "Content-type: text/html\n\n")
```

### writeErrorMessage

[ref: #symbol-writeerrormessage]

**Input:**
- `data: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: WriteIOEffect`, `forbids: `

Tries to reset browser state and writes data to stdout in <plaintext> tag.

### xmlEncode

[ref: #symbol-xmlencode]

Encodes a value to be XML safe:

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Encodes a value to be XML safe:

* " is replaced by &quot;
* < is replaced by &lt;
* > is replaced by &gt;
* & is replaced by &amp;
* every other character is carried over.

## Type

### CgiError

[ref: #symbol-cgierror]

```nim
CgiError = object of IOError
```

Exception that is raised if a CGI error occurs.

### RequestMethod

[ref: #symbol-requestmethod]

```nim
RequestMethod = enum
  methodNone,               ## no REQUEST_METHOD environment variable
  methodPost,               ## query uses the POST method
  methodGet                  ## query uses the GET method
```

The used request method.
