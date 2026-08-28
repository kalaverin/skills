---
source_hash: 200abf71d7df30cc
source_path: lib/std/private/osappdirs.nim
---

# osappdirs

[ref: #module-osappdirs]

## Examples

```nim
import std/os
assert getHomeDir() == expandTilde("~")
```

## Proc

### getCacheDir

[ref: #symbol-getcachedir]

Returns the cache directory of the current user for applications.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns the cache directory of the current user for applications.

This makes use of the following environment variables:

* On Windows: getEnv("LOCALAPPDATA")
* On macOS: getEnv("XDG\_CACHE\_HOME", getEnv("HOME") / "Library/Caches")
* On other platforms: getEnv("XDG\_CACHE\_HOME", getEnv("HOME") / ".cache")

**See also:**

* [getHomeDir](#getHomeDir)
* [getTempDir](#getTempDir)
* [getConfigDir](#getConfigDir)
* [getDataDir](#getDataDir)

### getCacheDir

[ref: #symbol-getcachedir]

Returns the cache directory for an application app.

**Input:**
- `app: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns the cache directory for an application app.

* On Windows, this uses: getCacheDir() / app / "cache"
* On other platforms, this uses: getCacheDir() / app

### getConfigDir

[ref: #symbol-getconfigdir]

Returns the config directory of the current user for applications.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadEnvEffect, ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect, ReadIOEffect`, `raises: `, `forbids: `

Returns the config directory of the current user for applications.

On non-Windows OSs, this proc conforms to the XDG Base Directory spec. Thus, this proc returns the value of the XDG\_CONFIG\_HOME environment variable if it is set, otherwise it returns the default configuration directory ("~/.config/").

An OS-dependent trailing slash is always present at the end of the returned string: \\ on Windows and / on all other OSs.

See also:

* [getHomeDir](#getHomeDir)
* [getDataDir](#getDataDir)
* [getTempDir](#getTempDir)
* [expandTilde](#expandTilde)
* [getCurrentDir](#getCurrentDir)
* [setCurrentDir](#setCurrentDir)

### getDataDir

[ref: #symbol-getdatadir]

Returns the data directory of the current user for applications.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadEnvEffect, ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect, ReadIOEffect`, `raises: `, `forbids: `

Returns the data directory of the current user for applications.

On non-Windows OSs, this proc conforms to the XDG Base Directory spec. Thus, this proc returns the value of the XDG\_DATA\_HOME environment variable if it is set, otherwise it returns the default configuration directory ("~/.local/share" or "~/Library/Application Support" on macOS).

See also:

* [getHomeDir](#getHomeDir)
* [getConfigDir](#getConfigDir)
* [getTempDir](#getTempDir)
* [expandTilde](#expandTilde)
* [getCurrentDir](#getCurrentDir)
* [setCurrentDir](#setCurrentDir)

### getHomeDir

[ref: #symbol-gethomedir]

Returns the home directory of the current user.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadEnvEffect, ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect, ReadIOEffect`, `raises: `, `forbids: `

Returns the home directory of the current user.

This proc is wrapped by the [expandTilde](#expandTilde) for the convenience of processing paths coming from user configuration files.

See also:

* [getDataDir](#getDataDir)
* [getConfigDir](#getConfigDir)
* [getTempDir](#getTempDir)
* [expandTilde](#expandTilde)
* [getCurrentDir](#getCurrentDir)
* [setCurrentDir](#setCurrentDir)

### getTempDir

[ref: #symbol-gettempdir]

Returns the temporary directory of the current user for applications to save temporary files in.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadEnvEffect, ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect, ReadIOEffect`, `raises: `, `forbids: `

Returns the temporary directory of the current user for applications to save temporary files in.

On Windows, it calls [GetTempPath](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-gettemppathw). On Posix based platforms, it will check TMPDIR, TEMP, TMP and TEMPDIR environment variables in order. On all platforms, /tmp will be returned if the procs fails.

You can override this implementation by adding -d:tempDir=mytempname to your compiler invocation.

**Note:** This proc does not check whether the returned path exists.

See also:

* [getHomeDir](#getHomeDir)
* [getConfigDir](#getConfigDir)
* [expandTilde](#expandTilde)
* [getCurrentDir](#getCurrentDir)
* [setCurrentDir](#setCurrentDir)
