---
name: bobplus-api
description: "Bobplus Payments API (Africa) integration knowledge: bearer auth, RSA request signing, X-Hash, C2B payins (mobile money, ZAR EFT/Capitec, Nigeria virtual accounts), B2C payouts (bank, mobile money), account services (balance, statement), utilities (bank codes, webhook callbacks, transaction status query). Use when answering questions or writing code against the Bobplus API: bobplus, bob+, developers.bobplus.africa, африканские платежи, mobile money, momo payin/payout, C2B/B2C Africa."
triggers:
  any:
    request: "bobplus, bob+, bob plus, bobplus api, bobplus africa, developers.bobplus.africa, бобплюс, африканские платежи, платежи африка, mobile money africa, momo payin, momo payout, c2b africa, b2c africa, m-pesa integration, mpesa africa payments"
    reason: "Questions or code work against the Bobplus payments platform must be answered from the captured reference corpus, not from training data."
runtime: true
requires:
  - frontmatter-protocol
version: 0.1.0
---

# SKILL: Bobplus Payments API (Africa)

This skill is the offline knowledge base for the **Bobplus Payments API v2** (financial, eCommerce, and business management APIs for Africa), captured from `https://developers.bobplus.africa`. Use it to answer integration questions and to write code against the API without visiting the site.

**Provenance pin:** docs version **V2.1.2**, scraped 2026-08-12 from 17 pages (the `/south-africa` guide page was broken, HTTP 500 — its ZAR flow is covered in `references/payins.md`). The site sends no `Last-Modified`/`ETag` headers, so freshness is only verifiable by re-scraping; the re-scrape runbook lives in `prompts/refresh.md`.

## 1. Compliance and Default Rules

- This corpus is the **binding source of truth** for Bobplus API facts in this workspace: endpoint paths, methods, field sets, channel codes, signature recipes, and payload shapes MUST come from `references/`, never from training data or guesses. If the corpus does not cover a question, say so and offer to check the live site per the `kagi-search` skill.
- **Base URLs are placeholders in the source docs** (`https://prod-url-here`, `https://base-url-here.com`, `https://here-prod-api-url.com`). Code you produce MUST take the real base URL from configuration, never hardcode a placeholder or an invented host.
- Examples in the corpus use masked credentials (`XXXXXXX`, `<token>`); keep them masked in your output.

## 2. The Signature Map (always check before writing request code)

Signature requirements differ per endpoint — every signed value is SHA-256 with the RSA private key, base64-encoded, per `references/security.md`:

| Operation | Signed concatenation | Extra headers |
|---|---|---|
| Auth login (`/api/v2/auth/login`) | — (no signature) | — |
| Balance (`GET /api/v2/wallet/{wallet_no}/{currency}`) | `wallet_no+currency` | — |
| Statement (`POST /api/v2/wallet/statement`) | `wallet_no+to_date+limit` | — |
| Payin (`POST /api/v2/payment/`) | `channel+reference+currency+amount` | `x-hash` used in docs' examples |
| Payout (`POST /api/v2/payment/`) | `channel+reference+currency+amount` | `x-hash` REQUIRED |
| Status query (`POST /api/v2/payment/status-query`) | `wallet_no+reference` | — |
| Inbound webhook (`result_url`) | HMAC-SHA256 keyed with the **consumer key** over the documented field order (success/failure differ) | verify `hash`, ack HTTP 200 |

Known source-doc inconsistencies (preserved deliberately — flag them to the user when relevant):

- NGN payout channel is documented both as `300043` (Nigeria guide, momo payout table) and as `900020`/`900021` (bank payout table).
- Rate limit is stated as 1500/minute on the main page and 1500/second on the bank-codes page.

## 3. Lazy-Load Protocol (CRITICAL)

You MUST NOT read the `references/` files in full. Route through their frontmatter cards and extract only the sections you need per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (subject map → card selection → bounded anchor extraction).

### Routing Index

