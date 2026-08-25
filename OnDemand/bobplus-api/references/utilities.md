---
subject: "Bobplus utility APIs; bank codes lookup, `/api/v2/banks/get-by-country`, `country_code`, webhook callback, `hash` HMAC-SHA256 verification, `result_code`, `third_party_id`, transaction status query, `/api/v2/payment/status-query`, `wallet_no+reference` signature, callback acknowledgment, fees, finality polling, missed callbacks, forged notifications, settlement confirmation."
index:
  - anchor: utilities-bank-codes
    what: "Bank code lookup: POST `/api/v2/banks/get-by-country` with `country_code` (e.g. `KE`, `TZ`) returns bank objects (`name`, `currency`, `code`) for populating `bank_code` in payout requests; bearer token only, no signature."
    problem: "Agent building payout needs recipient bank code and cannot hardcode stale lists; wrong or outdated code fails transfers; bank directory, routing identifiers, dropdown population, code resolution, kenya, tanzania, uganda, nigeria, ghana, selectors, mapping."
    use_when: "Populating a bank selector UI; resolving `bank_code` before a bank payout; refreshing cached bank lists per country."
    avoid_when: "Opay/PalmPay wallet codes — those are fixed (`100004`/`100033`, see nigeria.md); channel codes — those live in the payins and payouts tables."
    expected: "Payout requests carry current bank codes fetched per `country_code`, and bank pickers render the live list."
  - anchor: utilities-webhook-callback
    what: "The callback contract: Bobplus POSTs transaction outcomes (success and failure payloads with `channel`, `reference`, `transaction_id`, `third_party_id`, `fees`, `result_code`, `result_description`, `hash`) to `result_url`; `hash` is HMAC-SHA256 keyed with the consumer key over fields concatenated in a fixed order; acknowledge with HTTP 200."
    problem: "Agent exposes webhook endpoint and must distinguish genuine callbacks from forged ones; skipping HMAC verification lets attackers fake payment confirmations; authenticity, notification spoofing, HMAC check, field ordering, acknowledgment, replay, fraud, integrity, verifier."
    use_when: "Implementing the `result_url` receiver; verifying incoming callbacks before crediting or debiting; handling each terminal payload variant; deciding the acknowledgment response."
    avoid_when: "Polling status on demand — the transaction query section; generating outbound request signatures — security.md."
    expected: "Receiver recomputes the HMAC over the documented field order, processes only matching callbacks, and returns HTTP 200 to acknowledge."
  - anchor: utilities-transaction-query
    what: "On-demand status check: POST `/api/v2/payment/status-query` with `wallet_no` and the original `reference`, signed over `wallet_no+reference`; returns the transaction object with `status` (`SUCCESS`, `FAILED`, …) and `status_description`."
    problem: "Agent needs ground truth about transaction outcome when webhook is missed or delayed; relying solely on callbacks leaves orders stuck in unknown state; polling, verification, recovery, reconciliation, pending check, timeout, drain, certainty, inquiry, probe."
    use_when: "Verifying the final status of a payin or payout by `reference`; recovering from missed or delayed webhooks; building reconciliation or retry jobs; confirming before customer-facing state changes."
    avoid_when: "Real-time push handling — the callback section; bulk history export — the statement section in account_services.md."
    expected: "Jobs query `status-query` by reference and converge every transaction to a terminal state, webhook or no webhook."
---

# Bobplus Utility APIs

Scraped from `https://developers.bobplus.africa` (pages `bank-codes`, `callback-response`, `transaction-status/payment`; docs version V2.1.2) on 2026-08-25.

## Bank Codes

