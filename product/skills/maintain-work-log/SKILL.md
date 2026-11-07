---
name: maintain-work-log
description: Vede stručnou, dohledatelnou a append-only pracovní historii repozitáře v .logs/YYYY/MM/YYYY-MM-DD.md. Použijte po každé materiální změně kódu, dokumentace, konfigurace nebo struktury, před finálním předáním práce a při hledání dřívějších rozhodnutí, změn či plánů.
---

# Maintain work log

## Účel

Zaznamenávejte, co se v repozitáři skutečně změnilo, jak byla změna ověřena a co zůstává otevřené. Log je chronologická pracovní paměť; současný autoritativní stav patří do `docs/agent-context/` a fyzická historie změn do Gitu.

## Project Memory

Každá úspěšná sémantická MCP mutace už zapisuje `.logs/` ve stejném commitu.
Pro tutéž mutaci nepřidávejte duplicitní ruční záznam; tento skill použijte pro
materiální práci mimo MCP. Log nenahrazuje epic Session, Checkpoint ani Milestone
a neuděluje právo měnit `.project-memory/` revizi nebo serverové indexy.

## Kdy zapisovat

Zápis je povinný po materiální změně repozitáře, zejména po úpravě kódu, dokumentace, pravidel, konfigurace, struktury, nástrojů nebo veřejného chování. Více těsně souvisejících úprav shrňte jedním zápisem. Nezapisujte pouhé čtení bez výsledku, triviální diagnostiku ani každou jednotlivou editaci.

Před finálním předáním ověřte, že dnešní dokončená práce má odpovídající zápis. Při navazování na starší práci nejprve použijte `recent` nebo `search`.

## Postup zápisu

1. Oddělte ověřená fakta od plánované nebo otevřené práce.
2. Napište stručný název a shrnutí výsledku, ne průběh uvažování ani přepis konverzace.
3. Uveďte změněné soubory odkazy relativními k repozitáři.
4. Uveďte skutečně provedené validace a jejich výsledek. Neprovedenou validaci neprezentujte jako úspěšnou.
5. Otevřené kroky zapište samostatně; pozdější předělávka vytváří nový zápis a starý se nepřepisuje.
6. Pokud vznikl nebo změnil stav ADR, uveďte jej pomocí `--decision docs/agent-context/decisions/<soubor>.md`.
7. Zápis vytvořte nástrojem `python toolkit/work-log/work-log.py add ...`.
8. Nakonec spusťte `python toolkit/work-log/work-log.py validate .`.

Minimální příklad:

```bash
python toolkit/work-log/work-log.py add . --title "Zpřesnění validace" --type change --status done --summary "Validátor nyní odmítá nástroje mimo toolkit." --change "toolkit/agent-infrastructure/repository_architecture.py" --validation "python toolkit/agent-infrastructure/repository_architecture.py validate . — PASS"
```

## Hledání historie

```bash
python toolkit/work-log/work-log.py recent . --days 14
python toolkit/work-log/work-log.py search . --query "replikace" --tag architecture
```

Výsledek vyhledávání berte jako historickou stopu. Je-li v rozporu s aktuální dokumentací nebo kódem, má přednost současný autoritativní zdroj.

## Obsahová omezení

- Nezapisujte secrets, tokeny, osobní údaje, produkční data ani celé výpisy nástrojů.
- Nezapisujte skryté uvažování, prompty ani přepis konverzace.
- Log nepoužívejte jako náhradu aktuální dokumentace, issue trackeru, changelogu vydání ani commitu.
- Existující historický zápis opravte jen kvůli zjevnému překlepu nebo nefunkčnímu odkazu; změnu závěru zachyťte novým zápisem.
