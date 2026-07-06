# tree — directory tree. ls not enough.

**Scope:** agent directory tree view tool. tree default for structure.

## Default Behavior

`tree [dir]` → print directory tree. Recursive. Skips hidden files. Sorts alphabetically. Prints indentation lines.

## Agent Rules
[ref: #tree-agent-rules]

1. Always tree for directory structure. Never use ls.
2. **MANDATORY ARGS, ALWAYS USE THIS FLAGS**: `--gitignore --prune --condense --compress 3 --dirsfirst -vnx`
3. Use `-L` to limit depth. Default recursive can be huge.
4. Use `-f` for full paths. Good for piping.
5. Use `-P` or `-I` to filter. Narrow scope first.
6. Use `-J` or `-X` for machine-readable output.

## 1. Scope and Filters

Control what appears.

| Flag | Effect |
|---|---|
| `-L N` | Max depth. Essential. |
| `-d` | Directories only. |
| `-a` | All files. Include hidden. |
| `-f` | Full path prefix for each file. |
| `-x` | Stay on current filesystem. |
| `-P pattern` | List only files matching pattern. |
| `-I pattern` | Exclude files matching pattern. |
| `--gitignore` | Filter using `.gitignore`. |
| `--gitfile X` | Read explicit gitignore file. |
| `--ignore-case` | Ignore case in pattern matching. |
| `--matchdirs` | Include directory names in `-P` matching. |
| `--prune` | Prune empty directories from output. |
| `--filelimit #` | Do not descend dirs with more than # files. |
| `--condense` | Condense directory singletons to one line. |
| `-l` | Follow symbolic links like directories. |
| `-R` | Rerun tree when max dir level reached. |

## 2. Display

Graphics and color.

| Flag | Effect |
|---|---|
| `-C` | Color on always. |
| `-n` | Color off always. |
| `-i` | No indentation lines. |
| `-A` | ANSI graphic indentation lines. |
| `-S` | CP437 graphic indentation lines. |
| `--compress #` | Compress indentation lines. |
| `--charset X` | Use charset X for terminal/HTML output. |
| `--metafirst` | Print meta-data at beginning of each line. |
| `--noreport` | No file/directory count at end. |
| `-o filename` | Output to file instead of stdout. |

## 3. File Metadata

Show file properties.

| Flag | Effect |
|---|---|
| `-s` | Size in bytes. |
| `-h` | Human readable size. |
| `--si` | Like `-h`, SI units (powers of 1000). |
| `--du` | Directory size by contents. |
| `-D` | Date of last modification. |
| `--timefmt fmt` | Format time string. |
| `-p` | Protections/permissions. |
| `-u` | Owner or UID. |
| `-g` | Group or GID. |
| `-F` | Append `/`, `=`, `*`, `@`, `\|`, `>` like `ls -F`. |
| `--inodes` | Inode number. |
| `--device` | Device ID. |
| `-q` | Non-printable chars as `?`. |
| `-N` | Non-printable chars as is. |
| `-Q` | Quote filenames with double quotes. |

## 4. Sorting

Control order.

| Flag | Effect |
|---|---|
| `--sort X` | Select sort: name, version, size, mtime, ctime, none. |
| `-r` | Reverse sort order. |
| `--dirsfirst` | Directories before files. |
| `--filesfirst` | Files before directories. |
| `-v` | Sort alphanumerically by version. |
| `-t` | Sort by modification time. |
| `-c` | Sort by status change time. |
| `-U` | Leave files unsorted. |

## 5. Machine Output

Structured formats.

| Flag | Effect |
|---|---|
| `-J` | JSON output. |
| `-X` | XML output. |

## 6. HTML and Hyperlinks

Web and terminal links.

| Flag | Effect |
|---|---|
| `-H baseHREF` | HTML output with base directory. |
| `-T string` | HTML title and H1 header. |
| `--nolinks` | No hyperlinks in HTML output. |
| `--hintro X` | HTML intro file. |
| `--houtro X` | HTML outro file. |
| `--hyperlink` | OSC 8 terminal hyperlinks. |
| `--scheme X` | Hyperlink scheme. Default `file://`. |
| `--authority X` | Hyperlink authority/hostname. |

## 7. Input and Misc

Rarely used.

| Flag | Effect |
|---|---|
| `--fromfile` | Read paths from files (`.=` stdin). |
| `--fromtabfile` | Read trees from tab-indented files. |
| `--fflinks` | Process link info with `--fromfile`. |
| `--info` | Print info from `.info` files. |
| `--infofile X` | Read explicit info file. |
| `--opt-toggle` | Enable option toggling. |
| `--version` | Print version. |
| `--help` | Print help. |
| `--` | Options terminator. |

## 8. Agent Recipes
[ref: #tree-agent-recipes]

Daily commands for code work.

```bash
# quick project overview. limit depth. respect gitignore.
tree -L 2 --gitignore --prune --condense --compress 3 --dirsfirst -vnx

# full source tree, no deps. clean view.
tree -L 3 --gitignore --prune --condense --compress 3 --dirsfirst -vnx -I 'node_modules|venv|.git|__pycache__|target|dist|build'

# show only directories. understand architecture.
tree -d -L 3 --gitignore --prune --condense --compress 3 --dirsfirst -vnx src/

# machine-readable structure for script processing
tree -J -L 3 --gitignore --prune --condense --compress 3 --dirsfirst -vnx > structure.json

# recent changes sort. find recently touched files.
tree -t -L 2 --gitignore --prune --condense --compress 3 --dirsfirst -vnx src/

```
