---
subject: "Bobplus API security layer; OAuth bearer token issuance, `/api/v2/auth/login`, `consumer_key`, `consumer_secret`, `access_token`, RSA key pair, `openssl_sign`, SHA-256 signatures, `signature` header, `X-Hash` header, `businessId`, base64 encoding, token expiry, credential rotation, headers, tampering, authenticity."
index:
  - anchor: security-authentication
    what: "Bearer-token issuance: POST `consumer_key` + `consumer_secret` to `/api/v2/auth/login`, receive `access_token` (type `bearer`, `expires_in` 3600 seconds), send it as `Authorization: Bearer <token>` on every call; includes the error matrix (400/401/429/500)."
    problem: "Agent cannot call any endpoint until token flow works; missing or expired token yields `401` on otherwise correct requests; credential exchange, token lifecycle, auth handshake, unauthorized errors, header setup, session bootstrap, renewal, secrets management, login."
    use_when: "Obtaining or refreshing the access token; setting up the Authorization header; diagnosing 401 responses; implementing token caching with the one-hour expiry."
    avoid_when: "Request signing with RSA keys — the signature and x-hash sections; IP-based rejections — the whitelisting section in getting_started.md."
    expected: "Client obtains tokens on demand, attaches `Authorization: Bearer ...` to every request, and refreshes before `expires_in` elapses."
  - anchor: security-signature
    what: "The `signature` header recipe: generate an RSA-2048 key pair (`openssl genrsa`, `openssl rsa -pubout`), upload the public key to the business portal, concatenate designated payload fields in order, sign with SHA-256 via the private key, base64-encode into the `signature` header."
    problem: "Agent sends sensitive transaction requests without required digital signature; tampering checks fail server-side and requests are rejected despite valid token; request signing, field concatenation, key management, integrity protection, anti-tamper, cryptographic authenticity, verification, fraud."
    use_when: "Sending payout/payin or other sensitive requests; setting up RSA keys with openssl; implementing signing in any language (the docs show PHP `openssl_sign`); debugging rejected signed requests."
    avoid_when: "Simple token retrieval — the authentication section; the `X-Hash` identity header — the x-hash section."
    expected: "Every sensitive request carries a base64 SHA-256 `signature` over the documented field order, verifiable by Bobplus with the uploaded public key."
  - anchor: security-x-hash
    what: "The `X-Hash` header recipe: sign the `businessId` (found on the merchant portal) with the RSA private key using SHA-256, base64-encode it, and send it as the `x-hash` header alongside the bearer token and `signature`."
    problem: "Agent's requests lack additional identity proof layer demanded by some endpoints; impersonation checks reject unsigned calls even with correct token and signature; extra verification, header trio, signed identity, gating, authenticity, defense."
    use_when: "Calling endpoints that require the `x-hash` header; combining token, `signature`, and `x-hash` in one request; locating `businessId` on the merchant portal."
    avoid_when: "Payload-integrity signing — that is the `signature` section; initial key generation — covered once in the signature section."
    expected: "Requests carry token, `signature`, and `x-hash` together, with `x-hash` as base64 SHA-256 over `businessId`, and pass server verification."
---

# Bobplus API Security

Scraped from `https://developers.bobplus.africa` (pages `authentication`, `generate-signature`, `generate-x-hash`; docs version V2.1.2) on 2026-08-12.

## Authentication (Bearer Token)