| Trigger / Situation | File | Anchor |
|---|---|---|
| Platform conventions, versioning, rate limits, API families. | `references/getting_started.md` | `[ref: #getting-started-platform-overview]` |
| Supported countries, currencies, operators, payin/payout coverage per market. | `references/getting_started.md` | `[ref: #getting-started-country-support]` |
| IP whitelist setup and production cutover. | `references/getting_started.md` | `[ref: #getting-started-ip-whitelisting]` |
| Bearer token issuance, expiry, 401 handling. | `references/security.md` | `[ref: #security-authentication]` |
| RSA key pair, request `signature` generation. | `references/security.md` | `[ref: #security-signature]` |
| `x-hash` header generation. | `references/security.md` | `[ref: #security-x-hash]` |
| Wallet balance lookup. | `references/account_services.md` | `[ref: #account-services-balance]` |
| Full transaction statement over a date range. | `references/account_services.md` | `[ref: #account-services-statement]` |
| Mobile money payin in any country; per-country payin channel codes. | `references/payins.md` | `[ref: #payins-mobile-money]` |
| ZAR payin: EFT `900017`, Capitec `900018`, `acc_ref`. | `references/payins.md` | `[ref: #payins-south-africa]` |
| NGN payin via dynamic virtual account `300041`. | `references/payins.md` | `[ref: #payins-nigeria-virtual-account]` |
| Nigeria channels, request fields, all NGN examples, statuses. | `references/nigeria.md` | `[ref: #nigeria-payment-channels]`, `[ref: #nigeria-request-fields]`, `[ref: #nigeria-payin-examples]`, `[ref: #nigeria-payout-example]`, `[ref: #nigeria-statuses-and-notes]` |
| Bank payout to account number; bank channel codes. | `references/payouts.md` | `[ref: #payouts-bank]` |
| Mobile money payout; per-country payout channel codes. | `references/payouts.md` | `[ref: #payouts-mobile-money]` |
| Bank code lookup by country. | `references/utilities.md` | `[ref: #utilities-bank-codes]` |
| Webhook callback payload and HMAC verification. | `references/utilities.md` | `[ref: #utilities-webhook-callback]` |
| On-demand transaction status check. | `references/utilities.md` | `[ref: #utilities-transaction-query]` |
| Re-scraping and actualizing this corpus. | `prompts/refresh.md` | — |

## 4. Source URL Map

Base URL: `https://developers.bobplus.africa`. Page names as rendered on each page; every section in `references/` also carries a `Sources:` line pointing at the page(s) it was curated from.

| Page | URL | Covered in |
|---|---|---|
| Developer Docs (home) | `/` | `references/getting_started.md` |
| Country Support | `/country-support` | `references/getting_started.md` |
| IP Whitelisting | `/ip-whitelist` | `references/getting_started.md` |
| API Authentication | `/authentication` | `references/security.md` |
| Generate Signature | `/generate-signature` | `references/security.md` |
| Generate X-Hash | `/generate-x-hash` | `references/security.md` |
| Fetch Balance | `/account-services/get-balance` | `references/account_services.md` |
| Account Full Statement | `/account-services/full-statement` | `references/account_services.md` |
| Mobile Money Deposit | `/c2b/momo-payin` | `references/payins.md` |
| South Africa Payin — EFT / Capitec | `/c2b/south-africa-payin` | `references/payins.md` |
| Nigeria Collections — Virtual Account | `/c2b/nigeria-payin` | `references/payins.md` |
| Nigeria (NGN) Integration Guide | `/nigeria` | `references/nigeria.md` |
| South Africa Integration Guide | `/south-africa` | broken (HTTP 500) at pin date |
| Bank Payout — To Account Number | `/b2c/bank-payout` | `references/payouts.md` |
| MoMo Payout (Business to Client) | `/b2c/momo-payout` | `references/payouts.md` |
| Bank Codes | `/bank-codes` | `references/utilities.md` |
| Webhook Callback | `/callback-response` | `references/utilities.md` |
| Payment Transaction Status | `/transaction-status/payment` | `references/utilities.md` |

## 5. Master Execution Workflow

1. **Classify the task:** question answering, integration design, or code writing against the Bobplus API.
2. **Route:** pick the section(s) from the Routing Index (or the corpus subject map when the index misses), extract per the bounded-extraction mechanics.
3. **Answer or write code** strictly from the extracted material: correct endpoint, method, field set, channel code, and signature recipe (§2).
4. **Verify:** base URL comes from configuration; signatures use the right concatenation for the endpoint; payouts include `x-hash`; `reference` is unique per transaction; `result_url` handling and HMAC verification are in place for webhooks.

## 6. Violation Protocol

If you answer Bobplus API questions from training data, invent endpoints/fields/channel codes, hardcode a placeholder or invented base URL, or skip the corpus routing before writing integration code, halt immediately, discard the offending output, load the correct section per §3, and redo the work from the corpus.
