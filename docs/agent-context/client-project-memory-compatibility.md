# Sladění klientských projektů s Project Memory

- Ověřeno: 2026-10-19 proti lokálním zdrojům, bez změny klientského projektu nebo publikace.
- Rozhodnutí: [ADR-0009](decisions/0009-project-memory-consumer-support.md), rozšířeno [ADR-0010](decisions/0010-documentation-management-and-project-memory-installation.md) dne 2026-10-29.
- Primární typ: stále `client-project`; rozlišujeme dva layouty, nikoli nový typ repository.

## Návrh a realizovaný rozsah

Repository-helper rozumí existující Project Memory a respektuje její zdroje pravdy.
Zakladatelem zůstává MCP s verzovanou šablonou Orchestrátoru. Helper nevlastní projektovou
identitu, sémantické formáty ani přechody stavů. Dosavadní helper-native klientské projekty
zůstávají podporované bez automatické migrace.

Změna rozšiřuje stávající `maintain-client-project-dimension`, audit, inicializační,
migrační a validační skill. Doplněné hranice misí, ADR, nabídek a logu brání tomu, aby
jiný obecný postup vytvořil druhý analytický strom. Detailní mapu obsahuje
[přenositelná reference](../../.agents/skills/maintain-client-project-dimension/references/project-memory.md),
která se distribuuje spolu se skillem. Nevzniká kopie MCP schémat ani vlastní template.

## Podklady a jejich autorita

| Podklad | Vyhodnocení |
| --- | --- |
| [Kontrakt Orchestrátoru](../../../Flexideo-orchestrator/docs/agent-context/domain/project-memory-repository-contract.md) a [ADR-0065](../../../Flexideo-orchestrator/docs/agent-context/decisions/0065-epic-first-project-memory.md) | Autorita layoutu. Aktuální je úvodní Epic-first část; rozsáhlý zbytek kontraktu je výslovně historická Memory 0.1. |
| [Project 2 schema](../../../Flexideo-orchestrator/product/contracts/project-v2.schema.json), [Memory 0.2 schema](../../../Flexideo-orchestrator/product/contracts/project-memory-v0.2.schema.json), [template 2.0.0](../../../Flexideo-orchestrator/product/project-repo-template/2.0.0/README.md) | Strojové kontrakty a provisioning vlastní Orchestrátor/MCP; helper je nekopíruje ani neimplementuje podruhé. |
| Uživatelova příloha „Kam ukládat dokumentaci struktury aplikace“ | Návrh `docs/reference/` pro kompletní generovanou sadu, oddělení definic, ruční architektury a externího dynamického indexu. Přijato jako interpretační vodítko; není hotovou publikací do Memory. |
| Uživatelova příloha „Ano. A myslím, že toto je důležité architektonické upřesnění…“ | Project Memory jako společný kontext Průvodce, Replicatoru a Implementátora s odlišným vlastnictvím a oprávněními. Přijato pro výklad, ne jako nové zápisové API. |
| [Dosavadní helper-native model](client-project-capability.md), [ADR-0003](decisions/0003-client-project-epic-structure.md) | Platný pro dosavadní implementační projekty. Nesmí se univerzálně aplikovat na Memory. |

Přílohy byly dodány v tomto zadání 2026-10-19; helper uchovává jejich závěry, nikoli
kopii soukromé přílohy nebo tvrzení o nezávislém ověření všech odkazovaných implementací.

## Rozdíly, které mění chování agenta

| Otázka | Helper-native | Project Memory 0.2 |
| --- | --- | --- |
| Kdo zakládá projekt? | Dosavadní init/capability helperu. | MCP a template; helper poskytuje orientaci v existujícím projektu. |
| Kde je analytický scope? | `docs/project/epics/<slug>/` a mise. | `project/epics/EPIC-NNNN/`, vlastní baseline, FAAM stav a historie. |
| Kde je Current Truth? | `docs/agent-context/` podle místních pravidel. | Sdílený `context/`, řízená promotion; žádná kopie do agent-context. |
| Kde jsou rozhodnutí? | Globální technické ADR se `Scope`. | Analytická `DEC-*` lokálně v epiku; technická aplikační ADR podle kontraktu vlastníka. |
| Jsou definice povinné už při analýze? | Capability zakládá XDS/XCF strukturu a hlásí chybějící vstupy. | Oblasti mohou vznikat lazy; žádné povinné XDS/XCF a prázdné podstromy od helperu. |
| Co znamená denní log? | Ruční append-only chronologie. | MCP mutace už loguje atomicky; mimo MCP se použije běžný log bez duplikace. |
| Co znamená nabídka? | Volitelná samostatná HTML capability. | Připnutý import schváleného offer releasu přes promotion. |

