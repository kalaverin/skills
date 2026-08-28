"""Extraction of runnable examples from generated HTML."""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import TYPE_CHECKING, override
from urllib.parse import unquote

import orjson
import structlog

from transformer import models, storage

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from transformer import config

logger = structlog.get_logger(__name__)

_DOC_TIMEOUT_SECONDS = 180


@dataclass(frozen=True)
class ExtractionError:
    """A structured ``nim doc``/parse failure for one module."""

    module_ref: models.ModuleRef
    returncode: int | None
    stderr: str
    exception: str | None


@dataclass(frozen=True)
class ExtractionResult:
    """The outcome of ensuring HTML/examples artifacts for one module."""

    success: bool
    examples: Sequence[models.Example]
    html_object: models.ContentObject | None
    examples_object: models.ContentObject | None
    error: ExtractionError | None


def extract_examples(
    scanned: models.ScannedModule,
    settings: config.Settings,
) -> ExtractionResult:
    """Ensure HTML and examples objects exist, then return parsed examples.

    Runs ``nim doc`` only when the pointers do not already reference the
    module's current source hash.

    Args:
        scanned: The module to extract examples from.
        settings: Validated transformer settings.

    Returns:
        An extraction result with examples and optional objects/error.
    """
    module_ref = scanned.module_ref
    cache_root = settings.cache_root
    html_pointer = storage.pointer_path(
        module_ref, models.ArtifactType.GENERATED_HTML, cache_root,
    )
    examples_pointer = storage.pointer_path(
        module_ref, models.ArtifactType.EXAMPLES_JSON, cache_root,
    )
    html_object_hash = storage.artifact_object_hash(
        scanned.source_hash, models.ArtifactType.GENERATED_HTML,
    )
    examples_object_hash = storage.artifact_object_hash(
        scanned.source_hash, models.ArtifactType.EXAMPLES_JSON,
    )
    html_fresh = storage.read_pointer(html_pointer) == html_object_hash
    examples_fresh = (
        storage.read_pointer(examples_pointer) == examples_object_hash
    )
    if html_fresh and examples_fresh:
        cached = _load_cached_examples(scanned, settings, examples_pointer)
        if cached is not None:
            logger.info(
                "examples_cache_hit", source_path=module_ref.source_path,
            )
            return ExtractionResult(
                success=True,
                examples=cached,
                html_object=models.ContentObject(
                    hash=html_object_hash,
                    object_path=storage.object_path(html_object_hash, cache_root),
                ),
                examples_object=models.ContentObject(
                    hash=examples_object_hash,
                    object_path=storage.object_path(
                        examples_object_hash, cache_root,
                    ),
                ),
                error=None,
            )
    with tempfile.TemporaryDirectory() as tmp_dir:
        html_file = Path(tmp_dir) / f"{module_ref.module_name}.html"
        command = [
            str(settings.nim_bin),
            "doc",
            "--noImportdoc",
            f"--outdir:{tmp_dir}",
        ]
        if module_ref.backend == models.Backend.JS:
            command.append("--backend:js")
        command.append(module_ref.source_path)
        failure = _run_doc(command, scanned, settings, html_file)
        if failure is not None:
            return failure
        try:
            html_bytes = html_file.read_bytes()
        except OSError as exc:
            return ExtractionResult(
                success=False,
                examples=(),
                html_object=None,
                examples_object=None,
                error=ExtractionError(
                    module_ref=module_ref,
                    returncode=None,
                    stderr="",
                    exception=str(exc),
                ),
            )
    html_object = storage.write_object(
        html_object_hash, html_bytes, cache_root,
    )
    storage.update_pointer(html_pointer, html_object_hash)
    symbol_lines = _load_symbol_lines(scanned, settings)
    examples = _parse_examples(
        html_bytes.decode("utf-8", errors="replace"), symbol_lines,
    )
    examples_object = storage.write_object(
        examples_object_hash, _serialize_examples(examples), cache_root,
    )
    storage.update_pointer(examples_pointer, examples_object_hash)
    logger.info(
        "examples_extracted",
        source_path=module_ref.source_path,
        count=len(examples),
    )
    return ExtractionResult(
        success=True,
        examples=examples,
        html_object=html_object,
        examples_object=examples_object,
        error=None,
    )


