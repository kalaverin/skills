"""Content-addressed cache with hardlink pointer storage."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import structlog
import xxhash
import zstandard

from transformer import models

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, Sequence

logger = structlog.get_logger(__name__)

_POINTER_FILENAMES: Mapping[models.ArtifactType, str] = {
    models.ArtifactType.GENERATED_JSON: "generated.json.z",
    models.ArtifactType.GENERATED_HTML: "generated.html.z",
    models.ArtifactType.EXAMPLES_JSON: "examples.json.z",
}


def object_path(hash: str, cache_root: Path) -> Path:  # noqa: A002
    """Return ``.tmp/cache/objects/<first_3>/<remaining_13>``."""
    return cache_root / "objects" / hash[:3] / hash[3:]


def object_exists(hash: str, cache_root: Path) -> bool:  # noqa: A002
    """Check whether a content object already exists."""
    return object_path(hash, cache_root).is_file()


def read_object(hash: str, cache_root: Path) -> bytes:  # noqa: A002
    """Read and decompress a content object.

    Args:
        hash: 16-character hex content hash.
        cache_root: Cache root directory.

    Returns:
        The decompressed object bytes.
    """
    compressed = object_path(hash, cache_root).read_bytes()
    return zstandard.ZstdDecompressor().decompress(compressed)


def write_object(
    hash: str,  # noqa: A002
    data: bytes,
    cache_root: Path,
) -> models.ContentObject:
    """Compress and atomically write a content object.

    Existing objects are never overwritten; content addressing makes
    concurrent writes of the same hash identical by construction.

    Args:
        hash: 16-character hex content hash.
        data: Raw uncompressed payload.
        cache_root: Cache root directory.

    Returns:
        The content object descriptor for the stored payload.
    """
    path = object_path(hash, cache_root)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        compressed = zstandard.ZstdCompressor().compress(data)
        _atomic_write_bytes(path, compressed)
    return models.ContentObject(hash=hash, object_path=path)


def artifact_object_hash(
    source_hash: str,
    artifact_type: models.ArtifactType,
) -> str:
    """Return the deterministic object hash for a module artifact.

    The JSON artifact is addressed by the source hash itself. Derived
    artifacts (HTML, examples) share the module's source hash and must
    be discriminated; otherwise their objects would collide with the
    JSON object in the content-addressed store.
    """
    if artifact_type == models.ArtifactType.GENERATED_JSON:
        return source_hash
    suffix = _POINTER_FILENAMES[artifact_type]
    return xxhash.xxh64(f"{source_hash}:{suffix}".encode()).hexdigest()


def pointer_path(
    module_ref: models.ModuleRef,
    artifact_type: models.ArtifactType,
    cache_root: Path,
) -> Path:
    """Return the stable hardlink path for a module artifact.

    Example: ``.tmp/cache/lib/std/enumutils/generated.json.z``.
    """
    stem = module_ref.source_path.removesuffix(".nim")
    return cache_root / stem / _POINTER_FILENAMES[artifact_type]


def read_pointer(pointer: Path) -> str | None:
    """Return the hash the pointer currently references, or None if missing.

    The pointer is a hardlink, so the target hash is recovered by finding
    the object file that shares the pointer's inode.
    """
    if not pointer.is_file():
        return None
    cache_root = _cache_root_for(pointer)
    if cache_root is None:
        return None
    target_inode = pointer.stat().st_ino
    for inode, candidate in _object_inodes(cache_root / "objects"):
        if inode == target_inode:
            return candidate
    return None


def update_pointer(pointer: Path, hash: str) -> None:  # noqa: A002
    """Atomically repoint a hardlink to the given hash object.

    Args:
        pointer: Stable pointer path inside the cache tree.
        hash: Hash of an existing content object.

    Raises:
        ValueError: If the cache root or the content object is missing.
    """
    cache_root = _cache_root_for(pointer)
    if cache_root is None:
        msg = f"cannot locate cache root for pointer: {pointer}"
        raise ValueError(msg)
    source = object_path(hash, cache_root)
    if not source.is_file():
        msg = f"content object missing for hash: {hash}"
        raise ValueError(msg)
    pointer.parent.mkdir(parents=True, exist_ok=True)
    temporary = pointer.with_name(pointer.name + ".tmp")
    temporary.unlink(missing_ok=True)
    os.link(source, temporary)
    temporary.replace(pointer)


def write_text(path: Path, content: str) -> None:
    """Write uncompressed UTF-8 text atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_bytes(path, content.encode("utf-8"))


def read_text(path: Path) -> str:
    """Read uncompressed UTF-8 text."""
    return path.read_text(encoding="utf-8")


def collect_orphans(cache_root: Path) -> Sequence[Path]:
    """Delete objects with ``st_nlink == 1`` and return the removed paths."""
    removed: list[Path] = []
    objects_root = cache_root / "objects"
    if not objects_root.is_dir():
        return ()
    for shard in sorted(objects_root.iterdir()):
        if not shard.is_dir():
            continue
        for entry in sorted(shard.iterdir()):
            if entry.is_file() and entry.stat().st_nlink == 1:
                entry.unlink()
                removed.append(entry)
        if not any(shard.iterdir()):
            shard.rmdir()
    logger.info("cache_orphans_collected", count=len(removed))
    return tuple(removed)


def remove_stale_parts(
    output_dir: Path,
    stem: str,
    current_part_count: int,
) -> Sequence[Path]:
    """Remove part files that no longer match the current split count.

    Args:
        output_dir: Directory containing the module's Markdown files.
        stem: File stem of the module (e.g. ``enumutils``).
        current_part_count: 1 for a single page, N for a split module.

    Returns:
        The paths that were removed.
    """
    removed: list[Path] = []
    if current_part_count <= 1:
        for _, candidate in _numbered_parts(output_dir, stem):
            candidate.unlink()
            removed.append(candidate)
    else:
        single = output_dir / f"{stem}.md"
        if single.is_file():
            single.unlink()
            removed.append(single)
        for number, candidate in _numbered_parts(output_dir, stem):
            if number > current_part_count:
                candidate.unlink()
                removed.append(candidate)
    return tuple(removed)


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    """Write bytes to a temporary sibling and atomically replace the target."""
    fd, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _cache_root_for(pointer: Path) -> Path | None:
    """Return the nearest ancestor of a pointer that contains ``objects/``."""
    for parent in pointer.parents:
        if (parent / "objects").is_dir():
            return parent
    return None


def _object_inodes(objects_root: Path) -> Iterator[tuple[int, str]]:
    """Yield ``(inode, hash)`` pairs for every file in the object store."""
    if not objects_root.is_dir():
        return
    for shard in objects_root.iterdir():
        if not shard.is_dir():
            continue
        for entry in shard.iterdir():
            if entry.is_file():
                yield entry.stat().st_ino, shard.name + entry.name


def _numbered_parts(output_dir: Path, stem: str) -> Iterator[tuple[int, Path]]:
    """Yield ``(part_number, path)`` for existing ``<stem>_<N>.md`` files."""
    for candidate in output_dir.glob(f"{stem}_*.md"):
        suffix = candidate.stem.removeprefix(f"{stem}_")
        if suffix.isdigit():
            yield int(suffix), candidate
