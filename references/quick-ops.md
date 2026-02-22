# Quick Ops

Use this page for fast command recall and common failure handling.

## Core command sequence

```bash
terraform fmt -check
terraform init
terraform validate
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
```

OpenTofu equivalent:

```bash
tofu fmt -check
tofu init
tofu validate
tofu plan -out=plan.bin
tofu show -json plan.bin > plan.json
```

## Common failures and fixes

### CI passes locally but fails in runner

- mismatch in runtime/provider versions
- missing lockfile updates
- environment variables present locally but missing in CI

Fix:

- pin runtime and providers
- commit lockfile
- make required env vars explicit in pipeline

### Large unexpected replacements in plan

- unstable iteration keys
- hidden rename without `moved` mapping
- data source drift feeding identity fields

Fix:

- stabilize keys
- add `moved` blocks
- separate identity from mutable attributes

### AWS RDS identifier validation errors

Symptoms:
- `InvalidParameterValue` for `identifier`
- `InvalidParameterValue` for `final_snapshot_identifier`
- names include dots (for example `lukasniessen.com-prod`)

Fix:
- normalize to lowercase letters, numbers, and hyphens
- reuse the same normalized base for both `identifier` and `final_snapshot_identifier`

```hcl
locals {
  rds_base = regexreplace(lower("${var.project}-prod"), "[^a-z0-9-]", "-")
}

resource "aws_db_instance" "main" {
  identifier = local.rds_base
  # ...
  final_snapshot_identifier = "${local.rds_base}-final"
}
```

Quick check:
- expected: `lukasniessen-com-prod`
- not allowed: `lukasniessen.com-prod`

### Apply contention on shared state

- concurrent pipelines targeting same backend key

Fix:

- serialize applies for that stack
- use lock timeout and per-stack concurrency guard

### Tests are too costly

Fix:

- tag tests by risk (`fast`, `integration`, `destructive`)
- run full suite nightly, risk-tier suite on PRs
- auto-clean ephemeral infra with TTL tags

### State lock stuck

Symptoms: `Error: Error acquiring the state lock`

Fix:

```bash
# Identify the lock holder from the error message (lock ID shown)
terraform force-unlock LOCK_ID
# OpenTofu equivalent:
tofu force-unlock LOCK_ID
```

Only force-unlock when you are certain no other apply is running. Check CI pipelines and team activity first.

### State corruption or lost state

Fix:

- restore from versioned state backend (S3 versioning, GCS versioning)
- if no backup: re-import resources using `import` blocks
- never manually edit state JSON unless absolutely no alternative and with peer review

```bash
# Pull current state for inspection
terraform state pull > state-backup.json
# List all tracked resources
terraform state list
```

### Backend migration

When changing state backends (e.g., local to S3, or S3 to different bucket):

```bash
# Update backend config in code, then:
terraform init -migrate-state
```

- always backup state before migration
- verify resource count matches after migration
- test plan shows no changes after migration

### Provider authentication failures in CI

Symptoms: `Error: No valid credential sources found`

Fix:

- verify environment variables are set in CI runner (`AWS_ACCESS_KEY_ID`, `ARM_CLIENT_ID`, `GOOGLE_CREDENTIALS`, etc.)
- prefer workload identity federation over static keys
- check credential expiry for short-lived tokens
- ensure CI runner IAM role/service account has required permissions

### `null_resource` vs `terraform_data`

Use `terraform_data` (TF 1.4+) instead of `null_resource` + `null` provider:

```hcl
# Prefer this (no extra provider needed):
resource "terraform_data" "bootstrap" {
  triggers_replace = [var.config_hash]

  provisioner "local-exec" {
    command = "bootstrap.sh"
  }
}

# Instead of this (requires hashicorp/null provider):
resource "null_resource" "bootstrap" {
  triggers = { config = var.config_hash }

  provisioner "local-exec" {
    command = "bootstrap.sh"
  }
}
```
