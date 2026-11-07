# Epiky klientského projektu

V klientském projektu představuje každá mise jeden epik. Epik má stabilní identifikátor
`<epic-id>` ve formátu malých písmen, číslic a pomlček, například `hypo-calc`.

Pro každý epik založte `docs/project/epics/<epic-id>/README.md`. Tento dokument je rozcestník
na misi, doménový kontext, ADR, zdroje, artefakty, nástroje a implementační soubory. Jednotlivé
úkoly nepatří do samostatné mise; zůstávají v řízení práce nebo jako stručný checklist mise.

Sdílený obsah projektu zůstává mimo `epics/`. Nedělejte kopie hlavní XDS ani XCF do epiku:
`definitions/` je ručně spravovaný jediný zdroj pravdy, dokud přijaté ADR neurčí jinou strategii.
