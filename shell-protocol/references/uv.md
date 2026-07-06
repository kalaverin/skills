# uv-safe — read-only uv. zero state changes.

**Scope:** safe uv subset. No writes. No mutations. No side effects.

## Absolute Rule: Read-Only Only

- uv-safe commands = commands that never modify files, envs, or remote state.
- Any command that writes `pyproject.toml`, `uv.lock`, `.venv`, `dist/`, cache, or remote index = FORBIDDEN.
- When in doubt, check this list. If not here, do not run.

## Forbidden Commands (Never Use)

| command | why forbidden |
|---------|---------------|
| `uv init` | Creates files. Mutates workspace. |
| `uv add` | Writes `pyproject.toml` and `uv.lock`. |
| `uv remove` | Writes `pyproject.toml` and `uv.lock`. |
| `uv lock` | Writes `uv.lock`. |
| `uv sync` | Modifies `.venv`. Installs/removes packages. |
| `uv venv` | Creates/modifies venv. |
| `uv format` | Rewrites source files. |
| `uv version --bump` / `uv version <VALUE>` | Writes `pyproject.toml`. |
| `uv build` | Writes to `dist/`. |
| `uv publish` | Uploads to remote index. |
| `uv tool install` | Installs globally. |
| `uv tool uninstall` | Removes global tools. |
| `uv tool update-shell` | Modifies shell config. |
| `uv python install` | Downloads/installs Python. |
| `uv python uninstall` | Removes Python. |
| `uv python update-shell` | Modifies shell config. |
| `uv cache clean` | Deletes cache entries. |
| `uv cache prune` | Deletes cache objects. |
| `uv self update` | Modifies uv binary. |
| `uv auth login` / `uv auth logout` | Modifies credentials. |

## Safe Commands (Allowed)

### uv run — with restrictions

Allowed only with `--no-sync` or `--frozen` or `--locked`. Prevents env mutation.

```
uv run --no-sync <command>
uv run --frozen <command>
uv run --locked <command>
```

| safe flag | action |
|-----------|--------|
| `--no-sync` | Skip env sync. Safe. |
| `--frozen` | No lock update. Safe if env exists. |
| `--locked` | Assert lock unchanged. Safe. |
| `-m, --module` | Run module. Safe with above. |
| `--env-file <file>` | Load env vars. Read-only. |
| `--no-env-file` | Skip env file. No-op. |
| `--with <pkg>` | Ephemeral install. Mutates nothing persistent. |
| `--isolated` | Isolated venv. Disposable. |
| `--no-project` | No project discovery. |

Forbidden flags in `uv run`:
| flag | reason |
|------|--------|
| `--exact` | May remove packages. |
| `--active` | May sync to active venv. |
| (without `--no-sync`/`--frozen`/`--locked`) | May trigger sync. |

---

### uv tree

Read-only dependency tree.

```
uv tree [OPTIONS]
```

| safe flag | action |
|-----------|--------|
| `--universal` | Platform-independent tree. |
| `-d, --depth <n>` | Limit depth. |
| `--prune <pkg>` | Prune display only. |
| `--package <pkg>` | Show only package. |
| `--no-dedupe` | Repeat duplicates in display. |
| `--invert` | Reverse deps. |
| `--outdated` | Show latest available. |
| `--show-sizes` | Show wheel sizes. |
| `--only-dev` | Only dev deps. |
| `--no-dev` | Skip dev deps. |
| `--group <group>` | Include group. |
| `--no-group <group>` | Exclude group. |
| `--only-group <group>` | Only specific group. |
| `--all-groups` | All groups. |
| `--frozen` | Display without locking. |
| `--script <script>` | Tree for script. |
| `--python-version <ver>` | Filter by version. |
| `--python-platform <platform>` | Filter by platform. |

Forbidden flags in `uv tree`:
| flag | reason |
|------|--------|
| `--locked` | May update lock if outdated. |
| (without `--frozen`) | May trigger lock update. |

---

### uv export

Read-only export. Must use `--frozen`.

```
uv export --frozen [OPTIONS]
```

