# Terraform Security and Governance

This guide covers security controls for Terraform and OpenTofu delivery pipelines. For framework-specific compliance mappings and evidence gates, see [Compliance Gates](../failure-modes/compliance-gates.md).

## Identity Controls

- Least privilege for CI identities
- Separate `plan` and `apply` roles where possible
- Short-lived credentials via workload identity federation
- Deny direct human write access to production backends

## Secret Controls

- Prohibit plaintext secret defaults in code
- Source sensitive values from managed secret stores
- Mark secret variables and outputs as sensitive
- Sanitize logs/artifacts and restrict access

## Supply-Chain Controls

- Pin provider/module versions with bounded constraints
- Commit lockfile and review lockfile diffs
- Verify action/container versions in CI workflows

## Policy Layers

Use layered controls, not single-tool reliance:

| Layer | Tool/Approach | Purpose |
|---|---|---|
| **Static scanning** | `tfsec`, `checkov`, equivalent | Catch common misconfigurations early |
| **Plan-policy checks** | Sentinel, OPA, Conftest | Enforce organizational policies on plan output |
| **Approval gates** | By risk class | Human oversight for high-impact changes |

## High-Impact Change Controls

Require elevated approval for:

- IAM privilege expansion
- Network exposure/public ingress changes
- Encryption disablement/key-policy weakening
- Backend/state changes
- Production replacement/destruction actions

## Minimal OPA Example

```javascript
package main

deny[msg] {
  r := input.resource_changes[_]
  r.type == "aws_security_group_rule"
  r.change.after.cidr_blocks[_] == "0.0.0.0/0"
  r.change.after.from_port == 22
  msg := sprintf("Public SSH is not allowed: %s", [r.address])
}
```

## Operational Governance

- Serialize applies for shared foundations
- Require explicit opt-in for destroy
- Keep break-glass runbook and test it periodically
- Retain run metadata and policy outputs for auditability
