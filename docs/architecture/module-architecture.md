# Terraform Module Architecture

This guide covers designing reusable Terraform modules, composition layers, and the deep hierarchy model for platform engineering at scale.

## Module Roles

| Role | Responsibility |
|---|---|
| **Primitive module** | Wraps one resource family with strict interface |
| **Composite module** | Assembles multiple primitives for a deployable capability |
| **Root composition** | Injects environment values and wiring only |

Keep business policy out of primitives when it is environment-specific.

## Contract Design

A good module contract has:

- Strongly typed inputs
- Defaults only for safe/common behavior
- Explicit outputs for consumers
- Preconditions for invariants

**Bad contract smells:**
- Many loosely typed maps
- Opaque passthrough variables
- Outputs that mirror entire provider objects

## Suggested File Layout

| File | Purpose |
|---|---|
| `main.tf` | Resources and module calls |
| `variables.tf` | Typed input contract and validation |
| `outputs.tf` | Explicit consumer interface |
| `versions.tf` | Runtime and provider constraints |
| `locals.tf` | Computed values, naming, shared labels |

## Composition Rules

- Pass only required values into child modules
- Avoid circular dependencies and hidden ordering
- Prefer data flow via input/output over broad `depends_on`
- Keep module count manageable; over-fragmentation hurts maintainability

## Deep Hierarchy Model

For platform engineering at scale, use a 5-level module hierarchy:

```
L4: Org Orchestration
  └── L3: Environment Roots
        └── L2: Domain Stacks
              └── L1: Composites
                    └── L0: Primitives
```

| Level | Role | Examples |
|---|---|---|
| **L0 Primitives** | One resource family, strict contract | VPC, IAM role, S3 bucket |
| **L1 Composites** | Capability units built from primitives | Networking stack, compute cluster |
| **L2 Domain stacks** | Bounded business domains | Payments, identity, observability |
| **L3 Environment roots** | Env-specific wiring and configuration | dev, staging, production |
| **L4 Org orchestration** | Account/project vending and shared policy | Organization policies, account factory |

### Composition Rules

- Dependencies flow downward only (L4 -> L3 -> L2 -> L1 -> L0)
- No lateral imports across the same level without an explicit interface contract
- Cross-state data flow is via explicit outputs or approved remote state access
- Each level owns its state boundary and apply lifecycle
- Environment roots should not embed business logic; keep it in L2/L1

### Decision Aid

Add a new level only if ownership, lifecycle, or blast radius requires it.

## Module Release Discipline

- Tag module versions
- Use bounded version constraints in consumers
- Run compatibility tests before raising lower bounds

## When to Create a New Module

Create a new module only when at least one is true:

- Reused across 2+ stacks
- Ownership differs from current module
- Lifecycle differs significantly
- Change blast radius needs isolation
