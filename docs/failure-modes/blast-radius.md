# Terraform Blast Radius: Limiting Change Impact Scope

Blast radius problems occur when infrastructure stacks are too large or poorly isolated, causing small changes to have widespread, unintended impact across unrelated services.

## Symptoms of Blast Radius Problems

- Tiny change triggers a very large plan
- Unrelated services share one state and fail together
- Production and non-production are entangled
- Review/approval ownership is unclear

## Boundary Model

Split stacks along three axes:

| Axis | Question |
|---|---|
| **Ownership** | Who approves and supports this? |
| **Change cadence** | What changes together? |
| **Recovery** | What can fail together? |

If these differ between components, split the stack/state.

## Architecture Patterns

| Pattern | Scope |
|---|---|
| **Platform foundation stack** | Network, identity, shared controls |
| **Service stack(s)** | One per business workload |
| **Bootstrap stack** | Backend/state prerequisites |

Do not combine all of them in one root.

## State Isolation Rules

- One backend key per isolated stack/environment
- Dedicated lock scope per stack
- Backup/versioning required for production states
- No shared prod/non-prod state files

## Environment Separation Options

1. **Separate directories** + separate backend keys (recommended default)
2. **Workspace per environment** (only with strict governance and access controls)
3. **Separate repositories** for hard regulatory segregation

## Apply Governance

- Serialize applies to shared foundations
- Require explicit approval for production and destructive plans
- Block auto-apply for high-impact stacks

## Example Directory Structure

```
infra/
  bootstrap/
  platform/
    dev/
    prod/
  services/
    billing/
      dev/
      prod/
    catalog/
      dev/
      prod/
```

## LLM Mistake Checklist

Common model mistakes the Terraform skill corrects:

- Proposes one monolithic root for convenience
- Recommends workspace-only isolation without access controls
- Mixes blast radius discussion with purely stylistic concerns
- Omits rollback path for shared foundation changes

## Verification Checks

Before applying, verify:

- Does the plan only touch the intended stack?
- Does the state key scope match the ownership boundary?
- Is the rollback path documented for this apply?
