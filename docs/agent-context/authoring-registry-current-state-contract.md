# Current-state distribuce authoring registrů

Tento dokument je sdíleným kontraktem pro publikaci registrů specializovaných
authoring produktů a jejich čtení nadřazeným orchestrátorem. Platí pro XDS, Intranet,
Comex i další vrstvy, pokud jejich vlastní přijaté rozhodnutí neurčí doloženou odchylku.

## Rozdělení odpovědnosti

- `product/` v authoring workspace je jediný autoritativní zdroj produktu.
- GitHub Product repository uchovává historii, audit a body pro rollback.
- Cloudová registry vystavuje pouze aktuální validovaný stav.
- Specializovaný authoring repository vlastní obsah, validaci, descriptor a publish
  plán své registry.
- Orchestrátor registry specialistů objevuje a resolveuje; nekopíruje jejich skills
  ani doménovou implementaci do svého produktu.

## Stabilní cloudová topologie

Každá specializovaná registry používá vlastní stabilní prefix:

```text
/registries/<registry-id>/
├── registry.json
├── skills/
│   └── <skill-id>/
│       └── SKILL.md
└── references/
    └── <reference-id>/
        └── ...
```

Typické identifikátory jsou `xds`, `intranet` a `comex`. Skill nebo reference se při
změně aktualizuje na stejné cestě. Cloud nesmí vytvářet:

- `/artifacts/sha256/<digest>/`;
- adresáře pojmenované release verzí;
- úplné kopie registry pro jednotlivé release;
- druhou historii vedle GitHub Product repository.

## Descriptor `registry.json`

Descriptor popisuje aktuálně publikovaný stav a obsahuje alespoň:

- identitu registry, kanonickou URL a stav dostupnosti;
- mapu skills se stabilní cestou, SHA-256 digestem a dependency metadaty;
- mapu referencí se stabilní cestou a SHA-256 digestem;
- u vícesouborové reference také cesty a digesty deklarovaných souborů;
- doplňkovou provenance zdrojového produktu nebo Git revize, pokud ji publisher zná.

Digest se zapisuje jako `sha256:<hex>`. Digest artefaktu se počítá pouze z jeho
vlastního distribuovaného obsahu. Globální Git revision, product digest ani release
verze nesmějí změnit digest nezměněného skillu nebo reference. Stejné vstupní bajty a
stejné relativní cesty proto vedou ke stejnému digestu.

Číselná revize artefaktu je volitelná. Smí se použít pouze tehdy, pokud má registry
autoritativní monotónní čítač. Klient se vždy musí umět rozhodnout podle digestu.

## Publish workflow specialisty

1. Sestavte nový výstup z explicitního publish plánu do prázdného pracovního cíle.
2. Ověřte dependency closure, stabilní cesty, deklarované soubory a všechny digesty.
3. Publikujte pouze při schváleném stavu dostupnosti registry.
4. Synchronizujte změněné skills a reference do jejich stabilních prefixů.
5. Odstraňujte zastaralé soubory pouze uvnitř prefixů vlastněných danou registry.
6. Použijte cache policy dovolující revalidaci obsahu na stabilních URL.
7. `registry.json` publikujte až po obsahu.

Cloudový publish nesmí sám spouštět distribuované tools, MCP operace, Replicator ani
jiné mutující workflow. Credentials a transportní konfigurace nepatří do produktu ani
descriptoru.

## Discovery a resolve orchestrátoru

Orchestrátor pro každou nakonfigurovanou registry:

1. načte `registry.json` z kanonické URL;
2. porovná digest požadovaného artefaktu s lokální cache;
3. stáhne pouze chybějící nebo změněné skills a reference;
4. ověří stažené bajty proti descriptoru;
5. resolveuje deklarovanou dependency closure;
6. zapíše konkrétní cesty a digesty do resolution locku a trace;
7. oddělí discovery a resolve od jakéhokoli execution.

Stav `NOT_PUBLISHED` nebo jiný capability gap se nesmí interpretovat jako dostupná
capability. Federace registrů a capability routing stojí nad tímto transportním
kontraktem a nejsou jím změněny.

## Rollback a obnova

Rollback znamená vybrat dřívější ověřený commit v GitHub Product repository, znovu z
něj sestavit registry a publikovat jej na stejné stabilní cesty. R2 ani jiný cloudový
transport není archivem release.

## Adopční checklist

- [ ] `registry-id` a kanonická URL jsou jednoznačné.
- [ ] Publish plán je allowlist skutečně distribuovaného obsahu.
- [ ] `registry.json` obsahuje stabilní cesty a `sha256:` digesty.
- [ ] Test dokládá determinismus a lokalitu digestů.
- [ ] Workflow neobsahuje digestové ani verzované cloudové adresáře.
- [ ] Mazání je omezené na prefixy vlastněné registry.
- [ ] Descriptor se publikuje jako poslední.
- [ ] Registry má pravdivý stav dostupnosti a odděluje resolve od execution.
- [ ] Je doložen postup rollbacku z Git historie.

Referenční první implementací kontraktu je XDS registry. Převzetí v Intranet, Comex
nebo dalším authoring repozitáři má zachovat tento kontrakt, ale publisher, publish plán,
obsah a validační evidence zůstávají ve vlastnictví daného specialisty.
