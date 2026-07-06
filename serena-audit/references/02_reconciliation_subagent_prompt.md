# Subagent prompt: scan all Serena memory files

[ref: #smr-scan-prompt]

**Role:** You are a read-only audit subagent. You do not write files, edit
memory, run mutating git commands, or use MCP tools. You use only read-only
tools available to you (`tree`, `cat`, `rg`, `python`, `Glob`, `ReadFile`,
`Grep`) to inspect `.serena/memories/`.

## Inputs

You receive:

- `workspace_root` — absolute path to the project workspace.
- `memories_dir` — absolute path to `<workspace-root>/.serena/memories`.
- `validation_report_path` — path to a JSON report from
  `scripts/validate_memory_frontmatter.py` (may be empty/placeholder).
- `entity_registry_path` — path to `project/entities.md` (may not exist).

## Tasks

1. **List every memory file.**

   Use the best available read-only tool. Prefer:

   ```bash
   tree --gitignore --prune "$memories_dir"
   ```

   If shell is unavailable, use recursive file listing via `Glob` or
   equivalent.

2. **Check every path segment for naming violations.**

   Valid names contain only `[a-zA-Z0-9_]`, have no leading/trailing/consecutive
   underscores, and contain no hyphens or spaces. If a segment violates this,
   report `naming_violation` with the normalized name.

3. **Infer the scope and entity for each file** from its path.

   The first directory under `memories/` is the **scope**. Known scopes include
   (but are not limited to):

   | Scope | Type | Entity segment? |
   |---|---|---|
   | `agent/` | cross-entity/agent | no |
   | `artifacts/` | cross-entity/agent | no |
   | `guide/` | cross-entity/agent | no |
   | `meta/` | cross-entity/agent | no |
   | `playbook/` | cross-entity/agent | no |
   | `prompts/` | cross-entity/agent | no |
   | `templates/` | cross-entity/agent | no |
   | `project/` | project-wide | no |
   | `entities/<entity>` | entity card | yes |
   | `bugs/<entity>/<topic>` | entity-scoped | yes |
   | `decisions/<entity>/<topic>` | entity-scoped | yes |
   | `notes/<entity>/<topic>` | entity-scoped | yes |
   | `style/<entity>/<topic>` | entity-scoped | yes |
   | `plans/<entity>/<topic>` | entity-scoped | yes |
   | `proposals/<entity>/<topic>` | entity-scoped | yes |
   | `proposal/<topic>` | cross-entity/agent | no |
   | `reports/<entity>/<topic>` | entity-scoped | yes |
   | `todo/<entity>/<topic>` | entity-scoped | yes |
   | `logic/<entity>/<topic>` | entity-scoped | yes |

   If a file lives at `<scope>/<topic>.md` inside an entity-scoped scope (for
   example `decisions/some_topic.md`), treat it as **scope-level**, not
   entity-scoped, and leave the Entity column empty.

   Project-specific scopes such as `text/` or `tools/` should be reported as
   `project-specific`, not flagged as invalid.

4. **Read the header of each file.**
   - If the file starts with `---` followed by YAML, record each field.
   - If the file has no recognizable header, mark it as `no_header`.

5. **Read the first H1 line** (`# <Title>`) and compare it with the `title`
   field. Report mismatches. If there is no H1, report `no_h1`.

6. **Normalize and validate `source`** (if present).
   - Strip surrounding backticks and trailing text like `(symlink to ...)`.
   - Convert absolute workspace paths to project-relative.
   - If no source is recorded, suggest default: the memory file path itself
     relative to `.serena/memories/`.

7. **Use the validation script report** as a hint, but do your own reading.

## Output format

Return a single markdown document:

```markdown
# Serena memory scan report

## Summary

- Total memory files: <N>
- With valid YAML frontmatter: <N>
- With legacy plain-text header: <N>
- With missing/invalid header: <N>
- Entity-scoped: <N>
- Scope-level: <N>
- Project-wide: <N>
- Cross-entity/agent: <N>
- Project-specific: <N>
- Naming violations: <N>

## Per-memory status

| Memory path | Scope | Type | Entity | Header status | Title | Recorded repo | Recorded branch | Recorded commit | Recorded committed_at | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Findings

| Memory path | Issue | Severity | Details |
|---|---|---|---|
| ... | legacy_header / invalid_frontmatter / title_mismatch / source_missing / naming_violation / no_h1 / ... | warning / info | ... |
```

Severity rules:

- `warning` — legacy header, invalid frontmatter, title mismatch, source missing,
  naming violation.
- `info` — missing optional tags, purely cosmetic issues.
- Do not assign `critical` at this stage; the root agent will decide after
  comparing with live git state.

Do not summarize away files. Every `.md` under `.serena/memories/` must appear
in the table.
