# Terraform Good Patterns

Eight strong implementation patterns that the Terraform skill uses as positive examples. Each pattern directly prevents one or more failure modes.

## 1. Stable Identity Map for Service Accounts

```javascript
variable "service_accounts" {
  type = map(object({
    display_name = string
    roles        = set(string)
  }))
}

resource "google_service_account" "app" {
  for_each     = var.service_accounts
  account_id   = each.key
  display_name = each.value.display_name
}
```

**Why this works:** Key-based identity survives insertion/removal changes. Contract is strict and predictable. Prevents identity churn.

## 2. Cross-Variable Validation for Safe Combinations

```javascript
variable "public_endpoint" {
  type    = bool
  default = false
}

variable "allowed_cidrs" {
  type    = list(string)
  default = []

  validation {
    condition     = var.public_endpoint || length(var.allowed_cidrs) == 0
    error_message = "allowed_cidrs must be empty unless public_endpoint is true."
  }
}
```

**Why this works:** Invalid combinations fail early. Intent is encoded directly in the module interface. Prevents blast radius from misconfigured access.

## 3. Strong Object Typing with Optional Fields

```javascript
variable "node_pool" {
  type = object({
    size           = string
    min_replicas   = number
    max_replicas   = number
    spot_instances = optional(bool, false)
  })
}
```

**Why this works:** Flexible without sacrificing schema clarity. Avoids ad-hoc maps and runtime surprises.

## 4. Narrow, Useful Outputs

```javascript
output "app_subnet_ids" {
  description = "Subnet ids for application workloads"
  value       = values(aws_subnet.app)[*].id
}
```

**Why this works:** Downstream modules get exactly what they need. Avoids leaking full provider objects that could expose sensitive data.

## 5. Controlled Provider Pinning

```javascript
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40.0, < 6.0.0"
    }
  }
}
```

**Why this works:** Controlled upgrade window prevents accidental major-version breakage. Prevents CI drift from floating versions.

## 6. Dynamic Block with Typed Variable

```javascript
variable "ingress_rules" {
  type = list(object({
    port        = number
    protocol    = string
    cidr_blocks = list(string)
  }))
}

resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

**Why this works:** Iterator uses `ingress.value` (named after the block label, not the variable). Typed input prevents runtime shape errors.

## 7. Provider Alias for Multi-Region

```javascript
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu"
  region = "eu-west-1"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.eu
  bucket   = "my-replica-bucket"
}

module "eu_network" {
  source = "./modules/network"
  providers = {
    aws = aws.eu
  }
}
```

**Why this works:** Explicit alias keeps region intent clear. Modules receive providers via `providers` map, not implicit inheritance.

## 8. `moved` Block for Safe Rename

```javascript
moved {
  from = aws_kms_key.logs
  to   = aws_kms_key.audit
}
```

**Why this works:** Keeps state continuity during naming refactors. Prevents unnecessary replacement that could destroy encryption keys.
