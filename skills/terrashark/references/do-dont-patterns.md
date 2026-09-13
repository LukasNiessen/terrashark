# Do and Don't Patterns

Use this guide as a fast checklist for safe Terraform/OpenTofu output.

## Identity and iteration

Do:
- use `for_each` with stable, business-meaningful keys
- keep identity keys separate from mutable attributes
- add `moved` blocks when renaming resources or module addresses

Don't:
- use list index as long-lived identity
- derive identity from a computed attribute
- delete/rename addresses without an explicit migration plan

## Secrets and sensitive data

Do:
- mark secret outputs as `sensitive = true`
- use secret managers and data sources for runtime injection
- avoid logging sensitive values in `locals` or `output`

Don't:
- put secrets in `default` values or `.tfvars` committed to VCS
- echo secrets in provisioner commands
- rely on `sensitive` alone to protect state contents

## State boundaries and blast radius

Do:
- keep production in isolated state backends or workspaces
- split large stacks by lifecycle and ownership
- use environment protection and approvals for apply

Don't:
- mix unrelated systems in a single root state
- apply directly to production from unreviewed branches
- use one monolithic stack for all environments

## Module contracts

Do:
- expose typed inputs and explicit outputs
- use `optional()` for evolution-friendly contracts
- validate invariants with `validation` and `precondition`

Don't:
- accept untyped `map(any)` for core interfaces
- expose entire provider objects as outputs
- push environment-specific policy into primitive modules

## Providers and versions

Do:
- pin runtime and providers with bounded constraints
- commit `.terraform.lock.hcl` intentionally
- pass provider aliases explicitly to child modules

Don't:
- float provider versions
- rely on implicit provider inheritance in multi-region setups
- mix upgrades with functional changes in the same PR

## Data sources and dependencies

Do:
- use data sources for read-only integration
- model dependencies via input/output wiring
- keep `depends_on` for real ordering requirements only

Don't:
- use `depends_on` to paper over missing interfaces
- use data sources for identity fields that can change
- create hidden ordering between unrelated resources

## CI/CD and policy

Do:
- separate plan and apply
- keep an auditable reviewed plan artifact
- run policy and cost checks on every plan

Don't:
- allow direct apply from arbitrary branches
- skip policy checks for production changes
- delete plan artifacts before approval

## Testing

Do:
- run `terraform test` / `tofu test` for module-level checks
- use Terratest for workflow or integration validation
- tier tests by risk and cost

Don't:
- rely on plan-only validation for runtime-only attributes
- run destructive tests without isolation and cleanup
- treat mocked provider tests as full integration coverage

## Migration and refactors

Do:
- include `moved` or `import` strategy in the same change
- run a reviewed plan before any apply
- document rollback steps for destructive changes

Don't:
- rename resources without preserving state identity
- apply refactors without plan review
- remove resources without lifecycle transition
