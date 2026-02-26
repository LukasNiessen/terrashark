# Terraform Compliance Gates: Enforceable Controls and Evidence

Compliance gate gaps occur when frameworks are referenced by name but no enforceable controls or evidence artifacts actually exist. The Terraform skill treats compliance as delivery gates, not static documentation.

## Core Principle

Every compliance framework mapping should translate into:

- **Preventative controls** — policy/validation that blocks non-compliant changes
- **Detective controls** — logging/monitoring that catches issues post-deploy
- **Evidence artifacts** — plans, approvals, audit records that prove compliance

## Framework Starter Mappings

### ISO 27001

**Focus:** Formal ISMS governance, access control and change management, incident response and evidence retention.

**IaC gate examples:**
- Mandatory change approval records
- Encryption and logging policy checks
- Periodic access review evidence from CI/CD systems

### SOC 2

**Focus:** Security, availability, confidentiality controls.

**IaC gate examples:**
- Least-privilege IAM enforcement
- Transport/at-rest encryption checks
- Audit logging enabled on critical services

### FedRAMP

**Focus:** Strict baseline controls, boundary protection, continuous monitoring (when US federal workloads apply).

**IaC gate examples:**
- Region/service allowlists for authorized environments
- Hardened network segmentation policies
- Continuous scan artifacts attached to each release

### GDPR

**Focus:** Data protection by design, minimization, lawful processing support (when processing EU personal data).

**IaC gate examples:**
- Data residency constraints via policy
- Retention/lifecycle enforcement for personal data stores
- Access logging for data systems with evidence retention

### PCI DSS

**Focus:** Segmentation, key management, hardening, monitoring (when cardholder data environment exists).

**IaC gate examples:**
- Deny public exposure of CDE components
- No default credentials
- Strong encryption and key rotation controls

### HIPAA

**Focus:** Confidentiality/integrity of ePHI, auditability, access controls (when handling protected health information).

**IaC gate examples:**
- Private network boundaries for ePHI systems
- Immutable audit trails for infra changes
- Backup/retention and recovery controls

## Policy-as-Code Gate Pattern

| Stage | Tool/Action | Purpose |
|---|---|---|
| **Stage 1** | Static scanning (`tfsec`, `checkov`) | Catch common misconfigurations |
| **Stage 2** | Plan policy checks (Sentinel/OPA/Conftest) | Enforce organizational policies |
| **Stage 3** | Approval workflow by risk class | Human oversight for high-impact changes |
| **Stage 4** | Evidence archival | Retain plan, policy result, approver identity |

## Risk-Classed Approval Model

| Risk Level | Required Approval |
|---|---|
| **Low** | One maintainer approval |
| **Medium** | Platform owner + service owner approval |
| **High** (identity/network/encryption/state) | Security or compliance sign-off required |

## Minimal Evidence Checklist

For each production apply, retain:

- Reviewed plan artifact and hash
- Policy scan output
- Approver identity and timestamp
- Runtime/provider versions
- Post-apply verification logs

## LLM Mistake Checklist

Common model mistakes the Terraform skill corrects:

- Mentions framework names but gives no enforceable gates
- Confuses security best practices with compliance evidence
- Omits who approves what risk class
- Ignores data-residency obligations for GDPR/FedRAMP-like contexts
