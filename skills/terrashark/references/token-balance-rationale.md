# Content Inclusion Rules

## Add content when at least one is true

1. It materially lowers probability of destructive or non-compliant changes.
2. It prevents common plan/apply surprises (identity churn, drift blind spots, unsafe upgrades).
3. It encodes organizational guardrails that general model knowledge cannot infer.

## Exclude content when

1. It is generic Terraform/OpenTofu knowledge with low failure impact.
2. It is provider-specific deep design that belongs in project docs, not in a shared skill.
3. It duplicates an existing rule without adding a new decision signal.

## Expansion rule

If repeated failure patterns emerge, add targeted lines for that failure mode instead of broad expansion.
