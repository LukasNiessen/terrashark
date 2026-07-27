# Installing the Terraform Skill

TerraShark can be installed in five ways depending on your environment: direct
clone for Claude Code, Antigravity, or Gemini CLI, the Claude marketplace, or
the native Codex plugin marketplace.

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

## Option 3: Codex Plugin

TerraShark includes `.codex-plugin/plugin.json` and a packaged skill under
`skills/terrashark/`. Add the repository as a marketplace and install it:

```bash
codex plugin marketplace add LukasNiessen/terrashark
codex plugin add terrashark@terrashark
```

Restart Codex and start a new task so the installed skill is included in skill
discovery. Codex can invoke the skill explicitly or activate it implicitly for
matching Terraform/OpenTofu requests.

## Option 4: Antigravity (Global Setup)

Cloning into the Antigravity skills directory enables the skill across all your workspaces.

### macOS / Linux

```bash
git clone https://github.com/LukasNiessen/terrashark.git ~/.gemini/antigravity/skills/terrashark
```

### Windows (PowerShell)

```powershell
git clone https://github.com/LukasNiessen/terrashark.git "$env:USERPROFILE\.gemini\antigravity\skills\terrashark"
```

Antigravity auto-discovers skills in the skills directory — **no restart needed**.

## Option 5: Gemini CLI (Global or Workspace Setup)

Gemini CLI discovers skills in several standard locations.

### Global Installation (All Workspaces)

Ideal for tools you want available in every project.

```bash
git clone https://github.com/LukasNiessen/terrashark.git ~/.gemini/skills/terrashark
```

### Local Installation (Current Workspace)

Ideal for project-specific workflow enforcement. Clone into the root of your project:

```bash
git clone https://github.com/LukasNiessen/terrashark.git .gemini/skills/terrashark
```

Gemini CLI auto-discovers skills in these directories. Run `/skills list` in the CLI to verify.

## Updating the Terraform Skill

To update to the latest version, pull the latest changes in the directory you installed it:

**Claude Code:**
```bash
cd ~/.claude/skills/terrashark
git pull origin main
```

**Antigravity:**
```bash
cd ~/.gemini/antigravity/skills/terrashark
git pull origin main
```

**Gemini CLI (Global):**
```bash
cd ~/.gemini/skills/terrashark
git pull origin main
```

**Codex plugin:**
```bash
codex plugin marketplace upgrade terrashark
codex plugin remove terrashark@terrashark
codex plugin add terrashark@terrashark
```

Restart Codex and test in a new task after upgrading.

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

- **Claude Code**, **Codex**, **Antigravity**, or **Gemini CLI** with skill support
- **Git** for cloning the repository
- No additional dependencies required — the skill is pure Markdown
