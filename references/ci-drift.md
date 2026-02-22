# CI Drift

Use this guide when pipeline behavior diverges from local behavior or from reviewed intent.

## Symptoms

- CI plan differs from local plan unexpectedly
- apply occurs without using reviewed plan artifact
- provider/runtime drift appears between runs
- scanner/policy stages are skipped on some paths

## Root causes

- unpinned runtime/provider versions
- missing or stale lockfile
- apply job running `plan` again instead of consuming reviewed artifact
- inconsistent credentials/auth between plan and apply

## Drift prevention baseline

- pin runtime and provider ranges
- commit lockfile and review lockfile changes
- generate one reviewed plan artifact and apply exactly that artifact
- run policy/security checks on every path to apply
- enforce branch protections and environment approvals

## Production-ready GitHub Actions template

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

Notes:
- replace auth steps with OIDC/provider-specific login actions
- in real repos, split plan/apply workflows if artifact lifetime across events is an issue

## Production-ready GitLab CI template

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

## LLM mistake checklist

Common model mistakes to correct:
- missing lockfile strategy
- apply without saved plan artifact
- no policy stage despite claiming compliance
- no branch/environment protection discussion

## Quick diagnostics

- compare runtime versions local vs CI
- diff lockfile in PR
- ensure apply consumes `plan.bin` from reviewed plan stage
- verify policy scanner runs on every apply path
