---
subject: "Quality checklists; pre-generation checks, freshness gate, per-service card checks, exhaustive interface, downstream coverage, project-level checks, eight sections, taxonomy completeness, persistence checks, Mermaid validation, `repos/<repo>/dependencies`, secrets exclusion, notes presence, commit matching."
index:
  - anchor: ra-checklists
    what: "The quality checklists for all repo-audit modes: pre-generation, per-service, project-level, persistence."
    problem: "Artifacts save with missing sections and stale inputs; defects surface at consumption time far from run; late defects, quality absence, check skip, save roulette, section rot, input decay, consumption-time surprises, save gamble."
    use_when: "Before saving any artifact; before launching subagents; closing a run."
    avoid_when: "Subagent self-checks — `[ref: #ra-subagent-checklist]` owns those."
    expected: "Every artifact passes its checklist before saving."
  - anchor: ra-checklists-pregen
    what: "The pre-generation checks: one repo, cards exist, commits match HEAD, memory read for context, findings skimmed."
    problem: "Run launches with missing or stale inputs; subagents build on rotten or absent context and output garbage; freshness lapse, launch haste, input neglect, context decay, produce failure, baseline rot, effort waste, garbage cascade, launch sin."
    use_when: "Before any subagent launch in any mode; verifying freshness; confirming context was read."
    avoid_when: "Mode selection — `[ref: #ra-gates-mode]` owns that decision."
    expected: "Launch only with present, fresh, actually-read inputs."
  - anchor: ra-checklists-service
    what: "The per-service card checks: header completeness, exhaustive interface and downstream tables, concrete protocols, valid Mermaid, no secrets."
    problem: "Dependency card saves with partial interface and vague protocols; consumers trust incomplete maps; false trust, exhaustiveness breach, diagram rot, protocol fog, coverage lies, table gaps, consumer deception, map poverty, row neglect."
    use_when: "Before saving `repos/<repo>/dependencies.md`; validating exhaustiveness; reviewing diagram coverage."
    avoid_when: "Card template itself — `templates/dependencies_card.md` owns the layout."
    expected: "Card passes all rows: complete tables, protocols, diagram, no secrets."
  - anchor: ra-checklists-project
    what: "The project-level checks: explicit request, all cards fresh, `generic` repo value, eight sections, full taxonomy."
    problem: "Project overview saves from partial stale inputs; aggregate map misleads whole organization; org mislead, taxonomy gaps, premature save, aggregate rot, input decay, organization-wide deception, freshness breach, map decay, trust abuse, staleness spread."
    use_when: "Before saving `project/dependencies.md`; verifying freshness of every per-service card; checking taxonomy completeness."
    avoid_when: "Generation conditions themselves — `[ref: #ra-tpl-deps-project-when]` owns them."
    expected: "Overview passes all rows before saving."
  - anchor: ra-checklists-persistence
    what: "The persistence checks: read-back verification and successful checkpoint before reporting completion."
    problem: "Run reports done with unverified, unpersisted artifacts; next session rediscovers gap; completion lies, checkpoint debt, persistence doubt, verification lapse, durability gap, repeat work, trust abuse, finish-line fraud, memory decay, redo spiral."
    use_when: "After writing any memory; before reporting completion to the user."
    avoid_when: "The mutation protocol itself — `serena-protocol` `[ref: #serena-memory-mutation]` owns it."
    expected: "Every artifact verified and checkpointed before completion claims."
---

# Quality Checklists (repo-audit)

[ref: #ra-checklists]

## Pre-generation checks

[ref: #ra-checklists-pregen]

Before launching subagents, verify:

- [ ] Exactly one repo is selected for a per-service card.
- [ ] `repos/<repo>/overview` exists.
- [ ] `repos/<repo>/business` exists (warn if missing; do not
      block unless business context is essential).
- [ ] The `commit` in the frontmatter of `repos/<repo>/overview` matches the latest
      commit of the repo's own git repository.
- [ ] The `commit` in the frontmatter of `repos/<repo>/business`,
      `repos/<repo>/integrations`, and `repos/<repo>/processes` matches the
      repo HEAD.
- [ ] All input memories for the same repo reflect a consistent commit. If
      they differ, STOP and report the inconsistency.
- [ ] All memory paths comply with `[ref: #serena-naming]`.
- [ ] Existing `repos/<repo>/business` (and split files, if present) was READ for context — not only existence/freshness-checked.
- [ ] Existing findings (`bugs/<repo>/...`, `notes/<repo>/...`, `decisions/<repo>/...`, `style/<repo>/...`, `todo/<repo>/...`) were skimmed for business context.

If any freshness check fails, STOP and ask the user to reconcile via
`serena-audit` or to refresh the upstream cards before proceeding.

## Per-service card checks

[ref: #ra-checklists-service]

Before saving `repos/<repo>/dependencies.md`, verify:

- [ ] Frontmatter completeness and tracking fields per the frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`); H1 matches `title` per `markdown-protocol` §6; content quality per `entity-protocol` `[ref: #entity-card-quality]`.
- [ ] `repo` is the repo's own repository name (logical source of the commit).
- [ ] `source` lists the repo directory and the memory files used as input.
- [ ] Identity line is present and uses a canonical type.
- [ ] `Provided interface` table is exhaustive:
  - Every gRPC method.
  - Every REST endpoint.
  - Every Temporal workflow/activity/signal/query/update.
  - Every library public symbol.
  - Every GitOps HelmRelease/Kustomization.
- [ ] `Downstream dependencies` table is exhaustive:
  - Every downstream service call.
  - Every database.
  - Every cache/message broker.
  - Every external integration.
  - Every shared library.
  - Every infrastructure component (secrets, identity, orchestration).
- [ ] Every table row has a concrete protocol.
- [ ] Every table row has a one-line purpose.
- [ ] `Databases, external integrations, libraries, infrastructure` list is
      complete; `None` is explicitly stated where applicable.
- [ ] `Notes` include architectural observations, gaps, and contradictions.
- [ ] Mermaid diagram includes every upstream consumer and every downstream
      target from the tables.
- [ ] Mermaid syntax is valid.
- [ ] No secrets, env values, defaults, or examples are included.
- [ ] No tests, linters, CI, Makefile, Docker, or entry points are included
      unless they are actual runtime dependencies.

## Project-level card checks

[ref: #ra-checklists-project]

Before saving `project/dependencies.md`, verify:

- [ ] The user explicitly requested the project-level card.
- [ ] A `repos/<repo>/dependencies.md` card exists for **every** repo in
      `repos/`.
- [ ] Every per-service card is fresh (frontmatter commit matches repo
      HEAD).
- [ ] Frontmatter `repo` is `generic` (project-wide memory); tracking fields
      per the frontmatter-protocol tracking extension (`[ref: #tracking-fields]`);
      H1 matches `title` per `markdown-protocol` §6; content quality per
      `entity-protocol` `[ref: #entity-card-quality]`.
- [ ] Exactly the eight mandatory sections are present in the correct order.
- [ ] `Service taxonomy` includes every repo or explicitly notes skips.
- [ ] `Consumer/provider matrix` covers every documented provider.
- [ ] `External / infrastructure systems inventory` covers every external/infra
      system from the per-service cards.
- [ ] No method-level details appear outside references to
      `repos/<repo>/dependencies.md`.
- [ ] All timestamps are UTC ISO 8601 with a `Z` suffix.

## Persistence checks

[ref: #ra-checklists-persistence]

After writing any memory:

- [ ] Verified and persisted per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).
- [ ] Do not report completion until persistence succeeds.
