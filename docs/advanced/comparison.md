# Terraform Skill Comparison: TerraShark vs Alternatives

A detailed comparison between TerraShark and other approaches to LLM-assisted Terraform code generation.

## Comparison Overview

| Dimension | TerraShark | terraform-skill | No Skill |
|---|---|---|---|
| **SKILL.md activation cost** | ~600 tokens | ~4,400 tokens | 0 |
| **Reference granularity** | 18 focused files | 6 large files | — |
| **Token burn per query** | Low (load 1-2 small refs) | High (large refs, e.g. 1,126 lines) | 0 |
| **Architecture** | Failure-mode workflow | Static reference manual | — |
| **Diagnoses before generating** | Yes (Step 2) | No | No |
| **Output contract** | Yes — assumptions, tradeoffs, rollback | No | No |
| **Migration playbooks** | Yes (5 playbooks) | Partial (inline snippets) | No |
| **Good/bad/neutral examples** | Yes (3 dedicated files) | Inline only | No |
| **Do/Don't checklist** | Yes (dedicated file) | Inline only | No |
| **Compliance framework mapping** | ISO 27001, SOC 2, FedRAMP, GDPR, PCI DSS, HIPAA | Partial | No |
| **MCP integration guidance** | Yes | No | No |
| **Hallucination prevention** | Core design goal | Not addressed | No |
| **Security-first defaults** | Built-in | Checklist-style | No |
| **CI/CD templates** | GitHub Actions, GitLab CI, Atlantis, Infracost | GitHub Actions, GitLab CI, Atlantis | No |
| **License** | MIT | Apache 2.0 | — |

## Architectural Difference

The key difference is architectural.

**Static reference approach** (terraform-skill and similar): Dumps thousands of tokens into context on every activation, then loads additional reference files that can be over 1,000 lines each. Gives the AI information but never tells it *how to think* about a problem. No diagnosis step, no risk assessment, no structured output.

**Failure-mode workflow** (TerraShark): The core SKILL.md is a 79-line operational workflow costing ~600 tokens on activation — over 7x leaner. Forces the AI through a diagnostic sequence: capture context, identify failure modes, load only relevant references, propose fixes with explicit risk controls, validate, and deliver a structured output contract.

## Why This Matters

### 1. Token Efficiency

Static skills burn ~4,400 tokens just to activate, before any reference files. A single reference file like `module-patterns.md` (1,126 lines, ~7,000 tokens) can double the cost. TerraShark's activation is ~600 tokens, and its 18 granular reference files mean the AI loads only what's needed.

### 2. Hallucination Prevention

Static skills provide good patterns but never ask the AI to diagnose what could go wrong. TerraShark's Step 2 forces failure-mode identification before any code is generated. Step 4 requires explicit risk controls. Step 7 enforces an output contract.

### 3. Reference Coverage

TerraShark ships 18 focused reference files covering failure modes, migration playbooks, good/bad/neutral examples, do/don't checklists, compliance framework mappings, and MCP integration. Alternatives typically have fewer, larger files that go deep on some topics but lack migration playbooks, anti-pattern banks, and compliance mappings.

## When to Use No Skill

For simple, one-off Terraform questions where the AI's built-in knowledge is sufficient and you don't need:
- Failure mode diagnosis
- Output contracts
- Migration safety
- Compliance evidence

## Summary

TerraShark provides 7x leaner activation, a failure-mode-first diagnostic workflow, output contracts, granular references, and LLM-specific hallucination prevention. Its architecture is fundamentally designed for the core use case of LLM-assisted IaC generation.
