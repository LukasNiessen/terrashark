# Terraform Coding Standards

This guide covers implementation-level consistency for Terraform and OpenTofu code generation, including naming, typing, iteration, and version discipline.

## Naming and Metadata

- Use names that reflect business purpose (`payments_api`, `audit_kms`), not temporary implementation details
- Reserve `this` for real singleton resources only
- Centralize tags/labels in `locals` and apply consistently
- Normalize provider-constrained identifiers before use

### Identifier Normalization Pattern

Some resources reject characters valid in domains or service names (e.g., `.` in RDS identifiers):

```hcl
locals {
  raw_name        = "${var.domain}-prod"
  normalized_name = regexreplace(lower(local.raw_name), "[^a-z0-9-]", "-")
}
```

Then use `local.normalized_name` for fields like `identifier` and `final_snapshot_identifier`.

## Resource Block Ordering

Preferred order inside resource blocks:

1. Identity/core arguments
2. Behavior/config arguments
3. Nested blocks
4. Tags/labels
5. Lifecycle/meta-arguments

This keeps diffs predictable and reviewable.

## Variable Contract Style

Variable attribute order:

1. `description`
2. `type`
3. `default` (if used)
4. `nullable`
5. `sensitive`
6. `validation`

Prefer explicit objects with `optional()` over untyped maps for long-lived module contracts.

## Iteration and Identity

| Pattern | Use When |
|---|---|
| `count` | Optional singleton toggles (`0` or `1`) |
| `for_each` | Any collection with stable logical identities |

Never use list index as long-lived identity key.

## Set-Type Handling

Rules to avoid ordering bugs and test failures:

- Never index sets directly; convert with `sort(tolist(...))` when order matters
- Use `for_each` with `toset(...)` only when identity is the value itself
- For stable diff output, transform sets to sorted lists in outputs
- In tests, prefer `contains()` or set equality over positional assertions

## Outputs

- Expose only stable interfaces needed by consumers
- Mark secret-bearing outputs as `sensitive = true`
- Avoid dumping entire provider objects

## Version and Lock Discipline

- Set runtime floor in `required_version`
- Bound provider and module versions
- Commit lockfile changes intentionally
- Keep upgrade PRs separate from functional changes where possible

## Terraform Feature Guard Table

Use this table when deciding what to emit for a given runtime floor. Maps features to their minimum version and the specific LLM error pattern for each.

| Feature | Min Version | LLM Error Pattern |
|---|---|---|
| `moved` blocks | 1.1+ | Omitted during refactor, causing destroy/create |
| `for_each` over `count` | 0.12+ | Model defaults to `count` for every collection |
| `write_only` arguments | 1.11+ | Model uses `sensitive` and assumes state is safe |
| `optional()` defaults | 1.3+ | Model emits wrapper variables and loose maps |
| Cross-variable validation | 1.9+ | Model pushes checks into postconditions only |
| Declarative `import` blocks | 1.5+ | Model recommends ad-hoc CLI import only |
| `check` blocks | 1.5+ | Model ignores runtime assertions entirely |
| `removed` blocks | 1.7+ | Model deletes resources with no lifecycle transition |
| Provider-defined functions | 1.8+ | Model overuses data sources for transformations |

If target runtime is below a feature floor, emit fallback guidance explicitly.

## Review Checklist

- Typed inputs and validations present
- Iteration model chosen for address stability
- No plaintext secret defaults
- Version constraints and lockfile strategy are explicit
- Migration-sensitive changes include `moved`/`import` plan
