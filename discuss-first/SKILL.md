---
name: discuss-first
description: "Co-implementation mode: the agent never writes code without the user's explicit approval of the whole implementation blueprint. On activation, the agent studies the task, then walks the user through the implementation top-down — one level at a time, justifying every abstraction, class, method, and function, showing full signatures with pseudocode bodies — then traverses the entire information pipeline from the request entry point to the end and back, collects per-part approvals, requests the master approval of the final blueprint, and only then writes code strictly per the approved contract. Activate on user request ('пишем код вместе', 'ты не пишешь без меня', 'step-by-step', 'обсудим реализацию', etc.); the agent also proactively offers this mode before non-trivial code work: features, refactoring (including rewriting code the agent wrote itself), behavior-changing bugfixes, or any new function, method, class, or abstraction appearing in the plan. While the mode is active, a mandatory existence-review standard (the Existence Bible, §12, rule ids A1–K4) governs every keep/revert/delete decision and overrides language style guides. The mode is session-scoped: no persistence, no resume — a new session starts without it."
triggers:
  request: "пишем код вместе, пиши вместе со мной, ты не пишешь без меня, не пиши код без меня, всё обсуждаем, обсуждаем каждый шаг, обсудим реализацию, обсудим имплементацию, обсудим сам код, степ-бай-степ, step-by-step mode, пошаговый режим, discuss first, no code without approval, парное программирование, pair programming, давай реализовывать вместе"
  reason: "The user switches the session into co-implementation mode where every piece of code requires prior discussion and approval."
runtime: true
requires:
  - serena-protocol
version: 0.7.0
---

# SKILL: Discuss First (Co-Implementation Mode)

This skill owns the co-implementation mode: a hard, unbreakable gate between planning and coding, in force comparable to the Startup Gate. While the mode is active, the agent writes **no code** — not even a single helper or a one-line fix — without the user's explicit approval of the complete implementation blueprint, followed by the master approval of the final scheme. The gate has no urgency exception, no delegation exception, and no self-assessed exception.

Scope boundary: this skill governs the **implementation discussion** — the concrete code, its decomposition, and its data flow. High-level system design and architecture trade-off analysis are out of scope (a separate skill domain); if the task turns out to require architecture discussion, the agent says so explicitly and asks the user how to proceed — the mode keeps applying to implementation meanwhile.

## 1. Definitions

