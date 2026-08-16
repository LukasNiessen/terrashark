# Trusted Community / Vendor Modules

**Load this reference when detected:** provider `aws`, `azurerm`, `google`, `oci`, or `ibm`.

## Detection signals

- required provider names `aws`, `azurerm`, `google`, `oci`, or `ibm`
- requests to create common cloud primitives such as network, Kubernetes, database, object storage, load balancer, IAM, or security-group resources
- user asks for a reusable module and has not explicitly requested raw provider resources

## Why this matters

Raw `resource` blocks are the largest hallucination surface for LLMs — attribute names, defaults, and iteration shapes are where models slip. A pinned, verified registry module replaces hundreds of hand-rolled lines with a version-locked interface already tested across many production stacks.

Prefer a trusted module unless the user explicitly asked for raw resources, or no mature module covers the target service.

## Canonical sources

### AWS — `terraform-aws-modules`

- Registry namespace: `terraform-aws-modules`
- Common modules: `vpc/aws`, `eks/aws`, `rds/aws`, `s3-bucket/aws`, `lambda/aws`, `iam/aws`, `security-group/aws`, `alb/aws`, `cloudfront/aws`, `ecs/aws`
- Status: de-facto community standard, very active

### Azure — Azure Verified Modules (AVM)

- Registry namespace: `Azure`
- Resource modules: `Azure/avm-res-<service>-<resource>/azurerm`
- Pattern modules: `Azure/avm-ptn-<pattern>/azurerm`
- Examples: `avm-res-network-virtualnetwork`, `avm-res-storage-storageaccount`, `avm-res-containerservice-managedcluster` (AKS), `avm-res-keyvault-vault`
- Legacy `Azure/terraform-azurerm-*` modules still work but AVM is the strategic path
- Status: Microsoft official program, prefer for new work

### GCP — Cloud Foundation Toolkit

- Registry namespace: `terraform-google-modules`
- Common modules: `network/google`, `kubernetes-engine/google` (GKE), `project-factory/google`, `sql-db/google`, `cloud-storage/google`, `iam/google`
- Status: Google-endorsed, mature

### Oracle Cloud — `oracle-terraform-modules`

- Registry namespace: `oracle-terraform-modules`
- Common modules: `vcn/oci`, `oke/oci`, `database/oci`, `bastion/oci`
- Status: vendor-maintained, smaller catalog — fall back to raw `oci_*` resources when coverage is missing

### IBM Cloud — `terraform-ibm-modules`

- Registry namespace: `terraform-ibm-modules`
- Coverage: VPC, IKS/ROKS, Cloud Object Storage, IAM, Key Protect, Event Streams
- Status: IBM-maintained "Deployable Architectures"

## Rules

### Pin versions exactly in production

Do:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.13.0"
}
```

Don't float with `~>` for production stacks — a minor bump can change generated resource addresses and trigger destroy/create. `~>` is only acceptable for throwaway dev.

### Verify the source namespace

- Only pull from the official namespaces listed above. Typosquatted forks exist.
- Do not use a git SHA from an unverified fork. If a patch is needed, open a PR upstream or maintain an internal fork behind explicit review.

### Don't wrap trivially

Anti-pattern: a local `modules/vpc/main.tf` that only re-exposes every variable of `terraform-aws-modules/vpc/aws`. Adds maintenance burden with no abstraction gain.

Wrap only to:

- enforce org-specific defaults (tags, encryption, CIDR rules)
- compose multiple modules into a higher-level pattern
- hide cross-cutting policy from consumers

### Know when to skip the module

Prefer raw resources when:

- no mature module covers the service (check Registry downloads and last-updated date)
- the resource is trivial (a single SSM parameter, a lone DNS record)
- the module imposes opinions that would be fully overridden anyway

## Generation default

When a trusted module exists for the requested resource and the user has not asked for raw HCL:

- default to the registry module
- pin an exact version
- state the chosen source and version in the output contract's assumptions so the user can redirect

## Validation checks

- verify the module source namespace in the Terraform Registry or the vendor's official module catalog
- inspect recent release activity before recommending the module for production
- pin an exact version and record it in the output assumptions
- check the module interface instead of inventing input names from memory
- confirm generated outputs expose only the consumer contract, not full provider objects

## LLM mistake checklist

- inventing module names that do not exist in the trusted namespace
- using a mature module source but hallucinating its variable names
- floating production module versions with `~>` or no `version`
- wrapping a trusted module only to re-expose every input unchanged
- defaulting to raw resources when a mature trusted module covers the request
- using an unverified fork, typo namespace, or random Git source without review
