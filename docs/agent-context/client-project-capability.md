# Klientský projekt s epiky

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

## Volitelné nabídky

Nabídka není epik. Projekt, který ji skutečně potřebuje, instaluje samostatnou capability `client-offers`; ta přidává `docs/project/offers/`, `resources/offers/`, `public/offers/`, `artifacts/offers/` a `toolkit/offers/`. Nabídka může později odkázat na epik, ale epik ani definiční model se kvůli tomu nekopíruje ani nepřesouvá.

Validátor kontroluje minimální epikovou vrstvu, jedinečnost čísel misí a ADR, formát `Epic` a
`Scope` a existenci kontextu epiku v klientském projektu. Věcnou správnost zařazení posuzuje
odpovědný člověk během review.
