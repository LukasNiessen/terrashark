# Philosophy

This document describes TerraShark's design strategy, architectural decisions, and the empirical process behind its content.

## Failure-Mode-First Architecture

TerraShark is built around a single insight: telling an LLM *what good Terraform looks like* is less effective than telling it *how to think about Terraform problems*.

The core SKILL.md is not a reference manual. It is a 7-step operational workflow:

1. **Capture execution context** -- runtime, version, providers, backend, execution path, criticality
2. **Diagnose likely failure modes** -- identity churn, secret exposure, blast radius, CI drift, compliance gate gaps
3. **Load only relevant references** -- pull targeted guidance, not everything
4. **Propose fix path with risk controls** -- why this works, what could go wrong, guardrails
5. **Generate implementation artifacts** -- HCL, migration blocks, CI updates, compliance controls
6. **Validate before finalize** -- command sequence tailored to runtime and risk tier
7. **Output contract** -- assumptions, tradeoffs, validation plan, rollback notes

The model diagnoses before it generates. This prevents the most common failure pattern in LLM-assisted IaC: producing syntactically valid but operationally dangerous code.

## Token Efficiency

Context window space is a finite resource. Every token spent on skill content is a token unavailable for the user's actual codebase, conversation history, and tool results.

TerraShark is designed for minimal activation cost. The core SKILL.md is 79 lines (~600 tokens). It contains no HCL examples, no inline code blocks, no tutorial material. It is purely procedural: a workflow the model follows.

Depth lives in 18 granular reference files. The model loads only the 1-2 files relevant to the diagnosed failure mode. A query about secret handling never loads the CI delivery patterns. A query about module architecture never loads the compliance gates.

This granularity matters. A single large reference file forces the model to process thousands of irrelevant tokens. 18 small files let it load precisely what it needs.

## LLM-Aware Guardrails

Every reference file that covers a risk domain includes an **LLM mistake checklist** -- a list of specific errors that language models make when generating Terraform code. Examples:

- Defaulting to `count` instead of `for_each` for collections
- Omitting `moved` blocks during refactors, causing destroy/create cycles
- Using `sensitive` and assuming the value is safe from state
- Proposing plaintext credential defaults "for demo purposes"
- Recommending CLI-only `terraform import` instead of declarative import blocks

These checklists exist because the model needs to know *what it gets wrong*, not just *what is correct*. A reference that only shows the right pattern still allows the model to hallucinate the wrong one. A reference that explicitly names the hallucination pattern reduces it.

The **Feature guard table** in `coding-standards.md` takes this further: it maps Terraform features to their minimum version and the specific LLM error pattern associated with each. This lets the model check whether a feature is available for the target runtime before emitting it.

## Output Contracts

Every TerraShark response includes a structured output contract:

- **Assumptions and version floor** -- what the model assumed about the environment
- **Selected failure modes** -- which risks were diagnosed
- **Chosen remediation and tradeoffs** -- what was recommended and what was traded off
- **Validation/test plan** -- how to verify the output
- **Rollback/recovery notes** -- how to undo if something goes wrong

This makes outputs auditable. A reader can check whether the model's assumptions were correct, whether the right failure modes were identified, and whether the rollback path is viable -- before applying anything.

## Reference Granularity

The 18 reference files are organized by concern, not by Terraform concept:

**Primary failure modes** (loaded when the failure mode is diagnosed):
- Identity churn, secret exposure, blast radius, CI drift, compliance gates

**Structural guidance** (loaded when designing or refactoring):
- Structure and state, module architecture, coding standards

**Operational references** (loaded for specific tasks):
- Migration playbooks, testing matrix, CI delivery patterns, security and governance, quick ops

**Pattern banks** (loaded for review or teaching):
- Good examples, bad examples, neutral examples, do/don't patterns

**Integration and meta**:
- MCP integration, token balance rationale

Each file is self-contained. No file depends on another file being loaded simultaneously.

## Failure Modes as First-Class Concepts

TerraShark names five failure modes explicitly:

