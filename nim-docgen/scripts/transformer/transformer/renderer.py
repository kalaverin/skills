"""Rendering of module documentation via Jinja2 templates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

import jinja2

from transformer import models

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from transformer import config

_ANCHOR_PATTERN = re.compile(r"^\[ref: #([a-z0-9-]+)\]$")


@dataclass(frozen=True)
class IndexEntry:
    """One module's index metadata for ``INDEX.md`` rendering."""

    source_path: str
    module_name: str
    package: str
    part_count: int
    anchor: str


@dataclass(frozen=True)
class _SymbolView:
    """A template-ready, pre-formatted view of one symbol."""

    name: str
    anchor: str
    summary: str
    show_signature: bool
    inputs: tuple[str, ...]
    output: str | None
    generic_params: str
    pragmas: str
    effects: str
    code: str
    description: str
    examples: tuple[str, ...]


@dataclass(frozen=True)
class _GroupView:
    """A template-ready group of symbols sharing one kind."""

    kind: str
    symbols: tuple[_SymbolView, ...]


@dataclass(frozen=True)
class _IndexEntryView:
    """A template-ready index entry with a precomputed link."""

    name: str
    link: str
    anchor: str


@dataclass(frozen=True)
class _IndexGroupView:
    """A template-ready group of index entries from one directory."""

    name: str
    entries: tuple[_IndexEntryView, ...]


def render_module(
    module_document: models.ModuleDocument,
    settings: config.Settings,
) -> models.RenderedModule:
    """Render one module to Markdown.

    Args:
        module_document: The enriched module document to render.
        settings: Validated transformer settings.

    Returns:
        The rendered content with its anchor map and line count.
    """
    del settings  # Reserved for future template configuration.
    environment = _environment()
    template = environment.get_template("module.md.j2")
    groups = tuple(
        _GroupView(
            kind=kind,
            symbols=tuple(_symbol_view(symbol) for symbol in symbols),
        )
        for kind, symbols in module_document.groups.items()
    )
    content = template.render(
        module=module_document.module_ref,
        module_name=module_document.module_ref.module_name,
        source_hash=module_document.source_hash,
        source_path=module_document.module_ref.source_path,
        module_description=module_document.module_description_md or "",
        groups=groups,
    )
    return models.RenderedModule(
        module_ref=module_document.module_ref,
        source_hash=module_document.source_hash,
        content=content,
        anchors=_collect_anchors(content),
        line_count=len(content.splitlines()),
    )


def render_index(
    entries: Sequence[IndexEntry],
    settings: config.Settings,
) -> models.Index:
    """Render the top-level INDEX.md.

    Args:
        entries: Index metadata for every rendered module.
        settings: Validated transformer settings.

    Returns:
        The index content and the source path to link mapping.
    """
    environment = _environment()
    template = environment.get_template("index.md.j2")
    grouped: dict[str, list[IndexEntry]] = {}
    for entry in entries:
        directory = entry.source_path.rpartition("/")[0] or "."
        grouped.setdefault(directory, []).append(entry)
    groups = tuple(
        _IndexGroupView(
            name=name,
            entries=tuple(
                _IndexEntryView(
                    name=entry.module_name,
                    link=_entry_link(entry),
                    anchor=entry.anchor,
                )
                for entry in sorted(items, key=lambda item: item.module_name)
            ),
        )
        for name, items in sorted(grouped.items())
    )
    content = template.render(groups=groups)
    links = MappingProxyType({
        entry.source_path: _entry_link(entry) for entry in entries
    })
    return models.Index(
        path=settings.index_path,
        content=content,
        module_links=links,
    )


def _environment() -> jinja2.Environment:
    """Return a Jinja2 environment loading templates from the package."""
    return jinja2.Environment(
        loader=jinja2.PackageLoader("transformer", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,  # noqa: S701  # Markdown output, not HTML.
    )


def _symbol_view(symbol: models.Symbol) -> _SymbolView:
    """Build the pre-formatted template view for one symbol."""
    description = symbol.description_md or ""
    first_line, _, _ = description.partition("\n")
    summary = first_line if "\n" in description else ""
    signature = symbol.signature
    inputs: tuple[str, ...] = ()
    output: str | None = None
    generic_params = ""
    pragmas = ""
    effects = ""
    if signature is not None:
        inputs = tuple(
            f"{argument.name}: {argument.type}"
            + (f" = {argument.default}" if argument.default is not None else "")
            for argument in signature.inputs
        )
        output = signature.output
        generic_params = _backticked(signature.generic_params)
        pragmas = _backticked(signature.pragmas)
        effects = _backticked(
            tuple(
                f"{key}: {', '.join(items)}"
                for key, items in signature.effects.items()
            ),
        )
    return _SymbolView(
        name=symbol.name,
        anchor=f"symbol-{models.symbol_anchor(symbol)}",
        summary=summary,
        show_signature=signature is not None,
        inputs=inputs,
        output=output,
        generic_params=generic_params,
        pragmas=pragmas,
        effects=effects,
        code=symbol.code,
        description=description,
        examples=tuple(example.code for example in symbol.examples),
    )


def _backticked(values: Sequence[str]) -> str:
    """Join values as a comma-separated list of inline code spans."""
    if not values:
        return ""
    return "`" + "`, `".join(values) + "`"


def _collect_anchors(content: str) -> Mapping[str, int]:
    """Map each ``[ref: #anchor]`` line to its 1-based line number."""
    anchors: dict[str, int] = {}
    for number, line in enumerate(content.splitlines(), start=1):
        match = _ANCHOR_PATTERN.match(line.strip())
        if match:
            anchors[match.group(1)] = number
    return MappingProxyType(anchors)


def _entry_link(entry: IndexEntry) -> str:
    """Return the relative Markdown link for a module's first page."""
    base = f"references/{entry.source_path.removesuffix('.nim')}"
    if entry.part_count > 1:
        return f"{base}_1.md"
    return f"{base}.md"
