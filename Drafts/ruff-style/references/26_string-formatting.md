---
---

# String formatting

Prefer f-strings over `%` and `.format`; keep conversions and placeholders valid and matched; pass gettext a static message id and format afterward.

## Rule of thumb

1. Prefer f-strings for interpolation; reach for them before `.format` or `%`.
2. Match placeholders to arguments: count, names, types, and star-widths must align.
3. Keep each format string internally consistent: don't mix positional and named placeholders, or automatic and manual numbering.
4. Use supported format characters and matching argument types; avoid invalid conversions.
5. Pass gettext a static template, then format the returned translation; never pre-format inside `_()`.
6. Replace slice-and-function tricks (`bin(n)[2:]`) with format specifiers and use dedicated prefix/suffix removers.
7. Drop redundant syntax: empty `print("")`, f-strings without placeholders, and Python 2 `print >>`.

## Example: printf-style formatting

A report formatter written by a junior who still reaches for `%` syntax.

### Bad

```python
"""Report formatter using old % syntax."""

from datetime import datetime


def build_report(title, author, date, score, meta):
    """Return a multi-line report string."""
    header = "Report: %" % title  # F501
    greeting = "%(greeting)s, %(name)s" % ("Hello", author)  # F502,UP031
    body = "%s, %s" % {"greeting": "Hello", "name": author}  # F503,F507,UP031
    footer = "By %(name)s on %(date)s" % {"name": author, "date": date, "source": "web"}  # F504,UP031
    stats = "Score: %(score)s / %(total)s" % {"score": score}  # F505,UP031
    mixed = "%s, %(name)s" % ("Hello", {"name": "World"})  # F502,F506,UP031
    tags = "%s %s %s" % ("draft", title)  # F507,UP031
    precise = "%(n).*f" % {"n": (2, 3.14159)}  # F506,F508,PLE1307,UP031
    loud = "Title: %S" % title  # F509,PLE1300
    encoded = "%z" % 1  # F509,PLE1300
    numeric = "ID: %d" % "42"  # PLE1307,UP031
    lines = [header, greeting, body, footer, stats, mixed, tags, precise, loud, encoded, numeric]
    report = "\n".join(lines)
    return report.upper()
```

### Good

```python
"""Report formatter using f-strings."""


def build_report(title, author, date, score, meta):
    """Return a multi-line report string."""
    header = f"Report: {title}"
    byline = f"By {author} on {date}"
    summary = f"Score: {score} / 100"
    tags = f"Tags: draft, {title}, {meta}"
    ratio = f"Pi is {3.14159:.2f}"
    identifier = f"ID: {42}"
    lines = [header, byline, summary, tags, ratio, identifier]
    report = "\n".join(lines)
    return report.upper()
```

### Violations

1. **F501** — `"Report: %" % title`; bare `%` lacks a conversion type.
2. **F502** — `"%(greeting)s, %(name)s" % ("Hello", author)` and `"%s, %(name)s" % (...)`; named placeholders require a mapping.
3. **F503** — `"%s, %s" % {"greeting": "Hello", "name": author}`; positional placeholders require a sequence.
4. **F504** — `"...", "source": "web"}`; unused key `source` in the mapping.
5. **F505** — `"... / %(total)s" % {"score": score}`; missing value for the `total` placeholder.
6. **F506** — `"%s, %(name)s" % ("Hello", {"name": "World"})` and `"%(n).*f" % {"n": (2, 3.14159)}`; mixed positional and named placeholders.
7. **F507** — `"%s, %s" % {...}` and `"%s %s %s" % ("draft", title)`; placeholders outnumber the arguments.
8. **F508** — `"%(n).*f" % {"n": (2, 3.14159)}`; the `*` specifier needs a sequence argument.
9. **F509** — `"Title: %S"` and `"%z"`; `%S`/`%z` are not supported format characters.
10. **PLE1300** — `"Title: %S"` and `"%z"`; unsupported format characters.
11. **PLE1307** — `"ID: %d" % "42"` and `"%(n).*f" % {"n": (2, 3.14159)}`; the argument type does not match the format specifier.

## Example: str.format formatting

A logger that abuses `str.format` with invalid strings and mismatched arguments.

### Bad

```python
"""Logger using str.format."""


def format_event(level, message, user):
    """Return a formatted log entry.

    This builds several variants so callers can pick a layout.
    """
    banner = "{".format(level)  # F521
    prefix = "Level: {level}".format(level=level, unused=True)  # F522,UP032
    brief = "{}".format(message, level)  # F523,UP032
    full = "{level}: {user}".format(level=level)  # F524
    combo = "{0}, {}".format(level, message)  # F523,F525,UP032
    parts = [banner, prefix, brief, full, combo]
    return " | ".join(parts)


def emit(record):
    print(format_event(*record))
```

### Good

