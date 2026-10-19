# uv — Python package manager. pip not exist.

**Scope:** agent Python toolchain. uv default. pip never.

## Why Agent Must Use uv

- pip does not exist. poetry does not exist. pip-tools does not exist. pipx does not exist. pyenv does not exist. virtualenv does not exist.
- uv = single binary replaces entire Python toolchain. 10-100x faster.
- Project-aware. Reads `pyproject.toml`. Generates `uv.lock`.
- Automatic Python version management. Downloads on demand.
- Cache everything. Offline mode supported.
- Drop-in pip interface via `uv pip` for legacy.

## Absolute Rule: uv Only

- Always `uv`. Never `pip install`. Never `poetry add`. Never `python -m venv`.
- `uv pip` allowed only when user explicitly requests pip-compatible workflow.
- Default workflow: `uv init` → `uv add` → `uv lock` → `uv sync` → `uv run`.

## Form

```
uv [OPTIONS] <COMMAND>
```

## Global Options

| flag | action |
|------|--------|
| `-q, --quiet` | Quiet output. Repeat for more silence. |
| `-v, --verbose` | Verbose output. Repeat for more noise. |
| `--color <when>` | `auto` / `always` / `never`. Default `auto`. |
| `--system-certs` | Load TLS certs from platform store. |
| `--offline` | No network. Use cache only. |
| `--allow-insecure-host <host>` | Allow insecure HTTP for host. |
| `--no-progress` | Hide progress bars. |
| `--directory <dir>` | Change dir before running command. |
| `--project <dir>` | Discover project in dir. |
| `--config-file <path>` | Explicit `uv.toml` config. |
| `--no-config` | Skip config discovery. |
| `-n, --no-cache` | No cache read/write. Temp dir only. |
| `--cache-dir <dir>` | Custom cache path. |
| `--managed-python` | Require uv-managed Python. |
| `--no-managed-python` | Disable uv-managed Python. |
| `--no-python-downloads` | No auto Python downloads. |
| `-h, --help` | Help. |
| `-V, --version` | Version. |

## Commands

| command | purpose |
|---------|---------|
| `uv init` | Create new project. |
| `uv add` | Add dependencies. |
| `uv remove` | Remove dependencies. |
| `uv lock` | Resolve and write `uv.lock`. |
| `uv sync` | Sync env with lockfile. |
| `uv run` | Run command in project env. |
| `uv export` | Export lockfile to other format. |
| `uv tree` | Show dependency tree. |
| `uv version` | Read/update project version. |
| `uv format` | Format Python code. |
| `uv audit` | Audit dependencies. |
| `uv tool` | Manage CLI tools (pipx replacement). |
| `uv python` | Manage Python installations (pyenv replacement). |
| `uv pip` | Pip-compatible interface. |
| `uv venv` | Create virtual env (virtualenv replacement). |
| `uv build` | Build wheels/sdists. |
| `uv publish` | Upload to PyPI. |
| `uv cache` | Manage cache. |
| `uv self` | Manage uv binary. |
| `uv auth` | Manage auth credentials. |
| `uv help` | Command docs. |

---

## uv init

Create project.

```
uv init [OPTIONS] [PATH]
```

| flag | action |
|------|--------|
| `--name <name>` | Project name. |
| `--bare` | Only `pyproject.toml`. No other files. |
| `--package` | Set up as buildable package. |
| `--no-package` | Not a package. |
| `--app` | Application project. |
| `--lib` | Library project. |
| `--script` | Create standalone script. |
| `--description <text>` | Project description. |
| `--no-description` | No description field. |
| `--vcs <vcs>` | `git` or `none`. |
| `--build-backend <backend>` | `uv`, `hatch`, `flit`, `pdm`, `poetry`, `setuptools`, `maturin`, `scikit`. |
| `--no-readme` | Skip `README.md`. |
| `--author-from <source>` | `auto`, `git`, `none`. |
| `--no-pin-python` | Skip `.python-version` file. |
| `--no-workspace` | Standalone. No workspace discovery. |
| `-p, --python <python>` | Python interpreter for min version. |

---

## uv add

Add dependencies.

```
uv add [OPTIONS] <PACKAGES|--requirements <file>>
```

