# Quality Checklists (repo-audit)

[ref: #ra-checklists]

## Pre-generation checks

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

After writing any memory:

- [ ] Verified and persisted per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).
- [ ] Do not report completion until persistence succeeds.
