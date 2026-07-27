# Checklist platformního konektoru

## Společné

- [ ] Konektor byl výslovně zvolen nebo odpovídá aktuálnímu prostředí Codex.
- [ ] Nebyly bez požadavku vytvořeny konektory pro další platformy.
- [ ] `AGENTS.md` zůstává společným zdrojem pravidel.
- [ ] `.agents/profiles/` zůstává zdrojem profilů.
- [ ] `.agents/skills/` zůstává zdrojem skills.
- [ ] Adaptér nekopíruje celou projektovou znalost.
- [ ] Generované soubory obsahují označení zdroje.
- [ ] Existující ruční konfigurace nebyla přepsána bez kontroly.
- [ ] Nebyly přidány secrets ani osobní cesty.
- [ ] Neověřené capabilities nejsou prezentovány jako vynucená oprávnění.

## Codex

- [ ] Codex načte `AGENTS.md`.
- [ ] Codex vidí `.agents/skills/`.
- [ ] Každý `.codex/agents/*.toml` obsahuje povinná pole.
- [ ] `.codex/config.toml` obsahuje pouze potřebná projektová nastavení.

## Claude Code

- [ ] `CLAUDE.md` importuje `AGENTS.md`.
- [ ] Profily jsou v `.claude/agents/`.
- [ ] Kanonické skills zůstávají v `.agents/skills/`.
- [ ] Pokud byly na výslovné přání zpřístupněny v `.claude/skills/`, jde o synchronizovatelnou označenou kopii nebo funkční symlink.

## Gemini CLI

- [ ] `GEMINI.md` importuje `AGENTS.md`.
- [ ] `.agents/skills/` je použitá bez zbytečné kopie.
- [ ] `.gemini/settings.json` je validní JSON a obsahuje jen potřebná nastavení.

## GitHub Copilot

- [ ] `.github/copilot-instructions.md` je krátký doplněk.
- [ ] Agentní profily mají příponu `.agent.md`.
- [ ] Tools odpovídají cílovému Copilot povrchu.
