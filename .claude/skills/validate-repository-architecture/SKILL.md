---
name: validate-repository-architecture
description: Ověří agent-ready strukturu repozitáře, oddělení README, AGENTS.md, docs/agent-context, .agents/profiles, .agents/skills, jednotného toolkit a resources, validitu YAML frontmatter, existenci odkazovaných souborů a tenkost platformních adaptérů. Použijte po inicializaci, migraci, změně skillů, resources nebo profilů a před commitem či pull requestem.
compatibility: Pro plnou automatickou kontrolu je doporučen Python 3 a PyYAML.
metadata:
  version: "1.0"
  mutates-repository: "false"
---

# Validace architektury repozitáře

## Cíl

Prokázat, že repozitář odpovídá dohodnuté struktuře a že platformní adaptéry nevytvářejí nové zdroje pravdy.

## Kontroly

Součástí kontroly je `.logs/README.md`, skill `.agents/skills/maintain-work-log/SKILL.md`, nástroj `toolkit/work-log/work-log.py` a explicitní povinnost `.logs/YYYY-MM/YYYY-MM-DD.md` v `AGENTS.md`.

### 1. Povinné vstupní body

Ověřte:

```text
README.md
AGENTS.md
docs/agent-context/README.md
.agents/README.md
.agents/profiles/README.md
.agents/skills/README.md
toolkit/README.md
```

### 2. Skills

Pro každý `.agents/skills/<name>/SKILL.md` ověřte:

- validní YAML frontmatter,
- `name` odpovídá názvu adresáře,
- `name` používá lowercase písmena, čísla a pomlčky,
- povinné `description`,
- description jasně říká, kdy skill použít,
- odkazy na references/assets/scripts existují,
- skill neřeší několik nesouvisejících prací,
- hlavní instrukce nejsou zbytečně dlouhé a detaily jsou v references.

### 3. Profily

Pro každý `.agents/profiles/*.agent.md` ověřte:

- `name` a `description`,
- unikátní jméno,
- existence uvedených skills,
- existence required context cest,
- capabilities jsou logické a platformně neutrální,
- restrictions nejsou mylně vydávány za technicky vynucené.

### 4. Toolkit

Ověřte:

- `toolkit/` je jediným kořenem všech exaktních a spustitelných nástrojů a má README,
- agentní, doménové, vývojové, skillové a runtime nástroje jsou oddělené vhodnými podsložkami,
- `.agents/tools/`, kořenové `tools/`, kořenové `scripts/` ani `.agents/skills/*/scripts/` neexistují,
- lze je spustit bez AI,
- skills odkazují na existující příkazy,
- nejsou v nich hardcoded secrets nebo absolutní uživatelské cesty.

### 5. Resources

Pokud `resources/` existuje, ověřte:

- `resources/README.md` popisuje účel, původ, licenci, autoritativnost a aktualizaci zdrojů,
- složka neobsahuje secrets, osobní produkční data ani nezdokumentované velké binární soubory,
- běhový kód nebyl bez technického důvodu vytržen ze standardní projektové struktury,
- zdroje jednoho přenositelného skillu nejsou zbytečně odděleny od jeho `references/` nebo `assets/`.

### 6. Platformní adaptéry

Ověřte pouze přítomné platformy:

- generované soubory uvádějí kanonický zdroj,
- platformní soubor není plnou kopií `docs/agent-context/`,
- Codex profily jsou validní TOML,
- Claude a Copilot profily mají validní frontmatter,
- Gemini settings jsou validní JSON,
- `CLAUDE.md` nebo `GEMINI.md` skutečně odkazují na `AGENTS.md`,
- kopie skills se nerozešly od kanonických zdrojů.

### 7. Duplicitní zdroje pravdy

Vyhledejte podezřelou shodu dlouhých bloků mezi:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/copilot-instructions.md
docs/agent-context/
```

Krátké shodné názvy a odkazy jsou v pořádku. Dlouhá totožná pravidla jsou varování.

### 8. Projektové kontroly

Spusťte příkazy předepsané v hlavním `AGENTS.md` a relevantní build/test dokumentaci.

## Automatická validace

```bash
python toolkit/agent-infrastructure/repository_architecture.py validate <repository>
python toolkit/agent-infrastructure/validate_skill_collection.py <repository>
python toolkit/work-log/work-log.py validate <repository>
```

Automatická kontrola nenahrazuje sémantickou revizi.

## Výstup

Použijte `references/validation-report-template.md`.

Chyby rozdělte na:

1. blokující,
2. významné,
3. varování,
4. doporučení.

Neoznačujte validaci za úspěšnou, pokud některý povinný příkaz nebyl spuštěn. Uveďte jej jako `not run` a důvod.
