# Backend State Safety

**Load this reference when detected:** state backend `s3`, `azurerm`, `gcs`, `remote`, `cloud`, `pg`, `consul`, or `local`; or task mentions backend migration, state storage, locking, force-unlock, state backup, or restore.

## Detection signals

- backend blocks using `s3`, `azurerm`, `gcs`, `remote`, `cloud`, `pg`, `consul`, or `local`
- commands or discussion around `init -migrate-state`, `init -reconfigure`, `state pull`, `force-unlock`, backup, restore, or backend migration
- CI or production work that creates, changes, or authenticates to state storage

## Why this matters

Terraform/OpenTofu state is the source of truth for live resource identity and often contains sensitive values. Backend mistakes can leak secrets, orphan resources, disable locking, or make a routine refactor look like a destructive replacement.

## Backend baseline

- Use remote state for every shared, CI, or production environment.
- Require locking on every apply path.
- Encrypt state at rest and in transit.
- Enable state versioning or point-in-time recovery where the backend supports it.
- Keep backend storage and lock primitives in a bootstrap root with a separate lifecycle.
- Never manage the backend bucket/container/table from the same root that uses it as its active backend.
- Keep backend credentials out of checked-in backend config; prefer workload identity or CI-provided partial backend config.

## Backend-specific checks

| Backend | Required checks |
| --- | --- |
| `s3` | Bucket versioning, encryption, public access block, narrow IAM, lock mechanism configured, state key split by environment/root. |
| `azurerm` | Storage account encryption, blob soft delete/versioning where available, lease-based locking, private/network restrictions, narrow data-plane RBAC. |
| `gcs` | Bucket versioning, uniform bucket-level access, encryption policy, narrow IAM, prefix split by environment/root. |
| `remote` / `cloud` | Workspace boundary matches blast radius, state sharing is restricted, sensitive variables are marked, applies use approved execution mode. |
| `pg` | TLS, database backups, least-privilege user, lock behavior verified, connection secrets kept out of code. |
| `consul` | TLS, ACLs, snapshots/backups, highly available quorum, lock/session behavior verified. |
| `local` | Solo prototype only; do not use for shared, CI, or production environments. |

## Migration guardrails

- Do not combine backend migration with unrelated resource changes.
- Freeze applies for the affected state before migrating.
- Pull and securely store a state backup before `init -migrate-state`; do not commit it.
- Record current backend type, address/key, workspace, runtime version, and actor.
- Migrate the lowest-risk environment first.
- After migration, compare resource addresses before/after and run a no-op plan.
- Keep the old backend retained and access-controlled until restore has been tested or the rollback window has passed.

Use `init -migrate-state` when moving state between backends. Use `init -reconfigure` only when intentionally accepting the configured backend without migrating existing state.

## Lock handling

- Treat a lock as a safety signal, not an inconvenience.
- Before `force-unlock`, verify the lock holder, CI run, process, and timestamp.
- Never recommend `force-unlock` while an apply may still be running.
- Serialize applies for shared foundation, backend, identity, and network roots.

## Access and secret handling

- Treat state readers as secret readers.
- Avoid storing plan/state artifacts in public or broad-access CI logs.
- If a secret entered state, rotate the secret and use the secret remediation playbook; masking output is not enough.
- Keep backend read/write permissions separate when the platform supports it.

## LLM mistake checklist

- Suggesting `local` backend for a team, CI, or production stack.
- Creating backend storage inside the same root that uses it.
- Omitting a lock strategy for a shared backend.
- Treating encryption as protection from anyone who can read state.
- Combining backend migration with broad resource refactors.
- Recommending `force-unlock` without proving no apply is active.
- Deleting old backend data immediately after migration.
- Hard-coding backend credentials in HCL or checked-in config.

## Validation commands

Use the active runtime (`terraform` or `tofu`) consistently:

```bash
terraform version
terraform workspace show
terraform state pull > state-backup.json
terraform state list > state-before.txt
terraform init -migrate-state
terraform state list > state-after.txt
diff -u state-before.txt state-after.txt
terraform plan -detailed-exitcode
```

Store `state-backup.json` in a secure temporary location outside the repository and delete it only after rollback is no longer needed.
