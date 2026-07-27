# Testing Matrix

Use this guide to choose testing depth proportional to risk and cost.

## Testing layers

1. static checks: format, validate, lint, security scan
2. plan checks: reviewed execution intent
3. native tests: module-level assertions (`terraform test` / `tofu test`)
4. integration tests: ephemeral apply + live assertions
5. Terratest: workflow/system validation in Go for complex scenarios

## Tier A (all changes)

Required:
- `fmt -check`
- `init -backend=false` + `validate`
- lint + security scan
- reviewed plan artifact

Use for low-risk isolated updates.

## Tier B (shared modules or medium-risk changes)

Add:
- native test runs for module behavior
- targeted integration apply tests in ephemeral environment
- policy checks on plan JSON

Typical triggers:
- shared module changes
- IAM/network updates
- encryption/data-boundary updates

## Tier C (high-risk production changes)

Add:
- staged rollout (dev -> stage -> prod)
- rollback rehearsal or documented rollback proof
- manual owner approvals + security/compliance sign-off where needed
- post-apply drift detection

Typical triggers:
- state backend migration
- major refactor with address changes
- foundational platform stack changes

## Native test guidance

### When to use `command = plan`

Use for:
- input validation
- static contract checks
- argument shape assertions not relying on computed runtime values

### When to use `command = apply`

Use for:
- computed attributes known only after creation
- assertions over provider-populated fields
- set/list semantics that are unresolved in plan stage

### Frequent pitfalls

- asserting unknown values in plan mode
- indexing set-type blocks directly
- assuming mocked providers equal integration confidence

## Terratest guidance

Use Terratest when native tests are insufficient:
- cross-module workflows
- external API verification (health checks, connectivity)
- failover/disaster-recovery scenarios
- multi-step lifecycle tests (apply-change-destroy)

### Terratest test pyramid

- fast contract tests (mocked or plan-level)
- environment integration tests (ephemeral)
- limited end-to-end smoke tests for critical paths

### Terratest cost controls

- tag tests by class (`unit`, `integration`, `destructive`)
- parallelize only isolated stacks
- auto-clean resources with TTL tags
- run expensive tests nightly and on protected branches

## Test framework scaffolding

Use a thin, consistent structure so tests are easy to run in CI:

```
.
  test/
    terratest/
      go.mod
      helpers/
      examples/
      network_test.go
    native/
      main.tftest.hcl
  Makefile
```

Minimal Makefile targets:

```makefile
test-native:
\tterraform test

test-terratest:
\tgo test ./test/terratest -timeout 45m
```

## Example command flow

```bash
terraform fmt -check
terraform init -backend=false
terraform validate
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
conftest test plan.json --policy policy/
terraform test
```

Terratest stage:

```bash
go test ./test -run TestCriticalPath -timeout 45m
```

## Selection quick rules

- tiny tag change in isolated stack: Tier A
- module contract change: Tier A + Tier B
- refactor with `moved` and shared impact: Tier A + Tier B + targeted Terratest
- production identity/network/encryption/state changes: Tier A + Tier B + Tier C + Terratest smoke

## Done criteria

Not done until:
- required tier passes
- reviewed plan is approved
- apply path is trusted and auditable
- evidence artifacts are retained
