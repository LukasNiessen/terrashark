# Contributing

Thanks for contributing to Terrashark.

## Goal of this repo

Improve Terraform/OpenTofu output quality while staying lean on token usage.

Every change should answer:
- which failure mode does this prevent?
- what measurable quality gain does it provide?
- is the token cost justified?

## Development flow

1. create a branch
2. make focused changes
3. run local checks
4. open PR using `.github/PULL_REQUEST_TEMPLATE.md`

## Local checks

```bash
# quick sanity checks
rg -n "FIXME|placeholder-text" README.md skills/terrashark/SKILL.md skills/terrashark/references/*.md
python - <<'PY'
from pathlib import Path
assert Path('skills/terrashark/SKILL.md').exists()
assert Path('README.md').exists()
for p in [
  'skills/terrashark/references/identity-churn.md',
  'skills/terrashark/references/secret-exposure.md',
  'skills/terrashark/references/blast-radius.md',
  'skills/terrashark/references/ci-drift.md',
  'skills/terrashark/references/compliance-gates.md',
]:
  assert Path(p).exists(), f'missing {p}'
print('basic structure OK')
PY
```

## Content rules

- Keep examples original and clearly distinct.
- Prefer failure-mode framing over generic "best-practice dump" text.
- Avoid provider-specific deep dives unless they directly reduce a known LLM failure mode.
- Keep claims precise; avoid vague "always" language when tradeoffs exist.

## Required for PR approval

- clear mapping to one or more failure modes
- no contradictory guidance across references
- updated links/indexes if files were moved/renamed
- validation workflow passing (`.github/workflows/validate.yml`)

## Security

- never commit credentials, tokens, or secret values
- do not paste real state snippets containing sensitive data

## Community

Open an issue with:
- observed hallucination/failure pattern
- minimal reproducible prompt/context
- expected behavior

