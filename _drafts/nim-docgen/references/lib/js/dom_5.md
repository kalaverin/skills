---
source_hash: d99fa24c025b2846
source_path: lib/js/dom.nim
---

### Selection

[ref: #symbol-selection]

```nim
Selection {.importc.} = ref object
  anchorNode*: Node
  anchorOffset*: int
  focusNode*: Node
  focusOffset*: int
  isCollapsed*: bool
  rangeCount*: int
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/Selection)

### ShadowRoot

[ref: #symbol-shadowroot]

```nim
ShadowRoot {.importc.} = ref object of DocumentOrShadowRoot
  delegatesFocus*: bool
  host*: Element
  innerHTML*: cstring
  mode*: cstring
```

### ShadowRootInit

[ref: #symbol-shadowrootinit]

```nim
ShadowRootInit = object of RootObj
  mode*: cstring
  delegatesFocus*: bool
```

### SlotOptions

[ref: #symbol-slotoptions]

```nim
SlotOptions = object of RootObj
  flatten*: bool
```

### StatusBar

[ref: #symbol-statusbar]

```nim
StatusBar = LocationBar
```

### Storage

[ref: #symbol-storage]

```nim
Storage {.importc.} = ref object
```

### StorageEvent

[ref: #symbol-storageevent]

```nim
StorageEvent {.importc.} = ref object of Event
  key*: cstring
  newValue*, oldValue*: cstring
  storageArea*: Storage
  url*: cstring
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/StorageEvent)

### Style

