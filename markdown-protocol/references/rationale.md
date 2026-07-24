---
subject: "Rationale for markdown headings standard; rejected alternatives, design decisions, evidence appendix, corpus study metrics, Again tooling context, chunking model, key scheme, edition notes, `markdown-protocol`, empty-slug rescue, deprecation asymmetry, errata history, prefix discipline."
index:
  - anchor: mds-rationale-scope
    what: "Why the standard exists and why its scope is any agent-authored Markdown."
    problem: "Reader accepts rules without knowing which collapse they prevent; unmotivated obedience, why-questions, rationale absence, context hunger, purpose doubt, motivation vacuum, justification need, standard skepticism, origin curiosity, birth rationale, existence questions."
    use_when: "Justifying the standard to a skeptic; teaching its motivation; onboarding to its scope decision."
    avoid_when: "Normative rule text — the specification owns it."
    expected: "Motivation for the contract and its reach understood."
  - anchor: mds-rationale-conformance-model
    what: "Why repair beats rejection: availability outranks purity."
    problem: "Reader asks why dirty files still index instead of being quarantined; rejection temptation, availability doubt, model confusion, purity myth, gate questions, refusal curiosity, repair philosophy, service doctrine, uptime doctrine, correction theory."
    use_when: "Explaining the repair model; defending availability-first enforcement."
    avoid_when: "Errata mechanics — the errata rationale and the specification's mechanism section."
    expected: "Rejection-alternative understood as deliberately rejected."
  - anchor: mds-rationale-slug-specification
    what: "Why slugging, the rejected alternatives, and the empty-slug hole story."
    problem: "Reader questions why identity is normalized and how symbol-only headings are rescued; normalization doubt, transliteration questions, hole curiosity, alphabet debate, rescue mechanics fog, identity theory, symbol philosophy, recovery doctrine, slug doctrine."
    use_when: "Defending slug design; explaining empty-slug handling to maintainers."
    avoid_when: "The normative computation — the specification's slug section."
    expected: "Slug design defended with alternatives accounted."
  - anchor: mds-rationale-anchor-specification
    what: "Why two identity layers exist and why anchors are not chunk keys."
    problem: "Reader conflates citation identity with index keys; layer confusion, key conflation, UUID questions, depth debate, identity model fog, layering philosophy, eternity debates, recompute doctrine, master separation, dual doctrine, id philosophy, key philosophy."
    use_when: "Explaining the two-layer identity design; defending slug ids over UUIDs."
    avoid_when: "Anchor form rules — the specification's anchor section."
    expected: "Citation-eternity vs recomputable-index layering understood."
  - anchor: mds-rationale-structural-rules
    what: "Per-rule commentary for H1, ATX, levels, depth, and the preamble carve-out."
    problem: "Reader challenges single-H1 dogma, setext ban, or flat-file exception; dogma doubt, setext questions, carve-out curiosity, structure debates, exception confusion, preamble economics, root philosophy, skeleton discussions, grammar philosophy, H1 doctrine, tree doctrine, skeleton lore."
    use_when: "Defending structural rules; explaining the flat-file carve-out economics."
    avoid_when: "The rules themselves — the specification's structural sections."
    expected: "Each structural choice explained with its rejected alternative."
  - anchor: mds-rationale-addressing-discipline
    what: "Per-rule commentary for chains, cosmetics, the rename ban, and plain text."
    problem: "Reader asks why renames are banned so harshly or why cosmetics are free; ban harshness, cosmetic confusion, discipline debates, identity philosophy questions, strictness curiosity, freedom paradox, edit doctrine, ban rationale, rigor doctrine."
    use_when: "Defending the rename ban; explaining cosmetic freedom."
    avoid_when: "The rules themselves — the specification's addressing sections."
    expected: "Harshness understood as deliberate externalization prevention."
  - anchor: mds-rationale-section-size-and-shape
    what: "Why merging was rejected and how the limit values form a three-party contract."
    problem: "Reader proposes merging small chunks or arbitrary caps; merge temptation, cap confusion, contract doubt, sizing debates, powers questions, glue proposals, threshold curiosity, value discussions, sizing philosophy, binary questions, sizing lore, contract lore."
    use_when: "Defending no-merge and the 8192/16536 contract values."
    avoid_when: "The caps themselves — the specification's size rules."
    expected: "No-merge and power-of-two caps defended concretely."
  - anchor: mds-rationale-lifecycle-and-tooling-rules
    what: "Per-rule commentary for deprecation asymmetry, fences, and frontmatter."
    problem: "Reader questions why writers may never delete or why headers are unhashable; deletion questions, asymmetry doubt, hash curiosity, lifecycle debates, purge confusion, immutability questions, header exclusion, delete temptation, lifecycle lore, tomb philosophy."
    use_when: "Defending deprecation asymmetry; explaining frontmatter exclusion."
    avoid_when: "The rules themselves — the specification's lifecycle sections."
    expected: "Writer-service asymmetry and hash exclusion understood."
  - anchor: mds-rationale-the-errata-mechanism
    what: "Why the queue lives in files, the naming history, and the write-rule amendment."
    problem: "Reader wonders why errors get recorded in documents instead of some registry, and who may write them; registry questions, placement doubt, naming curiosity, write-rule fog, storage debates, queue philosophy, field ownership, queue lore."
    use_when: "Defending in-file errata; explaining the amended recording duty."
    avoid_when: "The mechanism itself — the specification's errata section."
    expected: "In-file queue and honest-recording rule defended."
  - anchor: mds-rationale-cross-file-citation
    what: "Why the skills domain formalized global anchor uniqueness."
    problem: "Reader asks why bare anchors work across files in this domain; uniqueness curiosity, prefix questions, domain debate, collision history, practice codification fog, id globalization, namespace discipline, citation scaling, prefix lore, domain unity, scaling curiosity."
    use_when: "Explaining prefix discipline; extending it to new domains."
    avoid_when: "The recommendation text — the specification's citation section."
    expected: "Global uniqueness understood as codified practice."
  - anchor: mds-rationale-relationship-to-other-standards
    what: "Why notation is shared with lazyload and why positional numbers stay out of anchors."
    problem: "Reader questions notation reuse and positional-anchor bans; notation doubt, position debate, standards confusion, id philosophy questions, id purity discussions, shared-syntax curiosity, boundary philosophy, sharing questions, notation history, format overlap, syntax unity, id design."
    use_when: "Defending shared notation and position-free anchors."
    avoid_when: "The relationships map — the specification's relationship section."
    expected: "Shared notation and anchor purity defended."
  - anchor: mds-extras-again-tooling-context
    what: "The Again service machinery the standard was designed against: chunking, keys, and the full rejection graveyard."
    problem: "Reader wants service-side pictures this standard deliberately excludes from normative scope; machinery curiosity, chunking questions, key debates, tooling fog, internals hunger, backend debates, design backdrop, exclusion rationale, service lore, engineering context."
    use_when: "Learning Again's chunking and key model; reviewing rejected alternatives wholesale."
    avoid_when: "Writer duties — Again internals bind no writer here."
    expected: "Again internals understood without entering the normative scope."
  - anchor: mds-evidence-appendix
    what: "The corpus study metrics table driving each design choice."
    problem: "Reader demands numbers behind every rule and finds them here; evidence hunger, metric questions, study curiosity, data debates, proof demand, empirical basis, measurement traceability, data proof, corpus facts, statistical backing."
    use_when: "Citing study data; verifying a rule's data backing."
    avoid_when: "Normative text — the specification owns that."
    expected: "Every metric traceable to its driven rule."
  - anchor: mds-design-notes-of-this-edition
    what: "This edition's own decisions: section format over RFC, prefix, write-rule, waivers."
    problem: "Reader asks why this edition looks as it does versus an RFC draft; edition curiosity, format debates, prefix questions, decision history fog, revision archaeology, format history, choice rationale, design lore, edition rationale, format verdict, history record."
    use_when: "Understanding edition history; revisiting the format decision."
    avoid_when: "The standard itself — the specification is canonical."
    expected: "Edition choices and their reasons on record."
