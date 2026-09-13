# Changelog

## 2026-09-13 — Initial creation

- Created `review-standard` on-demand skill: SKILL.md, README.md, CHANGELOG.md,
  and seven reference files under `references/`.
- Corpus: Google eng-practices review standard, 10 pages archived in Serena scope
  `standard/gep/` (family `gep`), scraped and attested 2026-09-13. Verdicts pin
  to this snapshot.
- Registered in the on-demand manifest (`_on_demand/SKILL.md`) with EN+RU triggers.

## 2026-09-13 — SKILL.md enriched to full distillate (v0.2.0)

- New section **The Standard in One Pass**: every rule of the corpus compressed to one actionable line with `[ref: #anchor]` citations — SKILL.md alone is now sufficient to assess a review; references serve to deepen a topic or quote the exact letter.
- Workflow step ROUTE updated: assess from the distillate, load reference sections only for anchors the verdict cites.
- `SKILL.md` version 0.1.0 → 0.2.0.
- Post-audit conformance fixes (same pass): README `rs-` anchors; verbatim gaps restored in comments/process/author_side/coverage/conflicts (summary sections, tag examples, Google-framing sentences, speed.html relaxed-guidelines clause); pandoc fence residue cleaned; `comments-severity` card reworded; cr_respect URL and Sources-terminator exemption recorded in sources.md.
