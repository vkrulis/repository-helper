# Referenční model projektové dokumentace Flexideo

## 1. Účel a základní hranice

Projektová dokumentace odpovídá na otázku:

> **Co dnes v aplikaci máme a jak to funguje?**

Project Memory epik odpovídá na jinou otázku:

> **Proč jsme změnu otevřeli, co jsme zjistili, rozhodli, provedli a ověřili?**

Proto je v Project Memory základní hranice:

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
~~~

`docs/` je sdílená aktuální dokumentace celé aplikace napříč epiky. Není to archiv etap.
Historii drží Git a Project Memory.

## 2. Integrační rozhodnutí po revizi návrhu z XDS authoringu

Zdrojový návrh `client-application-documentation-proposal.md` z 28. 10. 2026 byl
obsahově zrevidován proti tomuto modelu. Přijímají se jeho významové hranice, identity,
karty, typed relations, coverage a refresh pravidla. Nepřebírá se však bez dalšího jeho
pracovní umístění ručního výkladu do `docs/agent-context/application/`, protože v cílovém
Project Memory modelu už je pro klientskou dokumentaci vyhrazeno `docs/`.

Mapování je:

| Zdrojový návrh | Cílový model Project Memory |
| --- | --- |
| ruční funkční výklad `docs/agent-context/application/functions/` | `docs/aplikace/funkce/` |
| ruční scénáře `docs/agent-context/application/scenarios/` | `docs/aplikace/scenare/` |
| datová reference FDT | `docs/reference/fdt/` |
| navržená aplikační reference | budoucí `docs/reference/application/` |
| navržená prezentační reference | budoucí `docs/reference/comex/` |
| navržená usage reference | budoucí `docs/reference/usage/` |
| navržené indexy | budoucí `docs/reference/indexes/` |

Tím se zachová jedna publikovatelná projektová dokumentace a současně nevznikne druhá
Current Truth v helperovém `docs/agent-context/`.

## 3. Dvě dokumentační vrstvy v `docs/`

### 3.1 Kurátorovaný lidský výklad

~~~text
docs/
├── index.md
├── aplikace/
├── datovy-model/
├── procesy/
├── integrace/
└── provoz/
~~~

Tato část vysvětluje účel, business význam, scénáře, odpovědnosti, výjimky,
akceptaci a provozní souvislosti. Ruční text se váže na stabilní identity technických
prvků, ale při refreshi technické reference se nepřepisuje.

### 3.2 Generované nebo odvozené technické reference

Dnes je potvrzená a produkovaná rodina:

~~~text
docs/reference/fdt/
~~~

Obsahový návrh dále počítá s rodinami:

~~~text
docs/reference/
├── application/
├── comex/
├── usage/
└── indexes/
~~~

Tyto rodiny jsou **návrh k implementaci, nikoli současný hotový kontrakt**. Dokud jejich
producenti, společný packager a manifest nepotvrdí formát, nevytvářejte je ručně jako
kanonickou reference. Pilotní nebo pracovní výstupy držte ve stagingu mimo
`docs/reference/`.

## 4. Matice autorit

| Otázka | Primární autorita | Dokumentace |
| --- | --- | --- |
| Co je požadováno a proč? | aktivní/uzavřený epic | odkazuje, nekopíruje pracovní stopu |
| Jaká je současná Current Truth? | `context/` + potvrzené promotion | shrnuje ji pro publikum aplikace |
| Jaké FDT a segmenty existují? | XDS | používá generovanou FDT referenci |
| Jak jsou XDS segmenty mapovány do DB? | DAD odvozený Replicatorem | vysvětluje významné fyzické mapování |
| Jak je složen intranet? | x-item + saved settings + registry/buildy | odvozuje aplikační technickou referenci |
| Jaké UI se skládá? | COMEX/CXD + registry komponent | odvozuje prezentační technickou referenci |
| Co je opravdu nasazeno? | konkrétní instance/release/runtime | uvádí prostředí a datum ověření |
| Jak se aplikace provozuje? | deployment/runtime konfigurace vlastníků | provozní návod bez secrets |
| Jaký je business účel? | potvrzené projektové zadání a doménová revize | ručně udržovaný funkční výklad |

