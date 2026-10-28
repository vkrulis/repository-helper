# Klientský projekt s epiky

## Dva podporované layouty

Primární typ zůstává `client-project`. Níže popsaný strom je **helper-native** layout
podle ADR-0003, zachovaný pro dosavadní implementace. Existující Flexideo **Project Memory**
má jiný kontrakt: analytika Memory 0.2 patří do `project/epics/EPIC-NNNN/`, sdílená
Current Truth do `context/`. Helper ji nezakládá ani nepřevádí na zdejší strom.

Před instalací, auditem nebo změnou přečtěte
[kompatibilitu s Project Memory](client-project-memory-compatibility.md). Ta vyhodnocuje
návrhy integrace Replicatoru, mapuje autority a popisuje hranice helperu.
Přenositelnou čtecí pomůcku obsahuje
[reference skillu](../../.agents/skills/maintain-client-project-dimension/references/project-memory.md).

## Model

Klientský implementační projekt je jeden repozitář, jedna historie Git, jedna aplikace a jeden
ručně spravovaný definiční model v `definitions/`. Dlouhodobé ucelené podtéma se vede jako epik;
v klientském projektu je jedna mise právě jeden epik.

Společný obsah zůstává v projektových kořenech. Obsah specifický pro epik se odděluje jen tam,
kde tím nevznikne druhý zdroj pravdy nebo se nezmění runtime/deployment cesta.

## Strom

```text
docs/project/
├── assignment.md
├── analysis/
├── design/
├── client/
├── traceability.md
└── epics/
    ├── README.md
    └── <epic-id>/README.md

docs/agent-context/
├── decisions/                 # jeden globální ADR registr, Scope rozlišuje epik
└── domain/<epic-id>/          # jen doménová pravda specifická pro epik

resources/epics/<epic-id>/
artifacts/epics/<epic-id>/
toolkit/epics/<epic-id>/
definitions/                   # jedna XDS/XCF větev; neklonuje se podle epiků
```

`<epic-id>` je stabilní slug z malých písmen, číslic a pomlček, například `hypo-calc`.

## Zdroje pravdy

- `docs/project/assignment.md` je jediné živé zadání celého klientského projektu.
- `docs/missions/NN-<epic-id>.md` je řídicí dokument epiku: cíl, stav, priorita, závislosti a
  stručný checklist; není to detailní task tracker.
- `docs/project/epics/<epic-id>/README.md` propojuje misi s konkrétním kontextem, zdroji,
  artefakty, nástroji a implementačními soubory.
- `docs/agent-context/` obsahuje aktuální technickou a doménovou pravdu.
- `docs/agent-context/decisions/` je jeden globální registr ADR. Každé ADR má `Scope: shared`
  nebo `Scope: <epic-id>`.
- `.logs/YYYY/MM/YYYY-MM-DD.md` je jeden append-only denní log pro celý projekt. Každý záznam
  uvádí scope v titulku nebo tagu a patří do stejného commitu jako změna.
- `definitions/` je do přijatého ADR o jiné strategii jediný ručně spravovaný zdroj pravdy pro
  projektovou XDS, XCF a jejich definiční obsah.

## Pravidla epiků

1. Založte epik jen pro cíl přesahující jednu materiální změnu; drobné úkoly zůstávají v logu
   nebo task trackeru.
2. Založte jednu misi se souborem `NN-<epic-id>.md` a stejné `Epic: <epic-id>`.
3. Založte `docs/project/epics/<epic-id>/README.md` a odkazy na relevantní cesty. Teprve potom
   zakládejte prázdné epikové podsložky pro skutečně potřebné zdroje, artefakty nebo nástroje.
4. Společné soubory neklonujte do epiku. U souboru sdíleného více epiky evidujte vlastnictví a
   vazbu v jejich rozcestnících.
5. Hlavní XDS, XCF a soubory s pevnou runtime cestou nepřesouvejte jen kvůli logickému členění.
6. Každé dlouhodobé rozhodnutí zapisujte jako ADR s globálním číslem a `Scope`. Konečné číslo
   přidělte při integraci do sdílené větve; návrh může mít pracovní název, aby paralelní autoři
   nevytvořili kolizi.
7. Každou materiální změnu commitujte společně s příslušným logem. `develop` je integrační větev;
   paralelní práce se má integrovat přes samostatný commit nebo review.

## Validace

## Volitelná projektová dokumentace

Klientský projekt může nainstalovat capability `project-documentation`. V Project Memory
používá existující sdílenou oblast `docs/` pro aktuální popis aplikace a nesmí vytvářet
druhý analytický strom vedle `project/epics/`. V helper-native projektu je dokumentace
aktuálního systému rovněž oddělená od `docs/project/`, které zůstává stopou zadání a
realizace. Podrobný kontrakt je v
[project-documentation-capability.md](project-documentation-capability.md).

## Volitelné nabídky

Nabídka není epik. Projekt, který ji skutečně potřebuje, instaluje samostatnou capability `client-offers`; ta přidává `docs/project/offers/`, `resources/offers/`, `public/offers/`, `artifacts/offers/` a `toolkit/offers/`. Nabídka může později odkázat na epik, ale epik ani definiční model se kvůli tomu nekopíruje ani nepřesouvá.

Validátor kontroluje minimální epikovou vrstvu, jedinečnost čísel misí a ADR, formát `Epic` a
`Scope` a existenci kontextu epiku v klientském projektu. Věcnou správnost zařazení posuzuje
odpovědný člověk během review.
