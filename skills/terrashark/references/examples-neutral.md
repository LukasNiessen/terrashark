# Neutral Examples (Context-Dependent)

## 1) Workspace-centric environment split

```hcl
locals {
  env = terraform.workspace
}

resource "aws_cloudwatch_log_group" "audit" {
  name = "/org/${local.env}/audit"
}
```

Tradeoff:
- clean for workspace-managed workflows
- harder to reason about in ad-hoc CLI usage across many environments

## 2) Single repo with many modules

```text
iac-repo/
  modules/
    network/
    identity/
    observability/
  environments/
    dev/
    prod/
```

Tradeoff:
- easy discovery and shared standards
- larger blast radius for repo-level process changes

## 3) Remote-state bridge across stacks

```hcl
data "terraform_remote_state" "platform" {
  backend = "gcs"
  config = {
    bucket = "infra-state-org"
    prefix = "platform/prod"
  }
}
```

Tradeoff:
- quick integration path
- introduces coupling to producer stack internals

## 4) Composite module owning many primitives

```hcl
module "payments_platform" {
  source = "./modules/payments-platform"
}
```

Tradeoff:
- simplifies root composition
- can become hard to evolve if boundaries inside module are unclear

## 5) Apply-mode native tests in CI

```hcl
run "database_contract" {
  command = apply
}
```

Tradeoff:
- catches real runtime behavior
- increases cost and pipeline duration

## 6) Aggressive precondition usage

```hcl
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

Tradeoff:
- protects conventions early
- too many strict checks can reduce module reuse across org units
