# ruplacer

> Find-replace source files. Respects `.gitignore`. Dry-run default.

## Why Agent Must Use ruplacer

- ruplacer = single tool for search + replace across entire codebase.
- Dry-run by default. Safe by design. No accidental writes.
- Respects `.gitignore` out of box. Skips binaries and non-UTF-8 auto.
- Supports regex, literal strings, whole-word, case-preserving, file-type filtering.
- Perfect for bulk refactors, renames, migration scripts, deprecation cleanups.

## Absolute Rule: DRY RUN First, Always
[ref: #ruplacer-dry-run]

- **NEVER** use `--go` on first invocation. Never.
- Step 1: run without `--go`. Review diffs on stdout.
- Step 2: verify zero side effects. Check file list, check replacement scope.
- Step 3: only after full verification, append `--go` and re-run.
- Violation = protocol breach. No exceptions. Not even for "trivial" one-liners.

## Form

```
ruplacer <PATTERN> <REPLACEMENT> [PATH]
```

- `PATH` defaults cwd.
- No `--go` = dry run only. Prints diffs. Zero writes.
- Quote args in shell. Protects `$` and special chars.

## Tier 1 — Daily Use

| flag | action |
|------|--------|
| `--go` | **Write to disk.** Only flag that mutates files. |
| `--no-regex` | Literal string match. No regex engine. |
| `--word-regex` / `-w` | Whole-word match only. `\b` semantics. |
| `--preserve-case` | One pass replaces `FooBar` → `SpamEggs` and `foo_bar` → `spam_eggs`. |
| `--type <t...>` / `-t` | Only scan matching file types or globs. Multiple OK. |
| `--type-not <t...>` / `-T` | Skip matching file types or globs. |

## Tier 2 — Often Use

| flag | action |
|------|--------|
| `--hidden` | Scan dotfiles. Default: skipped. |
| `--ignored` | Scan `.gitignore`d files. Default: skipped. |
| `--type-list` | Dump known file types. Exit. |
| `--quiet` | Silent except errors. |
| `--color <when>` | `always` / `auto` / `never`. Default `auto`. |
| `--allow-empty` / `-e` | Exit 0 on zero matches. |
| `-h, --help` | Help text. |
| `-V, --version` | Version string. |

## Regex Notes

- Default: Rust regex.
- Capture groups: `$1`, `$2`, … in replacement.
- No lookaround. No backreferences.
- Pattern starts with `-`? Prefix `--` (e.g. `-- --foo --bar`).

## Examples
[ref: #ruplacer-examples]

```bash
# dry run first — ALWAYS
ruplacer 'console\.log' 'logger.debug' src/

# verify output. then write changes
ruplacer --go 'console\.log' 'logger.debug' src/

# literal replace
ruplacer --no-regex --go 'TODO' 'FIXME' .

# whole word
ruplacer -w --go 'oldName' 'newName' .

# case preserve
ruplacer --preserve-case --go 'FooBar' 'SpamEggs' .

# only rust + py
ruplacer -t rust py --go 'foo' 'bar' .

# skip md + json
ruplacer -T md json --go 'foo' 'bar' .

# include hidden + ignored
ruplacer --hidden --ignored --go 'foo' 'bar' .

# capture groups
ruplacer --go '(\w+), (\w+)' '$2 $1' .

# CI quiet run
ruplacer --go --quiet --allow-empty 'foo' 'bar' .
```

## Symbol Renaming and Naming Collision Prevention
[ref: #ruplacer-rename-collision-check]

**HARD RULE for any rename-like operation:**
Before running `ruplacer` with a replacement name — even as a dry run — you MUST verify with `rg` that the replacement name is not already used anywhere in the codebase.

**Execution:**
1. Run `rg -n '<new_name>'` across the project.
2. If `rg` returns any matches, the new name is already in use.
3. Do NOT proceed with `ruplacer`.
4. Either choose a different name and repeat the check, or stop and inform the user.

**Why this is mandatory:**
If the replacement name already exists, `ruplacer` will merge two distinct symbols into one, creating naming collisions that break code, tests, and business logic.
This damage is often silent and extremely hard to undo.

**Tool hierarchy for renaming:**

- **Global renames** (across documentation, configuration, strings, multiple file types, or non-code content): use `ruplacer` directly.
- **Code symbol renames** (functions, classes, methods, variables, fields, etc.): first try the Serena `rename_symbol` tool. Fall back to `ruplacer` only when Serena cannot handle the target language or symbol.
- **Never use `sed`, `awk`, or similar text tools for any rename.** They are not symbol-aware and are forbidden for rename operations.

**Exception:**
You MAY proceed without the collision check only when you are intentionally renaming an entity to a universally accepted, exact same term AND you have received explicit, full approval from the user after explaining the full scope and consequences of the rename.

## Safety Rules

- Binary files skipped auto.
- Non-UTF-8 text skipped auto.
- `--go` = sole write trigger. Without it, filesystem read-only.
- Dry-run diffs to stdout for review before `--go`.
- **Mandatory workflow: dry run → inspect → `--go`. No skips.**
