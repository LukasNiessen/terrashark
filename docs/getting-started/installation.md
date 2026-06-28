# Installing the Terraform Skill

TerraShark can be installed in four ways depending on your environment: skills CLI, marketplace, manual Claude Code skill install, or per-project for Codex.

## Option 1: Skills CLI

If you manage skills with the `skills` CLI, install TerraShark directly from GitHub:

```bash
npx skills add https://github.com/lukasniessen/terrashark --skill terrashark
```

## Option 2: Marketplace Install

Claude Code has a built-in plugin system with marketplace support. Add TerraShark directly from the CLI:

```text
/plugin marketplace add LukasNiessen/terrashark
/plugin install terrashark
```

Or use the interactive plugin manager:
1. Run `/plugin`
2. Switch to the **Discover** tab
3. Install TerraShark from there

The marketplace reads the `.claude-plugin/marketplace.json` in the repository to register TerraShark as an installable plugin.

## Option 3: Manual Claude Code Skill

If you cannot use the marketplace, clone the repo and copy the packaged skill directory into Claude Code's skills directory.

### macOS / Linux

```bash
git clone https://github.com/LukasNiessen/terrashark.git /tmp/terrashark
mkdir -p ~/.claude/skills/terrashark
cp -R /tmp/terrashark/skills/terrashark/. ~/.claude/skills/terrashark/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/LukasNiessen/terrashark.git "$env:TEMP\terrashark"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\terrashark"
Copy-Item -Recurse -Force "$env:TEMP\terrashark\skills\terrashark\*" "$env:USERPROFILE\.claude\skills\terrashark\"
```

Claude Code auto-discovers skills in `~/.claude/skills/` - no restart needed.

## Option 4: Codex (Per-Project Setup)

Codex has no global skill system - setup is per-project. Clone TerraShark into your repository and reference it from your `AGENTS.md`:

```bash
# Clone into your project root
git clone https://github.com/LukasNiessen/terrashark.git .terrashark
```

Then add to your `AGENTS.md` (or create one in the repo root):

```markdown
## Terraform

When working with Terraform or OpenTofu, follow the workflow in `.terrashark/skills/terrashark/SKILL.md`.
Load references from `.terrashark/skills/terrashark/references/` as needed.
```

## Updating the Terraform Skill

To update a marketplace install, reinstall TerraShark from Claude Code's plugin manager. To update a manual skill install, refresh the clone and copy the packaged skill directory again.

```bash
cd /tmp/terrashark
git pull origin main
cp -R skills/terrashark/. ~/.claude/skills/terrashark/
```

## Verifying the Installation

After installing through the marketplace, test it by asking Claude Code any Terraform question:

```text
/terrashark:terrashark Create a multi-region S3 module with replication
```

Or ask naturally - the Terraform skill activates automatically for any Terraform/OpenTofu task:

```text
Review my main.tf for security issues
```

The response should follow the 7-step failure-mode workflow and include an output contract with assumptions, tradeoffs, and rollback notes.

## System Requirements

- **Claude Code** or **Codex** with skill support
- **Git** for cloning the repository
- No additional dependencies required - the skill is pure Markdown
