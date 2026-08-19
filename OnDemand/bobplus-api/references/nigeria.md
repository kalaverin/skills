---
subject: "Nigeria integration guide for Bobplus API; NGN payins, payouts, channel codes `300041` `300043` `300044` `300045`, virtual accounts, checkout payment links, Opay, PalmPay, NUBAN bank transfer, `bank_code`, `reference`, `result_url`, request examples, response statuses, webhooks, expiry, redirects."
index:
  - anchor: nigeria-payment-channels
    what: "The Nigeria channel map: payin channels `300041` (dynamic virtual accounts), `300044` (checkout payment links), `300045` (Opay and PalmPay wallets) and payout channel `300043` (NUBAN bank transfer), each with its customer-facing flow."
    problem: "Agent implements NGN money movement and must select correct channel before composing any request; wrong channel choice strands customers on flows they cannot complete; naira, wallets, deposits, collections, disbursement, routing, operators, corridors, payouts."
    use_when: "Choosing between virtual account, checkout link, wallet, and bank transfer channels for NGN; explaining the customer-facing steps of each channel; deciding payin versus payout direction."
    avoid_when: "Field-level request composition — the request-fields section owns it; non-NGN corridors — the country matrix in getting_started.md."
    expected: "Selected channel code matches the intended money flow and the integration guides the customer through that channel's steps."
  - anchor: nigeria-request-fields
    what: "The NGN request contract: `wallet_no`, `reference`, `acc_name`, `acc_no`, `email`, `amount`, `currency`, `channel`, `description`, `result_url`, conditional `bank_code`, plus Opay/PalmPay bank codes `100004` and `100033`."
    problem: "Agent composes NGN API call and risks rejection from missing or malformed fields; conditional `bank_code` rules and dual meaning of `acc_no` (phone for payins, bank account for payouts) trip integrations; field schema, mandatory parameters, conditional validation, payload composition, uniqueness constraint."
    use_when: "Building or reviewing any NGN request payload; deciding whether `bank_code` is required for a channel; generating unique `reference` values; wiring `result_url` webhooks."
    avoid_when: "Channel selection itself — the channels section; response interpretation — the examples and statuses sections."
    expected: "Every NGN payload passes validation: all mandatory fields present, `bank_code` included exactly when the channel demands it, `reference` unique per transaction."
  - anchor: nigeria-payin-examples
    what: "Copy-paste NGN payin request/response pairs: virtual account creation (`300041`) with `virtual_account` expiry block, Opay/PalmPay collection (`300045`) and checkout link (`300044`) returning `redirect_url`."
    problem: "Agent writes NGN collection code without knowing exact response shapes; missing `redirect_url` handling or ignored account expiry breaks customer payment completion; response parsing, JSON shape, sample payloads, integration testing, sandbox trials, fixtures."
    use_when: "Coding NGN payin initiation; parsing initiation responses; building mock fixtures from real response shapes; implementing redirect or account-display UX."
    avoid_when: "Payout payloads — the payout example section; status polling after initiation — the utilities file."
    expected: "Collection code posts valid initiation payloads and handles both completion paths: redirecting the customer via `redirect_url` or displaying account details before expiry."
  - anchor: nigeria-payout-example
    what: "The NGN bank transfer payout (`300043`) request/response pair: disbursement to a NUBAN account with `bank_code`, `acc_name` matching the account holder, and `PENDING` initiation status."
    problem: "Agent implements NGN disbursement to customer bank accounts and needs exact payout payload plus response semantics before coding; mismatched recipient name or wrong bank code causes failed transfers and support tickets; holder matching, initiation, settlement, beneficiaries, remittance."
    use_when: "Coding NGN payouts to bank accounts or wallets; validating recipient details before disbursement; interpreting the `PENDING` initiation state."
    avoid_when: "Collections from customers — the payin examples section; payout flows in other markets — payouts.md."
    expected: "Payout request carries holder-exact `acc_name`, valid `bank_code`, and the integration treats `PENDING` as initiated-not-settled."
  - anchor: nigeria-statuses-and-notes
    what: "NGN transaction status vocabulary (`PROCESSING`, `PENDING`, `SUCCESS`, `FAILED`) plus operational notes: virtual account expiry, redirect handling, reference uniqueness, webhook pointer, and security practices."
    problem: "Agent maps transaction states onto business logic and must avoid misreading intermediate states as final; treating `PROCESSING` or `PENDING` as failure or success corrupts reconciliation; status machine, lifecycle, callbacks, idempotency, finality, polling, settlement lag, retries."
    use_when: "Interpreting status values from API responses or webhooks; building reconciliation or retry logic; hardening the integration (HTTPS, signature verification, callback validation)."
    avoid_when: "Webhook payload structure itself — the utilities file callback section owns it; field-level payload rules — the request-fields section."
    expected: "Business logic treats only `SUCCESS` and `FAILED` as terminal, waits on `PROCESSING`/`PENDING`, and enforces unique references with validated webhook data."