[ref: #security-authentication]

Sources: [API Authentication](https://developers.bobplus.africa/authentication)

The API uses OAuth 2.0-style authentication: obtain a short-lived **Bearer Token** with the **Consumer Key** and **Consumer Secret** before any API requests.

Authentication endpoint:

| | |
|---|---|
| HTTP Method | POST |
| Endpoint URL | `/api/v2/auth/login` |
| Base URL | `https://prod-url-here` (as issued to your account) |
| Description | Obtain a Bearer Token using your Consumer Key and Secret |

Request headers: `Accept: application/json`, `Content-Type: application/json` (both required).

Request body fields:

| Field | Type | Description | Required |
|---|---|---|---|
| `consumer_key` | string | Your API consumer key | Yes |
| `consumer_secret` | string | Your API consumer secret | Yes |

Token request example:

```bash
curl --location --request POST 'https://prod-url-here/api/v2/auth/login' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "consumer_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "consumer_key": "XXXXXXXXXXXXXXXXXXXX"
}'
```

Success response fields: `success` (boolean), `message` (string), `data.access_token` (the Bearer Token), `data.token_type` (`bearer`), `data.expires_in` (token lifetime in seconds):

```json
{
    "success": true,
    "message": "Success",
    "data": {
        "access_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "token_type": "bearer",
        "expires_in": 3600
    }
}
```

The `access_token` goes into every API request as:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Error responses:

| Status | Example | Description |
|---|---|---|
| 400 | `{"success": false, "message": "Invalid credentials."}` | Bad Request |
| 401 | `{"success": false, "message": "Unauthorized."}` | Missing or invalid credentials |
| 429 | `{"success": false, "message": "Rate limit exceeded."}` | Too many requests |
| 500 | `{"success": false, "message": "Internal server error."}` | Server error |

Practices: keep the Consumer Key, Secret, and tokens confidential; tokens expire after **3600 seconds** (1 hour) — refresh as needed; rotate credentials regularly and revoke if compromised; use HTTPS for all API requests.

## Generate Signature

[ref: #security-signature]

Sources: [Generate Signature](https://developers.bobplus.africa/generate-signature)

All sensitive requests must be signed with a digital signature so Bobplus can verify authenticity and prevent tampering.

Flow overview: generate an RSA key pair → share the public key via the business portal → concatenate the designated fields from the request payload in the specified order → sign the concatenated string with the private key using SHA-256 → base64-encode the signature into the request header.

Generate the key pair:

```bash
openssl genrsa -out privatekey.pem 2048 -nodes
```

Export the public key (upload its contents to the business portal):

```bash
openssl rsa -in privatekey.pem -outform PEM -pubout -out publickey.pem
```

Prepare the data to sign — concatenate the required payload fields in the specified order. Example payload:

```json
{
    "wallet_no": "45594949",
    "reference": "KXXXXXXXXX",
    "acc_name": "John Doe",
    "acc_no": "2547XXXXXXXX",
    "currency": "KES",
    "amount": 10,
    "channel": 100000,
    "email": "johndoe@gmail.com",
    "description": "order payment",
    "result_url": "https://webhook.site/947e8f48-c03a-4717-a2dd-8cdb2f64e897"
}
```

Sign the concatenated string with SHA-256 (PHP example from the docs):

```php
$plainText  = "100000KXXXXXXXXXKES10"; // Concatenated string
$privateKeyString = str_replace("\\n", "\n", env('PRIVATE_KEY'));
$privateKey = openssl_pkey_get_private($privateKeyString);
openssl_sign($plainText, $signature, $privateKey, OPENSSL_ALGO_SHA256);
```

Curator's note — source inconsistency: the docs' Step 3 says "you might concatenate `account` and `customer_code` as: `2018709129392`", but the worked example signs `channel+reference+currency+amount` (`100000KXXXXXXXXXKES10`), and the field set differs per endpoint. Always take the exact fields and their order from the endpoint's own documentation section (the per-endpoint recipes in this corpus), never from this generic page.

Base64-encode the signature and add it to the request headers:

```php
CURLOPT_HTTPHEADER => array(
    "Authorization: Bearer " . $token,
    "cache-control: no-cache",
    "Content-Type: application/json",
    "signature: " . base64_encode($signature)
)
```

Practices: keep the private key secure and never share it; rotate keys regularly and update the public key in the portal; always use HTTPS.

## Generate X-Hash

[ref: #security-x-hash]

Sources: [Generate X-Hash](https://developers.bobplus.africa/generate-x-hash)

The `X-Hash` header adds a second signature layer: it is a digital signature generated with your private key over your `businessId` (or the agreed payload), verified by Bobplus with your public key.

Flow: reuse the RSA key pair from the signature guide → sign the `businessId` → base64-encode → send as the `x-hash` header.

Sign the `businessId` (found on the merchant portal) with SHA-256:

```php
$businessId        = "XXXXXXXXXXXXX"; // Found on your merchant portal
$privateKeyString  = str_replace("\\n", "\n", env('PRIVATE_KEY'));
$privateKey        = openssl_pkey_get_private($privateKeyString);

$dataToSign        = $businessId;
openssl_sign($dataToSign, $signature, $privateKey, OPENSSL_ALGO_SHA256);
$xHash             = base64_encode($signature);
```

Send the request with the full header set — token, `signature`, and `x-hash`:

```php
curl_setopt_array($curl, [
    CURLOPT_URL            => "https://base-url-here/api/v2/payment/",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CUSTOMREQUEST  => "POST",
    CURLOPT_POSTFIELDS     => $data_string,
    CURLOPT_HTTPHEADER     => [
        "Authorization: Bearer {$token}",
        "Content-Type: application/json",
        "cache-control: no-cache",
        "signature: XXXXXXXXXXXXXXXXXXXX", // per the signature guide
        "x-hash: {$xHash}"                 // generated X-Hash header
    ]
]);
```

The `X-Hash` is verified on the server using your public key. Practices mirror the signature guide: protect the private key, rotate keys regularly, use HTTPS everywhere.
