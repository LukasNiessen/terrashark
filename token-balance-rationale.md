# 🧠 Token Balance Rationale

## ✅ Decision

Keep this skill compact, but not minimal to the point of risk.

## 📉 Why not add much more?

- LLMs already know generic IaC syntax and common Terraform terms.
- Repeating broad tutorials increases token cost with limited quality gain.
- Large reference files are often loaded unnecessarily, which reduces context available for the actual task.

## 🧪 How we found the balance (real process)

We did not guess this.

- We started with significantly larger reference content.
- We ran a large automated test suite across practical Terraform/OpenTofu task patterns.
- We stripped sections step by step and re-ran tests.
- The moment quality degraded, we restored that content.
- If quality did not degrade, that content stayed removed.

That loop gave us a clear boundary: keep only what materially protects output quality.

## ⚠️ Why not keep it even smaller?

Some topics are high-impact and easy to get wrong if underspecified. These stay explicit:
- state boundaries and backend safety
- version pinning and upgrade discipline
- secret handling and least privilege
- CI gates and approval flow
- risk-based testing depth

## 🧭 Inclusion rule used in this repo

Add content only if at least one is true:
1. It materially lowers probability of destructive or non-compliant changes.
2. It prevents common plan/apply surprises (identity churn, drift blind spots, unsafe upgrades).
3. It encodes organizational guardrails that general model knowledge cannot infer.

Exclude content when:
1. It is generic Terraform/OpenTofu knowledge with low failure impact.
2. It is provider-specific deep design that belongs in project docs, not in a shared skill.
3. It duplicates an existing rule without adding a new decision signal.

## 🚀 Quality guardrail

This skill aims for high signal density:
- short `SKILL.md` for execution flow
- references only for non-obvious, failure-prone decisions
- examples focused on behavior and tradeoffs, not cookbook volume

If future use shows repeated failure patterns, add targeted lines for that failure mode instead of broad expansion.

## 📌 What we intentionally added back

After testing and trimming cycles, these sections stayed because quality dropped without them:
- module role boundaries and composition rules
- migration playbooks (`moved`, import-first adoption, upgrade flow)
- native testing caveats (plan vs apply, unknown values, set semantics)
- CI delivery templates and approval gate structure
- quick troubleshooting for common failure modes