| safe flag | action |
|-----------|--------|
| `--format <fmt>` | `requirements.txt`, `pylock.toml`, `cyclonedx1.5`. |
| `--all-packages` | Export workspace. |
| `--package <pkg>` | Export specific. |
| `--prune <pkg>` | Prune from display. |
| `--extra <extra>` | Include extra. |
| `--all-extras` | All extras. |
| `--no-dev` | Skip dev. |
| `--only-dev` | Only dev. |
| `--group <group>` | Include group. |
| `--no-group <group>` | Exclude group. |
| `--only-group <group>` | Only specific. |
| `--all-groups` | All groups. |
| `--no-annotate` | No comments. |
| `--no-header` | No header. |
| `--no-hashes` | Omit hashes. |
| `--frozen` | Mandatory. No lock update. |

---

### uv version — read-only

Allowed only without arguments or flags that write.

```
uv version
uv version --short
uv version --output-format json
```

Forbidden: `uv version <VALUE>`, `uv version --bump <bump>`, `uv version --dry-run` still modifies state conceptually.

---

### uv audit

Read-only vulnerability scan.

```
uv audit [OPTIONS]
```

| safe flag | action |
|-----------|--------|
| `--no-extra <extra>` | Skip extra. |
| `--no-dev` | Skip dev. |
| `--no-group <group>` | Skip group. |
| `--only-group <group>` | Only group. |
| `--only-dev` | Only dev. |
| `--frozen` | Audit without locking. |
| `--script <script>` | Audit script. |
| `--python-version <ver>` | Filter by version. |
| `--python-platform <platform>` | Filter by platform. |
| `--ignore <id>` | Ignore vulnerability. |
| `--ignore-until-fixed <id>` | Ignore until fix. |
| `--service-format <fmt>` | `osv`. |
| `--service-url <url>` | Custom API. |

Forbidden: `--locked` (may update lock).

---

### uv tool — read-only

```
uv tool list
uv tool dir
uv tool run <pkg>    # ephemeral. no persistent install
uvx <pkg>            # alias for uv tool run. safe
```

Forbidden: `uv tool install`, `uv tool uninstall`, `uv tool upgrade`, `uv tool update-shell`.

---

### uv python — read-only

```
uv python list
uv python find
uv python dir
```

Forbidden: `uv python install`, `uv python uninstall`, `uv python pin`, `uv python update-shell`.

---

### uv pip — read-only subcommands

```
uv pip list
uv pip show <pkg>
uv pip tree
uv pip check
uv pip freeze
```

Forbidden: `uv pip install`, `uv pip uninstall`, `uv pip sync`, `uv pip compile` (writes file).

---

### uv cache — read-only

```
uv cache dir
uv cache size
```

Forbidden: `uv cache clean`, `uv cache prune`.

---

### uv auth — read-only

```
uv auth dir
uv auth token
```

Forbidden: `uv auth login`, `uv auth logout`.

---

### uv self — read-only

```
uv self version
```

Forbidden: `uv self update`.

---

### uv help

```
uv help [command]
```

Always safe.

---

## Safe Workflow Checklist
[ref: #uv-safe-workflow-checklist]

Before running any uv command:

1. Is the command in the **Safe Commands** list above?
2. Are all flags used also in the safe flags list?
3. Does the command lack `--go` equivalent (no implicit write triggers)?
4. If using `uv run`, is `--no-sync` or `--frozen` or `--locked` present?
5. If using `uv export`, is `--frozen` present?
6. If using `uv tree`, is `--frozen` present?

If any check fails → STOP. Ask user before proceeding.

## Examples

```bash
# safe: show dependency tree
uv tree --frozen

# safe: export requirements without updating lock
uv export --frozen --no-dev -o /tmp/requirements.txt

# safe: run script without syncing env
uv run --no-sync python script.py

# safe: list installed packages
uv pip list

# safe: check for vulnerabilities
uv audit --frozen

# safe: run black ephemerally
uvx black --check src/

# safe: show Python installations
uv python list

# safe: cache info
uv cache size
```
