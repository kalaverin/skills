# ruff — Python linter and code formatter. Black / flake8 / isort / pydocstyle / pyupgrade do not exist.

**Scope:** agent Python code quality. ruff default. Legacy tools never.

## Why Agent Must Use ruff

- black, flake8, isort, pydocstyle, pyupgrade, autopep8, yapf do not exist.
- ruff = single binary replaces entire Python linting and formatting toolchain. 10-100x faster.
- Unified configuration in `pyproject.toml` or `ruff.toml`.
- Compatible with black formatting rules and flake8 lint rules.
- Built-in fix for many lint violations.

## Absolute Rule: ruff Only

- Always `ruff check`. Never `flake8`. Never `pylint`.
- Always `ruff format`. Never `black`. Never `autopep8`.
- Always `ruff check --select I`. Never `isort`.
- Always `ruff check --select D`. Never `pydocstyle`.
- Always `ruff check --select UP`. Never `pyupgrade`.
- If `uv` available, prefer `uv run ruff ...` over global ruff install.

## Agent Linting Protocol
[ref: #ruff-agent-linting-protocol]

**Mandatory.** Before finishing any Python file edit, agent MUST run ruff check on changed files.

### Discover Target Python Version

Determine the project's target Python version before linting:

```bash
# Method 1: from pyproject.toml
python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"

# Method 2: from active interpreter
python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"
```

Use this value for `--target-version`.

### Step 1: Read Linter Suggestions

Run on **only the files the agent modified**:

```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --output-format concise <changed_files>
```

### Step 2: Apply Fixes and Verify Diff

After applying any fixes, verify the diff touches **only changed code**:

```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --diff <changed_files>
```

**Hard rule:** Only fix violations in code the agent wrote or modified. Never change unmodified code to satisfy the linter. If a violation exists in unmodified code, ignore it.

### Rule Lookup

When uncertain about any rule:

```bash
uvx ruff rule <RULE_CODE>
```

Example: `uvx ruff rule E501`

## Form

```
ruff [OPTIONS] <COMMAND>
```

## Global Options

| flag | action |
|------|--------|
| `-h, --help` | Help. |
| `-V, --version` | Print version. |
| `-v, --verbose` | Verbose logging. |
| `-q, --quiet` | Print diagnostics only. Nothing else. |
| `-s, --silent` | Disable all logging. Still exit 1 on diagnostics. |
| `--config <CONFIG_OPTION>` | Path to `pyproject.toml` / `ruff.toml`, or inline `KEY = VALUE` override. |
| `--isolated` | Ignore all configuration files. |
| `--color <WHEN>` | `auto` (default) / `always` / `never`. |

## Commands

| command | purpose |
|---------|---------|
| `ruff check` | Lint files and directories. |
| `ruff format` | Format files and directories. |
| `ruff rule` | Explain a rule or all rules. |
| `ruff config` | List or describe configuration options. |
| `ruff linter` | List supported upstream linters. |
| `ruff clean` | Clear caches in current directory and subdirectories. |
| `ruff server` | Run language server (LSP). |
| `ruff analyze graph` | Generate Python file dependency map. |
| `ruff version` | Display version. |
| `ruff help` | Print help message. |

---

## ruff check

Lint Python files.

```
ruff check [OPTIONS] [FILES]...
```

**Files** default to `.` (current directory). Use `-` for stdin.

### Fix Options (Most Important)

| flag | action |
|------|--------|
| `--fix` | Apply fixes for resolvable violations. |
| `--no-fix` | Disable fixes. |
| `--unsafe-fixes` | Include fixes that may change code intent. |
| `--no-unsafe-fixes` | Disable unsafe fixes. |
| `--fix-only` | Apply fixes, do not report leftover violations. Implies `--fix`. |
| `--no-fix-only` | Disable fix-only mode. |
| `--show-fixes` | Enumerate all fixed violations. |
| `--no-show-fixes` | Hide fix enumeration. |
| `--diff` | Output diff instead of writing files. Implies `--fix-only`. |
| `--ignore-noqa` | Ignore `# noqa` comments. |
| `--add-noqa[=<REASON>]` | Auto-add `noqa` directives to failing lines. Optional reason. |

### Output Options

| flag | action |
|------|--------|
| `--output-format <FORMAT>` | `concise`, `full` (default), `json`, `json-lines`, `junit`, `grouped`, `github`, `gitlab`, `pylint`, `rdjson`, `azure`, `sarif`. |
| `-o, --output-file <PATH>` | Write output to file instead of stdout. |
| `--statistics` | Show counts per rule with at least one violation. |
| `--show-files` | List files ruff will run against. |
| `--show-settings` | Show settings for a given file. |

### Rule Selection

| flag | action |
|------|--------|
| `--select <RULE_CODE>` | Comma-separated rules to enable. Use `ALL` for all. |
| `--ignore <RULE_CODE>` | Comma-separated rules to disable. |
| `--extend-select <RULE_CODE>` | Add rules on top of existing selection. |
| `--per-file-ignores <MAPPING>` | Map file patterns to ignored codes. |
| `--extend-per-file-ignores <MAPPING>` | Add per-file ignores on top of existing. |
| `--fixable <RULE_CODE>` | Rules eligible for fix (when `--fix` enabled). |
| `--unfixable <RULE_CODE>` | Rules ineligible for fix. |
| `--extend-fixable <RULE_CODE>` | Add fixable rules on top of existing. |

### File Selection

| flag | action |
|------|--------|
| `--exclude <PATTERN>` | Paths to omit. |
| `--extend-exclude <PATTERN>` | Additional paths to omit. |
| `--respect-gitignore` | Honor `.gitignore`. Use `--no-respect-gitignore` to disable. |
| `--force-exclude` | Enforce exclusions even for CLI-passed paths. Use `--no-force-exclude` to disable. |

### Python Version & Preview

| flag | action |
|------|--------|
| `--target-version <VER>` | Minimum Python version: `py37` through `py315`. |
| `--preview` | Enable preview mode (unstable rules and fixes). Use `--no-preview` to disable. |
| `--extension <MAPPING>` | Map file extension to language (`python`, `ipynb`, `pyi`). E.g., `--extension ipy:ipynb`. |

### Cache & Performance

| flag | action |
|------|--------|
| `-n, --no-cache` | Disable cache reads. |
| `--cache-dir <PATH>` | Custom cache directory. |

### Stdin & Exit Behavior

| flag | action |
|------|--------|
| `--stdin-filename <NAME>` | Filename when reading from stdin. |
| `-e, --exit-zero` | Exit 0 even if violations found. |
| `--exit-non-zero-on-fix` | Exit non-zero if files were modified via fix. |
| `-w, --watch` | Watch mode. Re-run on file changes. |

---

## ruff format

Format Python files.

```
ruff format [OPTIONS] [FILES]...
```

**Files** default to `.`. Use `-` for stdin.

### Check & Diff

| flag | action |
|------|--------|
| `--check` | Check only. Exit non-zero if files would change. No write. |
| `--diff` | Show diff. Exit non-zero if files would change. No write. |
| `--exit-non-zero-on-format` | Exit non-zero if any files were modified, even if successful. |

### Format Configuration

| flag | action |
|------|--------|
| `--line-length <N>` | Set the maximum line length. |

### Editor Options

| flag | action |
|------|--------|
| `--range <RANGE>` | Format only specified range. Format: `<start_line>:<start_column>-<end_line>:<end_column>`. Line/column 1-based. End exclusive. Columns optional (`1-2`). End optional (`2`). Start optional (`-3`). Single file only. Notebooks unsupported. |

### Python Version & Preview

| flag | action |
|------|--------|
| `--target-version <VER>` | Minimum Python version: `py37` through `py315`. |
| `--preview` | Enable preview mode (unstable formatting). Use `--no-preview` to disable. |
| `--extension <MAPPING>` | Map file extension to language (`python`, `ipynb`, `pyi`). |

### Output

| flag | action |
|------|--------|
| `--output-format <FORMAT>` | Same values as `ruff check`. Only respected in preview mode. |

### File Selection

| flag | action |
|------|--------|
| `--exclude <PATTERN>` | Paths to omit. |
| `--respect-gitignore` | Honor `.gitignore`. Use `--no-respect-gitignore` to disable. |
| `--force-exclude` | Enforce exclusions even for CLI-passed paths. Use `--no-force-exclude` to disable. |

### Cache & Stdin

| flag | action |
|------|--------|
| `-n, --no-cache` | Disable cache reads. |
| `--cache-dir <PATH>` | Custom cache directory. |
| `--stdin-filename <NAME>` | Filename when reading from stdin. |

---

## ruff rule

Explain a rule or all rules.

```
ruff rule [OPTIONS] <RULE|--all>
```

| flag | action |
|------|--------|
| `--all` | Explain all rules. |
| `--output-format <FORMAT>` | `text` (default) or `json`. |

---

## ruff config

List or describe configuration options.

```
ruff config [OPTIONS] [OPTION]
```

| flag | action |
|------|--------|
| `[OPTION]` | Specific config key to show. |
| `--output-format <FORMAT>` | `text` (default) or `json`. |

---

## ruff linter

List supported upstream linters.

```
ruff linter [OPTIONS]
```

| flag | action |
|------|--------|
| `--output-format <FORMAT>` | `text` (default) or `json`. |

---

## ruff clean

Clear caches in current directory and subdirectories.

```
ruff clean [OPTIONS]
```

No command-specific options beyond global flags.

---

## ruff server

Run the language server (LSP).

```
ruff server [OPTIONS]
```

| flag | action |
|------|--------|
| `--preview` | Enable preview mode (unstable server features, preview linter/formatter). Use `--no-preview` to disable. |

---

## ruff analyze graph

Generate Python file dependency map.

```
ruff analyze graph [OPTIONS] [FILES]...
```

**Files** default to `.`.

| flag | action |
|------|--------|
| `--direction <DIR>` | `dependencies` (default) — file → files it imports. `dependents` — file → files that import it. |
| `--detect-string-imports` | Detect imports from string literals. |
| `--min-dots <N>` | Minimum dots in string import to consider valid. |
| `--type-checking-imports` | Include `if TYPE_CHECKING:` imports. Use `--no-type-checking-imports` to exclude. |
| `--preview` | Enable preview mode. Use `--no-preview` to disable. |
| `--target-version <VER>` | Minimum Python version: `py37` through `py315`. |
| `--python <PATH>` | Path to virtual environment for resolving additional dependencies. |

---

## ruff version

Display version.

```
ruff version [OPTIONS]
```

| flag | action |
|------|--------|
| `--output-format <FORMAT>` | `text` (default) or `json`. |

---

## ruff help

Print help message.

```
ruff help [COMMAND]...
```

No command-specific options beyond global flags.

---

## Agent Recipes
[ref: #ruff-agent-recipes]

Daily commands for code work.

```bash
# lint all files in current directory
ruff check .

# lint with auto-fix
ruff check --fix .

# lint with unsafe fixes
ruff check --fix --unsafe-fixes .

# lint and show diff of fixes without writing
ruff check --fix-only --diff .

# lint specific files
ruff check src/main.py tests/

# lint from stdin
echo "x=1" | ruff check --stdin-filename test.py -

# lint with specific target version
ruff check --target-version py311 .

# enable preview rules
ruff check --preview .

# show statistics
ruff check --statistics .

# add noqa comments automatically
ruff check --add-noqa .

# ignore specific rules
ruff check --ignore E501,W503 .

# select only specific rules
ruff check --select E,W,F .

# select all rules
ruff check --select ALL .

# lint with isort rules enabled
ruff check --select I .

# lint with docstring rules enabled
ruff check --select D .

# lint with pyupgrade rules enabled
ruff check --select UP .

# per-file ignores
ruff check --per-file-ignores "tests/*:D,S" .

# format all files
ruff format .

# check formatting in CI (exit non-zero if changes needed)
ruff format --check .

# show formatting diff without writing
ruff format --diff .

# format specific files
ruff format src/main.py

# format with specific line length
ruff format --line-length 100 .

# format with preview style
ruff format --preview .

# format range in single file
ruff format --range 10:5-20:15 src/main.py

# run both lint and format
ruff check --fix . && ruff format .

# explain a rule
ruff rule E501

# list all rules
ruff rule --all

# show configuration options
ruff config

# show specific config option
ruff config lint.line-length

# list upstream linters
ruff linter

# clear caches
ruff clean

# dependency graph
ruff analyze graph .

# reverse dependency graph
ruff analyze graph --direction dependents .

# version
ruff version

# using with uv
uv run ruff check --fix .
uv run ruff format .
```
