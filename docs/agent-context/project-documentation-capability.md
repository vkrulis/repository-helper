# Projektová dokumentace klientské aplikace

- Stav: accepted target capability
- Datum: 2026-10-28
- ADR: [ADR-0010](decisions/0010-project-documentation-capability.md)
- Skill: `maintain-project-documentation`

## Účel

Capability `project-documentation` přidává do klientského projektu přenositelný postup pro
udržování **aktuální dokumentace skutečně existující aplikace**. Nenahrazuje zadání,
analýzu ani prováděcí historii.

Ve Flexideo Project Memory platí základní hranice:

~~~text
project/epics/EPIC-NNNN/   proč a jak se změna analyzovala a provedla
context/                   sdílená Current Truth
docs/                      co aplikace nyní je a jak funguje
~~~

Dokumentace v `docs/` je sdílená napříč epiky. Po uzavření změny se aktualizuje na nový
současný stav; nekopíruje otázky, evidence, checkpointy ani historii jednotlivých epiků.

## Cílový obsah

Základní navigační model:

~~~text
docs/
├── index.md
├── aplikace/
├── datovy-model/
├── procesy/
├── integrace/
├── provoz/
└── reference/
    └── fdt/
~~~

Složky se materializují až tehdy, když mají skutečný obsah. Skill nevytváří prázdnou
dokumentaci jen kvůli tvaru stromu.

### Autority vrstev

| Vrstva | Autorita | Co z ní dokumentace bere |
| --- | --- | --- |
| XDS | autorské definice konkrétní aplikace | FDT, segmenty, datové vlastnosti, deklarované přístupy a zdrojové vztahy |
| FDT/DAD reference | generovaný balík Replicatoru | ověřitelnou technickou projekci XDS/FDT/DAD |
| Intranet | x-item, saved settings, action registry a procesní vazby | strom aplikace, přehledy, akce, procesní uzly a jejich vazby |
| COMEX | generovaná/provozní UI projekce | jak se komponenty a stránky promítají do uživatelského rozhraní |
| běžící instance | runtime evidence | co je skutečně nasazeno a viditelné v dané roli/prostředí |
| Project Memory | epiky, Current Truth a historie | původ rozhodnutí a změn; ne publikační kopii analytiky |
| `docs/` | kurátorovaný současný výklad | lidsky čitelný obraz aplikace se zdroji a odkazy na technické reference |

## Datový model

Technickou autoritou datového modelu není ručně kreslené ERD, ale XDS a jeho odvozené
FDT/DAD artefakty. Replicator publikuje referenční sadu pod
`docs/reference/fdt/`.

Za podkladový databázový FDT se podle současné implementace považuje finální
`DocumentDef`, který nemá `view-of` a není pseudo typem. Tuto klasifikaci má poskytovat
producent/reference; dokumentace ji nemá znovu heuristicky odvozovat z názvu.

`docs/datovy-model/` proto obsahuje business výklad, vztahy, stavové modely,
číselníky a fyzické mapování s odkazy na FDT reference. Generovaný FDT Markdown se ručně
nepřepisuje.

## Intranetová a COMEX vrstva

Jedna uživatelská funkce může být složena z více vrstev: x-item hlavičky, saved settings,
MTP pomocných přehledů, transformace/akce, registrace, procesního kontextu a COMEX projekce.
Dokumentace proto nesmí vydávat jeden XML soubor za celý funkční celek.

Rozlišují se nejméně tyto grafy:

- navigační rodičovství x-item;
- procesní členství;
- settings linky;
- výstupní hrany procesu;
- graf volání akcí;
- UI vazby a COMEX projekce.

COMEX je výsledná/provozní vrstva UI. `on_comex` samo o sobě nedokazuje efektivní
viditelnost ani oprávnění. Tvrzení o skutečném UI konkrétní role vyžaduje odpovídající
runtime nebo nasazenou CXD evidenci.

## Přenos do Project Memory

Tato capability je výjimkou z původního pravidla helperu „do Memory pouze orientation skill“,
protože:

- nezakládá ani nemění `project/epics/`, `context/`, `.project-memory/` ani projektové stavy;
- instaluje jen skill, jeho přenositelnou referenci a read-only validační/inventory nástroj;
- obsah `docs/` vzniká až při výslovné dokumentační práci v rámci již existujícího projektu;
- provisioning, revize a sémantickou validaci Memory nadále vlastní Orchestrátor/MCP.

V helper-native klientském projektu capability rozšiřuje `client-project`. V Project Memory
se instaluje bez druhého helper-native scaffoldu.

## Instalace

Helper-native klientský projekt:

~~~bash
python toolkit/agent-infrastructure/repository_architecture.py install-capability <repo> --name project-documentation
~~~

Project Memory 0.1/0.2 používá stejný příkaz; installer vloží pouze přenositelné soubory
capability a nepřepisuje AGENTS ani analytickou strukturu.

## Validace

Po instalaci:

~~~bash
python toolkit/skills/maintain-project-documentation/project_documentation.py validate .
python toolkit/skills/maintain-project-documentation/project_documentation.py inventory .
~~~

Nástroj je záměrně read-only. Neparsuje XDS jako druhý producent, negeneruje FDT a
nedotazuje živou instanci.
