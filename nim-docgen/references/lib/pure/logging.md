---
source_hash: 29a8810276bc7571
source_path: lib/pure/logging.nim
---

# logging

[ref: #module-logging]

This module implements a simple logger.

It has been designed to be as simple as possible to avoid bloat. If this library does not fulfill your needs, write your own.

# [Basic usage](#basic-usage)

To get started, first create a logger:

```
import std/logging

var logger = newConsoleLogger()
```

The logger that was created above logs to the console, but this module also provides loggers that log to files, such as the [FileLogger](#FileLogger). Creating custom loggers is also possible by inheriting from the [Logger](#Logger) type.

Once a logger has been created, call its [log proc](#log.e,ConsoleLogger,Level,varargs[string,]) to log a message:

```
logger.log(lvlInfo, "a log message")
# Output: INFO a log message
```

The INFO within the output is the result of a format string being prepended to the message, and it will differ depending on the message's level. Format strings are [explained in more detail here](#basic-usage-format-strings).

There are six logging levels: debug, info, notice, warn, error, and fatal. They are described in more detail within the [Level enum's documentation](#Level). A message is logged if its level is at or above both the logger's levelThreshold field and the global log filter. The latter can be changed with the [setLogFilter proc](#setLogFilter,Level).

**Warning:**
For loggers that log to a console or to files, only error and fatal messages will cause their output buffers to be flushed immediately by default. set flushThreshold when creating the logger to change this.

## [Handlers](#basic-usage-handlers)

When using multiple loggers, calling the log proc for each logger can become repetitive. Instead of doing that, register each logger that will be used with the [addHandler proc](#addHandler,Logger), which is demonstrated in the following example:

```
import std/logging

var consoleLog = newConsoleLogger()
var fileLog = newFileLogger("errors.log", levelThreshold=lvlError)
var rollingLog = newRollingFileLogger("rolling.log")

addHandler(consoleLog)
addHandler(fileLog)
addHandler(rollingLog)
```

After doing this, use either the [log template](#log.t,Level,varargs[string,]) or one of the level-specific templates, such as the [error template](#error.t,varargs[string,]), to log messages to all registered handlers at once.

```
# This example uses the loggers created above
log(lvlError, "an error occurred")
error("an error occurred")  # Equivalent to the above line
info("something normal happened")  # Will not be written to errors.log
```

Note that a message's level is still checked against each handler's levelThreshold and the global log filter.

## [Format strings](#basic-usage-format-strings)

Log messages are prefixed with format strings. These strings contain placeholders for variables, such as $time, that are replaced with their corresponding values, such as the current time, before they are prepended to a log message. Characters that are not part of variables are unaffected.

The format string used by a logger can be specified by providing the fmtStr argument when creating the logger or by setting its fmtStr field afterward. If not specified, the [default format string](#defaultFmtStr) is used.

The following variables, which must be prefixed with a dollar sign ($), are available:

| Variable | Output |
| --- | --- |
| $date | Current date |
| $time | Current time |
| $datetime | $dateT$time |
| $app | [os.getAppFilename()](os.html#getAppFilename) |
| $appname | Base name of $app |
| $appdir | Directory name of $app |
| $levelid | First letter of log level |
| $levelname | Log level name |

Note that $app, $appname, and $appdir are not supported when using the JavaScript backend.

The following example illustrates how to use format strings:

```
import std/logging

var logger = newConsoleLogger(fmtStr="[$time] - $levelname: ")
logger.log(lvlInfo, "this is a message")
# Output: [19:50:13] - INFO: this is a message
```

## [Notes when using multiple threads](#basic-usage-notes-when-using-multiple-threads)

There are a few details to keep in mind when using this module within multiple threads:

* The global log filter is actually a thread-local variable, so it needs to be set in each thread that uses this module.
* The list of registered handlers is also a thread-local variable. If a handler will be used in multiple threads, it needs to be registered in each of those threads.

# [See also](#see-also)

* [strutils module](strutils.html) for common string functions
* [strformat module](strformat.html) for string interpolation and formatting
* [strscans module](strscans.html) for scanf and scanp macros, which offer easier substring extraction than regular expressions

## Examples

```nim
import std/logging

var logger = newConsoleLogger()
```

```nim
logger.log(lvlInfo, "a log message")
# Output: INFO a log message
```

```nim
import std/logging

var consoleLog = newConsoleLogger()
var fileLog = newFileLogger("errors.log", levelThreshold=lvlError)
var rollingLog = newRollingFileLogger("rolling.log")

addHandler(consoleLog)
addHandler(fileLog)
addHandler(rollingLog)
```

```nim
# This example uses the loggers created above
log(lvlError, "an error occurred")
error("an error occurred")  # Equivalent to the above line
info("something normal happened")  # Will not be written to errors.log
```

```nim
import std/logging

var logger = newConsoleLogger(fmtStr="[$time] - $levelname: ")
logger.log(lvlInfo, "this is a message")
# Output: [19:50:13] - INFO: this is a message
```

```nim
var logger = newConsoleLogger()
addHandler(logger)
doAssert logger in getHandlers()
```

```nim
var normalLog = newConsoleLogger()
var formatLog = newConsoleLogger(fmtStr=verboseFmtStr)
var errorLog = newConsoleLogger(levelThreshold=lvlError, useStderr=true)
```

```nim
var messages = open("messages.log", fmWrite)
var formatted = open("formatted.log", fmWrite)
var errors = open("errors.log", fmWrite)

var normalLog = newFileLogger(messages)
var formatLog = newFileLogger(formatted, fmtStr=verboseFmtStr)
var errorLog = newFileLogger(errors, levelThreshold=lvlError)
```

```nim
var normalLog = newFileLogger("messages.log")
var formatLog = newFileLogger("formatted.log", fmtStr=verboseFmtStr)
var errorLog = newFileLogger("errors.log", levelThreshold=lvlError)
```

```nim
var normalLog = newRollingFileLogger("messages.log")
var formatLog = newRollingFileLogger("formatted.log", fmtStr=verboseFmtStr)
var shortLog = newRollingFileLogger("short.log", maxLines=200)
var errorLog = newRollingFileLogger("errors.log", levelThreshold=lvlError)
```

```nim
setLogFilter(lvlError)
doAssert getLogFilter() == lvlError
```

```nim
doAssert substituteLog(defaultFmtStr, lvlInfo, "a message") == "INFO a message"
doAssert substituteLog("$levelid - ", lvlError, "an error") == "E - an error"
doAssert substituteLog("$levelid", lvlDebug, "error") == "Derror"
```

```nim
var consoleLog = newConsoleLogger()
consoleLog.log(lvlInfo, "this is a message")
consoleLog.log(lvlError, "error code is: ", 404)
```

```nim
var fileLog = newFileLogger("messages.log")
fileLog.log(lvlInfo, "this is a message")
fileLog.log(lvlError, "error code is: ", 404)
```

```nim
var rollingLog = newRollingFileLogger("messages.log")
rollingLog.log(lvlInfo, "this is a message")
rollingLog.log(lvlError, "error code is: ", 404)
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

debug("myProc called with arguments: foo, 5")
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

error("An exception occurred while processing the form.")
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

fatal("Can't open database -- exiting.")
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

info("Application started successfully.")
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

log(lvlInfo, "This is an example.")
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

notice("An important operation has completed.")
```

```nim
var logger = newConsoleLogger()
addHandler(logger)

warn("The previous operation took too long to process.")
```

## Const

### defaultFmtStr

[ref: #symbol-defaultfmtstr]

```nim
defaultFmtStr = "$levelname "
```

The default format string.

### LevelNames

[ref: #symbol-levelnames]

```nim
LevelNames: array[Level, string] = ["DEBUG", "DEBUG", "INFO", "NOTICE", "WARN",
                                    "ERROR", "FATAL", "NONE"]
```

Array of strings representing each logging level.

### verboseFmtStr

[ref: #symbol-verbosefmtstr]

A more verbose format string.

```nim
verboseFmtStr = "$levelid, [$datetime] -- $appname: "
```

A more verbose format string.

This string can be passed as the frmStr argument to procs that create new loggers, such as the [newConsoleLogger proc](#newConsoleLogger).

If a different format string is preferred, refer to the [documentation about format strings](#basic-usage-format-strings) for more information, including a list of available variables.

## Proc

### addHandler

[ref: #symbol-addhandler]

Adds a logger to the list of registered handlers.

**Input:**
- `handler: Logger`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds a logger to the list of registered handlers.

**Warning:**
The list of handlers is a thread-local variable. If the given handler will be used in multiple threads, this proc should be called in each of those threads.

See also:

* [removeHandler](#removeHandler)
* [getHandlers proc](#getHandlers)

### defaultFilename

[ref: #symbol-defaultfilename]

Returns the filename that is used by default when naming log files.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadIOEffect`, `forbids: `

Returns the filename that is used by default when naming log files.

**Note:** This proc is not available for the JavaScript backend.

### getHandlers

[ref: #symbol-gethandlers]

Returns a list of all the registered handlers.

**Input:**
- *(none)*

**Output:** `seq[Logger]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a list of all the registered handlers.

See also:

* [addHandler proc](#addHandler,Logger)

### getLogFilter

[ref: #symbol-getlogfilter]

Gets the global log filter.

**Input:**
- *(none)*

**Output:** `Level`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the global log filter.

See also:

* [setLogFilter proc](#setLogFilter,Level)

### newConsoleLogger

[ref: #symbol-newconsolelogger]

Creates a new [ConsoleLogger](#ConsoleLogger).

**Input:**
- `levelThreshold:  = lvlAll`
- `fmtStr:  = defaultFmtStr`
- `useStderr:  = false`
- `flushThreshold:  = defaultFlushThreshold`

**Output:** `ConsoleLogger`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new [ConsoleLogger](#ConsoleLogger).

By default, log messages are written to stdout. If useStderr is true, they are written to stderr instead.

For the JavaScript backend, log messages are written to the console, and useStderr is ignored.

See also:

* [newFileLogger proc](#newFileLogger,File) that uses a file handle
* [newFileLogger proc](#newFileLogger,FileMode,int) that accepts a filename
* [newRollingFileLogger proc](#newRollingFileLogger,FileMode,Positive,int)

**Examples:**

```
var normalLog = newConsoleLogger()
var formatLog = newConsoleLogger(fmtStr=verboseFmtStr)
var errorLog = newConsoleLogger(levelThreshold=lvlError, useStderr=true)
```

### newFileLogger

[ref: #symbol-newfilelogger]

Creates a new [FileLogger](#FileLogger) that uses the given file handle.

**Input:**
- `file: File`
- `levelThreshold:  = lvlAll`
- `fmtStr:  = defaultFmtStr`
- `flushThreshold:  = defaultFlushThreshold`

**Output:** `FileLogger`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new [FileLogger](#FileLogger) that uses the given file handle.

**Note:** This proc is not available for the JavaScript backend.

See also:

* [newConsoleLogger proc](#newConsoleLogger)
* [newFileLogger proc](#newFileLogger,FileMode,int) that accepts a filename
* [newRollingFileLogger proc](#newRollingFileLogger,FileMode,Positive,int)

**Examples:**

```
var messages = open("messages.log", fmWrite)
var formatted = open("formatted.log", fmWrite)
var errors = open("errors.log", fmWrite)

var normalLog = newFileLogger(messages)
var formatLog = newFileLogger(formatted, fmtStr=verboseFmtStr)
var errorLog = newFileLogger(errors, levelThreshold=lvlError)
```

### newFileLogger

[ref: #symbol-newfilelogger]

Creates a new [FileLogger](#FileLogger) that logs to a file with the given filename.

**Input:**
- `filename:  = defaultFilename()`
- `mode: FileMode = fmAppend`
- `levelThreshold:  = lvlAll`
- `fmtStr:  = defaultFmtStr`
- `bufSize: int = -1`
- `flushThreshold:  = defaultFlushThreshold`

**Output:** `FileLogger`
**Pragmas:** `raises: [IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError`, `tags: `, `forbids: `

Creates a new [FileLogger](#FileLogger) that logs to a file with the given filename.

bufSize controls the size of the output buffer that is used when writing to the log file. The following values can be provided:

* -1 - use system defaults
* 0 - unbuffered
* > 0 - fixed buffer size

**Note:** This proc is not available for the JavaScript backend.

See also:

* [newConsoleLogger proc](#newConsoleLogger)
* [newFileLogger proc](#newFileLogger,File) that uses a file handle
* [newRollingFileLogger proc](#newRollingFileLogger,FileMode,Positive,int)

**Examples:**

```
var normalLog = newFileLogger("messages.log")
var formatLog = newFileLogger("formatted.log", fmtStr=verboseFmtStr)
var errorLog = newFileLogger("errors.log", levelThreshold=lvlError)
```

### newRollingFileLogger

[ref: #symbol-newrollingfilelogger]

Creates a new [RollingFileLogger](#RollingFileLogger).

**Input:**
- `filename:  = defaultFilename()`
- `mode: FileMode = fmReadWrite`
- `levelThreshold:  = lvlAll`
- `fmtStr:  = defaultFmtStr`
- `maxLines: Positive = 1000`
- `bufSize: int = -1`
- `flushThreshold:  = defaultFlushThreshold`

**Output:** `RollingFileLogger`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadDirEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadDirEffect, ReadIOEffect`, `forbids: `

Creates a new [RollingFileLogger](#RollingFileLogger).

Once the current log file being written to contains maxLines lines, a new log file will be created, and the old log file will be renamed.

bufSize controls the size of the output buffer that is used when writing to the log file. The following values can be provided:

* -1 - use system defaults
* 0 - unbuffered
* > 0 - fixed buffer size

**Note:** This proc is not available in the JavaScript backend.

See also:

* [newConsoleLogger proc](#newConsoleLogger)
* [newFileLogger proc](#newFileLogger,File) that uses a file handle
* [newFileLogger proc](#newFileLogger,FileMode,int) that accepts a filename

**Examples:**

```
var normalLog = newRollingFileLogger("messages.log")
var formatLog = newRollingFileLogger("formatted.log", fmtStr=verboseFmtStr)
var shortLog = newRollingFileLogger("short.log", maxLines=200)
var errorLog = newRollingFileLogger("errors.log", levelThreshold=lvlError)
```

### removeHandler

[ref: #symbol-removehandler]

Removes a logger from the list of registered handlers.

**Input:**
- `handler: Logger`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Removes a logger from the list of registered handlers.

Note that for n times a logger is registered, n calls to this proc are required to remove that logger.

### setLogFilter

[ref: #symbol-setlogfilter]

Sets the global log filter.

**Input:**
- `lvl: Level`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the global log filter.

Messages below the provided level will not be logged regardless of an individual logger's levelThreshold. By default, all messages are logged.

**Warning:**
The global log filter is a thread-local variable. If logging is being performed in multiple threads, this proc should be called in each thread unless it is intended that different threads should log at different logging levels.

See also:

* [getLogFilter proc](#getLogFilter)

### substituteLog

[ref: #symbol-substitutelog]

Formats a log message at the specified level with the given format string.

**Input:**
- `frmt: string`
- `level: Level`
- `args: varargs[string, `$`]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadIOEffect, TimeEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadIOEffect, TimeEffect`, `forbids: `

Formats a log message at the specified level with the given format string.

The [format variables](#basic-usage-format-strings) present within frmt will be replaced with the corresponding values before being prepended to args and returned.

Unless you are implementing a custom logger, there is little need to call this directly. Use either a logger's log method or one of the logging templates.

See also:

* [log method](#log.e,ConsoleLogger,Level,varargs[string,]) for the ConsoleLogger
* [log method](#log.e,FileLogger,Level,varargs[string,]) for the FileLogger
* [log method](#log.e,RollingFileLogger,Level,varargs[string,]) for the RollingFileLogger
* [log template](#log.t,Level,varargs[string,])

## Template

### debug

[ref: #symbol-debug]

Logs a debug message to all registered handlers.

**Input:**
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs a debug message to all registered handlers.

Debug messages are typically useful to the application developer only, and they are usually disabled in release builds, although this template does not make that distinction.

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

debug("myProc called with arguments: foo, 5")
```

See also:

* [log template](#log.t,Level,varargs[string,])
* [info template](#info.t,varargs[string,])
* [notice template](#notice.t,varargs[string,])

### error

[ref: #symbol-error]

Logs an error message to all registered handlers.

**Input:**
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs an error message to all registered handlers.

Error messages are for application-level error conditions, such as when some user input generated an exception. Typically, the application will continue to run, but with degraded functionality or loss of data, and these effects might be visible to users.

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

error("An exception occurred while processing the form.")
```

See also:

* [log template](#log.t,Level,varargs[string,])
* [warn template](#warn.t,varargs[string,])
* [fatal template](#fatal.t,varargs[string,])

### fatal

[ref: #symbol-fatal]

Logs a fatal error message to all registered handlers.

**Input:**
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs a fatal error message to all registered handlers.

Fatal error messages usually indicate that the application cannot continue to run and will exit due to a fatal condition. This template only logs the message, and it is the application's responsibility to exit properly.

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

fatal("Can't open database -- exiting.")
```

See also:

* [log template](#log.t,Level,varargs[string,])
* [warn template](#warn.t,varargs[string,])
* [error template](#error.t,varargs[string,])

### info

[ref: #symbol-info]

Logs an info message to all registered handlers.

**Input:**
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs an info message to all registered handlers.

Info messages are typically generated during the normal operation of an application and are of no particular importance. It can be useful to aggregate these messages for later analysis.

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

info("Application started successfully.")
```

See also:

* [log template](#log.t,Level,varargs[string,])
* [debug template](#debug.t,varargs[string,])
* [notice template](#notice.t,varargs[string,])

### log

[ref: #symbol-log]

Logs a message at the specified level to all registered handlers.

**Input:**
- `level: Level`
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs a message at the specified level to all registered handlers.

Whether the message is logged depends on both the FileLogger's levelThreshold field and the global log filter set using the [setLogFilter proc](#setLogFilter,Level).

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

log(lvlInfo, "This is an example.")
```

See also:

* [debug template](#debug.t,varargs[string,])
* [info template](#info.t,varargs[string,])
* [notice template](#notice.t,varargs[string,])
* [warn template](#warn.t,varargs[string,])
* [error template](#error.t,varargs[string,])
* [fatal template](#fatal.t,varargs[string,])

### notice

[ref: #symbol-notice]

Logs an notice to all registered handlers.

**Input:**
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs an notice to all registered handlers.

Notices are semantically very similar to info messages, but they are meant to be messages that the user should be actively notified about, depending on the application.

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

notice("An important operation has completed.")
```

See also:

* [log template](#log.t,Level,varargs[string,])
* [debug template](#debug.t,varargs[string,])
* [info template](#info.t,varargs[string,])

### warn

[ref: #symbol-warn]

Logs a warning message to all registered handlers.

**Input:**
- `args: varargs[string, `$`]`

**Output:** *(none)*
Logs a warning message to all registered handlers.

A warning is a non-error message that may indicate impending problems or degraded performance.

**Examples:**

```
var logger = newConsoleLogger()
addHandler(logger)

warn("The previous operation took too long to process.")
```

See also:

* [log template](#log.t,Level,varargs[string,])
* [error template](#error.t,varargs[string,])
* [fatal template](#fatal.t,varargs[string,])

## Type

### ConsoleLogger

[ref: #symbol-consolelogger]

A logger that writes log messages to the console.

```nim
ConsoleLogger = ref object of Logger
  useStderr*: bool           ## If true, writes to stderr; otherwise, writes to stdout
  flushThreshold*: Level     ## Only messages that are at or above this
                             ## threshold will be flushed immediately
```

A logger that writes log messages to the console.

Create a new ConsoleLogger with the [newConsoleLogger proc](#newConsoleLogger).

See also:

* [FileLogger](#FileLogger)
* [RollingFileLogger](#RollingFileLogger)

### FileLogger

[ref: #symbol-filelogger]

A logger that writes log messages to a file.

```nim
FileLogger = ref object of Logger
  file*: File                ## The wrapped file
  flushThreshold*: Level     ## Only messages that are at or above this
                             ## threshold will be flushed immediately
```

A logger that writes log messages to a file.

Create a new FileLogger with the [newFileLogger proc](#newFileLogger,File).

**Note:** This logger is not available for the JavaScript backend.

See also:

* [ConsoleLogger](#ConsoleLogger)
* [RollingFileLogger](#RollingFileLogger)

### Level

[ref: #symbol-level]

Enumeration of logging levels.

```nim
Level = enum
  lvlAll,                   ## All levels active
  lvlDebug,                 ## Debug level and above are active
  lvlInfo,                  ## Info level and above are active
  lvlNotice,                ## Notice level and above are active
  lvlWarn,                  ## Warn level and above are active
  lvlError,                 ## Error level and above are active
  lvlFatal,                 ## Fatal level and above are active
  lvlNone                    ## No levels active; nothing is logged
```

Enumeration of logging levels.

Debug messages represent the lowest logging level, and fatal error messages represent the highest logging level. lvlAll can be used to enable all messages, while lvlNone can be used to disable all messages.

Typical usage for each logging level, from lowest to highest, is described below:

* **Debug** - debugging information helpful only to developers
* **Info** - anything associated with normal operation and without any particular importance
* **Notice** - more important information that users should be notified about
* **Warn** - impending problems that require some attention
* **Error** - error conditions that the application can recover from
* **Fatal** - fatal errors that prevent the application from continuing

It is completely up to the application how to utilize each level.

Individual loggers have a levelThreshold field that filters out any messages with a level lower than the threshold. There is also a global filter that applies to all log messages, and it can be changed using the [setLogFilter proc](#setLogFilter,Level).

### Logger

[ref: #symbol-logger]

The abstract base type of all loggers.

```nim
Logger = ref object of RootObj
  levelThreshold*: Level     ## Only messages that are at or above this
                             ## threshold will be logged
  fmtStr*: string            ## Format string to prepend to each log message;
                             ## defaultFmtStr is the default
```

The abstract base type of all loggers.

Custom loggers should inherit from this type. They should also provide their own implementation of the [log method](#log.e,Logger,Level,varargs[string,]).

See also:

* [ConsoleLogger](#ConsoleLogger)
* [FileLogger](#FileLogger)
* [RollingFileLogger](#RollingFileLogger)

### RollingFileLogger

[ref: #symbol-rollingfilelogger]

A logger that writes log messages to a file while performing log rotation.

```nim
RollingFileLogger = ref object of FileLogger
```

A logger that writes log messages to a file while performing log rotation.

Create a new RollingFileLogger with the [newRollingFileLogger proc](#newRollingFileLogger,FileMode,Positive,int).

**Note:** This logger is not available for the JavaScript backend.

See also:

* [ConsoleLogger](#ConsoleLogger)
* [FileLogger](#FileLogger)
