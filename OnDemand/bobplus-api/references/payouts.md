---
subject: "Bobplus B2C payouts; bank payout, mobile money payout, `/api/v2/payment/`, `bank_code`, recipient account, `100002` BANK-KENYA, `100003` M-PESA-KENYA, `900019` ZAR RTC, `900020` NGN VA, `900021` NGN NUBAN, `300043` Nigeria bank transfer, `x-hash` header, bulk disbursement, payroll, vendor payments, recipient wallets, cashout rails."
index:
  - anchor: payouts-bank
    what: "Bank payout to an account number: POST `/api/v2/payment/` with recipient `acc_no`/`bank_code`, per-country bank channel codes (`100002` Kenya, `300003` Tanzania, `300013` Uganda, `900019` ZAR RTC, `900020`/`900021` NGN), `Signature` over `channel+reference+currency+amount`, and mandatory `x-hash`."
    problem: "Agent disburses funds to bank accounts for payroll or vendors and must resolve bank code plus channel per market; wrong pairing routes money incorrectly or rejects; salary runs, supplier settlement, account transfer, routing, bulk payments, treasury."
    use_when: "Paying out to bank accounts (employees, vendors); selecting the right channel per destination country; fetching recipient `bank_code`; composing the payout signature and `x-hash`."
    avoid_when: "Paying to mobile money wallets — the momo payout section; collecting money — payins.md; NGN payout deep-dive — nigeria.md."
    expected: "Bank payouts initiate with the correct channel/bank-code pair and the full header trio, and the integration tracks `transaction_id` to the webhook final status."
  - anchor: payouts-mobile-money
    what: "Mobile money payout to a wallet: POST `/api/v2/payment/` with the recipient's registered phone as `acc_no`, per-country momo channel codes (table of 30+ markets, e.g. `100003` M-PESA-KENYA), `Signature` over `channel+reference+currency+amount`, and mandatory `x-hash`."
    problem: "Agent pays out to customer wallets across markets and must pick correct momo channel per country; payin/payout channel confusion (different code sets) misroutes disbursements; cashout, salary to phone, operators, last-mile delivery, recipients, disbursers."
    use_when: "Disbursing to mobile money wallets in any supported market; looking up the momo payout channel code for a country; formatting recipient phone numbers with country code; bulk or individual payouts."
    avoid_when: "Bank account recipients — the bank payout section; collections — payins.md; channel codes for payins — they differ from payout codes."
    expected: "Momo payouts initiate with the correct per-country payout channel, recipient phone in international format, and the full header trio, and complete on the webhook status."
---

# Bobplus Payouts (B2C)

Scraped from `https://developers.bobplus.africa` (pages `b2c/bank-payout`, `b2c/momo-payout`; docs version V2.1.2) on 2026-08-25.

## Bank Payout