Významy platformních XML uzlů zůstávají u příslušných authoringů. Projektová dokumentace
popisuje jejich **konkrétní použití v klientské aplikaci**, nikoli znovu platformní syntaxi.

## 5. Definition-driven osa Flexidea

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
 ├── UI nástroje
 ├── akce / transformace
 └── procesní uzly a vazby
        │
        ▼
COMEX/CXD
 ├── stránky a rámce
 ├── komponenty
 ├── modifikátory
 ├── šablony
 └── navigace / event connections
        │
        ▼
runtime konkrétní role / prostředí
~~~

Základ projektové dokumentace je proto propojená mapa:

> **data → aplikační funkce → použití v UI**

## 6. Generovaná FDT reference

Replicator vlastní současný balík pod:

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

Dnešní potvrzené minimum je manifest, Markdowny FDT a segmentové indexy.
`documents.jsonl` je vhodné cílové rozšíření pro explicitní klasifikaci typů;
skill nesmí jeho existenci předstírat.

Reference je odvozená. Nenahrazuje autorské XDS ani nezávislý business kontext.

### Datový FDT

Současný Replicator má technickou klasifikaci databázového dokumentu: finální
`DocumentDef`, který je ve `Definition_Group`, nemá neprázdné `view-of` a není
pseudo typem.

Tuto klasifikaci má publikovat producent nebo ji má dodat ověřený XDS specialista.
Projektová dokumentace ji nesmí znovu heuristicky odvozovat jen z jména, tabulky nebo
labelu.

## 7. `docs/datovy-model/`

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

Kurátorovaný seznam významných business objektů odkazuje na FDT reference a může uvést:

- business název;
- FDT name;
- XDS ID;
- účel;
- životní cyklus;
- citlivost/retenci podle relevance;
- odkaz do `reference/fdt/`.

Technické segmenty a pole se neopisují ručně.

### Vztahy

Rozlišujte:

1. business vztah potvrzený doménou;
2. technickou XDS referenci;
3. DAD/databázovou vazbu;
4. použití aplikační funkcí nebo UI.

Join nebo shodný DAD path sám neprokazuje business kardinalitu.

### Fyzické mapování

~~~text
business objekt
  → FDT
  → XDS segment
  → DAD array / field
  → SQL tabulka / sloupec
~~~

DAD je databázový obraz, ne nezávislý zdroj návrhu.

## 8. `docs/aplikace/`

Tato oblast je **ručně kurátorovaný výklad aktuální aplikace**. Technické karty, které
mají být regenerovatelné z instance, patří po implementaci producenta do
`docs/reference/application/`.

Doporučené členění:

~~~text
docs/aplikace/
├── index.md
├── architektura.md
├── strom-aplikace.md
├── uzivatelske-rozhrani.md
├── role-a-pristupy.md
├── funkce/
│   └── <stable-key>.md
└── scenare/
    └── <stable-key>.md
~~~

### Funkce

Funkce vysvětluje business cíl a používá odkazy na technické identity:

- role a odpovědnosti;
- vstupní místo/stránku;
- používané přehledy a akce;
- vstupní/výstupní FDT;
- běžný průchod a výjimky;
- akceptační příklady;
- odpovědného člověka a datum doménového potvrzení.

### Scénář

Scénář je uživatelský nebo provozní průchod konkrétní funkcí. Nemá nahrazovat technickou
kartu přehledu, akce ani COMEX stránky.

## 9. Technická aplikační reference — návrhový směr

Navržená budoucí rodina:

~~~text
docs/reference/application/
├── index.md
├── tree.md
├── folders/<key>.md
├── views/<key>.md
├── tools/<key>.md
├── actions/<key>.md
├── processes/<key>.md
└── projections/<key>.md
~~~

Má být odvozena z aktuálních hlaviček, settings, registrací a doložených buildů.
Nesmí se ručně udržovat jako druhý katalog.

Jedna funkční entita může zahrnovat:

1. x-item hlavičku a předky;
2. owning saved setting;
3. linkovaný zdroj settingu;
4. MTP parent/child;
5. transformaci nebo akci;
6. registraci a build;
7. procesní členství;
8. access metadata;
9. projekci do COMEXu.

Jeden XML setting nebo jedna hlavička proto nejsou úplnou kartou funkce.

## 10. Technická COMEX reference — návrhový směr

Navržená budoucí rodina:

