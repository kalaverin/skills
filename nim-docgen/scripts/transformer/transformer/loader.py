"""Loading of cached JSON artifacts into domain models."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

import orjson
import structlog
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from transformer import models, storage

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from transformer import config

logger = structlog.get_logger(__name__)

_EFFECT_KEYS = frozenset({"raises", "tags", "forbids"})


@dataclass(frozen=True)
class LoadError(Exception):
    """A cached artifact could not be loaded into domain models."""

    source_path: str
    reason: str
    exception: str | None


class _JsondocArgument(BaseModel):
    """One argument of the jsondoc structured signature."""

    model_config = ConfigDict(extra="ignore")

    name: str
    type: str
    default: str | None = None


class _JsondocGenericParam(BaseModel):
    """One generic parameter of the jsondoc structured signature."""

    model_config = ConfigDict(extra="ignore")

    name: str
    types: str | None = None


class _JsondocSignature(BaseModel):
    """The jsondoc structured signature (compiler/docgen.nim schema)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    return_: str | None = Field(default=None, alias="return")
    arguments: list[_JsondocArgument] = Field(default_factory=list)
    pragmas: list[str] = Field(default_factory=list)
    generic_params: list[_JsondocGenericParam] = Field(
        default_factory=list, alias="genericParams",
    )


class _JsondocEntry(BaseModel):
    """One exported symbol entry of a jsondoc document."""

    model_config = ConfigDict(extra="ignore")

    name: str
    type: str
    line: int
    col: int
    code: str = ""
    description: str | None = None
    signature: _JsondocSignature | None = None


class _JsondocDocument(BaseModel):
    """Top-level jsondoc document for one module."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    orig: str = ""
    nimble: str = ""
    module_description: str | None = Field(
        default=None, alias="moduleDescription",
    )
    entries: list[_JsondocEntry] = Field(default_factory=list)


def load_module_document(
    scanned: models.ScannedModule,
    settings: config.Settings,
) -> models.ModuleDocument:
    """Load and validate the jsondoc object for a module.

    Args:
        scanned: The module whose JSON artifact should be loaded.
        settings: Validated transformer settings.

    Returns:
        A module document without Markdown descriptions or examples;
        the orchestrator enriches those later.

    Raises:
        LoadError: If the artifact is missing, unreadable, or invalid.
    """
    module_ref = scanned.module_ref
    pointer = storage.pointer_path(
        module_ref, models.ArtifactType.GENERATED_JSON, settings.cache_root,
    )
    digest = storage.read_pointer(pointer)
    if digest is None:
        raise LoadError(
            source_path=module_ref.source_path,
            reason="generated.json.z pointer missing or dangling",
            exception=None,
        )
    try:
        raw = storage.read_object(digest, settings.cache_root)
    except OSError as exc:
        raise LoadError(
            source_path=module_ref.source_path,
            reason="jsondoc object unreadable",
            exception=str(exc),
        ) from exc
    try:
        document = _JsondocDocument.model_validate(orjson.loads(raw))
    except (orjson.JSONDecodeError, ValidationError) as exc:
        raise LoadError(
            source_path=module_ref.source_path,
            reason="jsondoc object failed schema validation",
            exception=str(exc),
        ) from exc
    symbols = tuple(_to_symbols(document, module_ref))
    return models.ModuleDocument(
        module_ref=module_ref,
        source_hash=scanned.source_hash,
        module_description_html=document.module_description,
        module_description_md=None,
        symbols=symbols,
        groups=group_symbols(symbols),
    )


def load_examples(
    scanned: models.ScannedModule,
    settings: config.Settings,
) -> Sequence[models.Example]:
    """Load parsed examples from the examples.json.z object.

    Returns an empty sequence when the pointer or object is missing.
    """
    module_ref = scanned.module_ref
    pointer = storage.pointer_path(
        module_ref, models.ArtifactType.EXAMPLES_JSON, settings.cache_root,
    )
    digest = storage.read_pointer(pointer)
    if digest is None:
        return ()
    try:
        raw = storage.read_object(digest, settings.cache_root)
        payload = orjson.loads(raw)
    except (OSError, orjson.JSONDecodeError) as exc:
        logger.warning(
            "examples_unreadable",
            source_path=module_ref.source_path,
            error=str(exc),
        )
        return ()
    return tuple(
        models.Example(
            code=str(item["code"]),
            target_symbol=str(item["target_symbol"]),
            target_line=int(item["target_line"]),
            order=int(item["order"]),
        )
        for item in payload
    )


def _to_symbols(
    document: _JsondocDocument,
    module_ref: models.ModuleRef,
) -> list[models.Symbol]:
    """Convert validated jsondoc entries into domain symbols."""
    symbols: list[models.Symbol] = []
    for entry in document.entries:
        try:
            kind = models.SymbolKind(entry.type)
        except ValueError:
            logger.warning(
                "unknown_symbol_kind",
                source_path=module_ref.source_path,
                symbol=entry.name,
                kind=entry.type,
            )
            continue
        symbols.append(
            models.Symbol(
                name=entry.name,
                kind=kind,
                line=entry.line,
                col=entry.col,
                code=entry.code,
                signature=_to_signature(entry.signature)
                if entry.signature is not None
                else None,
                description_html=entry.description,
                description_md=None,
                examples=(),
            ),
        )
    return symbols


def _to_signature(signature: _JsondocSignature) -> models.Signature:
    """Convert a validated jsondoc signature into the domain signature."""
    return models.Signature(
        inputs=tuple(
            models.Argument(
                name=argument.name,
                type=argument.type,
                default=argument.default,
            )
            for argument in signature.arguments
        ),
        output=signature.return_,
        generic_params=tuple(param.name for param in signature.generic_params),
        pragmas=tuple(signature.pragmas),
        effects=MappingProxyType(_parse_effects(signature.pragmas)),
    )


def _parse_effects(pragmas: Sequence[str]) -> dict[str, tuple[str, ...]]:
    """Extract ``raises``/``tags``/``forbids`` lists from pragma strings."""
    effects: dict[str, tuple[str, ...]] = {}
    for pragma in pragmas:
        key, separator, value = pragma.partition(":")
        if not separator or key.strip() not in _EFFECT_KEYS:
            continue
        items = tuple(
            item.strip()
            for item in value.strip().strip("[]").split(",")
            if item.strip()
        )
        effects[key.strip()] = items
    return effects


def group_symbols(
    symbols: Sequence[models.Symbol],
) -> Mapping[str, Sequence[models.Symbol]]:
    """Group symbols by title-cased kind and sort alphabetically.

    Also used by the orchestrator to rebuild groups after enriching
    symbols with Markdown descriptions and examples.
    """
    groups: dict[str, list[models.Symbol]] = {}
    for symbol in symbols:
        key = symbol.kind.value.removeprefix("sk").title()
        groups.setdefault(key, []).append(symbol)
    return MappingProxyType({
        key: tuple(sorted(items, key=lambda symbol: symbol.name.casefold()))
        for key, items in sorted(groups.items())
    })
