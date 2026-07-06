# Temporal workflow worker template (agent prompt)

[ref: #pe-temporal]

Use the common template `references/04_service_card_common.md` first. This file adds only the worker-specific sections.

## Type-specific additions

### Temporal workflows

```markdown
## Temporal workflows

| Temporal name | Class | Purpose | Signals | Updates | Queries | Cron / schedule |
|---------------|-------|---------|---------|---------|---------|-----------------|
| `payin` | `Payin` | Merchant pay-in processing | — | `accept_payin_order`, `reject_payin_order` | — | — |
| `exchange` | `Exchange` | P2P exchange lifecycle | — | `accept_order_by_user`, `confirm_order_by_buyer`, ... | — | — |
| ... | ... | ... | ... | ... | ... | ... |
```

Rules:
- Use the Temporal workflow name, not only the Python class name.
- List signals, updates, queries, and cron/schedule triggers if they exist.
- Mark placeholder/stub workflows explicitly.

### Temporal activities

```markdown
## Temporal activities

| Activity name | Function | Downstream resource | Purpose |
|---------------|----------|---------------------|---------|
| `get_client_by_id` | `activities.important_api.get_client_by_id` | `important-api` (`ImportantService.GetClientById`) | Fetch client record |
| `create_order` | `activities.orders_api.create_order` | `orders-api` (`OrdersService.CreateOrder`) | Create payin order |
| ... | ... | ... | ... |
```

Rules:
- Use the Temporal activity name.
- Map each activity to the downstream service/method it calls.
- Group activities by downstream domain if there are many.
- Mark activities that are defined but not registered in the worker.

### Schedules, signals, queries

```markdown
## Cron schedules

- `generate new pizza` — `@every 1m`
- `collect empty bottles` — `@every 5m`

## Signals

- `unlock_transfer` → `Clearing`
- `confirm_refund_start` → `Deposit`
```

### Business logic / state machines (if relevant)

Add only explicit domain rules, e.g. order status flows, retry/timeout policies that affect behavior, or idempotency rules.

```markdown
## Business logic

- Idempotency key for deposits: `deposit:{tx_hash}:{log_index}`.
- `Clearing` calls `continue_as_new` on FAILED transfers.
```