[ref: #utilities-bank-codes]

Sources: [Bank Codes](https://developers.bobplus.africa/bank-codes)

Fetches the list of banks and their codes for a given country — for payment integrations, bank selection UIs, and operations requiring bank identification.

Endpoint reference:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/banks/get-by-country` |
| Base URL | `https://base-url-here.com` (as issued to your account) |
| Description | Fetches a list of banks and their codes for a given country |

Request headers: `Authorization: Bearer <token>`, `Accept: application/json`, `Content-Type: application/json` (all required).

Request body — single field `country_code` (e.g. `KE`, `TZ`):

```json
{
    "country_code": "KE"
}
```

Example request:

```bash
curl --location --request POST 'https://base-url-here.com/api/v2/banks/get-by-country' \
--header 'Authorization: Bearer <your_token>' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "country_code": "KE"
}'
```

Success response — `data` is an array of bank objects (`name`, `currency`, `code`):

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": [
        {
            "name": "UBA Kenya Bank Ltd",
            "currency": "KES",
            "code": "76"
        },
        {
            "name": "Victoria Commercial Bank Ltd",
            "currency": "KES",
            "code": "54"
        }
    ]
}
```

Error responses:

| Status | Example | Description |
|---|---|---|
| 400 | `{"success": false, "message": "Invalid country code."}` | Bad Request |
| 401 | `{"success": false, "message": "Unauthorized."}` | Missing or invalid token |
| 429 | `{"success": false, "message": "Rate limit exceeded."}` | Too many requests (the docs state a `Retry-After` header is returned) |
| 500 | `{"success": false, "message": "Internal server error."}` | Server error |

Rate limit note: the bank-codes page states "1500 requests per **second**" while the main page states "1500 per **minute**" — treat per-minute as the safer budget; contact Bobplus support for higher limits.

## Webhook Callback

[ref: #utilities-webhook-callback]

Sources: [Webhook Callback](https://developers.bobplus.africa/callback-response)

Bobplus sends a webhook callback to your system after every **successful** or **failed** deposit or payout transaction. Handling: expose a POST endpoint → parse the JSON payload → verify the `hash` parameter → process the result → respond with HTTP 200 OK to acknowledge receipt.

Sample success callback:

```json
{
  "channel": "100001",
  "reference": "3883328",
  "transaction_id": "CP7S36ULT8P",
  "third_party_id": "SP7S36U3T8",
  "currency": "KES",
  "amount": "10",
  "fees": "0.2",
  "acc_name": "John Doe",
  "result_code": 0,
  "result_description": "The service request is processed successfully.",
  "hash": "c920aaebae731f9e16d9a8f1fc1e349b99313cf230f18126a0bbd07d64aac2e0"
}
```

Sample failed callback:

```json
{
  "channel": "100001",
  "reference": "3883328",
  "result_code": 1032,
  "transaction_id": "2345432345",
  "result_description": "DS timeout user cannot be reached",
  "hash": "e07f51540e120030f5beb594ba34f335f16f2f78c4a7a7b0d53647ac44590ff9"
}
```

Hash verification: the `hash` parameter is a SHA-256 HMAC proving the callback is from Bobplus. Concatenate all response fields in the order sent, **except the `hash` parameter**, then HMAC the resulting string with your **consumer key** (provided during registration). Field order:

- **Success callback:** `channel+reference+transaction_id+third_party_id+currency+amount+fees+acc_name+result_code+result_description`
- **Failed callback:** `channel+reference+transaction_id+result_code+result_description`

Curator's note — source inconsistency: the sample failed callback above orders its JSON fields `channel → reference → result_code → transaction_id → result_description`, which differs from the documented hash order (`transaction_id` before `result_code`). Use the documented concatenation order for HMAC verification, not the JSON sample's field order.

JavaScript example from the docs:

```js
const crypto = require('crypto');

function implodeAll(sep, arr) {
    return arr.map(item => Array.isArray(item) ? implodeAll(sep, item) : item).join(sep);
}

const callBackResponse = {
  "channel": "100001",
  "reference": "3883328",
  "transaction_id": "CP7S36ULT8P",
  "third_party_id": "SP7S36U3T8",
  "currency": "KES",
  "amount": "10",
  "fees": "0.2",
  "acc_name": "John Doe",
  "result_code": 0,
  "result_description": "The service request is processed successfully.",
  "hash": "c920aaebae731f9e16d9a8f1fc1e349b99313cf230f18126a0bbd07d64aac2e0"
};

const stringToHash = implodeAll('', Object.values(callBackResponse).filter((_, i, arr) => arr[i] !== callBackResponse.hash));

const consumerKey = 'CONSUMER KEY HERE'; // Replace with actual consumer key
const hashedString = crypto.createHmac('sha256', consumerKey).update(stringToHash).digest('hex');

console.log(hashedString);
```

Practices: always verify the hash before processing; keep the consumer key secret; respond with HTTP 200 OK to acknowledge receipt.

## Transaction Status Query

[ref: #utilities-transaction-query]

Sources: [Payment Transaction Status](https://developers.bobplus.africa/transaction-status/payment)

Checks the status of a payment transaction in real time — confirming whether a payment succeeded, failed, or is still pending.

Endpoint reference:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/payment/status-query` |
| Base URL | `https://here-prod-api-url.com` (as issued to your account) |
| Description | Check the status of a payment transaction |

Request body:

| Field | Type | Description | Required |
|---|---|---|---|
| `wallet_no` | string | Business wallet number assigned | Yes |
| `reference` | string | Reference passed during payment/payout | Yes |

Request headers:

| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | string | Bearer token used to access the API | Yes |
| `Signature` | string | SHA-256 signature: concatenate `wallet_no+reference`, sign with the private key, base64-encode | Yes |

Example request:

```bash
curl --location 'https://here-prod-api-url.com/api/v2/payment/status-query' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <token>' \
--header 'Signature: 23454321' \
--header 'Content-Type: application/json' \
--data '{
  "wallet_no": "234xxx2343",
  "reference": "052423213417"
}'
```

Success response — `data` carries the transaction details (`acc_name`, `acc_no`, `description`, `transaction_id`, `reference`, `status`, `status_description`, `date`):

```json
{
    "success": true,
    "message": "Successfully fetched",
    "data": {
        "acc_name": "John Doe",
        "acc_no": "2547xxxxxxxxxx",
        "description": "Deposit to wallet",
        "transaction_id": "052423213417",
        "reference": "K902101",
        "status": "SUCCESS",
        "status_description": "Unable to lock subscriber, a transaction is already in process for the current subscriber",
        "date": "2024-02-17 16:06:45 PM"
    }
}
```

A failed transaction returns the same shape with `status: "FAILED"` and an empty `transaction_id`:

```json
{
    "success": true,
    "message": "Successfully fetched",
    "data": {
        "acc_name": "John Doe",
        "acc_no": "2547xxxxxxxxxx",
        "description": "Deposit to wallet",
        "transaction_id": "",
        "reference": "K902001",
        "status": "FAILED",
        "status_description": "Unable to lock subscriber, a transaction is already in process for the current subscriber",
        "date": "2024-02-17 16:06:45 PM"
    }
}
```

Note that `status_description` is free-form and may not match the `status` semantics literally — branch on `status`, log the description.
