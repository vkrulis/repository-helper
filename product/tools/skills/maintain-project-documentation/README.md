# Project documentation helper

Read-only helper pro capability `maintain-project-documentation`.

## Příkazy

~~~bash
python project_documentation.py validate <repository>
python project_documentation.py inventory <repository>
python project_documentation.py inventory <repository> --json
~~~

Nástroj:

- rozpozná Project Memory;
- zkontroluje základní hranici `docs/` vůči `project/epics/`;
- ověří tvar existující FDT reference;
- pokud existuje `documents.jsonl`, zkontroluje explicitní třídy `data/view/pseudo`;
- inventarizuje kurátorované oblasti `aplikace/datovy-model/procesy/integrace/provoz`;
- upozorní na kurátorované věcné stránky bez sekce `Zdroje a aktuálnost`;
- inventarizuje návrhové reference `application/comex/usage/indexes`, ale nevydává je
  za implementovaný kontrakt;
- upozorní, pokud se návrhová generated reference objeví v `docs/reference/` bez
  potvrzeného producer/packager kontraktu.

Nástroj nic nezapisuje, neparsuje XDS, nekopíruje parsery Intranetu/COMEXu a
nepřipojuje se k živé aplikaci.

## Důležitá hranice

`docs/reference/fdt/` má existujícího producenta Replicator.

`docs/reference/application/`, `comex/`, `usage/` a `indexes/` jsou podle obsahové
revize z 28. 10. 2026 návrhové rodiny. Dokud se jejich vlastníci neshodnou na packageru,
manifestu a refresh lifecycle, validátor je pouze inventarizuje a varuje; nesnaží se
jejich obsah sémanticky validovat.
