---
subject: "Documented contradictions, inconsistencies, and ambiguous facts found across Bobplus Payments API documentation; each entry cites exact source URLs where conflicting statements appear; entries preserve original wording instead of resolving conflicts arbitrarily."
index:
  - anchor: contradictions-nigeria-payout-channel
    what: "Nigeria NGN bank-transfer endpoint lists channel 300043 inside integration guide, while separate bank-payout page lists 900020 and 900021 for same flow."
    problem: "Integrator cannot determine correct channel identifier for Nigeria NGN bank disbursement because documentation presents two unrelated code sets without reconciliation; routing confusion causes failed payout execution and unreliable channel selection; payout channel mismatch, NGN disbursement ambiguity."
    use_when: "Writing Nigeria payout documentation; comparing bank-payout page against integration guide; encountering 300043 or 900020/900021 in implementation."
    avoid_when: "Unrelated country corridors; mobile-money payouts where Nigeria is not involved."
    expected: "Reader understands both code sets are documented, conflict is preserved as-is, and chooses based on live endpoint behavior or Bobplus clarification."
  - anchor: contradictions-south-africa-payin-channel
    what: "South Africa ZAR payin rails use 500000 on mobile-money page and 900017/900018 on EFT/Capitec page without cross-reference."
    problem: "Two distinct ZAR deposit channel families exist in different documents with no explanation of relationship; integrator may select wrong rail for desired customer experience or payment flow; ZAR deposit rail confusion, payin routing conflict."
    use_when: "Documenting South Africa payins; choosing between EFT/Capitec and mobile-money flows; updating South Africa payin section."
    avoid_when: "Other countries or South Africa payout documentation."
    expected: "Reader sees both channel families, understands they likely target different user experiences, and validates with Bobplus if unclear."
  - anchor: contradictions-rate-limit-unit
    what: "Rate limit numeric value 1500 appears as requests per minute on home page and requests per second on bank-codes page."
    problem: "Order-of-magnitude difference in throttling policy breaks client backoff logic when wrong unit is assumed; documented throughput limits diverge by factor of sixty between home page and bank-codes page; throttling unit collision, rate policy mismatch."
    use_when: "Writing rate-limit guidance; comparing global versus endpoint-specific limits; configuring retry/backoff logic."
    avoid_when: "Sections that do not mention rate limits."
    expected: "Reader knows both values appear verbatim and must confirm effective limit with Bobplus or empirical testing."
  - anchor: contradictions-nigeria-va-bank-code
    what: "Nigeria virtual-account page treats bank_code as optional with default 1067, while Nigeria guide treats same field as conditional only for Opay/PalmPay and bank payouts."
    problem: "Virtual-account request shape is unclear because default 1067 does not match conditional model that limits bank_code to Opay/PalmPay and bank-transfer rails; optional field semantics collide with required-when guidance; VA bank code drift, Nigeria optional field conflict."
    use_when: "Documenting Nigeria virtual-account requests; validating bank_code field semantics; reconciling virtual-account page with Nigeria guide."
    avoid_when: "Non-VA Nigeria flows; payout documentation."
    expected: "Reader flags discrepancy and tests whether bank_code is accepted or required on virtual-account endpoint."
  - anchor: contradictions-callback-failed-hash-order
    what: "Failed callback prose lists transaction_id before result_code for HMAC, while sample JSON orders result_code before transaction_id."
    problem: "Hash verification will fail when implementor follows wrong field order because prose recipe and JSON sample disagree on sequence; webhook consumers cannot deterministically reproduce signature; callback hash order inversion, verification sequence mismatch."
    use_when: "Writing webhook verification code; documenting callback HMAC recipe; updating webhook section."
    avoid_when: "Non-webhook topics; success callback where order matches sample."
    expected: "Reader knows textual order and JSON sample disagree and must confirm canonical order with Bobplus."
  - anchor: contradictions-va-expiry-timestamp
    what: "Nigeria VA examples show expires timestamp one hour earlier than date and fetched_at, making expiry impossible."
    problem: "Example values are logically inconsistent because expiry precedes account generation timestamps; integrator cannot derive valid TTL, timezone semantics, or acceptable clock skew from published documentation; virtual account TTL ambiguity, documentation error."
    use_when: "Documenting VA expiry behavior; writing TTL logic; updating VA Nigeria samples."
    avoid_when: "Non-VA flows."
    expected: "Reader treats example as erroneous and asks Bobplus for real expiry window."
  - anchor: contradictions-statement-signature-omits-from-date
    what: "Full-statement request body requires from_date, but signature concatenation uses only wallet_no, to_date, and limit."
    problem: "Required body field remains unprotected by signature because signing string omits from_date while to_date and limit are included; omission creates potential tampering vector or documentation gap; statement signature incompleteness, request signing gap."
    use_when: "Writing full-statement signing recipe; reviewing security-critical signing strings."
    avoid_when: "Other endpoints where signature string is fully specified."
    expected: "Reader flags omission and verifies with Bobplus whether from_date should be included."
  - anchor: contradictions-x-hash-payload
    what: "X-Hash header is required for payouts, but exact signed payload is only described as businessId or agreed payload."
    problem: "Integrator cannot deterministically generate X-Hash for payout endpoints because documentation never defines exact bytes to sign beyond generic businessId reference; incomplete recipe blocks secure header construction; payout signature payload ambiguity, X-Hash recipe gap."
    use_when: "Writing X-Hash generation code; documenting payout headers; reconciling generate-x-hash page with payout pages."
    avoid_when: "Endpoints where X-Hash is not required."
    expected: "Reader knows docs do not define payout X-Hash payload and must obtain recipe from Bobplus."
  - anchor: contradictions-telco-values
    what: "Request-body table lists telco examples as orange, mtn, moov, wave, while footnote expands list to add vodacom and airtel."
    problem: "Implementor may reject valid operator names when following table alone because footnote contains additional values not shown in request-body examples; accepted value set remains under-documented; mobile operator enum incompleteness, telco value mismatch."
    use_when: "Documenting telco field for Cameroon, Senegal, Ivory Coast, Mali, DRC, Benin; validating carrier list."
    avoid_when: "Countries where telco is not required."
    expected: "Reader uses fuller footnote list and confirms per-country mapping with Bobplus if needed."
  - anchor: contradictions-base-url-placeholders
    what: "No real production host is documented; hostnames used in examples vary across pages."
    problem: "Placeholder hostnames differ across documentation pages, so client configuration lacks authoritative source for production endpoint; every shown base URL is non-functional and cannot be used directly without replacement; base URL ambiguity, placeholder host drift."
    use_when: "Writing getting-started or configuration sections; comparing endpoint hostnames across pages."
    avoid_when: "Sections that already take hostname from configuration."
    expected: "Reader knows all documented hosts are placeholders and must obtain real host from Bobplus."
  - anchor: contradictions-timestamp-formats
    what: "Response timestamp formats vary across endpoints: some omit AM/PM, others append PM to 24-hour values."
    problem: "Client parsing logic cannot assume one canonical timestamp layout because examples mix HH:MM:SS, HH:MM:SS PM, and 24-hour values with invalid PM suffix; no documented format rule exists for response timestamps across endpoints; timestamp parsing ambiguity, invalid clock notation."
    use_when: "Writing response parsing guidance; documenting example responses; updating references with sample JSON."
    avoid_when: "Request field documentation where timestamps are not returned."
    expected: "Reader knows no canonical timestamp format is stated and should ask Bobplus for real format."
  - anchor: contradictions-signature-header-casing
    what: "Curl examples use Signature header in title case, while signature generation PHP example uses lower-case signature."
    problem: "Cosmetic inconsistency may confuse implementors even though HTTP headers are case-insensitive; documentation shows two different casings for same header name across example code samples; header casing drift, signature example inconsistency."
    use_when: "Normalizing header examples across corpus; writing code samples."
    avoid_when: "Functional discussions where casing does not matter."
    expected: "Reader normalizes to single casing convention in skill corpus."
  - anchor: contradictions-amount-type
    what: "Full-statement response table declares amount as numeric, but example shows quoted string 10."
    problem: "Schema and example disagree for full-statement amount field; client type mapping breaks when generated types expect numeric but API returns quoted value; response field type inconsistency, statement amount type mismatch."
    use_when: "Documenting amount field for statements; generating SDK types; validating examples against schemas."
    avoid_when: "Other statement fields where schema and example align."
    expected: "Reader flags mismatch and confirms real returned type."
  - anchor: contradictions-payin-x-hash-table-vs-example
    what: "Mobile-money payin request-headers table omits x-hash while same page curl example sends x-hash as active header since 2026-09-09 re-scrape."
    problem: "Integrator cannot determine whether payin endpoint requires x-hash because normative table and worked example disagree; silent rejection risk when header omitted, wasted signing effort when included; payin header ambiguity, x-hash requirement conflict, table versus example drift."
    use_when: "Writing payin request code; deciding header set for mobile-money deposits; reconciling payins.md curator note."
    avoid_when: "Payout endpoints where x-hash is explicitly required; endpoints without x-hash mentions."
    expected: "Reader knows example includes x-hash while table omits it, treats requirement as unconfirmed, and raises with Bobplus."
  - anchor: contradictions-nigeria-va-response-acc-no
    what: "Nigeria VA response shows acc_no shaped like generated account number rather than customer phone sent in request across c2b/nigeria-payin and nigeria pages."
    problem: "Integrator cannot map response acc_no to request acc_no because examples imply different meanings for same field name; reconciliation between sent customer phone and returned virtual account number breaks; acc_no semantic drift, response field shape conflict, VA identifier ambiguity."
    use_when: "Parsing VA payin responses; reconciling payin requests with responses; writing field-mapping tables."
    avoid_when: "Non-Nigeria flows; endpoints without VA responses."
    expected: "Reader treats response acc_no as VA number candidate, not customer phone, and confirms semantics with Bobplus."
  - anchor: contradictions-signature-example-field-order
    what: "Generate-signature Step-3 shows payin payload with wallet_no, reference, acc_name fields, but prose then instructs concatenating unrelated account and customer_code names."
    problem: "Integrator cannot derive correct signing string because prose references fields absent from example payload; signature recipe ambiguous between documented field order and phantom names; signature field mismatch, phantom concatenation example, signing recipe confusion."
    use_when: "Writing signature generation code; reconciling generate-signature page with endpoint recipes; updating security.md."
    avoid_when: "Endpoints with fully specified signing strings."
    expected: "Reader uses per-endpoint signature map in SKILL.md and treats account+customer_code prose as documentation error."
  - anchor: contradictions-status-query-reference-semantics
    what: "Status-query example response sets transaction_id equal to request reference while response reference carries different value."
    problem: "Client cannot determine which response field echoes original request reference because worked example contradicts documented field descriptions; correlation logic may bind to wrong identifier; reference echo ambiguity, transaction_id semantics drift, status-query correlation conflict."
    use_when: "Writing status reconciliation jobs; mapping status-query responses to original requests; updating utilities.md."
    avoid_when: "Endpoints without status polling."
    expected: "Reader correlates on both fields defensively and asks Bobplus which field echoes the request reference."
  - anchor: contradictions-bank-payout-currency-examples
    what: "Bank-payout currency field examples list KES, TZS, UGX, ZAR but omit NGN while same page channel table includes Nigeria channels 900020 and 900021."
    problem: "Example list appears authoritative but excludes NGN despite Nigeria bank channels documented on same page; integrator may wrongly conclude NGN bank payouts unsupported; currency example incompleteness, NGN omission, example versus table drift."
    use_when: "Composing NGN bank payouts; documenting supported currencies; updating payouts.md."
    avoid_when: "Currencies explicitly listed; non-bank-payout flows."
    expected: "Reader treats example list as non-exhaustive and relies on channel table for NGN support."
  - anchor: contradictions-nigeria-result-url
    what: "Nigeria payout request-fields table marks result_url as required, but bank-transfer payout example omits it."
    problem: "Integrator cannot know whether to include result_url in Nigeria payout requests because required-field table conflicts with omission in worked example; omitted field may cause request rejection or silent success; payout result_url ambiguity, result_url requirement drift."
    use_when: "Writing Nigeria payout request examples; validating mandatory field list against samples; updating Nigeria guide."
    avoid_when: "Non-Nigeria flows; payout fields where table and example match."
    expected: "Reader flags conflict and tests whether result_url is accepted or rejected when omitted."