```python
"""Logger using f-strings."""


def format_event(level, message, user):
    """Return a formatted log entry."""
    banner = f"Level: {level}"
    brief = f"{level}: {message}"
    full = f"{level}: {user}"
    combo = f"{level}, {message}"
    parts = [banner, brief, full, combo]
    return " | ".join(parts)


def emit(record):
    print(format_event(*record))
```

### Violations

1. **F521** — `"{".format(level)`; unbalanced braces make the format string invalid.
2. **F522** — `"Level: {level}".format(level=level, unused=True)`; unused keyword argument `unused`.
3. **F523** — `"{}".format(message, level)` and `"{0}, {}".format(level, message)`; extra positional arguments.
4. **F524** — `"{level}: {user}".format(level=level)`; missing value for the `user` placeholder.
5. **F525** — `"{0}, {}".format(level, message)`; mixing manual `{0}` and automatic `{}` numbering.

## Example: pyupgrade modernization

A formatter still using percent syntax and explicit `.format` indices that should be f-strings.

### Bad

```python
"""Formatter with outdated spelling."""


def show(user):
    """Build greetings with legacy syntax.

    Demonstrates percent formatting, explicit positional indices, and
    single-argument str.format that should all be f-strings.
    """
    old = "%s, %s" % ("Hello", user)  # UP031
    indexed = "{0}, {1}".format("Hello", user)  # UP030
    single = "{}".format(user)  # UP032
    lines = [old, indexed, single]
    return "\n".join(lines)


def display(users):
    for user in users:
        print(show(user))
```

### Good

```python
"""Formatter using f-strings."""


def show(user):
    """Build greetings with f-strings."""
    old = f"Hello, {user}"
    indexed = f"Hello, {user}"
    single = f"{user}"
    lines = [old, indexed, single]
    return "\n".join(lines)


def display(users):
    for user in users:
        print(show(user))
```

### Violations

1. **UP030** — `"{0}, {1}".format("Hello", user)`; redundant positional indices.
2. **UP031** — `"%s, %s" % ("Hello", user)`; prefer f-strings over percent formatting.
3. **UP032** — `"{}".format(user)`; prefer f-strings over `.format`.

## Example: modern string building and print hygiene

Console helpers that misuse `join`, `print`, f-strings, and `strip`.

### Bad

```python
"""Console utilities."""
import sys


def greet(name):
    message = f"Hello, world!"  # F541
    joined = " ".join(("Hello", name))  # FLY002
    return message, joined


def show_bits(n):
    print("")  # FURB105
    print(bin(n)[2:])  # FURB116
    print >> sys.stderr, "done"  # F633


def clean_url():
    url = "https://example.com/path"
    return url.strip("https:// ")  # PLE1310
```

### Good

```python
"""Console utilities."""
import sys


def greet(name):
    message = "Hello, world!"
    joined = f"Hello {name}"
    return message, joined


def show_bits(n):
    print()
    print(f"{n:b}")
    print("done", file=sys.stderr)


def clean_url():
    url = "https://example.com/path"
    return url.removeprefix("https://")
```

### Violations

1. **F541** — `f"Hello, world!"`; f-string with no placeholders.
2. **F633** — `print >> sys.stderr, "done"`; Python 2 print statement syntax.
3. **FLY002** — `" ".join(("Hello", name))`; use an f-string instead of joining a fixed tuple.
4. **FURB105** — `print("")`; unnecessary empty string argument.
5. **FURB116** — `bin(n)[2:]`; use the format specifier `f"{n:b}"`.
6. **PLE1310** — `url.strip("https:// ")`; duplicate characters in `strip`; use `removeprefix`/`removesuffix` for exact removal.

## Example: gettext

A greeting service that formats strings before passing them to gettext.

### Bad

```python
"""Greeting service with gettext."""

from gettext import gettext as _


name = "Maria"


def say_hello():
    """Return three localized greetings for comparison.

    Each branch demonstrates a different anti-pattern: formatting before
    translation means the catalog sees the already-interpolated string.
    """
    a = _(f"Hello, {name}!")  # INT001
    b = _("Hello, {}!".format(name))  # INT002,UP032
    c = _("Hello, %s!" % name)  # INT003,UP031
    return {
        "fstring": a,
        "format": b,
        "percent": c,
    }
```

### Good

```python
"""Greeting service with gettext."""

from gettext import gettext as _


name = "Maria"


def say_hello():
    """Return a localized greeting."""
    template = _("Hello, %s!")
    return template % name
```

### Violations

1. **INT001** — `_(f"Hello, {name}!")`; the f-string is resolved before gettext lookup.
2. **INT002** — `_("Hello, {}!".format(name))`; `.format` is resolved before gettext lookup.
3. **INT003** — `_("Hello, %s!" % name)`; percent formatting is resolved before gettext lookup.
