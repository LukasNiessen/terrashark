# Terraform Skill Quick Start Guide

Get productive with the Terraform skill in under 2 minutes.

## Step 1: Install

```bash
git clone https://github.com/LukasNiessen/terrashark.git ~/.claude/skills/terrashark
```

## Step 2: Use It

### Explicit Invocation

Use the `/terrashark` command to explicitly invoke the Terraform skill:

```bash
/terrashark Create a multi-region S3 module with replication
```

```bash
/terrashark Refactor our EKS stack into separate state files per environment, add moved blocks to avoid recreation, set up a GitHub Actions pipeline with plan on PR and gated apply on merge, and wire in Checkov for compliance scanning
```

### Automatic Activation

The Terraform skill activates automatically for any Terraform/OpenTofu task. Just ask naturally:

```
Review my main.tf for security issues
```

```
Migrate this module from count to for_each
```

```
Set up a CI pipeline for our Terraform modules
```

## What to Expect

Every TerraShark response follows the 7-step workflow and includes a structured output:

1. **Assumptions** — what the skill assumed about your environment and versions
2. **Failure modes** — which risks were identified (identity churn, secret exposure, etc.)
3. **Remediation** — what was recommended and what tradeoffs were made
4. **Validation plan** — how to verify the output before applying
5. **Rollback notes** — how to undo changes if something goes wrong

## Example Tasks

Here are some common tasks the Terraform skill excels at:

| Task | Example Prompt |
|------|---------------|
| Module creation | "Create an AWS VPC module with public and private subnets" |
| Security review | "Review my Terraform for secret exposure risks" |
| Migration | "Migrate from count to for_each for my subnet resources" |
| CI/CD setup | "Set up GitHub Actions for Terraform with plan on PR and apply on merge" |
| Compliance | "Add SOC 2 compliance gates to our Terraform pipeline" |
| Refactoring | "Split this monolithic root into service stacks with blast radius isolation" |
| Troubleshooting | "Why does my plan show replacements after renaming a module?" |

## Next Steps

- Read about the [7-Step Workflow](../core-concepts/workflow.md) to understand how the skill processes tasks
- Explore the [Five Failure Modes](../core-concepts/failure-modes.md) that drive every diagnostic
- Check the [Good Patterns](../examples/good-patterns.md) and [Bad Patterns](../examples/bad-patterns.md) for reference
