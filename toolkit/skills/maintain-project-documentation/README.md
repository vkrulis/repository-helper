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
- zkontroluje základní hranici `docs/`;
- ověří tvar existující FDT reference;
- pokud existuje `documents.jsonl`, zkontroluje explicitní třídy `data/view/pseudo`;
- vytvoří inventuru dokumentačních oblastí.

Nástroj nic nezapisuje, neparsuje XDS a nepřipojuje se k živé aplikaci.
