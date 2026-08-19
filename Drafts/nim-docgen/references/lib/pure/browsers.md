---
source_hash: f72523814250bfa1
source_path: lib/pure/browsers.nim
---

# browsers

[ref: #module-browsers]

This module implements a simple proc for opening URLs with the user's default browser.

Unstable API.

## Examples

```nim
block: openDefaultBrowser()
```

```nim
block: openDefaultBrowser("https://nim-lang.org")
```

## Const

### osOpenCmd

[ref: #symbol-osopencmd]

```nim
osOpenCmd = "open"
```

## Proc

### openDefaultBrowser

[ref: #symbol-opendefaultbrowser]

Opens url with the user's default browser. This does not block. The URL must not be empty string, to open on a blank page see openDefaultBrowser().

**Input:**
- `url: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: [ExecIOEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ExecIOEffect`, `forbids: `

Opens url with the user's default browser. This does not block. The URL must not be empty string, to open on a blank page see openDefaultBrowser().

Under Windows, ShellExecute is used. Under Mac OS X the open command is used. Under Unix, it is checked if xdg-open exists and used if it does. Otherwise the environment variable BROWSER is used to determine the default browser to use.

This proc doesn't raise an exception on error, beware.

```
block: openDefaultBrowser("https://nim-lang.org")
```

### openDefaultBrowser

[ref: #symbol-opendefaultbrowser]

Intends to open the user's default browser without any url (blank page). This does not block. Intends to implement IETF RFC-6694 Section 3, ("about:blank" is reserved for a blank page).

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `deprecated: "not implemented, please open with a specific url instead"`, `raises: []`, `tags: [ExecIOEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ExecIOEffect`, `forbids: `

Intends to open the user's default browser without any url (blank page). This does not block. Intends to implement IETF RFC-6694 Section 3, ("about:blank" is reserved for a blank page).

Beware that this intended behavior is **not** implemented and considered not worthy to implement here.

The following describes the behavior of current implementation:

* Under Windows, this will only cause a pop-up dialog
  asking the assocated application with about
  (as Windows simply treats about: as a protocol like http).
* Under Mac OS X the open "about:blank" command is used.
* Under Unix, it is checked if xdg-open exists and used
  if it does and open the application assocated with text/html mime
  (not x-scheme-handler/http, so maybe html-viewer
  other than your default browser is opened).
  Otherwise the environment variable BROWSER is used
  to determine the default browser to use.

This proc doesn't raise an exception on error, beware.

```
block: openDefaultBrowser()
```

**See also:**

* <https://tools.ietf.org/html/rfc6694#section-3>