---

# Nigeria (NGN) Integration Guide

Scraped from `https://developers.bobplus.africa/nigeria` (docs version V2.1.2) on 2026-08-12; currency NGN (Nigerian Naira).

## Payment Channels

[ref: #nigeria-payment-channels]

Sources: [Nigeria (NGN) Integration Guide](https://developers.bobplus.africa/nigeria)

Nigeria supports multiple payment methods for accepting customer payments and processing payouts.

| Channel code | Payment method | Type | Description |
|---|---|---|---|
| `300041` | Virtual Accounts | Payin | Dynamic virtual bank account for customer deposits |
| `300044` | Checkout Payment Links | Payin | Payment link/checkout page for bank payments |
| `300045` | Opay & PalmPay | Payin | Direct payments via Opay and PalmPay wallets |
| `300043` | Bank Transfer | Payout | Bank transfer disbursements to customer accounts |

Payin flows:

- **Virtual Accounts (`300041`):** initiate → display the virtual account to the customer → customer transfers → webhook confirmation.
- **Checkout Payment Links (`300044`):** initiate → receive payment link → customer completes payment (cards, bank transfer, or other supported methods) → webhook confirmation.
- **Opay & PalmPay (`300045`):** initiate with customer wallet details → customer authorizes → webhook confirmation.

Payout flow:

- **Bank Transfer (`300043`):** disburse funds directly to customer bank accounts via NUBAN (Nigeria Uniform Bank Account Number); requires bank code, account number, and account name.

## Request Fields

[ref: #nigeria-request-fields]

Sources: [Nigeria (NGN) Integration Guide](https://developers.bobplus.africa/nigeria)

All NGN requests go to `/api/v2/payment/` and carry this field set:

| Field | Type | Description | Required |
|---|---|---|---|
| `wallet_no` | string | Your business wallet account number | Yes |
| `reference` | string | Unique order reference per request | Yes |
| `acc_name` | string | Customer/Recipient name | Yes |
| `acc_no` | string | Customer phone number (payins) or bank account number (payouts) | Yes |
| `email` | string | Customer email address | Yes |
| `amount` | numeric | Transaction amount (no commas) | Yes |
| `currency` | string | Currency code: `NGN` | Yes |
| `channel` | numeric | Payment channel code (`300041`, `300044`, `300045`, `300043`) | Yes |
| `description` | string | Transaction description | Yes |
| `result_url` | string | Webhook URL for payment status callbacks | Yes |
| `bank_code` | string | Bank code (for `300045` Opay/PalmPay and `300043` payouts) | Conditional |

Bank codes for wallet channels:

| `bank_code` | Wallet | Usage |
|---|---|---|
| `100004` | Opay | Opay wallet collections & payouts |
| `100033` | PalmPay | PalmPay wallet collections & payouts |

For other Nigerian banks, use the full bank codes reference in `utilities.md`.

Quickstart for a virtual account payin: POST to `/api/v2/payment/` with channel `300041` → receive virtual account details in the response → display them to the customer → the customer transfers the exact amount → confirmation arrives via webhook on `result_url`.

## Payin Examples

[ref: #nigeria-payin-examples]

Sources: [Nigeria (NGN) Integration Guide](https://developers.bobplus.africa/nigeria)

Virtual account payin (channel `300041`) — request:

```json
{
    "wallet_no": "XXXXXXX",
    "reference": "CORNGN0089123036",
    "acc_name": "Test Customer",
    "acc_no": "08012345678",
    "email": "customer@example.com",
    "currency": "NGN",
    "amount": 100,
    "channel": 300041,
    "description": "Order payment",
    "result_url": "https://your-server.com/webhook"
}
```

Virtual account payin — response (note the `virtual_account` block and its `expires` timestamp):

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "acc_name": "Test Customer",
        "acc_no": "08012345678",
        "description": "Order payment",
        "transaction_id": "126072834240",
        "reference": "CORNGN0089123036",
        "status": "PROCESSING",
        "amount": 100,
        "charges": 0,
        "currency": "NGN",
        "status_description": "Account generated successfully",
        "date": "2026-07-28 13:23:15 PM",
        "fetched_at": "2026-07-28 13:23:21 PM",
        "virtual_account": {
            "account_number": "1251258358",
            "account_name": "BOBPLUS AFRICA Checkout",
            "bank_name": "78 Finance Company limited (Bank78)",
            "expires": "2026-07-28 12:23:21 PM"
        }
    }
}
```

Opay & PalmPay collection (channel `300045`) — request (`bank_code` is `100004` for Opay, `100033` for PalmPay):

```json
{
    "wallet_no": "XXXXXXX",
    "reference": "CORWALLET0199065",
    "acc_name": "Test Customer",
    "acc_no": "08012345678",
    "email": "customer@example.com",
    "currency": "NGN",
    "amount": 100,
    "channel": 300045,
    "bank_code": "100004",
    "description": "Test opay payment",
    "result_url": "your-callback-url"
}
```

Opay & PalmPay collection — response (returns `redirect_url`):

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "acc_name": "Test",
        "acc_no": "08012345678",
        "description": "Test opay payment",
        "transaction_id": "126072844637",
        "reference": "CORWALLET0199065",
        "status": "PROCESSING",
        "amount": 100,
        "charges": 0,
        "currency": "NGN",
        "status_description": "Payment initialized successfully",
        "date": "2026-07-28 16:39:10 PM",
        "fetched_at": "2026-07-28 16:39:15 PM",
        "bank_code": "100004",
        "bank_name": "N/A",
        "redirect_url": "https://opaycheckouturl"
    }
}
```

Checkout payment link (channel `300044`) — request:

```json
{
    "wallet_no": "XXXXXXX",
    "reference": "CORCHK00012349970",
    "acc_name": "Test Customer",
    "acc_no": "08012345678",
    "email": "customer@example.com",
    "currency": "NGN",
    "amount": 100,
    "channel": 300044,
    "description": "Order payment",
    "result_url": "https://your-server.com/webhook"
}
```

Checkout payment link — response (returns `redirect_url`):

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "acc_name": "Test",
        "acc_no": "08012345678",
        "description": "checkout test payment",
        "transaction_id": "126073182949",
        "reference": "CORCHK000123499780",
        "status": "PROCESSING",
        "amount": 100,
        "charges": 0,
        "currency": "NGN",
        "status_description": "Payment initialized successfully",
        "date": "2026-07-31 16:54:14 PM",
        "fetched_at": "2026-07-31 16:54:19 PM",
        "redirect_url": "https://redirect-url-to-pay"
    }
}
```

## Payout Example

[ref: #nigeria-payout-example]

Sources: [Nigeria (NGN) Integration Guide](https://developers.bobplus.africa/nigeria)

Bank transfer payout (channel `300043`) — request (`bank_code` is `100004` for Opay, `100033` for PalmPay; other banks have different codes, see `utilities.md`):

```json
{
    "wallet_no": "XXXXXXX",
    "reference": "CORNGNPAY00123744",
    "acc_name": "Elizabeth Julius",
    "acc_no": "8127586313",
    "bank_code": "100004",
    "email": "customer@example.com",
    "currency": "NGN",
    "amount": 100,
    "channel": 300043,
    "description": "Test NGN Opay payout"
}
```

Bank transfer payout — response:

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "acc_name": "Elizabeth Julius",
        "acc_no": "8127586313",
        "description": "Test NGN Opay payout",
        "transaction_id": "126072846655",
        "reference": "CORNGNPAY00123744",
        "status": "PENDING",
        "amount": 100,
        "charges": 0,
        "currency": "NGN",
        "status_description": "initiated, pending payment",
        "date": "2026-07-28 17:07:37 PM",
        "fetched_at": "2026-07-28 17:07:37 PM",
        "bank_code": "100004",
        "bank_name": "bank name"
    }
}
```

## Statuses and Operational Notes

[ref: #nigeria-statuses-and-notes]

Sources: [Nigeria (NGN) Integration Guide](https://developers.bobplus.africa/nigeria)

Transaction status vocabulary:

| Status | Description |
|---|---|
| `PROCESSING` | Transaction initiated, awaiting customer action or processing |
| `PENDING` | Transaction is pending completion |
| `SUCCESS` | Transaction completed successfully |
| `FAILED` | Transaction failed |

Important notes:

- **Virtual accounts (`300041`):** the virtual account has an expiry time; display it so customers complete the transfer before expiry.
- **Checkout & Opay/PalmPay (`300044`, `300045`):** these return a `redirect_url`; redirect the customer to it to complete payment.
- **Bank payouts (`300043`):** `acc_name` must match the bank account holder's name exactly to avoid failed transactions.
- **Bank codes:** Opay is `100004`, PalmPay is `100033`; other banks use different codes from the full list in `utilities.md`.
- **References:** every `reference` must be unique per transaction; duplicates are rejected.
- **`result_url` caveat:** the request-fields table marks `result_url` as required for all channels, yet the docs' `300043` payout example omits it — send it anyway (or confirm with Bobplus support).
- **Webhooks:** payment status updates are POSTed to `result_url`; the callback payload structure is documented in `utilities.md`.

Security practices: use HTTPS everywhere, keep the private key secret, verify signatures server-side on every request, verify webhook signatures, and validate all callback data before processing.
