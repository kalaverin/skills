# ripgrep (rg) Agent Skill

**Scope:** This skill governs all agent use of the `rg` (ripgrep) command-line search tool.

## Default Behavior

When invoked as `rg PATTERN`, ripgrep **recursively** searches the current directory for lines matching a regex pattern. By default it:

- Respects `.gitignore`, `.ignore`, and `.rgignore` rules.
- Skips hidden files and directories.
- Skips binary files.
- Enables line numbers and colorized headings when stdout is a TTY.
- Uses multiple threads automatically.

Do not assume recursive search must be explicitly enabled — it is the default.

## Agent Decision Rules

1. **Prefer `rg` over `grep`**. `rg` is faster, recursive by default, and respects ignore files.
2. **Use `-F`** when searching for literal strings that may contain regex metacharacters (dots, brackets, asterisks).
3. **Use `-t` or `-g`** to narrow scope before adding complex patterns — this improves speed dramatically.
4. **Use `-l`** when you only need filenames; it short-circuits per file after the first match.
5. **Do not use `-a` casually** — it can dump binary garbage to the terminal.
6. **For scripting / parsing**, disable colors and headings: `--color=never --no-heading`.
7. **Respect `.gitignore` by default**. Only override with `-u` / `--no-ignore` when the user explicitly asks to search ignored files.

## Agent Index — Mandatory Lookups by Task

| Trigger / Situation | Section |
|---|---|
| Need to search for a literal string containing regex metacharacters. | **Match Control** |
| Need to search across multiple lines or use look-around. | **Match Control** |
| Need to restrict search to specific file types or globs. | **Filtering and Scope** |
| Need to list only filenames, count matches, or format output for editors. | **Output Modes** |
| Need to control how filenames, headings, or colors are displayed. | **File Presentation and Colors** |
| Search is slow or needs to traverse ignored/hidden files. | **Filter Overrides** |
| Need to sort results or tune performance. | **Execution and Performance** |
| Need to search inside compressed files or preprocess content. | **Archive and Preprocessing** |
| Need to debug why ripgrep is not finding expected matches. | **Diagnostics and Meta** |

## Basic Search Patterns

- `rg PATTERN [PATH...]` — Default regex search. `PATH` may be files or directories.
- `rg -e PATTERN` — Explicit pattern flag. **Use this** when the pattern starts with a dash.
- `rg -f FILE` — Read patterns from `FILE`, one per line.
- `rg --files` — List all files that would be searched (respects filters). Useful for piping.
- `command | rg PATTERN` — Pipe mode. Search stdin instead of files.

