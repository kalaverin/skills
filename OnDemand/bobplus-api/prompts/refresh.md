# Agent Prompt: Refresh the Bobplus API Skill Corpus

You are refreshing the `bobplus-api` skill so it remains the binding source of truth for Bobplus API facts in this workspace. The skill is both documentation and canonical knowledge: every factual claim must reflect the scraped docs, every section must carry a `Sources:` proof-URL, and every contradiction must be preserved, not "fixed". Work from the skills workspace root `~/src/agent/skills`.

---

## 0. Bootstrap and environment check

1. Execute the `bootstrap` skill Startup Gate fully.
2. Load `frontmatter-protocol` (core + lazyload extension), `markdown-protocol`, `serena-protocol`, and the `bobplus-api` skill itself.
3. Verify tooling in one probe:
   ```bash
   command -v pandoc curl uv && python -c "import bs4, yaml" && pandoc --version | head -1
   ```
   If `yaml` is missing, validation will use `uvx --with pyyaml`; do not install packages into the project environment.
4. Today is the new provenance date; use ISO format `YYYY-MM-DD`.

---

## 1. Prepare scratch workspace

```bash
rm -rf .tmp/bobplus
mkdir -p .tmp/bobplus/{raw,frag,md2,md,reports}
```

---

## 2. Discover and fetch pages

### 2.1 Slug rule
Map each path to a filesystem-safe slug:
- `/` → `home`
- `/c2b/momo-payin` → `c2b-momo-payin`
- `/transaction-status/payment` → `transaction-status-payment`
Replace all `/` with `-`; drop leading `/`.

### 2.2 Mandatory manifest (always fetch these)

| URL | Slug | Corpus destination |
|---|---|---|
| `https://developers.bobplus.africa/` | `home` | `references/getting_started.md` |
| `https://developers.bobplus.africa/country-support` | `country-support` | `references/getting_started.md` |
| `https://developers.bobplus.africa/ip-whitelist` | `ip-whitelist` | `references/getting_started.md` |
| `https://developers.bobplus.africa/nigeria` | `nigeria` | `references/nigeria.md` |
| `https://developers.bobplus.africa/south-africa` | `south-africa` | re-probe; historically 500 |
| `https://developers.bobplus.africa/authentication` | `authentication` | `references/security.md` |
| `https://developers.bobplus.africa/generate-signature` | `generate-signature` | `references/security.md` |
| `https://developers.bobplus.africa/generate-x-hash` | `generate-x-hash` | `references/security.md` |
| `https://developers.bobplus.africa/account-services/get-balance` | `account-services-get-balance` | `references/account_services.md` |
| `https://developers.bobplus.africa/account-services/full-statement` | `account-services-full-statement` | `references/account_services.md` |
| `https://developers.bobplus.africa/c2b/momo-payin` | `c2b-momo-payin` | `references/payins.md` |
| `https://developers.bobplus.africa/c2b/south-africa-payin` | `c2b-south-africa-payin` | `references/payins.md` |
| `https://developers.bobplus.africa/c2b/nigeria-payin` | `c2b-nigeria-payin` | `references/payins.md` |
| `https://developers.bobplus.africa/b2c/bank-payout` | `b2c-bank-payout` | `references/payouts.md` |
| `https://developers.bobplus.africa/b2c/momo-payout` | `b2c-momo-payout` | `references/payouts.md` |
| `https://developers.bobplus.africa/bank-codes` | `bank-codes` | `references/utilities.md` |
| `https://developers.bobplus.africa/callback-response` | `callback-response` | `references/utilities.md` |
| `https://developers.bobplus.africa/transaction-status/payment` | `transaction-status-payment` | `references/utilities.md` |

### 2.3 Re-discover links
After fetching `home`, parse its sidebar/footer for links under `https://developers.bobplus.africa/`. Add any new page to the manifest before fetching. If a new page appears, stop after discovery and ask the user where it belongs (new section vs new reference file) unless its destination is obvious from the URL.

### 2.4 Fetch
```bash
curl -s -L -o .tmp/bobplus/raw/<slug>.html <url>
```
Record status per URL in `.tmp/bobplus/MANIFEST.md`:
```markdown
| Slug | URL | Status |
|---|---|---|
```
Retry a 5xx once; persistent 500 is a finding. `/south-africa` historically returns 500 — record it and continue.

---

## 3. Extract and normalize

Use this exact pipeline:

```bash
python - <<'PY'
from bs4 import BeautifulSoup
from pathlib import Path
for p in sorted(Path('.tmp/bobplus/raw').glob('*.html')):
    soup = BeautifulSoup(p.read_text(), 'html.parser')
    card = soup.select_one('.page-body .card')
    out = Path('.tmp/bobplus/frag', p.name)
    out.write_text(str(card) if card else '')
PY

for f in .tmp/bobplus/frag/*.html; do
  pandoc -f html -t gfm --wrap=none "$f" -o ".tmp/bobplus/md2/$(basename "$f" .html).md"
done

python - <<'PY'
import re, pathlib, json
# Build slug -> url map from the manifest
manifest = pathlib.Path('.tmp/bobplus/MANIFEST.md').read_text()
slug_url = {}
for line in manifest.splitlines():
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 4 and parts[1] and parts[1] != 'Slug':
        slug_url[parts[1]] = parts[2]

for p in sorted(pathlib.Path('.tmp/bobplus/md2').glob('*.md')):
    text = p.read_text()
    # Remove wrapper divs and style blocks
    text = re.sub(r'<div[^>]*>', '', text)
    text = re.sub(r'</div>', '', text)
    text = re.sub(r'<style>.*?</style>', '', text, flags=re.S)
    # Remove "Copy" button lines
    lines = [ln for ln in text.splitlines() if not ln.strip().lower() == 'copy']
    slug = p.stem
    url = slug_url.get(slug, f'https://developers.bobplus.africa/{slug.replace("-", "/")}')
    header = [f'Source: {url}', f'Slug: {slug}', '']
    out = pathlib.Path('.tmp/bobplus/md', p.name)
    out.write_text('\n'.join(header + lines) + '\n')
PY
```

Important cleanup rules:
- Keep all JSON/curl/PHP/JS examples verbatim.
- Do not edit numbers, channel codes, or placeholder hosts.
- Flatten HTML tables to markdown tables; if `pandoc` emits broken tables, fix them manually and document the fix in the report.
- Write a `Source: <url>` and `Slug: <slug>` line at the top of each clean markdown file. Build the URL map from the manifest, not from slug guessing.

---

## 4. Pre-diff against current corpus

Before involving subagents, produce a quick orientation map:

```bash
python - <<'PY'
import pathlib, hashlib
src_dir = pathlib.Path('.tmp/bobplus/md')
print('Fetched sources:')
for p in sorted(src_dir.glob('*.md')):
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    print(f'  {p.name:40} {h}')
PY
```

This is not a direct file-to-file diff (one reference may merge several sources), but it lets you spot new or changed source files quickly. Also note the docs version string and any new pages from §2.3.

---

## 5. Run overlapping subagent analysis

Launch **3 coder subagents** with the identical prompt below. Use default model (do not pass an explicit model alias — the system will use the parent model). Each writes its report to `.tmp/bobplus/reports/agent-{A,B,C}-update-requirements.md`.

> **Subagent prompt**
> You are a coding agent analyzing the Bobplus Payments API skill corpus for update requirements after a documentation refresh.
>
> Inputs:
> 1. Current corpus: `.kimi/mirror/OnDemand/bobplus-api/SKILL.md` and `.kimi/mirror/OnDemand/bobplus-api/references/*.md`.
> 2. If `references/contradictions.md` exists, read it; if not, note that it is missing and treat all contradictions as unregistered.
> 3. Refreshed source: `.tmp/bobplus/md/*.md` and `.tmp/bobplus/MANIFEST.md`.
> 4. Orientation map: fetched source file list and SHA-256 prefixes from §4.
>
> Produce a structured report and save it to `.tmp/bobplus/reports/agent-{A,B,C}-update-requirements.md` with exactly these sections:
> - **Executive Summary** — 3–5 bullets on the biggest discrepancies.
> - **Per-Reference Update Requirements** — for each `references/*.md` file, list concrete tasks using exactly one of: ADD, REWRITE, REMOVE, CLARIFY, VERIFY. Cite source file path and, where possible, heading/line in the current reference.
> - **New Contradictions** — conflicts not already in `references/contradictions.md`. For each: describe, cite both source URLs, recommend add-to-contradictions.md vs resolve-in-corpus.
> - **Questions for Bobplus** — factual questions the docs cannot answer.
> - **Meta-Observations** — limitations, source artifacts, or contradictions in your own analysis.
>
> Rules: evidence-backed; every claim cites a file path or URL; do not edit files; use English; target 600–1200 words.

Wait for all three. If one times out, read its partial report.

---

## 6. Synthesize subagent outputs and resolve conflicts

1. Read all three reports.
2. Where all three agree, treat as consensus.
3. Where they disagree, verify directly from `.tmp/bobplus/md/<slug>.md` and the current reference. If the disagreement itself reveals an ambiguity, document it as a meta-contradiction in `references/contradictions.md`.
4. Create `references/contradictions.md` if it does not exist. Use lazyload frontmatter: `subject` (30–50 words, no articles), `index` cards with `anchor`, `what`, `problem` (30–50 words, no articles, semicolon-separated cloud), `use_when`, `avoid_when`, `expected`. Each body section needs `[ref: #<anchor>]` and a `Sources:` line.
5. Validate: `uvx --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py OnDemand/bobplus-api/references/contradictions.md`. Fix until PASS.

---

## 7. Update the corpus

For each reference file, apply the consensus update requirements. Preserve existing `[ref: #...]` anchors and heading slugs (heading renames are forbidden by `markdown-protocol`). Only rewrite changed sections; unchanged sections keep their existing wording and `Sources:` line.

