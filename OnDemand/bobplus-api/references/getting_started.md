---
subject: "Bobplus onboarding, platform conventions, country coverage; REST architecture, `/api/v2/` prefix, bearer token auth, JSON payloads, rate limiting, supported markets, currencies, payment methods, payins, payouts, webhook callbacks, IP whitelisting, quickstart checklist, environment readiness."
index:
  - anchor: getting-started-platform-overview
    what: "Platform-level conventions of the Bobplus API: REST/stateless architecture, `/api/v2/` URL prefix, bearer-token auth model, JSON-only payloads, error semantics, `1500` requests/minute throttle — the baseline every integration decision builds on."
    problem: "Agent kicks off integration with payments platform and needs ground rules before first call; guessing base URL layout, versioning scheme, auth model, throttling budget yields rejected requests and rework; greenfield projects, spec compliance, architecture conventions, rate headroom, environment onboarding."
    use_when: "First contact with the Bobplus API; choosing HTTP verbs or payload formats; estimating request volume against the published throttle; any question about API version or endpoint URL shape."
    avoid_when: "Concrete endpoint schemas — those live in the payins, payouts, account-services, and utilities files; credential issuance and signing flows — those live in the security file."
    expected: "Every request the agent drafts uses the correct `/api/v2/` prefix, JSON content type, bearer header, and stays inside the rate budget."
  - anchor: getting-started-country-support
    what: "The supported-market matrix: every country with its currency, payment methods (mobile money operators, bank transfers, cards, vouchers), and whether each runs payins, payouts, or both."
    problem: "Agent must confirm whether target market or operator is covered before writing payment code; wrong coverage assumption surfaces as failed transactions late in integration; geographic scope, currency mapping, operator availability, momo acceptance, corridor validation, geography."
    use_when: "Scoping which countries or currencies an integration must handle; selecting wallet and bank operators per market; answering 'is method X supported in country Y' questions; planning payout versus payin capability per corridor."
    avoid_when: "Endpoint request/response schemas for a specific channel — load payins or payouts; bank code values — load utilities; Nigeria channel-specific fields — load the Nigeria guide file."
    expected: "Integration scope names only markets, currencies, and operators the matrix confirms, with payin/payout direction known per method."
  - anchor: getting-started-ip-whitelisting
    what: "The IP whitelisting prerequisite: only API requests from approved IPs are accepted; setup flow (identify public IPs, send to the Bobplus technical team, wait for confirmation) plus upkeep practices."
    problem: "Integration works in development yet production calls get rejected; unregistered server IPs silently block every request regardless of valid credentials; network restrictions, source filtering, environment cutover, infrastructure changes, allowlist, connectivity, helpdesk tickets, firewall rules."
    use_when: "Moving from sandbox to production; diagnosing rejected calls despite valid token; planning infrastructure with changing egress IPs; onboarding new servers."
    avoid_when: "Credential or signature problems — the security file covers auth failures; endpoint-level errors — the respective API section owns those."
    expected: "All server egress IPs are whitelisted and confirmed, and calls from unapproved addresses are understood to fail by design, not by misconfiguration."
---

# Getting Started with the Bobplus API

Scraped from `https://developers.bobplus.africa` (docs version V2.1.2) on 2026-08-25; the Nigeria country guide lives in `nigeria.md`.

## Platform Overview

