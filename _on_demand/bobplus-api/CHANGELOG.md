# Changelog

All notable changes to the `bobplus-api` skill corpus.

## 2026-09-09 — Refresh against re-fetched docs

### Changed
- `SKILL.md`: provenance pin to 2026-09-09 (docs version still V2.1.2, `/south-africa` still HTTP 500); payin row of the Signature Map now records `x-hash` as ACTIVE in the curl example; known-inconsistencies list extended with the payin `x-hash` table-vs-example conflict; open question #3 reworded; open questions #12 (balance `account.name` semantics) and #13 (personal-data field semantics) added.
- `references/payins.md`: curator note rewritten — the momo-payin curl example now sends `x-hash` as an active header (was commented out at the 2026-08-25 pin) while the headers table still omits it; example block updated to match the source.
- `references/nigeria.md`: Opay payout example updated to match the refreshed source (`"bank_name": "bank_name"`, was `"N/A"`).
- `references/utilities.md`: curator note added to the status-query section — example `transaction_id` equals the request `reference` while the response `reference` differs; `acc_name`/`acc_no` semantics undefined.
- `references/account_services.md`: curator note added — balance `data.account.name` is empty in the source example, semantics undocumented.

### Added
- `references/contradictions.md`: 5 new registered contradictions (14 → 19): payin `x-hash` table-vs-example, Nigeria VA response `acc_no` shape, generate-signature field-order mismatch, status-query reference semantics, bank-payout currency examples omitting NGN.

### Removed
- (nothing)

### Notes
- Owner-focus audit: exhaustive per-endpoint sweep of personal-data fields (`acc_name`, `account_name`, `account.name`) across all 18 fresh pages — no name-bearing field present in the source is missing from the corpus; the status-query REQUEST body contains only `wallet_no`+`reference` (ФИО appears only in its RESPONSE, as `data.acc_name`). Two fields flagged as undersold (present, semantics unexplained) and escalated to open questions #12–#13.
- Country-matrix "drift" reported by two analysis agents (Nigeria Airtel Money, Ivory Coast Orange, Sierra Leone method) was verified against raw HTML and proven to be a pandoc rowspan-flatten artifact — the live page still contains those rows; corpus matrix unchanged.
- All 14 previously registered contradictions persist verbatim in the refreshed source.
- Analysis: 3 parallel subagent reports in `.tmp/bobplus/reports/`; mirror updated manually per runbook §9.

## 2026-08-25 — Refresh against re-fetched docs

### Changed
- `SKILL.md`: updated provenance pin to 2026-08-25; expanded known-inconsistencies list; added payin `x-hash` ambiguity note; added "Open Questions for Bobplus" section.
- `references/getting_started.md`: added Burundi (`BIF`, Lumicash) and Zimbabwe (`ZWG`, Ecocash); updated DRC operators to `Africel`, `Mpesa`, `Orange`, `Airtel`; updated Senegal operators to `Wave`, `Mix`; added `telco` field note.
- `references/payins.md`: rewrote Mobile Money Deposit channel-code table with refreshed codes (Benin `800017`, Cameroon `800009`, DRC `800011`, Ivory Coast `800003`, Mali `800007`, Rwanda `910001`, Senegal `800005`, Burundi `910003`, Zimbabwe `180003`); added conditional `telco` field; marked `x-hash` example as commented/ambiguous; added Burundi SMS-approval note.
- `references/payouts.md`: rewrote Mobile Money Payout channel-code table with refreshed codes (Benin `800018`, Cameroon `800010`, DRC `800012`, Ivory Coast `800004`, Mali `800008`, Rwanda `910002`, Senegal `800006`, Burundi `910004`, Zimbabwe `180004`); added conditional `telco` field.
- `references/security.md`: clarified X-Hash wording to "`businessId` or the agreed payload"; noted that payout X-Hash payload is undefined; added header-casing note.
- `references/nigeria.md`: refreshed `300043` payout example to match current source (`Test Customer`, account `8127589303`).

### Added
- `references/contradictions.md`: new reference file registering 14 documented contradictions and ambiguities in the Bobplus API docs.

### Notes
- `references/account_services.md` and `references/utilities.md` required only the scrape-date update; their factual content already matched the refreshed source.
- `just sync-skills-mirror` did not copy uncommitted files (it compares git timestamp to mirror mtime), so the mirror was updated manually.
