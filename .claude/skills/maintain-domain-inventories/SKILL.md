<!-- GENERATED FROM: .agents/skills/maintain-domain-inventories/SKILL.md -->
<!-- DO NOT EDIT DIRECTLY. Re-run toolkit/agent-infrastructure/render_platform_connectors.py. -->
---
name: maintain-domain-inventories
description: Udržuje živé doménové inventáře toho, co je v aktuálním zdrojovém kódu a v jakém je to stavu. Použijte při opakovaných mapovacích průzkumech, sledování migrace nebo refaktoringu, při návrhu generovaného přehledu a při aktualizaci inventáře po změně sledovaného souboru.
---

# Maintain domain inventories

## Rozlišení vrstev

- `.logs/` odpovídá na „co se stalo a kdy“.
- `docs/agent-context/decisions/` odpovídá na „proč jsme zvolili A místo B“.
- `docs/agent-context/development-rules.md` popisuje opakovatelný převod vzoru.
- `docs/agent-context/domain/` odpovídá na „co v kódu aktuálně je a v jakém je to stavu“.

Inventář není náhrada za ADR, pracovní log ani katalog všech zdrojových souborů.

## Postup

1. Ověřte aktuální stav přímo v repozitáři.
2. Fakta, která lze deterministicky spočítat, generujte nástrojem pod `toolkit/domain/` do `docs/agent-context/domain/*.generated.md`.
3. Ke generovanému výstupu udržujte krátký ručně psaný kontextový dokument; čísla do něj nekopírujte.
4. Při porovnání s baseline uveďte její zdroj a autoritativnost; bez baseline netvrďte, že výskyt vznikl právě touto prací.
5. Nový dokument odkažte z `docs/agent-context/README.md` a inventář aktualizujte spolu se sledovanou změnou.
6. Do ADR vložte pouze závěr a odkaz na inventář.

## Aktualizace a distribuce

Skill je kanonicky uložen v `.agents/skills/maintain-domain-inventories/`. Do jiného repozitáře jej instalujte z repository-helper:

```text
python <repository-helper>/toolkit/agent-infrastructure/repository_architecture.py install-capability <target-repository> --name domain-inventories
```

Pro cílenou aktualizaci již nainstalované kopie použijte `--force` až po kontrole lokálních změn. Platformní kopie se regenerují až po aktualizaci kanonické `.agents/skills/`.

## Kontrola

Po instalaci nebo změně spusťte z kořene cílového repozitáře:

```text
python toolkit/agent-infrastructure/validate_skill_collection.py .
python toolkit/agent-infrastructure/repository_architecture.py validate .
python toolkit/work-log/work-log.py validate .
```

Konkrétní generátor inventáře zůstává projektovým nástrojem.
