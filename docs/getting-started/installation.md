# Installing the Terraform Skill

TerraShark can be installed in three ways depending on your environment: direct clone, marketplace, or per-project for Codex.

## Option 1: Clone to Skills Directory (Recommended)

The simplest method. Clone the repository into Claude Code's skills directory.

### macOS / Linux

```bash
git clone https://github.com/LukasNiessen/terrashark.git ~/.claude/skills/terrashark
```

### Windows (PowerShell)

```powershell
git clone https://github.com/LukasNiessen/terrashark.git "$env:USERPROFILE\.claude\skills\terrashark"
```

### Windows (Command Prompt)

```cmd
git clone https://github.com/LukasNiessen/terrashark.git "%USERPROFILE%\.claude\skills\terrashark"
```

Claude Code auto-discovers skills in `~/.claude/skills/` — **no restart needed**.

## Option 2: Marketplace Install

Claude Code has a built-in plugin system with marketplace support. Add TerraShark directly from the CLI:

```bash
/plugin marketplace add LukasNiessen/terrashark
/plugin install terrashark
```

Or use the interactive plugin manager:
1. Run `/plugin`
2. Switch to the **Discover** tab
3. Install TerraShark from there

The marketplace reads the `.claude-plugin/marketplace.json` in the repository to register TerraShark as an installable plugin.

## Option 3: Codex (Per-Project Setup)

Codex has no global skill system — setup is per-project. Clone TerraShark into your repository and reference it from your `AGENTS.md`:

```bash
# Clone into your project root
git clone https://github.com/LukasNiessen/terrashark.git .terrashark
```

Then add to your `AGENTS.md` (or create one in the repo root):

```markdown
## Terraform

When working with Terraform or OpenTofu, follow the workflow in `.terrashark/SKILL.md`.
Load references from `.terrashark/references/` as needed.
```

## Updating the Terraform Skill

To update to the latest version, pull the latest changes:

```bash
cd ~/.claude/skills/terrashark
git pull origin main
```

## Verifying the Installation

After installing, test it by asking Claude Code any Terraform question:

```
/terrashark Create a multi-region S3 module with replication
```

Or ask naturally — the Terraform skill activates automatically for any Terraform/OpenTofu task:

```
Review my main.tf for security issues
```

The response should follow the 7-step failure-mode workflow and include an output contract with assumptions, tradeoffs, and rollback notes.

## System Requirements

- **Claude Code** or **Codex** with skill support
- **Git** for cloning the repository
- No additional dependencies required — the skill is pure Markdown
