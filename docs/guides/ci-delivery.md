# Terraform CI/CD Delivery Patterns

This guide covers implementing auditable Terraform and OpenTofu delivery pipelines with GitHub Actions, GitLab CI, Atlantis, and Infracost.

## Delivery Principles

- Plan and apply are separate concerns
- Apply must consume the reviewed plan artifact when architecture permits
- Policy and security checks run on every apply path
- Production applies require environment protection and approvals

## Baseline Stages

Every production Terraform pipeline should include:

1. `fmt` + `validate`
2. Lint + security scan
3. Plan creation
4. Policy checks against plan JSON
5. Approval gate
6. Apply from trusted branch/runner
7. Post-apply drift and evidence capture

## GitHub Actions Template

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

**Notes:**
- Configure provider auth with OIDC (avoid static cloud keys)
- For strict "apply reviewed PR plan" semantics, keep plan/apply in same workflow run or externalize signed plan storage

## GitLab CI Template

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

## Atlantis (PR-Driven Delivery)

Use Atlantis for chat-driven, PR-scoped plan/apply with locking.

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

**Hardening notes:**
- Restrict apply to approved PRs and protected branches
- Enable Atlantis server-side locking
- Use custom workflows to add policy checks and cost steps
- Keep CI auth in OIDC where supported; avoid static secrets

## Infracost (Cost Visibility)

Surface cost deltas from plan JSON in PRs:

```bash
terraform plan -out=plan.bin
terraform show -json plan.bin > plan.json
infracost breakdown --path plan.json --format json --out-file infracost.json
```

Store `plan.json` and `infracost.json` as artifacts for auditability. Treat cost checks like policy checks for high-risk environments.

## Pipeline Hardening Checklist

- Enforce branch protection on default branch
- Require CODEOWNERS review for prod-impacting paths
- Restrict apply jobs to protected runners
- Set artifact retention + access policies
- Preserve audit trail (approver, actor, commit, runtime version)

## Cost and Speed Controls

- Run expensive integration suites only for IaC path changes
- Serialize shared-foundation applies
- Use provider plugin cache where supported
- Schedule cleanup for ephemeral test environments
