# Validation checklist and edit rules

[ref: #smr-validate]

## Validation checklist

Before applying any subagent-proposed edit, the root agent MUST verify:

1. **Git metadata is fresh.**
   - `branch` matches `git rev-parse --abbrev-ref HEAD` in the chosen git source.
   - `commit` matches `git rev-parse --short HEAD`.
   - `committed_at` matches `git log -1 --format=%cd --date=iso-strict`,
     normalized to UTC `Z`.

2. **Every cited commit hash exists.**

   ```bash
   git -C <git-source> cat-file -t <hash>
   ```

   Must return `commit`.

3. **Every cited source file exists.**

   ```bash
   test -f <source-path> || test -d <source-path>
   ```

4. **Line ranges are in bounds (when given).**

   ```bash
   wc -l <source-file>
   ```

5. **No unresolved contradictions remain.**
   - Prefer newer memory over older memory.
   - Prefer `AGENTS.md` over session memory unless explicitly overridden.
   - If still unresolved, STOP and report to the user.

6. **Entity prerequisite is satisfied.**
   - Before writing any entity-scoped memory, `entities/<entity>` MUST exist.
   - If it does not exist, STOP and ask the user to create it via
     `project-audit`.

7. **Naming is compliant.**
   - Every directory segment and filename matches `^[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$`.
   - No hyphens, spaces, or consecutive/leading/trailing underscores.

8. **`write_memory` size.**
   - Any content written via `write_memory` MUST be under **25 KB**.
   - If larger, split, use `edit_memory`, or store the full artifact outside
     Serena memory.

## Edit rules

### Renaming non-compliant paths

Use the Serena MCP `rename_memory` tool. Compute the new name with the
normalization recipe from `[ref: #serena-naming]`:

1. Replace separators with `_`.
2. Remove non-allowed characters.
3. Strip leading/trailing underscores.
4. Collapse consecutive underscores.

Do not use raw filesystem `mv`.

### Header-only refresh

When the content is correct but the header is stale/legacy:

1. Determine the correct git source (`[ref: #smr-git-source]`).
2. Build a fresh YAML frontmatter block.
3. Preserve the exact H1 title and all content below it.
4. Replace the old header directly at `.serena/memories/<path>.md`.
5. Read the file back and run `just agent-memory-commit`.

### Full content rewrite

When the content needs to change:

1. Call `write_memory` with the complete new content.
2. Include a fresh YAML frontmatter block.
3. Update `updated_at` to the current UTC time.
4. Update `commit`, `branch`, and `committed_at` from the chosen git source.
5. Keep the payload under 25 KB.

### Appending to a memory

Use `edit_memory` with:

```json
{
  "mode": "regex",
  "needle": "\\Z",
  "repl": "\n\n## <New Section>\n<new content>"
}
```

Simultaneously refresh `updated_at` in the YAML frontmatter.

### Partial update

Use `edit_memory` with a precise regex that targets only the outdated paragraph
or table row. Refresh `updated_at` and, if the git state changed, `commit`,
`branch`, and `committed_at`.

### Routing new findings

Route each finding to exactly one namespace per `serena-protocol`
`[ref: #serena-findings-traceability]`:

| Finding kind | Target namespace |
|---|---|
| Broken or inconsistent behavior | `bugs/<entity>/<topic>` |
| Observation, caveat, surprising pattern | `notes/<entity>/<topic>` |
| Architectural decision or trade-off | `decisions/<entity>/<topic>` |
| Style convention or technical debt | `style/<entity>/<topic>` |
| Short actionable item from code/docs | `todo/<entity>/<topic>` |
| Business-domain insight | `logic/<entity>/<topic>` |

Every finding MUST include:

- Severity: `critical`, `warning`, or `info`.
- Location: `path/to/file.py:line_num`.
- Hash: `(commit <hash>)`.

## Persistence

After ANY memory mutation:

1. Read the memory back to verify it.
2. Run `just agent-memory-commit` from the workspace root.

The agent always persists automatically. Do not wait for manual user approval.
