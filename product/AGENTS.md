# Repository Foundation — produktová mapa

Tento adresář je samostatně použitelný produkt pro strukturu a capability repozitářů.
Začni `skills/bootstrap-repository-foundation/SKILL.md`.

- `skills/` jsou kanonické produktové postupy; nevytvářej jejich kopie mimo produkt.
- `tools/` obsahují všechny deterministické instalátory a validátory produktu.
- `templates/` jsou zdroje souborů materializovaných v cílovém repozitáři.
- `references/` vysvětlují repository typy, hranice a kompatibilitu.
- Cílové projektové soubory nikdy neukládej do tohoto distribuovaného produktu.

Repository Foundation je výchozí podpůrný produkt, nikoli skupina A–E / 1–6.
FCL jej připíná pro projektový preflight a pak samostatně vybírá odborné authoringové
vrstvy. Project Memory a provisioning vlastní Orchestrátor.

Před zápisem do cílového repozitáře nejprve proveď audit a zkontroluj lokální změny.
Neznámou verzi Project Memory neměň. Neukládej credentials ani produkční data.

Pokud authoringový běh skutečně použije capability z FCL, dokončení zahrnuje vrstvový
feedback skill A.6–E.6 a `skills/record-authoring-feedback/SKILL.md`. Zapisovač uloží
validní event do append-only denního logu klientského projektu; samotné vybrání nebo
načtení capability se za použití nepovažuje a nepovinný uživatelský rating neblokuje.
