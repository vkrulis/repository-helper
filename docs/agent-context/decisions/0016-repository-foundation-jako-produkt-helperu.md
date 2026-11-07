# ADR-0016: Repository Foundation jako produkt Repository-helperu

- Stav: accepted
- Datum: 2026-11-07
- Scope: shared
- Vlastník: Repository-helper
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Repository-helper dosud poskytoval přenositelné skills a nástroje přímo ze svého
workspace. Současně sám definoval pravidlo, že authoring repozitář má jediný
publikovatelný zdroj v `product/` a nesmí kombinovat `public/` s `product/`.
Kořen navíc obsahoval materializovaný klientský scaffold a prázdný `public/offers/`,
což směšovalo authoring workspace s jedním cílovým klientským projektem.

## Rozhodovací kritéria

- jediný produktový zdroj pravdy;
- samostatná přenositelnost a testovatelnost bez interních ADR a logů;
- zachování všech obecných, vývojových, authoringových i klientských capabilities;
- bezpečná kompatibilita s Project Memory bez druhé analytické autority;
- možnost připnout produkt do společné lokální sestavy.

## Zvažované možnosti

### Možnost A: ponechat workspace jako přímo distribuovaný balík

Vyžaduje kopírování selektivních kořenových cest, zachovává směšování interního
kontextu s produktem a odporuje authoring repository modelu Helperu.

### Možnost B: autoritativní `product/` Repository Foundation

Produkt drží skills, profily, tools, reference, templates a testy. Kořen drží pouze
workspace kontext, mise, ADR, zdroje a build/release údržbu.

## Rozhodnutí

Přijímá se možnost B. `product/` je jediný publikovatelný zdroj produktu
`flexideo-repository-foundation`. Všechny přenositelné skills a exaktní nástroje se
přesouvají pod tuto hranici. Klientské `definitions/`, `docs/project/`, `artifacts/`,
offers a související resource kostry existují pouze jako produktové šablony pro
instalaci do cílového repozitáře. Kořenový `public/` se ruší.

Repository Foundation je průřezový podpůrný produkt a není novou skupinou A–E / 1–6.
Project Memory nadále provisionuje Orchestrátor; Helper instaluje jen schválený
neanalytický klientský obal a provozní capability.

## Důvody

Produktová hranice umožňuje stejné digesty, testy a distribuční mechanismus jako u
ostatních authoring produktů, aniž by FCL nebo Orchestrátor kopírovaly obsah Helperu.

## Důsledky

- instalační CLI načítá zdroje výhradně z `product/`;
- workspace `.agents/` neobsahuje druhou kopii produktových skills;
- testy produktu jsou v `product/tests/`;
- aktualizace společné sestavy může připnout přesný Helper commit a digest;
- Product Repository Sync ani vzdálená publikace tímto rozhodnutím nevznikají.

## Navazující práce

- přidat `repository-foundation` jako výchozí support product FCL;
- rozšířit assembler Orchestrátoru a aktivovat novou lokální sestavu;
- později doplnit plně manifestované plánování aktualizací všech capability bundles.
