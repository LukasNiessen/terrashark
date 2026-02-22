# Bad Examples

## 1) List-driven `count` for mutable identities

```hcl
variable "queue_names" {
  type = list(string)
}

resource "aws_sqs_queue" "worker" {
  count = length(var.queue_names)
  name  = var.queue_names[count.index]
}
```

Why this fails:
- reordering list entries can force unexpected replacements
- object identity is tied to index, not business key

## 2) No type constraints on critical input

```hcl
variable "network" {
  default = {}
}
```

Why this fails:
- consumer mistakes surface late and noisily
- module contract is ambiguous

## 3) Sensitive defaults committed in code

```hcl
variable "api_token" {
  type    = string
  default = "token-please-change"
}
```

Why this fails:
- secret can leak via VCS and logs
- violates basic secret hygiene

## 4) Floating provider versions

```hcl
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}
```

Why this fails:
- pulls latest provider implicitly
- increases non-deterministic CI behavior

## 5) Blanket `ignore_changes`

```hcl
resource "aws_db_instance" "main" {
  identifier = "core-db"
  engine     = "postgres"

  lifecycle {
    ignore_changes = all
  }
}
```

Why this fails:
- masks drift and important config regressions
- erodes trust in plan output

## 6) Dynamic block with wrong iterator reference

```hcl
variable "ports" {
  type = list(number)
}

resource "aws_security_group" "app" {
  name = "app-sg"

  dynamic "ingress" {
    for_each = var.ports
    content {
      from_port   = ports.value   # WRONG: should be ingress.value
      to_port     = ports.value   # WRONG: should be ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

Why this fails:
- iterator name defaults to the dynamic block label (`ingress`), not the variable name
- using `ports.value` causes an unknown reference error
- common LLM hallucination pattern

## 7) Hidden ordering via unrelated `depends_on`

```hcl
resource "aws_iam_role" "app" {
  name = "app-role"
}

resource "aws_cloudwatch_log_group" "app" {
  name       = "/app/runtime"
  depends_on = [aws_iam_role.app]
}
```

Why this fails:
- artificial dependency reduces parallelism
- hides poor interface boundaries
