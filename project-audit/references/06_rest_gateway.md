# REST API gateway template (agent prompt)

[ref: #pe-rest]

Use the common template `references/04_service_card_common.md` first. This file adds only the REST-gateway-specific sections.

## Type-specific additions

### Exported REST API

Split into public/unauthenticated endpoints and authenticated `/api/v1` endpoints.

```markdown
## Exported REST API

#### Health / misc (unauthenticated)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/ping` | Liveness probe |
| GET | `/api/version` | Service version |
| GET | `/healthcheck` | Health check |
| GET | `/status` | Health + dependency status |
| POST | `/secret` | Vault injector callback |

#### `/api/v1/orders`

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/api/v1/orders` | OAuth2 | List orders |
| GET | `/api/v1/orders/{order_id}` | OAuth2 | Get order |
| PATCH | `/api/v1/orders/{order_id}/status` | OAuth2 | Close order by bartender |
| ... | ... | ... | ... |
```

Rules:
- Group endpoints by router/domain.
- Include auth requirement per endpoint (e.g. `none`, `OAuth2`, `RSA-PSS`, `HMAC`).
- For path parameters, use `{param}` notation.
- Do not list full request/response schemas — only path, method, auth, and one-line purpose.

### Authentication scheme (if relevant)

```markdown
## Authentication

- Zitadel OAuth2 bearer token introspection via `authlib`/`pyjwt` (RS256).
- RSA-PSS SHA-256 request/response signing for merchant endpoints.
- HMAC webhooks for KYC/KYT callbacks.
```

Add only the scheme that is actually used, with a reference to the code files where it is implemented.
