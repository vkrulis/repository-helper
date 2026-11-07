---
name: audit-repository-structure
description: Beze změn zmapuje existující repozitář, rozpozná skutečný účel dokumentace, analytických resources, agentních instrukcí, profilů, skills, nástrojů a platformních konfigurací a připraví migrační mapu do cílové struktury. Použijte před jakoukoli významnou reorganizací, při sloučení CLAUDE.md, AGENTS.md a dalších instrukcí nebo když není jasné, kde leží zdroj pravdy. Skill nesmí během auditu přesouvat ani mazat soubory.
compatibility: Vyžaduje read přístup k repozitáři; Git a Python 3 jsou doporučené.
metadata:
  version: "1.0"
  mutates-repository: "false"
---

# Audit struktury repozitáře

## Cíl

Vytvořit důkazně podložený obraz stávajícího uspořádání a návrh cílové struktury bez jakýchkoli změn souborů.

## Povinné pravidlo

**Audit je read-only.** Nevytvářejte migrační adresáře, nepřesouvejte soubory a neopravujte obsah.

Jedinou přípustnou změnou je uživatelem výslovně požadované uložení auditní zprávy.

## Postup

### 1. Základní stav

Zjistěte:

- Git root a aktivní větev,
- stav pracovního stromu,
- velikost a primární typ repozitáře podle `docs/agent-context/repository-types.md`:
  `development`, `authoring`, `client-project` nebo `documentation`,
- u authoringu roli `specialist` nebo `orchestrator`, autoritativní produktovou hranici
  a případné duplicity mezi `product/skills/` a `.agents/skills/`,
- monorepo/submodule/worktree vlastnosti,
- hlavní jazyky a build systémy,
- CI/CD a deployment konfiguraci.

U klientského projektu nejprve zkontrolujte `project.yaml` a `.project-memory/`.
Project Memory 0.2 má analytiku v `project/epics/EPIC-NNNN/`; 0.1 v historických
kořenových oblastech. Přečtěte kontrakt projektu a případně referenci
`maintain-client-project-dimension/references/project-memory.md`. Zmapujte vlastnictví,
Current Truth, generované reference a externí snapshoty. Nenavrhujte přesun do
`docs/project/` ani převod epiku na misi jen kvůli obecné struktuře helperu.

### 2. Inventura agentní vrstvy

Vyhledejte zejména:

```text
AGENTS.md
AGENTS.override.md
CLAUDE.md
GEMINI.md
.github/copilot-instructions.md
.github/instructions/
.github/agents/
.claude/
.codex/
.gemini/
.agents/
**/SKILL.md
**/*.agent.md
**/settings.json
**/config.toml
```

Nevycházejte pouze z těchto názvů. Hledejte také vlastní adresáře jako `prompts/`, `ai/`, `automation/`, `scripts/`, `bin/`, `playbooks/`, `manual/`, `wiki/`, `resources/`, `data/`, `schemas/` nebo `fixtures/`.

### 3. Inventura znalostí a nástrojů

Rozlište:

- projektovou dokumentaci,
- doménové reference,
- rozhodovací záznamy,
- návody a runbooky,
- opakovatelné AI postupy,
- deterministické skripty,
- generované výstupy,
- datové korpusy, schémata, snapshoty a cizí zdrojový kód určený k analýze,
- lokální a citlivé soubory.

### 4. Sémantická klasifikace

Nejprve doložte primární typ podle autoritativního výstupu repozitáře. Každý významný
kandidát pak zařaďte podle cílové architektury:

```text
README
AGENTS rules
agent context
agent profile
skill
tool
analysis resource
platform adapter
platform enforcement
application code
operations/deployment
generated
archive/obsolete
ambiguous
```

Přečtěte obsah dostatečně na to, abyste klasifikaci doložili.

### 5. Duplicitní a konfliktní zdroje

Porovnejte instrukční a dokumentační soubory. Zaznamenejte:

- stejné pravidlo v různých souborech,
- odporující si příkazy,
- zastaralé cesty,
- platformní kopie vydávající se za autoritativní zdroj,
- pravidla skrytá pouze v promptu nebo agentním profilu,
- nástroje popsané v dokumentaci, ale neexistující v repozitáři.

### 6. Migrační mapa

Pro každý navržený přesun použijte tabulku z `references/audit-report-template.md`.

Každý záznam musí obsahovat důvod a riziko. U nejasných položek navrhněte konkrétní rozhodovací otázku.

### 7. Doporučená cílová struktura

Navrhněte čistý cílový strom. Nezachovávejte historické uspořádání pouze ze zvyku, pokud nemá technický důvod.

Současně nerozbíjejte standardní strukturu aplikačního ekosystému jen kvůli agentnímu modelu. Například `src/`, `tests/`, `.github/workflows/`, `infra/` nebo `deploy/` zůstávají tam, kde dávají smysl.

### 8. Otázky

Položte pouze otázky s vysokým dopadem. Seskupte je podle tématu a u každé vysvětlete, které migrační rozhodnutí ovlivní.

## Pomocný příkaz

```bash
python toolkit/agent-infrastructure/repository_architecture.py audit <repository> --output repository-audit.md
```

Výstup nástroje je inventura, nikoli konečný sémantický závěr. Ověřte jej čtením obsahu.

## Výstup

Použijte strukturu `references/audit-report-template.md`.

Na konci jednoznačně uveďte:

- zda je repozitář připraven k migraci,
- které body vyžadují potvrzení,
- které změny jsou bezpečné a mechanické,
- které změny jsou radikální nebo rizikové.
