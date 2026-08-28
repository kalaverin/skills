---
---

# Pathlib

Make `pathlib.Path` the single currency for filesystem paths: one object carries construction, joining, decomposition, inspection, mutation, globbing, and I/O — `os.path` string functions and the `glob`/`py.path` modules never appear.

## Rule of thumb

1. Convert strings to `Path` once at the boundary and pass `Path` objects everywhere inside; join with `/` and decompose with `.name`, `.parent`, `.stem`, `.suffix`, and `.parts` — never `os.path.join`/`basename`/`dirname`/`splitext` or manual `split(os.sep)`.
2. Ask the object every question: `.exists()`, `.is_dir()`, `.is_file()`, `.is_symlink()`, `.is_absolute()`, `.samefile()`, and one `.stat()` for all `st_*` fields instead of one `os.path` function per fact.
3. Mutate through the object: `.mkdir(parents=True, exist_ok=True)`, `.rename()`, `.replace()`, `.unlink(missing_ok=True)`, `.rmdir()`, `.chmod()`, and `Path(link).symlink_to(target)` — note the flipped argument order against `os.symlink(src, dst)`.
4. Anchor glob patterns on a directory `Path` with `.glob()`/`.rglob()` and list directories with `.iterdir()`; remember `Path.glob` includes hidden files, is lazy, and needs no `recursive=True` for `**`.
5. Open and slurp through the path: `.open()`, `.read_text()`, `.write_text()`; get the working directory from `Path.cwd()`; drop the maintenance-mode `py.path` dependency entirely.
6. Know the semantic deltas before migrating: `.resolve()` follows symlinks (`os.path.abspath` does not), `.expanduser()` raises `RuntimeError` when home is unresolvable, and `.name`/`.parent` normalize duplicate slashes, trailing slashes, and `.` components.
7. Never use `os.path.commonprefix` for paths — it compares characters, not components; use `os.path.commonpath`, and always pass a dot-prefixed suffix to `.with_suffix()`.

## Example: Path construction and decomposition

A report locator that builds every path by string surgery and fumbles a suffix rename.

### Bad

```python
"""Locate and rename monthly reports."""

import os
from pathlib import Path

ROOT_PATH = "/srv/reports"


def locate_report(month):
    config_path = os.path.join(os.path.join(ROOT_PATH, "config"), "app.toml")  # PTH118
    work_dir = Path(".")  # PTH201
    raw = os.path.join(ROOT_PATH, month + ".csv")  # PTH118
    filename = os.path.basename(raw)  # PTH119
    parent = os.path.dirname(raw)  # PTH120
    root, ext = os.path.splitext(filename)  # PTH122
    parts = raw.split(os.sep)  # PTH206
    return work_dir, config_path, filename, parent, root, ext, parts


def shared_root(paths):
    # Returns "/srv/re" for ["/srv/reports", "/srv/releases"] — not a directory!
    return os.path.commonprefix(paths)  # RUF071


def as_markdown(path):
    return Path(path).with_suffix(".")  # PTH210
```

### Good

```python
"""Locate and rename monthly reports."""

import os
from pathlib import Path

ROOT_PATH = Path("/srv/reports")


def locate_report(month):
    config_path = ROOT_PATH / "config" / "app.toml"
    work_dir = Path()
    raw = ROOT_PATH / f"{month}.csv"
    filename = raw.name
    parent = raw.parent
    root = raw.parent / raw.stem
    ext = raw.suffix
    parts = raw.parts
    return work_dir, config_path, filename, parent, root, ext, parts


def shared_root(paths):
    # Compares path components: returns "/srv" for ["/srv/reports", "/srv/releases"].
    return os.path.commonpath(paths)


def as_markdown(path):
    return Path(path).with_suffix(".md")
```

### Violations

1. **PTH118** — `os.path.join(os.path.join(ROOT_PATH, "config"), "app.toml")` and `os.path.join(ROOT_PATH, month + ".csv")`; nested string joins read inside-out and stay dumb strings — chain `/` on a `Path`.
2. **PTH119** — `os.path.basename(raw)`; the final component is the `.name` property of a `Path`.
3. **PTH120** — `os.path.dirname(raw)`; `.parent` chains naturally and stays a `Path` instead of a string needing re-wrapping.
4. **PTH122** — `os.path.splitext(filename)`; the "root" conflates directory and stem — pick exactly what you mean from `.parent`, `.stem`, `.suffix`.
5. **PTH201** — `Path(".")`; the `Path()` constructor already defaults to the current directory.
6. **PTH206** — `raw.split(os.sep)`; manual separator splitting reinvents `.name`, `.parent.name`, and `.parts`, keeping empty/`.` artifacts.
7. **PTH210** — `path.with_suffix(".")`; a bare dot is an invalid suffix (a dotless `"md"` raises before Python 3.14) — pass a dot-prefixed suffix.
8. **RUF071** — `os.path.commonprefix(paths)`; compares characters, not path components, so it returns fragments of no real directory (deprecated in Python 3.15) — use `os.path.commonpath`.

