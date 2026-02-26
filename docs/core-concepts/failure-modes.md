# Five Terraform Failure Modes

TerraShark organizes all its guidance around five explicit failure modes. These are not arbitrary categories — they represent the five most common ways LLM-generated Terraform causes real operational damage.

Every piece of content in the Terraform skill maps to at least one failure mode. Content that does not reduce the probability of any failure mode is excluded.

## 1. Identity Churn

**What it is**: Resource addressing instability that causes unexpected destroy/create cycles during refactors or collection changes.

**Common symptoms**:
- Plan shows broad replace actions after small list edits
- Renaming resources or modules triggers destroy/create
- Refactor from `count` to `for_each` causes churn
- Imported resources keep drifting because addressing is unstable

**Root causes**:
- Index-based identity (`count`) used for long-lived objects
- Keys derived from unstable data (sorted lists, transient IDs)
- Missing `moved` blocks during refactors
- `for_each` keys derived from values unknown at plan time

**LLM-specific risks**: Models default to `count` for every collection, omit `moved` blocks during refactors, and build `for_each` keys from computed IDs not known until apply.

[Full reference: Identity Churn](../failure-modes/identity-churn.md)

## 2. Secret Exposure

**What it is**: Secrets leaking into state files, CI logs, plan output, variable defaults, or artifact storage.

**Common symptoms**:
- Secret values appear in plan output or logs
- Credentials defined in variable defaults
- Sensitive outputs printed in CI
- Generated passwords stored in state unintentionally

**Root causes**:
- Hardcoded defaults in `variables.tf`
- Secret-bearing resources whose values persist in state
- Logging `terraform show` outputs without redaction
- Artifact retention policies keeping plan/state exports too long

**LLM-specific risks**: Models assume `sensitive` alone means "not in state", propose plaintext defaults for demo convenience, and use outputs that expose connection strings in PR comments.

[Full reference: Secret Exposure](../failure-modes/secret-exposure.md)

## 3. Blast Radius

**What it is**: Oversized stacks where a small change can cause widespread, unintended impact across unrelated services.

**Common symptoms**:
- Tiny change triggers a very large plan
- Unrelated services share one state and fail together
- Production and non-production are entangled
- Review/approval ownership is unclear

**Root causes**:
- No ownership boundaries between services
- Monolithic root modules mixing all concerns
- Weak state isolation between environments
- Missing apply governance for shared foundations

**LLM-specific risks**: Models propose one monolithic root for convenience, recommend workspace-only isolation without access controls, and omit rollback paths for shared foundation changes.

[Full reference: Blast Radius](../failure-modes/blast-radius.md)

## 4. CI Drift

**What it is**: Pipeline behavior diverging from local behavior or from reviewed intent, causing unreviewed or inconsistent applies.

**Common symptoms**:
- CI plan differs from local plan unexpectedly
- Apply occurs without using the reviewed plan artifact
- Provider/runtime drift between runs
- Scanner/policy stages skipped on some code paths

**Root causes**:
- Unpinned runtime/provider versions
- Missing or stale lockfile
- Apply job re-running `plan` instead of consuming the reviewed artifact
- Inconsistent credentials/auth between plan and apply

**LLM-specific risks**: Models produce CI pipelines with missing lockfile strategies, apply without saved plan artifacts, skip policy stages despite claiming compliance, and omit branch/environment protection.

[Full reference: CI Drift](../failure-modes/ci-drift.md)

## 5. Compliance Gate Gaps

**What it is**: Missing enforceable controls and evidence artifacts despite referencing compliance frameworks by name.

**Common symptoms**:
- Frameworks mentioned but no enforceable gates exist
- Security best practices confused with compliance evidence
- Missing approval workflows for different risk classes
- No evidence retention for production applies

**Root causes**:
- No preventative controls (policy/validation)
- No detective controls (logging/monitoring)
- No evidence artifacts (plans, approvals, audit records)

**LLM-specific risks**: Models mention framework names without providing enforceable gates, confuse security best practices with compliance evidence, omit risk-class approvals, and ignore data-residency obligations.

[Full reference: Compliance Gate Gaps](../failure-modes/compliance-gates.md)

## How Failure Modes Drive the Terraform Skill

The 7-step workflow uses these failure modes as the diagnostic lens in Step 2. Every reference file, every example, and every checklist in TerraShark traces back to preventing one or more of these five failure modes. This ensures the skill is focused, measurable, and directly actionable.
