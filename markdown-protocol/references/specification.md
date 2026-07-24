---
subject: "Markdown headings as public API; slugs, anchors, `mds-` prefix, unique chains, rename ban, plain-text headings, writer limit 8192 queue limit 16536, deprecation, fence-aware parsing, frontmatter stripping, errata queue, cross-file citation, `markdown-protocol`, ATX grammar, conformance classes, wild corpora."
index:
  - anchor: mds-abstract
    what: "The document's abstract: what the headings-as-API contract is and whom it binds."
    problem: "Reader opens this standard and needs one-paragraph contract before any rule; missing frame, context absence, contract fog, entry confusion, purpose vacuum, orientation absence, first-contact doubt, framing gap, reach doubt, reader fog."
    use_when: "First read of the standard; presenting it to a user; deciding whether it governs a document."
    avoid_when: "Any concrete rule lookup — later sections carry the normative text."
    expected: "Reader knows the contract, its three parties, and the standard's reach."
  - anchor: mds-scope-and-conformance-classes
    what: "The scope statement: any agent-authored Markdown, split into writer and tooling conformance classes."
    problem: "Agent writes plans, reports, memories and must know which rules bind which role; role confusion, scope questions, class mismatch, applicability fog, boundary questions, duty uncertainty, coverage questions, assignment fog, realm fog."
    use_when: "Deciding whether a document falls under the standard; distinguishing writer duties from tooling duties."
    avoid_when: "Specific rule text — the dedicated sections own each rule."
    expected: "Applicability and role assignment settled for any document."
  - anchor: mds-terminology
    what: "The glossary: chain, slug, anchor, section, own body, preamble, flat document, wild corpus."
    problem: "Terms like chain and own body carry precise technical meaning here; misreading them inverts rules downstream; term confusion, meaning inversion, vocabulary gap, misread specs, definition absence, lexicon gap, term drift, jargon fog."
    use_when: "Any term in the standard reads ambiguous; teaching the vocabulary to another agent."
    avoid_when: "Normative rules — later sections own them."
    expected: "Shared precise vocabulary for all later sections."
  - anchor: mds-conformance-model
    what: "The repair-not-rejection model: tooling indexes everything and marks violations for agent remediation."
    problem: "Agent wonders whether some dirty file gets refused or fixed during indexing; refusal fear, rejection anxiety, model doubt, availability question, enforcement fog, quarantine fear, purity myth, gate confusion, repair path, correction model."
    use_when: "Deciding how violations are treated; explaining why errata never blocks indexing."
    avoid_when: "The errata field mechanics — the errata mechanism section owns them."
    expected: "Availability over purity understood as the enforcement stance."
  - anchor: mds-slug-specification
    what: "The seven-step slug computation and the writer/tooling alphabet split."
    problem: "Agent renames heading cosmetically and worries about re-keying, or computes identity inconsistently; identity drift, inconsistent normalization, cosmetic paranoia, slug confusion, stability doubt, edit anxiety, computation chaos, key stability, edit safety, norm stability."
    use_when: "Computing a heading's slug; judging whether an edit is cosmetic; handling non-Latin headings."
    avoid_when: "Anchor id rules — the anchor specification owns those."
    expected: "Deterministic slug per heading; cosmetic edits provably free."
  - anchor: mds-anchor-specification
    what: "The anchor form, id format, coverage requirements, stability, tombstone, and injection duties."
    problem: "Agent must attach identifiers that outlive reorganizations; wrong form, wrong coverage, or reused ids silently kill citations; identifier fragility, citation death, form drift, id reuse, stability doubt, link fragility, marker absence, id chaos."
    use_when: "Adding anchors to new sections; choosing ids; handling deprecated sections; tooling injecting missing anchors."
    avoid_when: "Chunk-key computation — that is service machinery, not this contract."
    expected: "Every H1/H2 anchored with eternal, unique, position-free ids."
  - anchor: mds-structural-rules
    what: "The structural rule group heading: H1, grammar, levels, depth, preamble rules."
    problem: "Agent needs map of structural constraints before any single one; group fog, structure overview absence, section orientation, navigation doubt, family confusion, rule scatter, lookup friction, guidance vacuum, rule index, group clarity."
    use_when: "Scanning which structural rule applies; onboarding to the document's skeleton rules."
    avoid_when: "Any single rule's full text — its own subsection anchor carries it."
    expected: "Structural rule family located quickly."
  - anchor: mds-single-h1-matching-title
    what: "The one-H1 rule with exact title matching."
    problem: "Documents sprout multiple H1s or H1-title drift; file loses its single identity root; forked identity, title mismatch, multi-root chaos, address ambiguity, entity fracture, naming disorder, anchor confusion, root fork, citation doubt, entity doubt."
    use_when: "Authoring or reviewing any frontmatter-carrying document; checking title-H1 pairing."
    avoid_when: "Multi-root processing — degradation detail, not the writer rule."
    expected: "One H1 per document, byte-identical to its title."
  - anchor: mds-atx-headings-only
    what: "The ATX-only heading grammar and the setext ban."
    problem: "Setext underline reads byte-identically to some frontmatter delimiter; parsers trap on it and structure falsifies; delimiter collision, structure corruption, grammar ambiguity, setext hazard, parsing confusion, envelope breach, underline menace, detection failure, grammar drift."
    use_when: "Writing headings; migrating setext documents; understanding the delimiter trap."
    avoid_when: "Delimiter law itself — frontmatter-protocol owns that."
    expected: "All headings ATX; no delimiter ambiguity anywhere."
  - anchor: mds-no-skipped-levels
    what: "The no-skipped-levels tree rule."
    problem: "Heading jumps H1 straight to H3 and tree becomes ambiguous for chunking and citation; hierarchy ambiguity, orphan sections, level jumps, structure fog, parentage doubt, chain confusion, hierarchy gaps, attach doubt, level disorder, tree disorder."
    use_when: "Structuring any document; reviewing heading trees; migrating wild corpora."
    avoid_when: "Re-parenting mechanics — tooling degradation, not writer duty."
    expected: "Continuous heading levels throughout every document."
  - anchor: mds-depth-unlimited
    what: "The unlimited-depth allowance with opt-in deep anchors."
    problem: "Agent avoids deep decomposition fearing some phantom cap, or anchors every H4 in noise; cap myth, depth doubt, over-marking, anchor clutter, level confusion, coverage anxiety, hierarchy hesitation, marker spam, depth paralysis, scale myth."
    use_when: "Decomposing complex topics deeply; deciding anchor coverage below H2."
    avoid_when: "Anchor requirements themselves — the anchor specification owns them."
    expected: "Depth chosen freely; anchors only where citation needs them."
  - anchor: mds-preamble-discipline
    what: "The preamble ban with the meta-remark allowance and the flat-document carve-out."
    problem: "Intro text before first H2 belongs to no section and cannot be chunked or cited; unaddressable content, preamble sprawl, orphan text, hybrid confusion, flat-file doubt, homeless prose, index limbo, rootless content, address vacuum, address-free words."
    use_when: "Writing sectioned documents; keeping or removing intro text; authoring flat findings."
    avoid_when: "Meta-remarks about the document itself — those stay legal."
    expected: "Zero semantic preamble; flat files legitimately whole."
  - anchor: mds-addressing-discipline
    what: "The addressing rule group heading: chains, cosmetics, renames, anchor coverage, heading text."
    problem: "Agent needs map of identity rules before any single one; group fog, identity overview absence, section orientation, navigation doubt, family confusion, rule scatter, lookup friction, guidance vacuum, rule index, group clarity."
    use_when: "Scanning which addressing rule applies; onboarding to identity discipline."
    avoid_when: "Any single rule's full text — its own subsection anchor carries it."
    expected: "Addressing rule family located quickly."
  - anchor: mds-unique-heading-chain
    what: "The per-document chain uniqueness rule."
    problem: "Two sections share one chain and every key derived from it collides; key collision, chain duplication, addressing failure, content overwrite, identity clash, merge accident, retrieval corruption, uniqueness breach, map fracture, key chaos."
    use_when: "Naming sections; reviewing duplicate headings; tooling flagging dup_chain."
    avoid_when: "Cross-document uniqueness — the cross-file citation section owns that."
    expected: "Every chain unique within its document."
  - anchor: mds-cosmetic-differences-unregulated
    what: "The explicit non-regulation of case, punctuation, and emphasis differences."
    problem: "Agent polices cosmetic variants needlessly, inventing rules this standard deliberately omits; over-policing, fabricated rules, cosmetic anxiety, rule invention, scope creep, style enforcement, false violations, wasted vigilance, purity theater, style persecution."
    use_when: "Judging whether a cosmetic difference violates anything; reviewing heading style."
    avoid_when: "Slug computation itself — the slug specification owns it."
    expected: "No cosmetic rule invented; collisions caught post-slugging only."
  - anchor: mds-heading-renames-forbidden
    what: "The rename ban with cosmetic, typo, and repository-waiver exemptions."
    problem: "Agent must alter some heading but every rename re-keys chunks and rots citations; re-key cascades, rename temptation, identity break, waiver doubt, link decay, anchor grief, history fracture, reference loss, permanence loss."
    use_when: "Considering any heading or title edit; applying typo fixes; checking repo waivers before retitling."
    avoid_when: "Deprecating content — the deprecation rule owns that path."
    expected: "No renames; exemptions applied exactly as enumerated."
  - anchor: mds-anchors-on-h1-h2
    what: "The H1/H2 anchor requirement restated as a writer duty."
    problem: "New sections ship without anchors and future citations have nothing to hold; anchor absence, citation void, coverage gap, requirement fog, ship-and-forget ids, reference vacuum, linking impossibility, identity void, citability loss, hold absence."
    use_when: "Creating any H1 or H2 section; auditing anchor coverage."
    avoid_when: "Deep H3+ anchors — optional per the anchor specification."
    expected: "Complete anchor coverage at H1 and H2."
  - anchor: mds-plain-text-headings
    what: "The plain-text heading rule with the backticked code exception and the symbol ban."
    problem: "Markup in headings diverges display from identity and symbol-only heads slug to nothing; markup poison, collision bait, formatting drift, display mismatch, symbol loss, style pollution, vanishing anchors, name decay, text noise, format decay."
    use_when: "Writing heading text; wrapping code identifiers; catching pure-symbol headings."
    avoid_when: "Visual styling debates — headings need no emphasis, they are emphasis."
    expected: "Headings plain, identifiers backticked, no empty slugs."
  - anchor: mds-section-size-and-shape
    what: "The size rule group heading: thought granularity and byte caps."
    problem: "Agent needs map of sizing rules before either single one; group fog, sizing overview absence, section orientation, navigation doubt, family confusion, rule scatter, lookup friction, guidance vacuum, rule index, group clarity."
    use_when: "Scanning which sizing rule applies; onboarding to section shaping."
    avoid_when: "Any single rule's full text — its own subsection anchor carries it."
    expected: "Sizing rule family located quickly."
  - anchor: mds-one-section-one-thought
    what: "The one-thought-per-section principle with the no-merging guarantee."
    problem: "Sections merge small thoughts into unreadable blocks while writers fear atomic sections; thought mixing, merge pressure, granularity doubt, block bloat, atomicity anxiety, cohesion loss, reader fatigue, scale confusion, glue temptation."
    use_when: "Sizing sections; deciding against merging small sections."
    avoid_when: "Byte caps — the next rule owns those."
    expected: "Atomic thoughts per section, zero forced merges."
  - anchor: mds-size-limits
    what: "The 8192-byte writer limit and the 16536-byte queue limit with the no-mechanical-split rule."
    problem: "Sections grow past embedding windows and chunking breaks, or machines butcher prose mid-sentence to comply; window overflow, butchered text, cap breach, split confusion, measure fog, token explosion, boundary ignorance, compliance mangling, boundary drift."
    use_when: "Sizing or splitting long sections; interpreting over_cap flags."
    avoid_when: "Mechanical splitting — forbidden absolutely; rewrite manually instead."
    expected: "Sections within caps; over-cap flagged, never auto-cut."
  - anchor: mds-lifecycle-and-tooling-rules
    what: "The lifecycle rule group heading: deprecation, fence-awareness, frontmatter stripping."
    problem: "Agent needs map of lifecycle and parsing rules before any single one; group fog, lifecycle overview absence, section orientation, navigation doubt, family confusion, rule scatter, lookup friction, guidance vacuum, rule index."
    use_when: "Scanning which lifecycle or tooling rule applies; onboarding to document lifecycle."
    avoid_when: "Any single rule's full text — its own subsection anchor carries it."
    expected: "Lifecycle rule family located quickly."
  - anchor: mds-deprecation-instead-of-deletion
    what: "The deprecation ceremony: format, tombstones, service-side purge asymmetry."
    problem: "Obsolete content tempts deletion and every inbound citation orphans instantly; citation death, reference loss, lifecycle fog, tombstone absence, history erasure, link rot, resurrection impossibility, cemetery need, grace absence, pointer decay."
    use_when: "Retiring sections or anchors; writing deprecation lines; understanding purge asymmetry."
    avoid_when: "Renaming — that path is forbidden separately."
    expected: "Deprecations recorded; nothing writer-deleted ever."
  - anchor: mds-fence-aware-parsing
    what: "The fence-awareness mandate for any parser."
    problem: "Naïve parsers read fenced lookalikes as headings and mint phantom keys that overwrite real sections; phantom structure, fake keys, content overwrite, parser naivety, fence blindness, structure poisoning, identity theft, lookalike traps."
    use_when: "Building or using any parser over these documents; auditing heading extraction."
    avoid_when: "Content rules — parsing mechanics only here."
    expected: "Zero phantom headings from fenced content."
  - anchor: mds-frontmatter-stripping
    what: "The frontmatter-strip mandate: never chunked, never hashed."
    problem: "Closing delimiter parses as setext heading and header churn invalidates every chunk on every edit; delimiter trap, hash invalidation, metadata pollution, arm risk, identity decay, verification noise, boundary confusion, key erosion, header decay."
    use_when: "Parsing documents for structure; deciding what enters chunks and hashes."
    avoid_when: "Tracking field semantics — frontmatter-protocol owns those."
    expected: "Frontmatter excluded from all structure and identity."
  - anchor: mds-the-errata-mechanism
    what: "The errata field: semantics, computation, writer recording duty, clearing, forward compatibility, reason enum."
    problem: "Agent must know how deviations get queued, recorded honestly, and never silently dropped during maintenance; queue fog, recording doubt, silent-drop risk, enum absence, repair blindness, mechanism blindness, honesty gap, process fog."
    use_when: "Recording deviations; shrinking on fixes; enumerating dirty pages via grep; extending reasons."
    avoid_when: "Rejecting documents — the conformance model forbids rejection."
    expected: "Every deviation queued, honestly maintained, greppable."
  - anchor: mds-cross-file-citation
    what: "The global-uniqueness recommendation with owner naming and domain prefixes."
    problem: "Bare anchor citations collide across files and skills in one shared domain; citation collision, cross-file ambiguity, prefix absence, ownership fog, domain clash, reference confusion, id overlap, resolution failure, namespace war, link rot."
    use_when: "Citing anchors across files or skills; minting new anchor prefixes."
    avoid_when: "Within-document anchors — the anchor specification covers those."
    expected: "Unambiguous citations anywhere in the domain."
  - anchor: mds-relationship-to-other-standards
    what: "The boundary map to markdown-protocol core rules, tracking, and lazyload."
    problem: "Agent cannot tell which standard owns markers, tracking fields, or errata registration; ownership fog, boundary doubt, standard collision, overlap confusion, jurisdiction questions, authority drift, map absence, governance fog, realm confusion, boundary maze."
    use_when: "Resolving which standard governs a question; onboarding to the standards family."
    avoid_when: "Rule text of those standards — they own their sections."
    expected: "Clear ownership per concern, zero contradictions."
  - anchor: mds-out-of-scope
    what: "The explicit exclusions: adoption planning, service schemas, cemetery implementation, retrieval expansion."
    problem: "Agent expects answers this standard deliberately withholds from its text; expectation drift, missing-feature confusion, boundary fog, demand mismatch, adoption questions, machinery curiosity, scope guessing, deferred topics, hunting elsewhere, scope creep."
    use_when: "Checking whether a topic belongs here; deferring service-specific machinery."
    avoid_when: "Anything normative — sections above carry all of it."
    expected: "No misread boundaries; exclusions named exactly."
