# MCP Integration

Use this guide when MCP servers are available to supply trusted context during Terraform/OpenTofu work.

## When to use MCP

- fetch authoritative provider or platform facts for the current environment
- read organization-specific standards, naming rules, or guardrails
- pull inventory or baseline state summaries when local context is missing

## What MCP should not do

- do not retrieve or transmit plaintext secrets
- do not treat MCP responses as change authorization
- do not use MCP to bypass review or approval controls

## Safe integration pattern

1. Query MCP for environment facts and constraints.
2. Compare with local inputs and repo defaults.
3. Emit assumptions explicitly if MCP data is partial.
4. Preserve least-privilege access and log sources used.

## Output hygiene

- quote MCP-derived values as inputs, not hard-coded defaults
- keep environment-specific data out of reusable primitives
- record MCP-provided versions or IDs in notes for traceability

## Example uses

- resolve account or project IDs for the target environment
- confirm region allow-lists and data residency boundaries
- retrieve approved module registry versions or constraints

## Failure handling

- if MCP is unavailable, proceed with explicit assumptions
- avoid speculative values for IDs, names, or policy constraints
- request confirmation before emitting high-impact changes
