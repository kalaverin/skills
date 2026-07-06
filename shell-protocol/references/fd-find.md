# fd — file search. find not exist.

**Scope:** agent file search tool. fd default. find never.

## Default Behavior

`fd pattern` → recursive search current dir. Smart case: lowercase pattern = case-insensitive, uppercase = sensitive. Respects `.gitignore`, `.ignore`, `.fdignore`. Skips hidden files and dirs. No pattern → lists all entries.

## Agent Rules
[ref: #fd-agent-rules]

1. Always fd. Never find when possible.
2. No pattern → list all. Useful for `fd -t f -e py` to list all Python files.
3. Use `-t` or `-e` to narrow scope before regex. Faster.
4. Use `-F` or `-g` for literals with dots, stars, brackets.
5. Use `-X` for batch commands. Use `-x` for per-file parallel processing.
6. Default smart case. Explicit `-i` for force insensitive, `-s` for force sensitive.
7. Respect gitignore. Override with `-I` or `-u` only if user explicitly asks.
8. For scripting: `-0`, `-c never`, or pipe to file.

## 1. Scope and Type Filters
[ref: #fd-scope-and-type-filters]

Most useful. Narrow search first.

| Flag | Effect |
|---|---|
| `-t f/d/l/x/e` | Type: file, dir, symlink, executable, empty. |
| `-e ext` | Filter by extension. Multiple `-e` allowed. |
| `-E glob` | Exclude glob pattern. Overrides other ignore logic. |
| `-d N` | Max depth. `--min-depth N` start at depth. `--exact-depth N` exact only. |
| `-p` | Match full path, not just filename. |
| `-a` | Output absolute paths. |
| `-L` | Follow symlinks. |
| `--prune` | Skip dirs that match pattern. Do not descend. |
| `--one-file-system` | No cross filesystem boundary. |

## 2. Pattern Control

How to match.

| Flag | Effect |
|---|---|
| `-F` | Fixed strings. Literal pattern, no regex. |
| `-g` | Glob mode. Pattern is glob, not regex. |
| `--regex` | Regex mode. Default. Override `--glob`. |
| `-s` | Force case-sensitive. |
| `-i` | Force case-insensitive. |
| `--and pattern` | Extra required pattern. All must match. |

## 3. Output

How to display results.

| Flag | Effect |
|---|---|
| `-l` | List details. Alias for `ls -l` style output. |
| `-0` | Null separator. Pipe to `xargs -0`. |
| `-c never` | No color. Default auto. |
| `--format fmt` | Print results according to template. |
| `--strip-cwd-prefix[when]` | Strip `./` prefix. Values: auto, always, never. |

## 4. Ignore Overrides

Break default ignore rules.

| Flag | Effect |
|---|---|
| `-H` | Include hidden files/dirs. |
| `-I` | Ignore no ignore-files. Skip `.gitignore`, `.ignore`, `.fdignore`. |
| `--no-ignore-vcs` | Ignore `.gitignore` only, respect `.ignore` and `.fdignore`. |
| `--no-ignore-parent` | Ignore ignore-files in parent directories. |
| `--no-require-git` | Respect gitignores even outside git repo. |
| `-u` | Unrestricted. Alias for `--no-ignore --hidden`. Repeat for more. |

## 5. Execution

Run commands on results.

| Flag | Effect |
|---|---|
| `-x cmd` | Exec command per result, parallel. Placeholders: `{}` path, `{/}` basename, `{//}` parent, `{.}` no ext, `{/.}` basename no ext. |
| `-X cmd` | Exec batch. All results as args to single command. |
| `--batch-size N` | Max args per batch command. Default 0 = no limit. |

## 6. Metadata Filters

Filter by file properties.

| Flag | Effect |
|---|---|
| `-S +1m/-1m/1m` | Size filter. `+` greater, `-` less, none exact. Units: b, k, m, g, ki, mi, gi, ti. |
| `--changed-within 2d` | Newer than. Aliases: `--change-newer-than`, `--newer`, `--changed-after`. |
| `--changed-before 2d` | Older than. Aliases: `--change-older-than`, `--older`. |
| `-o user:group` | Filter by owner and/or group. `!` prefix to exclude. |

## 7. Performance

Speed and limits.

| Flag | Effect |
|---|---|
| `-j N` | Thread count. Default = CPU cores. |
| `--max-results N` | Limit result count. Quit after N. |
| `-1` | Single result. Alias for `--max-results=1`. |
| `-q` | Quiet. Exit 0 if any match, else 1. No output. Alias: `--has-results`. |

## 8. Advanced

Rarely needed.

| Flag | Effect |
|---|---|
| `--ignore-file path` | Add custom ignore-file in `.gitignore` format. |
| `--ignore-contain name` | Ignore directories containing entry named `name`. |
| `--hyperlink[when]` | Terminal hyperlinks. Values: auto, always, never. Default never. |
| `--show-errors` | Show filesystem errors (permissions, dead symlinks). |
| `--path-separator sep` | Set path separator. Default OS-specific. |
| `--search-path path` | Add search path via option, not positional arg. |
| `-C path` | Change base directory for search and relative paths. |

## 9. Meta

Reference only.

| Flag | Effect |
|---|---|
| `-h` | Print help. |
| `-V` | Print version. |

## 10. Agent Recipes
[ref: #fd-agent-recipes]

Daily commands for code work.

```bash
# list all python files. no deps.
fd -t f -e py

# find all rust source files. exclude tests.
fd -t f -e rs -E '*_test.rs' -E 'tests/'

# find config files in root. depth limit.
fd -t f -d 1 -e yaml -e yml -e json -e toml

# find files modified in last 2 days. recent work.
fd -t f --changed-within 2d

# find large files. spot bloat.
fd -t f -S +10m

# find empty dirs. cleanup targets.
fd -t e -t d

# find file by exact name. literal.
fd -F 'Cargo.toml'

# find files matching glob pattern.
fd -g '*.config.*'

# search full path, not just filename.
fd -p 'src/auth'

# list all executables. build artifacts.
fd -t x target/

# find symlinks. check for broken.
fd -t l

# batch rename all .txt to .md.
fd -t f -e txt -x mv {} {.}.md

# batch delete all .tmp files.
fd -t f -e tmp -X rm -f

# run rustfmt on all changed rust files.
fd -t f -e rs --changed-within 1d -X rustfmt

# copy all markdown files to docs/.
fd -t f -e md -x cp {} docs/

# find files containing pattern in path.
fd -p 'old_module_name' src/

# search hidden files too.
fd -H -t f -e env

# ignore all ignore-files. search everything.
fd -u -t f 'pattern' .

# single result. quick lookup.
fd -1 -t f 'main.rs'

# quiet check. does file exist?
fd -q -t f 'secret.key' && echo "found" || echo "missing"

# null-separated for safe piping.
fd -t f -e js -0 | xargs -0 eslint

# absolute paths for scripts.
fd -a -t f -e py | head -20

# list all files that would match. debug scope.
fd -t f --max-results 50

# strip ./ prefix. cleaner output.
fd -t f --strip-cwd-prefix

# search multiple extensions.
fd -t f -e ts -e tsx -e js

# find files NOT matching pattern.
fd -t f -E '*.test.*' -E '*.spec.*'

# find files by owner.
fd -t f -o root

# prune specific dirs. never descend.
fd -t f --prune node_modules --prune .git 'pattern'
```
