# Terraform Secret Exposure: Preventing Credential Leaks

Secret exposure occurs when credentials, tokens, or sensitive data leak into Terraform state files, CI logs, plan output, variable defaults, or artifact storage. This is a critical security failure mode.

## Symptoms of Secret Exposure

- Secret values appear in plan output or logs
- Credentials are defined in variable defaults
- Sensitive outputs are printed in CI
- Generated passwords are stored in state unintentionally

## Exposure Paths

- **Hardcoded defaults** in `variables.tf`
- **State persistence** — secret-bearing resources whose values are persisted in state
- **Logging** — `terraform show` outputs without redaction
- **Artifact retention** — policies that keep plan/state exports too long

## Prevention Baseline

- Never set secret defaults in code
- Source secrets from managed secret stores at runtime
- Mark secret variables and outputs as `sensitive = true`
- Restrict state backend access aggressively
- Avoid publishing raw plan JSON as broadly accessible artifact

## Runtime Patterns (Preferred Order)

1. **External secret manager lookup** (AWS Secrets Manager, HashiCorp Vault, etc.)
2. **Workload identity federation** for providers
3. **Short-lived credentials** from trusted broker

Avoid long-lived static credentials in repository or runner config.

## Understanding `sensitive` and `write_only`

- `sensitive = true` masks display but the value can still exist in state depending on provider behavior
- `write_only` arguments (where supported) reduce state persistence risk
- Always verify provider docs before assuming secret material is excluded from state

## Good Example: Secret Manager Integration

```javascript
variable "db_admin_username" {
  description = "Database admin user"
  type        = string
}

data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/admin"
}

resource "aws_db_instance" "core" {
  identifier = "core-db-prod"
  username   = var.db_admin_username
  password   = jsondecode(
    data.aws_secretsmanager_secret_version.db_password.secret_string
  )["password"]
}
```

## Bad Example: Plaintext Default

```javascript
variable "db_password" {
  type    = string
  default = "ChangeMe123!"  # NEVER do this
}
```

## Rotation Playbook

1. Create new secret version in manager
2. Update application to consume new version
3. Roll infrastructure safely
4. Revoke old credential
5. Verify no leaked copies remain in logs/artifacts

## LLM Mistake Checklist

Common model mistakes the Terraform skill corrects:

- Assumes `sensitive` alone means "not in state"
- Proposes plaintext defaults for demo convenience
- Uses outputs that expose full connection strings in PR comments
- Forgets artifact retention and access controls in CI

## Verification Commands

```bash
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
# Ensure secret fields are not emitted to shared artifacts/logs
```
