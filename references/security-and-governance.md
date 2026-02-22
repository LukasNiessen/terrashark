# Security and Governance

Use this guide for security controls in IaC delivery. For framework mappings and evidence gates, use `compliance-gates.md`.

## Identity controls

- least privilege for CI identities
- separate `plan` and `apply` roles where possible
- short-lived credentials via workload identity federation
- deny direct human write access to production backends

## Secret controls

- prohibit plaintext secret defaults in code
- source sensitive values from managed secret stores
- mark secret variables and outputs as sensitive
- sanitize logs/artifacts and restrict access

## Supply-chain controls

- pin provider/module versions with bounded constraints
- commit lockfile and review lockfile diffs
- verify action/container versions in CI workflows

## Policy layers

Use layered controls, not single-tool reliance:
1. static scanners (`tfsec`, `checkov`, equivalent)
2. plan-policy checks (Sentinel/OPA/Conftest)
3. approval gates by risk class

## High-impact change controls

Require elevated approval for:
- IAM privilege expansion
- network exposure/public ingress changes
- encryption disablement/key-policy weakening
- backend/state changes
- production replacement/destruction actions

## Minimal OPA example

```rego
package main

deny[msg] {
  r := input.resource_changes[_]
  r.type == "aws_security_group_rule"
  r.change.after.cidr_blocks[_] == "0.0.0.0/0"
  r.change.after.from_port == 22
  msg := sprintf("Public SSH is not allowed: %s", [r.address])
}
```

## Operational governance

- serialize applies for shared foundations
- require explicit opt-in for destroy
- keep break-glass runbook and test it periodically
- retain run metadata and policy outputs for auditability