Memory 0.1 zůstává čitelná ve vlastním historickém layoutu. Migrace 0.1 → 0.2 vyžaduje
reviewed manifest a konkrétní head/blob SHA; helper ji nevytváří. Slug helper-native epiku
se automaticky nepřekládá na `EPIC-NNNN`.

## Návrhy z příloh a otevřené kontrakty

- `definitions/` je zdrojový model; ruční a generované části rozlišuje vlastník producenta.
  Generovaná dokumentace sestaveného `role.xds`/DAD nenahrazuje autorský zdroj.
- `docs/reference/` je doporučený publikační kořen kompletní sady Replicatoru včetně
  manifestu, FDT Markdownů a textových indexů. Helper ji klasifikuje jako kandidáta na
  generovanou referenci a vyžaduje při výkladu ověření producenta, scope a provenience.
  Nezavádí nový formát manifestu, generátor ani publikační adaptér.
- `docs/architecture/decisions/` a `application/{application.yaml,instances/,snapshots/}`
  jsou navržené konvence. Memory 0.2 neurčuje tyto konkrétní soubory; helper je nezakládá
  ani nevyžaduje. `application/` chápe jako sdílenou aplikační oblast.
- Reference reprezentuje výslovně doložený model/instanci a verzi. Poslední DEV build
  není automaticky referencí PROD. Git snapshot nedokazuje aktuální živý stav ani nasazení.
- Remote Version Store a živá instance si ponechávají vlastní autoritu. Dynamický SQLite
  index je externí obnovitelná projekce nebo autorizovaný read-only snapshot; do Memory
  patří případně připnutá reference, nikoli povinná binární databáze.
- Pro budoucí publikaci zbývá vlastníkům dohodnout identitu projekt/aplikace/instance,
  výběr referenčního zdroje, scope zápisů, úplnost a atomické přepnutí celé sady. Podpora
  porozumění v helperu neznamená implementaci těchto mechanismů ani rozšíření oprávnění MCP.

## Chování CLI a instalace

`repository_architecture.py` detekuje `.project-memory/` nebo textovou stopu Flexideo
Project kontraktu v `project.yaml`. Jde o konzervativní směrování, nikoli YAML validaci;
i neúplná či budoucí Memory má být chráněna před obecným scaffoldem. Obyčejný `project.yaml`
bez těchto stop zůstává v obecném režimu.

- `audit`: čtecí inventura označí verzi a oblasti, neaktivuje epik a neslibuje validitu.
- `validate`: u Memory ověří také případnou spravovanou dokumentační instalaci a její profil;
  dále neprázdné orientační soubory README, project.yaml a
  schema-version a rozpoznaný marker 0.1/0.2. Výslovně vypíše, že sémantická validace
  **neproběhla**. Neověřuje revize, ID, obsah rozhodnutí ani soulad kontraktu s markerem.
- `init`: rozpoznanou i podezřelou Memory odmítne před prvním zápisem, včetně `--force`.
- `install-capability --name client-project`: u rozpoznané Memory 0.1/0.2 instaluje pouze
  klientský čtecí skill, UI metadata a jeho referenci, případně synchronizuje již používanou
  označenou Claude kopii. Nemění AGENTS, analytiku, definitions ani metadata serveru.
- `install-capability --name documentation-management`: u známé Memory 0.1/0.2 instaluje
  obecné dokumentační skills, vyhledávač a jejich profil/manifest. Nemění projektový obsah,
  AGENTS ani metadata serveru; lokální změny odmítá i s `--force`. Viz
  [kontrakt instalace](documentation-management-capability.md).
- Ostatní instalace a neznámý marker zůstávají odmítnuté bez zápisu a bez fallbacku.

Z kořene helperu, pro existující projekt:

```bash
python toolkit/agent-infrastructure/repository_architecture.py audit <project-repository>
python toolkit/agent-infrastructure/repository_architecture.py validate <project-repository>
python toolkit/agent-infrastructure/repository_architecture.py install-capability <project-repository> --name client-project
```

Samostatně použijte matching MCP nebo validátor vlastníka:

```bash
python ../Flexideo-orchestrator/product/tools/project-memory/project_memory_repository.py validate <project-repository>
```

Žádný klientský repozitář nebyl touto změnou založen, migrován ani aktualizován.
Ověření zde popisuje [testing.md](testing.md); další instalace a publikace jsou samostatná práce.
