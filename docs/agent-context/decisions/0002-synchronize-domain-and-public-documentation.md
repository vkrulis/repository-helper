# ADR-0002: Synchronize domain and public documentation

- Stav: accepted
- Datum: 2026-08-09
- Scope: shared
- Vlastník: správci repository-helper
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Doménové repozitáře obsahují technické detaily a odkazy na skutečné soubory, zatímco společný `documentation` repozitář obsahuje obecné Docusaurus stránky. Zkušenost z `fxd-updater` ukázala, že bez explicitního pořadí, vazeb a revizních metadat se tyto vrstvy rozcházejí.

## Rozhodovací kritéria

- Doménová revize musí předcházet revizi obecné dokumentace.
- Obecná dokumentace musí zachovat původ exportu a strojově čitelnou stopu revize.
- Nové repozitáře i existující agent-ready repozitáře musí získat stejnou capability.
- Deterministická kontrola nesmí vyžadovat retroaktivní přepis všech historických exportů.

## Zvažované možnosti

### Pouze pravidlo v AGENTS.md

Jednoduché, ale bez opakovatelného postupu, metadatového kontraktu a kontroly odkazů.

### Samostatný skill bez nástroje

Zachytí pořadí a úsudek, ale nekontroluje spolehlivě hlavičky a explicitní vazby.

### Capability se skillem a validator tool

Odděluje rozhodování agenta od deterministické kontroly a lze ji distribuovat přes `repository_architecture.py`.

## Rozhodnutí

Zavést capability `documentation-sync` se skillem `maintain-documentation-sync` a nástrojem `validate_documentation_metadata.py`. Capability se instaluje do nových repozitářů při `init` a do existujících příkazem `install-capability`.

## Důvody

Tento model zachovává doménovou dokumentaci jako první ověřovaný zdroj, umožňuje společné dokumentaci evidovat revize bez zásahu do starých exportů a sjednocuje distribuci i validaci.

## Důsledky

- Každý nový nebo migrovaný repozitář může používat stejný workflow.
- Změněné veřejné stránky mají povinnou stopu rozsahu, důvodu a času revize.
- Publikace zůstává odpovědností dokumentačního repozitáře a jeho pravidel.
- Stávající historické stránky se nemusí hromadně přepisovat; validator kontroluje soubory explicitně označené jako změněné.
