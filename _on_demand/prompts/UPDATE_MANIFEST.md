# Prompt: Update the On-Demand Skill Manifest
[ref: #update-manifest-intro]

This prompt owns the canonical procedure for regenerating `_on_demand/SKILL.md` after any change to the `_on_demand/<skill>/` directory tree or to the manifest schema. It is the single source of truth for the update ritual; do not invent shortcuts.

## When to run
[ref: #update-manifest-when]

Run this procedure when:

- A skill is added to, removed from, or moved within `_on_demand/`.
- An on-demand skill's frontmatter triggers, `runtime` flag, `description`, or `name` changes.
- The manifest schema changes (for example, the `ondemand:` entry shape is simplified or extended).

## Procedure
[ref: #update-manifest-procedure]

1. **Harvest.** From the repository root, generate the raw manifest from every `_on_demand/<skill>/SKILL.md` frontmatter:

   ```bash
   uv run --no-project --with pyyaml python _on_demand/scripts/harvest_manifest.py
   ```

   This writes `.tmp/_on_demand/.manifest.raw.yaml`. Each entry contains `name`, `description`, `triggers`, and optionally `runtime`. There is NO `path` field; `name` is the canonical directory name and must stay equal to the directory name.

2. **Compress (optional but recommended).** Produce `.tmp/_on_demand/.manifest.compressed.yaml`. Compression is needed when the generated frontmatter exceeds **100 lines or 8 KB**. If it is below both thresholds, copy the raw file directly. When compressing, use a subagent to shorten each `description` while preserving:

   - the skill's purpose;
   - the trigger keywords and conditions;
   - the `runtime` flag, if present;
   - the absence of a `path` field.

   The compression may be performed by a subagent tasked with "compress these descriptions without losing trigger semantics". Review the compressed file before applying it.

   If no compression is needed, copy the raw file directly:

   ```bash
   cp .tmp/_on_demand/.manifest.raw.yaml .tmp/_on_demand/.manifest.compressed.yaml
   ```

3. **Apply.** From the repository root, read `.tmp/_on_demand/.manifest.compressed.yaml` and write the final `_on_demand/SKILL.md`:

   ```bash
   uv run --no-project --with pyyaml python _on_demand/scripts/apply_manifest.py
   ```

4. **Lint.** Run Ruff on the helper scripts if you touched them:

   ```bash
   ruff check _on_demand/scripts/harvest_manifest.py _on_demand/scripts/apply_manifest.py
   ruff format _on_demand/scripts/harvest_manifest.py _on_demand/scripts/apply_manifest.py
   ```

5. **Verify discovery.** Confirm that `_on_demand/SKILL.md` is discovered and contains the expected entries, and that `_drafts/` skills remain excluded. Use the active skill tree (`.kimi/skills/` when it is the live runtime tree, otherwise `.kimi/mirror/`):

   ```bash
   SKILL_ROOTS=".kimi/skills"
   [ -L .kimi/skills ] || SKILL_ROOTS=".kimi/mirror"
   fd -t f SKILL.md $SKILL_ROOTS \
     --exclude '_on_demand/*/SKILL.md' \
     --exclude '_drafts/*/SKILL.md' \
     2>/dev/null | LC_ALL=C sort -u | while IFS= read -r f; do
       printf '\n### %s\n' "$f"
       awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"
   done
   ```

   Inspect the output for `name: ondemand` and the expected `ondemand:` entry list. After a successful update you may delete `.tmp/_on_demand/.manifest.raw.yaml` and `.tmp/_on_demand/.manifest.compressed.yaml` if you do not want to keep them.

## Constraints
[ref: #update-manifest-constraints]

- Never add a `path` field to an `ondemand:` entry. `name` is the directory name; duplicating it as `path` is forbidden.
- Never drop a trigger keyword or condition during compression.
- Never change the `runtime` flag value.
- Do not edit `_on_demand/SKILL.md` by hand; always regenerate it through the scripts so the body table stays consistent with the frontmatter.
- Do not commit the manifest update without running the verification step.
