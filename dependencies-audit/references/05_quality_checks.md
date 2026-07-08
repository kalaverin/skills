[ref: #dcc-quality]

# Dependency card creator: quality checks

## Pre-generation checks

Before launching subagents, verify:

- [ ] Exactly one entity is selected for a per-service card.
- [ ] `entities/<entity>` exists.
- [ ] `logic/<entity>/business_domain_report` exists (warn if missing; do not
      block unless business context is essential).
- [ ] The `commit` in the frontmatter of `entities/<entity>` matches the latest
      commit of the entity's own git repository.
- [ ] The `commit` in the frontmatter of `logic/<entity>/business_domain_report`,
      `logic/<entity>/integrations`, and `logic/<entity>/processes` matches the
      entity repo HEAD.
- [ ] All input memories for the same entity reflect a consistent commit. If
      they differ, STOP and report the inconsistency.
- [ ] All memory paths comply with `[ref: #serena-naming]`.

If any freshness check fails, STOP and ask the user to reconcile via
`serena-audit` or to refresh the upstream cards before proceeding.

## Per-service card checks

Before saving `logic/<entity>/dependencies.md`, verify:

- [ ] YAML frontmatter has all 8 required fields and matches `[ref: #serena-metadata]`.
- [ ] `repo` is the entity's own repository name (logical source of the commit).
- [ ] `source` lists the entity directory and the memory files used as input.
- [ ] H1 title matches `title` in frontmatter.
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
- [ ] A `logic/<entity>/dependencies.md` card exists for **every** entity in
      `entities/`.
- [ ] Every per-service card is fresh (frontmatter commit matches entity repo
      HEAD).
- [ ] YAML frontmatter has all 8 required fields; `repo` is `serena`.
- [ ] H1 title matches `title` in frontmatter.
- [ ] Exactly the eight mandatory sections are present in the correct order.
- [ ] `Service taxonomy` includes every entity or explicitly notes skips.
- [ ] `Consumer/provider matrix` covers every documented provider.
- [ ] `External / infrastructure systems inventory` covers every external/infra
      system from the per-service cards.
- [ ] No method-level details appear outside references to
      `logic/<entity>/dependencies.md`.
- [ ] All timestamps are UTC ISO 8601 with a `Z` suffix.

## Persistence checks

After writing any memory:

- [ ] Read the memory back to verify it was written correctly.
- [ ] Run `just serena-checkpoint` from the project root.
- [ ] Do not report completion until persistence succeeds.
