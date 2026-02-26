# Terraform Identity Churn: Preventing Resource Address Instability

Identity churn is one of the most common and dangerous Terraform failure modes. It occurs when resource addresses or object identity shift unexpectedly, causing destroy/create cycles that can take down production infrastructure.

## Symptoms of Identity Churn

- Plan shows broad replace actions after small list edits
- Renaming resources/modules triggers destroy/create instead of in-place updates
- Refactor from `count` to `for_each` causes churn
- Imported resources keep drifting because addressing is unstable

## Primary Causes

- **Index-based identity** (`count`) used for long-lived logical objects
- **Unstable keys** derived from sorted lists or transient IDs
- **Missing `moved` blocks** during refactors
- **Hidden dependencies** forcing replacement chains
- **`for_each` keys** derived from values unknown at plan time

## Prevention Rules

- Use `for_each` for long-lived identities
- Choose stable keys from business identity (e.g., `zone-a`, `payments-api`)
- Keep identity attributes separate from mutable attributes
- Add `moved` blocks before first apply after rename/restructure

## Decision Matrix: `count` vs `for_each`

### Use `count` only when:
- Resource is truly optional singleton (`0` or `1`)
- No downstream references depend on stable per-item addresses

### Use `for_each` when:
- Multiple logical instances are expected
- Insertion/removal/reordering happens over time
- Downstream references need stable keys
- Keys are fully known during planning

### When keys are unknown at plan time:
- Drive `for_each` from known input keys
- Use `count` for conditional/singleton creation when key-stable `for_each` is not possible

## Safe Migration: `count` to `for_each`

1. Define stable key map
2. Refactor resource to `for_each`
3. Add one `moved` block per old index
4. Verify plan reports move operations, not replace
5. Apply in lower environment first

### Example

```javascript
locals {
  app_subnets = {
    a = { cidr = "10.40.1.0/24", az = "us-east-1a" }
    b = { cidr = "10.40.2.0/24", az = "us-east-1b" }
  }
}

resource "aws_subnet" "app" {
  for_each          = local.app_subnets
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az
  tags = {
    Name = "app-${each.key}"
  }
}

moved {
  from = aws_subnet.app[0]
  to   = aws_subnet.app["a"]
}

moved {
  from = aws_subnet.app[1]
  to   = aws_subnet.app["b"]
}
```

## Rename Playbook

When renaming resource/module labels, always add `moved` first:

```javascript
moved {
  from = module.network_core
  to   = module.network_foundation
}
```

## Known-at-Plan Failure Pattern

**Bad** — key depends on apply-time value:

```javascript
resource "aws_security_group_rule" "egress" {
  for_each                 = toset([aws_security_group.ecs.id])
  type                     = "egress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = each.value
  cidr_blocks              = ["0.0.0.0/0"]
}
```

**Safer fallback** for optional singleton behavior:

```javascript
resource "aws_security_group_rule" "egress" {
  count                    = var.enable_egress_rule ? 1 : 0
  type                     = "egress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ecs.id
  cidr_blocks              = ["0.0.0.0/0"]
}
```

## LLM Mistake Checklist

Common model mistakes the Terraform skill corrects:

- Defaults to `count` for every collection
- Omits `moved` blocks in refactors
- Uses list index as identity key
- Suggests `terraform state mv` in automation where `moved` is safer and reviewable
- Builds `for_each` keys from computed IDs not known until apply

## Verification Commands

```bash
terraform fmt -check
terraform validate
terraform plan -out=plan.bin
terraform show plan.bin | grep -i moved
```

OpenTofu equivalent:

```bash
tofu fmt -check
tofu validate
tofu plan -out=plan.bin
tofu show plan.bin | grep -i moved
```
