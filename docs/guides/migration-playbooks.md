# Terraform Migration Playbooks

Five dedicated playbooks for safely migrating Terraform resources without causing identity churn, data loss, or downtime.

## Playbook 1: `count` to `for_each` Migration

**Goal:** Keep object identity stable during refactor.

### Steps

1. Define stable keys (not list indexes)
2. Add `for_each` implementation
3. Add `moved` mappings from old index addresses to new keyed addresses
4. Run plan and confirm move operations (not destroy/create)
5. Apply in low-risk environment first

### Example Mapping

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

## Playbook 2: Resource/Module Rename

Use `moved` for address renames before any apply.

```hcl
moved {
  from = module.edge_cache
  to   = module.cdn_edge
}
```

## Playbook 3: Import-First Adoption

When taking over manually created resources:

1. Confirm remote object exactly matches intended config shape
2. Import into correct address
3. Run plan and ensure no surprise replacements

### Declarative `import` Block (TF 1.5+ / OpenTofu 1.5+)

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

### Bulk Import with `for_each`

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

### Post-Import Checklist

- Run `terraform plan` and verify zero changes (no-diff)
- If plan shows changes, align config with actual state before applying
- Remove `import` blocks after successful apply (they are one-time directives)

## Playbook 4: Secrets Remediation

If secrets are currently in state:

1. Create new secret path in managed secret store
2. Switch resources to reference external secret material
3. Rotate credentials after cutover
4. Remove old secret-generating Terraform resources where possible

## Playbook 5: Runtime/Provider Upgrade Flow

1. Bump constraints intentionally
2. Regenerate lockfile
3. Run full test tier for target risk
4. Inspect deprecations and behavior shifts
5. Ship upgrade independently from functional changes when possible

## Migration Red Flags

Watch for these warning signs during any migration:

- Plan shows broad replace for unrelated resources
- Key changes derived from unstable list order
- Unknown ownership of imported resources
- No rollback narrative for production apply
