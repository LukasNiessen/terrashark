# Terraform Neutral Patterns (Context-Dependent)

Six patterns that are neither universally good nor bad — they depend on organizational context, team size, and governance maturity. The Terraform skill presents these as explicit tradeoffs rather than recommendations.

## 1. Workspace-Centric Environment Split

```javascript
locals {
  env = terraform.workspace
}

resource "aws_cloudwatch_log_group" "audit" {
  name = "/org/${local.env}/audit"
}
```

**Tradeoff:** Clean for workspace-managed workflows. Harder to reason about in ad-hoc CLI usage across many environments.

## 2. Single Repo with Many Modules

```
iac-repo/
  modules/
    network/
    identity/
    observability/
  environments/
    dev/
    prod/
```

**Tradeoff:** Easy discovery and shared standards. Larger blast radius for repo-level process changes.

## 3. Remote-State Bridge Across Stacks

```javascript
data "terraform_remote_state" "platform" {
  backend = "gcs"
  config = {
    bucket = "infra-state-org"
    prefix = "platform/prod"
  }
}
```

**Tradeoff:** Quick integration path. Introduces coupling to producer stack internals.

## 4. Composite Module Owning Many Primitives

```javascript
module "payments_platform" {
  source = "./modules/payments-platform"
}
```

**Tradeoff:** Simplifies root composition. Can become hard to evolve if internal boundaries are unclear.

## 5. Apply-Mode Native Tests in CI

```javascript
run "database_contract" {
  command = apply
}
```

**Tradeoff:** Catches real runtime behavior. Increases cost and pipeline duration significantly.

## 6. Aggressive Precondition Usage

```javascript
resource "aws_s3_bucket" "artifact" {
  bucket = var.bucket_name

  lifecycle {
    precondition {
      condition     = startswith(var.bucket_name, "org-")
      error_message = "Bucket names must start with org-."
    }
  }
}
```

**Tradeoff:** Protects conventions early and enforces naming standards. Too many strict checks can reduce module reuse across different org units.
