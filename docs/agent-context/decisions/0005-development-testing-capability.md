# ADR-0005: Volitelná capability pro vývojové testování

- Stav: accepted
- Datum: 2026-08-14
- Vlastník: správci repository-helper
- Scope: shared
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Vývojové repozitáře potřebují testy a diagnostiku, ale jejich runtime, framework i míra izolace se liší. Jediný předepsaný browserový nebo CI stack by část projektů zbytečně zatížil; bez společné konvence se naopak mísí krátkodobé průzkumy, regrese, secrets a citlivé artefakty.

## Rozhodovací kritéria

- Přenést opakovatelný bezpečný postup bez vazby na klientský projekt nebo konkrétní technologii.
- Rozlišit dlouhodobé regresní scénáře od průzkumné diagnostiky.
- Chránit credentials, produkční data a diagnostické artefakty.
- Umožnit instalovat capability do existujícího repozitáře deterministicky.

## Zvažované možnosti

### Předepsat jeden testovací framework

Zrychlilo by první browserový scénář, ale nefungovalo by pro služby, desktopové aplikace ani existující frameworkové konvence.

### Ponechat testování bez společného modelu

Neomezuje projekty, ale nepřenáší zkušenost s klasifikací scénářů, bezpečností testovacích dat ani s přechodem od reprodukce vady k regresi.

### Volitelná frameworkově neutrální capability

Definuje vrstvy, bezpečné hranice a doporučené umístění vývojové automatizace. Konkrétní runner, selektory, CI a testovací prostředí zůstávají rozhodnutím cílového projektu.

## Rozhodnutí

Zavádíme volitelnou capability `development-testing`. Přidává kontext `development-testing-capability.md` a skill `maintain-development-testing`; instalace je dostupná přes `repository_architecture.py install-capability --name development-testing`.

Capability rozlišuje unit, integration, workflow, regression a probe. Mutující testy jsou explicitně označené a vyžadují opt-in a resetovatelná data. Izolované vývojové testovací balíčky patří do `toolkit/development/`, aniž by se přesouval existující runtime testovací kód.

## Důsledky

- Nový repozitář si capability instaluje pouze tehdy, když ji skutečně využije.
- Každý cílový projekt dokumentuje konkrétní runner, příkazy, prostředí a výjimky v `docs/agent-context/testing.md`.
- Jednotlivé projekty mohou volit Playwright, jiný browserový nástroj nebo žádný browserový test.
- Přidání povinného CI, centrální evidence výsledků nebo test-data service zůstává samostatným rozhodnutím projektu.
