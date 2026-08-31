---
name: discuss-first
description: "Co-implementation mode: the agent never writes code without the user's explicit approval of the whole implementation blueprint. On activation, the agent studies the task, then walks the user through the implementation top-down — one level at a time, justifying every abstraction, class, method, and function, showing full signatures with pseudocode bodies — then traverses the entire information pipeline from the request entry point to the end and back, collects per-part approvals, requests the master approval of the final blueprint, and only then writes code strictly per the approved contract. Activate on user request ('пишем код вместе', 'ты не пишешь без меня', 'step-by-step', 'обсудим реализацию', etc.); the agent also proactively offers this mode before non-trivial code work: features, refactoring (including rewriting code the agent wrote itself), behavior-changing bugfixes, or any new function, method, class, or abstraction appearing in the plan. While the mode is active, a mandatory existence-review standard (the always-loaded `existence-bible` skill, rule ids A1–K4) governs every keep/revert/delete decision and overrides language style guides. The mode is session-scoped: no persistence, no resume — a new session starts without it. Every approval event is recorded to the owned Serena scope `solutions/<repo>/<subject>/` (the Solutions Journal, §13) via direct disk writes (owner ruling 2026-08-29)."
triggers:
  request: "пишем код вместе, пиши вместе со мной, ты не пишешь без меня, не пиши код без меня, всё обсуждаем, обсуждаем каждый шаг, обсудим реализацию, обсудим имплементацию, обсудим сам код, степ-бай-степ, step-by-step mode, пошаговый режим, discuss first, no code without approval, парное программирование, pair programming, давай реализовывать вместе"
  reason: "The user switches the session into co-implementation mode where every piece of code requires prior discussion and approval."
runtime: true
requires:
  - serena-protocol
version: 0.9.0
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
5. **Journal scope approval:** in the same overview-approval message the agent proposes the `<repo>` and `<subject>` of the Solutions Journal (§13); the user approves or corrects them together with the overview. The repo gate applies (entity-protocol `[ref: #entity-prerequisite]`): a concrete `<repo>` without a card at `repos/<repo>/overview` is a STOP-and-ask; the meta-entity `project` is exempt. On receiving the overview approval the agent immediately resolves the absolute journal path and writes `stages/begin.md` — before any further question, per the §13.5 order; no reminder is ever needed. A resumption re-approval (§9, §13.6) is the exception: it is recorded as a regular numbered card, never a second `begin.md`.
6. **Scale valve:** the collapse decision is a separate approval item, asked standalone per §1 AFTER the overview is approved. For `trivial`, the loop collapses to a single plan message with a single explicit approval ONLY when the user confirms the `trivial` classification; for `small`, the agent asks the collapse question («Схлопываем цикл в один план?») and the user decides. The scale is confirmed only by a reply that addresses the scale, and the overview-approval question MUST name the scale estimate explicitly. The collapsed loop is still the loop: explicit approval is required, and it authorizes only what the plan message stated.
7. **Every edit goes through the loop:** while the mode is active, even a one-character fix in code requires the (possibly collapsed) loop — there is no "too small to discuss" outside the valve.

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
4. On approval, the blueprint and the chosen implementation style are recorded as a decision card in Serena memory per `serena-protocol` `[ref: #serena-memory-mutation]` (scope `decisions/<repo>/<topic>`; artifact language English, per the workspace language rules). This card is an artifact, not mode state (§4), and it references the full approval trail via `mem:solutions/<repo>/<subject>/` (§13). The master approval round itself is recorded as a stage card and the finale files are written, per the §13 finalization.

## 9. Phase 4 — Contract Implementation