## Example: Path inspection

A cache validator that interrogates every file through one-off `os.path` string functions.

### Bad

```python
"""Validate cached dumps before serving them."""

import os

CACHE = "/var/cache/dumps"


def describe_dump(name):
    full = os.path.abspath(os.path.join("..", "cache", name))  # PTH100,PTH118
    home_cfg = os.path.expanduser("~/dumps/config.toml")  # PTH111
    if not os.path.exists(full):  # PTH110
        return None
    if os.path.isdir(full):  # PTH112
        return None
    if not os.path.isfile(full):  # PTH113
        return None
    if os.path.islink(full):  # PTH114
        return None
    size = os.path.getsize(full)  # PTH202
    accessed = os.path.getatime(full)  # PTH203
    modified = os.path.getmtime(full)  # PTH204
    created = os.path.getctime(full)  # PTH205
    same = os.path.samefile(full, home_cfg)  # PTH121
    return size, accessed, modified, created, same


def resolve(name):
    if not os.path.isabs(name):  # PTH117
        name = os.path.join(CACHE, name)  # PTH118
    return name
```

### Good

```python
"""Validate cached dumps before serving them."""

from pathlib import Path

CACHE = Path("/var/cache/dumps")


def describe_dump(name):
    full = (Path("..") / "cache" / name).resolve()
    home_cfg = Path("~/dumps/config.toml").expanduser()
    if not full.exists() or full.is_dir() or not full.is_file():
        return None
    if full.is_symlink():
        return None
    stat = full.stat()
    same = full.samefile(home_cfg)
    return stat.st_size, stat.st_atime, stat.st_mtime, stat.st_ctime, same


def resolve(name):
    file_path = Path(name)
    if not file_path.is_absolute():
        file_path = CACHE / file_path
    return file_path
```

### Violations

1. **PTH100** — `os.path.abspath(...)`; use `Path.resolve()` — delta: `resolve()` also follows symlinks and removes `..`, so pick `Path.absolute()` only when symlink resolution must be avoided.
2. **PTH110** — `os.path.exists(full)`; existence is a method on the path object.
3. **PTH111** — `os.path.expanduser("~/dumps/config.toml")`; `Path.expanduser()` does the same job — delta: it raises `RuntimeError` when the home directory is unresolvable instead of silently returning the input.
4. **PTH112** — `os.path.isdir(full)`; the type test belongs on the `Path` and composes with iteration and joining on the same object.
5. **PTH113** — `os.path.isfile(full)`; the check is a method whose result feeds straight into `.open()`/`.read_text()` on the same object.
6. **PTH114** — `os.path.islink(full)`; `.is_symlink()` names the concept precisely.
7. **PTH117** — `os.path.isabs(name)`; `.is_absolute()` checks the path's shape without touching the filesystem, and the fix-up join becomes `/`.
8. **PTH121** — `os.path.samefile(full, home_cfg)`; identity-by-inode is a method on one path against another.
9. **PTH202** — `os.path.getsize(full)`; one `Path.stat()` exposes the full `os.stat_result` including `st_size`.
10. **PTH203** — `os.path.getatime(full)`; `.stat().st_atime` replaces a dedicated string function per stat field.
11. **PTH204** — `os.path.getmtime(full)`; `.stat().st_mtime` for freshness checks.
12. **PTH205** — `os.path.getctime(full)`; `.stat().st_ctime` — metadata-change time on Unix, creation time on Windows.

## Example: Filesystem mutation

A deploy script that drives every filesystem change through `os` module functions on raw strings.

### Bad

```python
"""Deploy a build artifact and clean up afterwards."""

import os


def deploy(artifact):
    os.makedirs("./dist/releases/", exist_ok=True)  # PTH103
    os.mkdir("./dist/tmp")  # PTH102
    os.rename(artifact, "./dist/tmp/app.bin")  # PTH104
    os.replace("./dist/tmp/app.bin", "./dist/releases/app.bin")  # PTH105
    os.chmod("./dist/releases/app.bin", 0o755)  # PTH101


def cleanup():
    if os.path.exists("./dist/tmp/app.lock"):  # PTH110
        os.remove("./dist/tmp/app.lock")  # PTH107
    try:
        os.unlink("./dist/tmp/app.pid")  # PTH108
    except FileNotFoundError:
        pass
    os.rmdir("./dist/tmp")  # PTH106
```

### Good

```python
"""Deploy a build artifact and clean up afterwards."""

from pathlib import Path

DIST = Path("./dist")


def deploy(artifact):
    releases = DIST / "releases"
    tmp = DIST / "tmp"
    releases.mkdir(parents=True, exist_ok=True)
    tmp.mkdir()
    staged = Path(artifact).rename(tmp / "app.bin")
    final = staged.replace(releases / "app.bin")
    final.chmod(0o755)


def cleanup():
    tmp = DIST / "tmp"
    (tmp / "app.lock").unlink(missing_ok=True)
    (tmp / "app.pid").unlink(missing_ok=True)
    tmp.rmdir()
```

### Violations

