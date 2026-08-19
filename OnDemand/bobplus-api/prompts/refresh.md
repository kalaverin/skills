# Refresh Runbook: Re-scraping the Bobplus API Documentation

Operational prompt for the agent tasked with actualizing the `bobplus-api` skill (recommended cadence: ~6 months, or on user request). Work from the skills workspace root. Load `frontmatter-protocol` (core + lazyload extension) before touching the corpus, and `serena-protocol` before writing the closing memory entry.

## Context and Constraints

[ref: #bob-refresh-context]

- The skill's `references/` corpus was scraped from `https://developers.bobplus.africa` (docs version **V2.1.2**) on 2026-08-12. The pin lives in `bobplus-api/SKILL.md` §"Provenance pin".
- The site is server-rendered HTML (custom "luno" theme, Prism.js). No `llms.txt`, no `.md` endpoints, no `openapi.json` (all 404 as of the pin date — re-check, platforms change).
- HEAD requests return only `Cache-Control: no-cache` — **no `Last-Modified`, no `ETag`**. Conditional re-fetch is impossible; change detection is content-hash diffing against the committed corpus, plus the docs version string in the site's sidebar (V2.1.2 at pin date) and the changelog section on the home page.
- Known broken page at pin date: `/south-africa` returned HTTP 500 twice. Re-probe it on every refresh; if it starts answering, capture it and update `references/payins.md` (south-africa section) and `references/getting_started.md` (the note about the broken guide).
- Known source-doc inconsistencies to preserve (not "fix"): NGN payout channel `300043` vs `900020`/`900021`; rate limit 1500/minute vs 1500/second.

## Page Manifest

[ref: #bob-refresh-manifest]

The full page list at pin date (17 working pages + the broken `/south-africa` = 18 URLs). Re-discover links from the home page and each page's sidebar on every run — new pages may appear.

| URL | Corpus destination |
|---|---|
| `/` | `references/getting_started.md` (platform overview) |
| `/country-support` | `references/getting_started.md` (country matrix) |
| `/ip-whitelist` | `references/getting_started.md` (ip whitelisting) |
| `/nigeria` | `references/nigeria.md` (whole file) |
| `/south-africa` | broken (500) at pin date — re-probe |
| `/authentication` | `references/security.md` |
| `/generate-signature` | `references/security.md` |
| `/generate-x-hash` | `references/security.md` |
| `/account-services/get-balance` | `references/account_services.md` |
| `/account-services/full-statement` | `references/account_services.md` |
| `/c2b/momo-payin` | `references/payins.md` |
| `/c2b/south-africa-payin` | `references/payins.md` |
| `/c2b/nigeria-payin` | `references/payins.md` |
| `/b2c/bank-payout` | `references/payouts.md` |
| `/b2c/momo-payout` | `references/payouts.md` |
| `/bank-codes` | `references/utilities.md` |
| `/callback-response` | `references/utilities.md` |
| `/transaction-status/payment` | `references/utilities.md` |

## Pipeline

[ref: #bob-refresh-pipeline]

1. **Scrape raw:** `curl -s -L` each URL into `.tmp/bobplus/raw/<slug>.html` (raw-fetch is the sanctioned kagi-search §1.1 case — exact bytes, no transformation). Record HTTP codes; a persistent 500 after a retry is a finding, not a blocker.
2. **Extract content:** pull the `.card` element inside `div.page-body` from each HTML file (BeautifulSoup `select_one(".page-body .card")`), write fragments to `.tmp/bobplus/frag/`.
3. **Convert:** `pandoc -f html -t gfm --wrap=none frag/<slug>.html -o md2/<slug>.md`.
4. **Normalize** (reproduce these exact choices so diffs stay meaningful): strip wrapper `<div>` lines, `<style>` blocks, "Copy" button lines, sidebar/footer; flatten rowspan HTML tables into plain markdown tables; deduplicate repeated rows (the country table ships a duplicated block); keep all JSON/curl/PHP/JS examples verbatim.
5. **Diff:** compare normalized content section-by-section against the committed `references/` bodies. Identical content → done for that page (no edit).
6. **Update** only the sections whose source changed: keep existing `[ref: #...]` anchors and headings stable (heading renames are forbidden by `markdown-protocol` — new content gets new sections; dead content is deprecated, not deleted); keep the per-section `Sources:` lines in sync with the URL map in `SKILL.md` §4 (new pages get new `Sources:` entries); update frontmatter cards when a section's meaning shifted (word band 30–50, firm `problem` style, cross-field dedup — the lazyload extension is the binding standard).
7. **Bump the pin:** docs version string (if changed) and the scrape date in `bobplus-api/SKILL.md` and in each touched file's intro line.
8. **Validate:** `uv run --no-project --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py bobplus-api/references` — all files must pass the lazyload profile.
9. **Persist:** run `just sync-skills-mirror`, then record the refresh outcome (what changed, what was checked unchanged, new broken/fixed pages) as a Serena memory under `reports/project/bobplus_api_refresh_<date>` per `serena-protocol`, and update the decision card `decisions/project/bobplus_api_skill` if the pipeline itself changed.

## Guardrails

[ref: #bob-refresh-guardrails]

- Never answer "did the docs change?" from HEAD headers — they carry no freshness signal; only content comparison answers it.
- Never edit corpus bodies to match what the API "probably" does — the corpus mirrors the site; site bugs and contradictions are preserved and flagged, not corrected.
- New pages beyond the manifest: propose to the user where they belong (new section vs new file) before writing; anchor prefix follows the filename per the lazyload layout rule.
- If the site structure changed fundamentally (new platform, new IA), STOP and report to the user instead of forcing the old mapping.
