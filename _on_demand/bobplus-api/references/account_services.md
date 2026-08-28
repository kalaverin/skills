---
subject: "Bobplus Account Services API; wallet balance lookup, `/api/v2/wallet/{wallet_no}/{currency}`, full statement, `/api/v2/wallet/statement`, `from_date`, `to_date`, `limit`, transaction history, debit, credit, reconciliation, reporting, auditing, merchant wallet, available funds, date range, signature concatenation, funds verification."
index:
  - anchor: account-services-balance
    what: "Balance lookup: GET `/api/v2/wallet/{wallet_no}/{currency}` returns the wallet's available balance with account number, name, currency, and `last_update`; the `Signature` header signs the concatenation `wallet_no+currency`."
    problem: "Agent needs current money position of wallet before disbursement or reporting; malformed URL shape or incorrectly signed concatenation yields rejected calls; available funds, wallet state, pre-payout check, real-time balance, treasury monitoring, liquidity, polling."
    use_when: "Reading the available balance of a wallet in a given currency; pre-flight funds check before payouts; building the balance signature (`wallet_no+currency`); reconciliation dashboards."
    avoid_when: "Transaction-level history — the statement section; moving money — the payins and payouts files."
    expected: "Balance calls return `data.account.balance` with currency and timestamp, signed over `wallet_no+currency`, and feed funds checks before money movement."
  - anchor: account-services-statement
    what: "Full statement retrieval: POST `/api/v2/wallet/statement` with `wallet_no`, `from_date`/`to_date` (`YYYY-MM-DD`), and `limit` (max 5000) returns the transaction list (`txnId`, `type` Debit/Credit, `amount`, running `balance`, `description`, `confirmed`, `date`); the `Signature` header signs `wallet_no+to_date+limit`."
    problem: "Agent builds reconciliation or audit export and needs complete transaction history over date range; wrong date format, oversized `limit`, or mismatched signature concatenation breaks retrieval; trail, ledger, bookkeeping, period filter, pagination cap, statements."
    use_when: "Pulling transaction history for a wallet over a period; reconciliation, reporting, or auditing jobs; respecting the 5000-row `limit`; building the statement signature (`wallet_no+to_date+limit`)."
    avoid_when: "Current balance only — the balance section is cheaper; single-transaction status — the transaction query in utilities.md."
    expected: "Statement jobs page through date ranges within the `limit`, parse the typed transaction list, and reconcile against the running `balance`."
---

# Bobplus Account Services API

Scraped from `https://developers.bobplus.africa` (pages `account-services/get-balance`, `account-services/full-statement`; docs version V2.1.2) on 2026-08-25.

## Fetch Balance

[ref: #account-services-balance]

Sources: [Fetch Balance](https://developers.bobplus.africa/account-services/get-balance)

Retrieves the current available balance of a given account in a specified currency — for reconciliation, reporting, or business logic. Quickstart: obtain a Bearer Token and generate the signature → GET the balance endpoint → parse the response.

Endpoint reference:

| | |
|---|---|
| HTTP Method | GET |
| Endpoint URL | `/api/v2/wallet/{wallet_no}/{currency}` |
| Base URL | `https://prod-url-here` (as issued to your account) |
| Description | Fetch the current balance for a specific wallet and currency |

URL parameters:

| Parameter | Description | Required | Example |
|---|---|---|---|
| `wallet_no` | The account ID | Yes | `00201XXXX14605` |
| `currency` | The currency code (`KES` for Kenya, etc.) | Yes | `KES` |

Request headers:

| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | string | Bearer token for API authentication | Yes |
| `Signature` | string | SHA-256 signature: concatenate `wallet_no+currency`, sign with the private key, base64-encode | Yes |

Example request:

```bash
curl --location 'https://prod-url-here/api/v2/wallet/08xxxxx17/KES' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--header 'Signature: XXCCCXXXXXXXXX'
```

Success response fields: `success`, `message`, `data.account.number`, `data.account.name`, `data.account.currency`, `data.account.balance` (float):

```json
{
    "success": true,
    "message": "Successfully fetched",
    "data": {
        "uuid": "f93be5e9-0b9c-4968-8cf6-2fe4f274e594",
        "account": {
            "number": "33815317",
            "name": "",
            "currency": "USD",
            "balance": 1000000.00
        },
        "last_update": "2025-02-10 18:11:57"
    }
}
```

## Full Statement

[ref: #account-services-statement]

Sources: [Account Full Statement](https://developers.bobplus.africa/account-services/full-statement)

Retrieves the full transaction history for a specific account within a defined date range — for reconciliation, reporting, or auditing. Quickstart: obtain a Bearer Token and generate the signature → POST the statement endpoint → parse the transaction history.

Endpoint reference:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/wallet/statement` |
| Base URL | `https://base-url-here` (as issued to your account) |
| Description | Fetch the full transaction statement for a wallet within a date range |

Request body:

| Field | Type | Description | Required |
|---|---|---|---|
| `wallet_no` | string | Wallet account number | Yes |
| `from_date` | date | Start date of the statement period, `YYYY-MM-DD` | Yes |
| `to_date` | date | End date of the statement period, `YYYY-MM-DD` | Yes |
| `limit` | numeric | Maximum number of transactions returned (max: 5000) | Yes |

Request headers:

| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | string | Bearer token for API authentication | Yes |
| `Signature` | string | SHA-256 signature: concatenate `wallet_no+to_date+limit`, sign with the private key, base64-encode | Yes |

Example request:

```bash
curl --location 'https://base-url-here/api/v2/wallet/statement' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <token>' \
--header 'Signature: XXCCCXXXXXXXXX' \
--data '{
    "wallet_no":"7XXXXXXXXX48",
    "from_date":"2024-01-01",
    "to_date":"2024-03-01",
    "limit":10
}'
```

Success response fields: `success`, `message`, `data` (array of transactions with `txnId`, `type` = Debit or Credit, `amount`, `balance` after the transaction, `description`, `confirmed`, `date`):

```json
{
    "success": true,
    "message": "Successfully fetched",
    "data": [
        {
            "txnId": "375829475809",
            "type": "Credit",
            "amount": "10",
            "balance": 20,
            "description": "Credited KES10.00 as new payment received.",
            "confirmed": true,
            "date": "2024-02-12 19:36:29 PM"
        },
        {
            "txnId": "067198135548",
            "type": "Credit",
            "amount": "10",
            "balance": 10,
            "description": "Credited KES10.00 as new payment received.",
            "confirmed": true,
            "date": "2024-02-12 19:32:32 PM"
        }
    ]
}
```

Curator's note — source inconsistency: the response-fields table on the docs page types `data.amount` as numeric, but the JSON example carries it as a string (`"10"`). Parse `amount` tolerantly (accept both).

Both endpoints: use HTTPS, keep the private key secret, and verify signatures server-side on every request.
