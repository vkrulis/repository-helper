# ADR-0001: Obecná správa architektonických rozhodnutí

- Stav: accepted
- Datum: 2026-07-22
- Scope: shared
- Vlastník: správci repository-helper
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Cílová architektura již počítá s `docs/agent-context/decisions/` a migrační skill obsahoval izolovanou šablonu rozhodnutí. Chyběla však obecná metodika, konzervativní rozhodovací brána, přenositelný skill, instalační mechanismus a povinné propojení ADR s chronologickým pracovním logem.

## Rozhodovací kritéria

- Nevytvářet ADR pro každou materiální změnu.
- Zachovat jedno místo pravdy pro metodiku a šablonu.
- Umožnit instalaci schopnosti do nových i existujících agent-ready repozitářů.
- Zachovat oddělení dlouhodobého rozhodnutí v dokumentaci od události v `.logs/`.

## Zvažované možnosti

### Pouze pracovní log

Jednoduché, ale dlouhodobé důvody rozhodnutí by zapadly v chronologii.

### ADR uvnitř `.logs/`

Zachovalo by časovou stopu, ale smísilo by autoritativní projektovou znalost s pracovním deníkem.

### ADR v `docs/agent-context/decisions/` se samostatným skillem

Odděluje významovou a časovou osu a umožňuje řízené přenášení schopnosti.

## Rozhodnutí

Kanonická ADR metodika bude poskytována skillem `maintain-decision-records`. ADR budou uložena v `docs/agent-context/decisions/`; každý vznik nebo změna stavu ADR musí být odkázán z denního pracovního logu. Schopnost se instaluje příkazem `repository_architecture.py install-capability ... --name decision-records` a je součástí inicializace nového agent-ready repozitáře.

## Důvody

Rozhodnutí zachovává jeden zdroj pravdy, je platformně neutrální a dovoluje agentovi vyžádat jen potřebnou repository schopnost. Konzervativní brána omezuje dokumentační režii.

## Důsledky

- Vzniká nový kanonický skill a šablona ADR.
- Pracovní log podporuje explicitní odkazy na rozhodnutí.
- Validátor kontroluje strukturu ADR, supersession odkazy a odkazy z logu.
- Přijaté ADR se nepřepisují; změna závěru vzniká novým záznamem.
