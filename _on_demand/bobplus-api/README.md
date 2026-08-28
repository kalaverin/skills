# bobplus-api
[ref: #ba-intro]

Integration knowledge for the Bobplus Payments API (Africa): authentication, signing, payins, payouts, and account services.

## What it does
[ref: #ba-what]

This skill is the offline knowledge base for the **Bobplus Payments API v2**. It covers bearer token authentication, RSA+SHA-256 request signing, the outbound `x-hash` header, C2B payins (mobile money, ZAR EFT/Capitec, Nigeria virtual accounts), B2C payouts (bank, mobile money), account services (balance, statement), and utility endpoints (bank codes, transaction status, webhook callbacks). All facts are pinned to docs version **V2.1.2** scraped 2026-08-12.

## When it activates
[ref: #ba-when]

Activates when the user mentions Bobplus, Bob+, `developers.bobplus.africa`, African payments, mobile money, MOMO payin/payout, C2B/B2C, or related keywords in English or Russian.

Examples:

- "Add Bobplus payin."
- "Implement Bob+ mobile money deposit."
- "Sign Bobplus requests with RSA."
- "Validate Bobplus webhook."

## How to run / use it
[ref: #ba-how]

The skill is reference material used when writing or reviewing integration code.
When a request touches Bobplus, the agent routes through the reference corpus using the `frontmatter-protocol` lazy-load funnel and extracts only the sections needed for the task.
All endpoint paths, channel codes, field sets, and signature recipes are drawn from the captured corpus rather than from training data.
Use `prompts/refresh.md` if the docs need to be re-scraped.

## What it produces
[ref: #ba-produces]

- Correctly authenticated and signed HTTP requests to Bobplus endpoints.
- Webhook handlers that verify the HMAC-SHA256 `hash` field using the **consumer key**.
- Polling logic that queries transaction status with proper retry semantics.

## Dependencies and why they matter
[ref: #ba-deps]

- **frontmatter-protocol** — provides the lazy-load routing used to consume the `references/` corpus without reading every file whole.
- **python-lang** or another language skill — supplies language-specific implementation style while this skill supplies the domain rules.

## Strengths and trade-offs
[ref: #ba-tradeoffs]

### Strong sides
[ref: #ba-strong]

- Consolidates mobile-money, bank-transfer, and wallet payout flows in one place.
- Includes exact RSA signing concatenations and `x-hash` rules that are easy to get wrong.
- Covers both initiation and reconciliation (status polls and webhooks).

### Weak sides / limits
[ref: #ba-weak]

- The corpus reflects a specific provider snapshot (V2.1.2, 2026-08-12) and can become stale if Bobplus changes its contracts.
- It is reference, not code; the agent still has to implement the actual HTTP calls.
- The source docs contain placeholder base URLs and a few internal inconsistencies (see Gotchas).

### Common pitfalls / gotchas
[ref: #ba-pitfalls]

- **Base URLs are placeholders in the source docs** (`https://prod-url-here`, `https://base-url-here.com`, etc.). Always take the real base URL from configuration; avoid hardcoding a placeholder or an invented host.
- **Outbound signed requests** use RSA+SHA-256. Payouts **require** the `x-hash` header; payin examples also show it.
- **Inbound webhooks** (`result_url`) are verified as **HMAC-SHA256 keyed with the consumer key** over the documented field order, comparing against the payload's `hash` field. Compare against the payload's `hash` field rather than verifying with a generic "configured secret" or the `x-hash` logic.
- **Known source-doc inconsistencies** (flag them to the user when relevant):
  - NGN payout channel is documented both as `300043` (Nigeria guide, MoMo payout table) and as `900020`/`900021` (bank payout table).
  - Rate limit is stated as 1500/minute on the main page and 1500/second on the bank-codes page.
- Keep credentials masked (`XXXXXXX`, `<token>`) in output.
- The `/south-africa` guide page returned HTTP 500 at the pin date; the ZAR flow is covered in `references/payins.md`.

## Repository layout
[ref: #ba-layout]

```text
_on_demand/bobplus-api/
├── references/           # Curated provider docs
│   ├── getting_started.md      # Platform overview, country support, IP whitelisting
│   ├── security.md             # Bearer auth, RSA signature, x-hash generation
│   ├── account_services.md     # Balance and statement
│   ├── payins.md               # C2B payins: mobile money, ZAR EFT/Capitec, NGN virtual account
│   ├── nigeria.md              # NGN integration guide and examples
│   ├── payouts.md              # B2C payouts: bank and mobile money
│   └── utilities.md            # Bank codes, webhook callback, transaction status query
├── prompts/
│   └── refresh.md              # Re-scrape runbook for updating the corpus
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: routing index, signature map, violation protocol
```

## Reference overview
[ref: #ba-refs]

| File | What it covers |
|------|----------------|
| `references/getting_started.md` | Platform conventions, versioning, rate limits, country support, IP whitelisting |
| `references/security.md` | Bearer token, RSA+SHA-256 signature recipe, `x-hash` header generation |
| `references/account_services.md` | Wallet balance lookup and full statement |
| `references/payins.md` | Mobile money payin, ZAR EFT/Capitec, NGN virtual account |
| `references/nigeria.md` | NGN channels, request fields, examples, statuses |
| `references/payouts.md` | Bank payout and mobile money payout |
| `references/utilities.md` | Bank codes, webhook callback payload/HMAC verification, transaction status query |
| `prompts/refresh.md` | Re-scraping and actualizing this corpus |

## Important conventions / gotchas
[ref: #ba-conventions]

- Treat the corpus as the source of truth for Bobplus facts; avoid answering from training data or guessing endpoints, fields, or channel codes.
- Route through `frontmatter-protocol` lazy-load anchors instead of reading files whole.
- Inbound webhook verification uses HMAC-SHA256 keyed with the **consumer key**, not a generic secret.
- Outbound payouts require the `x-hash` header.
- Take the real base URL from configuration; source docs use placeholders.
- Avoid storing raw credentials, consumer keys, or RSA private keys in memory files.
