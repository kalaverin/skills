"""Validated settings for the documentation transformer."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Immutable runtime configuration for the transformer."""

    model_config = SettingsConfigDict(env_prefix="NIM_DOCGEN_", frozen=True)

    repo_root: Path = Field(default_factory=Path.cwd)
    nim_bin: Path = Path("bin/nim")
    cache_root: Path = Path(".tmp/cache")
    md_output_root: Path = Path(".kimi/skills/nim-docgen/references")
    index_path: Path = Path(".kimi/skills/nim-docgen/INDEX.md")
    workers: int | None = None
    log_level: str = "INFO"
    max_lines_per_file: int = 1000
    js_modules: frozenset[str] = frozenset({
        "lib/js/asyncjs.nim",
        "lib/js/dom.nim",
        "lib/js/jsconsole.nim",
        "lib/js/jsffi.nim",
        "lib/js/jscore.nim",
        "lib/js/jsre.nim",
        "lib/std/jsbigints.nim",
        "lib/std/jsfetch.nim",
        "lib/std/jsformdata.nim",
        "lib/std/jsheaders.nim",
    })
    excluded_modules: frozenset[str] = frozenset({
        "lib/js/asyncjs.nim",
        "lib/js/jscore.nim",
    })

    @field_validator(
        "repo_root",
        "nim_bin",
        "cache_root",
        "md_output_root",
        "index_path",
        mode="after",
    )
    @classmethod
    def _resolve_paths(cls, value: Path) -> Path:
        return value.expanduser().resolve()

    @field_validator("workers", mode="after")
    @classmethod
    def _bound_workers(cls, value: int | None) -> int:
        cpus = os.cpu_count() or 1
        return min(value or cpus, cpus)

    @model_validator(mode="after")
    def _check_nim_bin(self) -> Settings:
        if not self.nim_bin.is_file():
            msg = f"nim binary not found: {self.nim_bin}"
            raise ValueError(msg)
        if not os.access(self.nim_bin, os.X_OK):
            msg = f"nim binary is not executable: {self.nim_bin}"
            raise ValueError(msg)
        return self


def load_settings() -> Settings:
    """Parse CLI/env and return validated Settings."""
    return Settings()
