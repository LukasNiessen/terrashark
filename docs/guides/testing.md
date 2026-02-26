# Terraform Testing Matrix

This guide covers choosing testing depth proportional to risk and cost for Terraform and OpenTofu modules.

## Testing Layers

1. **Static checks**: format, validate, lint, security scan
2. **Plan checks**: reviewed execution intent
3. **Native tests**: module-level assertions (`terraform test` / `tofu test`)
4. **Integration tests**: ephemeral apply + live assertions
5. **Terratest**: workflow/system validation in Go for complex scenarios

## Tier A: All Changes (Minimum)

Required for every change:

- `fmt -check`
- `init -backend=false` + `validate`
- Lint + security scan
- Reviewed plan artifact

Use for low-risk isolated updates.

## Tier B: Shared Modules and Medium-Risk Changes

Add on top of Tier A:

- Native test runs for module behavior
- Targeted integration apply tests in ephemeral environment
- Policy checks on plan JSON

**Typical triggers:**
- Shared module changes
- IAM/network updates
- Encryption/data-boundary updates

## Tier C: High-Risk Production Changes

Add on top of Tier A + B:

- Staged rollout (dev -> stage -> prod)
- Rollback rehearsal or documented rollback proof
- Manual owner approvals + security/compliance sign-off
- Post-apply drift detection

**Typical triggers:**
- State backend migration
- Major refactor with address changes
- Foundational platform stack changes

## Native Test Guidance

### When to Use `command = plan`

- Input validation
- Static contract checks
- Argument shape assertions not relying on computed runtime values

### When to Use `command = apply`

- Computed attributes known only after creation
- Assertions over provider-populated fields
- Set/list semantics unresolved in plan stage

### Frequent Pitfalls

- Asserting unknown values in plan mode
- Indexing set-type blocks directly
- Assuming mocked providers equal integration confidence

## Terratest Guidance

Use Terratest when native tests are insufficient:

- Cross-module workflows
- External API verification (health checks, connectivity)
- Failover/disaster-recovery scenarios
- Multi-step lifecycle tests (apply-change-destroy)

### Terratest Test Pyramid

- **Fast**: contract tests (mocked or plan-level)
- **Medium**: environment integration tests (ephemeral)
- **Slow**: limited end-to-end smoke tests for critical paths

### Cost Controls

- Tag tests by class (`unit`, `integration`, `destructive`)
- Parallelize only isolated stacks
- Auto-clean resources with TTL tags
- Run expensive tests nightly and on protected branches

## Test Framework Scaffolding

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

```bash
test-native:
	terraform test

test-terratest:
	go test ./test/terratest -timeout 45m
```

## Example Command Flow

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

## Quick Selection Rules

| Change Type | Testing Tier |
|---|---|
| Tiny tag change in isolated stack | Tier A |
| Module contract change | Tier A + Tier B |
| Refactor with `moved` and shared impact | Tier A + B + targeted Terratest |
| Production identity/network/encryption/state changes | Tier A + B + C + Terratest smoke |

## Done Criteria

Not done until:

- Required tier passes
- Reviewed plan is approved
- Apply path is trusted and auditable
- Evidence artifacts are retained
