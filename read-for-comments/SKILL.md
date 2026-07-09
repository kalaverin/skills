---
name: read-for-comments
description: >
  Always-active local reference library for technical standards (RFC, OWASP, STD, etc.).
  Before fetching any standard from the internet, the agent MUST check this skill's
  references/ directory. Use Kagi search only when the requested standard is not
  present locally.
triggers:
  always: true
  reason: "Local copies of common standards should be preferred over web searches in every session."
---

# SKILL: Local Standards Reference Library

This skill hosts local copies of frequently referenced technical standards. It is **always active**.

## Lookup protocol

1. When you need a standard (RFC, OWASP, STD, etc.), first list this skill's `references/` directory.
2. If the standard is present locally, read that file. Do **not** search the web.
3. If it is absent, fall back to `kagi_search_fetch` or `kagi_fastgpt`.
4. Always save the complete standard body using the `serena` tool to the `standard/` scope with the appropriate path structure, e.g.: `standard/rfc/rfc1439` or `standard/pep/pep8`.

## Listing local standards

```bash
fd -t f . references/
```

## Current inventory

| Standard | File |
|---|---|
| RFC 2119 — Key words for requirement levels | `references/rfc2119.md` |
| RFC 8174 — Ambiguity of uppercase vs lowercase in RFC 2119 | `references/rfc8174.md` |

Add new standards as plain Markdown or text files under `references/` using predictable names (`rfc<id>.md`, `owasp<id>.md`, `std<id>.md`, etc.).