1. **Identity churn** -- resource addressing instability, refactor breakage, index-based identity
2. **Secret exposure** -- secrets leaking through state, logs, defaults, or artifacts
3. **Blast radius** -- oversized stacks, weak boundaries, unsafe production applies
4. **CI drift** -- version mismatches, unreviewed applies, missing plan artifacts
5. **Compliance gate gaps** -- missing policies, approvals, audit controls, evidence

These are not arbitrary categories. They represent the five most common ways LLM-generated Terraform causes real damage. Every piece of content in the skill maps to at least one of these failure modes. Content that does not reduce the probability of any failure mode is excluded.

## Deep Hierarchy Model

For platform engineering at scale, TerraShark defines a 5-level module hierarchy:

- **L0 primitives** -- one resource family, strict contract
- **L1 composites** -- capability units built from primitives
- **L2 domain stacks** -- bounded business domains (payments, identity, observability)
- **L3 environment roots** -- env-specific wiring and configuration
- **L4 org orchestration** -- account/project vending and shared policy baselines

Dependencies flow downward only. No lateral imports across the same level without an explicit interface contract. Each level owns its state boundary and apply lifecycle.

## Content Inclusion Rules

Content enters TerraShark only when at least one condition is met:

1. It materially lowers the probability of destructive or non-compliant changes
2. It prevents common plan/apply surprises (identity churn, drift, unsafe upgrades)
3. It encodes organizational guardrails that general model knowledge cannot infer

Content is excluded when:

1. It is generic Terraform/OpenTofu knowledge with low failure impact
2. It is provider-specific deep design that belongs in project docs
3. It duplicates an existing rule without adding a new decision signal

If repeated failure patterns emerge, targeted lines are added for that specific failure mode instead of broad expansion.

---

## Token Experiment

The content in TerraShark was not designed by intuition. It was empirically tested.

### Process

1. **Started large.** The initial reference content was significantly larger -- broader coverage, more examples, more inline explanations, more tutorial-style material.

2. **Built an automated test suite.** A large set of practical Terraform/OpenTofu task patterns was assembled: module creation, refactoring, CI pipeline setup, migration, security review, compliance checks, and others.

3. **Measured baseline quality.** The full-size skill was run against the test suite. Output quality was scored across correctness, safety, completeness, and hallucination rate.

4. **Stripped content iteratively.** Sections were removed one at a time. After each removal, the full test suite was re-run.

5. **Measured quality impact.** For each removal:
   - If quality dropped: the content was restored. It carried signal the model needed.
   - If quality stayed stable: the content was permanently removed. It was redundant with the model's existing knowledge.

6. **Converged on current size.** The process continued until every remaining section was load-bearing -- removing any further content caused measurable quality degradation.

### What Survived

The content that survived the stripping process reveals what models actually need help with versus what they already know:

- **Module role boundaries and composition rules** -- models struggle with when to split modules, how deep hierarchies should work, and where business logic belongs
- **Migration playbooks** -- models frequently omit `moved` blocks, mishandle `count`-to-`for_each` transitions, and skip import strategies
- **Native test caveats** -- models incorrectly index set-type blocks, assert computed values in plan mode, and treat mocked providers as integration coverage
- **CI delivery templates** -- models produce CI pipelines that skip policy checks, re-run plan during apply instead of using artifacts, and lack environment protection
- **Quick troubleshooting** -- models struggle with operational failures (stuck locks, backend migration, provider auth in CI) that are not well-covered in training data

### What Was Removed

Content that did not affect output quality when removed:

- Generic HCL syntax tutorials (models know this)
- Provider-specific resource deep dives (better served by MCP or docs)
- Broad "best practice" prose without failure-mode framing (low signal density)
- Duplicate explanations of concepts covered by multiple rules

### Design Principle

The token experiment established a core design principle: **high signal density**. Every line in TerraShark must earn its token cost by preventing a specific failure mode or encoding knowledge the model demonstrably lacks. Content that merely restates what the model already knows is actively harmful -- it burns context window space without improving output quality.
