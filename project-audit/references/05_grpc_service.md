# gRPC API service template (agent prompt)

[ref: #pe-grpc]

Use the common template `references/04_service_card_common.md` first. This file adds only the gRPC-specific sections.

## Type-specific additions

### Exported gRPC service(s)

For every gRPC service exposed by the application, create a subsection.

```markdown
## Exported gRPC service: `<ServiceName>`

- **Proto package:** e.g. `classic.grpc.stubs.adverts`
- **Server framework:** internal async/sync gRPC server (`classic-grpc[async]` 0.1 / `classic-grpc[sync]` 0.1)
- **Platform servicers also exposed:** `HealthServicer`, `InjectableServicer`

#### Implemented / routed methods

| Method | Request | Response | Handler | Notes |
|--------|---------|----------|---------|-------|
| `CreateOrder` | `CreateOrderRequest` | `order_pb2.IdMessage` | `handlers.create_order` | — |
| ... | ... | ... | ... | ... |

#### Declared but not implemented

| Method | Reason / status |
|--------|-----------------|
| `UpdateNickname` | Mapped in routes but not declared in pinned proto; unreachable. |
| ... | ... |
```

Rules:
- Include both implemented and declared-but-unimplemented proto methods.
- Mark method aliases if the same handler answers multiple proto names.
- Keep request/response types as protobuf message names, not raw fields.

### Business logic / state machines (if relevant)

Add only when the domain has explicit rules worth documenting:

```markdown
## Business logic

- Status workflow: `NEW → PROCESSING → RESOLVED / REJECTED`.
- `UpdateType` rejects changing type to `DISPUTE` for existing cases.
- `DeleteClientPaymentMethod` transitions status only from `ACTIVE` or `CLOSING`.
```

Do not duplicate the method table here; only domain rules, status values, and lifecycle constraints.