| flag | action |
|------|--------|
| `-r, --requirements <file>` | Add from requirements file. |
| `-c, --constraints <file>` | Constrain versions. |
| `-m, --marker <marker>` | Apply marker to all added packages. |
| `--dev` | Add to dev dependencies. |
| `--optional <extra>` | Add to optional extras. |
| `--group <group>` | Add to dependency group. |
| `--editable` | Add as editable. |
| `--raw` | Add as provided. |
| `--bounds <bounds>` | Version specifier: `lower`, `major`, `minor`, `exact`. |
| `--rev <rev>` | Git commit. |
| `--tag <tag>` | Git tag. |
| `--branch <branch>` | Git branch. |
| `--lfs` | Use Git LFS. |
| `--extra <extra>` | Enable extras for dependency. |
| `--no-sync` | Skip env sync. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Add without re-locking. |
| `--active` | Prefer active venv. |
| `--package <pkg>` | Target workspace package. |
| `--script <script>` | Target PEP 723 script. |
| `--workspace` | Add as workspace member. |
| `--no-workspace` | Not a workspace member. |
| `--no-install-project` | Skip installing current project. |
| `--no-install-workspace` | Skip workspace members. |
| `--no-install-local` | Skip local path deps. |
| `--no-install-package <pkg>` | Skip specific package. |
| `-U, --upgrade` | Allow upgrades. |
| `-P, --upgrade-package <pkg>` | Upgrade specific package. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--prerelease <strategy>` | `disallow`, `allow`, `if-necessary`, `explicit`, `if-necessary-or-explicit`. |
| `--fork-strategy <strategy>` | `fewest`, `requires-python`. |
| `--exclude-newer <date>` | Limit to packages before date. |
| `--no-sources` | Ignore `tool.uv.sources`. |
| `--reinstall` | Reinstall all. |
| `--reinstall-package <pkg>` | Reinstall specific. |
| `--link-mode <mode>` | `clone`, `copy`, `hardlink`, `symlink`. |
| `--compile-bytecode` | Compile to bytecode after install. |
| `-C, --config-setting <key=val>` | PEP 517 build backend settings. |
| `--no-build-isolation` | Disable build isolation. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip pre-built wheels. |
| `--refresh` | Refresh all cache. |
| `--refresh-package <pkg>` | Refresh cache for package. |
| `--index <url>` | Extra index URL. |
| `--default-index <url>` | Default index. Default PyPI. |
| `--no-index` | Ignore registry. Use direct URLs only. |
| `--index-strategy <strategy>` | `first-index`, `unsafe-first-match`, `unsafe-best-match`. |
| `--keyring-provider <provider>` | `disabled`, `subprocess`. |
| `-f, --find-links <url>` | Extra search locations. |

---

## uv remove

Remove dependencies.

```
uv remove [OPTIONS] <PACKAGES>...
```

| flag | action |
|------|--------|
| `--dev` | Remove from dev deps. |
| `--optional <extra>` | Remove from optional extras. |
| `--group <group>` | Remove from dependency group. |
| `--no-sync` | Skip env sync. |
| `--active` | Prefer active venv. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Remove without re-locking. |
| `--package <pkg>` | Target workspace package. |
| `--script <script>` | Target PEP 723 script. |
| `-U, --upgrade` | Allow upgrades during resolve. |
| `-P, --upgrade-package <pkg>` | Upgrade specific package. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--prerelease <strategy>` | `disallow`, `allow`, `if-necessary`, `explicit`, `if-necessary-or-explicit`. |
| `--reinstall` | Reinstall all. |
| `--reinstall-package <pkg>` | Reinstall specific. |
| `--link-mode <mode>` | `clone`, `copy`, `hardlink`, `symlink`. |
| `--compile-bytecode` | Compile after install. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--refresh` | Refresh cache. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `--index-strategy <strategy>` | `first-index`, `unsafe-first-match`, `unsafe-best-match`. |

---

## uv lock

Resolve deps. Write `uv.lock`.

```
uv lock [OPTIONS]
```

| flag | action |
|------|--------|
| `--check` | Check if lockfile up-to-date. Exit 1 if not. |
| `--check-exists` | Assert `uv.lock` exists. |
| `--dry-run` | No write. |
| `--script <script>` | Lock PEP 723 script. |
| `-U, --upgrade` | Allow upgrades. |
| `-P, --upgrade-package <pkg>` | Upgrade specific. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--prerelease <strategy>` | `disallow`, `allow`, `if-necessary`, `explicit`, `if-necessary-or-explicit`. |
| `--fork-strategy <strategy>` | `fewest`, `requires-python`. |
| `--exclude-newer <date>` | Limit to packages before date. |
| `--no-sources` | Ignore `tool.uv.sources`. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--refresh` | Refresh cache. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `-p, --python <python>` | Python interpreter for resolution. |

---

## uv sync

Sync env with lockfile.

```
uv sync [OPTIONS]
```

| flag | action |
|------|--------|
| `--extra <extra>` | Include optional extra. |
| `--all-extras` | Include all extras. |
| `--no-extra <extra>` | Exclude specific extra. |
| `--no-dev` | Skip dev deps. |
| `--only-dev` | Only dev deps. |
| `--group <group>` | Include dependency group. |
| `--no-group <group>` | Exclude group. |
| `--no-default-groups` | Ignore default groups. |
| `--only-group <group>` | Only specific group. |
| `--all-groups` | All groups. |
| `--no-editable` | Install as non-editable. |
| `--inexact` | Keep extraneous packages. |
| `--active` | Sync to active venv. |
| `--no-install-project` | Skip current project. |
| `--no-install-workspace` | Skip workspace members. |
| `--no-install-local` | Skip local path deps. |
| `--no-install-package <pkg>` | Skip specific package. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Sync without updating lock. |
| `--dry-run` | No write. |
| `--all-packages` | Sync all workspace packages. |
| `--package <pkg>` | Sync specific package. |
| `--script <script>` | Sync PEP 723 script. |
| `--python-platform <platform>` | Platform for install. |
| `--check` | Check if env synchronized. |
| `--output-format <fmt>` | `text` or `json`. |
| `-U, --upgrade` | Allow upgrades. |
| `-P, --upgrade-package <pkg>` | Upgrade specific. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--prerelease <strategy>` | `disallow`, `allow`, `if-necessary`, `explicit`, `if-necessary-or-explicit`. |
| `--reinstall` | Reinstall all. |
| `--reinstall-package <pkg>` | Reinstall specific. |
| `--link-mode <mode>` | `clone`, `copy`, `hardlink`, `symlink`. |
| `--compile-bytecode` | Compile after install. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--refresh` | Refresh cache. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `-p, --python <python>` | Python interpreter. |

---

## uv run

Run command in project env.

```
uv run [OPTIONS] [COMMAND]
```

| flag | action |
|------|--------|
| `--extra <extra>` | Include optional extra. |
| `--all-extras` | Include all extras. |
| `--no-extra <extra>` | Exclude specific extra. |
| `--no-dev` | Skip dev deps. |
| `--group <group>` | Include dependency group. |
| `--no-group <group>` | Exclude group. |
| `--no-default-groups` | Ignore default groups. |
| `--only-group <group>` | Only specific group. |
| `--all-groups` | All groups. |
| `-m, --module` | Run Python module. |
| `--only-dev` | Only dev deps. |
| `--no-editable` | Install as non-editable. |
| `--exact` | Exact sync. Remove extraneous. |
| `--env-file <file>` | Load `.env` file. |
| `--no-env-file` | Skip `.env`. |
| `-w, --with <pkg>` | Run with extra package. |
| `--with-editable <pkg>` | Run with editable package. |
| `--with-requirements <file>` | Run with requirements file. |
| `--isolated` | Run in isolated venv. |
| `--active` | Prefer active venv. |
| `--no-sync` | Skip env sync. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Run without updating lock. |
| `-s, --script` | Run as Python script. |
| `--gui-script` | Run as Python GUI script. |
| `--all-packages` | Run with all workspace members. |
| `--package <pkg>` | Run in specific package. |
| `--no-project` | No project discovery. |
| `--python-platform <platform>` | Platform for install. |
| `-U, --upgrade` | Allow upgrades. |
| `-P, --upgrade-package <pkg>` | Upgrade specific. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--prerelease <strategy>` | `disallow`, `allow`, `if-necessary`, `explicit`, `if-necessary-or-explicit`. |
| `--reinstall` | Reinstall all. |
| `--reinstall-package <pkg>` | Reinstall specific. |
| `--link-mode <mode>` | `clone`, `copy`, `hardlink`, `symlink`. |
| `--compile-bytecode` | Compile after install. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--refresh` | Refresh cache. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `-p, --python <python>` | Python interpreter. |

---

## uv export

Export lockfile.

```
uv export [OPTIONS]
```

| flag | action |
|------|--------|
| `--format <fmt>` | `requirements.txt`, `pylock.toml`, `cyclonedx1.5`. |
| `--all-packages` | Export entire workspace. |
| `--package <pkg>` | Export specific package. |
| `--prune <pkg>` | Prune package from tree. |
| `--extra <extra>` | Include optional extra. |
| `--all-extras` | Include all extras. |
| `--no-extra <extra>` | Exclude specific extra. |
| `--no-dev` | Skip dev deps. |
| `--only-dev` | Only dev deps. |
| `--group <group>` | Include group. |
| `--no-group <group>` | Exclude group. |
| `--no-default-groups` | Ignore default groups. |
| `--only-group <group>` | Only specific group. |
| `--all-groups` | All groups. |
| `--no-annotate` | No source comments. |
| `--no-header` | No header comment. |
| `--no-editable` | Export as non-editable. |
| `--no-hashes` | Omit hashes. |
| `-o, --output-file <file>` | Write to file. |
| `--no-emit-project` | Skip current project. |
| `--no-emit-workspace` | Skip workspace members. |
| `--no-emit-local` | Skip local path deps. |
| `--no-emit-package <pkg>` | Skip specific package. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Export without updating lock. |
| `--script <script>` | Export PEP 723 script deps. |
| `-U, --upgrade` | Allow upgrades. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |

---

## uv tree

Show dependency tree.

```
uv tree [OPTIONS]
```

| flag | action |
|------|--------|
| `--universal` | Platform-independent tree. |
| `-d, --depth <n>` | Max depth. Default 255. |
| `--prune <pkg>` | Prune package from display. |
| `--package <pkg>` | Show only specific package. |
| `--no-dedupe` | Repeat duplicate deps. |
| `--invert` | Reverse deps. Show what depends on package. |
| `--outdated` | Show latest available version. |
| `--show-sizes` | Show compressed wheel sizes. |
| `--only-dev` | Only dev deps. |
| `--no-dev` | Skip dev deps. |
| `--group <group>` | Include group. |
| `--no-group <group>` | Exclude group. |
| `--no-default-groups` | Ignore default groups. |
| `--only-group <group>` | Only specific group. |
| `--all-groups` | All groups. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Display without locking. |
| `--script <script>` | Show tree for PEP 723 script. |
| `--python-version <ver>` | Filter by Python version. |
| `--python-platform <platform>` | Filter by platform. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `-U, --upgrade` | Allow upgrades. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `-p, --python <python>` | Python interpreter. |

---

## uv version

Read or update project version.

```
uv version [OPTIONS] [VALUE]
```

| flag | action |
|------|--------|
| `[VALUE]` | Set version to this value. |
| `--bump <bump>` | Bump: `major`, `minor`, `patch`, `stable`, `alpha`, `beta`, `rc`, `post`, `dev`. |
| `--dry-run` | No write. |
| `--short` | Only show version string. |
| `--output-format <fmt>` | `text` or `json`. |
| `--no-sync` | Skip env sync. |
| `--active` | Prefer active venv. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Update without re-locking. |
| `--package <pkg>` | Target workspace package. |
| `-U, --upgrade` | Allow upgrades. |
| `--resolution <strategy>` | `highest`, `lowest`, `lowest-direct`. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `-p, --python <python>` | Python interpreter. |

---

## uv format

Format Python code. Uses Ruff.

```
uv format [OPTIONS] [-- <EXTRA_ARGS>...]
```

| flag | action |
|------|--------|
| `--check` | Check only. No write. |
| `--diff` | Show diff. No write. |
| `--version <ver>` | Ruff version to use. |
| `--exclude-newer <date>` | Limit Ruff version by date. |
| `--no-project` | No project discovery. |

---

## uv audit

Audit dependencies for vulnerabilities.

```
uv audit [OPTIONS]
```

| flag | action |
|------|--------|
| `--no-extra <extra>` | Skip specific extra. |
| `--no-dev` | Skip dev deps. |
| `--no-group <group>` | Skip group. |
| `--no-default-groups` | Skip default groups. |
| `--only-group <group>` | Only specific group. |
| `--only-dev` | Only dev deps. |
| `--locked` | Assert lockfile unchanged. |
| `--frozen` | Audit without locking. |
| `--script <script>` | Audit PEP 723 script. |
| `--python-version <ver>` | Filter by Python version. |
| `--python-platform <platform>` | Filter by platform. |
| `--ignore <id>` | Ignore vulnerability by ID. |
| `--ignore-until-fixed <id>` | Ignore until fix available. |
| `--service-format <fmt>` | `osv` (default). |
| `--service-url <url>` | Custom vulnerability API. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `-U, --upgrade` | Allow upgrades. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `-p, --python <python>` | Python interpreter. |

---

## uv tool

Manage CLI tools. pipx replacement.

```
uv tool [OPTIONS] <COMMAND>
```

| subcommand | action |
|------------|--------|
| `uv tool run <pkg>` | Run tool in ephemeral env. Alias: `uvx`. |
| `uv tool install <pkg>` | Install tool globally. |
| `uv tool upgrade <pkg>` | Upgrade installed tool. |
| `uv tool list` | List installed tools. |
| `uv tool uninstall <pkg>` | Uninstall tool. |
| `uv tool update-shell` | Ensure tool dir on PATH. |
| `uv tool dir` | Show tool directory path. |

---

## uv python

Manage Python versions. pyenv replacement.

```
uv python [OPTIONS] <COMMAND>
```

| subcommand | action |
|------------|--------|
| `uv python list` | List available Python installations. |
| `uv python install <ver>` | Download and install Python. |
| `uv python upgrade` | Upgrade installed Pythons. |
| `uv python find` | Search for Python installation. |
| `uv python pin <ver>` | Pin Python version. |
| `uv python dir` | Show Python installation directory. |
| `uv python uninstall <ver>` | Uninstall Python versions. |
| `uv python update-shell` | Ensure Python dir on PATH. |

---

## uv pip

Pip-compatible interface. Legacy only.

```
uv pip [OPTIONS] <COMMAND>
```

| subcommand | action |
|------------|--------|
| `uv pip compile <in> -o <out>` | Compile requirements.in to requirements.txt. |
| `uv pip sync <file>` | Sync env with requirements file. |
| `uv pip install <pkg>` | Install packages. |
| `uv pip uninstall <pkg>` | Uninstall packages. |
| `uv pip freeze` | List installed in requirements format. |
| `uv pip list` | List installed in table format. |
| `uv pip show <pkg>` | Show package info. |
| `uv pip tree` | Dependency tree. |
| `uv pip check` | Verify compatible deps. |

---

## uv venv

Create virtual environment.

```
uv venv [OPTIONS] [PATH]
```

| flag | action |
|------|--------|
| `[PATH]` | Venv path. Default `.venv`. |
| `--no-project` | No project discovery. |
| `--seed` | Install pip/setuptools/wheel. |
| `-c, --clear` | Remove existing at target. |
| `--allow-existing` | Preserve existing files. |
| `--prompt <text>` | Custom prompt prefix. |
| `--system-site-packages` | Access system site-packages. |
| `--relocatable` | Make venv relocatable. |
| `--index-strategy <strategy>` | `first-index`, `unsafe-first-match`, `unsafe-best-match`. |
| `--keyring-provider <provider>` | `disabled`, `subprocess`. |
| `--exclude-newer <date>` | Limit packages by date. |
| `--link-mode <mode>` | `clone`, `copy`, `hardlink`, `symlink`. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `-p, --python <python>` | Python interpreter. |

---

## uv build

Build wheels and sdists.

```
uv build [OPTIONS] [SRC]
```

| flag | action |
|------|--------|
| `[SRC]` | Source dir or sdist archive. Default cwd. |
| `--package <pkg>` | Build specific workspace package. |
| `--all-packages` | Build all workspace packages. |
| `-o, --out-dir <dir>` | Output directory. |
| `--sdist` | Build source distribution only. |
| `--wheel` | Build wheel only. |
| `--no-build-logs` | Hide build backend logs. |
| `--force-pep517` | Always use PEP 517. |
| `--clear` | Clear output dir before build. |
| `--no-create-gitignore` | Skip `.gitignore` in output. |
| `-b, --build-constraints <file>` | Constrain build deps. |
| `--require-hashes` | Require matching hashes. |
| `--no-verify-hashes` | Skip hash validation. |
| `-C, --config-setting <key=val>` | PEP 517 backend settings. |
| `--no-build-isolation` | Disable build isolation. |
| `--no-build` | Skip source dist builds. |
| `--no-binary` | Skip wheels. |
| `--index <url>` | Extra index. |
| `--default-index <url>` | Default index. |
| `--no-index` | Ignore registry. |
| `-p, --python <python>` | Python interpreter. |

---

## uv publish

Upload to index.

```
uv publish [OPTIONS] [FILES]...
```

| flag | action |
|------|--------|
| `[FILES]...` | Files to upload. Default `dist/*`. |
| `--index <name>` | Index name from config. |
| `-u, --username <user>` | Username. |
| `-p, --password <pass>` | Password. |
| `-t, --token <token>` | Token. |
| `--trusted-publishing <mode>` | `automatic`, `always`, `never`. |
| `--keyring-provider <provider>` | `disabled`, `subprocess`. |
| `--publish-url <url>` | Upload endpoint URL. |
| `--check-url <url>` | Check index for duplicates. |
| `--dry-run` | No upload. |
| `--no-attestations` | Skip attestations. |

---

## uv help

Display command docs.

```
uv help [OPTIONS] [COMMAND]...
```

| flag | action |
|------|--------|
| `--no-pager` | Disable pager. |

---

## Agent Recipes

Daily commands for code work.

```bash
# new project
uv init --app myproject
cd myproject

# add dependency
uv add requests

# add dev dependency
uv add --dev pytest

# add optional extra
uv add --optional "redis" redis-py

# add from git
uv add git+https://github.com/user/package.git --rev main

# lock only. no install.
uv lock

# sync env with lockfile
uv sync

# sync without dev deps
uv sync --no-dev

# dry run sync. review changes.
uv sync --dry-run

# check if env is synced
uv sync --check

# run script in project env
uv run python script.py

# run module
uv run -m pytest

# run with extra deps
uv run --with jupyter notebook.ipynb

# run in isolated env
uv run --isolated python script.py

# export requirements.txt
uv export -o requirements.txt

# export without dev deps
uv export --no-dev -o requirements.txt

# show dependency tree
uv tree

# show outdated deps
uv tree --outdated

# show reverse deps
uv tree --invert --package requests

# bump version
uv version --bump patch

# set version
uv version 1.2.3

# format all code
uv format

# check formatting in CI
uv format --check

# audit deps
uv audit

# install global tool
uv tool install black

# run tool without install
uvx black file.py
uv tool run black file.py

# list installed Pythons
uv python list

# install Python
uv python install 3.12

# pin Python version
uv python pin 3.12

# create venv
uv venv .venv

# create venv with specific Python
uv venv -p 3.12

# build wheel and sdist
uv build

# build wheel only
uv build --wheel

# publish to PyPI
uv publish

# dry run publish
uv publish --dry-run

# clean cache
uv cache clean

# update uv
uv self update

# legacy: compile requirements
uv pip compile requirements.in -o requirements.txt

# legacy: sync from requirements
uv pip sync requirements.txt

# offline mode
uv sync --offline

# no progress bars in CI
uv sync --no-progress --quiet

# use specific Python
uv run -p 3.11 python script.py

# workspace: sync all packages
uv sync --all-packages

# workspace: add dep to specific package
uv add --package subpkg requests
```
