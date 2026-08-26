---
subject: "Bobplus C2B payins; mobile money deposit, `/api/v2/payment/`, per-country channel codes, `100000` M-PESA-KENYA, `900017` ZAR EFT, `900018` Capitec, `acc_ref`, `300041` Nigeria virtual account, `channel+reference+currency+amount` signature, `redirect_url`, `result_url` webhook, customer collections, checkout redirect, async confirmation, deposit initiation, wallet funding, payer notifications."
index:
  - anchor: payins-mobile-money
    what: "Generic mobile money deposit: POST `/api/v2/payment/` with wallet, customer, amount, currency, per-country `channel` code and `result_url`; the response returns `transaction_id` with an initial status; the `Signature` header signs `channel+reference+currency+amount`; full per-country channel code table included."
    problem: "Agent implements customer collections across African markets and must map each country to its correct channel code before initiating deposits; wrong code or misordered signature fields break initiation; momo acceptance, operator routing, phone payments, wallets, multi-country, momo, merchants, fintech, corridors, depositors."
    use_when: "Accepting customer mobile money in any supported country; looking up a country's channel code; composing the payin signature (`channel+reference+currency+amount`); handling the initiation response and the webhook wait."
    avoid_when: "South Africa EFT/Capitec specifics — the south-africa section; Nigeria virtual accounts — the nigeria sections; sending money out — payouts.md."
    expected: "Payin requests initiate with the right per-country channel and a valid signature, and the integration records `transaction_id` while awaiting the webhook final status."
  - anchor: payins-south-africa
    what: "ZAR payin flows: EFT via channel `900017` (phone in `acc_no`) and Capitec via channel `900018` (adds `acc_ref` = 13-digit SA ID); both return `redirect_url` for the customer to complete payment at their bank, and the final status arrives on `result_url`."
    problem: "Agent integrates South African collections and must choose between EFT and Capitec flows with correct extra fields before initiating; missing `acc_ref` on Capitec or wrong channel code rejects initiation outright; rand payments, bank redirect, identity number, payers, merchants, checkout."
    use_when: "Building ZAR collections; deciding EFT versus Capitec; obtaining the Capitec-required payer identifier; implementing the bank-redirect completion UX."
    avoid_when: "Other markets — the generic payin section and the country matrix; the standalone South Africa guide page — broken (HTTP 500) at scrape time, this section carries its content."
    expected: "ZAR initiation uses `900017` or `900018` with the right field set, and the customer is redirected to complete payment while the integration awaits `result_url`."
  - anchor: payins-nigeria-virtual-account
    what: "Nigeria collection via dynamic virtual account (channel `300041`, NGN): initiate, receive `virtual_account` details (`account_number`, `bank_name`, `expires`), display funding instructions, the customer transfers the exact amount, final status on `result_url`; `bank_code` optional (VA provider default `1067`)."
    problem: "Agent wires NGN collections and must handle bank-transfer completion instead of instant debit; hiding account details or ignoring expiry leaves payments unclaimed; naira deposits, funding account, customer action, reconciliation, timeout, async, webhooks."
    use_when: "Implementing NGN virtual-account collections; rendering funding instructions from the initiation response; deciding whether to pass `bank_code`; correlating the webhook with the initiated reference."
    avoid_when: "Other Nigerian channels (checkout links `300044`, wallets `300045`) — nigeria.md; generic multi-country momo — the mobile money section."
    expected: "Integration displays virtual account details before `expires`, matches the incoming bank transfer to the reference, and finalizes on the webhook status."
---

# Bobplus Payins (C2B)

Scraped from `https://developers.bobplus.africa` (pages `c2b/momo-payin`, `c2b/south-africa-payin`, `c2b/nigeria-payin`; docs version V2.1.2) on 2026-08-25.

## Mobile Money Deposit

