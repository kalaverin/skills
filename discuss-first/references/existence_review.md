---
subject: "Existence review standard for code changesets; subtraction, existence proof, derive-not-declare, strict types, pydantic, layer isolation, hexagonal DDD, error mapping, naming vocabulary, readability flow, local development, migration legacy, logging, review discipline, operating workflow, discuss-first pairing."
index:
  - anchor: exist-mission
    what: "The mission of the standard: every line of a changeset earns its existence with a strong current reason; 'why does this exist' outranks 'is this correct'."
    problem: "Changesets accumulate lines nobody can justify; reviewer asks correctness questions while unneeded code ships; unjustified lines, existence debt, review drift, purpose absence, cargo cult additions, changeset bloat, maintenance tax, meaning dilution."
    use_when: "Opening any changeset review; framing the reviewer's mindset; explaining the standard's purpose."
    avoid_when: "Concrete rule lookup — the family sections carry the normative lines."
    expected: "Reader adopts existence-first mindset before touching any rule."
  - anchor: exist-existence-subtraction
    what: "Family A: existence proof and subtraction — burden of proof on added lines, defensive-code probability estimates, dead code removal, one-PR-one-purpose, reuse before writing."
    problem: "Diff grows with speculative helpers, defensive branches for impossible scenarios, commented corpses, unused exports, orthogonal improvements smuggled inside; scope creep, orphan symbols, re-exports, duplicate primitives, smuggled refactors, purpose mixing, zombie code."
    use_when: "Judging whether a line or symbol may stay; challenging defensive code; splitting multi-purpose changesets."
    avoid_when: "Type-shape questions — family C owns those; layer placement — family D owns that."
    expected: "Every surviving line names its consumer and its breakage scenario; everything else is removed."
  - anchor: exist-derive-dont-declare
    what: "Family B: derive, do not declare — no derivable state, no parallel bookkeeping, single-source configuration, coordination primitives re-justified against the current execution model."
    problem: "Codebase keeps flags duplicating what values say, second structures shadowing first ones, env reads scattered across modules, locks and events inherited from extinct architectures; state clones, bookkeeping twins, config scatter, stale coordination, redundant caches, source drift."
    use_when: "Reviewing state, flags, config flow, or coordination primitives; designing initialization."
    avoid_when: "Naming questions — family F owns those; error design — family E owns that."
    expected: "Every stored value has exactly one source; primitives match the live execution model."
  - anchor: exist-types-shapes
    what: "Family C (STRICT): typed shapes — never raw dict returns or inputs, raise-not-None lookups, explicit field mapping, frozen-by-default, pydantic only at the border, enum constants, no staticmethods, truthful structures, behavior-complete contracts."
    problem: "Functions hand out raw dicts, nullable fields multiply without reasons, staticmethods fake cohesion, declared shapes lie about content, models miss fields their behavior needs, constants get lowercased downstream; type lies, optional sprawl, shape drift, contract gaps, transform chains."
    use_when: "Reviewing signatures, models, return types, optionality; designing data contracts."
    avoid_when: "Layer placement of those types — family D owns boundaries."
    expected: "Declared shapes equal actual content; optionality exists only with named reasons at the boundary."
  - anchor: exist-layers-isolation
    what: "Family D (paranoid DDD/hexagonal): layer isolation — domain free of transport, per-layer data shapes, no app semantics in libraries, no abstraction leaks, single-boundary validation, plain strings over shared enums, no foreign types across boundaries, async-first ports."
    problem: "Grpc imports creep into domain, layers parse foreign formats, app concepts leak into shared libraries, internals escape module boundaries, validation repeats at every level, shared enums break sibling services; domain pollution, boundary violations, isolation decay, transport coupling, format parsing."
    use_when: "Reviewing imports, layer boundaries, shared libraries, validation placement, cross-service contracts."
    avoid_when: "Within-layer type shapes — family C owns those."
    expected: "Dependencies point inward only; each layer speaks its own shape; validation happens once."
  - anchor: exist-errors
    what: "Family E: error design — crash-loud at startup, one central mapping place, few differentiated error types, no stringly-typed matching, single error vocabulary with one serializer."
    problem: "Codebase grows cleanup theater before startup, try except confetti everywhere, error classes without differentiated handling, string tags dispatched by reflection; error sprawl, exception soup, silent catches, dispatch magic, startup cowardice, mapping duplication."
    use_when: "Reviewing exception handling, error taxonomies, startup behavior, interceptors."
    avoid_when: "Logging of errors — family J owns observability."
    expected: "Startup crashes loud; mapping lives in one place; every error type earns differentiated handling."
  - anchor: exist-naming-vocabulary
    what: "Family F: naming discipline — business language over pattern language, uniform verbs and prepositions, one-word function names, no utils packages, no opaque aliases, const/types modules per package, one module one feature, behavior on the owning object, explicit facades."
    problem: "Interfaces speak Strategy and Manager instead of domain words, verbs drift per file, function names need four words, utils packages swallow orphans, aliases hide real calls; vocabulary drift, pattern speak, utils dumping, alias opacity, naming inflation."
    use_when: "Naming any public interface, function, or package; reviewing vocabulary uniformity."
    avoid_when: "Structural flow questions — family G owns readability."
    expected: "Names speak domain language uniformly; every function sits next to its caller."
  - anchor: exist-flow-readability
    what: "Family G: flow and readability — early return, one comprehension one job, structure over comments, co-located logic, lifecycle symmetry."
    problem: "Happy path nests three levels deep, comprehensions query parse and build at once, comment blocks explain what structure should, related logic scatters across files, setup lacks shutdown; nesting depth, comprehension abuse, comment crutches, co-location decay, lifecycle asymmetry."
    use_when: "Reviewing control flow, comprehensions, comment blocks, setup/teardown pairing."
    avoid_when: "Vocabulary choices — family F owns naming."
    expected: "Happy path unnested; structure self-documents; lifecycle pairs visibly."
  - anchor: exist-local-development
    what: "Family H: local development — service boots without infrastructure, env-selectable auth flavors with production-shaped defaults, required envs crash named at startup."
    problem: "Service demands vault and sidecars for local boot, auth defaults fail open, missing env surfaces three requests later unnamed; boot friction, infra coupling, permissive defaults, late crashes, silent dev modes, configuration traps."
    use_when: "Reviewing configuration, env handling, local boot path, auth selection."
    avoid_when: "Config single-sourcing mechanics — family B owns that."
    expected: "Service boots locally with literals and no-ops; every required env fails fast and named."
  - anchor: exist-migration-legacy
    what: "Family I: migration and legacy — requirements restated in new-world terms, indirection needs a named current consumer, validation complete or absent."
    problem: "Legacy schemes survive porting unquestioned, values hide behind references to references, regex validates half patterns then manual patch-up covers rest; legacy drag, indirection abuse, partial validation, prefix fossils, blind inheritance, old-world leakage, scheme zombies."
    use_when: "Reviewing migrations, ported schemas, indirection layers, validation rules."
    avoid_when: "New-world type shapes — family C owns those."
    expected: "Every inherited scheme re-earns its place or dies; validation is total or absent."
  - anchor: exist-logging-observability
    what: "Family J: logging discipline — level per entry, secrets never logged, structured extras, one log per event, operational logging at the central layer, CLI logging to stderr."
    problem: "Debug toggle leaks DSN into logs forcing credential rotation, f-strings replace structured extras, three loggers report one fact; secret leakage, log noise, duplicate events, unstructured output, observability decay, level chaos."
    use_when: "Reviewing log calls, levels, extras, operational logging placement."
    avoid_when: "Error taxonomy itself — family E owns error design."
    expected: "No secret ever logged at any level; one structured entry per event."
  - anchor: exist-review-answer-discipline
    what: "Family K (meta): review-answer discipline — facts before answers, trade-offs surfaced explicitly, deployment reality in scope, library escalation stop-and-ask."
    problem: "Agent answers reviewer from memory instead of checking library, hides trade-offs behind silent decisions, forgets manifests and migrations until deploy breaks; unfounded answers, hidden trade-offs, deploy surprises, guesswork, evidence absence, scope blindness."
    use_when: "Answering any reviewer question; preparing review responses; planning env or schema changes."
    avoid_when: "The code rules themselves — families A–J own those."
    expected: "Every answer factual; every trade-off explicit; deployment planned, not discovered."
  - anchor: exist-operating-workflow
    what: "The operating workflow pairing with discuss-first: as-is map, top-down keep/revert/delete walkthrough justified by rule ids, pipeline traversal, master approval, contract implementation with defined deliverables."
    problem: "Standard exists on paper yet execution improvises: diff never inventoried, deletions lack rule citations, traversal skipped after removals, deliverables vague; workflow absence, execution drift, citation gaps, missing contour, approval holes, delivery fog, ad-hoc review."
    use_when: "Running any review or refactor under the standard; pairing with the discuss-first mode phases."
    avoid_when: "Greenfield design with no existing diff — the as-is map step is vacuous there."
    expected: "Minimal diff delivered with keep/delete table, ready answers, follow-ups list."
