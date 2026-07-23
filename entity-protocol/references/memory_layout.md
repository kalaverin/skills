---
subject: "Canonical repos memory layout and legacy migration; `repos/<repo>/overview` card path, business split-model subfiles, glossary, dependencies, `project/repos` registry rename, reserved `cards/` scope, ruplacer link refresh, ordering hazard, frontmatter refresh, design decisions, path contract."
index:
  - anchor: entity-memory-layout
    what: "The canonical `repos/` directory contract fixing every per-repo artifact path and the design decisions behind it."
    problem: "Agents scatter repo analysis across ad-hoc paths; cards, reports, glossaries land inconsistently and gates cannot find them; path chaos, layout drift, scattered artifacts, broken gates, unpredictable locations, reserved-name misuse, lookup friction."
    use_when: "Creating or locating any per-repo artifact; checking where card, business report, split files, glossary, dependencies live; reviewing layout decisions."
    avoid_when: "Scope routing beyond `repos/` — `[ref: #entity-namespace-registry]`; physical moves from legacy scopes — sibling anchor below."
    expected: "Every artifact sits at its canonical path under `repos/<repo>/`."
  - anchor: entity-migration-legacy
    what: "The binding physical migration procedure from legacy `entities/` + `logic/` scopes: file moves, ordered `rup` link-refresh commands, and the double-rewrite ordering hazard."
    problem: "Host repositories still carry legacy scopes; careless bulk rewrites double-rewrite paths into `repos/<x>/repos/<name>` and destroy links; outdated layout, link rot, ordering trap, migration hazard, stale frontmatter, cutover, backlog item, dry-run discipline."
    use_when: "Migrating `.serena/memories/` of any host repository; refreshing links after file moves; executing backlog F20."
    avoid_when: "Fresh workspaces without legacy scopes; layout rules for new artifacts — anchor above."
    expected: "All memories and links under canonical `repos/` paths, frontmatter refreshed, checkpoint committed."
---

# Memory Layout and Legacy Migration (entity-protocol reference)

The canonical `repos/` memory layout and the migration procedure from the legacy `entities/` + `logic/` scopes. Loaded lazily via the routing index in `entity-protocol/SKILL.md`.

## Canonical Memory Layout

[ref: #entity-memory-layout]

The unified per-repo scope is `repos/`. All repo analysis lives under it:

```text
repos/<repo>/overview.md              # technical card (legacy: entities/<repo>)
repos/<repo>/business.md              # business analysis report (legacy: logic/<repo>/business_domain_report); single model or executive summary of the split model
repos/<repo>/entities/<name>.md       # split-model business entities (legacy: logic/<repo>/entities/<name>)
repos/<repo>/processes/<name>.md      # split-model processes (legacy: logic/<repo>/processes/<name>)
repos/<repo>/rules/<topic>.md         # split-model rules (legacy: logic/<repo>/rules/<topic>)
repos/<repo>/integrations/<topic>.md  # split-model integrations (legacy: logic/<repo>/integrations/<topic>)
repos/<repo>/risks/<topic>.md         # split-model risks (legacy: logic/<repo>/risks/<topic>)
repos/<repo>/glossary.md              # repo glossary (legacy: logic/<repo>/glossary)
repos/<repo>/dependencies.md          # dependency card (legacy: logic/<repo>/dependencies)
```

Decisions behind the layout:

- The card lives INSIDE the repo directory as `repos/<repo>/overview.md`; the prerequisite gate (`[ref: #entity-prerequisite]`) checks `repos/<repo>/overview`.
- The name registry is renamed: `project/entities` → `project/repos`.
- Project scope otherwise unchanged: `project/glossary`, `project/dependencies` stay.
- Findings scopes (`bugs|notes|decisions|style|todo|plans|proposals|reports/<repo>/...`) stay as-is; they are shared across all skills, not audit-owned.
- The scope name `cards/` is RESERVED for future use — never use it.

## Migration from Legacy

[ref: #entity-migration-legacy]

Physical memory migration in each host repository, executed by the agent when working with that repository. The detailed ordered plan is tracked as backlog F20; this section is the binding summary.

**File moves (inside `.serena/memories/`):**

- `entities/<x>.md` → `repos/<x>/overview.md`
- `logic/<x>/business_domain_report.md` → `repos/<x>/business.md`
- `logic/<x>/**` → `repos/<x>/**` (all remaining files keep their relative names)
- `project/entities.md` → `project/repos.md`

**Link refresh across ALL memory files** (ruplacer; ALWAYS dry-run first without `--go`, review stdout, then re-run with `--go`):

```bash
rup --no-regex 'logic/' 'repos/' .serena/memories/
rup --no-regex 'project/entities' 'project/repos' .serena/memories/
rup --no-regex 'business_domain_report' 'business' .serena/memories/
rup --no-regex 'entities/' 'repos/' .serena/memories/
```

**Ordering hazard:** run `logic/` → `repos/` BEFORE any `entities/` replacement, otherwise business-entity subpaths (`logic/<x>/entities/<name>` → `repos/<x>/entities/<name>`) get double-rewritten into `repos/<x>/repos/<name>`. The `entities/` pass must run LAST and must be reviewed carefully in dry-run output because after the first pass it matches both legacy card references and the new business-entity subdirectories.

**After migration:** refresh the YAML frontmatter of every touched memory and verify + persist per the mutation protocol (`serena-protocol` `[ref: #serena-memory-mutation]`).

**Post-migration verification:** `rg -l 'entities/|logic/' .serena/memories/` — expected: no live references outside deliberately kept historical records; spot-check that every moved file exists at its new `repos/` path and that every cross-memory link resolves.
