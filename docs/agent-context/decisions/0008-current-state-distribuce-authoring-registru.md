# ADR-0008: Current-state distribuce authoring registrů

- Stav: accepted
- Datum: 2026-08-19
- Scope: shared
- Vlastník: Repository-helper maintainers
- Nahrazuje: —
- Nahrazeno: —
- Upřesňuje: [ADR-0007](0007-typy-repozitaru-a-authoring-produkt.md)

## Kontext a problém

ADR-0007 zavedlo autoritativní `product/`, samostatné specializované authoring produkty
a orchestrátor, který načítá jejich registry. Neurčilo však, zda cloud uchovává archiv
všech release, nebo pouze aktuální distribuci. XDS pilot prokázal, že úplné kopie pod
digestovými adresáři komplikují hosting a duplikují historii dostupnou v GitHub Product
repository.

Společný kontrakt je nutný pro XDS, Intranet, Comex, další specialisty i nadřazený
orchestrátor, aby každý repository nevytvořil jinou fyzickou topologii a resolver.

## Rozhodovací kritéria

- zachovat `product/` jako jediný zdroj pravdy;
- poskytnout stabilní URL a jednoduchý deployment;
- neduplikovat Git historii v object storage;
- zachovat ověření integrity a reprodukovatelný resolution lock;
- umožnit aktualizovat jeden artefakt bez nové kopie celé registry;
- neměnit federaci, ownership, capability routing ani execution hranice.

## Zvažované možnosti

### Možnost A — cloudový archiv obsahově adresovaných release

Každý publish vytvoří úplnou kopii registry pod digestovým nebo verzovaným adresářem.
Cloud uchovává historii paralelně s GitHub Product repository.

### Možnost B — aktuální stav na stabilních cestách

GitHub Product repository uchovává historii. Cloud vystavuje jediný aktuální validovaný
stav pod `/registries/<registry-id>/`; digest je kontrolou obsahu, nikoli adresou.

## Rozhodnutí

Přijímá se možnost B jako výchozí distribuční kontrakt authoring registrů Flexideo.
Normativní pravidla jsou v
[current-state kontraktu](../authoring-registry-current-state-contract.md).

Specialista publikuje `registry.json`, `skills/<skill-id>/SKILL.md` a deklarované
`references/<reference-id>/...` na stabilních cestách. Descriptor nese SHA-256 digesty
a publikuje se po obsahu. Historické stavy se obnovují z Git historie a znovu publikují;
cloud nevytváří `/artifacts/sha256/<digest>/` ani úplné release kopie.

Orchestrátor načítá descriptory specialistů, porovnává digests, stahuje pouze změněné
artefakty, ověřuje integritu a zapisuje resolution lock. Discovery a resolve samy
nespouštějí žádný distribuovaný tool.

## Důvody

- Jeden distribuční model lze opakovat v každém authoring repozitáři.
- Stabilní cesty jsou jednoduché pro hosting i klienty.
- Git již poskytuje audit, historii a rollback.
- Digest zachovává přesnou identitu obsahu bez vynucení fyzických kopií.

## Důsledky

### Pozitivní

- XDS, Intranet, Comex a další registry mají společnou topologii a klientský postup.
- Orchestrátor potřebuje jeden obecný current-state resolver.
- Změna jednoho artefaktu neprodukuje novou kopii celé registry.

### Negativní

- Cloud neposkytuje historické snapshoty; rollback vyžaduje republish z Git commitu.
- Aktualizace stabilních cest není plně transakční, proto se descriptor publikuje
  poslední a artefakty musejí umožnit cache revalidaci.

### Neutrální

- Release verze a Git revision mohou zůstat doplňkovou provenance, ale nejsou součástí
  cesty ani digestu nezměněného artefaktu.
- Specialista nadále vlastní svůj publish plán, validace a transportní konfiguraci.

## Navazující práce

- Propagovat kontrakt capability `authoring-repository` do existujících specialistů a
  orchestrátoru.
- Použít XDS jako referenční implementaci před aktivací Intranet a Comex registrů.
