"""Conversion of nimdoc HTML fragments to Markdown."""

from __future__ import annotations

import re

import markdownify


def convert(html: str) -> str:
    """Convert an HTML/RST snippet to Markdown.

    Args:
        html: The HTML fragment produced by the Nim RST renderer.

    Returns:
        Clean Markdown with ATX headings and collapsed blank lines.
    """
    markdown = markdownify.markdownify(html, heading_style="ATX")
    return re.sub(r"\n{3,}", "\n\n", markdown).strip()


def convert_module_description(html: str | None) -> str:
    """Convert module-level description; returns empty string for None."""
    if not html:
        return ""
    return convert(html)


def convert_symbol_description(html: str | None) -> str:
    """Convert symbol-level description; returns empty string for None."""
    if not html:
        return ""
    return convert(html)
