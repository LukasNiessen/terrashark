# Blast Radius

Use this guide to limit impact scope for changes, failures, and rollbacks.

## Symptoms

- tiny change triggers very large plan
- unrelated services share one state and fail together
- production and non-production are entangled
- review/approval ownership is unclear

## Boundary model

Split along:
- ownership boundaries
- change cadence boundaries
- recovery boundaries

If these differ, split stack/state.

## Architecture patterns

- platform foundation stack (network, identity, shared controls)
- service stack(s) per business workload
- bootstrap stack for backend/state prerequisites

Do not combine all of them in one root.

## State isolation rules

- one backend key per isolated stack/environment
- dedicated lock scope per stack
- backup/versioning required for production states
- no shared prod/non-prod state files

## Environment separation options

1. separate directories + separate backend keys
2. workspace per environment (only with strict governance)
3. separate repositories for hard regulatory segregation

## Apply governance

- serialize applies to shared foundations
- require explicit approval for production and destructive plans
- block auto-apply for high-impact stacks

## Example structure

```text
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

## LLM mistake checklist

Common model mistakes to correct:
- proposes one monolithic root for convenience
- recommends workspace-only isolation without access controls
- mixes blast radius discussion with purely stylistic concerns
- omits rollback path for shared foundation changes

## Verification checks

- does plan only touch intended stack?
- does state key scope match ownership boundary?
- is rollback path documented for this apply?
