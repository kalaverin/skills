# Addendum: api-design presentation choices for the Cross-Skill Reference Standard

This addendum documents the api-design-specific presentation decisions for the `references/` corpus. It **defers to** `bootstrap/references/REFERENCE_STANDARD.md` for everything covered there (frontmatter schema, card semantics, anchor mechanics, body skeleton, loader contract, conformance checking) and MUST NOT contradict it. What follows is only what the standard leaves to the owning skill, plus accepted waivers.

## 1. Corpus layout

- Flat `references/` directory, **no tiers**. 11 files: `01_foundation_and_process.md` … `10_protocol_buffers.md` plus `rfc_verbs.md`.
- One topic chapter per file; the `NN_` numeric prefix mirrors the chapter order of the source AIP guide and is stable.
- Title style: exactly one `# Title Case` H1 per file, immediately after the frontmatter.
- List style: term–description list items use the single-line inline colon form (`` - `term`: description ``) everywhere in the corpus. The two-line indented description-list forms inherited verbatim from aip.dev were normalized to this form on 2026-07-22 (formatting-only deviation from AIP-verbatim; wording preserved). New content MUST follow the inline colon form.
- Verbatim deviations: spelling/grammar corrections applied to the AIP source text on 2026-07-22 — `identifer`→`identifier` (AIP-162), `indepedent`→`independent`, stray space in a fenced URI, `heterogenous`→`heterogeneous`, `resolution on at time`→`resolution at time`, `specific or order semantic structure`→`specific order or semantic structure`, `unreachable resource missing`→`unreachable resources missing` (all AIP-217). These are the only sanctioned departures from the verbatim-freeze rule; everything else stays byte-identical to the source.

## 2. Content type: normative rules, not recipes

The corpus adapts Google AIP rule sections, so card field semantics are the normative-rule variant of the standard schema:

- `problem` — the **design risk or cost the AIP prevents** (inconsistency, breaking change, client friction), written as agent situation + stake per §4.4.
- `what` — the AIP's rule mechanism, framed as applied to that risk; the AIP number names the mechanism (`The AIP-NNN …`).
- `use_when` — design/review situations that mandate the section.
- `avoid_when` — where the section is inapplicable, routing to the better alternative via the cross-reference convention (§4 below).
- `expected` — the **compliant end state**: what holds when the design follows the section.
- Pure lookup sections (Glossary `glossary-aip-9`, `rfc-verbs`) leave `avoid_when`/`expected` empty per the standard's lookup convention.

## 3. Anchor marker placement (accepted waiver)

The standard's §6.1 separate-line form shows a blank line above and below the marker. This corpus uses the **tight placement form**: the marker sits at column 0 on its own line directly under the section heading — **no blank line above**, one blank line below. It is applied uniformly to all 73 markers and was accepted as this skill's one placement form (§6.1: "A skill MUST choose one placement form and apply it uniformly"). New sections MUST follow the tight form. Extraction tooling MUST NOT depend on a blank line above the marker.

## 4. Cross-reference convention inside card fields

- `(sibling card)` — another card for the **same anchor** in the same file (convergence pair/triple).
- `(<NN>_<name> › <topic>)` — a section in another (or the same) corpus file, e.g. `(07_design_patterns › soft delete)`, `(05_operations › standard methods)`.
- AIP numbers (`AIP-164`) remain the canonical citation in prose; the `(<file> › <topic>)` form is the actionable routing pointer.
- Skill-external routing names the skill instead (`protobuf-lang skill`, `read-for-comments skill`).

## 5. `subject` composition

- Form per §4.2: `<chapter essence>; <cloud of every section area>`, 30–50 words, no articles.
- Nine files embed `AIP-NNN` hooks in the cloud. **Waiver:** `07_design_patterns.md` (at the 50-word ceiling) and `10_protocol_buffers.md` carry semantic hooks only; their AIP numbers live exclusively in the `aips` field (decision P4-Q1). Coarse routing for an AIP-number-citing request uses `aips`, not `subject`.

## 6. `aips` skill-extra metadata

- Declared in `SKILL.md` §2.4 per the standard's §2 skill-extra mechanism.
- Sorted flat list of integers, one per AIP covered by the file's body sections; **required** in every file (empty list allowed, e.g. `rfc_verbs.md`).
- Mechanically cross-checked against the AIP numbers in body section headings by `scripts/validate_reference_frontmatter.py`; fenced code blocks are skipped during the check.

## 7. Validation

`scripts/validate_reference_frontmatter.py` enforces the standard's §9 checklist plus this corpus's extras: the `aips` cross-check (§6 above), deep cross-field dedup with the §4.5 identifier exemption (backticked identifiers and `›` cross-reference pointers are exempt; prose phrases are not), cloud sub-gram leaks, and the cloud-vs-situation paraphrase heuristic. Run it per file:

```bash
uv run --no-project --with pyyaml python scripts/validate_reference_frontmatter.py references/<FILE>.md
```

Every reference file MUST pass before a change is called done.