[ref: #payins-mobile-money]

Sources: [Mobile Money Deposit](https://developers.bobplus.africa/c2b/momo-payin)

Accepts mobile money payments from customers across multiple countries into the business wallet. Quickstart: obtain a Bearer Token and generate the signature → POST the deposit endpoint → parse the response for transaction status.

Endpoint reference:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/payment/` |
| Base URL | `https://base-url-here.com` (as issued to your account) |
| Description | Initiate a mobile money deposit from a customer to your business wallet |

Request body:

| Field | Type | Description | Required |
|---|---|---|---|
| `wallet_no` | string | Business wallet account number assigned | Yes |
| `reference` | string | Order reference, unique per request | Yes |
| `acc_name` | string | Customer name | Yes |
| `email` | string | Customer email | Yes |
| `acc_no` | string | Customer mobile-money registered phone number; format `{countryCode}{phone}`, e.g. `2547XXXXXXXX` | Yes |
| `amount` | numeric | Order amount to be paid (no commas as thousands separator) | Yes |
| `currency` | string | Currency (`KES`, `TZS`, `XOF`, `MWK`, `RWF`, `UGX`, `ZMW`, `BWP`, `XAF`, `CDF`, `EGP`, `GMD`, `GHS`, `GNF`, `LSL`, `MRU`, `MZN`, `NGN`, `SLL`, `ZAR`) | Yes |
| `description` | string | Your order description | Yes |
| `channel` | numeric | Channel unique code, e.g. `100000` for M-PESA-KENYA (table below) | Yes |
| `result_url` | string | URL on your server for the callback response | Yes |
| `telco` | string | Mobile network operator (`orange`, `mtn`, `moov`, `wave`, `vodacom`, `airtel`). Conditional: required for Cameroon, Senegal, Ivory Coast, Mali, DRC, and Benin. | Conditional |

Channel codes:

| Channel code | Name | Currency |
|---|---|---|
| `100000` | MOBILE MONEY - KENYA | KES |
| `180003` | MOBILE MONEY - ZIMBABWE | ZWG |
| `210000` | MOBILE MONEY - BOTSWANA | BWP |
| `230000` | MOBILE MONEY - MALAWI | MWK |
| `250000` | MOBILE MONEY - BURKINA FASO | XOF |
| `260000` | MOBILE MONEY - ZAMBIA | ZMW |
| `280000` | MOBILE MONEY - CENTRAL AFRICAN REPUBLIC | XAF |
| `290000` | MOBILE MONEY - CHAD | XAF |
| `300001` | MOBILE MONEY - TANZANIA | TZS |
| `300011` | MOBILE MONEY - UGANDA | UGX |
| `300041` | VIRTUAL ACCOUNTS - NIGERIA | NGN |
| `300044` | CHECKOUT PAYMENT LINKS - NIGERIA | NGN |
| `300045` | OPAY & PALMPAY - NIGERIA | NGN |
| `310000` | MOBILE MONEY - CONGO BRAZZAVILLE | XAF |
| `330000` | MOBILE MONEY - EGYPT | EGP |
| `340000` | MOBILE MONEY - EQUATORIAL GUINEA | XAF |
| `350000` | MOBILE MONEY - GABON | XAF |
| `360000` | MOBILE MONEY - GAMBIA | GMD |
| `370000` | MOBILE MONEY - GHANA | GHS |
| `380000` | MOBILE MONEY - GUINEA | GNF |
| `390000` | MOBILE MONEY - GUINEA BISSAU | XOF |
| `420000` | MOBILE MONEY - LESOTHO | LSL |
| `440000` | MOBILE MONEY - MAURITANIA | MRU |
| `450000` | MOBILE MONEY - MOZAMBIQUE | MZN |
| `460000` | MOBILE MONEY - NIGER | XOF |
| `490000` | MOBILE MONEY - SIERRA LEONE | SLL |
| `500000` | MOBILE MONEY - SOUTH AFRICA | ZAR |
| `510000` | MOBILE MONEY - TOGO | XOF |
| `800003` | MOBILE MONEY - IVORY COAST \* | XOF |
| `800005` | MOBILE MONEY - SENEGAL \* | XOF |
| `800007` | MOBILE MONEY - MALI \* | XOF |
| `800009` | MOBILE MONEY - CAMEROON \* | XAF |
| `800011` | MOBILE MONEY - DRC \* | CDF |
| `800017` | MOBILE MONEY - BENIN \* | XOF |
| `910001` | MOBILE MONEY - RWANDA | RWF |
| `910003` | MOBILE MONEY - BURUNDI | BIF |

Request headers:

| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | string | Bearer token used to access the API | Yes |
| `Signature` | string | SHA-256 signature: concatenate `channel+reference+currency+amount`, sign with the private key, base64-encode | Yes |

Curator's note — source ambiguity: the request-headers table does not list `x-hash`, but the curl example includes `# --header 'x-hash: xxxxxx' # Generated X-Hash header` as a comment. Payout endpoints explicitly require `x-hash`; for payins the requirement is unclear.

Example request:

```bash
curl --location --request POST 'https://base-url-here.com/api/v2/payment/' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--header 'Signature: xxx' \
# --header 'x-hash: xxxxxx' # Generated X-Hash header \
--data-raw '{'
    "wallet_no": "xxxxxxx",
    "reference": "TRXXXX79",
    "acc_name": "JOHN DOE",
    "acc_no": "2547XXXXXXXX",
    "currency": "KES",
    "amount": 10,
    "channel": 100000,
    "email": "johndoe@gmail.com",
    "description": "Deposit to order",
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
- Burundi (`910003`): after initiation the customer receives an SMS approval request and must dial `*163#` and choose option 2 to approve the transaction.
- Security best practices from the docs: always use HTTPS for all API requests; keep your private key secure and never share it; verify the signature on the server side for every request.

## South Africa (EFT and Capitec)

[ref: #payins-south-africa]

Sources: [South Africa Payin — EFT / Capitec](https://developers.bobplus.africa/c2b/south-africa-payin)

ZAR payins use merchant channel codes with a bank-redirect completion: **EFT** via channel `900017` (redirect to bank) and **Capitec** via channel `900018` (redirect; requires `acc_ref`: 13-digit SA ID). The standalone South Africa integration guide page returned HTTP 500 at scrape time; this section carries the flow.

Endpoint: POST `/api/v2/payment/`, currency `ZAR`, channel `900017` (EFT) or `900018` (Capitec).

Integration flow: POST with the chosen channel → for Capitec include `acc_ref` (13-digit SA ID) → receive `redirect_url` in the response → redirect the customer to complete payment at their bank → receive the final status on the `result_url` webhook.

Capitec versus EFT:

| Flow | How to trigger | Extra fields |
|---|---|---|
| ZAR EFT | Channel `900017` | Phone in `acc_no`; omit `acc_ref` |
| ZAR Capitec | Channel `900018` + `acc_ref` | 13-digit SA ID + Capitec phone in `acc_no` |

EFT example request:

```json
{
    "wallet_no": "xxxxxxx",
    "reference": "SA-EFT-001",
    "acc_name": "John Doe",
    "acc_no": "27113785456",
    "email": "john@example.com",
    "currency": "ZAR",
    "amount": 100,
    "channel": 900017,
    "description": "Order payment",
    "result_url": "https://your-server.com/webhook"
}
```

Capitec example request:

```json
{
    "wallet_no": "xxxxxxx",
    "reference": "SA-CAP-001",
    "acc_name": "John Doe",
    "acc_no": "08166750025",
    "acc_ref": "9401090445083",
    "email": "john@example.com",
    "currency": "ZAR",
    "amount": 100,
    "channel": 900018,
    "description": "Capitec payment",
    "result_url": "https://your-server.com/webhook"
}
```

Example response (returns `redirect_url`):

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "transaction_id": "056341150381",
        "status": "PENDING",
        "status_description": "Transaction Initiated successfully",
        "amount": 100,
        "currency": "ZAR",
        "redirect_url": "https://bank-redirect.example.com/...",
        "date": "2026-07-08 12:00:00 PM"
    }
}
```

## Nigeria Virtual Account

[ref: #payins-nigeria-virtual-account]

Sources: [Nigeria Collections — Virtual Account](https://developers.bobplus.africa/c2b/nigeria-payin), [Nigeria (NGN) Integration Guide](https://developers.bobplus.africa/nigeria)

Nigeria payins use a **dynamic virtual bank account**: after initiation the customer transfers the exact amount to the account details returned in the API response. Channel `300041`, currency `NGN`. The full Nigeria guide (other channels, payout, statuses) lives in `nigeria.md`.

Integration flow: POST with channel `300041` → receive `virtual_account` in the response (`account_number`, `bank_name`, `amount`) → display funding instructions to the customer → the customer completes a bank transfer to the virtual account → final status arrives on the `result_url` webhook.

Curator's note — source inconsistency: the integration flow lists `amount` inside `virtual_account`, but the example response carries `amount` at the `data` level (outside `virtual_account`); `virtual_account` itself contains `account_number`, `account_name`, `bank_name`, `expires`.

Request fields specific to this flow:

| Field | Required | Notes |
|---|---|---|
| `acc_name` | Yes | Customer full name |
| `acc_no` | Yes | Customer phone (e.g. `08012345678`) |
| `email` | Yes | Customer email |
| `amount` | Yes | Exact amount the customer must transfer |
| `bank_code` | No | VA provider bank (default `1067`) |

Example request:

```json
{
    "wallet_no": "XXXXXXX",
    "reference": "CORNGN0089123036",
    "acc_name": "test",
    "acc_no": "08012345678",
    "email": "customer@example.com",
    "currency": "NGN",
    "amount": 5000,
    "channel": 300041,
    "description": "Order payment",
    "result_url": "https://your-server.com/webhook"
}
```

Example response:

```json
{
    "success": true,
    "message": "Successfully initiated",
    "data": {
        "acc_name": "Test Customer",
        "acc_no": "1234876588",
        "description": "Order payment",
        "transaction_id": "126072834240",
        "reference": "CORNGN0089123036",
        "status": "PROCESSING",
        "amount": 5000,
        "charges": 0,
        "currency": "NGN",
        "status_description": "Account generated successfully",
        "date": "2026-07-28 13:23:15 PM",
        "fetched_at": "2026-07-28 13:23:21 PM",
        "virtual_account": {
            "account_number": "123456789",
            "account_name": "account-name",
            "bank_name": "bank-name",
            "expires": "2026-07-28 12:23:21 PM"
        }
    }
}
```
