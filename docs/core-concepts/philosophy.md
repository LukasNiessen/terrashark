# Terraform Skill Design Philosophy

This page describes the architectural decisions and empirical process behind TerraShark's design.

## Failure-Mode-First Architecture

TerraShark is built around a single insight: **telling an LLM what good Terraform looks like is less effective than telling it how to think about Terraform problems**.

The core `SKILL.md` is not a reference manual. It is a 7-step operational workflow that forces the model to diagnose before it generates. This prevents the most common failure pattern in LLM-assisted IaC: producing syntactically valid but operationally dangerous code.

## Token Efficiency as a Design Constraint

Context window space is a finite resource. Every token spent on skill content is a token unavailable for the user's actual codebase, conversation history, and tool results.

TerraShark is designed for minimal activation cost:

| Metric | TerraShark | Typical Alternative |
|---|---|---|
| Activation cost | ~600 tokens | ~4,400 tokens |
| Reference files | 18 focused files | 6 large files |
| Loaded per query | 1-2 small files | Large reference dumps |

The core `SKILL.md` is 79 lines containing no HCL examples, no inline code blocks, and no tutorial material. It is purely procedural. Depth lives in 18 granular reference files loaded on demand.

## LLM-Aware Guardrails

Every reference file that covers a risk domain includes an **LLM mistake checklist** — a list of specific errors that language models make when generating Terraform code:

- Defaulting to `count` instead of `for_each` for collections
- Omitting `moved` blocks during refactors, causing destroy/create cycles
- Using `sensitive` and assuming the value is safe from state
- Proposing plaintext credential defaults "for demo purposes"
- Recommending CLI-only `terraform import` instead of declarative import blocks

These checklists exist because the model needs to know **what it gets wrong**, not just what is correct. A reference that only shows the right pattern still allows the model to hallucinate the wrong one. A reference that explicitly names the hallucination pattern reduces it.

The **Feature Guard Table** in `coding-standards.md` maps Terraform features to their minimum version and the specific LLM error pattern associated with each, letting the model check feature availability before emitting code.

## Output Contracts

Every TerraShark response includes a structured output contract:

- **Assumptions and version floor** — what the model assumed
- **Selected failure modes** — which risks were diagnosed
- **Chosen remediation and tradeoffs** — what was recommended and why
- **Validation/test plan** — how to verify the output
- **Rollback/recovery notes** — how to undo if something goes wrong

This makes outputs auditable. A reader can check assumptions, verify failure mode coverage, and validate the rollback path before applying anything.

## Reference Granularity

The 18 reference files are organized by concern, not by Terraform concept:

| Category | Files | When Loaded |
|---|---|---|
| **Primary failure modes** | Identity churn, secret exposure, blast radius, CI drift, compliance gates | When that failure mode is diagnosed |
| **Structural guidance** | Structure/state, module architecture, coding standards | When designing or refactoring |
| **Operational references** | Migration playbooks, testing matrix, CI delivery, security/governance, quick ops | For specific operational tasks |
| **Pattern banks** | Good examples, bad examples, neutral examples, do/don't patterns | For review or teaching |
| **Integration and meta** | MCP integration, token balance rationale | When relevant |

Each file is self-contained. No file depends on another file being loaded simultaneously.

## Deep Hierarchy Model

For platform engineering at scale, TerraShark defines a 5-level module hierarchy:

| Level | Role | Scope |
|---|---|---|
| **L0** | Primitives | One resource family, strict contract |
| **L1** | Composites | Capability units built from primitives |
| **L2** | Domain stacks | Bounded business domains |
| **L3** | Environment roots | Env-specific wiring and configuration |
| **L4** | Org orchestration | Account/project vending and shared policy |

Dependencies flow downward only. Each level owns its state boundary and apply lifecycle.

## Content Inclusion Rules

Content enters TerraShark only when at least one condition is met:

1. It materially lowers the probability of destructive or non-compliant changes
2. It prevents common plan/apply surprises
3. It encodes organizational guardrails that general model knowledge cannot infer

Content is excluded when:

1. It is generic Terraform/OpenTofu knowledge with low failure impact
2. It is provider-specific deep design that belongs in project docs
3. It duplicates an existing rule without adding a new decision signal

## The Token Experiment

The content in TerraShark was empirically tested, not designed by intuition.

### Process

1. **Started large** — broader coverage, more examples, more tutorial material
2. **Built automated test suite** — practical Terraform/OpenTofu task patterns
3. **Measured baseline quality** — correctness, safety, completeness, hallucination rate
4. **Stripped iteratively** — removed sections one at a time, re-running the full test suite
5. **Measured quality impact** — if quality dropped, content was restored; if stable, content was permanently removed
6. **Converged** — continued until every remaining section was load-bearing

### What Survived (Models Need Help With)

- Module role boundaries and composition rules
- Migration playbooks (moved blocks, count-to-for_each, imports)
- Native test caveats (set indexing, computed values, mocked providers)
- CI delivery templates (policy checks, artifact integrity, env protection)
- Quick troubleshooting (stuck locks, backend migration, provider auth in CI)

### What Was Removed (Models Already Know)

- Generic HCL syntax tutorials
- Provider-specific resource deep dives
- Broad "best practice" prose without failure-mode framing
- Duplicate explanations of concepts covered by multiple rules

### Core Design Principle

**High signal density.** Every line must earn its token cost by preventing a specific failure mode or encoding knowledge the model demonstrably lacks. Content that merely restates what the model already knows is actively harmful — it burns context window space without improving output quality.
