# ADR-0003: Klientský projekt s epiky a scoped ADR

- Stav: accepted
- Datum: 2026-08-11
- Vlastník: správci repository-helper
- Scope: shared
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Velký klientský projekt může obsahovat více dlouhodobých podtémat, která mají vlastní výstup,
zdroje, nástroje a rozhodnutí, ale sdílejí aplikaci, Git historii, denní log a definiční model.
Dosavadní capability neuměla taková podtémata jednotně evidovat.

## Rozhodovací kritéria

- Zachovat jeden zdroj pravdy pro XDS a XCF.
- Oddělit epikový obsah bez duplikace společných souborů.
- Udržet jeden globální, validovatelný registr ADR.
- Umožnit paralelní přípravu návrhů bez trvalé kolize čísel.

## Zvažované možnosti

### Samostatný repozitář pro každý epik

Oddělil by historii, ale rozpadl by jednu aplikaci a její definiční model do více zdrojů pravdy.

### Podsložka pro každý epik včetně kopií definitions

Zlepšila by lokální orientaci, ale kopie XDS/XCF a runtime souborů by vytvářely nejasné vlastnictví.

### Jeden repozitář s epikovou vrstvou a scoped ADR

Zachová společné zdroje pravdy a zároveň poskytne stabilní organizační hranici pro epik.

## Rozhodnutí

V klientském projektu je jedna mise jeden epik se stabilním `Epic: <epic-id>`. Epik má rozcestník
v `docs/project/epics/<epic-id>/README.md` a volitelné specifické podsložky v resources,
artifacts a toolkit. ADR zůstávají v jednom globálním registru, mají globální číslo a povinné
`Scope: shared|<epic-id>`. `definitions/` je do nového přijatého ADR jediný ručně spravovaný
zdroj pravdy.

## Důvody

Model odpovídá jedné aplikaci a jedné integrační historii, přitom neukrývá odpovědnost epiku v
nepojmenovaných souborech. Scope ADR zajišťuje čitelnost bez rozdělení registru.

## Důsledky

- Capability a validátor vyžadují minimální epikovou vrstvu.
- Nová ADR a mise používají rozšířená metadata.
- Konečné číslo souběžně připraveného ADR se přiděluje při integraci.
- Přesuny definičních souborů vyžadují posouzení runtime cesty, ne jen tématu.

## Navazující práce

- Aktualizovat klientské projekty při jejich nejbližší materiální změně.
- Migrovat RDO hypo-calc jako první ověřovací epik.
