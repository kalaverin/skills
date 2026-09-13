---
subject: "Provenance and source map for review-standard corpus; ten canonical Google eng-practices pages mapped to reference files with full URLs, archive location in Serena standard gep family, scrape pin dated 2026-09-13, background material limited to Google-owned styleguide and SWE book chapter, Chromium respect doc flagged external non-authoritative."
index:
  - anchor: sources-corpus-map
    what: "Canonical corpus map: all ten archived eng-practices review pages with full URLs, the reference file each one feeds, and where its verified copy lives in Serena memory."
    problem: "Agent must trace every verdict back to an exact source page; without complete map, citations drift and coverage gaps hide; page inventory, file mapping, verdict grounding, gap detection, verbatim source, upstream page."
    use_when: "Resolving which page backs a verdict; checking corpus completeness; locating the archived original of any section."
    avoid_when: "Applying rules to a case (other reference files); refreshing the archive (read-for-comments runbook)."
    expected: "Every reference section resolves to exactly one mapped page and one archive card."
  - anchor: sources-provenance-pin
    what: "Provenance pin: corpus scraped and attested 2026-09-13, archived under the Serena standard/gep family with stamped headers carrying source URL, family, and retrieval dates; verdicts must name this pin."
    problem: "Agent and reader need to know which corpus snapshot each verdict relied on; undated verdicts silently rot when upstream pages change; scrape date, snapshot identity, header stamp, freshness bound, verdict pin, upstream drift, re-verification trigger."
    use_when: "Writing the Standard pin line of a verdict; deciding whether the corpus needs re-verification; auditing old verdicts."
    avoid_when: "Content-level questions about the rules themselves (other reference files)."
    expected: "Every verdict names the 2026-09-13 pin; staleness checks compare against it."
  - anchor: sources-background
    what: "Background material: Google styleguide and the SWE book chapter 3 on team culture are Google-owned companions; the Chromium respect doc is external, referenced by Google, and not authoritative for this skill."
    problem: "Agent may need adjacent context beyond review pages; unclear authority levels let external docs override canonical corpus; companion documents, hierarchy of authority, external reference, Google provenance, styleguide link, knowledge sharing chapter, non-authoritative flag."
    use_when: "A case touches style or culture beyond the ten review pages; deciding whether an outside document may inform a verdict."
    avoid_when: "Core review-rule questions fully covered by the canonical corpus."
    expected: "Verdicts cite background only as context, never as overriding authority."
---

# Sources and Provenance

Full source map of the `review-standard` corpus. Every verdict this skill produces must trace back to a page listed here.

## Canonical Corpus Map

[ref: #sources-corpus-map]

All ten canonical pages live under `https://google.github.io/eng-practices/review/`. Archived attested copies live in Serena memory scope `standard/gep/` (family `gep`).

| Page | Full URL | Reference file | Archive card |
|---|---|---|---|
| The Standard of Code Review | https://google.github.io/eng-practices/review/reviewer/standard.html | `principles.md` | `standard/gep/gep_reviewer_standard` |
| What to Look For | https://google.github.io/eng-practices/review/reviewer/looking-for.html | `coverage.md` | `standard/gep/gep_reviewer_looking_for` |
| Navigating a CL | https://google.github.io/eng-practices/review/reviewer/navigate.html | `process.md` | `standard/gep/gep_reviewer_navigate` |
| Speed of Reviews | https://google.github.io/eng-practices/review/reviewer/speed.html | `process.md` | `standard/gep/gep_reviewer_speed` |
| How to Write Comments | https://google.github.io/eng-practices/review/reviewer/comments.html | `comments.md` | `standard/gep/gep_reviewer_comments` |
| Handling Pushback | https://google.github.io/eng-practices/review/reviewer/pushback.html | `conflicts.md` | `standard/gep/gep_reviewer_pushback` |
| Emergencies | https://google.github.io/eng-practices/review/emergencies.html | `conflicts.md` | `standard/gep/gep_emergencies` |
| Writing CL Descriptions | https://google.github.io/eng-practices/review/developer/cl-descriptions.html | `author_side.md` | `standard/gep/gep_developer_cl_descriptions` |
| Small CLs | https://google.github.io/eng-practices/review/developer/small-cls.html | `author_side.md` | `standard/gep/gep_developer_small_cls` |
| Handling Reviewer Comments | https://google.github.io/eng-practices/review/developer/handling-comments.html | `author_side.md` | `standard/gep/gep_developer_handling_comments` |

Coverage rule: every section in every reference file of this skill resolves to exactly one row of this table, and each section ends with a `Sources:` line carrying the full URL.

## Provenance Pin

[ref: #sources-provenance-pin]

- **Scraped and attested:** 2026-09-13 (all ten pages, single pass).
- **Archive location:** `.serena/memories/standard/gep/` — each card carries a stamped header (title, created_at, updated_at, repo: generic, branch: main, commit, committed_at, source URL, family: gep).
- **Family registry:** the `gep` family is registered in `read-for-comments` with fetch base `https://google.github.io/eng-practices/<path>`; the Lookup Gate checks this archive before any web fetch.
- **Verdict pin:** every assessment this skill produces names this pin ("Standard pin: gep @ 2026-09-13") so readers know which snapshot was applied.
- **Self-description:** this file is its own source map; the per-section `Sources:` terminator rule applies to the gep-content sections of the other six reference files.
- **Re-verification:** if the upstream site may have changed materially, re-run the `read-for-comments` archival pipeline for the `gep` family, then bump the pin in this file, in `SKILL.md`, and in `CHANGELOG.md`.

## Background Material

[ref: #sources-background]

Google-owned companions (safe to cite as context):

- Google styleguides: https://google.github.io/styleguide/
- *Software Engineering at Google*, chapter 3 (Knowledge Sharing): https://abseil.io/resources/swe-book/html/ch03.html

External, referenced by Google, **not authoritative** for this skill:

- Chromium `cr_respect.md` (respectful reviews guidance): https://chromium.googlesource.com/chromium/src/+/master/docs/cr_respect.md — may be mentioned as related practice, never as a source of verdicts.

Authority rule: when background material and the canonical corpus disagree, the corpus wins; external documents inform context only and must be flagged as non-authoritative in any verdict that mentions them.
