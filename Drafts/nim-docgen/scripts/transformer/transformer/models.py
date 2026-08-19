"""Immutable domain models for the documentation transformer."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path


class Backend(StrEnum):
    """Compilation backend deciding which ``nim`` flags are used."""

    NATIVE = "native"
    JS = "js"


class SymbolKind(StrEnum):
    """Nim symbol kind with the ``sk`` prefix as produced by jsondoc."""

    PROC = "skProc"
    FUNC = "skFunc"
    ITERATOR = "skIterator"
    TEMPLATE = "skTemplate"
    MACRO = "skMacro"
    TYPE = "skType"
    CONST = "skConst"
    VAR = "skVar"
    LET = "skLet"


class ArtifactType(StrEnum):
    """Cached artifact kinds stored under the content-addressed cache."""

    GENERATED_JSON = "generated_json"
    GENERATED_HTML = "generated_html"
    EXAMPLES_JSON = "examples_json"


@dataclass(frozen=True)
class ModuleRef:
    """A stable identifier for a module, used throughout the pipeline."""

    source_path: str
    module_name: str
    backend: Backend
    package: str


@dataclass(frozen=True)
class ScannedModule:
    """A `ModuleRef` enriched with the source-file hash."""

    module_ref: ModuleRef
    source_hash: str


@dataclass(frozen=True)
class ContentObject:
    """A content-addressed artifact in the object store."""

    hash: str
    object_path: Path


@dataclass(frozen=True)
class ArtifactPointer:
    """A stable hardlink pointing a module artifact to a `ContentObject`."""

    pointer_path: Path
    artifact_type: ArtifactType
    target_hash: str | None


@dataclass(frozen=True)
class Argument:
    """A single routine argument: name, type, and optional default."""

    name: str
    type: str
    default: str | None = None


@dataclass(frozen=True)
class Signature:
    """A cleaned, agent-friendly view of a symbol's interface."""

    inputs: Sequence[Argument]
    output: str | None
    generic_params: Sequence[str]
    pragmas: Sequence[str]
    effects: Mapping[str, Sequence[str]]


@dataclass(frozen=True)
class Example:
    """A runnable example mapped to its closest symbol."""

    code: str
    target_symbol: str
    target_line: int
    order: int


@dataclass(frozen=True)
class Symbol:
    """An exported Nim symbol loaded from a JSON artifact."""

    name: str
    kind: SymbolKind
    line: int
    col: int
    code: str
    signature: Signature | None
    description_html: str | None
    description_md: str | None
    examples: Sequence[Example]


@dataclass(frozen=True)
class ModuleDocument:
    """The loaded and normalized view of one module."""

    module_ref: ModuleRef
    source_hash: str
    module_description_html: str | None
    module_description_md: str | None
    symbols: Sequence[Symbol]
    groups: Mapping[str, Sequence[Symbol]]


@dataclass(frozen=True)
class RenderedModule:
    """The full Markdown content for a module before splitting."""

    module_ref: ModuleRef
    source_hash: str
    content: str
    anchors: Mapping[str, int]
    line_count: int


@dataclass(frozen=True)
class MarkdownFile:
    """A final Markdown file written under ``references/``."""

    path: Path | None
    content: str
    part_number: int | None
    prev_path: Path | None
    next_path: Path | None


@dataclass(frozen=True)
class Index:
    """The top-level ``INDEX.md`` content and module link map."""

    path: Path
    content: str
    module_links: Mapping[str, str]


def symbol_anchor(symbol: Symbol) -> str:
    """Return the deterministic lowercase kebab-case anchor id for a symbol."""
    return re.sub(r"[^a-z0-9]+", "-", symbol.name.lower()).strip("-")