[ref: #getting-started-platform-overview]

Sources: [Developer Docs (home)](https://developers.bobplus.africa/)

The Bobplus API is RESTful and stateless: the application communicates over HTTPS with Bearer Token authentication, and all data is exchanged as JSON.

Quickstart checklist:

1. **Sign up** on the Bobplus business portal to get API keys.
2. **Obtain a Bearer Token** per the authentication guide (security file).
3. **Test endpoints** with Postman, curl, or any HTTP client.
4. **Integrate** and go live.

Design and standards:

- **HTTP methods:** `GET` retrieves, `POST` creates, `PUT`/`PATCH` update, `DELETE` removes.
- **Data format:** all requests and responses use `application/json`.
- **Authentication:** all endpoints require a Bearer Token in the `Authorization` header.
- **Error handling:** standard HTTP status codes with clear error messages.

Versioning: current API version is **v2**; every endpoint is prefixed with `/api/v2/`.

Rate limiting: **1500 requests per minute** by default; exceeding it returns HTTP `429` with a `Retry-After` header.

API families:

- **Account Services API** — account information, balances, statements.
- **Receive Money API (C2B / payins)** — accept customer payments via mobile money and other channels.
- **Send Money / BULK Payment API (B2C / payouts)** — disburse payments to customers, employees, and vendors, individually or in bulk.

## Supported Countries, Currencies and Payment Methods

[ref: #getting-started-country-support]

Sources: [Country Support](https://developers.bobplus.africa/country-support)

The matrix below lists every supported market with its currency, payment methods, and supported directions (flattened from the source table; duplicate rows removed). **Payins** are Customer-to-Business (C2B) collections; **Payouts** are Business-to-Customer (B2C) disbursements.

| Market | Currency | Payment method | Directions |
|---|---|---|---|
| Kenya | KES | Mpesa | Payins, Payouts |
| Kenya | KES | Airtel Money | Payins, Payouts |
| Kenya | KES | Bank Transfer | Payouts |
| Uganda | UGX | MTN | Payins, Payouts |
| Uganda | UGX | Airtel Money | Payins, Payouts |
| Uganda | UGX | Bank Transfers | Payouts |
| Tanzania | TZS | Halotel | Payins, Payouts |
| Tanzania | TZS | Airtel Money | Payins, Payouts |
| Tanzania | TZS | Tigo | Payins, Payouts |
| Tanzania | TZS | Vodacom | Payins, Payouts |
| Ivory Coast | XOF | Orange | Payins, Payouts |
| Ivory Coast | XOF | MTN | Payins, Payouts |
| Ivory Coast | XOF | Moov | Payins, Payouts |
| Ivory Coast | XOF | Wave | Payins, Payouts |
| Nigeria | NGN | Airtel Money | Payins, Payouts |
| Nigeria | NGN | MTN | Payins, Payouts |
| Nigeria | NGN | Bank Transfers / Local Cards / E-wallets | Payins, Payouts |
| Nigeria | NGN | Cards / Bank Transfers / Momo | Payins, Payouts |
| Nigeria | NGN | Virtual Account | Payins |
| Nigeria | NGN | NUBAN Bank Transfer | Payouts |
| South Africa | ZAR | EFT | Payins |
| South Africa | ZAR | Capitec | Payins |
| South Africa | ZAR | RTC Bank Transfer | Payouts |
| Benin | XOF | Moov | Payins, Payouts |
| Benin | XOF | MTN | Payins, Payouts |
| Benin | XOF | Celtis | Payins, Payouts |
| Burkina Faso | XOF | Moov | Payins, Payouts |
| Burkina Faso | XOF | Orange | Payins, Payouts |
| Cameroon | XAF | Orange | Payins, Payouts |
| Cameroon | XAF | MTN | Payins, Payouts |
| Congo Brazzaville | XAF | Airtel Money | Payins, Payouts |
| Congo Brazzaville | XAF | MTN | Payins, Payouts |
| DRC | CDF | Africel | Payins, Payouts |
| DRC | CDF | Mpesa | Payins, Payouts |
| DRC | CDF | Orange | Payins, Payouts |
| DRC | CDF | Airtel | Payins, Payouts |
| Gabon | XAF | Airtel Money | Payins, Payouts |
| Gabon | XAF | Moov | Payins, Payouts |
| Ghana | GHS | MTN | Payins, Payouts |
| Ghana | GHS | Telecel | Payins, Payouts |
| Ghana | GHS | AT | Payins, Payouts |
| Guinea | GNF | MTN | Payins, Payouts |
| Guinea | GNF | Orange | Payins, Payouts |
| Lesotho | LSL | Mpesa | Payins, Payouts |
| Malawi | MWK | TNM | Payins, Payouts |
| Malawi | MWK | Airtel Money | Payins, Payouts |
| Malawi | MWK | Airtel Money, TNM | Payins, Payouts |
| Mozambique | MZN | Mpesa | Payins, Payouts |
| Mozambique | MZN | Movitel | Payins, Payouts |
| Rwanda | RWF | Airtel Money | Payins, Payouts |
| Rwanda | RWF | MTN | Payins, Payouts |
| Senegal | XOF | Wave | Payins, Payouts |
| Senegal | XOF | Mix | Payins, Payouts |
| Sierra Leone | SLL | Orange | Payins, Payouts |
| Zambia | ZMW | Airtel Money | Payins, Payouts |
| Zambia | ZMW | MTN | Payins, Payouts |
| Zambia | ZMW | Zamtel | Payins, Payouts |
| Egypt | EGP | Orange, Fawry, Vodafone, Etisalat & Cards | Payins, Payouts |
| Egypt | EGP | Cards | Payouts |
| Egypt | EGP | Bank Payouts | Payouts |
| Egypt | EGP | Fawry, Meeza | Payins, Payouts |
| Gambia | GMD | Momo | Payins, Payouts |
| Gambia | GMD | Wave, Afrimoney, Qcell | Payins, Payouts |
| Chad | XAF | Airtel, Moov | Payins, Payouts |
| Equatorial Guinea | XAF | MTN, Orange | Payins, Payouts |
| Central African Republic | XAF | Orange | Payins, Payouts |
| Botswana | BWP | Prepaid Voucher | Payins, Payouts |
| Mali | XOF | Momo (Orange, Moov, Sama) | Payins, Payouts |
| Guinea Bissau | XOF | Momo (Orange, MTN) | Payins, Payouts |
| Togo | XOF | Momo (Tmoney, Moov) | Payins, Payouts |
| Niger | XOF | Momo | Payins, Payouts |
| Mauritania | MRU | Momo | Payins, Payouts |
| Burundi | BIF | Lumicash | Payins, Payouts |
| Zimbabwe | ZWG | Ecocash | Payins, Payouts |

Notes from the source documentation:

- Some payment methods support both directions, others only one.
- Nigeria and South Africa have dedicated country integration guides; the Nigeria guide is captured in `nigeria.md`, while the South Africa guide page was broken (HTTP 500) at scrape time — the ZAR EFT payin flow is documented in `payins.md` instead.
- For **Cameroon, Senegal, Ivory Coast, Mali, DRC, and Benin**, mobile-money payin and payout requests require/accept an additional `telco` field specifying the operator. Accepted values include `orange`, `mtn`, `moov`, `wave`, `vodacom`, `airtel` (per-country mapping is in `references/payins.md` and `references/payouts.md`).

## IP Whitelisting

[ref: #getting-started-ip-whitelisting]

Sources: [IP Whitelisting](https://developers.bobplus.africa/ip-whitelist)

Bobplus requires all clients to provide an **IP whitelist**: only API requests originating from approved IP addresses are accepted. Without an approved whitelist, all API requests are rejected.

Setup flow:

1. Identify the public IP addresses of the production and test servers.
2. Send the IP list to the Bobplus technical team.
3. Wait for confirmation that the IPs are whitelisted.
4. After approval, only requests from those IPs are allowed; all others are rejected.

Upkeep practices:

- Keep the whitelist current; remove unused or deprecated IPs promptly.
- Notify Bobplus support immediately when infrastructure changes.
- Combine IP whitelisting with strong authentication for maximum security.
