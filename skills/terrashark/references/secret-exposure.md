# Secret Exposure

Use this guide when secrets may leak into state, logs, defaults, or CI artifacts.

## Symptoms

- secret values appear in plan output or logs
- credentials are defined in variable defaults
- sensitive outputs are printed in CI
- generated passwords are stored in state unintentionally

## Exposure paths

- hardcoded defaults in `variables.tf`
- secret-bearing resources whose values are persisted in state
- logging `terraform show` outputs without redaction
- artifact retention policies that keep plan/state exports too long

## Prevention baseline

- never set secret defaults in code
- source secrets from managed secret stores at runtime
- mark secret variables and outputs as `sensitive = true`
- restrict state backend access aggressively
- avoid publishing raw plan JSON as broadly accessible artifact

## Runtime patterns

Preferred order:
1. external secret manager lookup
2. workload identity federation for providers
3. short-lived credentials from trusted broker

Avoid long-lived static credentials in repository or runner config.

## Write-only and sensitive handling

- `sensitive = true` masks display, but value can still exist in state depending on provider behavior
- `write_only` arguments (where supported) reduce state persistence risk
- always verify provider docs before assuming secret material is excluded from state

## Rotation playbook

1. create new secret version in manager
2. update application to consume new version
3. roll infrastructure safely
4. revoke old credential
5. verify no leaked copies remain in logs/artifacts

## Good example

```hcl
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
  password   = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

## Bad example

```hcl
variable "db_password" {
  type    = string
  default = "ChangeMe123!"
}
```

## LLM mistake checklist

Common model mistakes to correct:
- assumes `sensitive` alone means "not in state"
- proposes plaintext defaults for demo convenience
- uses outputs that expose full connection strings in PR comments
- forgets artifact retention and access controls in CI

## Verification commands

```bash
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
# Ensure secret fields are not emitted to shared artifacts/logs
```
