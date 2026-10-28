# Referenční model projektové dokumentace Flexideo

## 1. Účel a základní hranice

Projektová dokumentace odpovídá na otázku:

> **Co dnes v aplikaci máme a jak to funguje?**

Project Memory epik odpovídá na jinou otázku:

> **Proč jsme změnu otevřeli, co jsme zjistili, rozhodli, provedli a ověřili?**

Proto je v Project Memory 0.2 základní hranice:

~~~text
project/
├── epics/
│   ├── EPIC-0001/
│   └── EPIC-0002/
└── visions/

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

`docs/` je sdílená aktuální dokumentace celé aplikace napříč epiky. Není to archiv etap.
Historii drží Git a Project Memory.

## 2. Matice autorit

| Otázka | Primární autorita | Dokumentace |
| --- | --- | --- |
| Co je požadováno a proč? | aktivní/uzavřený epic | odkazuje, nekopíruje pracovní stopu |
| Jaká je současná Current Truth? | `context/` + potvrzené promotion | shrnuje ji pro publikum aplikace |
| Jaké FDT a segmenty existují? | XDS | používá generovanou FDT referenci |
| Jak jsou XDS segmenty mapovány do DB? | DAD odvozený Replicatorem | vysvětluje významné fyzické mapování |
| Jak je složen intranet? | x-item + saved settings + registry | vytváří karty komponent a mapu aplikace |
| Jaké UI se generuje? | COMEX/CXD + nasazené artefakty | popisuje uživatelský obraz |
| Co je opravdu nasazeno? | konkrétní instance/release | uvádí prostředí a datum ověření |
| Jak se aplikace provozuje? | deployment/runtime konfigurace vlastníků | provozní návod bez secrets |

## 3. Definition-driven osa Flexidea

Flexideo aplikace se nechápe jako ručně sestavený soubor formulářů. Základní osa je:

~~~text
XDS
 ├── definuje FDT a jejich strukturu
 ├── deklaruje zdroje, přístupy a chování
 └── je vstupem pro Replicator
        │
        ├── FDT
        ├── DAD
        ├── formulářové a konfigurační artefakty
        └── instalovatelnou verzi

Intranet
 ├── x-item hlavičky a strom
 ├── saved settings
 ├── přehledy / tabulky
 ├── akce / transformace
 └── procesní uzly a vazby
        │
        ▼
COMEX/CXD
 ├── komponenty
 ├── nástroje
 └── stránky / výsledné UI
~~~

Tento tok určuje dokumentační strategii: každá vrstva má svého vlastníka a `docs/`
je spojuje do čitelného současného obrazu.

## 4. Generovaná FDT reference

Replicator vlastní balík pod:

~~~text
docs/reference/fdt/
├── manifest.json
├── index.md
├── fdt/
│   ├── index.md
│   └── <name>.md
└── indexes/fdt/
    ├── segments.jsonl
    ├── by-xds-id.json
    └── documents.jsonl        # volitelné/cílové doplnění producenta
~~~

Dnešní potvrzené minimum je manifest, Markdowny FDT a segmentové indexy. `documents.jsonl`
je vhodné cílové rozšíření pro explicitní klasifikaci dokumentových typů; skill nesmí jeho
existenci předstírat.

Reference je odvozená. Obsahuje technický výklad a DAD vazby, ale nenahrazuje autorské XDS
ani nezávislý business kontext.

### Datový FDT

Současný Replicator má technickou klasifikaci databázového dokumentu: finální
`DocumentDef`, který:

- je v `Definition_Group`;
- nemá neprázdné `view-of`;
- není pseudo typem.

Tuto klasifikaci má publikovat producent nebo ji má dodat ověřený XDS specialista. Projektová
dokumentace ji nesmí znovu heuristicky odvozovat jen z jména, tabulky nebo labelu.

Pohledové FDT a pseudo typy jsou důležité, ale obvykle představují projekce/pomocné vrstvy,
nikoli primární business datové entity.

## 5. `docs/datovy-model/`

Tato oblast není ruční kopií XDS.

Doporučené stránky:

~~~text
docs/datovy-model/
├── index.md
├── datove-objekty.md
├── vztahy.md
├── stavove-modely.md
├── ciselniky.md
└── fyzicke-mapovani.md
~~~

### Datové objekty

Kurátorovaný seznam významných business objektů odkazuje na FDT reference:

- business název;
- FDT name;
- XDS ID;
- účel;
- životní cyklus;
- citlivost/retence, pokud je relevantní;
- odkaz do `reference/fdt/`.

Technické segmenty a pole se neopisují ručně.

### Vztahy

Rozlišujte:

1. **business vztah** – význam potvrzený doménou;
2. **technickou XDS referenci** – zdroj/foreign/source vztah;
3. **DAD/databázovou vazbu** – fyzické nebo logické mapování;
4. **UI použití** – přehled či akce, která typ čte/zapisuje.

Join nebo shodný DAD path sám neprokazuje business kardinalitu.

