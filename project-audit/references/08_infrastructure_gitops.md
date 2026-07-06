# Infrastructure / GitOps template (agent prompt)

[ref: #pe-infra]

Use the common template `references/04_service_card_common.md` first. This file adds only the infrastructure-specific sections.

## Type-specific additions

### Deployed services / environments

```markdown
## Deployed backend services

#### Namespace `important` (production)

| Release | Helm chart | Image tag | Notes |
|---------|------------|-----------|-------|
| `important-api` | `important-api` | 0.0.12 | — |
| `important-wf` | `temporal-worker` | 8.2.0 | Queue `default`, namespace `important-api` |
| ... | ... | ... | ... |

#### Frontends (namespace `frontend`)

| Release | Helm chart | Image | Ingress host |
|---------|------------|-------|--------------|
| `important-nginx` | `nginx` | `important-nginx` | `kalaver.in`, `www.kalaver.in` |
| ... | ... | ... | ... |
```

Rules:
- Group by namespace/environment.
- Include chart name and image tag.
- Add a short note for special configuration (queue, namespace, ingress gateway, etc.).

### Key files / entry points

```markdown
## Key files

| File | Purpose |
|------|---------|
| `clusters/classic-prod/important-apps.yaml` | Root Flux Kustomization |
| `apps/classic-prod/important/kustomization.yaml` | Aggregates backend HelmReleases |
| `apps/base/important/<service>/release.yaml` | Per-service base HelmRelease |
```

### Infrastructure dependencies

```markdown
## Infrastructure dependencies

| Component | Nature | Details |
|-----------|--------|---------|
| Flux CD | GitOps engine | `important-apps` Kustomization |
| Kubernetes | Runtime | `classic-prod` cluster |
| Helm | Packaging | `gar` HelmRepository in `flux-system` |
| Istio | Service mesh | Sidecars, VirtualServices, ingress gateways |
| HashiCorp Vault | Secrets | `vault-injector` |
| PostgreSQL | Database | `1.1.1.1:5432`; per-app DB names |
```

### Conventions

```markdown
## Conventions

- Base + overlay GitOps pattern.
- One HelmRelease per app; `metadata.name` == `spec.releaseName`.
- Temporal workers use chart `temporal-worker` 0.6.2.
- Dedicated `important` nodegroup via taints/tolerations.
```

Do not list anomalies or gotchas here — route them to the appropriate entity-scoped namespace as defined in `serena-protocol` `[ref: #serena-findings-traceability]`.