[ref: #symbol-style]

```nim
Style {.importc.} = ref object of RootObj
  alignContent*: cstring
  alignItems*: cstring
  alignSelf*: cstring
  all*: cstring
  animation*: cstring
  animationDelay*: cstring
  animationDirection*: cstring
  animationDuration*: cstring
  animationFillMode*: cstring
  animationIterationCount*: cstring
  animationName*: cstring
  animationPlayState*: cstring
  animationTimingFunction*: cstring
  backdropFilter*: cstring
  backfaceVisibility*: cstring
  background*: cstring
  backgroundAttachment*: cstring
  backgroundBlendMode*: cstring
  backgroundClip*: cstring
  backgroundColor*: cstring
  backgroundImage*: cstring
  backgroundOrigin*: cstring
  backgroundPosition*: cstring
  backgroundRepeat*: cstring
  backgroundSize*: cstring
  blockSize*: cstring
  border*: cstring
  borderBlock*: cstring
  borderBlockColor*: cstring
  borderBlockEnd*: cstring
  borderBlockEndColor*: cstring
  borderBlockEndStyle*: cstring
  borderBlockEndWidth*: cstring
  borderBlockStart*: cstring
  borderBlockStartColor*: cstring
  borderBlockStartStyle*: cstring
  borderBlockStartWidth*: cstring
  borderBlockStyle*: cstring
  borderBlockWidth*: cstring
  borderBottom*: cstring
  borderBottomColor*: cstring
  borderBottomLeftRadius*: cstring
  borderBottomRightRadius*: cstring
  borderBottomStyle*: cstring
  borderBottomWidth*: cstring
  borderCollapse*: cstring
  borderColor*: cstring
  borderEndEndRadius*: cstring
  borderEndStartRadius*: cstring
  borderImage*: cstring
  borderImageOutset*: cstring
  borderImageRepeat*: cstring
  borderImageSlice*: cstring
  borderImageSource*: cstring
  borderImageWidth*: cstring
  borderInline*: cstring
  borderInlineColor*: cstring
  borderInlineEnd*: cstring
  borderInlineEndColor*: cstring
  borderInlineEndStyle*: cstring
  borderInlineEndWidth*: cstring
  borderInlineStart*: cstring
  borderInlineStartColor*: cstring
  borderInlineStartStyle*: cstring
  borderInlineStartWidth*: cstring
  borderInlineStyle*: cstring
  borderInlineWidth*: cstring
  borderLeft*: cstring
  borderLeftColor*: cstring
  borderLeftStyle*: cstring
  borderLeftWidth*: cstring
  borderRadius*: cstring
  borderRight*: cstring
  borderRightColor*: cstring
  borderRightStyle*: cstring
  borderRightWidth*: cstring
  borderSpacing*: cstring
  borderStartEndRadius*: cstring
  borderStartStartRadius*: cstring
  borderStyle*: cstring
  borderTop*: cstring
  borderTopColor*: cstring
  borderTopLeftRadius*: cstring
  borderTopRightRadius*: cstring
  borderTopStyle*: cstring
  borderTopWidth*: cstring
  borderWidth*: cstring
  bottom*: cstring
  boxDecorationBreak*: cstring
  boxShadow*: cstring
  boxSizing*: cstring
  breakAfter*: cstring
  breakBefore*: cstring
  breakInside*: cstring
  captionSide*: cstring
  caretColor*: cstring
  clear*: cstring
  clip*: cstring
  clipPath*: cstring
  color*: cstring
  colorAdjust*: cstring
  columnCount*: cstring
  columnFill*: cstring
  columnGap*: cstring
  columnRule*: cstring
  columnRuleColor*: cstring
  columnRuleStyle*: cstring
  columnRuleWidth*: cstring
  columnSpan*: cstring
  columnWidth*: cstring
  columns*: cstring
  contain*: cstring
  content*: cstring
  counterIncrement*: cstring
  counterReset*: cstring
  counterSet*: cstring
  cursor*: cstring
  direction*: cstring
  display*: cstring
  emptyCells*: cstring
  filter*: cstring
  flex*: cstring
  flexBasis*: cstring
  flexDirection*: cstring
  flexFlow*: cstring
  flexGrow*: cstring
  flexShrink*: cstring
  flexWrap*: cstring
  cssFloat*: cstring
  font*: cstring
  fontFamily*: cstring
  fontFeatureSettings*: cstring
  fontKerning*: cstring
  fontLanguageOverride*: cstring
  fontOpticalSizing*: cstring
  fontSize*: cstring
  fontSizeAdjust*: cstring
  fontStretch*: cstring
  fontStyle*: cstring
  fontSynthesis*: cstring
  fontVariant*: cstring
  fontVariantAlternates*: cstring
  fontVariantCaps*: cstring
  fontVariantEastAsian*: cstring
  fontVariantLigatures*: cstring
  fontVariantNumeric*: cstring
  fontVariantPosition*: cstring
  fontVariationSettings*: cstring
  fontWeight*: cstring
  gap*: cstring
  grid*: cstring
  gridArea*: cstring
  gridAutoColumns*: cstring
  gridAutoFlow*: cstring
  gridAutoRows*: cstring
  gridColumn*: cstring
  gridColumnEnd*: cstring
  gridColumnStart*: cstring
  gridRow*: cstring
  gridRowEnd*: cstring
  gridRowStart*: cstring
  gridTemplate*: cstring
  gridTemplateAreas*: cstring
  gridTemplateColumns*: cstring
  gridTemplateRows*: cstring
  hangingPunctuation*: cstring
  height*: cstring
  hyphens*: cstring
  imageOrientation*: cstring
  imageRendering*: cstring
  inlineSize*: cstring
  inset*: cstring
  insetBlock*: cstring
  insetBlockEnd*: cstring
  insetBlockStart*: cstring
  insetInline*: cstring
  insetInlineEnd*: cstring
  insetInlineStart*: cstring
  isolation*: cstring
  justifyContent*: cstring
  justifyItems*: cstring
  justifySelf*: cstring
  left*: cstring
  letterSpacing*: cstring
  lineBreak*: cstring
  lineHeight*: cstring
  listStyle*: cstring
  listStyleImage*: cstring
  listStylePosition*: cstring
  listStyleType*: cstring
  margin*: cstring
  marginBlock*: cstring
  marginBlockEnd*: cstring
  marginBlockStart*: cstring
  marginBottom*: cstring
  marginInline*: cstring
  marginInlineEnd*: cstring
  marginInlineStart*: cstring
  marginLeft*: cstring
  marginRight*: cstring
  marginTop*: cstring
  mask*: cstring
  maskBorder*: cstring
  maskBorderMode*: cstring
  maskBorderOutset*: cstring
  maskBorderRepeat*: cstring
  maskBorderSlice*: cstring
  maskBorderSource*: cstring
  maskBorderWidth*: cstring
  maskClip*: cstring
  maskComposite*: cstring
  maskImage*: cstring
  maskMode*: cstring
  maskOrigin*: cstring
  maskPosition*: cstring
  maskRepeat*: cstring
  maskSize*: cstring
  maskType*: cstring
  maxBlockSize*: cstring
  maxHeight*: cstring
  maxInlineSize*: cstring
  maxWidth*: cstring
  minBlockSize*: cstring
  minHeight*: cstring
  minInlineSize*: cstring
  minWidth*: cstring
  mixBlendMode*: cstring
  objectFit*: cstring
  objectPosition*: cstring
  offset*: cstring
  offsetAnchor*: cstring
  offsetDistance*: cstring
  offsetPath*: cstring
  offsetRotate*: cstring
  opacity*: cstring
  order*: cstring
  orphans*: cstring
  outline*: cstring
  outlineColor*: cstring
  outlineOffset*: cstring
  outlineStyle*: cstring
  outlineWidth*: cstring
  overflow*: cstring
  overflowAnchor*: cstring
  overflowBlock*: cstring
  overflowInline*: cstring
  overflowWrap*: cstring
  overflowX*: cstring
  overflowY*: cstring
  overscrollBehavior*: cstring
  overscrollBehaviorBlock*: cstring
  overscrollBehaviorInline*: cstring
  overscrollBehaviorX*: cstring
  overscrollBehaviorY*: cstring
  padding*: cstring
  paddingBlock*: cstring
  paddingBlockEnd*: cstring
  paddingBlockStart*: cstring
  paddingBottom*: cstring
  paddingInline*: cstring
  paddingInlineEnd*: cstring
  paddingInlineStart*: cstring
  paddingLeft*: cstring
  paddingRight*: cstring
  paddingTop*: cstring
  pageBreakAfter*: cstring
  pageBreakBefore*: cstring
  pageBreakInside*: cstring
  paintOrder*: cstring
  perspective*: cstring
  perspectiveOrigin*: cstring
  placeContent*: cstring
  placeItems*: cstring
  placeSelf*: cstring
  pointerEvents*: cstring
  position*: cstring
  quotes*: cstring
  resize*: cstring
  right*: cstring
  rotate*: cstring
  rowGap*: cstring
  scale*: cstring
  scrollBehavior*: cstring
  scrollMargin*: cstring
  scrollMarginBlock*: cstring
  scrollMarginBlockEnd*: cstring
  scrollMarginBlockStart*: cstring
  scrollMarginBottom*: cstring
  scrollMarginInline*: cstring
  scrollMarginInlineEnd*: cstring
  scrollMarginInlineStart*: cstring
  scrollMarginLeft*: cstring
  scrollMarginRight*: cstring
  scrollMarginTop*: cstring
  scrollPadding*: cstring
  scrollPaddingBlock*: cstring
  scrollPaddingBlockEnd*: cstring
  scrollPaddingBlockStart*: cstring
  scrollPaddingBottom*: cstring
  scrollPaddingInline*: cstring
  scrollPaddingInlineEnd*: cstring
  scrollPaddingInlineStart*: cstring
  scrollPaddingLeft*: cstring
  scrollPaddingRight*: cstring
  scrollPaddingTop*: cstring
  scrollSnapAlign*: cstring
  scrollSnapStop*: cstring
  scrollSnapType*: cstring
  scrollbar3dLightColor*: cstring
  scrollbarArrowColor*: cstring
  scrollbarBaseColor*: cstring
  scrollbarColor*: cstring
  scrollbarDarkshadowColor*: cstring
  scrollbarFaceColor*: cstring
  scrollbarHighlightColor*: cstring
  scrollbarShadowColor*: cstring
  scrollbarTrackColor*: cstring
  scrollbarWidth*: cstring
  shapeImageThreshold*: cstring
  shapeMargin*: cstring
  shapeOutside*: cstring
  tabSize*: cstring
  tableLayout*: cstring
  textAlign*: cstring
  textAlignLast*: cstring
  textCombineUpright*: cstring
  textDecoration*: cstring
  textDecorationColor*: cstring
  textDecorationLine*: cstring
  textDecorationSkipInk*: cstring
  textDecorationStyle*: cstring
  textDecorationThickness*: cstring
  textEmphasis*: cstring
  textEmphasisColor*: cstring
  textEmphasisPosition*: cstring
  textEmphasisStyle*: cstring
  textIndent*: cstring
  textJustify*: cstring
  textOrientation*: cstring
  textOverflow*: cstring
  textRendering*: cstring
  textShadow*: cstring
  textTransform*: cstring
  textUnderlineOffset*: cstring
  textUnderlinePosition*: cstring
  top*: cstring
  touchAction*: cstring
  transform*: cstring
  transformBox*: cstring
  transformOrigin*: cstring
  transformStyle*: cstring
  transition*: cstring
  transitionDelay*: cstring
  transitionDuration*: cstring
  transitionProperty*: cstring
  transitionTimingFunction*: cstring
  translate*: cstring
  unicodeBidi*: cstring
  verticalAlign*: cstring
  visibility*: cstring
  whiteSpace*: cstring
  widows*: cstring
  width*: cstring
  willChange*: cstring
  wordBreak*: cstring
  wordSpacing*: cstring
  writingMode*: cstring
  zIndex*: cstring
```

### TextAreaElement

[ref: #symbol-textareaelement]

```nim
TextAreaElement {.importc.} = ref object of Element
  value*: cstring
  selectionStart*, selectionEnd*: int
  selectionDirection*: cstring
  rows*, cols*: int
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/HTMLTextAreaElement)

### TimeOut

[ref: #symbol-timeout]

```nim
TimeOut {.importc.} = ref object of RootObj
```

### ToolBar

[ref: #symbol-toolbar]

```nim
ToolBar = LocationBar
```

### Touch

[ref: #symbol-touch]

```nim
Touch {.importc.} = ref object of RootObj
  identifier*: int
  screenX*, screenY*, clientX*, clientY*, pageX*, pageY*: int
  target*: Element
  radiusX*, radiusY*: int
  rotationAngle*: int
  force*: float
```

### TouchEvent

[ref: #symbol-touchevent]

```nim
TouchEvent {.importc.} = ref object of UIEvent
  changedTouches*, targetTouches*, touches*: seq[Touch]
```

### TouchList

[ref: #symbol-touchlist]

```nim
TouchList {.importc.} = ref object of RootObj
  length*: int
```

### UIEvent

[ref: #symbol-uievent]

```nim
UIEvent {.importc.} = ref object of Event
  detail*: int64
  view*: Window
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/UIEvent)

### ValidityState

[ref: #symbol-validitystate]

```nim
ValidityState {.importc.} = ref object
  badInput*: bool
  customError*: bool
  patternMismatch*: bool
  rangeOverflow*: bool
  rangeUnderflow*: bool
  stepMismatch*: bool
  tooLong*: bool
  tooShort*: bool
  typeMismatch*: bool
  valid*: bool
  valueMissing*: bool
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/ValidityState)

### VisualViewport

[ref: #symbol-visualviewport]

```nim
VisualViewport {.importc.} = ref object of EventTarget
  offsetLeft*, offsetTop*, pageLeft*, pageTop*, width*, height*, scale*: float
  onResize*, onScroll*: proc (event: Event) {.closure.}
```

### Window

[ref: #symbol-window]

```nim
Window {.importc.} = ref object of EventTarget
  document*: Document
  event*: Event
  history*: History
  location*: Location
  closed*: bool
  defaultStatus*: cstring
  devicePixelRatio*: float
  innerHeight*, innerWidth*: int
  locationbar*: ref LocationBar
  menubar*: ref MenuBar
  name*: cstring
  outerHeight*, outerWidth*: int
  pageXOffset*, pageYOffset*: int
  scrollX*: float
  scrollY*: float
  personalbar*: ref PersonalBar
  scrollbars*: ref ScrollBars
  statusbar*: ref StatusBar
  status*: cstring
  toolbar*: ref ToolBar
  frames*: seq[Frame]
  screen*: Screen
  performance*: Performance
  onpopstate*: proc (event: Event)
  localStorage*: Storage
  sessionStorage*: Storage
  parent*: Window
```

## Var

### document

[ref: #symbol-document]

```nim
document {.importc, nodecl.}: Document
```

### navigator

[ref: #symbol-navigator]

```nim
navigator {.importc, nodecl.}: Navigator
```

### screen

[ref: #symbol-screen]

```nim
screen {.importc, nodecl.}: Screen
```

### window

[ref: #symbol-window]

```nim
window {.importc, nodecl.}: Window
```

[Prev](dom_4.md)
