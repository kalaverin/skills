# REFERENCE STANDARD ADDENDUM: python-lang

This addendum declares the `python-lang` reference corpus's local amendments to the canonical lazyload authoring standard (`frontmatter-protocol/references/lazyload.md`). Where this addendum is silent, the canonical standard applies unchanged.

## 1. Anchor Prefixes (Two-Tier Grammar)

Anchor ids follow the project-wide two-tier grammar `<skill-prefix>-<file-prefix>-<section-slug>` (ruled 2026-08-06; the ruling lives in the Serena decision memory `decisions/project/skill_file_anchor_prefixes`, not in a repo file):

- `py-lr-*` — `references/01_language_rules.md` (Google language rules)
- `py-st-*` — `references/02_style_rules.md` (Google style rules)
- `py-pr-*` — `references/03_personal_rules.md` (personal rules)

## 2. Marker Style

`marker_style` for every file in this corpus is **tight**: `[ref: #py-*]` at column 0, on the line immediately following the section heading, no blank line between heading and marker.

## 3. Numbered-Headings Exemption (Google Canon)

The corpus reproduces the Google Python Style Guide, an externally-arrived standard. Its chapter numbering (H1 `# 1.` / `# 2.`, rule sections `## 1.1` … `## 2.19` — including the upstream-authentic gaps 1.15 and 2.9) is **normative content**, not a markdown-protocol violation. Section renumbering, gap closure, and heading-number stripping are forbidden. The numbered-headings exemption of `markdown-protocol` applies and is hereby declared.

## 4. Pseudo-Heading Legalization

The Google corpus's inline facet markers — bold pseudo-headings such as `**Definition:**`, `**Pros:**`, `**Cons:**`, `**Decision:**`, `**Args:**`, `**Raises:**`, `**Returns:**`, `**Type Comments:**`, `**Annotated Assignments**` — are legalized as proper ATX headings. Two facet styles exist, both intentional: `01_language_rules.md` uses numbered facets (`#### 1.1.1 Definition`); `02_style_rules.md` keeps docstring-content labels unnumbered and colon-suffixed (`#### Args:`, `#### Returns:`, `#### Raises:`) because they mirror literal docstring section names, while its structural subsections stay numbered (`#### 2.8.2.1 Test Modules`). Facet-level routable markers exist only where the card schema demands subsection routing (chapters 2.8 / 2.10 / 2.16 / 2.19); ordinary facet headings carry no `[ref: #...]` marker.

## 5. Upstream Staleness Is Preserved

The corpus mirrors the Google guide verbatim, including its dated references (`six.moves`, `from __future__ import generator_stop`, withdrawn PEP-0533, `pylint`/`pytype` toolchains). These are upstream-authentic and MUST NOT be modernized inside the corpus; the local toolchain override lives in `SKILL.md` §2 (Toolchain precedence) and §3. Coverage gaps relative to modern practice (e.g. dataclass mechanics beyond the docstring exemption) are residual: route via the nearest cards (`py-lr-properties`, `py-st-comments-in-classes`, `py-lr-power-features`) and treat the silence as intentional, not as license to skip routing.

## 6. Routing Entry Point

`SKILL.md` §2 is the funnel entry point: subject map → frontmatter cards → bounded extraction of the selected `py-*` sections. Routing tables listing per-anchor rows are intentionally absent from `SKILL.md`; the corpus frontmatter is the single source of routable sections.
