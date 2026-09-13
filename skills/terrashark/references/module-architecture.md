# Module Architecture

Use this guide when designing reusable modules and composition layers.

## Module roles

- `primitive module`: wraps one resource family with strict interface.
- `composite module`: assembles multiple primitives for a deployable capability.
- `root composition`: injects environment values and wiring only.

Keep business policy out of primitives when it is environment-specific.

## Contract design

A good module contract has:

- strongly typed inputs
- defaults only for safe/common behavior
- explicit outputs for consumers
- preconditions for invariants

Bad contract smell:

- many loosely typed maps
- opaque passthrough variables
- outputs that mirror entire provider objects

## Suggested file layout

- `main.tf`: resources and module calls
- `variables.tf`: typed input contract and validation
- `outputs.tf`: explicit consumer interface
- `versions.tf`: runtime and provider constraints
- `locals.tf`: computed values, naming, shared labels
- `README.md`: short usage and contract notes (if repository policy requires docs)

## Composition rules

- pass only required values into child modules
- avoid circular dependencies and hidden ordering
- prefer data flow via input/output over broad `depends_on`
- keep module count manageable; over-fragmentation hurts maintainability

## Deep hierarchy model

Use this when a platform grows beyond a single composition layer.

Hierarchy levels:
- L0 primitives: one resource family, strict contract
- L1 composites: capability units built from primitives
- L2 domain stacks: bounded business domains (payments, identity, observability)
- L3 environment roots: env-specific wiring and configuration
- L4 org orchestration: account/project vending and shared policy baselines

Composition rules:
- dependencies flow downward only (L4 -> L3 -> L2 -> L1 -> L0)
- no lateral imports across same level without an explicit interface contract
- cross-state data flow is via explicit outputs or approved remote state access
- each level owns its state boundary and apply lifecycle
- environment roots should not embed business logic; keep it in L2/L1

Decision aid:
- add a new level only if ownership, lifecycle, or blast radius requires it

## Module release discipline

- tag module versions
- use bounded version constraints in consumers
- run compatibility tests before raising lower bounds

## Decision checkpoint

Create a new module only when one is true:

- reused across 2+ stacks
- ownership differs from current module
- lifecycle differs significantly
- change blast radius needs isolation
