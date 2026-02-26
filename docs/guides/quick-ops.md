# Terraform Quick Ops and Troubleshooting

Fast command recall and common failure handling for Terraform and OpenTofu operations.

## Core Command Sequence

### Terraform

```bash
terraform fmt -check
terraform init
terraform validate
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
```

### OpenTofu

```bash
tofu fmt -check
tofu init
tofu validate
tofu plan -out=plan.bin
tofu show -json plan.bin > plan.json
```

## Common Failures and Fixes

### CI Passes Locally but Fails in Runner

**Causes:**
- Mismatch in runtime/provider versions
- Missing lockfile updates
- Environment variables present locally but missing in CI

**Fix:**
- Pin runtime and providers
- Commit lockfile
- Make required env vars explicit in pipeline

### Large Unexpected Replacements in Plan

**Causes:**
- Unstable iteration keys
- Hidden rename without `moved` mapping
- Data source drift feeding identity fields

**Fix:**
- Stabilize keys
- Add `moved` blocks
- Separate identity from mutable attributes

### AWS RDS Identifier Validation Errors

**Symptoms:** `InvalidParameterValue` for `identifier` or `final_snapshot_identifier`, names include dots.

**Fix:** Normalize to lowercase letters, numbers, and hyphens:

```javascript
locals {
  rds_base = regexreplace(lower("${var.project}-prod"), "[^a-z0-9-]", "-")
}

resource "aws_db_instance" "main" {
  identifier                = local.rds_base
  final_snapshot_identifier = "${local.rds_base}-final"
}
```

### Apply Contention on Shared State

**Cause:** Concurrent pipelines targeting same backend key.

**Fix:**
- Serialize applies for that stack
- Use lock timeout and per-stack concurrency guard

### Tests Are Too Costly

**Fix:**
- Tag tests by risk (`fast`, `integration`, `destructive`)
- Run full suite nightly, risk-tier suite on PRs
- Auto-clean ephemeral infra with TTL tags

### State Lock Stuck

**Symptom:** `Error: Error acquiring the state lock`

**Fix:**

```bash
# Identify the lock holder from the error message (lock ID shown)
terraform force-unlock LOCK_ID
# OpenTofu equivalent:
tofu force-unlock LOCK_ID
```

Only force-unlock when you are certain no other apply is running. Check CI pipelines and team activity first.

### State Corruption or Lost State

**Fix:**
- Restore from versioned state backend (S3 versioning, GCS versioning)
- If no backup: re-import resources using `import` blocks
- Never manually edit state JSON unless absolutely no alternative and with peer review

```bash
# Pull current state for inspection
terraform state pull > state-backup.json
# List all tracked resources
terraform state list
```

### Backend Migration

When changing state backends (e.g., local to S3, or S3 to different bucket):

```bash
# Update backend config in code, then:
terraform init -migrate-state
```

- Always backup state before migration
- Verify resource count matches after migration
- Test plan shows no changes after migration

### Provider Authentication Failures in CI

**Symptom:** `Error: No valid credential sources found`

**Fix:**
- Verify environment variables are set in CI runner
- Prefer workload identity federation over static keys
- Check credential expiry for short-lived tokens
- Ensure CI runner IAM role/service account has required permissions

### `null_resource` vs `terraform_data`

Use `terraform_data` (TF 1.4+) instead of `null_resource` + `null` provider:

```javascript
# Prefer this (no extra provider needed):
resource "terraform_data" "bootstrap" {
  triggers_replace = [var.config_hash]

  provisioner "local-exec" {
    command = "bootstrap.sh"
  }
}
```