---

# Standard: Markdown Headings as a Public API

## 1. Abstract

[ref: #mds-abstract]

This document specifies the headings of a Markdown document as a public API: a stable, machine-addressable contract between writers (agents), maintainers (memory/index services), and readers (agents citing content across sessions). Every heading is an addressable entity with a computed identity; every section is a retrievable unit; documents can be indexed, cited, compacted, and reconciled by machines without human intervention. Rationale and evidence for every section: `references/rationale.md`.

> **Identity:** `markdown-headings-public-api` v0.1.0 (Standards Track). Supersedes: the frozen draft at `docs/standards/markdown-headings-public-api.md` (historical original — never edited, never stamped). Canonical home: `markdown-protocol` skill.

## 2. Scope and Conformance Classes

[ref: #mds-scope-and-conformance-classes]

This standard applies to ANY agent-authored Markdown intended for machine memory, indexing, or citation — memory files, reference corpora, plans, reports, standards. It has two conformance classes:

- **Writers** — agents authoring or editing documents. Sections 4–9 constrain what a writer may produce. The governing principle for writers is immutability of identity: a writer never renames headings, never modifies anchors, never changes the document title (waivers: §8.3 exemptions and repository-recorded exceptions).
- **Tooling** — indexers, compactors, reconcilers (present and future). Sections 10–11 define how tooling parses and marks documents, including mandatory degradation behavior for non-conformant ("wild") corpora.

Rationale: `[ref: #mds-rationale-scope]` in `references/rationale.md`.

## 3. Terminology

[ref: #mds-terminology]

- **Heading chain (chain):** the sequence of headings from the document root (H1) down to a given heading, inclusive.
- **Slug:** the normalized form of a heading text produced by §5.
- **Anchor:** a `[ref: #<id>]` marker line attached to a heading (§6).
- **Section:** a heading plus its body up to the next heading of the same or shallower level (its subtree).
- **Own body:** the bytes between a heading line and its first child heading (or the end of its subtree when childless).
- **Preamble:** content between the H1 line and the first H2 heading.
- **Flat document:** a document with an H1 and no H2+ headings.
- **Wild corpus:** any document set not authored under this standard (legacy, third-party, or pre-standard files).

Normative keywords (MUST, MUST NOT, SHOULD, MAY) follow RFC 2119 / RFC 8174 (local copies: `read-for-comments` skill).

## 4. Conformance Model

[ref: #mds-conformance-model]

Conformance is enforced through the errata mechanism (§11), not through rejection: tooling MUST index and serve every document it can parse, and MUST mark non-conformant documents for remediation. A violation of a writer-side MUST produces an `errata` entry; it never blocks indexing. Memory must remain available even when dirty; repair is a queued, greppable, agent-executable activity.

Rationale: `[ref: #mds-rationale-conformance-model]` in `references/rationale.md`.

## 5. Slug Specification

[ref: #mds-slug-specification]

A heading's **slug** is computed by applying these steps to the raw heading text, in exactly this order:

1. Unicode NFC normalization.
2. Lowercasing (Unicode-aware).
3. Strip all Unicode punctuation (category P*) **and symbols (category S*)**, including dashes and backticks present in the source text.
4. Convert every whitespace run to a single dash (`-`).
5. Collapse consecutive dashes into one.
6. Strip leading and trailing dashes.
7. Strip leading digits until the first letter: digits and dashes at the very start are removed; from the first letter onward digits are free anywhere.

Examples: `3.5 Parser` → `parser`; `2024 Report` → `report`; `RFC 2119` → `rfc-2119`; `2fa` → `fa`.

Leading digits in headings are POSITIONAL information (`3.5 Parser`), and position is never identity in this design. Consequence by design: sections differing only in leading numbers collide as `dup_chain` — writers MUST give sections meaningful names, not numbers.

**Cautionary example:** `7.3. No skipped levels` slugs to `no-skipped-levels` — the number is display only. But two differently numbered sections carrying the same words (`3.5 Parser` in one document and `5.2 Parser` in another, or twice in one document) collide identically. Name sections by meaning (`Parser`, `Skipped Levels`), never by position.

Canonical reference implementation:

```bash
python3 -c "import re,unicodedata; t=unicodedata.normalize('NFC','3.5 Parser Rules').lower(); t=''.join(c for c in t if not unicodedata.category(c).startswith(('P','S'))); t=re.sub(r'\s+','-',t); t=re.sub(r'-+','-',t).strip('-').lstrip('0123456789-'); print(t)"
```

The slug alphabet is all Unicode letters and digits. **Writers** MUST restrict heading text to Latin letters, digits, and whitespace-separated words (plus the backticked code exception in §8.5). **Tooling** MUST handle the full Unicode slug alphabet: non-Latin headings occur in the wild and remain indexable; they are flagged (`nonlatin_heading`) but never rejected.

Uniqueness of chains (§8.1) is evaluated **post-slugging**: two headings that differ only in case, punctuation, or emphasis markup are the same heading for addressing purposes. A heading consisting solely of symbols slugs to the empty string and is forbidden for writers (§8.5); tooling rephrases such headings into words during maintenance (always logged), with a synthetic `h` + first 12 hex chars of `xxh64(raw_heading_text)` as the last-resort fallback.

Rationale: `[ref: #mds-rationale-slug-specification]` in `references/rationale.md`.

## 6. Anchor Specification

[ref: #mds-anchor-specification]

An **anchor** attaches a stable, human-readable identifier to a heading:

```markdown
## Section Heading
[ref: #mds-section-heading]

Section body starts here.
```

1. **Form:** the literal line `[ref: #<id>]` at column 0, on its own line, directly under the heading line, with one blank line below the marker (tight placement, per `markdown-protocol` marker_style).
2. **Id format:** kebab-case, slug alphabet (§5); unique within the document. The id SHOULD be the slugged heading text; custom ids are permitted where the slug is ambiguous or misleading. Anchor ids never embed positional numbering, even when headings are numbered for human citation.
3. **Required coverage:** H1 and H2 headings MUST carry anchors. H3–H6 headings MAY carry anchors; an anchor is RECOMMENDED on any deep section intended for citation, and discouraged below H3 (an H4 anchor is a smell, not a crime).
4. **Stability:** once published, an anchor id is stable **forever**. Writers MUST NOT modify, rename, or move an anchor.
5. **Tombstone rule:** an anchor id MUST NOT be reused for a different section, even after its original section is deprecated. Deprecated anchors stay as tombstones (§10.1).
6. **Injection duty (shared):** writers add anchors when creating new H1/H2 sections; tooling injects missing H1/H2 anchors and repairs duplicates during maintenance (a silent mechanical fix — not an errata case, §11).

Rationale: `[ref: #mds-rationale-anchor-specification]` in `references/rationale.md`.

## 7. Structural Rules

[ref: #mds-structural-rules]

### 7.1. Single H1 matching the title (MUST)

[ref: #mds-single-h1-matching-title]

A document MUST contain exactly one H1, placed immediately after the frontmatter block, whose text matches the frontmatter `title` field exactly (where frontmatter is present). A writer MUST give every sectioned document a frontmatter block carrying a `title` field that matches the H1 exactly — conformance MUST be achievable by following writer rules alone. Tooling degrades (each H1 roots an independent tree) but flags `errata: multi_h1`.

### 7.2. ATX headings only (MUST)

[ref: #mds-atx-headings-only]

Headings MUST use the ATX form (`#` through `######`). Setext headings (underline-style `===`/`---`) are forbidden: a setext H2 underline is byte-identical to a frontmatter closing delimiter. Tooling treats setext as paragraph text and flags `errata: setext`.

### 7.3. No skipped levels (MUST)

[ref: #mds-no-skipped-levels]

Heading levels MUST NOT skip (an H1 MUST NOT be followed directly by an H3). Tooling re-attaches skipped headings to the nearest preceding shallower heading and flags `errata: skipped_level`.

### 7.4. Depth is unlimited (INFO)

[ref: #mds-depth-unlimited]

Heading depth is NOT restricted. H5/H6 are legitimate and serve fine-grained absolute addressing. Anchors are required only at H1/H2 (§6); deeper levels are opt-in for citation.

### 7.5. Preamble discipline (MUST)

[ref: #mds-preamble-discipline]

In any document that contains H2+ sections, no semantic content is allowed before the first H2. Preamble is permitted ONLY for meta-remarks about the document itself (status notes such as `> **ABANDONED**`, activation notes, or human-oriented comments). A flat document (H1 + body, no H2) is legitimate and carries its whole meaning in that body. Tooling indexes offending preambles under the H1 chunk and flags `errata: preamble_semantic`.

## 8. Addressing Discipline

[ref: #mds-addressing-discipline]

### 8.1. Unique heading chain per document (MUST)

[ref: #mds-unique-heading-chain]

The slugged heading chain (all parent slugs plus the own slug, per §5) MUST be unique within a document. This is the foundation of absolute addressing: the chain is the chunk-key input, so a duplicated chain is a key collision. Tooling: last write wins in the backends, the file is flagged `errata: dup_chain` and queued for rewriting; no occurrence-suffix machinery exists.

### 8.2. Cosmetic differences are not regulated (INFO)

[ref: #mds-cosmetic-differences-unregulated]

Beyond slug normalization (§5), no rule restricts case, punctuation, or emphasis differences between headings. Collisions that survive slugging are caught by §8.1 post-slugging.

### 8.3. Heading renames are forbidden for writers (MUST NOT)

[ref: #mds-heading-renames-forbidden]

A writer MUST NOT rename a heading. A rename changes the slug and therefore breaks every chunk key derived from the chain and every slug-based citation. New thought = new heading; an obsolete heading is deprecated (§10.1), never renamed. The document **title** is equally immutable: title = H1 = the file's identity root (§7.1 makes them one entity).

Exemptions:

- **Cosmetic edits** erased by slug normalization (case, punctuation, emphasis) remain free.
- **Typo fixes** with a Damerau–Levenshtein distance of **at most 2 AND at most 20% of the string length** are permitted; they re-key, and that is accepted.
- **Repository waivers:** a repository MAY record local exceptions in its agent memory (e.g. evolving plan/decision documents that may be retitled). Writers MUST check their project's recorded waivers before assuming the ban applies in full force. When in doubt, the writer asks the user.

A rename that happens anyway is an authoring bug, not a system failure: tooling survives it via keyset diff and rekey activities, at the price of a reindex.

### 8.4. Anchors on H1/H2 (MUST)

[ref: #mds-anchors-on-h1-h2]

Every H1 and H2 heading MUST carry an anchor per §6. The anchor is the primary citation key; the heading text is the display layer.

### 8.5. Plain-text headings (MUST)

[ref: #mds-plain-text-headings]

Heading text MUST be plain text: no bold, italic, links, or other inline markup. One forced exception: verbatim code identifiers (function, class, method, field, file, environment-variable, CLI command and flag names) MUST be wrapped in backticks when they appear in a heading. Pure-symbol headings are forbidden (they slug to empty, §5). Tooling flags `errata: heading_markup` / `errata: empty_slug`.

## 9. Section Size and Shape

[ref: #mds-section-size-and-shape]

### 9.1. One section = one thought (SHOULD)

[ref: #mds-one-section-one-thought]

Each section SHOULD carry exactly one thought. There is no numeric minimum size and no merging requirement: micro-sections are legitimate. Wider context at read time is a retrieval-time expansion feature; the index stays atomic and stable.

### 9.2. Size limits (MUST)

[ref: #mds-size-limits]

A section whose **own body** exceeds **8192 bytes (2^13, the writer limit)** MUST be split into subsections by its writer. No subtree (at any level) may exceed **16536 bytes (the queue limit)**: larger content is a conformance violation (`errata: over_cap`) but is indexed whole — tooling never splits content mechanically (no `.partN` chunks, ever). All sizes are measured in UTF-8 bytes EXCLUDING whitespace characters; anchor marker lines are excluded from the count. The terms "soft limit" and "hard limit" are forbidden here: limits trigger repair, never rejection (see Conformance Model). Purge grace for long-deprecated sections is a service-side parameter, not a writer concern.

Rationale for both: `[ref: #mds-rationale-section-size-and-shape]` in `references/rationale.md`.

## 10. Lifecycle and Tooling Rules

[ref: #mds-lifecycle-and-tooling-rules]

### 10.1. Deprecation instead of deletion (MUST)

[ref: #mds-deprecation-instead-of-deletion]

Sections and anchors are deprecated, never deleted and never renamed (by writers). Deprecation format — the first body line under the heading reads, in this exact order (heading → anchor marker → one blank line → DEPRECATED line):

```markdown
> **DEPRECATED <YYYY-MM-DDTHH:MM:SSZ>:** <reason>. See [ref: #<replacement-anchor>] (or: no replacement).
```

The date is full UTC ISO 8601 with a `Z` suffix, aligned with this skill's STRICTEST date rule.

The tombstone rule (§6) applies: a deprecated anchor id is never reused. **Boundary:** this rule governs sections and anchors INSIDE documents; whole-file lifecycle (creating or deleting files) is git's domain and is not restricted by it. Compaction (service-side) MAY purge long-deprecated sections; resolution of citations to purged anchors is a deferred feature (the "cemetery" — a tombstone index answering "existed, deprecated, see replacement"). **Interim behavior:** between purge and the cemetery, citations to purged anchors DANGLE (unresolvable) — purge is irreversible, so it is applied only with grace periods and never by writers.

### 10.2. Fence-aware parsing (MUST, tooling)

[ref: #mds-fence-aware-parsing]

Any tooling parsing these documents MUST be fence-aware: heading-looking lines inside fenced code blocks (```` ``` ```` or `~~~`) are content, not headings. A naïve parser does not produce slightly wrong structure; it produces phantom sections with real-looking keys that overwrite real content.

### 10.3. Frontmatter stripping (MUST, tooling)

[ref: #mds-frontmatter-stripping]

Tooling MUST strip the YAML frontmatter block before heading detection: its closing `---` line otherwise parses as a setext H2 underline (§7.2). Frontmatter is never part of any chunk and never hashed (tracking protocols bump header fields on mutation; hashing the header would invalidate every chunk on every edit). If the header is unparseable (`errata: bad_frontmatter`), the body still indexes; the H1–title pairing check is skipped for that document.

## 11. The Errata Mechanism

[ref: #mds-the-errata-mechanism]

Conformance is repaired, not rejected (§4). The repair queue lives inside the documents themselves, as a single optional top-level frontmatter field:

```yaml
errata: [over_cap, multi_h1]
```

YAML flow style is REQUIRED so the canonical enumeration command works everywhere: `rg '^errata: \['`.

**Semantics.** A non-empty `errata` list means the document REQUIRES rewriting to this standard by an agent — it demands, not requests. Absent or empty means clean.

**Computation (authoritative).** Tooling computes the authoritative reason set fresh at every indexing pass from the current document; the field in the file is a greppable snapshot between passes.

**Writer rules (MUST):**

1. Writers MAY add deviations they know of (self-report — outside a running index service this is the only detection channel).
2. A writer MAY remove a specific reason ONLY after a guaranteed complete fix of ALL instances of that reason type in the document.
3. Writers MUST NOT add, modify, or clear reasons they do not understand (forward compatibility: unknown reasons belong to their owners' standards).
4. Writers MUST NOT lose `errata` when rewriting the header for other reasons.

**Encounter rules (MUST):**

1. An agent that AUTHORS a violation MUST fix it.
2. An agent that encounters an unflagged violation in passing is NOT obliged to fix it, but MUST do one of two — fix it or flag it in `errata`. Silence is non-conformant.
3. For a document already carrying `errata`, there is NO remediation obligation — voluntary repair is allowed, and the agent's own writing MUST conform regardless.

**Clearing.** The field clears (shrinks, then disappears) only when ALL reasons resolve; partial fixes shrink the list.

**Silent mechanical fixes are NOT errata:** anchor injection, header normalization, and empty-slug rephrasing are performed by tooling in-line without flagging. Duplicate anchors are the exception: tooling repairs them silently for key integrity AND flags `dup_anchor` — flag-and-repair.

**Headerless documents.** A file without frontmatter gets an empty frontmatter block created by the service (or the remediating agent) with `errata: [no_frontmatter, …]` written into it; the remediator then writes the full conformant header.

**Reason enum** (extensible; new reasons are proposed to the user before use):

| Reason | Family | Meaning |
|---|---|---|
| `over_cap` | structure | a subtree exceeds the queue limit after all chunk rules |
| `multi_h1` | structure | more than one H1 |
| `zero_headings` | structure | no headings at all (whole-file chunk, synthetic `_file` chain) |
| `setext` | structure | setext heading present |
| `skipped_level` | structure | heading level skip |
| `preamble_semantic` | structure | semantic preamble in a sectioned document (§7.5) |
| `dup_chain` | addressing | duplicate slugged chain in the document |
| `dup_anchor` | addressing | duplicate anchor id (tooling repairs silently AND flags) |
| `empty_slug` | addressing | pure-symbol heading (slugs to empty) |
| `heading_markup` | addressing | bold/italic/link markup in a heading (§8.5) |
| `nonlatin_heading` | addressing | non-Latin letters in a heading (writer-side rule) |
| `no_frontmatter` | frontmatter | no frontmatter block (header created empty to hold it) |
| `bad_frontmatter` | frontmatter | unparseable YAML / broken envelope |
| `invalid_schema` | frontmatter | required fields missing or wrong |
| `title_mismatch` | frontmatter | frontmatter `title` ≠ H1 text (§7.1) |

**Family ownership.** Families `structure` and `addressing` live in THIS standard (`markdown-protocol`); family `frontmatter` is owned by `frontmatter-protocol` — its rules define what those reasons mean and its extension process adds new ones. Rulings about this mechanism are recorded in Serena decision cards (`decisions/project/markdown_headings_integration`). When skill reference corpora migrate to this standard, the families apply unchanged — `frontmatter`-family reasons are then evaluated against the lazyload/tracking schemas of the corpus.

Rationale: `[ref: #mds-rationale-the-errata-mechanism]` in `references/rationale.md`.

## 12. Cross-File Citation (recommendation)

[ref: #mds-cross-file-citation]

Anchor ids SHOULD be globally unique within their domain (e.g. all skills of one repository), so a bare `[ref: #<anchor>]` citation resolves unambiguously across files. When citing across files or skills, name the owner: `[ref: #<anchor>]` in `<skill>/<file>` (example: `[ref: #entity-namespace-registry]` in `entity-protocol/SKILL.md`). Domains mint their own anchor prefixes to keep the global space collision-free (`entity-`, `ra-`, `fm-`, `serena-`, `mds-`, …). **Minting prefixes (MUST):** a new prefix is NEVER created unilaterally — the agent presents variants to the user and writes only after the user's decision. Serena memories rarely need prefixes (the memory name is the address); domain artifacts (skills, standards, corpora) MUST carry a domain prefix for separation.

## 13. Relationship to Other Standards

[ref: #mds-relationship-to-other-standards]

- **`markdown-protocol` (the host skill):** this standard lives inside it; its other rules (date format, no manual line wrapping, no bare `---` in bodies, YAML quoting style) remain in force and are not restated here.
- **`frontmatter-protocol` (tracking extension):** owns the mandatory tracking field set; the `errata` key is registered there as an optional top-level field with semantics pointing here.
- **`frontmatter-protocol` (lazyload extension):** owns `[ref: #…]` marker usage for reference corpora routing; the marker syntax, tight placement, and kebab-case ids are deliberately the same notation — one mental model across memories and skill corpora.
- **Positional addresses** (e.g. `1.3.7.2`, `§8.3`): a display/citation layer computed from the document tree, never an identity layer. Positional numbers NEVER enter anchor ids.

## 14. Out of Scope

[ref: #mds-out-of-scope]

Retroactivity and enforcement planning (this is the authoring standard, not an adoption plan); index schemas of any particular service; embedding provider/model selection; dead-citation resolution ("cemetery" implementation); retrieval-time context expansion.
