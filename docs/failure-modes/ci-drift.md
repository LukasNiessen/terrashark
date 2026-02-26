# Terraform CI Drift: Preventing Pipeline Divergence

CI drift occurs when pipeline behavior diverges from local behavior or from reviewed intent. This leads to unreviewed applies, inconsistent infrastructure state, and broken trust in the delivery process.

## Symptoms of CI Drift

- CI plan differs from local plan unexpectedly
- Apply occurs without using the reviewed plan artifact
- Provider/runtime drift appears between runs
- Scanner/policy stages are skipped on some paths

## Root Causes

- **Unpinned runtime/provider versions** — different versions produce different plans
- **Missing or stale lockfile** — providers resolve differently across environments
- **Apply re-runs plan** — apply job runs `plan` again instead of consuming the reviewed artifact
- **Inconsistent auth** — different credentials between plan and apply stages

## Drift Prevention Baseline

- Pin runtime and provider version ranges
- Commit lockfile and review lockfile changes
- Generate one reviewed plan artifact and apply exactly that artifact
- Run policy/security checks on every path to apply
- Enforce branch protections and environment approvals

## Production-Ready GitHub Actions Template

```yaml
name: terraform-delivery

on:
  pull_request:
    paths:
      - '**/*.tf'
      - '**/*.tfvars'
  push:
    branches: [main]
    paths:
      - '**/*.tf'
      - '**/*.tfvars'

concurrency:
  group: terraform-${{ github.ref }}
  cancel-in-progress: false

permissions:
  contents: read
  id-token: write
  pull-requests: write

jobs:
  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check
      - run: terraform init -backend=false
      - run: terraform validate
      - run: terraform init
      - run: terraform plan -out=plan.bin
      - run: terraform show -json plan.bin > plan.json
      - run: conftest test plan.json --policy policy/
      - uses: actions/upload-artifact@v4
        with:
          name: reviewed-plan
          path: plan.bin

  apply:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: [validate]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: actions/download-artifact@v4
        with:
          name: reviewed-plan
      - run: terraform init
      - run: terraform apply -auto-approve plan.bin
```

**Notes:**
- Replace auth steps with OIDC/provider-specific login actions
- In real repos, split plan/apply workflows if artifact lifetime across events is an issue

## Production-Ready GitLab CI Template

```yaml
stages:
  - validate
  - plan
  - policy
  - apply

variables:
  TF_IN_AUTOMATION: "true"

validate:
  stage: validate
  image: hashicorp/terraform:1.7
  script:
    - terraform fmt -check
    - terraform init -backend=false
    - terraform validate

plan:
  stage: plan
  image: hashicorp/terraform:1.7
  script:
    - terraform init
    - terraform plan -out=plan.bin
    - terraform show -json plan.bin > plan.json
  artifacts:
    paths:
      - plan.bin
      - plan.json
    expire_in: 24h

policy:
  stage: policy
  image: openpolicyagent/conftest:latest
  script:
    - conftest test plan.json --policy policy/
  dependencies:
    - plan

apply:
  stage: apply
  image: hashicorp/terraform:1.7
  when: manual
  allow_failure: false
  script:
    - terraform init
    - terraform apply -auto-approve plan.bin
  dependencies:
    - plan
```

## LLM Mistake Checklist

Common model mistakes the Terraform skill corrects:

- Missing lockfile strategy
- Apply without saved plan artifact
- No policy stage despite claiming compliance
- No branch/environment protection discussion

## Quick Diagnostics

- Compare runtime versions local vs CI
- Diff lockfile in PR
- Ensure apply consumes `plan.bin` from the reviewed plan stage
- Verify policy scanner runs on every apply path
