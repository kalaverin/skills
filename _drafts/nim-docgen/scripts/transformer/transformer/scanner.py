"""Discovery of Nim source modules and content hashing."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import structlog
import xxhash

from transformer import models

if TYPE_CHECKING:
    from collections.abc import Sequence

    from transformer import config

logger = structlog.get_logger(__name__)

_SKIP_DIRS = frozenset({"includes", "deprecated", "genode"})


def discover(settings: config.Settings) -> Sequence[models.ScannedModule]:
    """Return all documented modules sorted by source_path.

    Walks ``lib/`` plus ``nimsuggest/sexp.nim`` when present, skipping
    include/deprecated/genode directories, non-``.nim`` files, and the
    configured crashers. Unreadable files are logged and skipped.

    Args:
        settings: Validated transformer settings.

    Returns:
        Immutable sequence of scanned modules sorted by source path.
    """
    discovered: list[models.ScannedModule] = []
    lib_root = settings.repo_root / "lib"
    for dirpath, dirnames, filenames in os.walk(lib_root):
        dirnames[:] = [name for name in dirnames if name not in _SKIP_DIRS]
        for filename in filenames:
            if not filename.endswith(".nim"):
                continue
            absolute = Path(dirpath) / filename
            relative = absolute.relative_to(settings.repo_root).as_posix()
            if relative in settings.excluded_modules:
                continue
            scanned = _build_scanned(absolute, relative, settings)
            if scanned is not None:
                discovered.append(scanned)
    sexp = settings.repo_root / "nimsuggest" / "sexp.nim"
    if sexp.is_file():
        scanned = _build_scanned(sexp, "nimsuggest/sexp.nim", settings)
        if scanned is not None:
            discovered.append(scanned)
    logger.info("modules_discovered", count=len(discovered))
    return tuple(
        sorted(discovered, key=lambda item: item.module_ref.source_path),
    )


def compute_source_hash(source_path: Path) -> str:
    """Return a 16-character hex xxhash64 of the file bytes.

    Args:
        source_path: Absolute path to the source file.

    Returns:
        Lowercase hex digest, exactly 16 characters.
    """
    return xxhash.xxh64(source_path.read_bytes()).hexdigest()


def select_backend(
    source_path: Path,
    js_modules: frozenset[str],
) -> models.Backend:
    """Return JS for JS-only modules, otherwise NATIVE.

    Args:
        source_path: Repository-relative module path.
        js_modules: Repository-relative paths of known JS modules.

    Returns:
        The backend matching the module location.
    """
    posix = source_path.as_posix()
    if posix in js_modules or posix.startswith("lib/js/"):
        return models.Backend.JS
    return models.Backend.NATIVE


def _build_scanned(
    absolute: Path,
    relative: str,
    settings: config.Settings,
) -> models.ScannedModule | None:
    """Hash one file and build its `ScannedModule`, or None on read errors."""
    try:
        source_hash = compute_source_hash(absolute)
    except OSError as exc:
        logger.exception(
            "module_unreadable",
            source_path=relative,
            error=str(exc),
        )
        return None
    module_ref = models.ModuleRef(
        source_path=relative,
        module_name=absolute.stem,
        backend=select_backend(Path(relative), settings.js_modules),
        package=_derive_package(relative),
    )
    return models.ScannedModule(module_ref=module_ref, source_hash=source_hash)


def _derive_package(relative: str) -> str:
    """Return the logical package name for a repository-relative path."""
    if relative.startswith("lib/"):
        return "stdlib"
    return relative.split("/", maxsplit=1)[0]
