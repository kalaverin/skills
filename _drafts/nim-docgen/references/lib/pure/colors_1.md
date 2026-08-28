---
source_hash: 4a1060cd664e2c7e
source_path: lib/pure/colors.nim
---

# colors

[ref: #module-colors]

This module implements color handling for Nim, namely color mixing and parsing the CSS color names.

## Examples

```nim
assert $colFuchsia == "#FF00FF"
```

```nim
var
  a = Color(0xaa_00_ff)
  b = Color(0x11_cc_cc)
assert a + b == Color(0xbb_cc_ff)
```

```nim
var
  a = Color(0xff_33_ff)
  b = Color(0x11_ff_cc)
assert a - b == Color(0xee_00_33)
```

```nim
var
  a = Color(0xff_00_ff)
  b = colFuchsia
  c = Color(0x00_ff_cc)
assert a == b
assert not (a == c)
```

```nim
var
  a = Color(0xff_00_ff)
  b = Color(0x00_ff_cc)
type
  Col = range[0..255]
# assert extractRGB(a) == (r: 255.Col, g: 0.Col, b: 255.Col)
# assert extractRGB(b) == (r: 0.Col, g: 255.Col, b: 204.Col)
echo extractRGB(a)
echo typeof(extractRGB(a))
echo extractRGB(b)
echo typeof(extractRGB(b))
```

```nim
var
  a = Color(0xff_00_ff)
  b = Color(0x00_42_cc)
assert a.intensity(0.5) == Color(0x80_00_80)
assert b.intensity(0.5) == Color(0x00_21_66)
```

```nim
var
  a = "silver"
  b = "#0179fc"
  c = "#zzmmtt"
assert a.isColor
assert b.isColor
assert not c.isColor
```

```nim
var
  a = "silver"
  b = "#0179fc"
  c = "#zzmmtt"
assert parseColor(a) == Color(0xc0_c0_c0)
assert parseColor(b) == Color(0x01_79_fc)
doAssertRaises(ValueError): discard parseColor(c)
```

```nim
assert rgb(0, 255, 128) == Color(0x00_ff_80)
```

```nim
var
  a = Color(0x0a2814)
  b = Color(0x050a03)

proc myMix(x, y: int): int =
  2 * x - 3 * y

assert mix(a, b, myMix) == Color(0x05_32_1f)
```

## Const

### colAliceBlue

[ref: #symbol-colaliceblue]

```nim
colAliceBlue = 15792383
```

### colAntiqueWhite

[ref: #symbol-colantiquewhite]

```nim
colAntiqueWhite = 16444375
```

### colAqua

[ref: #symbol-colaqua]

```nim
colAqua = 65535
```

### colAquamarine

[ref: #symbol-colaquamarine]

```nim
colAquamarine = 8388564
```

### colAzure

[ref: #symbol-colazure]

```nim
colAzure = 15794175
```

### colBeige

[ref: #symbol-colbeige]

```nim
colBeige = 16119260
```

### colBisque

[ref: #symbol-colbisque]

```nim
colBisque = 16770244
```

### colBlack

[ref: #symbol-colblack]

```nim
colBlack = 0
```

### colBlanchedAlmond

[ref: #symbol-colblanchedalmond]

```nim
colBlanchedAlmond = 16772045
```

### colBlue

[ref: #symbol-colblue]

```nim
colBlue = 255
```

### colBlueViolet

[ref: #symbol-colblueviolet]

```nim
colBlueViolet = 9055202
```

### colBrown

[ref: #symbol-colbrown]

```nim
colBrown = 10824234
```

### colBurlyWood

[ref: #symbol-colburlywood]

```nim
colBurlyWood = 14596231
```

### colCadetBlue

[ref: #symbol-colcadetblue]

```nim
colCadetBlue = 6266528
```

### colChartreuse

[ref: #symbol-colchartreuse]

```nim
colChartreuse = 8388352
```

### colChocolate

[ref: #symbol-colchocolate]

```nim
colChocolate = 13789470
```

### colCoral

[ref: #symbol-colcoral]

```nim
colCoral = 16744272
```

### colCornflowerBlue

[ref: #symbol-colcornflowerblue]

```nim
colCornflowerBlue = 6591981
```

### colCornsilk

[ref: #symbol-colcornsilk]

```nim
colCornsilk = 16775388
```

### colCrimson

[ref: #symbol-colcrimson]

```nim
colCrimson = 14423100
```

### colCyan

[ref: #symbol-colcyan]

```nim
colCyan = 65535
```

### colDarkBlue

[ref: #symbol-coldarkblue]

```nim
colDarkBlue = 139
```

### colDarkCyan

[ref: #symbol-coldarkcyan]

```nim
colDarkCyan = 35723
```

### colDarkGoldenRod

[ref: #symbol-coldarkgoldenrod]

```nim
colDarkGoldenRod = 12092939
```

### colDarkGray

[ref: #symbol-coldarkgray]

```nim
colDarkGray = 11119017
```

### colDarkGreen

[ref: #symbol-coldarkgreen]

```nim
colDarkGreen = 25600
```

### colDarkGrey

[ref: #symbol-coldarkgrey]

```nim
colDarkGrey = 11119017
```

### colDarkKhaki

[ref: #symbol-coldarkkhaki]

```nim
colDarkKhaki = 12433259
```

### colDarkMagenta

[ref: #symbol-coldarkmagenta]

```nim
colDarkMagenta = 9109643
```

### colDarkOliveGreen

[ref: #symbol-coldarkolivegreen]

```nim
colDarkOliveGreen = 5597999
```

### colDarkorange

[ref: #symbol-coldarkorange]

```nim
colDarkorange = 16747520
```

### colDarkOrchid

[ref: #symbol-coldarkorchid]

```nim
colDarkOrchid = 10040012
```

### colDarkRed

[ref: #symbol-coldarkred]

```nim
colDarkRed = 9109504
```

### colDarkSalmon

[ref: #symbol-coldarksalmon]

```nim
colDarkSalmon = 15308410
```

### colDarkSeaGreen

[ref: #symbol-coldarkseagreen]

```nim
colDarkSeaGreen = 9419919
```

### colDarkSlateBlue

[ref: #symbol-coldarkslateblue]

```nim
colDarkSlateBlue = 4734347
```

### colDarkSlateGray

[ref: #symbol-coldarkslategray]

```nim
colDarkSlateGray = 3100495
```

### colDarkSlateGrey

[ref: #symbol-coldarkslategrey]

```nim
colDarkSlateGrey = 3100495
```

### colDarkTurquoise

[ref: #symbol-coldarkturquoise]

```nim
colDarkTurquoise = 52945
```

### colDarkViolet

[ref: #symbol-coldarkviolet]

```nim
colDarkViolet = 9699539
```

### colDeepPink

[ref: #symbol-coldeeppink]

```nim
colDeepPink = 16716947
```

### colDeepSkyBlue

[ref: #symbol-coldeepskyblue]

```nim
colDeepSkyBlue = 49151
```

### colDimGray

[ref: #symbol-coldimgray]

```nim
colDimGray = 6908265
```

### colDimGrey

[ref: #symbol-coldimgrey]

```nim
colDimGrey = 6908265
```

### colDodgerBlue

[ref: #symbol-coldodgerblue]

```nim
colDodgerBlue = 2003199
```

### colFireBrick

[ref: #symbol-colfirebrick]

```nim
colFireBrick = 11674146
```

### colFloralWhite

[ref: #symbol-colfloralwhite]

```nim
colFloralWhite = 16775920
```

### colForestGreen

[ref: #symbol-colforestgreen]

```nim
colForestGreen = 2263842
```

### colFuchsia

[ref: #symbol-colfuchsia]

```nim
colFuchsia = 16711935
```

### colGainsboro

[ref: #symbol-colgainsboro]

```nim
colGainsboro = 14474460
```

### colGhostWhite

[ref: #symbol-colghostwhite]

```nim
colGhostWhite = 16316671
```

### colGold

[ref: #symbol-colgold]

```nim
colGold = 16766720
```

### colGoldenRod

[ref: #symbol-colgoldenrod]

```nim
colGoldenRod = 14329120
```

### colGray

[ref: #symbol-colgray]

```nim
colGray = 8421504
```

### colGreen

[ref: #symbol-colgreen]

```nim
colGreen = 32768
```

### colGreenYellow

[ref: #symbol-colgreenyellow]

```nim
colGreenYellow = 11403055
```

### colGrey

[ref: #symbol-colgrey]

```nim
colGrey = 8421504
```

### colHoneyDew

[ref: #symbol-colhoneydew]

```nim
colHoneyDew = 15794160
```

### colHotPink

[ref: #symbol-colhotpink]

```nim
colHotPink = 16738740
```

### colIndianRed

[ref: #symbol-colindianred]

```nim
colIndianRed = 13458524
```

### colIndigo

[ref: #symbol-colindigo]

```nim
colIndigo = 4915330
```

### colIvory

[ref: #symbol-colivory]

```nim
colIvory = 16777200
```

### colKhaki

[ref: #symbol-colkhaki]

```nim
colKhaki = 15787660
```

### colLavender

[ref: #symbol-collavender]

```nim
colLavender = 15132410
```

### colLavenderBlush

[ref: #symbol-collavenderblush]

```nim
colLavenderBlush = 16773365
```

### colLawnGreen

[ref: #symbol-collawngreen]

```nim
colLawnGreen = 8190976
```

### colLemonChiffon

[ref: #symbol-collemonchiffon]

```nim
colLemonChiffon = 16775885
```

### colLightBlue

[ref: #symbol-collightblue]

```nim
colLightBlue = 11393254
```

### colLightCoral

[ref: #symbol-collightcoral]

```nim
colLightCoral = 15761536
```

### colLightCyan

[ref: #symbol-collightcyan]

```nim
colLightCyan = 14745599
```

### colLightGoldenRodYellow

[ref: #symbol-collightgoldenrodyellow]

```nim
colLightGoldenRodYellow = 16448210
```

### colLightGray

[ref: #symbol-collightgray]

```nim
colLightGray = 13882323
```

### colLightGreen

[ref: #symbol-collightgreen]

```nim
colLightGreen = 9498256
```

### colLightGrey

[ref: #symbol-collightgrey]

```nim
colLightGrey = 13882323
```

### colLightPink

[ref: #symbol-collightpink]

```nim
colLightPink = 16758465
```

### colLightSalmon

[ref: #symbol-collightsalmon]

```nim
colLightSalmon = 16752762
```

### colLightSeaGreen

[ref: #symbol-collightseagreen]

```nim
colLightSeaGreen = 2142890
```

### colLightSkyBlue

[ref: #symbol-collightskyblue]

```nim
colLightSkyBlue = 8900346
```

### colLightSlateGray

[ref: #symbol-collightslategray]

```nim
colLightSlateGray = 7833753
```

### colLightSlateGrey

[ref: #symbol-collightslategrey]

```nim
colLightSlateGrey = 7833753
```

### colLightSteelBlue

[ref: #symbol-collightsteelblue]

```nim
colLightSteelBlue = 11584734
```

### colLightYellow

[ref: #symbol-collightyellow]

```nim
colLightYellow = 16777184
```

### colLime

[ref: #symbol-collime]

```nim
colLime = 65280
```

### colLimeGreen

[ref: #symbol-collimegreen]

```nim
colLimeGreen = 3329330
```

### colLinen

[ref: #symbol-collinen]

```nim
colLinen = 16445670
```

### colMagenta

[ref: #symbol-colmagenta]

```nim
colMagenta = 16711935
```

### colMaroon

[ref: #symbol-colmaroon]

```nim
colMaroon = 8388608
```

### colMediumAquaMarine

[ref: #symbol-colmediumaquamarine]

```nim
colMediumAquaMarine = 6737322
```

### colMediumBlue

[ref: #symbol-colmediumblue]

```nim
colMediumBlue = 205
```

### colMediumOrchid

[ref: #symbol-colmediumorchid]

```nim
colMediumOrchid = 12211667
```

### colMediumPurple

[ref: #symbol-colmediumpurple]

```nim
colMediumPurple = 9662683
```

### colMediumSeaGreen

[ref: #symbol-colmediumseagreen]

```nim
colMediumSeaGreen = 3978097
```

### colMediumSlateBlue

[ref: #symbol-colmediumslateblue]

```nim
colMediumSlateBlue = 8087790
```

### colMediumSpringGreen

[ref: #symbol-colmediumspringgreen]

```nim
colMediumSpringGreen = 64154
```

### colMediumTurquoise

[ref: #symbol-colmediumturquoise]

```nim
colMediumTurquoise = 4772300
```

### colMediumVioletRed

[ref: #symbol-colmediumvioletred]

```nim
colMediumVioletRed = 13047173
```

### colMidnightBlue

[ref: #symbol-colmidnightblue]

```nim
colMidnightBlue = 1644912
```

### colMintCream

[ref: #symbol-colmintcream]

```nim
colMintCream = 16121850
```

### colMistyRose

[ref: #symbol-colmistyrose]

```nim
colMistyRose = 16770273
```

### colMoccasin

[ref: #symbol-colmoccasin]

```nim
colMoccasin = 16770229
```

### colNavajoWhite

[ref: #symbol-colnavajowhite]

```nim
colNavajoWhite = 16768685
```

### colNavy

[ref: #symbol-colnavy]

```nim
colNavy = 128
```

### colOldLace

[ref: #symbol-cololdlace]

```nim
colOldLace = 16643558
```

### colOlive

[ref: #symbol-cololive]

```nim
colOlive = 8421376
```

### colOliveDrab

[ref: #symbol-cololivedrab]

```nim
colOliveDrab = 7048739
```

### colOrange

[ref: #symbol-colorange]

```nim
colOrange = 16753920
```

### colOrangeRed

[ref: #symbol-colorangered]

```nim
colOrangeRed = 16729344
```

### colOrchid

[ref: #symbol-colorchid]

```nim
colOrchid = 14315734
```

### colPaleGoldenRod

[ref: #symbol-colpalegoldenrod]

```nim
colPaleGoldenRod = 15657130
```

### colPaleGreen

[ref: #symbol-colpalegreen]

```nim
colPaleGreen = 10025880
```

### colPaleTurquoise

[ref: #symbol-colpaleturquoise]

```nim
colPaleTurquoise = 11529966
```

### colPaleVioletRed

[ref: #symbol-colpalevioletred]

```nim
colPaleVioletRed = 14381203
```


[Next](colors_2.md)
