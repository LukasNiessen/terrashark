# Terraform Do and Don't Checklist

A fast reference checklist for safe Terraform and OpenTofu code generation. Use this for quick reviews.

## Identity and Iteration

| Do | Don't |
|---|---|
| Use `for_each` with stable, business-meaningful keys | Use list index as long-lived identity |
| Keep identity keys separate from mutable attributes | Derive identity from a computed attribute |
| Add `moved` blocks when renaming resources or modules | Delete/rename addresses without an explicit migration plan |

## Secrets and Sensitive Data

| Do | Don't |
|---|---|
| Mark secret outputs as `sensitive = true` | Put secrets in `default` values or `.tfvars` committed to VCS |
| Use secret managers and data sources for runtime injection | Echo secrets in provisioner commands |
| Avoid logging sensitive values in `locals` or `output` | Rely on `sensitive` alone to protect state contents |

## State Boundaries and Blast Radius

| Do | Don't |
|---|---|
| Keep production in isolated state backends or workspaces | Mix unrelated systems in a single root state |
| Split large stacks by lifecycle and ownership | Apply directly to production from unreviewed branches |
| Use environment protection and approvals for apply | Use one monolithic stack for all environments |

## Module Contracts

| Do | Don't |
|---|---|
| Expose typed inputs and explicit outputs | Accept untyped `map(any)` for core interfaces |
| Use `optional()` for evolution-friendly contracts | Expose entire provider objects as outputs |
| Validate invariants with `validation` and `precondition` | Push environment-specific policy into primitive modules |

## Providers and Versions

| Do | Don't |
|---|---|
| Pin runtime and providers with bounded constraints | Float provider versions |
| Commit `.terraform.lock.hcl` intentionally | Rely on implicit provider inheritance in multi-region setups |
| Pass provider aliases explicitly to child modules | Mix upgrades with functional changes in the same PR |

## Data Sources and Dependencies

| Do | Don't |
|---|---|
| Use data sources for read-only integration | Use `depends_on` to paper over missing interfaces |
| Model dependencies via input/output wiring | Use data sources for identity fields that can change |
| Keep `depends_on` for real ordering requirements only | Create hidden ordering between unrelated resources |

## CI/CD and Policy

| Do | Don't |
|---|---|
| Separate plan and apply | Allow direct apply from arbitrary branches |
| Keep an auditable reviewed plan artifact | Skip policy checks for production changes |
| Run policy and cost checks on every plan | Delete plan artifacts before approval |

## Testing

| Do | Don't |
|---|---|
| Run `terraform test` / `tofu test` for module-level checks | Rely on plan-only validation for runtime-only attributes |
| Use Terratest for workflow or integration validation | Run destructive tests without isolation and cleanup |
| Tier tests by risk and cost | Treat mocked provider tests as full integration coverage |

## Migration and Refactors

| Do | Don't |
|---|---|
| Include `moved` or `import` strategy in the same change | Rename resources without preserving state identity |
| Run a reviewed plan before any apply | Apply refactors without plan review |
| Document rollback steps for destructive changes | Remove resources without lifecycle transition |