Per-file checklist:

### `SKILL.md`
- [ ] Update provenance pin: new date, docs version string if changed, `/south-africa` HTTP status.
- [ ] Update Source URL Map if new pages were discovered.
- [ ] Update Signature Map if channel codes or `x-hash` semantics changed.
- [ ] Add/update cross-references to `references/contradictions.md`.
- [ ] Add/update §"Open Questions for Bobplus".

### `references/getting_started.md`
- [ ] Country matrix: add/remove markets, update operator labels, merge duplicated rows.
- [ ] Rate-limit note (per-minute vs per-second conflict).
- [ ] `telco` field note.
- [ ] Update scrape date.

### `references/payins.md`
- [ ] Mobile Money Deposit channel-code table from `c2b-momo-payin.md`.
- [ ] Add/remove `telco` field in request-body table.
- [ ] Mark `x-hash` ambiguity (headers table omits it, curl example comments it).
- [ ] Burundi SMS-approval note.
- [ ] South Africa EFT/Capitec section if `/south-africa` becomes available.
- [ ] Update scrape date.

### `references/payouts.md`
- [ ] Mobile Money Payout channel-code table from `b2c-momo-payout.md`.
- [ ] Add/remove `telco` field.
- [ ] Preserve NGN bank-payout ambiguity (`300043` vs `900020`/`900021`).
- [ ] Update scrape date.

### `references/security.md`
- [ ] X-Hash wording: "`businessId` or the agreed payload"; note undefined payout payload.
- [ ] Signature example inconsistency (`account+customer_code` vs `channel+reference+currency+amount`).
- [ ] Header casing note (`signature:` vs `Signature:`).
- [ ] Update scrape date.

### `references/nigeria.md`
- [ ] Channel definitions if changed.
- [ ] Request-field semantics (`bank_code`, `result_url`).
- [ ] Payout/payin examples.
- [ ] Update scrape date.

### `references/account_services.md`
- [ ] Statement signature omission (`from_date` required but not signed).
- [ ] `amount` string-vs-numeric note.
- [ ] Update scrape date.

### `references/utilities.md`
- [ ] Webhook failed-hash field order.
- [ ] Rate-limit unit conflict.
- [ ] Transaction-status shape.
- [ ] Update scrape date.

General rules for edits:
- Do not invent facts.
- Preserve masked credentials (`XXXXXXX`, `<token>`).
- Every section must end with `Sources:` citing the URL it was curated from.
- Do not remove `[ref: #...]` markers.

---

## 8. Validate

```bash
uvx --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py \
    OnDemand/bobplus-api/references/*.md
```

Fix every FAIL before proceeding. This validator enforces the lazyload profile (word bands, cloud discipline, cross-field dedup, anchor/ref consistency).

---

## 9. Sync to mirror

`just sync-skills-mirror` will report `INSYNC` without copying because it compares the latest git commit timestamp to the mirror mtime. Therefore copy manually:

```bash
cp OnDemand/bobplus-api/SKILL.md .kimi/mirror/OnDemand/bobplus-api/SKILL.md
cp OnDemand/bobplus-api/CHANGELOG.md .kimi/mirror/OnDemand/bobplus-api/CHANGELOG.md
cp OnDemand/bobplus-api/prompts/refresh.md .kimi/mirror/OnDemand/bobplus-api/prompts/refresh.md
cp OnDemand/bobplus-api/references/*.md .kimi/mirror/OnDemand/bobplus-api/references/
```

Then re-run validation on the mirror copies to be sure:

```bash
uvx --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py \
    .kimi/mirror/OnDemand/bobplus-api/references/*.md
```

---

## 10. Update CHANGELOG

Append a dated section to `OnDemand/bobplus-api/CHANGELOG.md` with subsections Changed/Added/Removed/Notes. Do not retroactively edit old entries.

---

## 11. Persist memory

Record the refresh outcome as a Serena memory under `reports/project/bobplus_api_refresh_<YYYY-MM-DD>` per `serena-protocol`. Include: what changed, what was checked unchanged, broken/fixed pages, open questions.

---

## 12. Final summary

Write `.tmp/bobplus/REFRESH_SUMMARY.md` with:
- refresh date and docs version;
- changed files with one-line descriptions;
- validation result;
- open questions for Bobplus;
- risk notes.

Report the summary to the user in Russian.

---

## Guardrails and stop conditions

- **Stop and ask the user** if:
  - the site structure changed fundamentally (new platform, new IA);
  - a new page appears that does not obviously map to the existing reference files;
  - a previously working page now returns 404/500 persistently;
  - the docs version string changed but the change is unclear (major vs minor).
- Never "fix" contradictions in the docs — preserve them in `references/contradictions.md`.
- Never hardcode or invent a production base URL.
- Never drop a `Sources:` line.
- Never skip validation.
- Never install packages into the project environment; use `uvx --with <pkg>` for ephemeral needs.