### Fyzické mapování

Vysvětlujte tok:

~~~text
business objekt
  → FDT
  → XDS segment
  → DAD array / field
  → SQL tabulka / sloupec
~~~

DAD je databázový obraz, ne nezávislý zdroj návrhu.

## 6. Intranetová vrstva a `docs/aplikace/`

Intranet definuje aplikační kompozici nad datovými typy.

Základní x-item druhy relevantní pro klientskou dokumentaci:

- `f` – složka;
- `t` – přehled/tabulka; často také nosič akce/transformace;
- `p` – procesní kontejner;
- další typy existují a dokumentují se podle potřeby, ne plošným zjednodušením.

Jedna funkční entita může vyžadovat společné čtení:

1. identity instance/role;
2. x-item hlavičky a rodičovské cesty;
3. owning saved setting;
4. případného settings linku;
5. MTP parent/child přehledů;
6. `table/transformation`, akce, registrace a buildů;
7. access metadata a COMEX příznaku.

Jeden table XML soubor proto nemusí popsat celou funkci.

### Oddělené grafy

Nikdy neslučujte do jedné „vazby“:

- navigační rodičovství (`fdk1`);
- procesní členství (`to_process_id` / odpovídající compiled pole);
- settings link;
- procesní výstupní hrany;
- action-call graph;
- UI nástroje/přechody.

### Doporučené členění

~~~text
docs/aplikace/
├── index.md
├── architektura.md
├── strom-aplikace.md
├── uzivatelske-rozhrani.md
├── role-a-pristupy.md
└── komponenty/
    └── <stabilni-slug>.md
~~~

Nejde o povinné scaffoldované soubory; jde o preferované rozdělení, pokud je projekt potřebuje.

### Karta komponenty

Karta může mít:

- **Účel a uživatelský význam**
- **Typ komponenty**: složka / přehled / akce / procesní uzel / jiný
- **Identita**: oblast, scope shared/user, PDK, auto_id
- **Navigace**: rodič a cesta
- **Zdroj settings**: type, tb-id, user/role; případný link
- **Data**: čtené/zapisované FDT a významné segmenty
- **Přehled**: hlavní selecty, filtry, grouping a MTP
- **Akce**: transformace, registry, vstupy/výstupy, dostupná prostředí
- **Proces**: membership, output edges, automatické registrace
- **COMEX**: stránka, komponenty, nástroje a přechody
- **Viditelnost**: raw metadata + stav ověření
- **Zdroje a aktuálnost**

Technická karta může být částečně generovaná v budoucnu. Ruční business výklad má zůstat
oddělený od regenerovaných bloků.

## 7. COMEX: projekce uživatelského rozhraní

COMEX není druhý autorský strom. Vzniká z XDS/intranetových nastavení a obsahuje provozní
popis potřebný pro formuláře, komponenty, přehledy, filtry, akce a stránky.

Dokumentace rozlišuje:

~~~text
autorský stav        → x-item + saved settings + registr
odvozená UI projekce → COMEX/CXD
skutečný uživatelský stav → nasazený runtime + role
~~~

Důsledky:

- `on_comex=true` neznamená, že je prvek viditelný všem uživatelům;
- uložený setting není důkaz totožné nasazené CXD;
- administrátorský snapshot neprokazuje UI běžné role;
- explicitní tool není jediná cesta k editaci/náhledu; existují defaultní a legacy cesty.

Pro tvrzení „uživatel v roli X vidí Y“ potřebujete odpovídající roli/runtime nebo jiný
doložený důkaz.

## 8. `docs/procesy/`

Tato oblast dokumentuje business a uživatelské procesy, ne pouze x-item `p`.

Jeden business proces může používat:

- více FDT;
- více přehledů;
- ruční i automatické akce;
- několik procesních uzlů;
- COMEX stránky;
- externí integraci.

Stránka procesu má typicky:

- účel a trigger;
- role/aktéry;
- vstupní stav;
- hlavní kroky;
- alternativy a výjimky;
- stavové přechody;
- používaná data/FDT;
- komponenty UI;
- akce a automatizace;
- integrace;
- výsledný stav;
- odkazy na technické zdroje.

X-item procesní kontejner je technická implementační entita. Business proces je dokumentační
koncept; vztah mezi nimi má být explicitní, nikoli předpokládaný 1:1.

## 9. `docs/integrace/`

Každá integrace má uvádět:

- účel a vlastníka protistrany;
- směr/trigger;
- protokol/transport;
- autentizaci bez secrets;
- vstupní/výstupní FDT a mapování;
- konkrétní akci/službu/registraci;
- synchronní/asynchronní režim;
- timeout/retry/idempotenci podle doložené implementace;
- chybové stavy;
- testovací/provozní prostředí;
- monitoring a odpovědnost.

Pokud přesný kontrakt vlastní OpenAPI, XML schéma nebo jiný strojový artefakt, Markdown jej
vysvětluje a odkazuje na něj; neopisuje jej ručně.

