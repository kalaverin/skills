# Changelog

All notable changes to the `bobplus-api` skill corpus.

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