[ref: #payouts-bank]

Sources: [Bank Payout — To Account Number](https://developers.bobplus.africa/b2c/bank-payout)

Sends money or processes payouts directly to employees' or vendors' bank accounts — payroll, vendor payments, bulk and individual transactions. Quickstart: obtain a Bearer Token, generate the signature and X-Hash → POST the payout endpoint → parse the response.

Endpoint reference:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/payment/` |
| Base URL | `https://base-url-here.com` (as issued to your account) |
| Description | Initiate a bank payout to a recipient's account number |

Request body:

| Field | Type | Description | Required |
|---|---|---|---|
| `wallet_no` | string | Business wallet account number assigned | Yes |
| `reference` | string | Order reference, unique per request | Yes |
| `acc_name` | string | Recipient name | Yes |
| `email` | string | Recipient email | Yes |
| `acc_no` | string | Recipient bank account number | Yes |
| `bank_code` | string | Recipient bank code (full list in `utilities.md`) | Yes |
| `amount` | numeric | Order amount to be paid (no commas as thousands separator) | Yes |
| `currency` | string | Currency (`KES`, `TZS`, `XOF`, `MWK`, `RWF`, `UGX`, `ZMW`, `BWP`, `XAF`, `CDF`, `EGP`, `GMD`, `GHS`, `GNF`, `LSL`, `MRU`, `MZN`, `NGN`, `SLL`, `ZAR`) | Yes |
| `description` | string | Your order description | Yes |
| `channel` | numeric | Channel unique code, e.g. `100002` for BANK-KENYA (table below) | Yes |
| `result_url` | string | URL on your server for the callback response | Yes |

Channel codes:

| Channel code | Name | Currency |
|---|---|---|
| `100002` | BANK CHANNEL - KENYA | KES |
| `300003` | BANK CHANNEL - TANZANIA | TZS |
| `300013` | BANK CHANNEL - UGANDA | UGX |
| `900019` | BANK CHANNEL - SOUTH AFRICA (ZAR RTC) | ZAR |
| `900020` | BANK CHANNEL - NIGERIA (NGN VA) | NGN |
| `900021` | BANK CHANNEL - NIGERIA (NGN NUBAN) | NGN |

Curator's note — source inconsistency: the request-body `currency` example above lists only `KES`, `TZS`, `UGX`, `ZAR`, but the channel table includes the NGN channels `900020`/`900021` — treat the currency list as illustrative ("e.g."), NGN payouts are supported.

Per the docs: use `900019` for ZAR RTC payouts and `900021` for NGN NUBAN payouts. Note that `nigeria.md` and the momo payout table also document `300043` (BANK TRANSFER - NIGERIA) for NGN payouts — the source docs carry both; confirm the operative code with Bobplus when in doubt.

Request headers:

| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | string | Bearer token used to access the API | Yes |
| `Signature` | string | SHA-256 signature: concatenate `channel+reference+currency+amount`, sign with the private key, base64-encode | Yes |
| `x-hash` | string | Generated X-Hash header for additional security | Yes |

Example request:

```bash
curl --location --request POST 'https://base-url-here.com/api/v2/payment/' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--header 'Signature: xxx' \
--header 'x-hash: xxxxxx' \
--data-raw '{
    "wallet_no": "xxxxxxx",
    "reference": "TRXXXX79",
    "acc_name": "JOHN DOE",
    "acc_no": "0283938XXXXXX989",
    "currency": "KES",
    "amount": 10,
    "channel": 100002,
    "bank_code": 1323,
    "email": "johndoe@gmail.com",
    "description": "Pay for order #23243222",
    "result_url": "https://webhook.site/947e8f48-c03a-4717-a2dd-8cdb2f64e897"
}'
```

Success response fields: `success`, `message`, `data.transaction_id`, `data.status`, `data.status_description`, `data.date`:

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "transaction_id": "056341150381",
        "status": "PENDING",
        "status_description": "Transaction Initiated successfully",
        "date": "2024-02-17 13:34:02 PM"
    }
}
```

## Mobile Money Payout

[ref: #payouts-mobile-money]

Sources: [MoMo Payout (Business to Client)](https://developers.bobplus.africa/b2c/momo-payout)

Disburses funds to recipients' mobile money wallets — salary disbursements, vendor payments, and other financial transactions. Quickstart: obtain a Bearer Token, generate the signature and X-Hash → POST the payout endpoint → parse the response.

Endpoint reference:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/payment/` |
| Base URL | `https://base-url-here.com` (as issued to your account) |
| Description | Initiate a mobile money payout to a recipient's wallet |

Request body:

| Field | Type | Description | Required |
|---|---|---|---|
| `wallet_no` | string | Business wallet account number assigned | Yes |
| `reference` | string | Order reference, unique per request | Yes |
| `acc_name` | string | Recipient name | Yes |
| `email` | string | Recipient email | Yes |
| `acc_no` | string | Recipient mobile-money registered phone number; format `{countryCode=254}{phone=7XXXXXXXX}` (e.g. `2547XXXXXXXX`) | Yes |
| `amount` | numeric | Order amount to be paid (no commas as thousands separator) | Yes |
| `currency` | string | Currency (`KES`, `TZS`, `XOF`, `MWK`, `RWF`, `UGX`, `ZMW`, `BWP`, `XAF`, `CDF`, `EGP`, `GMD`, `GHS`, `GNF`, `LSL`, `MRU`, `MZN`, `NGN`, `SLL`, `ZAR`) | Yes |
| `description` | string | Your order description | Yes |
| `channel` | numeric | Channel unique code, e.g. `100003` for M-PESA-KENYA (table below) | Yes |
| `result_url` | string | URL on your server for the callback response | Yes |
| `telco` | string | Mobile network operator (`orange`, `mtn`, `moov`, `wave`, `vodacom`, `airtel`). Conditional: required for Cameroon, Senegal, Ivory Coast, Mali, DRC, and Benin. | Conditional |

