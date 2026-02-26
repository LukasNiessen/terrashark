# Terraform Skill Token Efficiency Strategy

This page explains the token efficiency strategy that makes TerraShark the leanest Terraform skill available, and the empirical process used to validate every line of content.

## The Problem with Large Skills

Most Terraform skills dump huge walls of text into the AI's context window on every activation. This creates three problems:

1. **Wasted tokens** — context window space spent on skill content is unavailable for the user's codebase and conversation
2. **Signal dilution** — when everything is included, the model has difficulty finding what matters
3. **Redundancy** — LLMs already know basic Terraform syntax; restating it burns tokens with no quality improvement

## TerraShark's Approach

### Lean Activation (~600 tokens)

The core `SKILL.md` is 79 lines containing:
- No HCL examples
- No inline code blocks
- No tutorial material
- Pure procedure: a workflow the model follows

### Granular References (18 files)

Instead of 6 large files (as in alternatives), TerraShark uses 18 focused files. The model loads only the 1-2 files relevant to the diagnosed failure mode.

### Content Inclusion Rules

Content enters TerraShark only when at least one condition is met:

1. It materially lowers the probability of destructive or non-compliant changes
2. It prevents common plan/apply surprises
3. It encodes organizational guardrails that general model knowledge cannot infer

Content is excluded when:

1. It is generic Terraform/OpenTofu knowledge with low failure impact
2. It is provider-specific deep design that belongs in project docs
3. It duplicates an existing rule without adding a new decision signal

### Expansion Rule

If repeated failure patterns emerge, targeted lines are added for that specific failure mode instead of broad expansion.

## The Token Experiment

The content was empirically tested, not designed by intuition.

### Process

1. Started with significantly larger reference content
2. Built automated test suite of practical Terraform/OpenTofu tasks
3. Measured baseline quality (correctness, safety, completeness, hallucination rate)
4. Stripped sections one at a time, re-running the full test suite
5. If quality dropped: content was restored (load-bearing)
6. If quality stayed stable: content was permanently removed (redundant)
7. Continued until every remaining section was load-bearing

### What Survived

Content the model demonstrably needs help with:

- Module role boundaries and composition rules
- Migration playbooks (moved blocks, count-to-for_each, imports)
- Native test caveats (set indexing, computed values, mocked providers)
- CI delivery templates (policy checks, artifact integrity, env protection)
- Quick troubleshooting (stuck locks, backend migration, provider auth in CI)

### What Was Removed

Content the model already knows well:

- Generic HCL syntax tutorials
- Provider-specific resource deep dives
- Broad "best practice" prose without failure-mode framing
- Duplicate explanations

### Core Principle

**High signal density.** Every line must earn its token cost by preventing a specific failure mode or encoding knowledge the model demonstrably lacks.
