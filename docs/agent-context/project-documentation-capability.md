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

## Obsahový model po revizi XDS authoring návrhu

Capability byla 28. 10. 2026 revidována proti
`Flexideo-XDS-authoring-workspace/docs/agent-context/client-application-documentation-proposal.md`
(blob `d604e20506ee333137b252d85eb0c20b2a3d6eb4`).

Z návrhu přebírá princip propojené mapy:

~~~text
data → aplikační funkce → použití v UI
~~~

a detailní pravidla pro x-item/settings/MTP/akce/procesy, COMEX stránky/komponenty,
typed relations, identity, coverage a refresh.

Nepřebírá bez dalšího pracovní umístění ručního výkladu do
`docs/agent-context/application/`. V cílovém Project Memory modelu patří klientský
kurátorovaný výklad přímo do `docs/aplikace/`, aby nevznikla druhá Current Truth.

## Cílový kurátorovaný obsah

~~~text
docs/
├── index.md
├── aplikace/
│   ├── funkce/
│   └── scenare/
├── datovy-model/
├── procesy/
├── integrace/
├── provoz/
└── reference/
~~~

Složky se materializují až tehdy, když mají skutečný obsah.

## Generované reference

Současně potvrzená produkovaná rodina:

~~~text
docs/reference/fdt/
~~~

Obsahově navržené budoucí rodiny:

~~~text
docs/reference/application/
docs/reference/comex/
docs/reference/usage/
docs/reference/indexes/
~~~

Tyto čtyři rodiny se **nevydávají za implementované**. Zdrojový ADR-0027 i Replicator
ADR-0046 jsou proposal-stage; před přijetím společného packageru/manifestu mají pilotní
výstupy zůstat mimo kanonický `docs/reference/`.

### Autority vrstev

| Vrstva | Autorita | Co z ní dokumentace bere |
| --- | --- | --- |
| XDS | autorské definice konkrétní aplikace | FDT, segmenty, datové vlastnosti, deklarované přístupy a zdrojové vztahy |
| FDT/DAD reference | generovaný balík Replicatoru | ověřitelnou technickou projekci XDS/FDT/DAD |
| Intranet | x-item, saved settings, registry/buildy a procesní vazby | aplikační kompozici a technické karty |
| COMEX | CXD, registry komponent a PageEdit/generator zdroje | prezentační kompozici |
| běžící instance | runtime evidence | skutečně nasazené a rolově ověřené chování |
| Project Memory | epiky, Current Truth a historie | původ rozhodnutí a změn |
| `docs/` | kurátorovaný současný výklad | lidsky čitelný obraz aplikace s odkazy na reference |

## Datový model

Technickou autoritou datového modelu není ručně kreslené ERD, ale XDS a jeho odvozené
FDT/DAD artefakty. `docs/datovy-model/` proto obsahuje business výklad, vztahy,
stavové modely, číselníky a fyzické mapování s odkazy na FDT reference.

Za podkladový databázový FDT se podle současné implementace považuje finální
`DocumentDef`, který nemá `view-of` a není pseudo typem. Klasifikaci má poskytovat
producent nebo ověřený XDS specialista; dokumentace ji nemá hádat podle názvu.

## Intranetová a COMEX vrstva

Jedna funkční entita může zahrnovat hlavičku, předky, source settings, MTP, transformaci,
registraci/build, procesní kontext a COMEX projekci. Karta přehledu proto nesmí vzniknout
jen z jednoho XML nebo jedné hlavičky.

Rozlišují se nejméně:

- navigační rodičovství;
- settings link;
- záložka;
- MTP členství;
- procesní členství a výstup;
- UI otevření/vyvolání;
- action calls;
- type read/write/matching;
- segment usage;
- COMEX projection;
- page composition;
- template use.

`on_comex` samo o sobě nedokazuje efektivní viditelnost ani nasazenou stránku.

## Aktuálnost a coverage

Technická karta nebo dotaz musí uvést scope, čas sběru, revize/otisky zdrojů, stav ověření
a mezery. Nedostupný zdroj není negativní důkaz.

Z „nenalezeno“ lze udělat „v tomto scope nepoužito“ až při doloženém úplném pokrytí.

Refresh aplikační/COMEX reference je nezávislý na replikaci: save settingu, změna registrace,
build nebo PageEdit může změnit dokumentovaný stav bez nové verze XDS.

## Přenos do Project Memory

Capability je v Project Memory obsahově neinvazivní:

- nezakládá ani nemění `project/epics/`, `context/`, `.project-memory/` ani projektové stavy;
- instaluje skill, přenositelné reference a read-only validační/inventory nástroj;
- nevytváří automaticky žádnou z navržených generated reference families;
- provisioning a sémantickou validaci Memory nadále vlastní Orchestrátor/MCP.

## Instalace

~~~bash
python toolkit/agent-infrastructure/repository_architecture.py install-capability <repo> --name project-documentation
~~~

## Validace

~~~bash
python toolkit/skills/maintain-project-documentation/project_documentation.py validate .
python toolkit/skills/maintain-project-documentation/project_documentation.py inventory .
~~~

Nástroj je read-only. Neparsuje XDS jako druhý producent, negeneruje aplikační/COMEX reference
a nedotazuje živou instanci.