~~~text
docs/reference/comex/
├── index.md
├── pages/<key>.md
├── components/<key>.md
├── modifiers/<key>.md
└── templates/<key>.md
~~~

COMEX je Presentation Composition Layer. Skládá existující aplikační schopnosti do
stránek, navigace, layoutu a komponent; nerefunduje jejich doménový model ani business
pravidla.

`on_comex=true` je kandidátní metadata, nikoli důkaz existence stránky, úspěšného
vygenerování, role-based visibility nebo spustitelnosti.

Pro tvrzení o skutečném UI je třeba rozlišit:

~~~text
autorský stav        → x-item + saved settings + registr
odvozená UI projekce → COMEX/CXD
skutečný stav        → nasazená definice + runtime + role
~~~

Podrobné kontrakty aplikačních a COMEX karet jsou v
[application-comex-reference.md](application-comex-reference.md).

## 11. Usage a společný index — návrhový směr

Zdrojový návrh i Replicator počítají se společnou odvozenou mapou použití. Projektová
capability nevytváří konkurenční databázi ani parser.

Budoucí rodiny mohou být:

~~~text
docs/reference/usage/
docs/reference/indexes/
~~~

Index má podporovat obousměrné hledání, například:

- FDT/segment → přehledy, sloupce, akce, procesy a COMEX stránky;
- x-item/větev → settings, MTP, nástroje, akce, FDT a UI projekce;
- akce → vyvolávající UI, další volání, čtené/zapisované typy a proces;
- stránka/komponenta → backend, FDT, nástroje, modifikátory, šablony a konzumenti.

SQLite nebo jiná databáze je obnovitelná projekce; není zdrojem pravdy a nepatří automaticky
do Gitu.

## 12. Oddělené grafy a typované vztahy

Nikdy neslučujte do jedné vazby:

- navigační rodičovství;
- settings link;
- záložku;
- MTP členství;
- procesní členství;
- procesní výstup;
- UI otevření;
- UI vyvolání akce;
- deklarované volání akce;
- staticky nalezené volání;
- typové čtení/zápis/matching;
- segmentové použití;
- projekci intranet → COMEX;
- složení stránky;
- použití šablony.

Každá hrana má mít zdrojovou a cílovou identitu, druh, podmínku, stav rozlišení a
důkaz. Stavy typu `resolved`, `ambiguous`, `dynamic`, `missing` nebo
`out-of-scope` se nesmějí převést na jednoduché true/false bez evidence.

## 13. Identity, které se nesmějí sloučit

- **X-item:** instance + document scope + oblast + PDK; `auto_id` zvlášť.
- **Setting:** instance + type/oblast + tb-id + user + language.
- **Akce:** PDK registrace, technické jméno transformace, autorský setting a build jsou
  samostatné identity.
- **Proces:** kontejner má vlastní auto_id; procesní uzel vlastní auto_id; matching na
  procesní uzel není PDK kontejneru.
- **COMEX:** stránka, instance komponenty a plný component source jsou různé entity.
- **Data:** dokumentový typ, DAD/SQL tabulka a intranetový přehled jsou různé entity.

Popisek ani pozice ve stromu nejsou stabilní identity.

## 14. `docs/procesy/`

Tato oblast dokumentuje business a uživatelské procesy, ne pouze x-item `p`.

Jeden business proces může používat více FDT, přehledů, akcí, procesních uzlů, COMEX
stránek i integrací. Vztah mezi business procesem a technickým procesním kontejnerem
musí být explicitní, nikoli předpokládaný 1:1.

Typická stránka procesu obsahuje:

- účel a trigger;
- role/aktéry;
- vstupní stav;
- hlavní kroky;
- alternativy a výjimky;
- stavové přechody;
- FDT/data;
- UI komponenty;
- akce a automatizace;
- integrace;
- výsledný stav;
- odkazy na technické reference.

## 15. `docs/integrace/`

Každá integrace má podle doložené implementace uvést:

- účel a vlastníka protistrany;
- směr/trigger;
- protokol/transport;
- autentizaci bez secrets;
- vstupní/výstupní FDT a mapování;
- konkrétní akci/službu/registraci;
- synchronní/asynchronní režim;
- timeout/retry/idempotenci;
- chybové stavy;
- testovací/provozní prostředí;
- monitoring a odpovědnost.

