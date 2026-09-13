# Migration Playbooks

Use this guide when changing addresses, iteration strategy, runtime versions, or secret handling.

## 1) `count` to `for_each` migration

Goal: keep object identity stable during refactor.

Steps:

1. define stable keys (not list indexes)
2. add `for_each` implementation
3. add `moved` mappings from old index addresses to new keyed addresses
4. run plan and confirm move operations (not destroy/create)
5. apply in low-risk environment first

Example mapping:

```hcl
moved {
  from = aws_subnet.app[0]
  to   = aws_subnet.app["a"]
}

moved {
  from = aws_subnet.app[1]
  to   = aws_subnet.app["b"]
}
```

## 2) Resource/module rename

Use `moved` for address renames before any apply.

```hcl
moved {
  from = module.edge_cache
  to   = module.cdn_edge
}
```

## 3) Import-first adoption

When taking over manually created resources:

- confirm remote object exactly matches intended config shape
- import into correct address
- run plan and ensure no surprise replacements

### `import` block (TF 1.5+ / OpenTofu 1.5+)

Prefer declarative `import` blocks over CLI `terraform import`:

```hcl
import {
  to = aws_s3_bucket.logs
  id = "my-existing-bucket-name"
}

resource "aws_s3_bucket" "logs" {
  bucket = "my-existing-bucket-name"
}
```

For multiple resources, use `for_each` on import blocks:

```hcl
locals {
  existing_buckets = {
    logs    = "prod-logs-bucket"
    archive = "prod-archive-bucket"
  }
}

import {
  for_each = local.existing_buckets
  to       = aws_s3_bucket.managed[each.key]
  id       = each.value
}

resource "aws_s3_bucket" "managed" {
  for_each = local.existing_buckets
  bucket   = each.value
}
```

After import:
- run `terraform plan` and verify zero changes (no-diff)
- if plan shows changes, align config with actual state before applying
- remove `import` blocks after successful apply (they are one-time directives)

## 4) Secrets remediation

If secrets are currently in state:

1. create new secret path in managed secret store
2. switch resources to reference external secret material
3. rotate credentials after cutover
4. remove old secret-generating Terraform resources where possible

## 5) Runtime/provider upgrade flow

- bump constraints intentionally
- regenerate lockfile
- run full test tier for target risk
- inspect deprecations and behavior shifts
- ship upgrade independently from functional changes when possible

## Migration red flags

- plan shows broad replace for unrelated resources
- key changes derived from unstable list order
- unknown ownership of imported resources
- no rollback narrative for production apply
