"""Splitting of oversized Markdown pages at symbol boundaries."""

from __future__ import annotations

from typing import TYPE_CHECKING

from transformer import models

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

_SYMBOL_HEADING = "### "
_GROUP_HEADING = "## "


def split(
    rendered: models.RenderedModule,
    base_path: Path,
    max_lines: int = 1000,
) -> Sequence[models.MarkdownFile]:
    """Split rendered Markdown into parts. base_path is the path for part 1.

    A module that fits is written as ``<stem>.md``; a split module is
    written as ``<stem>_1.md``, ``<stem>_2.md``, ... with frontmatter in
    every part and prev/next navigation links at the bottom.

    Args:
        rendered: The rendered module content.
        base_path: Target path of the unsplit page.
        max_lines: Maximum number of lines per output file.

    Returns:
        One MarkdownFile for a fitting module, otherwise the numbered parts.
    """
    if rendered.line_count <= max_lines:
        return (
            models.MarkdownFile(
                path=base_path,
                content=rendered.content,
                part_number=None,
                prev_path=None,
                next_path=None,
            ),
        )
    frontmatter, body = _split_frontmatter(rendered.content)
    header, chunks = _body_chunks(body)
    parts = _pack_chunks(header, chunks, frontmatter, max_lines)
    return _build_files(parts, frontmatter, base_path)


def _split_frontmatter(content: str) -> tuple[list[str], list[str]]:
    """Split content into the frontmatter block and the remaining body."""
    lines = content.splitlines()
    if lines and lines[0] == "---":
        for index in range(1, len(lines)):
            if lines[index] == "---":
                body = lines[index + 1:]
                while body and not body[0].strip():
                    body.pop(0)
                return lines[:index + 1], body
    return [], lines


def _body_chunks(body: list[str]) -> tuple[list[str], list[list[str]]]:
    """Split body lines into the header and per-symbol chunks.

    A ``##`` heading followed by a ``###`` symbol heading starts a new
    chunk so the group heading travels with its first symbol.
    """
    header: list[str] = []
    chunks: list[list[str]] = []
    current: list[str] | None = None
    for index, line in enumerate(body):
        if line.startswith(_SYMBOL_HEADING) or _is_group_heading(body, index):
            if current is None:
                header = header or []
            else:
                chunks.append(current)
            current = [line]
        elif current is None:
            header.append(line)
        else:
            current.append(line)
    if current is not None:
        chunks.append(current)
    return header, chunks


def _is_group_heading(body: list[str], index: int) -> bool:
    """Check for a ``##`` heading directly preceding a symbol heading."""
    if not body[index].startswith(_GROUP_HEADING):
        return False
    lookahead = index + 1
    while lookahead < len(body) and not body[lookahead].strip():
        lookahead += 1
    return (
        lookahead < len(body)
        and body[lookahead].startswith(_SYMBOL_HEADING)
    )


def _pack_chunks(
    header: list[str],
    chunks: list[list[str]],
    frontmatter: list[str],
    max_lines: int,
) -> list[list[str]]:
    """Greedily pack chunks into parts that respect the line budget."""
    overhead = len(frontmatter) + 2  # Frontmatter, blank line, nav line.
    limit = max(1, max_lines - overhead)
    parts: list[list[str]] = []
    current: list[str] = list(header)
    for chunk in chunks:
        has_content = any(line.strip() for line in current)
        if has_content and len(current) + len(chunk) > limit:
            parts.append(current)
            current = []
        current.extend(chunk)
    if current:
        parts.append(current)
    return parts


def _build_files(
    parts: list[list[str]],
    frontmatter: list[str],
    base_path: Path,
) -> tuple[models.MarkdownFile, ...]:
    """Materialize packed parts into numbered MarkdownFile instances."""
    total = len(parts)
    files: list[models.MarkdownFile] = []
    for index, content_lines in enumerate(parts, start=1):
        path = base_path.with_name(
            f"{base_path.stem}_{index}{base_path.suffix}",
        )
        prev_path = _part_path(base_path, index - 1) if index > 1 else None
        next_path = _part_path(base_path, index + 1) if index < total else None
        lines = [
            *frontmatter,
            "",
            *content_lines,
            "",
            _navigation_line(prev_path, next_path),
        ]
        files.append(
            models.MarkdownFile(
                path=path,
                content="\n".join(lines) + "\n",
                part_number=index,
                prev_path=prev_path,
                next_path=next_path,
            ),
        )
    return tuple(files)


def _part_path(base_path: Path, index: int) -> Path:
    """Return the numbered part path for the given 1-based index."""
    return base_path.with_name(f"{base_path.stem}_{index}{base_path.suffix}")


def _navigation_line(prev_path: Path | None, next_path: Path | None) -> str:
    """Render the bottom prev/next navigation line for a split part."""
    links: list[str] = []
    if prev_path is not None:
        links.append(f"[Prev]({prev_path.name})")
    if next_path is not None:
        links.append(f"[Next]({next_path.name})")
    return " | ".join(links)
