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

1. Před změnou ověřte aktuální stav přímo v repozitáři; nepřebírejte staré počty z chatu, ADR ani logu.
2. Rozhodněte, zda fakta lze deterministicky spočítat. Pokud ano, uložte generátor pod `toolkit/domain/` a výstup pod `docs/agent-context/domain/*.generated.md`.
3. Ke generovanému výstupu vytvořte krátký ručně psaný dokument `*.md`, který vysvětluje účel inventáře, význam sloupců, baseline a známé falešné poplachy. Čísla do něj nekopírujte.
4. Generátor musí pracovat nad aktuálním stavem, mít explicitní vstupní cesty a bezpečně zacházet s chybějícím baseline. Textové regexy označte jako heuristiku; pro syntaxi použijte parser.
5. Pokud porovnáváte migraci s předchozí verzí nebo sourozeneckým repozitářem, uveďte zdroj baseline, jeho autoritativnost a způsob aktualizace. Bez baseline netvrďte, že výskyt vznikl právě touto prací.
6. Přidejte odkaz na nový dokument do `docs/agent-context/README.md` a popište zdroj v `resources/README.md`, pokud se používá externí snapshot nebo export.
7. Při každé změně souboru, který inventář sleduje, spusťte generátor znovu a commitněte jeho výstup spolu se zdrojovou změnou.
8. Do ADR vložte pouze závěr a odkaz na inventář; syrové seznamy a počty ponechte v generovaném výstupu.

## Aktualizace a distribuce

Skill je kanonicky uložen v `.agents/skills/maintain-domain-inventories/`. Do jiného repozitáře jej instalujte z repository-helper nástrojem:

```text
python <repository-helper>/toolkit/agent-infrastructure/repository_architecture.py install-capability <target-repository> --name domain-inventories
```

Pro cílenou aktualizaci již nainstalované kopie použijte `--force` až po kontrole lokálních změn. Příkaz aktualizuje pouze soubory capability, ne projektové inventáře ani generátory. Pokud cílový repozitář už obsahuje `.claude/skills/`, instalace automaticky synchronizuje označenou kopii nového nebo aktualizovaného skillu; ručně upravenou neoznačenou kopii odmítne přepsat.

## Kontrola

Po instalaci nebo změně spusťte z kořene cílového repozitáře:

```text
python toolkit/agent-infrastructure/validate_skill_collection.py .
python toolkit/agent-infrastructure/repository_architecture.py validate .
python toolkit/work-log/work-log.py validate .
```

Samotný generátor inventáře spusťte podle jeho projektové dokumentace; helper neposkytuje univerzální detekční vzory.
