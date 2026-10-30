# ADR-0009: Helper jako konzument Project Memory bez provisioningu

- Stav: accepted
- Datum: 2026-10-19
- Vlastník: správci Repository-helper
- Scope: shared
- Nahrazuje: —
- Nahrazeno: [ADR-0010](0010-documentation-management-and-project-memory-installation.md) — částečně: další explicitně povolená dokumentační instalace; provisioning a sémantické hranice zůstávají platné.

## Kontext a problém

Dosavadní klientská capability předpokládá `docs/project/`, mise a ruční definiční větev.
Project Memory Orchestrátoru podle ADR-0065 používá vlastní epiky, sdílenou Current Truth
a sémantické MCP operace. Univerzální použití helperového scaffoldu by vytvořilo druhou
analytickou pravdu. Uživatel výslovně požaduje podporu porozumění a vylučuje helper jako zakladatele.

## Zvažované možnosti

- Nahradit celý helper-native model novou strukturou: zbytečně migruje dosavadní projekty.
- Zkopírovat template, schémata a sémantický validátor do helperu: vzniká další vlastník kontraktu.
- Rozlišit layouty ve stávajícím typu client-project a konzumovat kontrakt vlastníka.

## Rozhodnutí

Použijeme třetí variantu v rozsahu výslovného zadání z 2026-10-19. Helper poskytuje
orientaci v existující Memory, přenositelnou referenci a ochranu proti nekompatibilnímu
scaffoldu. Provisioning i sémantické zápisy a validaci nadále vlastní MCP/Orchestrátor.
ADR-0003 zůstává platné pro helper-native klientské projekty; tento záznam vymezuje
jeho působnost vůči externě vlastněnému layoutu, nemění jejich historii ani je nemigruje.

Detaily a vyhodnocení příloh: [kompatibilitní návrh](../client-project-memory-compatibility.md).

## Důsledky

Helper nesmí z úspěšné orientační kontroly odvozovat validitu analytických stavů.
Přenositelná reference potřebuje revizi při změně kontraktu Orchestrátoru, nikoli vlastní
fork schémat. Budoucí publikace Replicatoru, registry instancí a snapshotů zůstávají
kontrakty jejich vlastníků. Nové capability se musí před instalací do Memory posoudit;
v tomto řezu je podporovaná pouze instalace čtecího klientského skillu.