---

# Existence Review Standard

Baked verbatim from the distilled review standard of a senior maintainer (~310 review comments, 2023–2026, 14 repos, plus owner rules). Mandatory hard rule of the `discuss-first` skill: while the mode is active, every element is justified against these rule ids (A1–K4). On conflict with language style guides (e.g. `python-lang` Google-style sections), this document wins. Applies to all code.

## Mission

[ref: #exist-mission]

Every line of a changeset must earn its existence with a strong, current reason. Anything the task can be solved without is removed — without losing meaning, quality, or behavior the business depends on. The reviewer mindset: "why does this exist?" outranks "is this correct?".

Distilled from ~310 review comments (2023–2026, 14 repos) of a senior maintainer, plus owner rules.

## Family A — Existence & Subtraction

[ref: #exist-existence-subtraction]

- A1. Every symbol and line answers: "who consumes it? what breaks if deleted?" No answer — deletion candidate. Burden of proof is on the added line, never on the deletion.
- A2. Defensive code requires a probability estimate of the scenario it defends against ("how likely is SIGTERM within milliseconds?"). No realistic probability — remove the defense.
- A3. Dead code dies immediately: commented-out lines, unreachable branches, unused exports, re-exports of nothing, dead event waits.
- A4. One PR = one purpose. Orthogonal improvements (even good ones) are extracted to a separate PR, never defended inside this one.
- A5. Before writing anything new, enumerate what master/library/existing primitives already provide. Slightly extending the old beats writing the new.

## Family B — Derive, Don't Declare

[ref: #exist-derive-dont-declare]

- B1. Any state derivable from another source must not exist: a mode flag when the value itself determines the source; a readiness event when startup is sequential in lifespan; a registered-set when the target dict can hold items.
- B2. No parallel bookkeeping: never maintain a second structure describing what the first one already knows.
- B3. Configuration is formed once, at the initialization point, from a single source (settings). Never spread env reads or config-builder helpers across modules.
- B4. Coordination primitives (events, locks, retries, caches) are re-justified against the CURRENT execution model, not the historical one that created them.

## Family C — Types & Shapes (STRICT)

[ref: #exist-types-shapes]

- C1. Functions and methods NEVER return raw dicts. Return a pydantic model or a frozen dataclass. Explicitly typed dicts (`dict[str, X]`) are tolerated only for verbatim passthrough — and must carry the type annotation.
- C2. No Optional/nullable fields or parameters without a named reason. Optionality is resolved ONCE at the outer boundary (handler/servicer); inner layers receive strict, already-validated shapes. Nullable input producing nullable output is doubly forbidden.
- C3. No staticmethods. A class without a state invariant is not a class — use flat module-level functions.
- C4. Structures tell the truth: declared shape == actual content (no "labelsets" that turn out to be tuples). Guarantees (ordering, format, casing) must survive transformations — re-derive them explicitly where needed.
- C5. A contract must describe the behavior it drives. A model missing the fields its behavior requires is a lie and is rejected on sight.
- C6. Define values correctly at the source; never define-then-transform (UPPER constants with lower() calls downstream).
- C7. Dicts are forbidden as function/method INPUTS too, not only as returns: every exchange is a pydantic model (cross-border validation) or a frozen dataclass (everything inside). A raw dict may exist only at the wire edge itself (codec encode/decode, driver rows inside an anti-corruption adapter) and never crosses the boundary.
- C8. No `X | None` returns: a lookup-style function returns the strict object or RAISES the domain exception at the source (unknown session raises `SessionNotFoundError` where detected, not `None` at every caller). Type-inference reconciliation becomes unmanageable otherwise.
- C9. Model-to-model conversion via `**` or `*` unpacking is STRICTLY FORBIDDEN — only explicit field-by-field mapping. `model_dump()` is legal ONLY for wire serialization at the boundary, never to feed one model from another.
- C10. Frozen dataclasses by default; mutable only when mutation is an explicit need, documented in the docstring. Pydantic lives ONLY at the cross-border (bus wire, HTTP/MCP surface, settings, frontmatter): strict validation at the edge, then convert to frozen and fly frozen through the process.
- C11. Text constants → `StrEnum`, numeric constants → `IntEnum` — members ALWAYS via `auto()`. No bare string/int magic values in signatures, comparisons, or wire payloads.

## Family D — Layers & Isolation (PARANOID DDD / HEXAGONAL)

[ref: #exist-layers-isolation]

- D1. The domain knows nothing of transport: no grpc/pb2/http/ORM imports in domain code. Dependencies point one way, inward. A leak (e.g. sqlalchemy in the grpc layer) is a blocking defect.
- D2. Each layer receives data in its own shape and never parses another layer's format: Timestamp at protocol, datetime in domain; domain models at business boundaries, primitives or named parameters at call sites.
- D3. App semantics never leak into shared libraries ("in the library it has decisively nothing to do"); library mechanics are never reimplemented in the app. Defects are fixed at the source repository, not worked around downstream.
- D4. Abstractions must not leak: internal state of a machine/module never escapes its boundary (a state machine's statuses are not other modules' constants). Cross-module, only the public interface exists.
- D5. Authorization lives at its designated layer; input validation happens exactly once, at the outer boundary — never repeated at lower levels.
- D6. Cross-service shared enums are fragile contracts (adding a value breaks every other service): prefer plain strings at protocol level.
- D7. No foreign types across package boundaries: driver/library types (db drivers, redis clients, httpx, pydantic, builtins) may exist INSIDE a package but NEVER cross its public boundary — domain types or sanitized values cross instead.
- D8. Async-first: all ports are `async`; sync adapters are wrapped, never the reverse. Carve-out: pure value providers (clocks, config) stay sync deliberately.

## Family E — Errors

[ref: #exist-errors]

- E1. Crash-loud at startup/config boundaries: "the process did not start, and that is correct." No cleanup theater before the process has even started.
- E2. One central error-mapping place (exception handler / interceptor). Local try/except is justified only where behavior genuinely differs.
- E3. Few error types; a new error class exists only with differentiated handling. Short message; details in extras.
- E4. No stringly-typed error matching, no reflection-driven dispatch, no class-level string tags checked elsewhere.
- E5. Errors carry a single machine vocabulary (a reason enum) consumed by ONE serializer; no other module references numeric codes directly. Every exception class name ends with `Error`.

## Family F — Naming & Vocabulary

[ref: #exist-naming-vocabulary]

- F1. Public interfaces speak business language, not pattern language — never Strategy/FSM/Factory/Manager in names ("how would the domain expert explain this concept?").
- F2. Uniform verbs (`list`), uniform prepositions (`by`), uniform error names across the entire codebase — for years and across services. A new word in a name needs a strong reason.
- F3. Function names: one word, two at most. Needing more signals an architecture problem or code dirt.
- F4. No `utils` packages — code sits next to its only caller. A function used in one file belongs to that file.
- F5. No opaque aliases — call the function itself. Prefer qualified imports (`uuid.UUID`, `postgresql.JSONB`) over aliased ones.
- F6. `const.py` per package — every constant (tuples, frozensets, limits, compiled regexes compiled exactly once); no magic values inside logic modules. `types.py` per package — `Annotated` aliases with constraints and a one-line comment each.
- F7. One module = one coherent feature: small modules merge into their consumer; never one module per function.
- F8. Behavior rides on the owning object as methods/properties (derived side-effect-free views are `@property`; factories are `@classmethod` like `from_parsed`) — not free functions.
- F9. Facades: explicit re-exports with a complete sorted `__all__`, always imported from the DEFINING module. `__init__.py` never imports heavy modules eagerly — heavy/experimental imports are lazy (PEP 562 `__getattr__`) or absent.

## Family G — Flow & Readability

[ref: #exist-flow-readability]

- G1. Early return / fail-fast: negative scenarios first, happy path unnested.
- G2. One comprehension = one job: never query + parse + build in a single comprehension; separate the steps.
- G3. Code self-documents through structure; a comment block explaining requirements means the structure is wrong.
- G4. Related logic is co-located: a unified config is not exploded into sub-functions that force jump-driven reading.
- G5. Lifecycle symmetry: setup pairs with shutdown; initialization pairs with teardown.

## Family H — Local Development

[ref: #exist-local-development]

- H1. The service boots locally without infrastructure: literals, no-op implementations, empty config — no vault, no cache, no sidecars required.
- H2. Auth method/infra flavor is selectable via env (e.g. `*_AUTH_TYPE`) with production-shaped defaults; never fail-open defaults.
- H3. Required envs crash at import/startup with the variable named; a dev opt-in is always explicit, never a silent default.

## Family I — Migration & Legacy

[ref: #exist-migration-legacy]

- I1. Requirements are restated in the new world's terms. Schemes leaked from the old system (custom prefixes, legacy DSN formats, sidecar flows) die unless they re-earn their place.
- I2. One level of indirection needs a named, current consumer (rotation, multi-tenancy). Otherwise store the value directly (literal in DB, not a reference to a reference).
- I3. Validation is complete or absent: a regex that checks patterns checks ALL patterns — no regex plus manual patch-up checks.

## Family J — Logging & Observability

[ref: #exist-logging-observability]

- J1. Level discipline per entry; secrets/DSN/credentials are never logged — not even at debug (a debug toggle must never force a credential rotation).
- J2. Structured extras over f-strings in log calls; one log per event (no duplicate loggers reporting the same fact).
- J3. Operational logging belongs at the central handler/interceptor layer.
- J4. CLI logging goes to stderr; stdout is reserved for program output and protocol channels.

## Family K — Review-Answer Discipline (meta)

[ref: #exist-review-answer-discipline]

- K1. Facts before answers: read the library, run the code, check the corpus — then respond. Every reviewer question maps to either a change or a factual answer.
- K2. Trade-offs are surfaced explicitly (e.g. "this moves the failure from startup to request time"); the decision belongs to the user, never silently taken by the agent.
- K3. Deployment reality is part of scope: env renames require a manifest transition plan; DB-held values are migration inputs, not afterthoughts.
- K4. Library escalation (HARD): whenever a change needs a library in a place where it is banned, any new dependency, or any exemption — STOP and escalate to the user. Placement, workarounds, and exemptions are decided together, never unilaterally.

## Operating Workflow (pairs with discuss-first when active)

[ref: #exist-operating-workflow]

0. As-is map: full diff vs base, every touched component, consumers per symbol (call sites, tests, manifests, DB data). Scale + overview tree. Gate: user approves the overview.
1. Top-down walkthrough, one level per message: per element — keep / revert / delete, justified by rule ids (A1–K4).
2. Pipeline traversal, forward and backward, after removals.
3. Final contour + master approval; blueprint recorded as a decision card.
4. Implementation exactly per contour; project lint/type/test gates green. Deliverables: minimal diff, keep/delete table, ready answers per reviewer question, follow-ups list.
