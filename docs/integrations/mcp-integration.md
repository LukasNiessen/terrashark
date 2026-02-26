# MCP Integration with the Terraform Skill

This guide covers how to safely use MCP (Model Context Protocol) servers to supply trusted context during Terraform and OpenTofu work.

## When to Use MCP

- Fetch authoritative provider or platform facts for the current environment
- Read organization-specific standards, naming rules, or guardrails
- Pull inventory or baseline state summaries when local context is missing

## What MCP Should Not Do

- Do not retrieve or transmit plaintext secrets
- Do not treat MCP responses as change authorization
- Do not use MCP to bypass review or approval controls

## Safe Integration Pattern

1. **Query** MCP for environment facts and constraints
2. **Compare** with local inputs and repo defaults
3. **Emit assumptions** explicitly if MCP data is partial
4. **Preserve** least-privilege access and log sources used

## Output Hygiene

- Quote MCP-derived values as inputs, not hard-coded defaults
- Keep environment-specific data out of reusable primitives
- Record MCP-provided versions or IDs in notes for traceability

## Example Uses

- Resolve account or project IDs for the target environment
- Confirm region allow-lists and data residency boundaries
- Retrieve approved module registry versions or constraints

## Failure Handling

- If MCP is unavailable, proceed with explicit assumptions
- Avoid speculative values for IDs, names, or policy constraints
- Request confirmation before emitting high-impact changes
