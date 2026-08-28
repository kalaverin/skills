"""Command-line interface for the documentation transformer."""

from __future__ import annotations

import dataclasses
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import structlog
import typer
from pydantic import ValidationError

from transformer import (
    config,
    exporter,
    html_extractor,
    html_to_markdown,
    loader,
    models,
    renderer,
    scanner,
    splitter,
    storage,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = structlog.get_logger(__name__)

app = typer.Typer(
    name="transformer",
    help="Transform Nim JSON documentation into Markdown pages.",
    no_args_is_help=False,
)


@dataclass(frozen=True)
class PipelineResult:
    """Summary statistics of one full pipeline run."""

    discovered: int
    json_generated: int
    json_reused: int
    json_failed: int
    html_extracted: int
    html_reused: int
    html_failed: int
    md_files_written: int
    orphans_removed: int
    elapsed_seconds: float


def main() -> None:
    """Run the Typer application."""
    app()


@app.callback(invoke_without_command=True)
def execute(
    repo_root: Path | None = typer.Option(
        None, "--repo-root", help="Nim repository root.",
    ),
    nim_bin: Path | None = typer.Option(
        None, "--nim-bin", help="Path to the nim compiler binary.",
    ),
    md_dir: Path | None = typer.Option(
        None, "--md-dir", help="Markdown output root (references/).",
    ),
    workers: int | None = typer.Option(
        None, "--workers", help="Parallel workers (default: cpu count).",
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Log level."),
) -> None:
    """Run the full transformation pipeline."""
    _configure_logging(log_level)
    try:
        settings = _build_settings(repo_root, nim_bin, md_dir, workers, log_level)
    except ValidationError as exc:
        logger.exception("invalid_settings", error=str(exc))
        raise typer.Exit(code=2) from exc
    result = run_pipeline(settings)
    raise typer.Exit(code=0 if result.md_files_written > 0 else 1)


def run_pipeline(settings: config.Settings) -> PipelineResult:
    """Execute the full pipeline and return summary statistics."""
    started = time.monotonic()
    modules = scanner.discover(settings)
    json_missing = [
        module
        for module in modules
        if not storage.object_exists(module.source_hash, settings.cache_root)
    ]
    html_missing = [
        module for module in modules if not _html_fresh(module, settings)
    ]
    json_generated, json_failed = _export_missing(json_missing, settings)
    html_extracted, html_failed = _extract_missing(html_missing, settings)
    md_files_written = 0
    index_entries: list[renderer.IndexEntry] = []
    for module in modules:
        files = _render_module_files(module, settings)
        if files is None:
            continue
        for md_file in files:
            if md_file.path is not None:
                storage.write_text(md_file.path, md_file.content)
                md_files_written += 1
        base_path = _base_path(module.module_ref, settings)
        part_count = 1 if files[0].part_number is None else len(files)
        storage.remove_stale_parts(base_path.parent, base_path.stem, part_count)
        index_entries.append(
            renderer.IndexEntry(
                source_path=module.module_ref.source_path,
                module_name=module.module_ref.module_name,
                package=module.module_ref.package,
                part_count=part_count,
                anchor=f"module-{module.module_ref.module_name}",
            ),
        )
    index = renderer.render_index(index_entries, settings)
    storage.write_text(index.path, index.content)
    orphans = storage.collect_orphans(settings.cache_root)
    result = PipelineResult(
        discovered=len(modules),
        json_generated=json_generated,
        json_reused=len(modules) - len(json_missing),
        json_failed=json_failed,
        html_extracted=html_extracted,
        html_reused=len(modules) - len(html_missing),
        html_failed=html_failed,
        md_files_written=md_files_written,
        orphans_removed=len(orphans),
        elapsed_seconds=time.monotonic() - started,
    )
    logger.info("pipeline_finished", **dataclasses.asdict(result))
    return result


def _configure_logging(log_level: str) -> None:
    """Configure structlog with the configured console log level."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(level),
    )


def _build_settings(
    repo_root: Path | None,
    nim_bin: Path | None,
    md_dir: Path | None,
    workers: int | None,
    log_level: str,
) -> config.Settings:
    """Build validated settings, resolving defaults against repo_root."""
    repo = (repo_root or Path.cwd()).expanduser().resolve()
    fields = config.Settings.model_fields
    overrides: dict[str, object] = {
        "repo_root": repo,
        "nim_bin": nim_bin if nim_bin is not None else repo / fields["nim_bin"].default,
        "cache_root": repo / fields["cache_root"].default,
        "md_output_root": (
            md_dir if md_dir is not None else repo / fields["md_output_root"].default
        ),
        "index_path": repo / fields["index_path"].default,
        "log_level": log_level,
    }
    if workers is not None:
        overrides["workers"] = workers
    return config.Settings(**overrides)  # type: ignore[arg-type]


def _html_fresh(module: models.ScannedModule, settings: config.Settings) -> bool:
    """Check whether HTML and examples pointers match the current hash."""
    cache_root = settings.cache_root
    html_pointer = storage.pointer_path(
        module.module_ref, models.ArtifactType.GENERATED_HTML, cache_root,
    )
    examples_pointer = storage.pointer_path(
        module.module_ref, models.ArtifactType.EXAMPLES_JSON, cache_root,
    )
    html_hash = storage.artifact_object_hash(
        module.source_hash, models.ArtifactType.GENERATED_HTML,
    )
    examples_hash = storage.artifact_object_hash(
        module.source_hash, models.ArtifactType.EXAMPLES_JSON,
    )
    return (
        storage.read_pointer(html_pointer) == html_hash
        and storage.read_pointer(examples_pointer) == examples_hash
    )


def _export_missing(
    modules: Sequence[models.ScannedModule],
    settings: config.Settings,
) -> tuple[int, int]:
    """Export JSON for missing modules in a process pool."""
    generated = 0
    failed = 0
    if not modules:
        return generated, failed
    with ProcessPoolExecutor(max_workers=settings.workers) as pool:
        futures = {
            pool.submit(exporter.export_json, module, settings): module
            for module in modules
        }
        for future in as_completed(futures):
            module = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # Isolation point: worker crashed.
                logger.exception(
                    "json_export_crashed",
                    source_path=module.module_ref.source_path,
                    error=str(exc),
                )
                failed += 1
                continue
            if result.success:
                generated += 1
            else:
                logger.error(
                    "json_export_failed",
                    source_path=module.module_ref.source_path,
                    returncode=result.error.returncode if result.error else None,
                    stderr=_tail(result.error.stderr if result.error else ""),
                )
                failed += 1
    return generated, failed


def _extract_missing(
    modules: Sequence[models.ScannedModule],
    settings: config.Settings,
) -> tuple[int, int]:
    """Extract HTML/examples for stale modules in a process pool."""
    extracted = 0
    failed = 0
    if not modules:
        return extracted, failed
    with ProcessPoolExecutor(max_workers=settings.workers) as pool:
        futures = {
            pool.submit(html_extractor.extract_examples, module, settings): module
            for module in modules
        }
        for future in as_completed(futures):
            module = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # Isolation point: worker crashed.
                logger.exception(
                    "html_extraction_crashed",
                    source_path=module.module_ref.source_path,
                    error=str(exc),
                )
                failed += 1
                continue
            if result.success:
                extracted += 1
            else:
                logger.error(
                    "html_extraction_failed",
                    source_path=module.module_ref.source_path,
                    returncode=result.error.returncode if result.error else None,
                    stderr=_tail(result.error.stderr if result.error else ""),
                )
                failed += 1
    return extracted, failed


def _render_module_files(
    module: models.ScannedModule,
    settings: config.Settings,
) -> Sequence[models.MarkdownFile] | None:
    """Load, enrich, render, and split one module; None on failure."""
    module_ref = module.module_ref
    try:
        document = loader.load_module_document(module, settings)
    except loader.LoadError as exc:
        logger.exception(
            "module_load_failed",
            source_path=module_ref.source_path,
            reason=exc.reason,
        )
        return None
    examples = loader.load_examples(module, settings)
    enriched = _enrich_document(document, examples)
    rendered = renderer.render_module(enriched, settings)
    return splitter.split(
        rendered,
        _base_path(module_ref, settings),
        settings.max_lines_per_file,
    )


def _enrich_document(
    document: models.ModuleDocument,
    examples: Sequence[models.Example],
) -> models.ModuleDocument:
    """Attach examples and convert descriptions for one module."""
    by_name: dict[str, models.Symbol] = {}
    for symbol in document.symbols:
        by_name.setdefault(symbol.name, symbol)
    attached: dict[str, list[models.Example]] = {}
    module_level: list[models.Example] = []
    for example in examples:
        target = by_name.get(example.target_symbol)
        if target is None and example.target_line > 0:
            candidates = [
                symbol
                for symbol in document.symbols
                if symbol.line <= example.target_line
            ]
            if candidates:
                target = max(candidates, key=lambda symbol: symbol.line)
        if target is None:
            module_level.append(example)
        else:
            attached.setdefault(target.name, []).append(example)
    enriched_symbols = tuple(
        dataclasses.replace(
            symbol,
            description_md=html_to_markdown.convert_symbol_description(
                symbol.description_html,
            ),
            examples=tuple(attached.get(symbol.name, ())),
        )
        for symbol in document.symbols
    )
    module_md = html_to_markdown.convert_module_description(
        document.module_description_html,
    )
    if module_level:
        section = _examples_section(module_level)
        module_md = f"{module_md}\n\n{section}" if module_md else section
    return dataclasses.replace(
        document,
        module_description_md=module_md,
        symbols=enriched_symbols,
        groups=loader.group_symbols(enriched_symbols),
    )


def _examples_section(examples: Sequence[models.Example]) -> str:
    """Render module-level examples as a fenced Markdown section."""
    blocks = ["## Examples"]
    blocks.extend(f"```nim\n{example.code}\n```" for example in examples)
    return "\n\n".join(blocks)


def _base_path(module_ref: models.ModuleRef, settings: config.Settings) -> Path:
    """Return the unsplit Markdown path for a module under the output root."""
    relative = Path(module_ref.source_path).with_suffix(".md")
    return settings.md_output_root / relative


def _tail(text: str, limit: int = 500) -> str:
    """Return the trailing slice of a subprocess stderr capture."""
    return text[-limit:] if len(text) > limit else text
