# Terraform Anti-Patterns (Bad Patterns)

Seven common anti-patterns that the Terraform skill explicitly prevents. Each pattern maps to a specific failure mode and is a known LLM hallucination risk.

## 1. List-Driven `count` for Mutable Identities

```hcl
variable "queue_names" {
  type = list(string)
}

resource "aws_sqs_queue" "worker" {
  count = length(var.queue_names)
  name  = var.queue_names[count.index]
}
```

**Why this fails:** Reordering list entries forces unexpected replacements. Object identity is tied to index, not business key. **Failure mode:** Identity churn.

## 2. No Type Constraints on Critical Input

```hcl
variable "network" {
  default = {}
}
```

**Why this fails:** Consumer mistakes surface late and noisily. Module contract is ambiguous. **Failure mode:** Blast radius from silent misconfiguration.

## 3. Sensitive Defaults Committed in Code

```hcl
variable "api_token" {
  type    = string
  default = "token-please-change"
}
```

**Why this fails:** Secret can leak via VCS and logs. Violates basic secret hygiene. **Failure mode:** Secret exposure.

## 4. Floating Provider Versions

```hcl
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}
```

**Why this fails:** Pulls latest provider implicitly. Increases non-deterministic CI behavior. **Failure mode:** CI drift.

## 5. Blanket `ignore_changes`

```hcl
resource "aws_db_instance" "main" {
  identifier = "core-db"
  engine     = "postgres"

  lifecycle {
    ignore_changes = all
  }
}
```

**Why this fails:** Masks drift and important config regressions. Erodes trust in plan output. **Failure mode:** CI drift and blast radius.

## 6. Dynamic Block with Wrong Iterator Reference

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

**Why this fails:** The iterator name defaults to the dynamic block label (`ingress`), not the variable name. Using `ports.value` causes an unknown reference error. **This is a common LLM hallucination pattern.**

## 7. Hidden Ordering via Unrelated `depends_on`

```hcl
resource "aws_iam_role" "app" {
  name = "app-role"
}

resource "aws_cloudwatch_log_group" "app" {
  name       = "/app/runtime"
  depends_on = [aws_iam_role.app]
}
```

**Why this fails:** Artificial dependency reduces parallelism. Hides poor interface boundaries. **Failure mode:** Blast radius from hidden coupling.
