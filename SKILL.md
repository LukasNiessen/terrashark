---
name: terrashark
description: "Prevent Terraform/OpenTofu hallucinations by diagnosing and fixing failure modes: identity churn, secret exposure, blast-radius mistakes, CI drift, and compliance gate gaps. Use when generating, reviewing, refactoring, or migrating IaC and when building delivery/testing pipelines."
---

# Terrashark: Failure-Mode Workflow for Terraform/OpenTofu

Run this workflow top to bottom.

## 1) Capture execution context

Record before writing code:
- runtime (`terraform` or `tofu`) and exact version
- provider(s), target platform, and state backend
- execution path (local CLI, CI, HCP Terraform/TFE, Atlantis)
- environment criticality (dev/shared/prod)

If unknown, state assumptions explicitly.

## 2) Diagnose likely failure mode(s)

Select one or more based on user intent and risk:
- identity churn: resource addressing instability, refactor breakage
- secret exposure: secrets in state, logs, defaults, artifacts
- blast radius: oversized stacks, weak boundaries, unsafe applies
- CI drift: version mismatch, unreviewed applies, missing artifacts
- compliance gate gaps: missing policies/approvals/audit controls

## 3) Load only the relevant reference file(s)

Primary references:
- `references/identity-churn.md`
- `references/secret-exposure.md`
- `references/blast-radius.md`
- `references/ci-drift.md`
- `references/compliance-gates.md`

Supplemental references (only when needed):
- `references/testing-matrix.md`
- `references/quick-ops.md`
- `references/examples-good.md`
- `references/examples-bad.md`
- `references/examples-neutral.md`
- `references/coding-standards.md`
- `references/module-architecture.md`
- `references/ci-delivery-patterns.md`
- `references/security-and-governance.md`
- `references/do-dont-patterns.md`
- `references/mcp-integration.md`

## 4) Propose fix path with explicit risk controls

For each fix, include:
- why this addresses the failure mode
- what could still go wrong
- guardrails (tests, approvals, rollback)

## 5) Generate implementation artifacts

When applicable, output:
- HCL changes (typed vars, stable keys, bounded versions)
- migration blocks (`moved`, import strategy)
- CI pipeline updates (plan/apply separation, artifacts, policy checks)
- compliance controls (approvals, policy rules, evidence paths)

## 6) Validate before finalize

Always provide command sequence tailored to runtime and risk tier.
Never recommend direct production apply without reviewed plan and approval.

## 7) Output contract

Return:
- assumptions and version floor
- selected failure mode(s)
- chosen remediation and tradeoffs
- validation/test plan
- rollback/recovery notes for destructive-impact changes
