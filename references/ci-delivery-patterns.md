# CI Delivery Patterns

Use this guide to implement auditable Terraform/OpenTofu delivery pipelines.

## Delivery principles

- plan and apply are separate concerns
- apply must consume reviewed plan artifact when architecture permits
- policy and security checks run on every apply path
- production applies require environment protection and approvals

## Baseline stages

1. `fmt` + `validate`
2. lint + security scan
3. plan creation
4. policy checks against plan JSON
5. approval gate
6. apply from trusted branch/runner
7. post-apply drift and evidence capture

## GitHub Actions (production-oriented template)

```yaml
name: terraform-delivery

on:
  pull_request:
    paths:
      - '**/*.tf'
      - '**/*.tfvars'
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - '**/*.tf'
      - '**/*.tfvars'

permissions:
  contents: read
  id-token: write
  pull-requests: write

concurrency:
  group: terraform-${{ github.ref }}
  cancel-in-progress: false

env:
  TF_IN_AUTOMATION: "true"

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check
      - run: terraform init -backend=false
      - run: terraform validate

  plan:
    if: github.event_name == 'pull_request'
    needs: [validate]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan -out=plan.bin
      - run: terraform show -json plan.bin > plan.json
      - run: conftest test plan.json --policy policy/
      - uses: actions/upload-artifact@v4
        with:
          name: reviewed-plan
          path: |
            plan.bin
            plan.json

  apply:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    needs: [validate]
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan -out=plan.bin
      - run: terraform apply -auto-approve plan.bin
```

Notes:
- configure provider auth with OIDC (avoid static cloud keys)
- if you require strict “apply reviewed PR plan” semantics, keep plan/apply in same workflow run or externalize signed plan storage

## GitLab CI (production-oriented template)

```yaml
stages:
  - validate
  - plan
  - policy
  - apply
  - verify

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
    paths: [plan.bin, plan.json]
    expire_in: 24h

policy:
  stage: policy
  image: openpolicyagent/conftest:latest
  dependencies: [plan]
  script:
    - conftest test plan.json --policy policy/

apply:
  stage: apply
  image: hashicorp/terraform:1.7
  dependencies: [plan]
  when: manual
  allow_failure: false
  script:
    - terraform init
    - terraform apply -auto-approve plan.bin

verify:
  stage: verify
  image: hashicorp/terraform:1.7
  script:
    - terraform plan -detailed-exitcode
```

## Pipeline hardening checklist

- enforce branch protection on default branch
- require CODEOWNERS review for prod-impacting paths
- restrict apply jobs to protected runners
- set artifact retention + access policies
- preserve audit trail (approver, actor, commit, runtime version)

## Cost and speed controls

- run expensive integration suites only for IaC path changes
- serialize shared-foundation applies
- use provider plugin cache where supported
- schedule cleanup for ephemeral test environments

## Atlantis (PR-driven delivery template)

Use Atlantis when you want chat-driven, PR-scoped plan/apply with locking.

Example `atlantis.yaml`:

```yaml
version: 3
projects:
  - name: platform
    dir: .
    workspace: default
    autoplan:
      enabled: true
      when_modified: ["**/*.tf", "**/*.tfvars"]
    workflow: default

workflows:
  default:
    plan:
      steps:
        - init
        - plan
    apply:
      steps:
        - apply
```

Hardening notes:
- restrict apply to approved PRs and protected branches
- enable Atlantis server-side locking
- use custom workflows to add policy checks and cost steps
- keep CI auth in OIDC where supported; avoid static secrets

## Infracost (cost visibility template)

Use Infracost to surface cost deltas from plan JSON in PRs.

Pattern:
1. run plan and export plan JSON
2. generate Infracost breakdown
3. publish result as PR comment or artifact

Example commands:

```bash
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
infracost breakdown --path plan.json --format json --out-file infracost.json
```

Notes:
- store `plan.json` and `infracost.json` as artifacts for auditability
- treat cost checks like policy checks for high-risk environments
