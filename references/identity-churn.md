# Identity Churn

Use this guide when resource addresses or object identity can shift unexpectedly.

## Symptoms

- plan shows broad replace actions after small list edits
- renaming resources/modules triggers destroy/create
- refactor from `count` to `for_each` causes churn
- imported resources keep drifting because addressing is unstable

## Primary causes

- index-based identity (`count`) used for long-lived logical objects
- keys derived from unstable data (sorted lists, transient IDs)
- missing `moved` blocks during refactor
- hidden dependencies forcing replacement chains
- `for_each` keys derived from values unknown at plan time

## Prevention rules

- use `for_each` for long-lived identities
- choose stable keys from business identity (e.g., `zone-a`, `payments-api`)
- keep identity attributes separate from mutable attributes
- add `moved` blocks before first apply after rename/restructure

## Decision matrix: `count` vs `for_each`

Use `count` only when:
- resource is truly optional singleton (`0` or `1`)
- no downstream references depend on stable per-item addresses

Use `for_each` when:
- multiple logical instances are expected
- insertion/removal/reordering happens over time
- downstream references need stable keys
- keys are fully known during planning

If keys are unknown at plan time, `for_each` will fail planning. In that case:
- drive `for_each` from known input keys, or
- use `count` for conditional/singleton creation when key-stable `for_each` is not possible

## Safe migration playbook (`count` -> `for_each`)

1. define stable key map
2. refactor resource to `for_each`
3. add one `moved` block per old index
4. verify plan reports move operations, not replace
5. apply in lower environment first

Example:

```hcl
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

## Rename playbook

When renaming resource/module labels, add `moved` first:

```hcl
moved {
  from = module.network_core
  to   = module.network_foundation
}
```

## LLM mistake checklist

Common model mistakes to correct:
- defaults to `count` for every collection
- omits `moved` blocks in refactors
- uses list index as identity key
- suggests `terraform state mv` in automation where `moved` is safer and reviewable
- builds `for_each` keys from computed IDs not known until apply

## Known-at-plan example (`for_each` failure pattern)

Bad (key depends on apply-time value):

```hcl
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

Safer fallback for optional singleton behavior:

```hcl
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

## Verification commands

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
