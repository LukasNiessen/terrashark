# The 7-Step Terraform Skill Workflow

The core of TerraShark is a 7-step operational workflow defined in `SKILL.md`. Unlike traditional reference manuals that dump information and hope the AI uses it correctly, this workflow forces the AI to **diagnose before generating** — the single most important pattern for preventing Terraform hallucinations.

## Overview

```
Capture Context → Diagnose Failure Modes → Load References → Propose Fix → Generate Artifacts → Validate → Output Contract
```

## Step 1: Capture Execution Context

Before writing any code, the Terraform skill records:

- **Runtime**: `terraform` or `tofu` and exact version
- **Providers**: which cloud providers and their versions
- **Target platform**: AWS, Azure, GCP, etc.
- **State backend**: S3, GCS, Azure Blob, HCP Terraform, etc.
- **Execution path**: local CLI, CI, HCP Terraform/TFE, Atlantis
- **Environment criticality**: dev, shared, or production

If any of these are unknown, the skill states assumptions explicitly in the output contract.

**Why this matters**: A module targeting Terraform 1.1 cannot use `import` blocks (requires 1.5+). A CI pipeline needs different patterns than local CLI. Production requires approval gates that dev does not.

## Step 2: Diagnose Likely Failure Modes

The skill selects one or more failure modes based on the user's intent and risk level:

| Failure Mode | When Diagnosed |
|---|---|
| **Identity churn** | Refactors, collection changes, count/for_each decisions |
| **Secret exposure** | Credential handling, state access, CI artifact management |
| **Blast radius** | Stack design, environment isolation, state boundaries |
| **CI drift** | Pipeline setup, version management, plan/apply separation |
| **Compliance gate gaps** | Policy setup, framework requirements, approval workflows |

This step is what makes TerraShark fundamentally different from static reference skills. The AI must identify **what could go wrong** before it starts generating code.

## Step 3: Load Only Relevant References

Based on the diagnosed failure modes, the skill loads targeted reference files:

**Primary references** (one per failure mode):
- `references/identity-churn.md`
- `references/secret-exposure.md`
- `references/blast-radius.md`
- `references/ci-drift.md`
- `references/compliance-gates.md`

**Supplemental references** (loaded only when needed):
- Testing, CI delivery, module architecture, coding standards, migration playbooks, security governance, quick ops, examples, and more

This granularity means a query about secret handling never loads CI delivery patterns, and a query about module architecture never loads compliance gates. Only 1-2 small, focused files are loaded per query instead of one massive dump.

## Step 4: Propose Fix Path with Explicit Risk Controls

For each proposed fix, the skill includes:

- **Why this addresses the failure mode** — direct mapping from diagnosis to solution
- **What could still go wrong** — honest risk assessment
- **Guardrails** — tests, approvals, and rollback steps to mitigate remaining risk

This forces transparency. The AI cannot silently generate code that might cause damage without disclosing the risks.

## Step 5: Generate Implementation Artifacts

When applicable, the output includes:

- **HCL changes**: typed variables, stable keys, bounded version constraints
- **Migration blocks**: `moved` blocks, `import` strategy
- **CI pipeline updates**: plan/apply separation, artifact management, policy checks
- **Compliance controls**: approval gates, policy rules, evidence paths

## Step 6: Validate Before Finalize

The skill provides a command sequence tailored to the runtime and risk tier:

```bash
terraform fmt -check
terraform validate
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
```

The skill **never recommends direct production apply** without a reviewed plan and approval gate.

## Step 7: Output Contract

Every response includes a structured contract:

| Section | Content |
|---|---|
| **Assumptions and version floor** | What was assumed about the environment |
| **Selected failure modes** | Which risks were diagnosed |
| **Chosen remediation and tradeoffs** | What was recommended and what was traded off |
| **Validation/test plan** | How to verify the output |
| **Rollback/recovery notes** | How to undo if something goes wrong |

This makes every output **auditable**. A reviewer can check assumptions, verify failure mode coverage, and validate the rollback path — all before applying anything.

## Why This Architecture Works

The 7-step workflow prevents the most common failure pattern in LLM-assisted infrastructure-as-code: **producing syntactically valid but operationally dangerous code**.

A static reference manual tells the AI what good Terraform looks like. The 7-step workflow tells the AI **how to think about Terraform problems**. This is the difference between giving someone a cookbook and giving them a diagnostic checklist.