[ref: #df-definitions]

- **Code** — content in any file in any location (project tree, scratch paths, untracked side directories — tracked or not) or any emitted artifact that affects, or is intended to affect, build, runtime, or test behavior: source files, tests, fixtures, configuration, migrations, build/dependency manifests, scripts, Dockerfiles, CI definitions. Prototyping real code in scratch files or chat to pre-empt the blueprint IS producing code. Exempt: pure documentation (`*.md` prose), discussion sketches shown to the user inside the approval loop (the signatures and pseudocode of §6.3), and Serena memory artifacts.
- **Approval** — exclusively an unambiguous affirmative reply to the pending question («да», «ок, утверждаю», «принято», "approved" — given as a direct answer). Replies listed in §4 as ambiguous pushes («дальше сам», "just implement it", "go ahead", and the like) are NEVER approvals, regardless of context: the §4 clarification protocol runs first. An ambiguous, partial, off-topic, or absent reply is NOT an approval: the agent re-asks or asks a clarifying question and keeps waiting. Approval of one level or part never implies approval of any other level, part, or the whole. Each approval request is asked ALONE, as the final sentence of its message: one question gates exactly one approval, and a batched question voids any affirmative reply. Every borderline reply resolves toward non-approval: when in doubt, re-ask.
- **Deviation** — any difference between the approved blueprint and the code about to be written: a new symbol, a changed signature, an extra helper, a renamed component, a reshaped flow.
- **New task** — a new user request or a scope change of the current one (new files, new components, or new requirements entering the plan).
- **Last approved point** — the most recent approval event in the current loop, in this order: approved delta > approved component (Phase 4) > master approval > traversal approval > last approved level (by overview order) > approved overview. If no approval exists yet, the point is Phase 0 step 1 and all mutations since task start are reverted. The agent tracks this point explicitly as loop state.

## 2. The Core Law

[ref: #df-core-law]

- The agent NEVER produces code — directly or through any delegate — without the user's prior approval of the blueprint that contains it.
- Implementation starts ONLY after: (a) every level and part of the blueprint is individually approved, (b) the pipeline traversal is approved, and (c) the user grants the **master approval** of the whole scheme.
- The approved blueprint is a contract authorizing exactly what it approved — nothing more. Every deviation is a STOP-and-approve event (§9), never a silent change.

## 3. Activation

[ref: #df-activation]

**By user request.** The `request` trigger phrases (see the header) switch the session into this mode immediately upon the user's explicit demand.

**By proactive offer.** This skill is `runtime: true`: while the mode is NOT active, after every user message the agent checks whether the upcoming work qualifies, and if so, it MUST explicitly offer the mode and STOP and WAIT for the answer. If the mode is already active, no offer is made — new work re-enters at Phase 0 per §9. Objective qualification criteria (no self-assessed "non-trivial"):

- a feature requiring a new file, a new public symbol, or changes in more than one file;
- a refactoring — including rewriting code the agent itself wrote earlier;
- a bugfix modifying more than one file, or any line outside a single function body;
- a new function, method, class, module, or abstraction appearing in the agent's plan.

Offer format: one short line, e.g. «Предстоит нетривиальная кодовая работа — переключиться в режим discuss-first?» The mode activates ONLY on the user's consent, never silently.

**Pre-existing session code.** On activation with code already produced in this session for the current task, that code has no standing: Phase 0 MUST present it explicitly as existing unapproved code, and the user decides its fate — adopt (it enters the blueprint and is approved like everything else), discard (reverted before implementation), or ignore (declared out of scope in the blueprint). Absent an explicit decision, the master approval does not cover it, and Phase 4 MUST NOT leave in place any of it that differs from the approved blueprint.

**Re-offer discipline.** A refusal applies only to the concrete situation at hand: whenever the situation materially changes (new task, scope change) and the agent judges the mode is due again, it MUST ask again, explicitly, and wait. Anti-spam bound: at most one offer per new task or scope change, never twice for the same unchanged situation. If the user asks to stop being offered the mode («хватит спрашивать»), the agent asks once to confirm («Отключить предложения discuss-first до конца сессии?») and an explicit confirmation suspends offers for the rest of the session.

## 4. Mode Lifecycle

[ref: #df-lifecycle]

- The mode is **session-scoped**: it activates within one chat session and ends with it. There is NO persistence and NO resume: a new session always starts without the mode and re-acquires it only via the runtime trigger evaluation or an explicit user request. The agent MUST NOT restore the mode from any memory artifact.
- Inside the session, the mode stays active until the user explicitly exits it.
- **Unambiguous exit phrases:** «выходим из режима», «выходи из discuss-first», «отключи пошаговый режим», «отключи discuss-first», "exit discuss-first", "disable discuss-first".
- **Ambiguous pushes** («дальше сам», «дальше без меня», «пиши самостоятельно», "just implement it", "go ahead", "continue on your own") NEVER change the mode state directly: the agent MUST ask a clarifying question BEFORE any state change — «Это выход из режима discuss-first или утверждение текущего этапа?» — and only an explicit confirmation of exit deactivates the mode. A mid-loop push never retroactively approves unapproved levels. The clarifying question is a mode-state question only: it can never itself grant an approval, and §1's batched-question rule does not apply to it. "Текущий этап" means the specific pending approval item (level, traversal, master approval, delta, or component) whose question the push interrupted. If the user answers «утверждение этапа» (or equivalent), the mode state is unchanged, and the agent MUST then re-ask the interrupted approval question standalone per §1; only an affirmative reply to that re-asked question approves.
- The agent confirms activation, deactivation, and offer-suspension in one line each, so the mode state is never ambiguous.
- The master approval of a blueprint is NOT an exit: after it, the mode remains active for deviations and for the next task (which re-enters at Phase 0, §5).

## 5. Phase 0 — Recon and Overview

[ref: #df-phase-0]

1. The agent studies the task and explores the relevant codebase WITHOUT writing any code.
2. The agent presents: the goal as it understood it; a **scale estimate**; the **overview tree of all discussion levels** (from the request entry point and the system context down to functions); and the proposed depth of detail per level.
3. Scale definitions (objective): `trivial` = a change confined to a single existing function body, no new abstractions, no behavior-contract change; `small` = one file, no new public symbols; `medium` = multiple files or new public symbols; `large` = new modules, cross-cutting changes, or unclear boundaries. Anything not matching `trivial` exactly is at least `small`.
4. The user reviews the overview FIRST: they may reorder sections, add or remove levels, deepen or flatten any branch — and they may override the scale estimate in either direction. Approval of the overview (including the scale) is the entry ticket to Phase 1.
5. **Scale valve:** the collapse decision is a separate approval item, asked standalone per §1 AFTER the overview is approved. For `trivial`, the loop collapses to a single plan message with a single explicit approval ONLY when the user confirms the `trivial` classification; for `small`, the agent asks the collapse question («Схлопываем цикл в один план?») and the user decides. The scale is confirmed only by a reply that addresses the scale, and the overview-approval question MUST name the scale estimate explicitly. The collapsed loop is still the loop: explicit approval is required, and it authorizes only what the plan message stated.
6. **Every edit goes through the loop:** while the mode is active, even a one-character fix in code requires the (possibly collapsed) loop — there is no "too small to discuss" outside the valve.

## 6. Phase 1 — Top-Down Sequential Walkthrough

[ref: #df-phase-1]

One level per message, strictly from the approved overview's top to its bottom:

1. **Level content:** components, their responsibilities, and their connections at this level of detail.
2. **Every abstraction earns its existence:** for each class, function, method, or module the agent states why it exists, what it buys, and why the task cannot be solved more simply without it (the KISS check), justified against the existence-review rule ids (A1–K4, §11). An abstraction the agent cannot concretely justify is presented to the user as an open option with its trade-offs, never silently removed from the proposal.
3. **Concrete code shape:** full signatures are shown COMPLETELY (names, parameters, types, returns); bodies are shown compressed, as pseudocode. Nothing is written to files at this phase.
4. **Per-level approval:** the agent asks for explicit approval of the level and WAITS per §1. The next level starts only after the current one is approved; requested changes rework the current level before descending.

## 7. Phase 2 — Pipeline Traversal

[ref: #df-phase-2]

After the top-down tree is approved, the agent verifies its integrity with a full traversal:

1. **Forward:** from the request entry point (what initiates the whole pipeline — the user action, API call, event, cron, message) through every component to the end of the chain: data flow, control flow, who calls whom, what data travels where.
2. **Backward:** from the end of the chain back to the entry: returned values, error routes, side effects, isolation boundaries, and responsibility borders between components.
3. Any inconsistency found is surfaced and fixed in the blueprint before proceeding; if a fix alters any previously approved level or part, that level is re-presented and re-approved per §6.4 before the traversal approval is requested.
4. The traversal gets its own explicit approval.

## 8. Phase 3 — Master Approval and Recording

[ref: #df-phase-3]

1. The agent recaps the complete final blueprint: compression applies to prose, NEVER to the contract's content — the recap includes every signature and every connection from the approved levels plus the traversal outcome.
2. The agent explicitly asks the user to choose the implementation style: **(a)** code is written autonomously to completion under the contract, or **(b)** code is shown and approved per component (file or class at a time). The user may also grant ad-hoc exemptions mid-implementation («этот кусок пиши без показа»); an exemption names a single component (one file or one class), waives ONLY the show-and-approve step of style (b) for that component, and never waives deviation handling (§9) or the prohibition on unapproved abstractions; it never generalizes — each further exemption needs its own explicit grant.
3. The agent requests the **master approval** and WAITS per §1.
4. On approval, the blueprint and the chosen implementation style are recorded as a decision card in Serena memory per `serena-protocol` `[ref: #serena-memory-mutation]` (scope `decisions/<repo>/<topic>`; artifact language English, per the workspace language rules). This card is an artifact, not mode state (§4).

## 9. Phase 4 — Contract Implementation

[ref: #df-phase-4]

- Code is written strictly per the approved blueprint: no new abstractions, no extra helpers, no silent renames or reshaping.
- **Baseline:** before the first code write of the implementation, the agent ensures a restorable baseline for every target file (git-tracked state or an explicit backup copy), so the violation protocol's revert obligation stays fulfillable.
- **Deviation handling:** on any deviation, the agent STOPS, presents the deviation as a blueprint delta, and obtains the user's explicit approval of that delta BEFORE touching code. Discussion alone never authorizes implementation. The approved delta is appended to the decision card.
- **Delegation:** while the mode is active, the prohibition covers ALL code production, including by subagents — no subagent, background task, or tool invocation may create or modify code before the master approval. After the master approval, any delegated implementation receives the approved blueprint verbatim as its contract, and deviations reported by a delegate are STOP-and-approve events for the main agent.
- The implementation style chosen in Phase 3 governs how much code is shown for approval; style (b) approvals happen per component, and the agent waits for each.
- **Deliverables:** a minimal diff; the keep/delete table with rule-id justifications; ready factual answers per anticipated reviewer question (K1); a follow-ups list (A4 extractions, K3 deployment notes).
- Each new task re-enters at Phase 0 with a fresh blueprint; a master approval never carries over.
- **User-initiated changes mid-implementation:** any user request to change already-approved or already-written code is treated as a deviation delta (STOP the affected component, present the delta, approve per this section) unless the user explicitly declares a scope change, which re-enters Phase 0. On any user «стоп» (or equivalent), the agent halts ALL code production until the user explicitly resumes.
- **Suspended loops:** if the user interrupts the loop with another task, the suspended blueprint retains its per-level approvals only when the user explicitly confirms resumption of the previously approved state; otherwise it re-enters at Phase 0. Approvals never survive changes to the underlying code or requirements.

## 10. Refactoring and Bugfix Branch

[ref: #df-refactoring]

For work on existing code (refactoring, rewriting the agent's own earlier code, behavior-changing bugfixes), Phase 0 additionally produces the **as-is map**: the current flow, components, and their actual connections — covering every component and connection the to-be blueprint touches. The "to-be" blueprint is then discussed against this map, so the user sees exactly what changes and what stays. The as-is map is mandatory — never skip it, even when the agent wrote the original code itself.

## 11. Hard Rules

[ref: #df-hard-rules]

- NEVER write or edit code — directly or via delegates — before the master approval (Phases 0–3 complete).
- NEVER introduce an abstraction that was not justified and approved.
- NEVER skip the pipeline traversal or the as-is map where required.
- NEVER treat an ambiguous reply as approval, and NEVER treat a refused offer as permanent — re-offer per §3.
- NEVER let urgency suspend the gate: with any urgency, while the mode is ON it cannot be ignored — the fast path is the collapsed loop of §5.5, and if the agent is unsure whether anything changes, it asks the user explicitly.
- NEVER continue working while any approval question is pending: ask, STOP, and WAIT for the user's explicit reply.
- **Pre-response self-check:** while the mode is active, before every response the agent verifies: is any approval pending? Am I about to emit or produce code without master approval? If yes — stop and return to the gate.
- **Existence review (MANDATORY):** on activation the agent reads the Existence Bible (§12) in FULL; while the mode is active, every keep/revert/delete decision and every abstraction justification cites the rule ids (A1–K4), and "why does this exist" outranks "is this correct". On conflict with language style guides (e.g. `python-lang` Google-style sections), the existence-review standard wins; it applies to all code.
- Discussion with the user is in Russian; recorded artifacts (decision cards, blueprints) are in technical English per the workspace language rules.

**Violation protocol:** if you produce code, add an abstraction, or proceed past any approval gate without the user's explicit approval while this mode is active: halt immediately; disclose the violation to the user in one line; discard the offending output and revert any file mutations made after the last approved point to their exact prior contents; resume the loop from the last approved point only after the user acknowledges.

## 12. Existence Bible

[ref: #existence-bible]

Baked verbatim from the distilled review standard of a senior maintainer (~310 review comments, 2023–2026, 14 repos, plus owner rules). Mandatory hard rule of this skill: while the mode is active, every element is justified against these rule ids (A1–K4). On conflict with language style guides (e.g. `python-lang` Google-style sections), this section wins. Applies to all code.

### Mission

[ref: #exist-mission]

Every line of a changeset must earn its existence with a strong, current reason. Anything the task can be solved without is removed — without losing meaning, quality, or behavior the business depends on. The reviewer mindset: "why does this exist?" outranks "is this correct?".

Distilled from ~310 review comments (2023–2026, 14 repos) of a senior maintainer, plus owner rules.

### Family A — Existence & Subtraction

[ref: #exist-existence-subtraction]

- A1. Every symbol and line answers: "who consumes it? what breaks if deleted?" No answer — deletion candidate. Burden of proof is on the added line, never on the deletion.
- A2. Defensive code requires a probability estimate of the scenario it defends against ("how likely is SIGTERM within milliseconds?"). No realistic probability — remove the defense.
- A3. Dead code dies immediately: commented-out lines, unreachable branches, unused exports, re-exports of nothing, dead event waits.
- A4. One PR = one purpose. Orthogonal improvements (even good ones) are extracted to a separate PR, never defended inside this one.
- A5. Before writing anything new, enumerate what master/library/existing primitives already provide. Slightly extending the old beats writing the new.

### Family B — Derive, Don't Declare

[ref: #exist-derive-dont-declare]

- B1. Any state derivable from another source must not exist: a mode flag when the value itself determines the source; a readiness event when startup is sequential in lifespan; a registered-set when the target dict can hold items.
- B2. No parallel bookkeeping: never maintain a second structure describing what the first one already knows.
- B3. Configuration is formed once, at the initialization point, from a single source (settings). Never spread env reads or config-builder helpers across modules.
- B4. Coordination primitives (events, locks, retries, caches) are re-justified against the CURRENT execution model, not the historical one that created them.

### Family C — Types & Shapes (STRICT)

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

### Family D — Layers & Isolation (PARANOID DDD / HEXAGONAL)

[ref: #exist-layers-isolation]

- D1. The domain knows nothing of transport: no grpc/pb2/http/ORM imports in domain code. Dependencies point one way, inward. A leak (e.g. sqlalchemy in the grpc layer) is a blocking defect.
- D2. Each layer receives data in its own shape and never parses another layer's format: Timestamp at protocol, datetime in domain; domain models at business boundaries, primitives or named parameters at call sites.
- D3. App semantics never leak into shared libraries ("in the library it has decisively nothing to do"); library mechanics are never reimplemented in the app. Defects are fixed at the source repository, not worked around downstream.
- D4. Abstractions must not leak: internal state of a machine/module never escapes its boundary (a state machine's statuses are not other modules' constants). Cross-module, only the public interface exists.
- D5. Authorization lives at its designated layer; input validation happens exactly once, at the outer boundary — never repeated at lower levels.
- D6. Cross-service shared enums are fragile contracts (adding a value breaks every other service): prefer plain strings at protocol level.
- D7. No foreign types across package boundaries: driver/library types (db drivers, redis clients, httpx, pydantic, builtins) may exist INSIDE a package but NEVER cross its public boundary — domain types or sanitized values cross instead.
- D8. Async-first: all ports are `async`; sync adapters are wrapped, never the reverse. Carve-out: pure value providers (clocks, config) stay sync deliberately.

### Family E — Errors

[ref: #exist-errors]

- E1. Crash-loud at startup/config boundaries: "the process did not start, and that is correct." No cleanup theater before the process has even started.
- E2. One central error-mapping place (exception handler / interceptor). Local try/except is justified only where behavior genuinely differs.
- E3. Few error types; a new error class exists only with differentiated handling. Short message; details in extras.
- E4. No stringly-typed error matching, no reflection-driven dispatch, no class-level string tags checked elsewhere.
- E5. Errors carry a single machine vocabulary (a reason enum) consumed by ONE serializer; no other module references numeric codes directly. Every exception class name ends with `Error`.

### Family F — Naming & Vocabulary

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

### Family G — Flow & Readability

[ref: #exist-flow-readability]

- G1. Early return / fail-fast: negative scenarios first, happy path unnested.
- G2. One comprehension = one job: never query + parse + build in a single comprehension; separate the steps.
- G3. Code self-documents through structure; a comment block explaining requirements means the structure is wrong.
- G4. Related logic is co-located: a unified config is not exploded into sub-functions that force jump-driven reading.
- G5. Lifecycle symmetry: setup pairs with shutdown; initialization pairs with teardown.

### Family H — Local Development

[ref: #exist-local-development]

- H1. The service boots locally without infrastructure: literals, no-op implementations, empty config — no vault, no cache, no sidecars required.
- H2. Auth method/infra flavor is selectable via env (e.g. `*_AUTH_TYPE`) with production-shaped defaults; never fail-open defaults.
- H3. Required envs crash at import/startup with the variable named; a dev opt-in is always explicit, never a silent default.

### Family I — Migration & Legacy

[ref: #exist-migration-legacy]

- I1. Requirements are restated in the new world's terms. Schemes leaked from the old system (custom prefixes, legacy DSN formats, sidecar flows) die unless they re-earn their place.
- I2. One level of indirection needs a named, current consumer (rotation, multi-tenancy). Otherwise store the value directly (literal in DB, not a reference to a reference).
- I3. Validation is complete or absent: a regex that checks patterns checks ALL patterns — no regex plus manual patch-up checks.

### Family J — Logging & Observability

[ref: #exist-logging-observability]

- J1. Level discipline per entry; secrets/DSN/credentials are never logged — not even at debug (a debug toggle must never force a credential rotation).
- J2. Structured extras over f-strings in log calls; one log per event (no duplicate loggers reporting the same fact).
- J3. Operational logging belongs at the central handler/interceptor layer.
- J4. CLI logging goes to stderr; stdout is reserved for program output and protocol channels.

### Family K — Review-Answer Discipline (meta)

[ref: #exist-review-answer-discipline]

- K1. Facts before answers: read the library, run the code, check the corpus — then respond. Every reviewer question maps to either a change or a factual answer.
- K2. Trade-offs are surfaced explicitly (e.g. "this moves the failure from startup to request time"); the decision belongs to the user, never silently taken by the agent.
- K3. Deployment reality is part of scope: env renames require a manifest transition plan; DB-held values are migration inputs, not afterthoughts.
- K4. Library escalation (HARD): whenever a change needs a library in a place where it is banned, any new dependency, or any exemption — STOP and escalate to the user. Placement, workarounds, and exemptions are decided together, never unilaterally.

### Operating Workflow

[ref: #exist-operating-workflow]

0. As-is map: full diff vs base, every touched component, consumers per symbol (call sites, tests, manifests, DB data). Scale + overview tree. Gate: user approves the overview.
1. Top-down walkthrough, one level per message: per element — keep / revert / delete, justified by rule ids (A1–K4).
2. Pipeline traversal, forward and backward, after removals.
3. Final contour + master approval; blueprint recorded as a decision card.
4. Implementation exactly per contour; project lint/type/test gates green. Deliverables: minimal diff, keep/delete table, ready answers per reviewer question, follow-ups list.