1. **PTH101** — `os.chmod("./dist/releases/app.bin", 0o755)`; permission change is `Path.chmod()`, keeping the octal mode attached to its object.
2. **PTH102** — `os.mkdir("./dist/tmp")`; directory creation is `Path.mkdir()`, which composes with `parents=`/`exist_ok=` instead of try/except wrappers.
3. **PTH103** — `os.makedirs("./dist/releases/", exist_ok=True)`; recursive creation is the same method with `parents=True` — one API covers both.
4. **PTH104** — `os.rename(artifact, ...)`; the source path is the natural subject — delta: `Path.rename()` returns the target `Path`, not `None`.
5. **PTH105** — `os.replace("./dist/tmp/app.bin", ...)`; atomic overwrite reads as a method on the source and also returns the target `Path`.
6. **PTH106** — `os.rmdir("./dist/tmp")`; removal of an empty directory is `Path.rmdir()` — for non-empty trees reach for `shutil.rmtree`.
7. **PTH107** — `os.remove("./dist/tmp/app.lock")`; `Path.unlink()` offers `missing_ok=True` to skip the existence guard entirely.
8. **PTH108** — `os.unlink("./dist/tmp/app.pid")`; alias of `os.remove` with the same method-form replacement.

## Example: Symlinks and ownership

A release switcher that creates a symlink with swapped-looking arguments and decodes ownership by hand.

### Bad

```python
"""Point the 'current' symlink at the newest release."""

import os
from grp import getgrgid
from pwd import getpwuid


def switch_release(release):
    # os.symlink(src, dst): target first, link name second — easy to swap.
    os.symlink(release, "releases/current", target_is_directory=False)  # PTH211
    return os.readlink("releases/current")  # PTH115


def who_owns(path):
    stat = os.stat(path)  # PTH116
    owner_name = getpwuid(stat.st_uid).pw_name
    group_name = getgrgid(stat.st_gid).gr_name
    return owner_name, group_name, stat.st_mode
```

### Good

```python
"""Point the 'current' symlink at the newest release."""

from pathlib import Path


def switch_release(release):
    # Path(link).symlink_to(target): the link being created is the subject.
    current = Path("releases/current")
    current.symlink_to(release)
    return current.readlink()


def who_owns(path):
    file_path = Path(path)
    return file_path.owner(), file_path.group(), file_path.stat().st_mode
```

### Violations

1. **PTH115** — `os.readlink("releases/current")`; reading a link's target is `Path.readlink()`, which returns a chainable `Path` instead of `str`/`bytes`.
2. **PTH116** — `os.stat(path)` plus the `pwd`/`grp` lookup dance; `Path.owner()`/`Path.group()` collapse it to one method each, and raw fields come from `Path.stat()`.
3. **PTH211** — `os.symlink(release, "releases/current", target_is_directory=False)`; the argument order flips — `Path(dst).symlink_to(src)` puts the link being created in subject position and prevents swapped-argument bugs.

## Example: Listing, globbing, and file I/O

A log collector that globs joined pattern strings, re-joins bare names from `listdir`, opens by string, and still depends on `py.path`.

### Bad

```python
"""Collect and merge log fragments."""

import glob
import os

import py.path


def collect_logs():
    cwd = os.getcwd()  # PTH109
    root = py.path.local(cwd).join("logs")  # PTH124
    fragments = glob.glob(os.path.join(str(root), "fragment*.log"))  # PTH118,PTH207
    recursive = glob.glob("logs/**/*.log", recursive=True)  # PTH207
    for name in os.listdir("logs"):  # PTH208
        full = os.path.join("logs", name)  # PTH118
        with open(full) as fp:  # PTH123
            yield fp.read()
```

### Good

```python
"""Collect and merge log fragments."""

from pathlib import Path


def collect_logs():
    logs = Path.cwd() / "logs"
    fragments = sorted(logs.glob("fragment*.log"))
    recursive = sorted(logs.rglob("*.log"))
    for child in logs.iterdir():
        with child.open() as fp:
            yield fp.read()
```

### Violations

1. **PTH109** — `os.getcwd()`; the current directory is a path — `Path.cwd()` returns it ready to join (also covers `os.getcwdb`, which has no `pathlib` bytes variant by design).
2. **PTH123** — `open(full)`; opening is an operation on the path — `Path.open()`, and whole-file slurps collapse to `.read_text()`/`.read_bytes()`.
3. **PTH124** — `py.path.local(cwd).join("logs")`; `py.path` is in maintenance mode — the stdlib already provides the same object model.
4. **PTH207** — `glob.glob(os.path.join(str(root), "fragment*.log"))` and `glob.glob("logs/**/*.log", recursive=True)`; anchor the pattern on a directory `Path` — deltas: `Path.glob` includes hidden files, is always lazy, and `**` needs no `recursive=True`.
5. **PTH208** — `os.listdir("logs")`; yields bare names that must be re-joined — `iterdir()` yields ready `Path` objects, and emptiness/membership tests read better as `any(p.iterdir())` / `(p / "file").exists()`.
