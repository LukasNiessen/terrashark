# Structure and State

Use this guide to choose repo shape, environment segmentation, and state boundaries.

## Boundary model

Define boundaries by three factors:

1. Change cadence (what changes together)
2. Blast radius (what can fail together)
3. Ownership (who approves and supports it)

If those differ, split stacks.

## Root module patterns

- `service-root`: one business service and its direct dependencies.
- `platform-root`: shared platform primitives (network, identity, observability).
- `bootstrap-root`: backend/state prerequisites and foundational security controls.

Avoid monolithic roots that mix all three.

## Environment isolation options

1. Separate root directories per environment.
2. Workspace-per-environment with strict policy and access control.
3. Separate repositories when regulatory or ownership requirements demand hard isolation.

Pick one and document why.

## State backend baseline

- remote backend only for collaborative environments
- lock protection for every apply path
- encryption at rest and in transit
- narrow IAM on state and lock stores
- versioned backup and restore test at least once

## Cross-stack dependencies

Preferred order:

1. explicit module outputs passed in the same root
2. published interface artifacts (preferred at scale)
3. `terraform_remote_state` as last-resort coupling

If `terraform_remote_state` is used, version and ownership of the producer stack must be explicit.

## Apply safety gates

Minimum gates:

- `fmt` and `validate`
- lint and security scan
- policy checks
- reviewed plan
- approved apply

## Change safety for state evolution

- Use `moved` blocks for renames and address changes.
- For imports, document source of truth and verify idempotency before apply.
- For manual state operations, require peer review and rollback notes.