## 10. `docs/provoz/`

Doporučené oblasti:

- prostředí a instance;
- release/deployment;
- konfigurace bez secrets;
- monitoring/alerting;
- plánované úlohy a joby;
- zálohy/obnova;
- incident/troubleshooting;
- rollback;
- externí provozní závislosti.

Dokumentace musí rozlišit „definováno“, „vydáno“ a „nasazeno“.

## 11. `docs/index.md`

Vstupní stránka má rychle vysvětlit:

- účel aplikace;
- hlavní uživatelské role;
- hlavní funkční oblasti;
- hlavní business datové objekty;
- hlavní procesy;
- externí systémy;
- provozní prostředí;
- mapu dokumentace;
- datum/scope poslední věcné revize.

Není to changelog ani seznam epiků.

## 12. Aktualizace po změně

Při ukončení nebo promotion epiku:

1. identifikovat dotčené současné chování;
2. ověřit výslednou Current Truth;
3. regenerovat technické reference vlastněné producenty;
4. znovu načíst dotčené intranetové settings/registry, pokud se měnily;
5. ověřit COMEX/runtime tam, kde dokumentace tvrdí skutečné UI;
6. změnit jen dotčené části `docs/`;
7. odkazy na původní epic/Decision ponechat jako provenance, ne jako současný výklad;
8. spustit validační/inventory nástroj.

## 13. Generované reference a budoucí rozšíření

Dnes je potvrzená generovaná oblast:

~~~text
docs/reference/fdt/
~~~

Budoucí oblasti:

~~~text
docs/reference/intranet/
docs/reference/comex/
~~~

jsou **rezervovaný návrhový směr**, nikoli povinný současný kontrakt. Nezakládejte je, dokud
existující authoring/producer neurčí formát, manifest, úplnost a aktualizační pravidlo.

## 14. Minimální kvalita stránky

Každá věcná stránka má umožnit zjistit:

- co popisuje;
- komu/čemu slouží;
- jaké zdroje ji podporují;
- zda jde o kurátorovaný nebo generovaný obsah;
- jaký projekt/aplikaci/prostředí/verzi popisuje, pokud je to relevantní;
- co nebylo ověřeno.

Doporučená závěrečná sekce:

~~~markdown
## Zdroje a aktuálnost

- Ověřeno: YYYY-MM-DD
- Scope: <projekt / aplikace / prostředí / role>
- Zdroj: <relativní odkaz nebo identita artefaktu>
- Omezení: <co tento zdroj nedokazuje>
~~~

## 15. Co do `docs/` nepatří

- pracovní otázky a hypotézy;
- syrové důkazy;
- úplné FAAM Decision Records;
- checkpointy a session logy;
- credentials a produkční osobní data;
- ručně upravená kopie generované FDT reference;
- „runtime pravda“ odvozená pouze z `on_comex`, access atributu nebo existence settingu;
- generovaný katalog bez provenance a bez známého producenta.

## 16. Validace

Přenositelný nástroj capability je read-only:

~~~bash
python toolkit/skills/maintain-project-documentation/project_documentation.py validate .
python toolkit/skills/maintain-project-documentation/project_documentation.py inventory .
~~~

Potom se vždy spouští validace vlastníka Project Memory nebo cílového repozitáře.


## 17. Zdrojové podklady modelu

Tato reference byla sestavena z aktuálně dostupných autoritativních a expertních podkladů
k 2026-10-28:

- `Flexideo-orchestrator-workspace/docs/agent-context/decisions/0065-epic-first-project-memory.md`
  a `docs/agent-context/domain/project-memory-repository-contract.md` – hranice epiků,
  sdíleného kontextu a `docs/`.
- `Flexideo-replicator-workspace/docs/agent-context/fdt-reference-package.md` – generovaný
  FDT/DAD referenční balík, manifest, indexy a jejich vlastnictví.
- `Flexideo-replicator-workspace/product/CReplicXdsUtilities.vb` – současná technická
  klasifikace databázového dokumentového typu versus view/pseudo.
- `flexideo-public-documentation/supp-fxd-concept-cz/Definition-driven/index.md` –
  definition-driven vztah XDS → FDT → DAD → Replicator → Intranet → COMEX.
- `Flexideo-intranet-authoring/docs/agent-context/application-tree/` – x-item topologie,
  saved settings, MTP, procesní vazby, viditelnost a analytické workflow.
- `Flexideo-intranet-authoring/docs/agent-context/action-settings/` a registry – akce,
  vstupy/výstupy, prostředí a vazby na UI.
- `Flexideo-orchestrator-workspace/docs/agent-context/application-reference-usage-proposal.md`
  – role FDT reference jako technického slovníku a hranice business výkladu.

Konkrétní klientská dokumentace musí vždy ověřit, že použité reference, instance, role a
verze patří ke stejnému aplikačnímu scope. Shodný název nebo číslo verze samo o sobě
neprokazuje shodu obsahu.