---

# Rationale: Markdown Headings as a Public API

Commentary, rejected alternatives, and evidence for `references/specification.md`. Each section maps 1:1 to a section of the standard (linked back via its anchor). Extras that have no standard counterpart live at the end (Again tooling context, evidence appendix, design notes).

## Rationale: Scope and Conformance Classes

[ref: #mds-rationale-scope]

**Why this standard exists.** Index services address chunks by hashes of heading chains. Without an authoring discipline, machine addressing collapses: renamed headings orphan citations, duplicated headings collide in key space, markup in headings poisons normalization, and parser-naïve corpora (headings inside code fences) produce phantom structure. The 2026-07-24 corpus study quantified every one of these failure modes in the wild (see the Evidence Appendix). The standard is the cheapest point of intervention: constrain the writer slightly so that every downstream machine consumer becomes simple, deterministic, and repair-driven instead of fallback-driven.

**Why "any agent-authored Markdown" and not "Serena memory files".** The original draft scoped itself to Serena memory files. The skills repository broadened it: plans, reports, reference corpora, and standards are written by the same agents and consumed by the same machines, so one discipline covers all of it.

## Rationale: Conformance Model

[ref: #mds-rationale-conformance-model]

**Rejected alternative: strict rejection.** An earlier idea treated conformance limits (size caps, uniqueness) as indexing gates: split, refuse, or quarantine non-conformant input. Rejected because a memory service that refuses memories fails its mission; availability outranks purity. The errata queue gives the same end state — a conformant corpus — via repair instead of rejection, and it degrades gracefully under future background reconciliation.

## Rationale: Slug Specification

[ref: #mds-rationale-slug-specification]

**Why slugging at all.** Identity must tolerate cosmetic edits: fixing letter case, dropping a colon, or reformatting bold markers must not re-key a section. Slug normalization makes those edits free.

**Rejected alternatives:** (a) raw heading text as identity — every cosmetic edit becomes a breaking rename, making the key system hostile to normal editing; (b) transliteration of non-Latin scripts — lossy, non-reversible, and unnecessary since the hash layer is charset-agnostic; (c) Latin-only slug alphabet — would make hundreds of real headings in the wild corpus unaddressable; the Latin rule belongs to writers, the service must be liberal in what it accepts (Postel's law, applied to identity).

**The empty-slug hole (closed).** A heading consisting solely of symbols (`` `%` ``, `` `**` ``, `` `.()` `` — 10+ real occurrences in one API-reference file) slugs to the empty string; all such headings in a file collide into one degenerate slug, destroying chain uniqueness unfixably. Therefore: pure-symbol headings are forbidden for writers; tooling rephrases them into words during maintenance (e.g. `` `%` `` → `operator-percent`; an exceptional service-side heading edit, always logged); the last-resort fallback is a synthetic slug `h` + first 12 hex chars of `xxh64(raw_heading_text)`. A plain "use the hash" rule without rephrasing was rejected: it produces keys no human can read or predict, and it hides an authoring defect instead of repairing it.

**Why symbols are stripped and leading digits are dropped.** Backticks are Unicode category Sk (symbol), not punctuation — stripping only P* would leave them in the slug and break the empty-slug analysis, so the algorithm strips S* alongside P*. Leading digits are POSITIONAL information (`3.5 Parser`), and position is never identity in this design — so digits and dashes at the very start are removed (`3.5 Parser` → `parser`, `2024 Report` → `report`, `2fa` → `fa`), while digits after the first letter are free (`RFC 2119` → `rfc-2119`, keeping the identifier intact instead of collapsing it to `rfc`). By-design consequence: sections differing only in leading numbers collide as `dup_chain` — writers MUST give sections meaningful names, not numbers.

## Rationale: Anchor Specification

[ref: #mds-rationale-anchor-specification]

**Why anchors exist, and why they are not the chunk key.** Two identity layers serve two masters. **Citations** need eternity: a cross-reference written into another memory, another project, or another session must resolve forever, across compactions that move and merge sections. **Index keys** need recomputability: the service must re-derive its entire state from files at any time, with no stored history. Anchors serve the first master (they live in the file and travel with their section through any reorganization); heading-chain hashes serve the second (they are pure functions of current content). The layering principle — *file anchors are eternal citation identity; chunk keys are recomputable index organization* — is the load-bearing idea of the whole design.

**Rejected alternatives:** (a) positional addresses as identity (`1.4.3`) — any insertion renumbers every later section, producing mass re-keys and rotting citations; positional addresses survive only as recomputed display/citation forms; (b) anchor-primary chunk keys — anchors cover only H1/H2, so deep sections would fall back to chains anyway, creating a two-form key space and a collision risk between the forms; a single chain-hashed key form with anchors as the citation layer is simpler and total; (c) UUID anchors — perfectly stable but unreadable; slug ids self-document; (d) mandatory anchors at all depths — marker noise on every H4 would pollute the documents agents read most; H1/H2 covers the overwhelming majority of real citation targets.

## Rationale: Structural Rules

[ref: #mds-rationale-structural-rules]

**Single H1.** One document = one identity. The title, the H1, and the file's addressing root are three faces of one entity; allowing several H1s forks that entity and makes "the document" unaddressable as a whole. Rejected: multi-root documents as legal — the service can process them (in degradation mode), but legalizing them would force every citation format to carry a root selector forever.

**ATX only — the `---` trap.** A setext H2 underline is byte-identical to a frontmatter closing delimiter and to a thematic break. `markdown-protocol` already forbids bare `---` in bodies for exactly this reason; setext reintroduces the ambiguity through the back door. One grammar (ATX) keeps the delimiter law enforceable by the simplest possible anchored-line parsers.

**No skipped levels.** Skipped levels make the tree ambiguous: is the H3 a child of the H1, or a missing-H2 authoring error? Deterministic re-parenting is fine for machines, but legalizing skips would hide real structural mistakes from their authors. Rejected: silent acceptance as a style choice — the study shows skips are accidents, not style (0.12%, randomly distributed).

**Depth unlimited — rejected: depth caps.** An early proposal limited depth to H3/H4 to keep documents "simple". Rejected: depth is the author's tool for decomposing complex topics, and the addressing model prices it correctly — anchors are required only at H1/H2, deeper levels are opt-in for citation. The corpus shows depth is self-limiting (H5: 134 headings, H6: 13 — under 0.7% combined).

**Preamble discipline — the flat-file carve-out is load-bearing.** The original draft banned preamble absolutely — and thereby outlawed ~39% of the memory corpus: flat single-thought memories ("one finding = one short file"), the canonical form of findings in this ecosystem. The carve-out keeps the mass form legal while making hybrid "intro + sections" files conform: their intro must move into the first section or into a meta-note. Trade-off accepted knowingly: 17.6% of memory files need this migration touch during compaction, and the meta-vs-semantic boundary is enforced editorially, not provable by a parser. Rejected: (a) absolute ban — kills the flat form; (b) free preamble — preamble text is unaddressable: it belongs to no section, so it can neither be chunked honestly nor cited.

## Rationale: Addressing Discipline

[ref: #mds-rationale-addressing-discipline]

**Unique chain — rejected: occurrence indexes (`:occN`).** An earlier design disambiguated duplicate chains with a positional occurrence suffix in the composite key. Dropped because it re-introduces positional instability exactly where duplicates live (inserting another same-named section renumbers the suffixes and re-keys them), and — more importantly — because it engineers *around* a defect instead of repairing it. The errata queue makes the document fix itself: duplicates are flagged, an agent rewrites the headings, keys stabilize forever. In conformant corpora the occurrence code path would be dead code carrying live risk.

**Cosmetic differences unregulated.** An early candidate rule forbade headings differing only by case/punctuation as a separate offense. Redundant: slugging erases those differences, so such headings are either identical (uniqueness violation) or distinct (no issue). One rule, one gate.

**Rename ban.** This is the harshest rule in the standard, and it is deliberate. The alternative — "rename freely, machines cope" — externalizes the cost of every casual edit onto reindexing, citation rot, and graph re-pointing. The ban externalizes nothing: it makes identity changes visible, rare, and intentional (deprecation ceremony instead of silent drift). The service-side machinery (keyset diff, meta-git rename detection, `rekey`) exists precisely so that the *ban is discipline, not fragility*: violations are survivable but countable.

**Plain-text headings.** Markup in headings buys nothing visually (headings are already emphasized) and costs identity hygiene: the same section written twice with different emphasis becomes a slug collision, and markup stripped by slugging makes the visible text and the identity diverge. Evidence: bold-vs-plain duplicate pairs (`**Risk-management-api**` vs `**risk-management-api**`) were the entire collision set of the memory corpus (8/8 cases). The backtick exception exists because code identifiers are literal names — `` `temporal.io` `` and "temporal.io" are different statements, and slugging treats backticks as punctuation anyway, so the exception is free.

## Rationale: Section Size and Shape

[ref: #mds-rationale-section-size-and-shape]

**One thought — rejected: minimum-size merging.** The study agent recommended merging chunks under 200 characters into the next sibling. Rejected, because merging makes a chunk's content a function of its neighbors' sizes: an edit to any sibling re-defines the merged chunk's boundaries and re-keys content that never changed — the same cascade instability the whole key design exists to eliminate. It also breaks the 1:1 mapping between a citation address and an index unit. Short embeddings are semantically precise (a single fact embeds better alone than glued to a neighbor).

**Size limits — why in the standard, and why these values.** The limits are a three-party contract: writers shape sections to them, the service chunks to them, and the databases (embedding model token windows, snippet sizes) are sized against them. Putting them in the standard (not in service config) gives all three parties one number to agree on; revising the limits is a standards revision coordinated with the databases. The writer limit 8192 bytes (2^13) is a power of two so it can be tuned jointly with storage/embedding parameters without fractional drift; at ~4 bytes per token of technical English it is ≈ 2k tokens — comfortably inside every current embedding window with room for metadata. The queue limit 16536 is sized against the service's storage and snippet parameters. The terms "soft limit" and "hard limit" are retired: they suggested a rejection semantics that the repair model forbids — limits trigger errata, never rejection. Rejected: hard mechanical splitting — a machine that cuts prose at a byte boundary produces chunks no human would write and no embedding model should see; the service's job is to index faithfully and demand repair (errata), not to mangle content into compliance.

## Rationale: Lifecycle and Tooling Rules

[ref: #mds-rationale-lifecycle-and-tooling-rules]

**Deprecation instead of deletion.** Deletion breaks citations identically to renaming: both orphan every inbound reference. Deprecation preserves resolvability at trivial cost — one line of text. The purge question was decided asymmetrically on purpose: writers may never delete (they cannot know who cites them), the service may purge (it owns the indexes and can apply grace periods), and dead-citation resolution is a designed-in future feature rather than an emergency patch.

**Fence-aware parsing.** In the combined study corpus, 1889 fenced lookalikes made up 8.0% of all ATX-like lines (115 in memory files, 1774 in skill references — 13% of its ATX-like lines). A naïve parser does not produce slightly wrong structure; it produces phantom sections with real-looking keys that overwrite real content.

**Frontmatter stripping.** ~99.9% of memory files carry frontmatter, so the setext trap (a closing `---` line read as a setext H2 underline) arms on essentially every file. Frontmatter is never part of any chunk and never hashed: our tracking protocol bumps `updated_at` on every mutation, and hashing the header would invalidate every chunk on every edit.

## Rationale: The Errata Mechanism

[ref: #mds-rationale-the-errata-mechanism]

**Why a queue in the files, and why this name.** Alternatives to in-file marking: registry-only tracking (invisible to agents, ungreppable, splits the truth across two stores) and silent auto-repair of semantic problems (machines should not rewrite meaning). The in-file list makes conformance a distributed, greppable, agent-executable work queue that both humans and future background reconciliation consume with zero new infrastructure. The reason list is mandatory (not a bare boolean) because a remediating agent must know what to fix without re-deriving it.

**Naming history:** `dirty` + `dirty_reasons` (initial proposal — two fields, blunt but industrial), `needs_rewrite` (rejected as long and bureaucratic), `lint`, `debt`, `fixme`, `tainted` (evaluated); **`errata`** won because it is dictionary-precise ("list of errors in a published work"), collapses flag and reasons into one field, and collides with no existing writer vocabulary.

**The `no_frontmatter` case** was first removed as absurd — a file without a header has nowhere to record it — and then restored by having the service create the empty header to hold it; registry-side tracking of headerless files was thereby eliminated as unnecessary.

**The write-rule amendment (skills-repo decision).** The original draft forbade writers to touch `errata` at all (service and remediators only). The final rule keeps the intent — never lose reasons to a careless header rewrite — while making honest handling a writer duty: writers self-report known deviations (outside a running index service, self-report is the only detection channel); a reason may be removed only after a guaranteed complete fix of ALL its instances; unknown reasons are never touched (forward compatibility). Encounter rules close the loop: authoring a violation obliges fixing it; passing by an unflagged one obliges fixing or flagging (silence is non-conformant); already-flagged documents carry no obligation. Duplicate anchors resolve as flag-and-repair (silent fix for key integrity plus the flag), not as silent-only fixes.

## Rationale: Cross-File Citation

[ref: #mds-rationale-cross-file-citation]

The original draft was silent on cross-file anchors. The skills repository already practices cross-file citation at scale (`[ref: #entity-…]`, `[ref: #serena-…]`, `[ref: #fm-…]`), so the recommendation formalizes it: globally unique anchor ids per domain, owner naming on citation, and domain-minted prefixes to keep the global space collision-free. The `mds-` prefix of this very corpus is an instance of that rule.

## Rationale: Relationship to Other Standards

[ref: #mds-rationale-relationship-to-other-standards]

The standard deliberately reuses the `[ref: #…]` notation of `frontmatter-protocol` (lazyload extension) rather than inventing a parallel marker syntax: one mental model across memories and skill corpora. The `errata` key lives in the frontmatter standard as an optional top-level field only — its enum and semantics live here, in the markdown standard, so each side owns what it is authoritative for.

**Positional addresses never enter anchor ids.** A numbered-heading display form (`§8.3`) is allowed for human citation, but anchors stay position-free slugs; embedding numbers in ids would make every renumbering a breaking identity change — the exact instability this standard exists to remove.

## Extras: Again Tooling Context (informative)

[ref: #mds-extras-again-tooling-context]

The Again memory service's machinery this standard was designed against. Informative for writers; normative only inside that service.

**Chunking model (summary):** (1) ascent — a whole file body within the writer limit (8192 bytes) becomes one H1 chunk (flat files are this case by definition); (2) base — every H2 subtree within the writer limit is one chunk; (3) targeted descent — an H2 subtree over the writer limit is chunked at H3 level inside that H2 only; the H2's own body becomes a chunk keyed `h1:h2`; no recursion below H3; (4) over cap — anything still over the queue limit (16536 bytes) is indexed whole and flagged `errata: over_cap`. Chunk content is always exactly one contiguous file region; content hashes cover section bytes only, never frontmatter.

**Key scheme (summary):** composite chunk key `ph:fh:ch` = `xxh64("domain:name") : xxh64(rel_path) : xxh64(slug(h1):…:slug(hN))` — hex-rendered, colon-joined, prefix-addressable (`ph:*` project, `ph:fh:*` file). Project identity `domain:name` = last two canonical-path segments, portable across machines (the multi-machine future requires it); identical `domain:name` from different canonical paths = HARD STOP with a rename requirement. Renames of a domain or project directory trigger a dedicated `rekey` activity recomputing only the `ph` component. Backends: Manticore receives a derived u64 `doc_id = xxh64(composite)`; Lance/Kuzu store the composite natively; `rel_path`, `heading_path`, `own_slug`, `level`, `version` are non-key attributes — class queries like "all sections named X" filter on `own_slug`, deliberately not a key property.

**Rejected alternatives (the full graveyard):** fixed-size byte chunking (no semantic alignment); dynamic per-file chunk-level policies (unpredictable keys); recursive descent below H3 (diminishing returns); `.partN` positional splits (killed by the errata model — caps are conformance gates, not indexing gates); tiny-chunk merging; "descend as deep as possible" and "ascend as high as possible" (both destroy granularity deliberately — descent and ascent are limit-violation resolvers, not policies); xxhash32 (birthday collisions: ~1% at 6k chunks, 50% at 77k); sha256 (dropped for one hash family everywhere — xxh64); a single hash of the whole tuple (loses prefix scans); random ULID project ids (requires a registration handshake, and orphans all backend data if the registry is rebuilt — the hash is stateless: a lightweight proxy computes it from its PWD with no round-trip); full canonical path as identity (breaks on every checkout move and is machine-specific — `domain:name` is portable); positional addresses as identity (renumbering cascades); own-slug as the chunk key (collides on within-file duplicates); `a:`/`c:` type prefixes (vacuous once anchor = slugged heading); `:occN` occurrence suffixes (see the occurrence-index rejection in the addressing rationale).

## Evidence Appendix (corpus study 2026-07-24, combined)

[ref: #mds-evidence-appendix]

| Metric | Value | Drives |
|---|---|---|
| Files / headings analyzed | 2157 / 21669 | — |
| Frontmatter share (memory files) | 99.94%, closed 8-field tracking set | frontmatter contract |
| Flat (H1-only) files (memory) | 623/1603 = 39% | preamble carve-out, ascent rule |
| H2 section size (memory) | p50=294, p90=1328, p99=4071 chars | H2 base level, 4096 limit (historical threshold) |
| H2 subtrees over 4096 / over 8192 | 6.0% / 0.17% | size limits, over_cap rarity (historical thresholds) |
| Duplicate slug chains in file | 152 files (references), 0 (memory) | unique chain, dup_chain |
| Slug collisions of distinct headings | 203 (9.37 per 1000; 1.01 per 1000 in memory) | plain-text headings, empty_slug |
| Pure-symbol headings slugging to empty | 10+ in one API-reference file | empty-slug hole |
| Fenced heading lookalikes | 1889 = 8.0% of ATX-like lines | fence-aware parsing |
| Setext headings | 1 total | ATX only |
| Skipped levels | 27 = 0.12% | no skipped levels |
| Multi-H1 files | 49 (references), 0 (memory) | single H1 |
| Tiny sections (<200 chars, H2) | 20.7% | one thought (no merging) |
| Non-ASCII headings | 1072 (memory) | slug alphabet |

## Design Notes of This Edition

[ref: #mds-design-notes-of-this-edition]

- **Edition choice.** Two editions were drafted: a section-structured one and an RFC-styled one with numbered anchors. The section edition won because numbered anchors embed position into identity — the exact instability this standard forbids (anchors are eternal; positional numbers are display-only). Salvaged from the RFC edition: the Abstract section, per-section rationale links, and positional numbering of headings for human citation — with anchor ids kept position-free by explicit rule.
- **Prefix.** All anchors of this corpus carry the `mds-` prefix per the cross-file citation recommendation (domain-minted prefix of the `markdown-protocol` skill).
- **Errata write-rule.** Amended per the skills-repo decision (see the errata rationale section): writers record and shrink honestly; the ban targets accidental loss only.
- **Repo waivers.** Local exceptions (e.g. evolving plan/decision documents that may be retitled) live in the repository's agent memory (`agent/allowed_violations`), not in this standard.