def _run_doc(
    command: list[str],
    scanned: models.ScannedModule,
    settings: config.Settings,
    html_file: Path,
) -> ExtractionResult | None:
    """Run the ``nim doc`` subprocess; return an ExtractionResult on failure."""
    module_ref = scanned.module_ref
    try:
        # Trusted input: the validated nim binary and repo-relative paths.
        completed = subprocess.run(  # noqa: S603
            command,
            cwd=settings.repo_root,
            capture_output=True,
            text=True,
            timeout=_DOC_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return ExtractionResult(
            success=False,
            examples=(),
            html_object=None,
            examples_object=None,
            error=ExtractionError(
                module_ref=module_ref,
                returncode=None,
                stderr="",
                exception=f"TimeoutExpired after {_DOC_TIMEOUT_SECONDS}s: {exc}",
            ),
        )
    except OSError as exc:
        return ExtractionResult(
            success=False,
            examples=(),
            html_object=None,
            examples_object=None,
            error=ExtractionError(
                module_ref=module_ref,
                returncode=None,
                stderr="",
                exception=str(exc),
            ),
        )
    if completed.returncode != 0 or not html_file.is_file():
        logger.warning(
            "nim_doc_failed",
            source_path=module_ref.source_path,
            returncode=completed.returncode,
        )
        return ExtractionResult(
            success=False,
            examples=(),
            html_object=None,
            examples_object=None,
            error=ExtractionError(
                module_ref=module_ref,
                returncode=completed.returncode,
                stderr=completed.stderr,
                exception=None
                if html_file.is_file()
                else f"nim doc produced no file: {html_file}",
            ),
        )
    return None


def _load_symbol_lines(
    scanned: models.ScannedModule,
    settings: config.Settings,
) -> Mapping[str, int]:
    """Return ``{symbol_name: line}`` from the cached jsondoc object."""
    module_ref = scanned.module_ref
    pointer = storage.pointer_path(
        module_ref, models.ArtifactType.GENERATED_JSON, settings.cache_root,
    )
    digest = storage.read_pointer(pointer)
    if digest is None:
        return {}
    try:
        document = orjson.loads(storage.read_object(digest, settings.cache_root))
    except (OSError, orjson.JSONDecodeError) as exc:
        logger.warning(
            "jsondoc_unreadable_for_mapping",
            source_path=module_ref.source_path,
            error=str(exc),
        )
        return {}
    lines: dict[str, int] = {}
    entries = document.get("entries", []) if isinstance(document, dict) else []
    for entry in entries:
        name = entry.get("name")
        line = entry.get("line")
        if isinstance(name, str) and isinstance(line, int) and name not in lines:
            lines[name] = line
    return lines


def _parse_examples(
    html: str,
    symbol_lines: Mapping[str, int],
) -> tuple[models.Example, ...]:
    """Parse ``<pre class="listing">`` blocks into mapped examples."""
    parser = _ListingParser()
    parser.feed(html)
    parser.close()
    counters: dict[str, int] = {}
    examples: list[models.Example] = []
    for symbol, code in parser.blocks:
        order = counters.get(symbol, 0)
        counters[symbol] = order + 1
        examples.append(
            models.Example(
                code=code,
                target_symbol=symbol,
                target_line=symbol_lines.get(symbol, 0),
                order=order,
            ),
        )
    return tuple(examples)


def _serialize_examples(examples: Sequence[models.Example]) -> bytes:
    """Serialize examples to a JSON byte payload for the object store."""
    return orjson.dumps(
        [
            {
                "code": example.code,
                "target_symbol": example.target_symbol,
                "target_line": example.target_line,
                "order": example.order,
            }
            for example in examples
        ],
    )


def _deserialize_examples(raw: bytes) -> tuple[models.Example, ...]:
    """Parse the examples JSON payload back into domain models."""
    payload = orjson.loads(raw)
    return tuple(
        models.Example(
            code=str(item["code"]),
            target_symbol=str(item["target_symbol"]),
            target_line=int(item["target_line"]),
            order=int(item["order"]),
        )
        for item in payload
    )


def _load_cached_examples(
    scanned: models.ScannedModule,
    settings: config.Settings,
    examples_pointer: Path,
) -> tuple[models.Example, ...] | None:
    """Return cached examples, or None when unreadable (forces regeneration)."""
    digest = storage.read_pointer(examples_pointer)
    if digest is None:
        return None
    try:
        raw = storage.read_object(digest, settings.cache_root)
        return _deserialize_examples(raw)
    except (OSError, orjson.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        logger.warning(
            "examples_cache_unreadable",
            source_path=scanned.module_ref.source_path,
            error=str(exc),
        )
        return None


class _ListingParser(HTMLParser):
    """Collects ``<pre class="listing">`` blocks with their symbol anchors."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._current_symbol = ""
        self._in_listing = False
        self._buffer: list[str] = []
        self.blocks: list[tuple[str, str]] = []

    @override
    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attr = dict(attrs)
        if tag == "a" and "name" in attr:
            name = attr["name"] or ""
            symbol, _, _ = name.partition(",")
            self._current_symbol = unquote(symbol)
        elif tag == "pre" and attr.get("class") == "listing":
            self._in_listing = True
            self._buffer = []

    @override
    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self._in_listing:
            self._in_listing = False
            code = "".join(self._buffer).strip("\n")
            self.blocks.append((self._current_symbol, code))

    @override
    def handle_data(self, data: str) -> None:
        if self._in_listing:
            self._buffer.append(data)
