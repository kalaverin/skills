"""Export of nimdoc JSON artifacts for Nim modules."""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import structlog

from transformer import models, storage

if TYPE_CHECKING:
    from transformer import config

logger = structlog.get_logger(__name__)

_JSONDOC_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class ExportError:
    """A structured ``nim jsondoc`` failure for one module."""

    module_ref: models.ModuleRef
    returncode: int | None
    stderr: str
    exception: str | None


@dataclass(frozen=True)
class ExportResult:
    """The outcome of ensuring a JSON artifact for one module."""

    success: bool
    content_object: models.ContentObject | None
    error: ExportError | None


def export_json(
    scanned: models.ScannedModule,
    settings: config.Settings,
) -> ExportResult:
    """Ensure a JSON object exists for the module and point generated.json.z to it.

    Runs ``nim jsondoc`` only when the content object for the module's
    source hash is missing; otherwise just repairs the pointer.

    Args:
        scanned: The module to export, with its source hash.
        settings: Validated transformer settings.

    Returns:
        An export result carrying either the content object or the error.
    """
    module_ref = scanned.module_ref
    cache_root = settings.cache_root
    pointer = storage.pointer_path(
        module_ref, models.ArtifactType.GENERATED_JSON, cache_root,
    )
    if storage.object_exists(scanned.source_hash, cache_root):
        if storage.read_pointer(pointer) != scanned.source_hash:
            storage.update_pointer(pointer, scanned.source_hash)
        logger.info("json_cache_hit", source_path=module_ref.source_path)
        return ExportResult(
            success=True,
            content_object=models.ContentObject(
                hash=scanned.source_hash,
                object_path=storage.object_path(
                    scanned.source_hash, cache_root,
                ),
            ),
            error=None,
        )
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_json = Path(tmp_dir) / f"{module_ref.module_name}.json"
        command = [
            str(settings.nim_bin),
            "jsondoc",
            "--noImportdoc",
        ]
        if module_ref.backend == models.Backend.JS:
            command.append("--backend:js")
        command.extend([f"-o:{output_json}", module_ref.source_path])
        failure = _run_jsondoc(command, scanned, settings, output_json)
        if failure is not None:
            return failure
        try:
            raw_json = output_json.read_bytes()
        except OSError as exc:
            return ExportResult(
                success=False,
                content_object=None,
                error=ExportError(
                    module_ref=module_ref,
                    returncode=None,
                    stderr="",
                    exception=str(exc),
                ),
            )
    content_object = storage.write_object(
        scanned.source_hash, raw_json, cache_root,
    )
    storage.update_pointer(pointer, scanned.source_hash)
    logger.info("json_exported", source_path=module_ref.source_path)
    return ExportResult(
        success=True, content_object=content_object, error=None,
    )


def _run_jsondoc(
    command: list[str],
    scanned: models.ScannedModule,
    settings: config.Settings,
    output_json: Path,
) -> ExportResult | None:
    """Run the jsondoc subprocess; return an ExportResult on failure."""
    module_ref = scanned.module_ref
    try:
        # Trusted input: the validated nim binary and repo-relative paths.
        completed = subprocess.run(  # noqa: S603
            command,
            cwd=settings.repo_root,
            capture_output=True,
            text=True,
            timeout=_JSONDOC_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return ExportResult(
            success=False,
            content_object=None,
            error=ExportError(
                module_ref=module_ref,
                returncode=None,
                stderr="",
                exception=f"TimeoutExpired after {_JSONDOC_TIMEOUT_SECONDS}s: {exc}",
            ),
        )
    except OSError as exc:
        return ExportResult(
            success=False,
            content_object=None,
            error=ExportError(
                module_ref=module_ref,
                returncode=None,
                stderr="",
                exception=str(exc),
            ),
        )
    if completed.returncode != 0:
        logger.warning(
            "jsondoc_failed",
            source_path=module_ref.source_path,
            returncode=completed.returncode,
        )
        return ExportResult(
            success=False,
            content_object=None,
            error=ExportError(
                module_ref=module_ref,
                returncode=completed.returncode,
                stderr=completed.stderr,
                exception=None,
            ),
        )
    if not output_json.is_file():
        return ExportResult(
            success=False,
            content_object=None,
            error=ExportError(
                module_ref=module_ref,
                returncode=completed.returncode,
                stderr=completed.stderr,
                exception=f"jsondoc produced no file: {output_json}",
            ),
        )
    return None