[ref: #df-phase-4]

- Code is written strictly per the approved blueprint: no new abstractions, no extra helpers, no silent renames or reshaping.
- **Baseline:** before the first code write of the implementation, the agent ensures a restorable baseline for every target file (git-tracked state or an explicit backup copy), so the violation protocol's revert obligation stays fulfillable.
- **Deviation handling:** on any deviation, the agent STOPS, presents the deviation as a blueprint delta, and obtains the user's explicit approval of that delta BEFORE touching code. Discussion alone never authorizes implementation. The approved delta is recorded as a fractional stage card (`NN_M_<topic>.md`) in the journal's `stages/` (§13); the decision card itself is never appended to mid-loop — it is updated only at finalization when a decision changed (§13).
- **Delegation:** while the mode is active, the prohibition covers ALL code production, including by subagents — no subagent, background task, or tool invocation may create or modify code before the master approval. After the master approval, any delegated implementation receives the approved blueprint verbatim as its contract, and deviations reported by a delegate are STOP-and-approve events for the main agent.
- The implementation style chosen in Phase 3 governs how much code is shown for approval; style (b) approvals happen per component, and the agent waits for each.
- **Deliverables:** a minimal diff; the keep/delete table with rule-id justifications; ready factual answers per anticipated reviewer question (K1); a follow-ups list (A4 extractions, K3 deployment notes).
- Each new task re-enters at Phase 0 with a fresh blueprint; a master approval never carries over.
- **User-initiated changes mid-implementation:** any user request to change already-approved or already-written code is treated as a deviation delta (STOP the affected component, present the delta, approve per this section) unless the user explicitly declares a scope change, which re-enters Phase 0. On any user «стоп» (or equivalent), the agent halts ALL code production until the user explicitly resumes.
- **Suspended loops:** if the user interrupts the loop with another task, the suspended blueprint retains its per-level approvals only when the user explicitly confirms resumption of the previously approved state; otherwise it re-enters at Phase 0 inside the SAME journal sequence (§13.6): an `NN_invalidation.md` card records the invalidation, the re-approved overview is a regular numbered card — never a second `begin.md`. Approvals never survive changes to the underlying code or requirements.

## 10. Refactoring and Bugfix Branch

[ref: #df-refactoring]

For work on existing code (refactoring, rewriting the agent's own earlier code, behavior-changing bugfixes), Phase 0 additionally produces the **as-is map**: the current flow, components, and their actual connections — covering every component and connection the to-be blueprint touches. The "to-be" blueprint is then discussed against this map, so the user sees exactly what changes and what stays. The as-is map is mandatory — never skip it, even when the agent wrote the original code itself.

## 11. Hard Rules

[ref: #df-hard-rules]

- NEVER write or edit code — directly or via delegates — before the master approval (Phases 0–3 complete).
- NEVER introduce an abstraction that was not justified and approved.
- NEVER skip the pipeline traversal or the as-is map where required.
- NEVER treat an ambiguous reply as approval, and NEVER treat a refused offer as permanent — re-offer per §3.
- NEVER let urgency suspend the gate: with any urgency, while the mode is ON it cannot be ignored — the fast path is the collapsed loop of §5.6, and if the agent is unsure whether anything changes, it asks the user explicitly.
- NEVER continue working while any approval question is pending: ask, STOP, and WAIT for the user's explicit reply.
- **Pre-response self-check:** while the mode is active, before every response the agent verifies: is any approval pending? Am I about to emit or produce code without master approval? If yes — stop and return to the gate.
- **Existence review (MANDATORY):** the Existence Bible is the always-loaded `existence-bible` skill (`existence-bible/SKILL.md`, `[ref: #existence-bible]`) — already in context from bootstrap, no re-read needed; while the mode is active, every keep/revert/delete decision and every abstraction justification cites the rule ids (A1–K4), and "why does this exist" outranks "is this correct". On conflict with language style guides (e.g. `python-lang` Google-style sections), the existence-review standard wins; it applies to all code.
- **Journal before the next question (§13):** while the mode is active, every approval event is recorded to the Solutions Journal — written and baked — BEFORE the next question or level is asked; a question is never asked while the previous round stands unrecorded.
- Discussion with the user is in Russian; recorded artifacts (decision cards, blueprints) are in technical English per the workspace language rules.

**Violation protocol:** if you produce code, add an abstraction, or proceed past any approval gate without the user's explicit approval while this mode is active: halt immediately; disclose the violation to the user in one line; discard the offending output and revert any file mutations made after the last approved point to their exact prior contents; resume the loop from the last approved point only after the user acknowledges.

## 12. Existence Bible
[ref: #existence-bible]

> **DEPRECATED 2026-08-31T20:55:01Z:** the Existence Bible moved to the standalone always-loaded skill `existence-bible/`; the rule ids A1–K4 and every `exist-*` anchor live there unchanged. See [ref: #existence-bible] in `existence-bible/SKILL.md`.

## 13. Solutions Journal

[ref: #df-solutions-journal]

While the mode is active, every approval event is recorded to the registered Serena memory scope `solutions/<repo>/<subject>/` (entity-protocol §5; owner: this skill) — immediately, without reminders — so that any agent can read the chain and continue from the exact stopping point. This section is the full contract of that journal.

**Transport: direct disk write, owner ruling 2026-08-29.** Cards are written straight to `<workspace-root>/.serena/memories/solutions/<repo>/<subject>/...` with one full-content `WriteFile` per card, deliberately bypassing the `serena-protocol` `[ref: #serena-memory-mutation]` write path (waiver recorded in `mem:agent/allowed_violations`). Everything else from `serena-protocol` stays in force: naming (`[ref: #serena-naming]`), the tracking header, one-topic granularity, the repo gate, and the scope registry.

### 13.1 Layout

- `solution.md` — the finale: problem, task, all approved decisions (the complete contract).
- `decisions.md` — every decision fork: options, what was chosen and why, what was rejected and why — complete enough for a future agent to re-think a decision.
- `stages/` — the per-round journal: `begin.md`, then `NN_<topic>.md` (two-digit event number, snake_case topic), with fractional `NN_M_<topic>.md` for re-approvals and deltas — `NN` is the last numbered card of the sequence, `M` increments per fractional event.
- The root of `<subject>/` holds ONLY the finale; every round card lives in `stages/`.

### 13.2 Card chain

- The first card of a sequence is `stages/begin.md` (approval event №1, `Previous: none`) — a fixed-name entry point, written at the Phase 0 overview approval (§5.5).
- Subsequent cards are numbered from `02_` in approval-event order, consecutive across the whole `<subject>` sequence, never reset inside it. If a sequence exceeds 99 events, widen to three digits from `100_` on — never renumber existing cards.
- Cards link BACKWARD only: each carries `Previous: ` + a `mem:solutions/<repo>/<subject>/stages/...` reference to the previous card. No next-links, no appends to existing stage cards — ever. The finale files and the ADR are not stage cards: they are written at finalization and batch-updated only per §13.6.
- One card = one approval event (a level, the traversal, the master approval, a delta, a per-component approval, a re-ask with a new decision). Never split a round across cards, never merge two rounds into one.

### 13.3 Card schema

Standard tracking header per `frontmatter-protocol` `[ref: #tracking-fields]` (the canonical assembled header lives there; zero journal-specific fields). Body, in this exact section order; an empty section is written as `- none` (a missing section reads as "forgotten", never as "nothing"):

```markdown
# Stage NN: <round topic>

Previous: `mem:solutions/<repo>/<subject>/stages/<prev>`
Session: <session-id>

## Approved

## Rationale

## Rejected

## Deferred

## Attention

## Next
```

- `Approved` — verbatim contract of the round (decisions, signatures, boundaries). `Rationale` — why. `Rejected` — each dropped variant with its reason. `Deferred` — what was postponed and where to. `Attention` — risks and open spots to watch. `Next` — the exact continuation point: the next open question, level, or pending approval event.
- `Session:` carries the current session's REAL id so a future agent can lift the raw transcript via session-inspector in a dispute. The id is obtained ONLY through the `session-inspector` skill's probe flow (`_on_demand/session-inspector/SKILL.md` `[ref: #si-tracking-flow]`, §7): if the id is not yet known in this conversation, the agent invents a probe UUID, publishes it explicitly in its visible reply or thinking (NO tool call in that step), then runs `track_session.py <probe>` in the next step and remembers the returned `session_id`. Resolution happens ONCE, before the first card (`begin.md`) is written; the remembered id is reused verbatim in every later card of the session. FORBIDDEN: inventing a random UUID and writing it as the session id (it matches nothing on disk), `python -c uuid` one-liners, shell variables. If the probe flow still fails after its documented retries, write `Session: unresolved` and note the failure in `Attention` — never leave a guessed value.
- Cards are self-sufficient about their own round but do not duplicate the whole task picture — that is what the chain and the finale are for.
- Artifact language: technical English.

### 13.4 Write mechanics

- The absolute journal path is resolved and fixed in Phase 0, at scope approval — before the first write.
- One card = one `WriteFile` with the full content (tracking header + all six sections). `edit_memory` and appends are forbidden, always.
- **Baking (per card, mandatory):** after the write, the card is read back once and checked; defects are thought through as a whole and fixed in ONE batch, with a second pass only to confirm the batch. The loop of a hundred back-and-forth edits with re-reads is forbidden.
- `just serena-checkpoint` runs after EVERY card, fire-and-forget: launch and move on, no waiting for the result; an overlapping or failed run is harmless — the next card's checkpoint picks up the same files.

### 13.5 Recording triggers and order

- Triggers: the Phase 0 overview approval (`begin.md`), every Phase 1 level approval, the traversal approval, the master approval, every Phase 4 delta and per-component approval, every ad-hoc exemption grant (§8.2), every re-ask that carries a new decision.
- Order inside a round: approval received → card written and baked → checkpoint → ONLY THEN the next question or level. A question is never asked while the previous round stands unrecorded (§11).

### 13.6 Lifecycle

- **New task** (§1, §9 re-entry): a new sequence — new `<subject>`, starting from `begin.md`. A scope change of the same task stays in the same sequence and is recorded as a delta card.
- **Suspension:** nothing extra is written — the last card's `Next:` IS the resume pointer; this is the answer to "the session died, start over": a new agent reads the chain to the last card and steps into its `Next:`.
- **Resumption** (§9 suspended loops): if the user confirms the previously approved state, continue from the last card's `Next:`. If not, the SAME sequence continues: an `NN_invalidation.md` card records what was invalidated and why, and the re-approved overview is recorded as a regular numbered card (never a second `begin.md`).
- **Finalization (at master approval), four steps:** (1) the master-approval stage card; (2) `solution.md` and `decisions.md`; (3) the self-contained ADR card in `decisions/<repo>/<topic>` (`<topic>` = the decision's own slug per serena-protocol naming, independent of `<subject>`) per `serena-protocol`, referencing `mem:solutions/<repo>/<subject>/`; (4) a read-back of the whole tree with single-batch fixes and a checkpoint. The finale is written before any code exists, so a session dying mid-implementation still leaves the complete contract; Phase-4 deltas batch-update it per the next bullet.
- **Phase 4 deltas:** if any delta cards appeared during implementation, then at Phase 4 completion `solution.md`, `decisions.md`, and the ADR are updated in ONE batch, followed by a final read-back and checkpoint. No deltas — nothing is touched.
- **Exit before finalization:** the sequence stays as-is, the finale is not written, no cleanup; the last card with its `Next:` is an honest snapshot of an unfinished discussion.
- **Cancelled discussion:** a final card with status `abandoned` in `Attention`, so no future agent mistakes the chain for a live contract.
- **Feature closing:** when the feature this journal belongs to is closed, the whole `solutions/<repo>/<subject>/` sequence is part of the feature's archival footprint (produced-by class) and is archived by the on-demand `feature-archival` skill (`[ref: #fa-pipeline]`); the chain survives in git per that skill's recovery recipe.
