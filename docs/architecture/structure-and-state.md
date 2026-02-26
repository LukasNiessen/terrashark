# Terraform Structure and State Management

This guide covers how to choose repository shape, environment segmentation, and state boundaries for Terraform projects.

## Boundary Model

Define boundaries by three factors:

1. **Change cadence** — what changes together
2. **Blast radius** — what can fail together
3. **Ownership** — who approves and supports it

If those differ between components, split stacks.

## Root Module Patterns

| Pattern | Scope |
|---|---|
| **service-root** | One business service and its direct dependencies |
| **platform-root** | Shared platform primitives (network, identity, observability) |
| **bootstrap-root** | Backend/state prerequisites and foundational security controls |

Avoid monolithic roots that mix all three.

## Environment Isolation Options

| Option | Best For |
|---|---|
| **Separate root directories** per environment | Default choice, clearest isolation |
| **Workspace-per-environment** with strict policy | When governance is strong and access controls exist |
| **Separate repositories** | Hard regulatory segregation requirements |

Pick one and document why.

## State Backend Baseline

- Remote backend only for collaborative environments
- Lock protection for every apply path
- Encryption at rest and in transit
- Narrow IAM on state and lock stores
- Versioned backup with restore tested at least once

## Cross-Stack Dependencies

Preferred order:

1. **Explicit module outputs** passed in the same root
2. **Published interface artifacts** (preferred at scale)
3. **`terraform_remote_state`** as last-resort coupling

If `terraform_remote_state` is used, version and ownership of the producer stack must be explicit.

## Apply Safety Gates

Minimum gates for any apply:

- `fmt` and `validate`
- Lint and security scan
- Policy checks
- Reviewed plan
- Approved apply

## Change Safety for State Evolution

- Use `moved` blocks for renames and address changes
- For imports, document source of truth and verify idempotency before apply
- For manual state operations, require peer review and rollback notes
