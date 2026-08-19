---
---

# Security: Content

Parse untrusted content defensively: safe XML/HTML/markup handling, no dangerous deserialization or template sinks.

## Rule of thumb

1. Treat every string from users, files, or network responses as hostile until a context-aware escaper has handled it.
2. Build markup with escaping helpers — `format_html`, `Markup("<b>{}</b>").format(...)` — never `mark_safe` or `Markup(f"...")` on dynamic data.
3. Turn on template auto-escaping (`jinja2.select_autoescape`, mako `|h`) or drop engines that render raw by default.
4. Parse XML only through `defusedxml`; keep every stdlib `xml.*` parser and import out of untrusted-data paths.
5. Patch `xmlrpc` with `defusedxml.xmlrpc.monkey_patch()` before importing it, and serve WSGI apps from real servers, never CGI handlers.
6. Silence unavoidable audit-class findings with a targeted `# noqa: CODE` that names the mitigation, not a blanket ignore.

## Example: HTML and template escaping

A profile page renderer that mixes Django, markupsafe, jinja2, and mako — and disables every escaper on the way.

### Bad

```python
"""Render user profile pages."""

import jinja2
from django.utils.safestring import mark_safe
from markupsafe import Markup
from mako.template import Template

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))  # S701


def render_username(username: str) -> str:
    return mark_safe(f"<i>{username}</i>")  # S308


def render_bio(bio: str) -> Markup:
    return Markup(f"<p>{bio}</p>")  # S704


def render_comment(comment: str) -> str:
    template = Template("<div>${ data }</div>")  # S702
    return template.render(data=comment)
```

### Good

```python
"""Render user profile pages."""

import jinja2
from django.utils.html import format_html
from markupsafe import Markup

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)


def render_username(username: str) -> str:
    return format_html("<i>{}</i>", username)


def render_bio(bio: str) -> Markup:
    return Markup("<p>{}</p>").format(bio)


def render_comment(comment: str) -> str:
    template = env.from_string("<div>{{ data }}</div>")
    return template.render(data=comment)
```

### Violations

1. **S308** — `mark_safe(f"<i>{username}</i>")`; marking an f-string safe bypasses Django auto-escaping and admits XSS.
2. **S701** — `jinja2.Environment(loader=...)`; `autoescape` defaults to `False`, so rendered variables go out unescaped.
3. **S702** — `Template("<div>${ data }</div>")`; mako renders HTML/JS raw by default unless every variable carries an `h`/`x` filter.
4. **S704** — `Markup(f"<p>{bio}</p>")`; a non-literal passed to `Markup` is flagged already-safe and never escaped.

## Example: XML feed ingestion

A legacy ingestion service where different helpers grew their own stdlib XML parser for partner uploads.

### Bad

```python
"""Parse partner XML feeds and config uploads."""

import xml.dom.expatbuilder  # S407
import xml.dom.minidom  # S408
import xml.dom.pulldom  # S409
import xml.etree.ElementTree as ET  # S405
import xml.sax  # S406
from xml.etree.cElementTree import fromstring  # S405
from xml.sax.expatreader import create_parser


def load_config(path: str):
    return ET.parse(path).getroot()  # S314


def parse_payload(text: str):
    return fromstring(text)  # S313


def sax_scan(path: str, handler) -> None:
    parser = xml.sax.make_parser()  # S317
    parser.setContentHandler(handler)
    parser.parse(path)


def fast_scan(path: str, handler) -> None:
    parser = create_parser()  # S315
    parser.setContentHandler(handler)
    parser.parse(path)


def dom_summary(path: str) -> str:
    doc = xml.dom.minidom.parse(path)  # S318
    return doc.documentElement.tagName


def dom_rebuild(path: str):
    return xml.dom.expatbuilder.parse(path)  # S316


def iter_items(path: str):
    events = xml.dom.pulldom.parse(path)  # S319
    for event, node in events:
        if event == xml.dom.pulldom.START_ELEMENT:
            yield node.tagName
```

### Good

```python
"""Parse partner XML feeds and config uploads."""

from defusedxml import ElementTree as ET
from defusedxml import expatbuilder, minidom, pulldom
from defusedxml.cElementTree import fromstring
from defusedxml.sax import make_parser


def load_config(path: str):
    return ET.parse(path).getroot()


def parse_payload(text: str):
    return fromstring(text)


def scan(path: str, handler) -> None:
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(path)


def dom_summary(path: str) -> str:
    doc = minidom.parse(path)
    return doc.documentElement.tagName


def dom_rebuild(path: str):
    return expatbuilder.parse(path)


def iter_items(path: str):
    events = pulldom.parse(path)
    for event, node in events:
        if event == pulldom.START_ELEMENT:
            yield node.tagName
```

### Violations

1. **S313** — `fromstring(text)`; cElementTree is open to entity-expansion attacks on untrusted input.
2. **S314** — `ET.parse(path)`; stdlib ElementTree parses untrusted files without entity or external-reference limits.
3. **S315** — `create_parser()`; the raw expat reader lacks XML attack mitigations.
4. **S316** — `xml.dom.expatbuilder.parse(path)`; the expat DOM builder inherits the same entity-expansion risks.
5. **S317** — `xml.sax.make_parser()`; the stdlib SAX parser is not hardened against malicious XML by default.
6. **S318** — `xml.dom.minidom.parse(path)`; minidom builds on the vulnerable stdlib XML stack.
7. **S319** — `xml.dom.pulldom.parse(path)`; pulldom pulls from the same unsafe XML backend.
8. **S405** — `import xml.etree.ElementTree as ET` and `from xml.etree.cElementTree import fromstring`; importing `xml.etree` keeps the vulnerable parser within reach of untrusted data.
9. **S406** — `import xml.sax`; `xml.sax` methods are vulnerable to XML attacks.
10. **S407** — `import xml.dom.expatbuilder`; direct expat import exposes the Expat attack surface.
11. **S408** — `import xml.dom.minidom`; relies on the vulnerable stdlib XML implementation.
12. **S409** — `import xml.dom.pulldom`; another wrapper around the unsafe XML backend.

## Example: XML-RPC behind CGI

A legacy admin service that exposes functions over XML-RPC and deploys its WSGI app through a CGI handler.

### Bad

```python
"""Legacy admin service exposed over CGI and XML-RPC."""

from xmlrpc import server  # S411
from wsgiref.handlers import CGIHandler  # S412


def approve_order(order_id: int) -> bool:
    return order_id > 0


def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"ok"]


rpc = server.SimpleXMLRPCServer(("localhost", 8000))
rpc.register_function(approve_order)

handler = CGIHandler()
handler.run(application)
```

### Good

```python
"""Admin service on a hardened WSGI server."""

from defusedxml import xmlrpc

xmlrpc.monkey_patch()

from xmlrpc.server import SimpleXMLRPCServer  # noqa: E402  # must follow defusedxml monkey_patch()
from wsgiref.simple_server import make_server


def approve_order(order_id: int) -> bool:
    return order_id > 0


def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"ok"]


def main() -> None:
    rpc = SimpleXMLRPCServer(("localhost", 8000))
    rpc.register_function(approve_order)
    make_server("localhost", 8001, application).serve_forever()
```

### Violations

1. **S411** — `from xmlrpc import server`; XMLRPC deserializes remote XML without hardening and is especially dangerous over a network.
2. **S412** — `from wsgiref.handlers import CGIHandler`; CGI-style handlers forward the `Proxy` header into the environment (httpoxy).
