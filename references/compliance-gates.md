# Compliance Gates

Use this guide to map infrastructure delivery to enforceable controls and evidence.

## Principle

Treat compliance as delivery gates, not static documentation.
Every framework mapping should translate into:
- preventative controls (policy/validation)
- detective controls (logging/monitoring)
- evidence artifacts (plans, approvals, audit records)

## Framework starter mappings (reordered)

The right set depends on organization scope. Common starting points:

### ISO 27001

Focus:
- formal ISMS governance
- access control and change management
- incident response and evidence retention

IaC gate examples:
- mandatory change approval records
- encryption and logging policy checks
- periodic access review evidence from CI/CD systems

### SOC 2

Focus:
- security, availability, confidentiality controls

IaC gate examples:
- least-privilege IAM enforcement
- transport/at-rest encryption checks
- audit logging enabled on critical services

### FedRAMP (when US federal workloads apply)

Focus:
- strict baseline controls, boundary protection, continuous monitoring

IaC gate examples:
- region/service allowlists for authorized environments
- hardened network segmentation policies
- continuous scan artifacts attached to each release

### GDPR (when processing EU personal data)

Focus:
- data protection by design, minimization, lawful processing support

IaC gate examples:
- data residency constraints via policy
- retention/lifecycle enforcement for personal data stores
- access logging for data systems with evidence retention

### PCI DSS (when cardholder data environment exists)

Focus:
- segmentation, key management, hardening, monitoring

IaC gate examples:
- deny public exposure of CDE components
- no default credentials
- strong encryption and key rotation controls

### HIPAA (when handling protected health information)

Focus:
- confidentiality/integrity of ePHI, auditability, access controls

IaC gate examples:
- private network boundaries for ePHI systems
- immutable audit trails for infra changes
- backup/retention and recovery controls

## Policy-as-code gate pattern

- Stage 1: static scanning (`tfsec`, `checkov`)
- Stage 2: plan policy checks (Sentinel/OPA/Conftest)
- Stage 3: approval workflow tied to risk class
- Stage 4: evidence archival (plan, policy result, approver identity)

## Risk-classed approval model

- low risk: one maintainer approval
- medium risk: platform owner + service owner approval
- high risk (identity/network/encryption/state): security or compliance sign-off required

## Minimal evidence checklist

For each production apply retain:
- reviewed plan artifact and hash
- policy scan output
- approver identity and timestamp
- runtime/provider versions
- post-apply verification logs

## LLM mistake checklist

Common model mistakes to correct:
- mentions framework names but gives no enforceable gates
- confuses security best practices with compliance evidence
- omits who approves what risk class
- ignores data-residency obligations for GDPR/FedRAMP-like contexts
