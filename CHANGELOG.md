# Changelog

## v2.4.0-alpha.0 — modern plugin layout

- Adopt the canonical Claude Code plugin layout: `.claude-plugin/plugin.json` + `skills/terrashark/SKILL.md` + `skills/terrashark/references/`.
- `/plugin install terrashark` now registers the skill as `terrashark:terrashark` (previously reported `0 skills`).
- Bump version to `2.4.0-alpha.0+modern-plugin-layout` in both `marketplace.json` and the new `plugin.json`.
- Update README install instructions for the new layout.
- Fixes [#11](https://github.com/LukasNiessen/terrashark/issues/11).

## v2.3.0 — Init
