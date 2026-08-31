---
name: existence-bible
description: "MANDATORY existence-review standard (rule ids A1–K5): every line of a changeset must earn its existence, and 'why does this exist' outranks 'is this correct'. Always active. Governs keep/revert/delete decisions, abstraction justification, types, layers, errors, naming, flow, local development, migration, logging, and review-answer discipline; overrides language style guides on conflict. Consumed by cross-skill reference — never copied — by discuss-first (co-implementation mode) and code-review (Existence Inquisition)."
triggers:
  always: true
  reason: "Existence review applies to every decision and every new abstraction in any session, including sessions that never enter discuss-first mode."
version: 0.2.0
---

# SKILL: Existence Bible (Existence-Review Standard)

[ref: #existence-bible]

On conflict with language style guides (e.g. `python-lang` Google-style sections), this standard wins. Applies to all code.

## Mission

[ref: #exist-mission]

Every line of a changeset must earn its existence with a strong, current reason. Anything the task can be solved without is removed — without losing meaning, quality, or behavior the business depends on. The reviewer mindset: "why does this exist?" outranks "is this correct?".

## Family A — Existence & Subtraction

[ref: #exist-existence-subtraction]

- A1. Every symbol and line answers: "who consumes it? what breaks if deleted?" No answer — deletion candidate. Burden of proof is on the added line, never on the deletion. Code is a liability, not an asset: every retained line costs review, build, and cognitive load.
- A2. Defensive code splits into two classes. Defense at trust boundaries (untrusted external input, security-sensitive paths) is presumed justified by a named threat. Defense of internal invariants requires a probability estimate of the scenario it defends against ("how likely is SIGTERM within milliseconds?"), weighted by the cost of the consequence (probability × impact). No realistic probability — remove the defense.
- A3. Dead code dies immediately: commented-out lines, unreachable branches, unused exports, re-exports of nothing, dead event waits.
- A4. One PR = one purpose. Orthogonal improvements (even good ones) are extracted to a separate PR, never defended inside this one. Small changes are reviewed faster and more thoroughly; a reviewer may reject a changeset for size alone (Google eng-practices, Small CLs). A patch is a minimal accurate answer to exactly one identified and agreed problem (Hintjens, Simplicity Oriented Design).
- A5. Before writing anything new, enumerate what master/library/existing primitives already provide. Slightly extending the old beats writing the new.
- A6. YAGNI is explicit: no features, parameters, hooks, layers, or abstractions built for hypothetical future requirements. A "we will need it later" claim requires a concrete, dated consumer; otherwise the code is deleted on sight. Do the simplest thing that could possibly work (Beck / XP).
- A7. Chesterton's fence — earned removal. A1–A3 put the burden of proof on lines added in this changeset. For pre-existing code the burden flips: before deleting, establish why it was introduced (git blame, consumers, incident history). "Looks pointless" is a research question, not a conclusion. Once the original reason is understood and is genuinely obsolete — remove confidently.

## Family B — Derive, Don't Declare

[ref: #exist-derive-dont-declare]

- B1. Any state derivable from another source must not exist: a mode flag when the value itself determines the source; a readiness event when startup is sequential in lifespan; a registered-set when the target dict can hold items.
- B2. No parallel bookkeeping: never maintain a second structure describing what the first one already knows. The failure mode has a name — update anomaly (database normalization): the same fact stored in multiple places, one copy updated, another missed. The fix is always "make the first structure answer the question", never "keep both in sync carefully".
- B3. Configuration is formed once, at the initialization point, from a single source (settings). Never spread env reads or config-builder helpers across modules. Mechanics: env is read exactly once at startup into a single validated settings object, passed down as a dependency. Forbidden: `os.environ`/`getenv` scattered across modules; import-time env reads outside the settings module (tests set env after import; pre-fork workers inherit stale state). Provenance: 12-factor config.
- B4. Coordination primitives (events, locks, retries, caches) are re-justified against the CURRENT execution model, not the historical one that created them. A primitive surviving the model that needed it is cargo cult (Feynman's cargo-cult science, applied to programming) — ritual code. Each surviving primitive names the current concurrency/ordering fact it protects ("two writers to this dict from asyncio tasks"); no fact — it dies.
- B5. Derived values are computed at read time, not stored and synced. If value X is computable from Y within the same lifetime scope, storing X creates a synchronization obligation: every write path to Y must also update X, and every missed path is a bug. Compute X instead. (Provenance: React docs — out-of-sync state variables are the bug class, not the exception.)

## Family C — Types & Shapes (STRICT)

[ref: #exist-types-shapes]

- C1. Functions and methods NEVER return raw dicts. Return a frozen dataclass by default — a pydantic model only at the cross-border (C7/C10). Explicitly typed dicts (`dict[str, X]`) are tolerated only for verbatim passthrough — and must carry the type annotation. The smell has a name — primitive obsession (Fowler/Beck): a raw dict flattens a domain concept into primitives; every caller must remember what each key means, which values are allowed, and which combinations are impossible.
- C2. No Optional/nullable fields or parameters without a named reason. Optionality is resolved ONCE at the outer boundary (handler/servicer); inner layers receive strict, already-validated shapes. Nullable input producing nullable output is doubly forbidden. Resolving optionality once at the boundary IS parsing (C12): a boundary check that does not produce a refined shape forces re-validation forever downstream.
- C3. No staticmethods. A class without a state invariant is not a class — use flat module-level functions.
- C4. Structures tell the truth: declared shape == actual content (no "labelsets" that turn out to be tuples). Guarantees (ordering, format, casing) must survive transformations — re-derive them explicitly where needed.
- C5. A contract must describe the behavior it drives. A model missing the fields its behavior requires is a lie and is rejected on sight.
- C6. Define values correctly at the source; never define-then-transform (UPPER constants with lower() calls downstream).
- C7. Dicts are forbidden as function/method INPUTS too, not only as returns: every exchange is a pydantic model (cross-border validation) or a frozen dataclass (everything inside). A raw dict may exist only at the wire edge itself (codec encode/decode, driver rows inside an anti-corruption adapter) and never crosses the boundary.
- C8. No `X | None` returns: a lookup-style function returns the strict object or RAISES the domain exception at the source (unknown session raises `SessionNotFoundError` where detected, not `None` at every caller). Type-inference reconciliation becomes unmanageable otherwise.
- C9. Model-to-model conversion via `**` or `*` unpacking is STRICTLY FORBIDDEN — only explicit field-by-field mapping. `model_dump()` is legal ONLY for wire serialization at the boundary, never to feed one model from another.
- C10. Frozen dataclasses by default; mutable only when mutation is an explicit need, documented in the docstring. Pydantic lives ONLY at the cross-border (bus wire, HTTP/MCP surface, settings, frontmatter): strict validation at the edge, then convert to frozen and fly frozen through the process.
- C11. Text constants → `StrEnum`, numeric constants → `IntEnum` — members ALWAYS via `auto()`. No bare string/int magic values in signatures, comparisons, or wire payloads. Enums close the allowed set (C13): an unknown member is unconstructable, not merely invalid. This applies inside a service/process; at the cross-service protocol level, follow D6 (plain strings).
- C12. Parse, don't validate (Alexis King). A validation check is point-in-time: it says the data was acceptable at that moment, and the guarantee decays the moment the data moves on. Parsing is one-way: untrusted input crosses the boundary ONCE and comes out as a type correct by construction, and from there the type itself carries the proof — no re-checking downstream. Corollary (King, "Names are not type safety"): a wrapper type that enforces no invariant at construction is a rename, not a guarantee.
- C13. Make illegal states unrepresentable (Yaron Minsky). Prefer shapes where invalid combinations cannot be constructed over shapes where they are merely rejected at runtime. Every runtime check guarding a representable-but-invalid state is a candidate for a shape change that deletes the check.

## Family D — Layers & Isolation (PARANOID DDD / HEXAGONAL)

[ref: #exist-layers-isolation]

- D1. The domain knows nothing of transport: no grpc/pb2/http/ORM imports in domain code. Dependencies point one way, inward — the Dependency Rule (Uncle Bob, Clean Architecture): outer circles are mechanisms, inner circles are policies. A leak (e.g. sqlalchemy in the grpc layer) is a blocking defect.
- D2. Each layer receives data in its own shape and never parses another layer's format: Timestamp at protocol, datetime in domain; domain models at business boundaries, primitives or named parameters at call sites. This is the anti-corruption layer's job (Evans): each layer's shape is its bounded context's model; translation happens at the boundary, in both directions, and nowhere else.
- D3. App semantics never leak into shared libraries ("in the library it has decisively nothing to do"); library mechanics are never reimplemented in the app. Defects are fixed at the source repository, not worked around downstream.
- D4. Abstractions must not leak: internal state of a machine/module never escapes its boundary (a state machine's statuses are not other modules' constants). Cross-module, only the public interface exists.
- D5. Authorization lives at its designated layer, exactly once. Input validation is owned by C2/C12 (parse once at the outer boundary); below the boundary everything is already parsed and authorized — never re-validated at lower levels.
- D6. Cross-service shared enums are fragile contracts (adding a value breaks every other service): prefer plain strings at protocol level.
- D7. No foreign types across package boundaries: driver/library types (db drivers, redis clients, httpx, pydantic, builtins) may exist INSIDE a package but NEVER cross its public boundary — domain types or sanitized values cross instead. The anti-corruption layer applies at package granularity: the package boundary is a mini bounded-context boundary; driver rows live and die inside the adapter.
- D8. Async-first: all ports are `async`; sync adapters are wrapped, never the reverse. Carve-out: pure value providers (clocks, config) stay sync deliberately.
- D9. Ports are owned by the core and written in the core's vocabulary (Cockburn). A port interface expresses what the domain needs (`get_session(id) -> Session`), never mirrors the external API or driver surface (`scan_index(cursor, count)` leaking redis-isms). The adapter translates; the port does not imitate. If a port signature changes when the driver changes, the port was drawn at the wrong boundary.

## Family E — Errors

[ref: #exist-errors]

- E1. Crash-loud at startup/config boundaries: "the process did not start, and that is correct." No cleanup theater before the process has even started. Crash-only software (Candea & Fox, 2003): the crash path is the ONLY recovery path; startup and crash-recovery share one code path, so it stays tested. Cleanup theater before startup is doubly wrong: untested code on a path that restart already covers.
- E2. One central error-mapping place (exception handler / interceptor). Local try/except is justified only where behavior genuinely differs. Ousterhout's exception aggregation: the goal is minimizing the NUMBER of places exceptions are handled; one top-level handler/interceptor is the default shape, local handling is the justified exception.
- E3. Few error types; a new error class exists only with differentiated handling. Short message; details in extras. Throwing is easy, handling is hard: every new error type multiplies handling sites across the codebase; a new class without differentiated handling is pure cost.
- E4. No stringly-typed error matching, no reflection-driven dispatch, no class-level string tags checked elsewhere.
- E5. Errors carry a single machine vocabulary (a reason enum) consumed by ONE serializer; no other module references numeric codes directly. Every exception class name ends with `Error`.
- E6. Define errors out of existence first (Ousterhout). Before adding an exception path, ask whether the semantics can absorb the case: `unset()` of an absent key is a no-op, not an exception; an idempotent retry makes the duplicate delivery unexceptional. The cheapest exception is the one the API revision deletes. Only the cases that survive this revision earn an error type (E3) and a mapping (E2).

## Family F — Naming & Vocabulary

[ref: #exist-naming-vocabulary]

- F1. Public interfaces speak business language, not pattern language — never Strategy/FSM/Factory/Manager in names ("how would the domain expert explain this concept?"). Ubiquitous language (Evans): the test is literal — the domain expert uses the same word. The language is exercised relentlessly in code, docs, and conversation; a name drifting from the domain word is renamed, not explained.
- F2. Uniform verbs (`list`), uniform prepositions (`by`), uniform error names across the entire codebase — for years and across services. A new word in a name needs a strong reason. This is "one word per concept" (F10) applied to verbs and prepositions: uniformity is not aesthetics, it removes the question "is this difference meaningful?" from every read.
- F3. Function names: one word, two at most. Needing more signals an architecture problem or code dirt.
- F4. No `utils` packages — code sits next to its only caller. A function used in one file belongs to that file.
- F5. No opaque aliases — call the function itself. Prefer qualified imports (`uuid.UUID`, `postgresql.JSONB`) over aliased ones.
- F6. `const.py` per package — every constant (tuples, frozensets, limits, compiled regexes compiled exactly once); no magic values inside logic modules. `types.py` per package — `Annotated` aliases with constraints and a one-line comment each.
- F7. One module = one coherent feature: small modules merge into their consumer; never one module per function.
- F8. Behavior rides on the owning object as methods/properties (derived side-effect-free views are `@property`; factories are `@classmethod` like `from_parsed`) — not free functions.
- F9. Facades: explicit re-exports with a complete sorted `__all__`, always imported from the DEFINING module. `__init__.py` never imports heavy modules eagerly — heavy/experimental imports are lazy (PEP 562 `__getattr__`) or absent.
- F10. One word per concept, and names must be searchable (Clean Code). Pick one term per abstract concept and stick to it across the codebase — mixing `fetch`/`retrieve`/`get` for the same operation forces every reader to ask whether the difference is meaningful. Noise-word distinctions are forbidden: if two names differ only by a noise word (`Data`/`Info`/`Manager`), one of them is lying. A name is also a search token: rg must find all its uses; single letters and overloaded words are confined to tiny scopes.

## Family G — Flow & Readability

[ref: #exist-flow-readability]

- G1. Early return / fail-fast: negative scenarios first, happy path unnested. Guard clauses are a named refactoring (Fowler catalog); the nested form is the arrow anti-pattern (Atwood, "Flattening Arrow Code") — cyclomatic complexity correlates with error frequency, so flattening is a defect-rate change, not cosmetics.
- G2. One comprehension = one job: never query + parse + build in a single comprehension; separate the steps.
- G3. Code self-documents through structure; a comment block explaining requirements means the structure is wrong. Two-sided with G6: a WHAT-comment means the structure is wrong; a WHY-comment without a checkable reference is incomplete.
- G4. Related logic is co-located: a unified config is not exploded into sub-functions that force jump-driven reading.
- G5. Lifecycle symmetry: setup pairs with shutdown; initialization pairs with teardown.
- G6. Comments carry the WHY; the code carries the WHAT. A comment restating what the code does is rot-in-waiting and means the structure is wrong (G3). A comment recording a non-obvious reason — workaround, external constraint, deliberate deviation — is load-bearing and MUST carry a checkable reference (issue link, ADR, source doc) so the reason survives to the next reader. A why-comment with a reference turns Chesterton's fence (A7) from archaeology into a lookup.

## Family H — Local Development

[ref: #exist-local-development]

- H1. The service boots locally without infrastructure: literals, no-op implementations, empty config — no vault, no cache, no sidecars required. This attacks the tools gap of dev/prod parity (12-factor X); the parity being kept is code path (H4), not infrastructure.
- H2. Auth method/infra flavor is selectable via env (e.g. `*_AUTH_TYPE`) with production-shaped defaults; never fail-open defaults. Secure by default / fail securely (OWASP): production-shaped defaults are fail-closed; the insecure flavor must be the explicit opt-in, never the default.
- H3. Required envs crash at import/startup with the variable named; a dev opt-in is always explicit, never a silent default. This is E1 (crash-loud) applied to configuration — the variable name in the crash message is the diagnostic, so name it exactly.
- H4. Local boot exercises the production code path; only adapters differ. No-op and literal implementations sit behind the same ports (D8/D9) — the domain flow, validation, and error mapping run identically. A local mode that bypasses domain logic (mocked handlers, special-cased flows) proves nothing and is a lie about deployability. Dev/prod parity (12-factor X) is parity of code path and config shape, never of backing services.

## Family I — Migration & Legacy

[ref: #exist-migration-legacy]

- I1. Requirements are restated in the new world's terms. Schemes leaked from the old system (custom prefixes, legacy DSN formats, sidecar flows) die unless they re-earn their place. Strangler fig (Fowler): the new world draws behavior out of the old; the migration ends at zero legacy responsibilities, not at "new path works".
- I2. One level of indirection needs a named, current consumer (rotation, multi-tenancy). Otherwise store the value directly (literal in DB, not a reference to a reference). Wheeler's aphorism: any problem can be solved with another level of indirection, except the problem of too many levels of indirection — an indirection layer is a cost item that needs a paying consumer.
- I3. Validation is complete or absent: a regex that checks patterns checks ALL patterns — no regex plus manual patch-up checks.
- I4. A migration that stops at "expand" is not a migration — it is permanent dual maintenance. Every expand step (parallel change: expand → migrate → contract, Fowler) carries its contract step in the plan: the old path has a deletion condition or date, and "both paths forever" is the explicitly rejected outcome. A strangler fig ends when the legacy has zero responsibilities left and is switched off; a half-finished strangler is two systems forever, with double the attack surface and double the reasoning cost.

## Family J — Logging & Observability

[ref: #exist-logging-observability]

- J1. Level discipline per entry; secrets/DSN/credentials are never logged — not even at debug (a debug toggle must never force a credential rotation). The exclusion list is canonical (OWASP Logging Vocabulary Cheat Sheet: passwords, keys, certs, PII, source code). Level semantics are fixed and identical everywhere: DEBUG = deep diagnostics (disabled/sampled in production), INFO = expected lifecycle events, WARN = unusual but not broken, ERROR = failure requiring attention.
- J2. Structured extras over f-strings in log calls; one log per event (no duplicate loggers reporting the same fact). The schema is consistent across services: field names are uniform vocabulary (F2/F10 applied to log fields) — a field renamed per service breaks cross-service queries.
- J3. Operational logging belongs at the central handler/interceptor layer.
- J4. CLI logging goes to stderr; stdout is reserved for program output and protocol channels.
- J5. Every operation carries a correlation id through all its log entries. A log entry that cannot be joined to its request/operation is half a fact. Logs are correlated with metrics and traces, not analyzed in isolation; a log-only investigation is a smell of missing instrumentation.

## Family K — Review-Answer Discipline (meta)

[ref: #exist-review-answer-discipline]

- K1. Facts before answers: read the library, run the code, check the corpus — then respond. Every reviewer question maps to either a change or a factual answer. Strong opinions, weakly held (Saffo): answer with facts AND a confidence level, plus what evidence would change the answer. When new facts arrive, the answer changes explicitly. The forbidden failure mode: "justified loudly until overwhelmed".
- K2. Trade-offs are surfaced explicitly (e.g. "this moves the failure from startup to request time"); the decision belongs to the user, never silently taken by the agent. Per Google eng-practices: every reviewer comment is either accepted as a change or answered with facts — and on disagreement, consider first whether the reviewer is right; they often are.
- K3. Deployment reality is part of scope: env renames require a manifest transition plan; DB-held values are migration inputs, not afterthoughts.
- K4. Library escalation (HARD): whenever a change needs a library in a place where it is banned, any new dependency, or any exemption — STOP and escalate to the user. Placement, workarounds, and exemptions are decided together, never unilaterally.
- K5. "Fix it in a later PR" is a debt instrument, not a plan (Google eng-practices, pushback). A deferred fix exists only as a tracked artifact: an issue or TODO with an owner and a checkable reference (G6), named in the review answer. An untracked "later" is how entropy wins. The default answer to pushback is fixing in THIS PR (A4); deferral needs the same justification as a loan.

## Operating Workflow

[ref: #exist-operating-workflow]

0. As-is map: full diff vs base, every touched component, consumers per symbol (call sites, tests, manifests, DB data). Scale + overview tree. Gate: user approves the overview.
1. Top-down walkthrough, one level per message: per element — keep / revert / delete, justified by rule ids (A1–K5).
2. Pipeline traversal, forward and backward, after removals.
3. Final contour + master approval; blueprint recorded as a decision card.
4. Implementation exactly per contour; project lint/type/test gates green. Deliverables: minimal diff, keep/delete table, ready answers per reviewer question, follow-ups list.
