---
source_hash: 4a1060cd664e2c7e
source_path: lib/pure/colors.nim
---

### colPapayaWhip

[ref: #symbol-colpapayawhip]

```nim
colPapayaWhip = 16773077
```

### colPeachPuff

[ref: #symbol-colpeachpuff]

```nim
colPeachPuff = 16767673
```

### colPeru

[ref: #symbol-colperu]

```nim
colPeru = 13468991
```

### colPink

[ref: #symbol-colpink]

```nim
colPink = 16761035
```

### colPlum

[ref: #symbol-colplum]

```nim
colPlum = 14524637
```

### colPowderBlue

[ref: #symbol-colpowderblue]

```nim
colPowderBlue = 11591910
```

### colPurple

[ref: #symbol-colpurple]

```nim
colPurple = 8388736
```

### colRebeccaPurple

[ref: #symbol-colrebeccapurple]

```nim
colRebeccaPurple = 6697881
```

### colRed

[ref: #symbol-colred]

```nim
colRed = 16711680
```

### colRosyBrown

[ref: #symbol-colrosybrown]

```nim
colRosyBrown = 12357519
```

### colRoyalBlue

[ref: #symbol-colroyalblue]

```nim
colRoyalBlue = 4286945
```

### colSaddleBrown

[ref: #symbol-colsaddlebrown]

```nim
colSaddleBrown = 9127187
```

### colSalmon

[ref: #symbol-colsalmon]

```nim
colSalmon = 16416882
```

### colSandyBrown

[ref: #symbol-colsandybrown]

```nim
colSandyBrown = 16032864
```

### colSeaGreen

[ref: #symbol-colseagreen]

```nim
colSeaGreen = 3050327
```

### colSeaShell

[ref: #symbol-colseashell]

```nim
colSeaShell = 16774638
```

### colSienna

[ref: #symbol-colsienna]

```nim
colSienna = 10506797
```

### colSilver

[ref: #symbol-colsilver]

```nim
colSilver = 12632256
```

### colSkyBlue

[ref: #symbol-colskyblue]

```nim
colSkyBlue = 8900331
```

### colSlateBlue

[ref: #symbol-colslateblue]

```nim
colSlateBlue = 6970061
```

### colSlateGray

[ref: #symbol-colslategray]

```nim
colSlateGray = 7372944
```

### colSlateGrey

[ref: #symbol-colslategrey]

```nim
colSlateGrey = 7372944
```

### colSnow

[ref: #symbol-colsnow]

```nim
colSnow = 16775930
```

### colSpringGreen

[ref: #symbol-colspringgreen]

```nim
colSpringGreen = 65407
```

### colSteelBlue

[ref: #symbol-colsteelblue]

```nim
colSteelBlue = 4620980
```

### colTan

[ref: #symbol-coltan]

```nim
colTan = 13808780
```

### colTeal

[ref: #symbol-colteal]

```nim
colTeal = 32896
```

### colThistle

[ref: #symbol-colthistle]

```nim
colThistle = 14204888
```

### colTomato

[ref: #symbol-coltomato]

```nim
colTomato = 16737095
```

### colTurquoise

[ref: #symbol-colturquoise]

```nim
colTurquoise = 4251856
```

### colViolet

[ref: #symbol-colviolet]

```nim
colViolet = 15631086
```

### colWheat

[ref: #symbol-colwheat]

```nim
colWheat = 16113331
```

### colWhite

[ref: #symbol-colwhite]

```nim
colWhite = 16777215
```

### colWhiteSmoke

[ref: #symbol-colwhitesmoke]

```nim
colWhiteSmoke = 16119285
```

### colYellow

[ref: #symbol-colyellow]

```nim
colYellow = 16776960
```

### colYellowGreen

[ref: #symbol-colyellowgreen]

```nim
colYellowGreen = 10145074
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `c: Color`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a color into its textual representation.

### `+`

[ref: #symbol-]

Adds two colors.

**Input:**
- `a: Color`
- `b: Color`

**Output:** `Color`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds two colors.

This uses saturated arithmetic, so that each color component cannot overflow (255 is used as a maximum).

### `-`

[ref: #symbol-]

Subtracts two colors.

**Input:**
- `a: Color`
- `b: Color`

**Output:** `Color`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Subtracts two colors.

This uses saturated arithmetic, so that each color component cannot underflow (0 is used as a minimum).

### `==`

[ref: #symbol-]

Compares two colors.

**Input:**
- `a: Color`
- `b: Color`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two colors.

```
var
  a = Color(0xff_00_ff)
  b = colFuchsia
  c = Color(0x00_ff_cc)
assert a == b
assert not (a == c)
```

### extractRGB

[ref: #symbol-extractrgb]

**Input:**
- `a: Color`

**Output:** `tuple[r, g, b: range[0 .. 255]]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Extracts the red/green/blue components of the color a.

### intensity

[ref: #symbol-intensity]

**Input:**
- `a: Color`
- `f: float`

**Output:** `Color`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a with intensity f. f should be a float from 0.0 (completely dark) to 1.0 (full color intensity).

### isColor

[ref: #symbol-iscolor]

**Input:**
- `name: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if name is a known color name or a hexadecimal color prefixed with #. Case insensitive.

### parseColor

[ref: #symbol-parsecolor]

Parses name to a color value.

**Input:**
- `name: string`

**Output:** `Color`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses name to a color value.

If no valid color could be parsed ValueError is raised. Case insensitive.

### rgb

[ref: #symbol-rgb]

**Input:**
- `r: range[0 .. 255]`
- `g: range[0 .. 255]`
- `b: range[0 .. 255]`

**Output:** `Color`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructs a color from RGB values.

## Template

### mix

[ref: #symbol-mix]

Uses fn to mix the colors a and b.

**Input:**
- `a: Color`
- `b: Color`
- `fn: untyped`

**Output:** `untyped`
Uses fn to mix the colors a and b.

fn is invoked for each component R, G, and B. If fn's result is not in the range[0..255], it will be saturated to be so.

## Type

### Color

[ref: #symbol-color]

```nim
Color = distinct int
```

A color stored as RGB, e.g. 0xff00cc.

[Prev](colors_1.md)
