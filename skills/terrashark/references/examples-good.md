# Good Examples

## 1) Stable identity map for service accounts

```hcl
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

Why this works:
- key-based identity survives insertion/removal changes
- contract is strict and predictable

## 2) Cross-variable validation for safe combinations

```hcl
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

Why this works:
- invalid combinations fail early
- intent is encoded directly in module interface

## 3) Strong object typing with optional fields

```hcl
variable "node_pool" {
  type = object({
    size          = string
    min_replicas  = number
    max_replicas  = number
    spot_instances = optional(bool, false)
  })
}
```

Why this works:
- flexible without sacrificing schema clarity
- avoids ad-hoc maps and runtime surprises

## 4) Narrow, useful outputs

```hcl
output "app_subnet_ids" {
  description = "Subnet ids for application workloads"
  value       = values(aws_subnet.app)[*].id
}
```

Why this works:
- downstream modules get exactly what they need
- avoids leaking full provider objects

## 5) Controlled provider pinning

```hcl
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

Why this works:
- controlled upgrade window
- avoids accidental major-version breakage

## 6) Dynamic block with typed variable

```hcl
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

Why this works:
- iterator uses `ingress.value` (named after the block label)
- typed input prevents runtime shape errors
- each dynamic block maps to exactly one nested block type

## 7) Provider alias for multi-region

```hcl
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

Why this works:
- explicit alias keeps region intent clear
- modules receive providers via `providers` map, not implicit inheritance

## 8) `moved` block for safe rename

```hcl
moved {
  from = aws_kms_key.logs
  to   = aws_kms_key.audit
}
```

Why this works:
- keeps state continuity during naming refactors
- prevents unnecessary replacement
