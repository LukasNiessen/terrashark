# Terraform Skill for Claude Code and Codex: TerraShark

TerraShark is a lean, failure-mode-first Terraform skill for [Claude Code](https://docs.claude.ai/docs/agent-skills) and [Codex](https://developers.openai.com/codex/skills/). It prevents Terraform and OpenTofu hallucinations by forcing the AI to **diagnose risks before generating code**.

## Why Use a Terraform Skill?

LLMs hallucinate frequently when generating Terraform code. They produce configurations that are syntactically valid but operationally dangerous — unstable resource identities, leaked secrets, oversized blast radii, CI drift, and missing compliance gates. TerraShark fixes this by embedding a 7-step diagnostic workflow and 18 granular reference files directly into the AI's context.

## Key Features

- **Failure-mode-first architecture** — diagnoses risks before generating code
- **~600 token activation cost** — over 7x leaner than alternatives
- **18 granular reference files** — loads only what's relevant per query
- **LLM-specific guardrails** — explicitly names and prevents common AI hallucination patterns
- **Output contracts** — every response includes assumptions, tradeoffs, and rollback notes
- **5 migration playbooks** — safe count-to-for_each, rename, import, secrets, and upgrade flows
- **Compliance framework mappings** — ISO 27001, SOC 2, FedRAMP, GDPR, PCI DSS, HIPAA
- **Production CI/CD templates** — GitHub Actions, GitLab CI, Atlantis, Infracost
- **Based on HashiCorp's official best practices** — prioritizes [HashiCorp recommended practices](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices) when guidance conflicts

## How It Works

When Claude Code encounters a Terraform or OpenTofu task, the Terraform skill activates and runs a 7-step workflow:

1. **Capture execution context** — runtime, version, providers, backend, risk level
2. **Diagnose failure modes** — identity churn, secret exposure, blast radius, CI drift, compliance gaps
3. **Load relevant references** — pull only the targeted guidance needed
4. **Propose fix path** — include risk notes, approvals, tests, and rollback expectations
5. **Generate artifacts** — HCL changes, migration blocks, CI/policy updates
6. **Validate** — runtime-appropriate command sequence and risk-tier checks
7. **Deliver output contract** — assumptions, remediation, tradeoffs, validation plan, recovery notes

## Quick Install

```bash
# macOS / Linux
git clone https://github.com/LukasNiessen/terrashark.git ~/.claude/skills/terrashark

# Windows (PowerShell)
git clone https://github.com/LukasNiessen/terrashark.git "$env:USERPROFILE\.claude\skills\terrashark"
```

That's it. Claude Code auto-discovers skills in `~/.claude/skills/` — no restart needed.

## Supported Runtimes

- **Terraform** (all versions, with feature guards for version-specific capabilities)
- **OpenTofu** (all versions, with equivalent command mappings)

## License

MIT License — see [GitHub repository](https://github.com/LukasNiessen/terrashark) for details.
