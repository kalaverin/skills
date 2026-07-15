---
source_hash: 5d35e245b165fe43
source_path: lib/pure/terminal.nim
---

# terminal

[ref: #module-terminal]

This module contains a few procedures to control the *terminal* (also called *console*). On UNIX, the implementation simply uses ANSI escape sequences and does not depend on any other module, on Windows it uses the Windows API. Changing the style is permanent even after program termination! Use the code exitprocs.addExitProc(resetAttributes) to restore the defaults. Similarly, if you hide the cursor, make sure to unhide it with showCursor before quitting.

# [Progress bar](#progress-bar)

Basic progress bar example:

## [Playing with colorful and styled text](#progress-bar-playing-with-colorful-and-styled-text)

Procs like styledWriteLine, styledEcho etc. have a temporary effect on text parameters. Style parameters only affect the text parameter right after them. After being called, these procs will reset the default style of the terminal. While setBackGroundColor, setForeGroundColor etc. have a lasting influence on the terminal, you can use resetAttributes to reset the default style of the terminal.

## Examples

```nim
import std/terminal
import std/[os, strutils]

for i in 0..100:
  stdout.styledWriteLine(fgRed, "0% ", fgWhite, '#'.repeat i, if i > 50: fgGreen else: fgYellow, "\t", $i , "%")
  sleep 42
  cursorUp 1
  eraseLine()

stdout.resetAttributes()
```

```nim
import std/terminal
stdout.styledWriteLine({styleBright, styleBlink, styleUnderscore}, "styled text ")
stdout.styledWriteLine(fgRed, "red text ")
stdout.styledWriteLine(fgWhite, bgRed, "white text in red background")
stdout.styledWriteLine(" ordinary text without style ")

stdout.setBackGroundColor(bgCyan, true)
stdout.setForeGroundColor(fgBlue)
stdout.write("blue text in cyan background")
stdout.resetAttributes()

# You can specify multiple text parameters. Style parameters
# only affect the text parameter right after them.
styledEcho styleBright, fgGreen, "[PASS]", resetStyle, fgGreen, " Yay!"

stdout.styledWriteLine(fgRed, "red text ", styleBright, "bold red", fgDefault, " bold text")
```

```nim
stdout.cursorBackward(2)
write(stdout, "Hello World!") # anything written at that location will be erased/replaced with this
```

```nim
stdout.cursorDown(2)
write(stdout, "Hello World!") # anything written at that location will be erased/replaced with this
```

```nim
stdout.cursorForward(2)
write(stdout, "Hello World!") # anything written at that location will be erased/replaced with this
```

```nim
stdout.cursorUp(2)
write(stdout, "Hello World!") # anything written at that location will be erased/replaced with this
```

```nim
write(stdout, "never mind")
stdout.eraseLine() # nothing will be printed on the screen
```

```nim
stdout.styledWrite(fgRed, "red text ")
stdout.styledWrite(fgGreen, "green text")
```

```nim
proc error(msg: string) =
  styledWriteLine(stderr, fgRed, "Error: ", resetStyle, msg)
```

## Const

### ansiResetCode

[ref: #symbol-ansiresetcode]

```nim
ansiResetCode = "\e[0m"
```

## Macro

### styledWrite

[ref: #symbol-styledwrite]

**Input:**
- `f: File`
- `m: varargs[typed]`

**Output:** `untyped`
Similar to write, but treating terminal style arguments specially. When some argument is Style, set[Style], ForegroundColor, BackgroundColor or TerminalCmd then it is not sent directly to f, but instead corresponding terminal style proc is called.

## Proc

### ansiBackgroundColorCode

[ref: #symbol-ansibackgroundcolorcode]

**Input:**
- `color: Color`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ansiForegroundColorCode

[ref: #symbol-ansiforegroundcolorcode]

**Input:**
- `fg: ForegroundColor`
- `bright:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ansiForegroundColorCode

[ref: #symbol-ansiforegroundcolorcode]

**Input:**
- `color: Color`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ansiStyleCode

[ref: #symbol-ansistylecode]

**Input:**
- `style: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cursorBackward

[ref: #symbol-cursorbackward]

**Input:**
- `f: File`
- `count:  = 1`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Moves the cursor backward by count columns.

### cursorDown

[ref: #symbol-cursordown]

**Input:**
- `f: File`
- `count:  = 1`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Moves the cursor down by count rows.

### cursorForward

[ref: #symbol-cursorforward]

**Input:**
- `f: File`
- `count:  = 1`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Moves the cursor forward by count columns.

### cursorUp

[ref: #symbol-cursorup]

**Input:**
- `f: File`
- `count:  = 1`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Moves the cursor up by count rows.

### disableTrueColors

[ref: #symbol-disabletruecolors]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Disables true color.

### enableTrueColors

[ref: #symbol-enabletruecolors]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: [RootEffect, ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect, ReadEnvEffect`, `forbids: `

Enables true color.

### eraseLine

[ref: #symbol-eraseline]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Erases the entire current line.

### eraseScreen

[ref: #symbol-erasescreen]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Erases the screen with the background colour and moves the cursor to home.

### getch

[ref: #symbol-getch]

**Input:**
- *(none)*

**Output:** `char`
**Pragmas:** `raises: [IOError, EOFError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, EOFError`, `tags: ReadIOEffect`, `forbids: `

Reads a single character from the terminal, blocking until it is entered. The character is not printed to the terminal.

### getCursorPos

[ref: #symbol-getcursorpos]

**Input:**
- *(none)*

**Output:** `tuple[x, y: int]`
**Pragmas:** `raises: [ValueError, IOError]`, `tags: [WriteIOEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: ValueError, IOError`, `tags: WriteIOEffect, ReadIOEffect`, `forbids: `

Returns cursor position (x, y) writes to stdout and expects the terminal to respond via stdin

### hideCursor

[ref: #symbol-hidecursor]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Hides the cursor.

### isatty

[ref: #symbol-isatty]

**Input:**
- `f: File`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if f is associated with a terminal device.

### isTrueColorSupported

[ref: #symbol-istruecolorsupported]

**Input:**
- *(none)*

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Returns true if a terminal supports true color.

### readPasswordFromStdin

[ref: #symbol-readpasswordfromstdin]

**Input:**
- `prompt: string`
- `password: var string`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect, WriteIOEffect]`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, WriteIOEffect`, `raises: IOError`, `forbids: `

### readPasswordFromStdin

[ref: #symbol-readpasswordfromstdin]

**Input:**
- `prompt:  = "password: "`

**Output:** `string`
**Pragmas:** `raises: [IOError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Reads a password from stdin without printing it.

### resetAttributes

[ref: #symbol-resetattributes]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Resets all attributes.

### resetAttributes

[ref: #symbol-resetattributes]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `noconv`, `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Resets all attributes on stdout. It is advisable to register this as a quit proc with exitprocs.addExitProc(resetAttributes).

### setBackgroundColor

[ref: #symbol-setbackgroundcolor]

**Input:**
- `f: File`
- `bg: BackgroundColor`
- `bright:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Sets the terminal's background color.

### setBackgroundColor

[ref: #symbol-setbackgroundcolor]

**Input:**
- `f: File`
- `color: Color`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: RootEffect, WriteIOEffect`, `forbids: `

Sets the terminal's background true color.

### setCursorPos

[ref: #symbol-setcursorpos]

**Input:**
- `f: File`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Sets the terminal's cursor to the (x,y) position. (0,0) is the upper left of the screen.

### setCursorXPos

[ref: #symbol-setcursorxpos]

**Input:**
- `f: File`
- `x: int`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Sets the terminal's cursor to the x position. The y position is not changed.

### setForegroundColor

[ref: #symbol-setforegroundcolor]

**Input:**
- `f: File`
- `fg: ForegroundColor`
- `bright:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Sets the terminal's foreground color.

### setForegroundColor

[ref: #symbol-setforegroundcolor]

**Input:**
- `f: File`
- `color: Color`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: RootEffect, WriteIOEffect`, `forbids: `

Sets the terminal's foreground true color.

### setStyle

[ref: #symbol-setstyle]

**Input:**
- `f: File`
- `style: set[Style]`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Sets the terminal style.

### showCursor

[ref: #symbol-showcursor]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Shows the cursor.

### terminalHeight

[ref: #symbol-terminalheight]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns some reasonable terminal height from either standard file descriptors, controlling terminal, environment variables or tradition. Zero is returned if the height could not be determined.

### terminalHeightIoctl

[ref: #symbol-terminalheightioctl]

**Input:**
- `fds: openArray[int]`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns terminal height from first fd that supports the ioctl.

### terminalSize

[ref: #symbol-terminalsize]

**Input:**
- *(none)*

**Output:** `tuple[w, h: int]`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns the terminal width and height as a tuple. Internally calls terminalWidth and terminalHeight, so the same assumptions apply.

### terminalWidth

[ref: #symbol-terminalwidth]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect`, `forbids: `

Returns some reasonable terminal width from either standard file descriptors, controlling terminal, environment variables or tradition.

### terminalWidthIoctl

[ref: #symbol-terminalwidthioctl]

**Input:**
- `fds: openArray[int]`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns terminal width from first fd that supports the ioctl.

### writeStyled

[ref: #symbol-writestyled]

**Input:**
- `txt: string`
- `style: set[Style] = {styleBright}`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Writes the text txt in a given style to stdout.

## Template

### ansiBackgroundColorCode

[ref: #symbol-ansibackgroundcolorcode]

**Input:**
- `color: static[Color]`

**Output:** `string`
**Generic parameters:** `color:type`

### ansiForegroundColorCode

[ref: #symbol-ansiforegroundcolorcode]

**Input:**
- `fg: static[ForegroundColor]`
- `bright: static[bool] = false`

**Output:** `string`
**Generic parameters:** `fg:type`, `bright:type`

### ansiForegroundColorCode

[ref: #symbol-ansiforegroundcolorcode]

**Input:**
- `color: static[Color]`

**Output:** `string`
**Generic parameters:** `color:type`

### ansiStyleCode

[ref: #symbol-ansistylecode]

**Input:**
- `style: Style`

**Output:** `string`
### ansiStyleCode

[ref: #symbol-ansistylecode]

**Input:**
- `style: static[Style]`

**Output:** `string`
**Generic parameters:** `style:type`

### cursorBackward

[ref: #symbol-cursorbackward]

**Input:**
- `count:  = 1`

**Output:** *(none)*
### cursorDown

[ref: #symbol-cursordown]

**Input:**
- `count:  = 1`

**Output:** *(none)*
### cursorForward

[ref: #symbol-cursorforward]

**Input:**
- `count:  = 1`

**Output:** *(none)*
### cursorUp

[ref: #symbol-cursorup]

**Input:**
- `count:  = 1`

**Output:** *(none)*
### eraseLine

[ref: #symbol-eraseline]

**Input:**
- *(none)*

**Output:** *(none)*
### eraseScreen

[ref: #symbol-erasescreen]

**Input:**
- *(none)*

**Output:** *(none)*
### hideCursor

[ref: #symbol-hidecursor]

**Input:**
- *(none)*

**Output:** *(none)*
### setBackgroundColor

[ref: #symbol-setbackgroundcolor]

**Input:**
- `bg: BackgroundColor`
- `bright:  = false`

**Output:** *(none)*
### setBackgroundColor

[ref: #symbol-setbackgroundcolor]

**Input:**
- `color: Color`

**Output:** *(none)*
### setCursorPos

[ref: #symbol-setcursorpos]

**Input:**
- `x: int`
- `y: int`

**Output:** *(none)*
### setCursorXPos

[ref: #symbol-setcursorxpos]

**Input:**
- `x: int`

**Output:** *(none)*
### setForegroundColor

[ref: #symbol-setforegroundcolor]

**Input:**
- `fg: ForegroundColor`
- `bright:  = false`

**Output:** *(none)*
### setForegroundColor

[ref: #symbol-setforegroundcolor]

**Input:**
- `color: Color`

**Output:** *(none)*
### setStyle

[ref: #symbol-setstyle]

**Input:**
- `style: set[Style]`

**Output:** *(none)*
### showCursor

[ref: #symbol-showcursor]

**Input:**
- *(none)*

**Output:** *(none)*
### styledEcho

[ref: #symbol-styledecho]

**Input:**
- `args: varargs[untyped]`

**Output:** *(none)*
Echoes styles arguments to stdout using styledWriteLine.

### styledWriteLine

[ref: #symbol-styledwriteline]

**Input:**
- `f: File`
- `args: varargs[untyped]`

**Output:** *(none)*
Calls styledWrite and appends a newline at the end.

## Type

### BackgroundColor

[ref: #symbol-backgroundcolor]

```nim
BackgroundColor = enum
  bgBlack = 40,             ## black
  bgRed,                    ## red
  bgGreen,                  ## green
  bgYellow,                 ## yellow
  bgBlue,                   ## blue
  bgMagenta,                ## magenta
  bgCyan,                   ## cyan
  bgWhite,                  ## white
  bg8Bit,                   ## 256-color (not supported, see `enableTrueColors` instead.)
  bgDefault                  ## default terminal background color
```

Terminal's background colors.

### ForegroundColor

[ref: #symbol-foregroundcolor]

```nim
ForegroundColor = enum
  fgBlack = 30,             ## black
  fgRed,                    ## red
  fgGreen,                  ## green
  fgYellow,                 ## yellow
  fgBlue,                   ## blue
  fgMagenta,                ## magenta
  fgCyan,                   ## cyan
  fgWhite,                  ## white
  fg8Bit,                   ## 256-color (not supported, see `enableTrueColors` instead.)
  fgDefault                  ## default terminal foreground color
```

Terminal's foreground colors.

### Style

[ref: #symbol-style]

```nim
Style = enum
  styleBright = 1,          ## bright text
  styleDim,                 ## dim text
  styleItalic,              ## italic (or reverse on terminals not supporting)
  styleUnderscore,          ## underscored text
  styleBlink,               ## blinking/bold text
  styleBlinkRapid,          ## rapid blinking/bold text (not widely supported)
  styleReverse,             ## reverse
  styleHidden,              ## hidden text
  styleStrikethrough         ## strikethrough
```

Different styles for text output.

### TerminalCmd

[ref: #symbol-terminalcmd]

```nim
TerminalCmd = enum
  resetStyle,               ## reset attributes
  fgColor,                  ## set foreground's true color
  bgColor                    ## set background's true color
```

commands that can be expressed as arguments
