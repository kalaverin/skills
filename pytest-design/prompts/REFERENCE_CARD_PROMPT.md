# Prompt: Generate a pytest-design Reference Card

This is the pytest-design companion to the generalized authoring prompt. The operational skeleton lives at `frontmatter-protocol/prompts/CARD_AUTHORING.md`; the authoritative standard is `frontmatter-protocol/references/lazyload.md`. This file adds ONLY pytest-design specifics — general rules are never restated here. On any conflict, the standard wins.

**Use it as follows:** take `frontmatter-protocol/prompts/CARD_AUTHORING.md`, fill its `{{...}}` inputs with the pytest-design values below, and follow its procedure.

## pytest-design input values

- `{{TIER_NOTE}}` — the corpus is tiered: core testing techniques go to `references/required/`, specialized or situational ones to `references/optional/`. The tier is the directory; tier markers NEVER appear in frontmatter text.
- `{{TERMINATOR_NOTE}}` — every body section ends with a **Variety booster** block: a short list of alternative angles, edge cases, or parameterizations that widen the recipe's coverage beyond the main example.
- `{{DOMAIN_IDIOMS}}` — Python 3 with pytest: full imports shown, type annotations in helpers, `faker` for generated data (never hardcoded emails/names), deterministic examples (seed or freeze where randomness appears), Google-style docstrings, Ruff-clean snippets.
- `{{LIBRARIES}}` — lowercase canonical PyPI names; keep significant pins (`pytest-asyncio>=0.23`) and extras (`testcontainers[postgresql]`); include `pytest` only when a recipe depends on a specific pytest feature version.
- `{{EXTRA_KEYS}}` — none.

## Routing within pytest-design

Consumers route this corpus per `pytest-design/SKILL.md` §3 (the two-command funnel per `frontmatter-protocol` `[ref: #lazy-load-routing]`); cards are evaluated per `[ref: #lazyload-cards]` and `[ref: #lazyload-dedup]`.

## Validation

After authoring, run the canonical validator (per `[ref: #lazyload-conformance]`):

```bash
uv run --no-project --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py <file>
```
