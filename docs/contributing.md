# Contributing to the Terraform Skill

We appreciate contributions to TerraShark. Every change should improve Terraform/OpenTofu output quality while staying lean on token usage.

## Contribution Principles

Every change should answer three questions:

1. **Which failure mode does this prevent?** — must map to at least one of the five failure modes
2. **What measurable quality gain does it provide?** — demonstrate improvement
3. **Is the token cost justified?** — every line must earn its place

## Development Flow

1. Create a branch
2. Make focused changes
3. Run local checks
4. Open PR using `.github/PULL_REQUEST_TEMPLATE.md`

## Local Checks

```bash
# Quick sanity checks
rg -n "FIXME|placeholder-text" README.md SKILL.md references/*.md
python - <<'PY'
from pathlib import Path
assert Path('SKILL.md').exists()
assert Path('README.md').exists()
for p in [
  'references/identity-churn.md',
  'references/secret-exposure.md',
  'references/blast-radius.md',
  'references/ci-drift.md',
  'references/compliance-gates.md',
]:
  assert Path(p).exists(), f'missing {p}'
print('basic structure OK')
PY
```

## Content Rules

- Keep examples original and clearly distinct
- Prefer failure-mode framing over generic "best-practice dump" text
- Avoid provider-specific deep dives unless they directly reduce a known LLM failure mode
- Keep claims precise; avoid vague "always" language when tradeoffs exist

## Required for PR Approval

- Clear mapping to one or more failure modes
- No contradictory guidance across references
- Updated links/indexes if files were moved/renamed
- Validation workflow passing (`.github/workflows/validate.yml`)

## Security

- Never commit credentials, tokens, or secret values
- Do not paste real state snippets containing sensitive data

## Reporting Issues

Open an issue with:

- Observed hallucination/failure pattern
- Minimal reproducible prompt/context
- Expected behavior

## Community

- Submit an [issue on GitHub](https://github.com/LukasNiessen/terrashark/issues/new/choose)
- Join [GitHub Discussions](https://github.com/LukasNiessen/terrashark/discussions)
- Star the repository if TerraShark helps your project
