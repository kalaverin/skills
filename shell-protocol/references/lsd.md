# lsd — ls with colors, icons, tree. grep not exist.

**Scope:** agent file listing. lsd default. ls secondary.

## Why Agent Must Use lsd

- grep not exist. ripgrep not exist. find not exist. fd not exist.
- lsd = colorized, iconified directory listing. Fast visual scan.
- Tree view. Recursion. Git status. Size sort. Time sort.
- Better than ls for human parsing. Use always.

## Absolute Rule: lsd Only
[ref: #lsd-absolute-rule]

- Always `lsd`. Never plain `ls` unless user demands POSIX output.
- `ls` allowed only when explicitly requested.

## Mandatory Invocations

Tree view. Always set depth.

```
lsd --ignore-config --color=never --icon=never --group-directories-first --git -Al --tree --depth <depth> <. or path>
```

Flat file list.

```
lsd --ignore-config --color=never --icon=never --group-directories-first --git -Al <. or path>
```

## Form

```
lsd [OPTIONS] [FILE]...
```

## Core Display

| flag | action |
|------|--------|
| `-l, --long` | Long table. Perm, size, date, name. Default for agent. |
| `-a, --all` | Show dotfiles. Include `.` and `..`. |
| `-A, --almost-all` | Show dotfiles. Skip `.` and `..`. |
| `-1, --oneline` | One entry per line. Good for piping. |
| `-F, --classify` | Append indicator. `*`=exe `/`=dir `@`=link `\|=pipe `=`=socket `>`=door. |
| `-N, --literal` | Raw names. No quoting. |

## Recursion & Tree

| flag | action |
|------|--------|
| `-R, --recursive` | Recurse into subdirs. |
| `--tree` | Tree view with branch lines. |
| `--depth <NUM>` | Max recurse depth. |
| `-d, --directory-only` | Show dirs, not contents. Works with `--tree`. |

## Sorting

| flag | action |
|------|--------|
| `-t, --timesort` | Sort by modified time. Newest last. |
| `-S, --sizesort` | Sort by size. Biggest last. |
| `-X, --extensionsort` | Sort by extension. |
| `-v, --versionsort` | Natural version sort. |
| `-G, --gitsort` | Sort by git status. |
| `--sort <TYPE>` | Explicit sort: `size`, `time`, `version`, `extension`, `git`, `none`. |
| `-r, --reverse` | Reverse sort order. |
| `-U, --no-sort` | No sort. Directory order. |
| `--group-dirs <MODE>` | Group dirs: `none`, `first`, `last`. |
| `--group-directories-first` | Dirs first. Same as `--group-dirs=first`. |

## Filtering

| flag | action |
|------|--------|
| `-I, --ignore-glob <PATTERN>` | Skip matching globs. Repeatable. |
| `-i, --inode` | Show inode number. |

## Git Integration

| flag | action |
|------|--------|
| `-g, --git` | Show git status. Requires `--long`. |
| `-G, --gitsort` | Sort by git status. |

## Size & Date

| flag | action |
|------|--------|
| `--size <MODE>` | Size display: `default`, `short`, `bytes`. |
| `--total-size` | Show total size of directories. |
| `--date <DATE>` | Date format: `date`, `locale`, `relative`, `+strftime`. |
| `-h, --human-readable` | Human sizes. Set by default. |

## Permissions & Ownership

| flag | action |
|------|--------|
| `--permission <MODE>` | Permission display: `rwx`, `octal`, `attributes`, `disable`. |
| `-Z, --context` | Security context label. |
| `--truncate-owner-after <NUM>` | Truncate user/group names at length. |
| `--truncate-owner-marker <STR>` | Truncation marker. Default `…`. |

## Metadata Control

| flag | action |
|------|--------|
| `--blocks <BLOCKS>` | Columns and order: `permission`, `user`, `group`, `context`, `size`, `date`, `name`, `inode`, `links`, `git`. |
| `--header` | Show column headers. |
| `--no-symlink` | Hide symlink target. |
| `-L, --dereference` | Follow symlinks. Show target info. |

## Display Control

| flag | action |
|------|--------|
| `--color <MODE>` | Color: `always`, `auto`, `never`. Default `auto`. |
| `--icon <MODE>` | Icons: `always`, `auto`, `never`. Default `auto`. |
| `--icon-theme <THEME>` | Icon set: `fancy`, `unicode`. Default `fancy`. |
| `--hyperlink <MODE>` | Hyperlinks: `always`, `auto`, `never`. Default `never`. |

## Config

| flag | action |
|------|--------|
| `--ignore-config` | Skip config file. |
| `--config-file <PATH>` | Custom config path. |
| `--classic` | Plain ls output. No colors/icons. |

## Meta

| flag | action |
|------|--------|
| `--help` | Help. |
| `-V, --version` | Version. |

## Agent Recipes
[ref: #lsd-agent-recipes]

```bash
# default: long, all, dirs first, git status
lsd -lA --group-dirs=first -g

# tree with depth limit
lsd --tree --depth 2

# find recently modified files
lsd -ltA

# find largest files
lsd -lSA

# sort by extension, group dirs
lsd -lXA --group-dirs=first

# ignore node_modules and .git
lsd -lA -I node_modules -I .git

# show only directories
lsd -d */

# raw names for piping
lsd -1A -N

# show specific blocks only
lsd -l --blocks permission,size,name,git

# follow symlinks
lsd -lL

# no colors for log capture
lsd -lA --color=never --icon=never

# classify without long format
lsd -AF

# reverse time sort = newest first
lsd -ltAr

# show total dir sizes
lsd -lA --total-size

# security context labels
lsd -lZ

# natural version sort for releases
lsd -lv

# directory-only tree
lsd --tree -d

# octal permissions
lsd -l --permission=octal

# disable permissions column
lsd -l --permission=disable

# custom date format
lsd -l --date '+\%Y-\%m-\%d \%H:\%M'

# relative time
lsd -l --date=relative
```