Channel codes (payout codes — they differ from the payin set):

| Channel code | Name | Currency |
|---|---|---|
| `100003` | MOBILE MONEY - KENYA | KES |
| `110013` | MOBILE MONEY - BOTSWANA | BWP |
| `120003` | MOBILE MONEY - MALAWI | MWK |
| `120013` | MOBILE MONEY - BURKINA FASO | XOF |
| `140003` | MOBILE MONEY - CENTRAL AFRICAN REPUBLIC | XAF |
| `150003` | MOBILE MONEY - ZAMBIA | ZMW |
| `160003` | MOBILE MONEY - CHAD | XAF |
| `170003` | MOBILE MONEY - CONGO BRAZZAVILLE | XAF |
| `180004` | MOBILE MONEY - ZIMBABWE | ZWG |
| `190003` | MOBILE MONEY - EGYPT | EGP |
| `200003` | MOBILE MONEY - EQUATORIAL GUINEA | XAF |
| `210003` | MOBILE MONEY - GABON | XAF |
| `220003` | MOBILE MONEY - GAMBIA | GMD |
| `230003` | MOBILE MONEY - GHANA | GHS |
| `240003` | MOBILE MONEY - GUINEA | GNF |
| `250003` | MOBILE MONEY - GUINEA BISSAU | XOF |
| `270003` | MOBILE MONEY - LESOTHO | LSL |
| `290003` | MOBILE MONEY - MAURITANIA | MRU |
| `300002` | MOBILE MONEY - TANZANIA | TZS |
| `300012` | MOBILE MONEY - UGANDA | UGX |
| `300043` | BANK TRANSFER - NIGERIA | NGN |
| `310003` | MOBILE MONEY - MOZAMBIQUE | MZN |
| `320003` | MOBILE MONEY - NIGER | XOF |
| `350003` | MOBILE MONEY - SIERRA LEONE | SLL |
| `360003` | MOBILE MONEY - SOUTH AFRICA | ZAR |
| `370003` | MOBILE MONEY - TOGO | XOF |
| `800004` | MOBILE MONEY - IVORY COAST \* | XOF |
| `800006` | MOBILE MONEY - SENEGAL \* | XOF |
| `800008` | MOBILE MONEY - MALI \* | XOF |
| `800010` | MOBILE MONEY - CAMEROON \* | XAF |
| `800012` | MOBILE MONEY - DRC \* | CDF |
| `800018` | MOBILE MONEY - BENIN \* | XOF |
| `910002` | MOBILE MONEY - RWANDA | RWF |
| `910004` | MOBILE MONEY - BURUNDI | BIF |

Request headers:

| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | string | Bearer token used to access the API | Yes |
| `Signature` | string | SHA-256 signature: concatenate `channel+reference+currency+amount`, sign with the private key, base64-encode | Yes |
| `x-hash` | string | Generated X-Hash header for additional security | Yes |

Example request:

```bash
curl --location --request POST 'https://base-url-here.com/api/v2/payment/' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--header 'Signature: xxx' \
--header 'x-hash: xxxxxx' \
--data-raw '{
    "wallet_no": "xxxxxxx",
    "reference": "TRXXXX79",
    "acc_name": "JOHN DOE",
    "acc_no": "2547XXXXXXXX",
    "currency": "KES",
    "amount": 10,
    "channel": 100003,
    "email": "johndoe@gmail.com",
    "description": "Pay for order #23243222",
    "result_url": "https://webhook.site/947e8f48-c03a-4717-a2dd-8cdb2f64e897"
}'
```

Success response fields: `success`, `message`, `data.transaction_id`, `data.status`, `data.status_description`, `data.date`:

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "transaction_id": "056341150381",
        "status": "PENDING",
        "status_description": "Transaction Initiated successfully",
        "date": "2024-02-17 13:34:02 PM"
    }
}
```

Notes:

- Countries marked `\*` (Cameroon, Senegal, Ivory Coast, Mali, DRC, Benin) require the `telco` field. Accepted values: `orange`, `mtn`, `moov`, `wave`, `vodacom`, `airtel` (per-country availability depends on the market).
- Both payout endpoints: use HTTPS, keep the private key secret, and verify the signature and X-Hash server-side on every request.