Přesný kontrakt vlastní strojově čitelný artefakt, pokud existuje; Markdown jej
vysvětluje a odkazuje na něj.

## 16. `docs/provoz/`

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

Dokumentace musí rozlišit **definováno**, **vydáno** a **nasazeno**.

## 17. Společná hlavička technické karty

Generovaná nebo odvozená technická karta má nést alespoň:

- stabilní identitu;
- popisek;
- účel, pokud je potvrzen;
- scope aplikace/instance/role/jazyka;
- revize/otisky zdrojů;
- čas sběru;
- stav aktuálnosti;
- stav ověření;
- coverage;
- odkazy na zdroje;
- známé mezery.

Ruční business účel má vlastní revizi a nesmí být při regeneraci technické karty ztracen.

## 18. Aktuálnost a coverage

Verze aplikace, hash zdroje a čas sběru jsou rozdílné údaje.

Pravidla:

- změna settingu může změnit dokumentaci bez nové replikace;
- změna registrace/buildů může změnit akce bez změny XDS;
- COMEX regenerace/PageEdit může změnit UI bez změny datového modelu;
- změna parseru/resolveru může vyžadovat nové vyhodnocení nezměněných zdrojů;
- smazání lze potvrdit až po úplném úspěšném sběru stejného scope;
- nedostupný zdroj se nesmí vyhodnotit jako „nepoužívá se“;
- více čtecích dávek není automaticky transakční snapshot.

Z „nenalezeno“ lze udělat „v tomto scope nepoužito“ pouze při doloženém úplném pokrytí.

## 19. Aktualizace po epiku nebo provozní změně

Při ukončení/promotion epiku:

1. identifikujte dotčené současné chování;
2. ověřte výslednou Current Truth;
3. regenerujte producentem vlastněné FDT reference, pokud se změnily definice;
4. obnovte dotčené intranetové zdroje, pokud se měnily settings/registry/buildy;
5. obnovte COMEX projekci, pokud se měnilo UI;
6. ověřte runtime jen tam, kde dokumentace tvrdí skutečné chování/viditelnost;
7. změňte kurátorovaný výklad v `docs/`;
8. historii ponechte epiku a Gitu.

Refresh aplikační nebo COMEX reference nemusí čekat na novou replikaci.

## 20. Minimální kvalita kurátorované stránky

Každá věcná stránka má umožnit zjistit:

- co popisuje;
- komu/čemu slouží;
- jaké technické identity/reference podporují tvrzení;
- jaký projekt/aplikaci/prostředí/verzi popisuje;
- kdy byla věcně ověřena;
- co nebylo ověřeno.

Doporučená závěrečná sekce:

~~~markdown
## Zdroje a aktuálnost

- Ověřeno: YYYY-MM-DD
- Scope: <projekt / aplikace / prostředí / role>
- Zdroj: <relativní odkaz nebo identita artefaktu>
- Omezení: <co tento zdroj nedokazuje>
~~~

## 21. Co do `docs/` nepatří

- pracovní otázky a hypotézy;
- syrové důkazy;
- úplné FAAM Decision Records;
- checkpointy a session logy;
- credentials a produkční osobní data;
- ručně upravená kopie generované reference;
- runtime tvrzení odvozené pouze z `on_comex`, access atributu nebo existence settingu;
- generovaný katalog bez provenance a známého producenta.

## 22. Zdrojové podklady a jejich stav

Tento model byl revidován 2026-10-28 proti:

- `Flexideo-XDS-authoring-workspace/docs/agent-context/client-application-documentation-proposal.md`
  z větve `develop`, blob `d604e20506ee333137b252d85eb0c20b2a3d6eb4`;
- jeho ADR-0027, který je nadále `proposed`;
- Replicator `application-documentation-index-architecture.md` a ADR-0046, rovněž proposal
  pro společný usage/index kontrakt;
- Intranet authoring application-tree/action dokumentaci;
- COMEX authoring architekturu a kanonický validační skill;
- existující FDT reference kontrakt a epic-first Project Memory kontrakt.

Proto se obsahové principy přijímají do této capability, ale **nové generované rodiny
`application/comex/usage/indexes` se nevydávají za implementované ani za již přijatý
packager kontrakt**.
