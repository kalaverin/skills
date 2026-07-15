---
source_hash: d99fa24c025b2846
source_path: lib/js/dom.nim
---

### unescape

[ref: #symbol-unescape]

**Input:**
- `uri: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### value

[ref: #symbol-value]

**Input:**
- `n: Node`

**Output:** `cstring`
**Pragmas:** `importcpp: "#.value"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### value=

[ref: #symbol-value]

**Input:**
- `n: Node`
- `v: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.value = #"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### vibrate

[ref: #symbol-vibrate]

**Input:**
- `self: Navigator`
- `pattern: cint`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vibrate>

### vibrate

[ref: #symbol-vibrate]

**Input:**
- `self: Navigator`
- `pattern: openArray[cint]`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vibrate>

### visualViewport

[ref: #symbol-visualviewport]

**Input:**
- `self: Window`

**Output:** `VisualViewport`
**Pragmas:** `importjs: "#.$1"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `d: Document`
- `text: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### writeln

[ref: #symbol-writeln]

**Input:**
- `d: Document`
- `text: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### AddEventListenerOptions

[ref: #symbol-addeventlisteneroptions]

```nim
AddEventListenerOptions = object
  capture*: bool
  once*: bool
  passive*: bool
```

### AnchorElement

[ref: #symbol-anchorelement]

```nim
AnchorElement {.importc.} = ref object of Element
  text*: cstring
  x*, y*: int
```

### Blob

[ref: #symbol-blob]

```nim
Blob {.importc.} = ref object of RootObj
  size*: int
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/Blob)

### BoundingRect

[ref: #symbol-boundingrect]

```nim
BoundingRect {.importc.} = object
  top*, bottom*, left*, right*, x*, y*, width*, height*: float
```

### ClassList

[ref: #symbol-classlist]

```nim
ClassList {.importc.} = ref object of RootObj
```

### ClipboardEvent

[ref: #symbol-clipboardevent]

```nim
ClipboardEvent {.importc.} = object of Event
  clipboardData*: DataTransfer
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/ClipboardEvent)

### DataTransfer

[ref: #symbol-datatransfer]

```nim
DataTransfer {.importc.} = ref object of RootObj
  dropEffect*: cstring
  effectAllowed*: cstring
  files*: seq[Element]
  items*: seq[DataTransferItem]
  types*: seq[cstring]
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/DataTransfer)

### DataTransferDropEffect

[ref: #symbol-datatransferdropeffect]

```nim
DataTransferDropEffect {.pure.} = enum
  None = "none", Copy = "copy", Link = "link", Move = "move"
```

### DataTransferEffectAllowed

[ref: #symbol-datatransfereffectallowed]

```nim
DataTransferEffectAllowed {.pure.} = enum
  None = "none", Copy = "copy", CopyLink = "copyLink", CopyMove = "copyMove",
  Link = "link", LinkMove = "linkMove", Move = "move", All = "all",
  Uninitialized = "uninitialized"
```

### DataTransferItem

[ref: #symbol-datatransferitem]

```nim
DataTransferItem {.importc.} = ref object of RootObj
  kind*: cstring
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/DataTransferItem)

### DataTransferItemKind

[ref: #symbol-datatransferitemkind]

```nim
DataTransferItemKind {.pure.} = enum
  File = "file", String = "string"
```

### Document

[ref: #symbol-document]

```nim
Document {.importc.} = ref object of Node
  activeElement*: Element
  documentElement*: Element
  alinkColor*: cstring
  bgColor*: cstring
  body*: Element
  charset*: cstring
  cookie*: cstring
  defaultCharset*: cstring
  fgColor*: cstring
  head*: Element
  hidden*: bool
  lastModified*: cstring
  linkColor*: cstring
  referrer*: cstring
  title*: cstring
  URL*: cstring
  visibilityState*: cstring
  vlinkColor*: cstring
  anchors*: seq[AnchorElement]
  forms*: seq[FormElement]
  images*: seq[ImageElement]
  applets*: seq[Element]
  embeds*: seq[EmbedElement]
  links*: seq[LinkElement]
  fonts*: FontFaceSet
```

### DocumentOrShadowRoot

[ref: #symbol-documentorshadowroot]

```nim
DocumentOrShadowRoot {.importc.} = object of RootObj
  activeElement*: Element
```

### DomEvent

[ref: #symbol-domevent]

```nim
DomEvent {.pure.} = enum
  Abort = "abort", BeforeInput = "beforeinput", Blur = "blur", Click = "click",
  CompositionEnd = "compositionend", CompositionStart = "compositionstart",
  CompositionUpdate = "compositionupdate", DblClick = "dblclick",
  Error = "error", Focus = "focus", FocusIn = "focusin", FocusOut = "focusout",
  Input = "input", KeyDown = "keydown", KeyPress = "keypress", KeyUp = "keyup",
  Load = "load", MouseDown = "mousedown", MouseEnter = "mouseenter",
  MouseLeave = "mouseleave", MouseMove = "mousemove", MouseOut = "mouseout",
  MouseOver = "mouseover", MouseUp = "mouseup", Resize = "resize",
  Scroll = "scroll", Select = "select", Storage = "storage", Unload = "unload",
  Wheel = "wheel"
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/Events)

### DomException

[ref: #symbol-domexception]

```nim
DomException {.importc.} = ref object
```

The DOMException interface represents an abnormal event (called an exception) which occurs as a result of calling a method or accessing a property of a web API. Each exception has a name, which is a short "CamelCase" style string identifying the error or abnormal condition. <https://developer.mozilla.org/en-US/docs/Web/API/DOMException>

### DomParser

[ref: #symbol-domparser]

DOM Parser object (defined on browser only, may not be on NodeJS).

```nim
DomParser = ref object
```

DOM Parser object (defined on browser only, may not be on NodeJS).

* <https://developer.mozilla.org/en-US/docs/Web/API/DOMParser>

  ```
  let prsr = newDomParser()
  discard prsr.parseFromString("<html><marquee>Hello World</marquee></html>".cstring, "text/html".cstring)
  ```

### DragEvent

[ref: #symbol-dragevent]

```nim
DragEvent {.importc.} = object of MouseEvent
  dataTransfer*: DataTransfer
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/DragEvent)

### DragEventTypes

[ref: #symbol-drageventtypes]

```nim
DragEventTypes = enum
  Drag = "drag", DragEnd = "dragend", DragEnter = "dragenter",
  DragExit = "dragexit", DragLeave = "dragleave", DragOver = "dragover",
  DragStart = "dragstart", Drop = "drop"
```

### Element

[ref: #symbol-element]

```nim
Element {.importc.} = ref object of Node
  className*: cstring
  classList*: ClassList
  checked*: bool
  defaultChecked*: bool
  defaultValue*: cstring
  disabled*: bool
  form*: FormElement
  name*: cstring
  readOnly*: bool
  options*: seq[OptionElement]
  selectedOptions*: seq[OptionElement]
  clientWidth*, clientHeight*: int
  contentEditable*: cstring
  isContentEditable*: bool
  dir*: cstring
  offsetHeight*: int
  offsetWidth*: int
  offsetLeft*: int
  offsetTop*: int
```

### EmbedElement

[ref: #symbol-embedelement]

```nim
EmbedElement {.importc.} = ref object of Element
  height*: int
  hspace*: int
  src*: cstring
  width*: int
  vspace*: int
```

### Event

[ref: #symbol-event]

```nim
Event {.importc.} = ref object of RootObj
  bubbles*: bool
  cancelBubble*: bool
  cancelable*: bool
  composed*: bool
  currentTarget*: Node
  defaultPrevented*: bool
  eventPhase*: int
  target*: Node
  isTrusted*: bool
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/Event)

### EventPhase

[ref: #symbol-eventphase]

```nim
EventPhase = enum
  None = 0, CapturingPhase, AtTarget, BubblingPhase
```

### EventTarget

[ref: #symbol-eventtarget]

```nim
EventTarget {.importc.} = ref object of RootObj
  onabort*: proc (event: Event) {.closure.}
  onblur*: proc (event: Event) {.closure.}
  onchange*: proc (event: Event) {.closure.}
  onclick*: proc (event: Event) {.closure.}
  ondblclick*: proc (event: Event) {.closure.}
  onerror*: proc (event: Event) {.closure.}
  onfocus*: proc (event: Event) {.closure.}
  onkeydown*: proc (event: Event) {.closure.}
  onkeypress*: proc (event: Event) {.closure.}
  onkeyup*: proc (event: Event) {.closure.}
  onload*: proc (event: Event) {.closure.}
  onmousedown*: proc (event: Event) {.closure.}
  onmousemove*: proc (event: Event) {.closure.}
  onmouseout*: proc (event: Event) {.closure.}
  onmouseover*: proc (event: Event) {.closure.}
  onmouseup*: proc (event: Event) {.closure.}
  onreset*: proc (event: Event) {.closure.}
  onselect*: proc (event: Event) {.closure.}
  onstorage*: proc (event: Event) {.closure.}
  onsubmit*: proc (event: Event) {.closure.}
  onunload*: proc (event: Event) {.closure.}
  onloadstart*: proc (event: Event) {.closure.}
  onprogress*: proc (event: Event) {.closure.}
  onloadend*: proc (event: Event) {.closure.}
```

### File

[ref: #symbol-file]

```nim
File {.importc.} = ref object of Blob
  lastModified*: int
  name*: cstring
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/File)

### FileReader

[ref: #symbol-filereader]

```nim
FileReader {.importc.} = ref object of EventTarget
```

The FileReader object lets web applications asynchronously read the contents of files (or raw data buffers) stored on the user's computer, using File or Blob objects to specify the file or data to read. <https://developer.mozilla.org/en-US/docs/Web/API/FileReader>

### FileReaderState

[ref: #symbol-filereaderstate]

```nim
FileReaderState = distinct range[0'u16 .. 2'u16]
```

### FontFaceSet

[ref: #symbol-fontfaceset]

```nim
FontFaceSet {.importc.} = ref object
  ready*: FontFaceSetReady
  onloadingdone*: proc (event: Event)
```

see: [docs](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet)

### FontFaceSetReady

[ref: #symbol-fontfacesetready]

```nim
FontFaceSetReady {.importc.} = ref object
  then*: proc (cb: proc ())
```

see: [docs](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready)

### FormElement

[ref: #symbol-formelement]

```nim
FormElement {.importc.} = ref object of Element
  acceptCharset*: cstring
  action*: cstring
  autocomplete*: cstring
  elements*: seq[Element]
  encoding*: cstring
  enctype*: cstring
  length*: int
  noValidate*: bool
  target*: cstring
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement)

### Frame

[ref: #symbol-frame]

```nim
Frame {.importc.} = ref object of Window
```

### History

[ref: #symbol-history]

```nim
History {.importc.} = ref object of RootObj
  length*: int
```

### HTMLSlotElement

[ref: #symbol-htmlslotelement]

```nim
HTMLSlotElement {.importc.} = ref object of RootObj
  name*: cstring
```

### ImageElement

[ref: #symbol-imageelement]

```nim
ImageElement {.importc.} = ref object of Element
  border*: int
  complete*: bool
  height*: int
  hspace*: int
  lowsrc*: cstring
  src*: cstring
  vspace*: int
  width*: int
```

### InputElement

[ref: #symbol-inputelement]

```nim
InputElement {.importc.} = ref object of Element
  formAction*: cstring
  formEncType*: cstring
  formMethod*: cstring
  formNoValidate*: bool
  formTarget*: cstring
  autofocus*: bool
  required*: bool
  value*: cstring
  validity*: ValidityState
  validationMessage*: cstring
  willValidate*: bool
  indeterminate*: bool
  alt*: cstring
  height*: cstring
  src*: cstring
  width*: cstring
  accept*: cstring
  files*: seq[Blob]
  autocomplete*: cstring
  maxLength*: int
  size*: int
  pattern*: cstring
  placeholder*: cstring
  min*: cstring
  max*: cstring
  selectionStart*: int
  selectionEnd*: int
  selectionDirection*: cstring
  dirName*: cstring
  accessKey*: cstring
  list*: Element
  multiple*: bool
  labels*: seq[Element]
  step*: cstring
  valueAsDate*: cstring
  valueAsNumber*: float
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement)

### Interval

[ref: #symbol-interval]

```nim
Interval {.importc.} = ref object of RootObj
```

### KeyboardEvent

[ref: #symbol-keyboardevent]

```nim
KeyboardEvent {.importc.} = ref object of UIEvent
  altKey*, ctrlKey*, metaKey*, shiftKey*: bool
  code*: cstring
  isComposing*: bool
  key*: cstring
  keyCode*: int
  location*: int
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent)

### KeyboardEventKey

[ref: #symbol-keyboardeventkey]

```nim
KeyboardEventKey {.pure.} = enum
  Alt, AltGraph, CapsLock, Control, Fn, FnLock, Hyper, Meta, NumLock,
  ScrollLock, Shift, Super, Symbol, SymbolLock, ArrowDown, ArrowLeft,
  ArrowRight, ArrowUp, End, Home, PageDown, PageUp, Backspace, Clear, Copy,
  CrSel, Cut, Delete, EraseEof, ExSel, Insert, Paste, Redo, Undo, Accept, Again,
  Attn, Cancel, ContextMenu, Escape, Execute, Find, Finish, Help, Pause, Play,
  Props, Select, ZoomIn, ZoomOut, BrigtnessDown, BrigtnessUp, Eject, LogOff,
  Power, PowerOff, PrintScreen, Hibernate, Standby, WakeUp, AllCandidates,
  Alphanumeric, CodeInput, Compose, Convert, Dead, FinalMode, GroupFirst,
  GroupLast, GroupNext, GroupPrevious, ModeChange, NextCandidate, NonConvert,
  PreviousCandidate, Process, SingleCandidate, HangulMode, HanjaMode, JunjaMode,
  Eisu, Hankaku, Hiragana, HiraganaKatakana, KanaMode, KanjiMode, Katakana,
  Romaji, Zenkaku, ZenkakuHanaku, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11,
  F12, F13, F14, F15, F16, F17, F18, F19, F20, Soft1, Soft2, Soft3, Soft4,
  AppSwitch, Call, Camera, CameraFocus, EndCall, GoBack, GoHome, HeadsetHook,
  LastNumberRedial, Notification, MannerMode, VoiceDial, ChannelDown, ChannelUp,
  MediaFastForward, MediaPause, MediaPlay, MediaPlayPause, MediaRecord,
  MediaRewind, MediaStop, MediaTrackNext, MediaTrackPrevious, AudioBalanceLeft,
  AudioBalanceRight, AudioBassDown, AudioBassBoostDown, AudioBassBoostToggle,
  AudioBassBoostUp, AudioBassUp, AudioFaderFront, AudioFaderRear,
  AudioSurroundModeNext, AudioTrebleDown, AudioTrebleUp, AudioVolumeDown,
  AUdioVolumeMute, AudioVolumeUp, MicrophoneToggle, MicrophoneVolumeDown,
  MicrophoneVolumeMute, MicrophoneVolumeUp, TV, TV3DMode, TVAntennaCable,
  TVAudioDescription, TVAudioDescriptionMixDown, TVAudioDescriptionMixUp,
  TVContentsMenu, TVDataService, TVInput, TVInputComponent1, TVInputComponent2,
  TVInputComposite1, TVInputComposite2, TVInputHDMI1, TVInputHDMI2,
  TVInputHDMI3, TVInputHDMI4, TVInputVGA1, TVMediaContext, TVNetwork,
  TVNumberEntry, TVPower, TVRadioService, TVSatellite, TVSatelliteBS,
  TVSatelliteCS, TVSatelliteToggle, TVTerrestrialAnalog, TVTerrestrialDigital,
  TVTimer, AVRInput, AVRPower, ColorF0Red, ColorF1Green, ColorF2Yellow,
  ColorF3Blue, ColorF4Grey, ColorF5Brown, ClosedCaptionToggle, Dimmer,
  DisplaySwap, DVR, Exit, FavoriteClear0, FavoriteClear1, FavoriteClear2,
  FavoriteClear3, FavoriteRecall0, FavoriteRecall1, FavoriteRecall2,
  FavoriteRecall3, FavoriteStore0, FavoriteStore1, FavoriteStore2,
  FavoriteStore3, Guide, GuideNextDay, GuidePreviousDay, Info, InstantReplay,
  Link, ListProgram, LiveContent, Lock, MediaApps, MediaAudioTrack, MediaLast,
  MediaSkipBackward, MediaSkipForward, MediaStepBackward, MediaStepForward,
  MediaTopMenu, NavigateIn, NavigateNext, NavigateOut, NavigatePrevious,
  NextFavoriteChannel, NextUserProfile, OnDemand, Pairing, PinPDown, PinPMove,
  PinPUp, PlaySpeedDown, PlaySpeedReset, PlaySpeedUp, RandomToggle,
  RcLowBattery, RecordSpeedNext, RfBypass, ScanChannelsToggle, ScreenModeNext,
  Settings, SplitScreenToggle, STBInput, STBPower, Subtitle, Teletext,
  VideoModeNext, Wink, ZoomToggle, SpeechCorrectionList, SpeechInputToggle,
  Close, New, Open, Print, Save, SpellCheck, MailForward, MailReply, MailSend,
  LaunchCalculator, LaunchCalendar, LaunchContacts, LaunchMail,
  LaunchMediaPlayer, LaunchMusicPlayer, LaunchMyComputer, LaunchPhone,
  LaunchScreenSaver, LaunchSpreadsheet, LaunchWebBrowser, LaunchWebCam,
  LaunchWordProcessor, LaunchApplication1, LaunchApplication2,
  LaunchApplication3, LaunchApplication4, LaunchApplication5,
  LaunchApplication6, LaunchApplication7, LaunchApplication8,
  LaunchApplication9, LaunchApplication10, LaunchApplication11,
  LaunchApplication12, LaunchApplication13, LaunchApplication14,
  LaunchApplication15, LaunchApplication16, BrowserBack, BrowserFavorites,
  BrowserForward, BrowserHome, BrowserRefresh, BrowserSearch, BrowserStop,
  Key11, Key12, Separator
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key/Key_Values)

### LinkElement

[ref: #symbol-linkelement]

```nim
LinkElement {.importc.} = ref object of Element
  target*: cstring
  text*: cstring
  x*: int
  y*: int
```

### Location

[ref: #symbol-location]

```nim
Location {.importc.} = ref object of RootObj
  hash*: cstring
  host*: cstring
  hostname*: cstring
  href*: cstring
  pathname*: cstring
  port*: cstring
  protocol*: cstring
  search*: cstring
  origin*: cstring
```

### LocationBar

[ref: #symbol-locationbar]

```nim
LocationBar {.importc.} = object of RootObj
  visible*: bool
```

### MediaQueryList

[ref: #symbol-mediaquerylist]

```nim
MediaQueryList {.importc.} = ref object of EventTarget
  matches*: bool
  media*: cstring
```

### MenuBar

[ref: #symbol-menubar]

```nim
MenuBar = LocationBar
```

### MimeType

[ref: #symbol-mimetype]

```nim
MimeType {.importc.} = object of RootObj
  description*: cstring
  enabledPlugin*: ref Plugin
  suffixes*: seq[cstring]
```

### MouseButtons

[ref: #symbol-mousebuttons]

```nim
MouseButtons = enum
  NoButton = 0, PrimaryButton = 1, SecondaryButton = 2, AuxilaryButton = 4,
  FourthButton = 8, FifthButton = 16
```

### MouseEvent

[ref: #symbol-mouseevent]

```nim
MouseEvent {.importc.} = ref object of UIEvent
  altKey*, ctrlKey*, metaKey*, shiftKey*: bool
  button*: int
  buttons*: int
  clientX*, clientY*: int
  movementX*, movementY*: int
  offsetX*, offsetY*: int
  pageX*, pageY*: int
  relatedTarget*: EventTarget
  screenX*, screenY*: int
  x*, y*: int
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent)

### Navigator

[ref: #symbol-navigator]

```nim
Navigator {.importc.} = ref object of RootObj
  appCodeName*: cstring
  appName*: cstring
  appVersion*: cstring
  buildID*: cstring          ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/buildID
  cookieEnabled*: bool
  deviceMemory*: float       ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/deviceMemory
  doNotTrack*: cstring       ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/doNotTrack
  language*: cstring
  languages*: seq[cstring]   ## https://developer.mozilla.org/en-US/docs/Web/API/NavigatorLanguage/languages
  maxTouchPoints*: cint      ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/maxTouchPoints
  onLine*: bool              ## https://developer.mozilla.org/en-US/docs/Web/API/NavigatorOnLine/onLine
  oscpu*: cstring            ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/oscpu
  platform*: cstring
  userAgent*: cstring
  vendor*: cstring           ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vendor
  webdriver*: bool           ## https://developer.mozilla.org/en-US/docs/Web/API/Navigator/webdriver
  mimeTypes*: seq[ref MimeType]
```

### Node

[ref: #symbol-node]

```nim
Node {.importc.} = ref object of EventTarget
  attributes*: seq[Node]
  childNodes*: seq[Node]
  children*: seq[Node]
  data*: cstring
  firstChild*: Node
  lastChild*: Node
  nextSibling*: Node
  nodeName*: cstring
  nodeType*: NodeType
  nodeValue*: cstring
  parentNode*: Node
  content*: Node
  previousSibling*: Node
  ownerDocument*: Document
  innerHTML*: cstring
  outerHTML*: cstring
  innerText*: cstring
  textContent*: cstring
  style*: Style
  baseURI*: cstring
  parentElement*: Element
  isConnected*: bool
```

### NodeType

[ref: #symbol-nodetype]

```nim
NodeType = enum
  ElementNode = 1, AttributeNode, TextNode, CDATANode, EntityRefNode,
  EntityNode, ProcessingInstructionNode, CommentNode, DocumentNode,
  DocumentTypeNode, DocumentFragmentNode, NotationNode
```

### OptionElement

[ref: #symbol-optionelement]

```nim
OptionElement {.importc.} = ref object of Element
  defaultSelected*: bool
  selected*: bool
  selectedIndex*: int
  text*: cstring
  value*: cstring
```

### Performance

[ref: #symbol-performance]

```nim
Performance {.importc.} = ref object
  memory*: PerformanceMemory
  timing*: PerformanceTiming
```

### PerformanceMemory

[ref: #symbol-performancememory]

```nim
PerformanceMemory {.importc.} = ref object
  jsHeapSizeLimit*: float
  totalJSHeapSize*: float
  usedJSHeapSize*: float
```

### PerformanceTiming

[ref: #symbol-performancetiming]

```nim
PerformanceTiming {.importc.} = ref object
  connectStart*: float
  domComplete*: float
  domContentLoadedEventEnd*: float
  domContentLoadedEventStart*: float
  domInteractive*: float
  domLoading*: float
  domainLookupEnd*: float
  domainLookupStart*: float
  fetchStart*: float
  loadEventEnd*: float
  loadEventStart*: float
  navigationStart*: float
  redirectEnd*: float
  redirectStart*: float
  requestStart*: float
  responseEnd*: float
  responseStart*: float
  secureConnectionStart*: float
  unloadEventEnd*: float
  unloadEventStart*: float
```

### PersonalBar

[ref: #symbol-personalbar]

```nim
PersonalBar = LocationBar
```

### Plugin

[ref: #symbol-plugin]

```nim
Plugin {.importc.} = object of RootObj
  description*: cstring
  filename*: cstring
  name*: cstring
```

### Range

[ref: #symbol-range]

```nim
Range {.importc.} = ref object
  collapsed*: bool
  commonAncestorContainer*: Node
  endContainer*: Node
  endOffset*: int
  startContainer*: Node
  startOffset*: int
```

see [docs](https://developer.mozilla.org/en-US/docs/Web/API/Range)

### RootNodeOptions

[ref: #symbol-rootnodeoptions]

```nim
RootNodeOptions = object of RootObj
  composed*: bool
```

### Screen

[ref: #symbol-screen]

```nim
Screen {.importc.} = ref object of RootObj
  availHeight*: int
  availWidth*: int
  colorDepth*: int
  height*: int
  pixelDepth*: int
  width*: int
```

### ScrollBars

[ref: #symbol-scrollbars]

```nim
ScrollBars = LocationBar
```

### ScrollIntoViewOptions

[ref: #symbol-scrollintoviewoptions]

```nim
ScrollIntoViewOptions = object
  behavior*: cstring
  inline*: cstring
```


[Prev](dom_3.md) | [Next](dom_5.md)
