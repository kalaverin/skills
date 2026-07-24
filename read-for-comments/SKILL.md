---
name: read-for-comments
description: "Mandatory local standards library and archive. Before fetching any standard from the internet, the agent MUST check the Serena `standard/` archive and this skill's `references/` seed; after ANY standard-body download, the agent MUST archive it per the event-bound Archival Rule. Governs standard lookup, fetch, archival, and the family and full-body rules."
triggers:
  always: true
  reason: "Local archived standards must be preferred over web fetches in every session, and every standard download must be archived."
requires:
  - frontmatter-protocol
  - serena-protocol
version: 0.1.0
---

# SKILL: Local Standards Library & Archive

This skill owns standard lookup and archival. Two stores with distinct roles:

- **Archive (searched FIRST):** Serena memories at `standard/<family>/<family>_<id>.md` — every standard ever fetched for this project. The fetch-once archive.
- **Seed (searched SECOND):** this skill's `references/` directory — a tiny curated set of frequently needed standards, hand-filled by the user, traveling with the skill mirror.

## 1. Lookup Gate (HARD)

Before ANY internet search for a standard, in this exact order:

1. **Check the archive:** `list_memories` with topic `standard` (or a path probe for `standard/<family>/<family>_<id>.md`). On a hit, read that memory.
2. **Check the seed:** `fd -t f . references/`. On a hit, read that file.
3. **Only when BOTH miss:** go to the web per `kagi-search`.

You MUST NOT fetch a standard from the internet that already exists in either store.

Current seed inventory:

| Standard | File |
|---|---|
| RFC 2119 — Key words for requirement levels | `references/rfc2119.md` |
| RFC 8174 — Ambiguity of uppercase vs lowercase in RFC 2119 | `references/rfc8174.md` |

## 2. Fetch Rules

- **Content needed in context** (answer, quote, procedure): use `kagi_extract` or `kagi_summarizer` per the `kagi-search` skill.
- **Archival download** (the body must be stored): use a raw downloader (`curl`, `wget`, or FreeBSD `fetch`) into a scratch path — the body NEVER passes through the agent's context. Raw fetch for the exact bytes of a standard is the sanctioned exception of `kagi-search` §1.1.

## 3. Archival Rule (HARD, event-bound)

**Trigger:** ANY download of a standard body from the web, no matter why it was fetched. Archival MUST complete BEFORE the content is used in the answer. No importance judgement: every fetched standard body is archived.

Pipeline (the bulk-import carve-out of `serena-protocol` `[ref: #serena-memory-mutation]`):

1. Download into `.tmp/standards/<family>-<id>.md` with a raw downloader.
2. `mv` into `.serena/memories/standard/<family>/<family>_<id>.md`.
3. **Subagent attestation:** a subagent receives the file path and the URL, then validates and confirms — this IS a standard; the file is complete (beginning and end present); no HTML or other garbage — gives a two-word description of the document, and drafts the frontmatter (~10 lines of YAML: `title`, the tracking fields, `source: <URL>`, `family: <family>`). **On attestation failure** (not a standard, broken file, garbage inside): delete the moved file, report to the user, and STOP. If no subagent is available, the main agent attests per `subagents-protocol` §12 and states the limitation.
4. **Stamp the header:** `edit_memory` with `mode: "regex"`, `needle: "\A"`, `repl: "<frontmatter>\n\n# <Title>\n\n"`. The synthetic H1 (matching `title`) is the boundary — the raw body below it stays UNTOUCHED. **One-H1 waiver:** archive entries are exempt from the one-H1 rule — the synthetic H1 is the only document-level heading; inner headings of the raw body are archive content, not document structure.
5. **Verify the header** ONLY via the canonical frontmatter extraction (`frontmatter-protocol` §6, Form 1) — never `head`/`tail`.
6. Run `just serena-checkpoint` from the workspace root.

**Retro-archival (HARD):** if you discover a standard that was fetched but never archived, archive it immediately on discovery and report the skip to the user.

## 4. What Counts as a Standard

A versioned technical text issued by an authoritative body with a stable URL. Families (the `<family>` path segment): `rfc` (IETF RFC), `std` (IETF STD), `bcp` (IETF BCP), `pep` (Python PEP), `aip` (Google AIP), `owasp` (OWASP cheat sheets, ASVS, API Top 10), `w3c` (W3C REC), `whatwg` (WHATWG living standards), `zmpc` (ZeroMQ RFC).

- **Full body only:** an archive entry is the complete standard text (raw download or `kagi_extract`). `kagi_summarizer` output is a derivative and is NEVER archived. If a summary sufficed for the answer but the document is a standard, fetch the full body for the archive anyway.
- **Not standards:** blogs, tutorials, vendor documentation (e.g. Temporal docs), marketing pages — never archived here.
- New families are owned by THIS skill (families are path segments inside the registered `standard/` scope, not scopes themselves — no registry amendment is needed). Propose a new family to the user before first use and extend the list here on approval.

## 5. Violation Protocol

If you fetch a standard from the web without checking both stores, use a fetched standard without archiving it, archive a summary or a non-standard, or edit the raw body of an archive entry, halt immediately, discard the offending step, perform the correct lookup/archival per §1/§3, and record the violation in `bugs/project/read_for_comments_bypass` or `notes/agent/read_for_comments_bypass`.