## Output Modes
[ref: #rg-output-modes]

| Flag | Effect |
|---|---|
| `--json` | Output matches as JSON lines. |
| `-l` | Print only filenames with matches. |
| `--files-without-match` | Print only filenames with **no** matches. |
| `-c, --count, --count-matches` | Print match count per file. |
| `--include-zero` | With `-c`, also print files with zero matches. |
| `-o, --only-matching` | Print only the matching portion of each line. |
| `-n, --line-number` | Show line numbers (default in TTY). |
| `-N, --no-line-number` | Suppress line numbers. |
| `--column` | Show column numbers (1-based byte offset). |
| `-b, --byte-offset` | Show byte offset of each match. |
| `-C NUM, --context NUM` | Show `NUM` lines of context around each match. |
| `-A NUM, --after-context NUM` | Show `NUM` lines after each match. |
| `-B NUM, --before-context NUM` | Show `NUM` lines before each match. |
| `--passthru` | Print all lines, highlighting matches. Overrides context flags. |
| `--trim` | Trim leading whitespace from matching lines. |
| `-0, --null` | Use NUL as line terminator (useful with `xargs -0`). |
| `--vimgrep` | Output in vim-friendly format (one match per line). |
| `-q, --quiet` | Suppress all output. Exit 0 if any match, else 1. |

## File Presentation and Colors

| Flag | Effect |
|---|---|
| `-H, --with-filename` | Prefix each match with the filename. Default when searching multiple files or recursively. |
| `-I, --no-filename` | Never prefix matches with the filename. Default when searching stdin. |
| `--heading` | Group matches by file path with heading (default TTY). |
| `--no-heading` | Prefix every line with `path:line:col:`. |
| `-p, --pretty` | Force pretty-printing: enable colors, headings, and line numbers even when stdout is not a TTY. |
| `--context-separator SEP` | String separating non-contiguous context blocks. Default `--`. |
| `--field-context-separator SEP` | Separator for contextual line fields. Default `-`. |
| `--field-match-separator SEP` | Separator for matching line fields. Default `:`. |

## Match Control

| Flag | Effect |
|---|---|
| `-i, --ignore-case` | Case-insensitive search. |
| `-s, --case-sensitive` | Case-sensitive search (default). |
| `-S, --smart-case` | Smart case: insensitive if pattern is all lowercase. |
| `-F, --fixed-strings` | Fixed strings — treat pattern as literal, not regex. |
| `-v, --invert-match` | Invert match: print non-matching lines. |
| `-w, --word-regexp` | Word regexp: match only whole words. |
| `-x, --line-regexp` | Line regexp: match only whole lines. |
| `-m NUM, --max-count NUM` | Stop after `NUM` matches per file. |
| `-U, --multiline` | Multiline search (allows `\n` in matches). |
| `--multiline-dotall` | With `-U`, make `.` match newlines. |
| `-P, --pcre2` | Use PCRE2 engine (supports look-around, backreferences). |
| `--engine ENGINE` | Choose regex engine: `default`, `pcre2`, `auto`. |
| `--no-unicode` | Disable Unicode mode. ASCII-only regex, smaller character classes. |
| `--null-data` | Use NUL as line terminator instead of `\n`. |
| `--stop-on-nonmatch` | Stop reading a file after first non-matching line following a match. |

## Filtering and Scope

| Flag | Effect |
|---|---|
| `-t TYPE, --type TYPE` | Search only files matching `TYPE` (e.g., `-t py`). Use `--type-list` to see available types. |
| `-T TYPE, --type-not TYPE` | Exclude files matching `TYPE`. |
| `--type-add TYPESPEC` | Add a custom glob for a file type. Example: `--type-add 'src:*.src' -tsrc`. |
| `--type-clear TYPE` | Clear globs for a file type. |
| `-g GLOB, --glob GLOB` | Include/exclude via glob (`!` prefix to exclude). Overrides ignore logic. |
| `--iglob GLOB` | Case-insensitive glob. |
| `--glob-case-insensitive` | Process all `-g` globs case-insensitively. |
| `-d NUM, --max-depth NUM` | Limit recursion depth. `0` = do not descend. |
| `--max-filesize SIZE` | Skip files larger than `SIZE` (e.g., `50M`). |
| `-L, --follow` | Follow symbolic links. |
| `--one-file-system` | Do not cross filesystem boundaries. |
| `--ignore-file PATH` | Add a custom ignore file in `.gitignore` format. |
| `--ignore-file-case-insensitive` | Process ignore files case-insensitively. |

## Filter Overrides

| Flag | Effect |
|---|---|
| `--no-ignore` | Ignore `.gitignore` / `.ignore` / `.rgignore`. |
| `--no-ignore-files` | Ignore `--ignore-file` flags. |
| `-u, --unrestricted` | Alias for `--no-ignore`. |
| `-uu` | `--no-ignore` + search hidden files (`--hidden`). |
| `-uuu` | Above + search binary files (`--binary`). |
| `--hidden, -.` | Search hidden files/directories. |

## Archive and Preprocessing

| Flag | Effect |
|---|---|
| `--pre CMD` | Run `CMD` on each file and search its stdout. |
| `--pre-glob GLOB` | Limit `--pre` to files matching glob. |

## Execution and Performance

| Flag | Effect |
|---|---|
| `--sort SORTBY` | Sort results by `path`, `modified`, `accessed`, `created`, or `none`. |
| `--sortr SORTBY` | Sort results in reverse order. |
| `--stats` | Print search statistics after results. |
| `--max-columns-preview` | When truncating long lines, show a preview of the match. |

## Advanced Search Engine

| Flag | Effect |
|---|---|
| `-E ENCODING, --encoding ENCODING` | Set text encoding. Default `auto` (sniffs UTF-8/UTF-16 BOM only). Use `none` for raw bytes. |

## Agent Recipes
[ref: #rg-agent-recipes]

Daily commands for code work.

```bash
# find function definition across codebase
rg "^\s*fn\s+foo" src/

# find all imports of a module
rg "^use\s+crate::auth" src/

# find where variable is used. only filenames.
rg -l "user_session" src/

# literal search. no regex escape hell.
rg -F "config[\"host\"]" src/

# search specific file type only
rg -t rust "TODO|FIXME|HACK"

# exclude tests from search
rg -T rusttest "unwrap()" src/

# find all files that import serde. machine output.
rg -l -t rust "use serde" | sort -u

# search with context. see surrounding lines.
rg -C 3 "panic!(" src/

# find and replace preview. dry run first.
# (ripgrep has no replace. pipe to sed or use ruplacer.)
# but ripgrep finds targets:
rg -n "old_function_name" src/

# check if pattern exists anywhere. quiet mode.
rg -q "deprecated_api" src/ && echo "found" || echo "clean"

# find unused imports by cross-referencing
rg -l "use crate::old_module" src/ | while read f; do
  name=$(basename old_module)
  rg -q "\b$name\b" "$f" || echo "$f"
done

# json output for parsing
rg --json -n "error" src/ | jq -s '.[] | select(.type=="match")'

# multiline search. find struct + derive
rg -U "#\[derive\(.*Serialize" src/

# word boundary search. exact identifier match.
rg -w "id" src/  # matches 'id', not 'uuid' or 'hidden'

# invert match. find lines without logging.
rg -v "tracing::|log::|println!" src/

# search in hidden files too
rg --hidden "API_KEY" .

# search ignored files (node_modules, vendor)
rg -u "jquery" .

# find large files first to avoid slow search
rg --max-filesize 10M "pattern" src/

# pcre2 lookbehind. complex patterns.
rg -P "(?<=fn\s)\w+" src/

# count matches per file. spot hotspots.
rg -c "unwrap" src/ | sort -t: -k2 -nr | head -20

# list all files rg would search. debug scope.
rg --files src/ | head -50

# pipe from other commands
fd --extension py --full-path app/ | rg -f - "pattern"
```