---

# Documented Contradictions in Bobplus API Docs

This file collects contradictions, inconsistencies, and ambiguous facts found in the scraped Bobplus Payments API documentation. Each entry preserves the exact source URLs so the corpus mirrors the site rather than "fixing" it.

## Nigeria bank payout channel codes
[ref: #contradictions-nigeria-payout-channel]

Three different code sets appear for Nigeria bank payouts:

- `300043` — used in the Nigeria integration guide for "Bank Transfer" payouts.
- `900020` — "BANK CHANNEL - NIGERIA (NGN VA)" in the bank-payout page.
- `900021` — "BANK CHANNEL - NIGERIA (NGN NUBAN)" in the bank-payout page; the page explicitly says "Use channel `900021` for NGN NUBAN payouts".

The bank-payout page and the Nigeria guide therefore disagree on the canonical NGN bank-payout channel. Additionally, `300043` appears inside the mobile-money payout channel table as "BANK TRANSFER - NIGERIA".

Sources: [Bank Payout](https://developers.bobplus.africa/b2c/bank-payout), [Nigeria Guide](https://developers.bobplus.africa/nigeria), [MoMo Payout](https://developers.bobplus.africa/b2c/momo-payout)

## South Africa payin channel codes
[ref: #contradictions-south-africa-payin-channel]

Two distinct ZAR payin channel families exist:

- `500000` — "MOBILE MONEY - SOUTH AFRICA" in the mobile-money payin channel table.
- `900017` (ZAR EFT) and `900018` (ZAR Capitec) in the South Africa payin page.

The mobile-money page treats South Africa as a generic mobile-money market, while the South Africa page documents bank-redirect flows. No cross-reference explains the relationship.

Sources: [Mobile Money Deposit](https://developers.bobplus.africa/c2b/momo-payin), [South Africa Payin](https://developers.bobplus.africa/c2b/south-africa-payin)

## Rate limit units
[ref: #contradictions-rate-limit-unit]

- Home page: "Default: **1500 requests per minute**."
- Bank-codes page: "Default: 1500 requests per second."

Both pages use the same numeric value but different time units, a 60× difference in effective throughput.

Sources: [Developer Docs (home)](https://developers.bobplus.africa/), [Bank Codes](https://developers.bobplus.africa/bank-codes)

## Nigeria virtual-account `bank_code`
[ref: #contradictions-nigeria-va-bank-code]

- Nigeria virtual-account page: `bank_code` is **No** (optional) with default `1067`.
- Nigeria guide: `bank_code` is **Conditional** and required only for Opay/PalmPay (`300045`) and bank payouts (`300043`), implying it is not needed for virtual-account payins (`300041`).

The default value `1067` in the VA page is not mentioned anywhere else.

Sources: [Nigeria Collections — Virtual Account](https://developers.bobplus.africa/c2b/nigeria-payin), [Nigeria Guide](https://developers.bobplus.africa/nigeria)

## Callback failed hash field order
[ref: #contradictions-callback-failed-hash-order]

The prose documents the failed-callback HMAC order as:

```text
channel+reference+transaction_id+result_code+result_description
```

But the sample failed JSON orders `result_code` before `transaction_id`:

```json
{
  "channel": "100001",
  "reference": "3883328",
  "result_code": 1032,
  "transaction_id": "2345432345",
  "result_description": "DS timeout user cannot be reached",
  "hash": "..."
}
```

Implementations following only one of these will fail verification.

Sources: [Webhook Callback](https://developers.bobplus.africa/callback-response)

## Virtual-account expiry timestamp
[ref: #contradictions-va-expiry-timestamp]

Nigeria VA examples show:

```json
"date": "2026-07-28 13:23:15 PM",
"fetched_at": "2026-07-28 13:23:21 PM",
"virtual_account": {
  "expires": "2026-07-28 12:23:21 PM"
}
```

`expires` is one hour earlier than generation, which is impossible for a future-expiring account.

Sources: [Nigeria Collections — Virtual Account](https://developers.bobplus.africa/c2b/nigeria-payin), [Nigeria Guide](https://developers.bobplus.africa/nigeria)

## Statement signature omits `from_date`
[ref: #contradictions-statement-signature-omits-from-date]

The full-statement request body requires `from_date`, `to_date`, `wallet_no`, and `limit`. The signature recipe signs only:

```text
wallet_no+to_date+limit
```

`from_date` is required in the body but not in the signature string.

Sources: [Account Full Statement](https://developers.bobplus.africa/account-services/full-statement)

## X-Hash payload ambiguity
[ref: #contradictions-x-hash-payload]

The X-Hash page instructs:

> "Use your private key to sign your `businessId` or the agreed payload."

The PHP example signs `$businessId` only. Payout pages require `x-hash` as a header but do not state what to sign for those endpoints.

Sources: [Generate X-Hash](https://developers.bobplus.africa/generate-x-hash), [Bank Payout](https://developers.bobplus.africa/b2c/bank-payout), [MoMo Payout](https://developers.bobplus.africa/b2c/momo-payout)

## `telco` accepted values
[ref: #contradictions-telco-values]

The request-body table lists `telco` examples as `orange`, `mtn`, `moov`, `wave`. The footnote expands the list to `orange`, `mtn`, `moov`, `wave`, `vodacom`, `airtel`. The table is therefore a subset of the accepted values.

Sources: [Mobile Money Deposit](https://developers.bobplus.africa/c2b/momo-payin), [MoMo Payout](https://developers.bobplus.africa/b2c/momo-payout)

## Base URL placeholders
[ref: #contradictions-base-url-placeholders]

No real production host is documented. Placeholders vary:

- `https://prod-url-here` — authentication, account-services-get-balance.
- `https://base-url-here` — account-services-full-statement, generate-x-hash, payouts.
- `https://base-url-here.com` — bank-codes, payouts.
- `https://here-prod-api-url.com` — transaction-status query.

Sources: multiple pages across the site

## Timestamp formats
[ref: #contradictions-timestamp-formats]

Examples use inconsistent formats:

- Balance: `2025-02-10 18:11:57` (no AM/PM).
- Statement: `2024-02-12 19:36:29 PM` (24-hour + PM, invalid).
- Payment responses: `2026-07-08 12:00:00 PM` (12-hour + PM).

No canonical timestamp format is stated.

Sources: [Fetch Balance](https://developers.bobplus.africa/account-services/get-balance), [Account Full Statement](https://developers.bobplus.africa/account-services/full-statement), [South Africa Payin](https://developers.bobplus.africa/c2b/south-africa-payin)

## Signature header casing
[ref: #contradictions-signature-header-casing]

Curl examples in endpoint pages use `Signature:` (title case). The PHP example in the signature generation page uses `signature:` (lower case). HTTP headers are case-insensitive, but the corpus should normalize examples.

Sources: [Generate Signature](https://developers.bobplus.africa/generate-signature), endpoint curl examples

## Statement amount type
[ref: #contradictions-amount-type]

The full-statement response table declares `amount` as `numeric`, but the example shows `"amount": "10"` (string). `balance` in the same example is numeric.

Sources: [Account Full Statement](https://developers.bobplus.africa/account-services/full-statement)

## Payin `x-hash`: table vs example
[ref: #contradictions-payin-x-hash-table-vs-example]

The mobile-money payin request-headers table lists only `Authorization` and `Signature`. The curl example on the same page sends `x-hash` as an active header:

```bash
--header 'x-hash: xxxxxx' # Generated X-Hash header \
```

Before the 2026-09-09 re-scrape this line was commented out (`# --header ...`); it is now active, while the table still omits the header. Whether payins require `x-hash` is undetermined.

Sources: [Mobile Money Deposit](https://developers.bobplus.africa/c2b/momo-payin)

## Nigeria VA response `acc_no` shape
[ref: #contradictions-nigeria-va-response-acc-no]

The Nigeria VA request sends `acc_no` as the customer phone number. The response examples show `data.acc_no` shaped like the generated virtual account number (e.g. `1234876588`), not the phone that was sent, while `virtual_account.account_number` carries the VA number too. The same field name therefore appears with two different meanings across request and response.

Sources: [Nigeria Collections — Virtual Account](https://developers.bobplus.africa/c2b/nigeria-payin), [Nigeria Guide](https://developers.bobplus.africa/nigeria)

## Signature example field-order mismatch
[ref: #contradictions-signature-example-field-order]

Generate-signature Step 3 shows a payin payload (`wallet_no`, `reference`, `acc_name`, `acc_no`, `currency`, `amount`, `channel`, ...), but the prose then says:

> "For this example, you might concatenate `account` and `customer_code` as: `2018709129392`."

Neither `account` nor `customer_code` exists in the payload shown. Endpoint pages document per-endpoint orders (e.g. `channel+reference+currency+amount` for payments); the generic page contradicts them.

Sources: [Generate Signature](https://developers.bobplus.africa/generate-signature), [Mobile Money Deposit](https://developers.bobplus.africa/c2b/momo-payin)

## Status-query reference semantics
[ref: #contradictions-status-query-reference-semantics]

In the status-query example, the request sends `"reference": "052423213417"`, but the success response carries `"transaction_id": "052423213417"` together with `"reference": "K902101"` — the response `transaction_id` equals the request `reference`, while the response `reference` is a different value. Which field echoes the request reference is undocumented; `acc_name`/`acc_no` semantics (payer, recipient, wallet holder) are also undefined.

Sources: [Payment Transaction Status](https://developers.bobplus.africa/transaction-status/payment)

## Bank-payout currency examples omit NGN
[ref: #contradictions-bank-payout-currency-examples]

The bank-payout request-body table describes `currency` as "Currency (e.g. KES, TZS, UGX, ZAR)", omitting NGN, while the channel table on the same page lists `900020` BANK CHANNEL - NIGERIA (NGN VA) and `900021` BANK CHANNEL - NIGERIA (NGN NUBAN), and the prose says "Use channel `900021` for NGN NUBAN payouts".

Sources: [Bank Payout](https://developers.bobplus.africa/b2c/bank-payout)

## Nigeria payout `result_url`
[ref: #contradictions-nigeria-result-url]

The Nigeria guide request-fields table marks `result_url` as `Yes` (required). The bank-transfer payout example in the same guide does not include `result_url` in the request body.

Sources: [Nigeria Guide](https://developers.bobplus.africa/nigeria)
