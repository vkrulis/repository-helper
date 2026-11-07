# DOporučené rozdělení Flexideo repozitářů

Stav rozhodnutí: 2026-07-23 (bráno jako silné doporučení, nikoli MUST BE)

Tento dokument shrnuje finální doporučení pro rozdělení autoritativních Git repozitářů pro vývoj Flexideo, jeho běhové produkty, agentní schopnosti a tři vrstvy tvorby aplikace. Rozdělení vychází z principu, že každý repozitář má vlastnit jednu dlouhodobě stabilní odpovědnost a nemá směšovat:

- implementaci běhového produktu;
- agentní znalosti a skilly pro jeho používání;
- hostitelské uživatelské rozhraní;
- obecnou platformní dokumentaci;
- zákaznická data a pracovní mezivýstupy.

Výsledná struktura obsahuje devět autoritativních repozitářů:

```text
fxdReplicator_NET
fxdIntranet_NET
fxd-intranet-web
fxd-xds-authoring
fxd-intranet-authoring
fxd-comex-authoring
fdt-templates
documentation
!repository-helper
```

---

## Základní architektonické pravidlo

Repozitáře se dělí na dvě hlavní skupiny:

1. **Runtime a produktové repozitáře** vlastní skutečnou implementaci, build, serverová nebo strojová rozhraní a programátorské skilly pro změny jejich kódu.
2. **Authoring repozitáře** vlastní znalost domény, skilly, agenty, workflow a klienty rozhraní, pomocí kterých se vytváří nebo konfiguruje výsledná Flexideo aplikace.

Z toho plyne:

> Runtime repozitář vlastní implementaci a rozhraní, které produkt skutečně poskytuje. Authoring repozitář vlastní znalost, jak toto rozhraní bezpečně a účelně používat.

Agentní schopnosti proto nejsou automaticky součástí produktu, kterého se týkají. Mohou pracovat s Replicatorem nebo Intranetem, ale mají zůstat nezávislé na tom, zda jsou spuštěny z Codexu, konzole, chatovacího okna, desktopového hostitele, webového klienta nebo přes MCP.

---

# 1. `fxdReplicator_NET`

## Hlavní odpovědnost

Autoritativní repozitář pro implementaci Replicatoru ve VB.NET.

Repozitář vlastní způsob, jakým je Replicator naprogramován, sestaven, testován a zpřístupněn uživatelským nebo strojovým klientům.

## Obsah

- GUI Replicator;
- konzolový a Headless Replicator;
- sdílené replikační jádro;
- kompletace XDS;
- syntaktická validace;
- tvorba DAD, rolí, stránek a dalších replikačních výstupů;
- instalační kroky;
- vestavěný XDS Designer;
- technická dokumentace dual-mode GUI/Headless architektury;
- build, testy a diagnostické nástroje;
- skilly pro bezpečné programování a refaktoring VB.NET Replicatoru;
- případné API, CLI kontrakty nebo MCP server Replicatoru.

## Agentní obsah

Agentní skilly v tomto repozitáři slouží k vývoji samotného Replicatoru, například:

- úpravy VB.NET kódu;
- zachování hranic GUI a Headless režimu;
- práce s třídami uživatelského vstupu;
- změny validačního jádra;
- regresní kontrola replikačních fází;
- vývoj a testování MCP nebo jiného strojového rozhraní.

Nejde o skilly pro obecnou tvorbu zákaznických XDS aplikací.

## Doporučená struktura

```text
fxdReplicator_NET/
├─ src/
│  ├─ gui/
│  ├─ headless/
│  ├─ shared/
│  ├─ designer/
│  └─ integrations/
│     └─ mcp/
├─ docs/
│  ├─ architecture/
│  ├─ development/
│  └─ contracts/
├─ .agents/
│  └─ skills/
├─ toolkit/
└─ tests/
```

## Co sem nepatří

- obecná XDS reference pro tvorbu aplikací;
- workflow analýza → XDS → replikace;
- uživatelské skilly pro tvorbu Flexideo aplikace;
- intranetová konfigurace;
- Comex authoring;
- obecná platformní dokumentace.

---

# 2. `fxdIntranet_NET`

## Hlavní odpovědnost

Autoritativní repozitář desktopového hostitelského rámce Intranetu ve VB.NET.

Repozitář vlastní aplikaci, která hostuje webové rozhraní Flexideo Intranetu a případně také agentní nebo chatovací panel.

## Obsah

- WinForms shell;
- WebView nebo WebView2 hostitel;
- přihlášení;
- komunikace se serverem;
- lokální konfigurace;
- zoom, refresh a životní cyklus okna;
- ukládání lokálního stavu;
- technická integrace agentního okna;
- předávání kontextu mezi webem, desktopovým hostitelem a agentem;
- programátorské skilly pro údržbu VB.NET hostitele.

## Agentní okno

Repozitář může obsahovat technickou implementaci agentního okna nebo jeho hostování, ale nevlastní samotné znalosti XDS, replikace, intranetových settings ani Comexu.

Hostitel může například:

- otevřít agentní panel;
- předat agentovi aktivní dokument, stránku nebo settings;
- zobrazit návrh změny;
- vyžádat potvrzení;
- odeslat schválenou operaci příslušnému runtime rozhraní.

Samotné skilly a doménová dokumentace se načítají z authoring repozitářů.

## Doporučená struktura

```text
fxdIntranet_NET/
├─ src/
│  ├─ shell/
│  ├─ web-host/
│  ├─ authentication/
│  ├─ server-communication/
│  └─ agent-host/
├─ docs/
├─ .agents/
│  └─ skills/
├─ toolkit/
└─ tests/
```

## Co sem nepatří

- produkční skripty intranetového webu;
- obecná reference intranetových settings;
- skilly pro návrh intranetových komponent;
- skilly pro finální konfiguraci stránek v Comexu;
- serverová implementace intranetového MCP rozhraní.

---

# 3. `fxd-intranet-web`

## Hlavní odpovědnost

Autoritativní repozitář samotné intranetové webové aplikace a jejího deterministického runtime.

Intranet musí být plně funkční i bez AI a bez připojeného agentního systému. Tento repozitář proto obsahuje vše, co je skutečně nasazováno a provozováno jako webová část Intranetu.

## Obsah

- produkční JavaScript;
- XSL a XSLT;
- CSS a styly;
- HTML a stránky;
- menu a navigace;
- runtime zpracování table settings;
- klientské akce, filtry a algoritmy;
- komunikační vrstva webu;
- testy webového runtime;
- skilly pro programování JavaScriptu, XSL, stránek a stylů;
- případný MCP server nebo jiné strojové rozhraní Intranetu.

## Agentní obsah

Agentní skilly zde slouží pouze k vývoji webové aplikace, například:

- změna algoritmu ve skriptu;
- úprava XSL transformace;
- přidání stránky nebo stylu;
- implementace nové podporované vlastnosti settings;
- vytvoření serverového nebo klientského komunikačního rozhraní.

Nejde o skilly, které používají běžní agenti k návrhu konkrétního přehledu nebo změně konfigurace zákaznické aplikace.

## MCP a další strojová rozhraní

Pokud Intranet zpřístupní MCP server, patří jeho implementace sem, protože je přímo spojena s možnostmi a verzí webového runtime.

MCP server může například poskytovat:

- načtení settings;
- získání kontextu aktivního přehledu;
- výpis podporovaných operací;
- provedení validované změny;
- předání změny uživatelskému rozhraní;
- návrat diagnostických informací.

## Doporučená struktura

```text
fxd-intranet-web/
├─ src/
│  ├─ scripts/
│  ├─ transforms/
│  ├─ styles/
│  ├─ pages/
│  ├─ menu/
│  ├─ settings-runtime/
│  └─ integrations/
│     └─ mcp/
├─ docs/
│  ├─ architecture/
│  ├─ development/
│  └─ contracts/
├─ .agents/
│  └─ skills/
├─ toolkit/
└─ tests/
```

## Co sem nepatří

- obecné skilly pro manipulaci s intranetovými settings;
- agentní orchestrace konfigurace zákaznické aplikace;
- znalostní dokumentace určená nezávislým agentům;
- desktopový hostitel;
- Comex authoring.

---

# Rodina `fxd-authoring`

`fxd-authoring` je zastřešující název celého procesu tvorby Flexideo aplikace. Proces má tři odlišné vrstvy a každá vrstva používá jiné agenty, znalosti a komunikační prostředky.

```text
1. XDS authoring
   analýza → XDS → validace → replikace → funkční základ

2. Intranet authoring
   funkční základ → komponenty a konfigurace běžící aplikace

3. Comex authoring
   komponenty → finální stránky a uživatelské rozhraní
```

Tyto tři vrstvy jsou reprezentovány samostatnými repozitáři:

```text
fxd-xds-authoring
fxd-intranet-authoring
fxd-comex-authoring
```

Samostatný kořenový repozitář `fxd-authoring` není nyní nutný. Název slouží jako společná rodina a terminologický rámec. Společný koordinační agent nebo end-to-end dokumentace mohou být později přidány do samostatného lehkého repozitáře, pokud pro to vznikne konkrétní potřeba.

---

# 4. `fxd-xds-authoring`

## Hlavní odpovědnost

Autoritativní repozitář první vrstvy tvorby Flexideo aplikace:

```text
analýza → XDS → validace → kompletace → replikace → funkční základ
```

Klíčovou odpovědností této vrstvy je authoring XDS: analýza, návrh, tvorba, validace a dlouhodobá údržba XDS definice aplikace. Proto je `authoring` v názvu klíčovým pojmem a `xds` přesněji vyjadřuje předmět práce než původní `replication`.

Replikace je tvorba funkčního základu aplikace řízená XDS definicí. Výsledná aplikace je odrazem XDS a všechny replikační kroky, včetně pozdějších drobných i rozsáhlých aktualizací a opakované replikace, se řídí touto definicí. Replicator je vykonavatelem procesu; autoritativním zdrojem návrhu zůstává XDS.

## Obsah

- XDS reference;
- živé schéma a `schema.mxl`;
- terminologie XDS;
- pravidla návrhu dokumentů, oblastí, prvků, šablon a services;
- analýza požadavků a převod do XDS;
- validace a opravy XDS;
- workflow jednotlivých replikačních fází;
- práce s Headless Replicatorem;
- bezpečnostní pravidla instalace;
- katalog validačních chyb;
- doplňování dokumentace do XDS;
- klient CLI nebo MCP rozhraní Replicatoru;
- agenti a skilly první authoring vrstvy.

## Vztah k Replicatoru

`fxdReplicator_NET` vlastní implementaci Replicatoru a formální kontrakt jeho rozhraní.

`fxd-xds-authoring` vlastní:

- znalost, kdy a jak Replicator použít;
- skládání operací do workflow;
- návrh XDS;
- interpretaci chyb;
- přípravu vstupů;
- vyhodnocení výsledků;
- bezpečné potvrzování změn.

Stejné skilly musí být použitelné:

- přímo vývojovým agentem;
- z konzolového workflow;
- z budoucího agentního okna v GUI Replicatoru;
- prostřednictvím MCP klienta;
- z jiného uživatelského rozhraní.

## Sloučení současných oblastí

Do tohoto repozitáře se sjednotí dosavadní oblasti:

- `xds-design`;
- `replication`;
- `xds-doc-add`.

Nejde o tři nezávislé domény, ale o specializované části jednoho procesu authoringu a údržby XDS, ze kterého se replikací vytváří funkční základ aplikace.

## Doporučená struktura

```text
fxd-xds-authoring/
├─ docs/
│  ├─ analysis/
│  ├─ xds-reference/
│  ├─ authoring/
│  ├─ validation/
│  ├─ replication/
│  └─ application-development/
├─ resources/
│  ├─ schema.mxl
│  ├─ terminology/
│  ├─ examples/
│  └─ replicator-contracts/
├─ .agents/
│  ├─ agents/
│  └─ skills/
│     ├─ xds-design/
│     ├─ xds-validation/
│     ├─ flexideo-replication/
│     ├─ xds-validator-fixes/
│     └─ xds-node-documentation/
├─ toolkit/
│  ├─ schema-reader/
│  ├─ xds-analysis/
│  ├─ replicator-client/
│  └─ documentation-enrichment/
├─ tests/
└─ outputs/
```

## Co sem nepatří

- VB.NET implementace Replicatoru;
- programátorské skilly pro změny Replicatoru;
- runtime skripty Intranetu;
- intranetová konfigurace běžící aplikace;
- finální konfigurace stránek v Comexu.

---

# 5. `fxd-intranet-authoring`

## Hlavní odpovědnost

Autoritativní repozitář druhé vrstvy tvorby Flexideo aplikace: konfigurace komponent a struktur v běžícím funkčním základu aplikace.

Tato vrstva dnes odpovídá intranetové konfigurační mezivrstvě. V budoucnu může být částečně nebo úplně nahrazena moderní vrstvou Comex, ale současný název má respektovat zavedenou terminologii a reálnou odpovědnost.

## Obsah

- popis intranetových settings;
- table settings;
- konfigurace komponent v aplikačním stromu;
- menu XMN;
- přehledy, filtry a akce;
- capability registry podporovaných vlastností;
- diagnostické scénáře;
- návody a příklady konfigurace;
- skilly pro návrh a manipulaci s konfigurací;
- agenti druhé authoring vrstvy;
- klienti a adaptéry pro MCP, chatovací okno, browser nebo desktopového hostitele;
- budoucí komunikace s třetí vrstvou a uživatelským rozhraním aplikace.

## Nezávislost na komunikačním kanálu

Schopnosti tohoto repozitáře nesmějí být svázány s jedním konkrétním UI.

Mohou být použity:

- samostatným agentem;
- z klientského JavaScriptu;
- z chatovacího okna;
- z desktopového hostitele;
- přes MCP server Intranetu;
- prostřednictvím budoucího moderního rozhraní stránek.

Repozitář proto vlastní znalost a klientské workflow, nikoli serverovou implementaci komunikačních rozhraní.

## Vztah k `fxd-intranet-web`

`fxd-intranet-web` vlastní:

- implementaci settings;
- skutečné webové algoritmy;
- runtime a podporované operace;
- MCP server nebo jiné strojové rozhraní.

`fxd-intranet-authoring` vlastní:

- popis významu settings;
- návrhové postupy;
- skilly pro vytváření a změny konfigurace;
- interpretaci možností rozhraní;
- klienta a bezpečné workflow změn.

## Doporučená struktura

```text
fxd-intranet-authoring/
├─ docs/
│  ├─ settings-reference/
│  ├─ components/
│  ├─ overview-design/
│  ├─ menu/
│  ├─ actions/
│  └─ diagnostics/
├─ resources/
│  ├─ schemas/
│  ├─ capability-registry/
│  ├─ examples/
│  └─ interface-contracts/
├─ .agents/
│  ├─ agents/
│  └─ skills/
│     ├─ intranet-settings/
│     ├─ intranet-components/
│     ├─ intranet-table-design/
│     ├─ intranet-menu/
│     └─ intranet-diagnostics/
├─ toolkit/
│  ├─ settings-analysis/
│  ├─ change-proposals/
│  ├─ diff/
│  └─ adapters/
│     ├─ mcp/
│     ├─ browser-client/
│     ├─ chat-window/
│     └─ application-ui/
└─ tests/
```

## Budoucí vývoj vrstvy

Pokud moderní Comex postupně převezme všechny schopnosti současné intranetové mezivrstvy, může nastat:

- postupné přesouvání jednotlivých skillů do `fxd-comex-authoring`;
- zachování repozitáře pouze pro starší aplikace;
- archivace po úplném ukončení mezivrstvy.

Není však vhodné přejmenovávat současnou vrstvu předem podle budoucí architektury, která ještě není skutečným stavem systému.

---

# 6. `fxd-comex-authoring`

## Hlavní odpovědnost

Autoritativní repozitář třetí vrstvy tvorby Flexideo aplikace: finální konfigurace stránek a uživatelského rozhraní v Comexu.

`Comex` je terminus technicus, proto se nepoužívá obecnější název jako `pages` nebo `ui`.

## Obsah

- znalost Comexu;
- tvorba a konfigurace stránek;
- skládání komponent;
- layout a rozmístění;
- vazby mezi komponentami;
- nastavení parametrů;
- akce a interakce dostupné v UI;
- skilly pro změny prostřednictvím uživatelského rozhraní;
- agenti třetí authoring vrstvy;
- adaptéry pro komunikaci s Comexem;
- pravidla bezpečného návrhu, náhledu a potvrzení změn.

## Vztah k předchozím vrstvám

Vrstva Comexu může používat výsledky obou předchozích vrstev:

- z replikační vrstvy přebírá základní datové a aplikační struktury;
- z intranetové vrstvy přebírá nakonfigurované komponenty a jejich schopnosti;
- z těchto prostředků vytváří výsledné stránky a uživatelské rozhraní.

Do budoucna může Comex převzít část nebo všechny odpovědnosti dnešní intranetové konfigurační mezivrstvy.

## Doporučená struktura

```text
fxd-comex-authoring/
├─ docs/
│  ├─ comex-reference/
│  ├─ pages/
│  ├─ components/
│  ├─ layouts/
│  ├─ interactions/
│  └─ workflows/
├─ resources/
│  ├─ schemas/
│  ├─ capability-registry/
│  ├─ examples/
│  └─ interface-contracts/
├─ .agents/
│  ├─ agents/
│  └─ skills/
│     ├─ comex-pages/
│     ├─ comex-layout/
│     ├─ comex-components/
│     └─ comex-interactions/
├─ toolkit/
│  ├─ page-analysis/
│  ├─ change-proposals/
│  ├─ preview/
│  └─ adapters/
└─ tests/
```

## Co sem nepatří

- implementace samotného Comex runtime, pokud je součástí jiného produktu;
- obecná intranetová konfigurace, která není prováděna přes Comex;
- XDS a replikace;
- VB.NET hostitelský rámec.

---

# 7. `fdt-templates`

## Hlavní odpovědnost

Autoritativní repozitář pro tvorbu tiskových šablon FDT.

## Obsah

- XSLT 1.0 pro tiskové výstupy;
- HTML tiskové vzory;
- layout a styly dokladů;
- anonymizované FDT/XML vstupy;
- očekávané výstupy;
- renderovací, porovnávací a anonymizační nástroje;
- skilly pro tvorbu a údržbu tiskových šablon.

## Důvod samostatnosti

FDT šablony mají:

- vlastní výstup;
- vlastní testovací postup;
- samostatný životní cyklus;
- možnost oddělené distribuce;
- potenciálně odlišná přístupová pravidla pro zákaznické varianty.

## Doporučená struktura

```text
fdt-templates/
├─ templates/
├─ samples/
│  ├─ inputs/
│  └─ expected/
├─ docs/
├─ .agents/
│  └─ skills/
├─ toolkit/
└─ outputs/
```

---

# 8. `documentation`

## Hlavní odpovědnost

Autoritativní repozitář kanonických a historických dokumentačních zdrojů Flexideo a jejich transformační nebo publikační pipeline.

## Obsah

- dokumentační XML;
- DTD, XSD a XSL;
- historické číslované dokumentační struktury;
- čtečky dokumentačního XML;
- převod publikovaného HTML do Markdownu;
- generované ukázky;
- publikační nástroje;
- dokumentační doménové skilly.

## Hranice

Repozitář není obecné skladiště všech Markdown dokumentů. Projektově specifická dokumentace zůstává u projektu, kterého se týká.

Může však vytvářet verzované referenční balíčky, které používají authoring repozitáře.

## Doporučená struktura

```text
documentation/
├─ sources/
├─ schemas/
├─ transforms/
├─ generated/
├─ examples/
├─ docs/
├─ .agents/
│  └─ skills/
└─ toolkit/
```

---

# 9. `!repository-helper`

## Hlavní odpovědnost

Vlastnický repozitář této dokumentace a pomocných podkladů pro správu architektury a členění repozitářů. Uchovává dokumenty, které popisují samotnou organizaci repozitářů a nepatří do žádné produktové ani authoring domény.

## Obsah

- tato architektonická dokumentace;
- pravidla a pomocné podklady pro správu repozitářů;
- nástroje související s údržbou seznamu a struktury repozitářů.

---

# Umístění MCP a dalších rozhraní

## Serverová část

Server nebo provider patří do repozitáře produktu, jehož skutečné funkce zpřístupňuje.

```text
fxdReplicator_NET
└─ MCP server Replicatoru

fxd-intranet-web
└─ MCP server Intranetu
```

Důvody:

- server musí odpovídat aktuální implementaci produktu;
- musí znát skutečně podporované operace;
- jeho kontrakt se mění společně s runtime;
- bezpečnostní omezení musí být vynucena na straně produktu;
- testy serveru patří k testům implementace.

## Klientská a agentní část

Klient, adaptér a orchestrace patří do authoring repozitáře.

```text
fxd-xds-authoring
└─ klient Replicator CLI/MCP

fxd-intranet-authoring
└─ klient Intranet MCP/web/chat/UI

fxd-comex-authoring
└─ klient nebo adaptér Comex rozhraní
```

Authoring repozitář rozhoduje:

- jaký nástroj použít;
- kdy operaci spustit;
- jak připravit vstupy;
- jak interpretovat výsledek;
- jak vytvořit diff nebo náhled;
- kdy vyžádat potvrzení uživatele.

---

# Vztahy a směr závislostí

Doporučený směr závislostí:

```text
fxdReplicator_NET
        ▲
        │ CLI / MCP / kontrakty
        │
fxd-xds-authoring


fxd-intranet-web
        ▲
        │ MCP / webové rozhraní / kontrakty
        │
fxd-intranet-authoring


Comex runtime nebo UI
        ▲
        │ uživatelské nebo strojové rozhraní
        │
fxd-comex-authoring
```

Hostitelský rámec může jednotlivé vrstvy spojovat:

```text
fxdIntranet_NET
├─ hostuje fxd-intranet-web
├─ může hostovat agentní okno
└─ předává kontext authoring agentům
```

Nemá však vlastnit jejich znalosti.

---

# Tři vrstvy tvorby Flexideo aplikace

## Vrstva 1: Replication

```text
analýza
→ návrh XDS
→ vytvoření nebo úprava XDS
→ validace
→ kompletace
→ replikace
→ funkční základ aplikace
```

Autoritativní repozitář:

```text
fxd-xds-authoring
```

Použitý runtime nástroj:

```text
fxdReplicator_NET
```

## Vrstva 2: Intranet

```text
funkční základ aplikace
→ připojení k běžícímu serveru
→ tvorba komponent
→ intranetová konfigurace
→ settings, menu, přehledy a akce
```

Autoritativní repozitář schopností:

```text
fxd-intranet-authoring
```

Použitý runtime:

```text
fxd-intranet-web
```

Možný hostitel:

```text
fxdIntranet_NET
```

## Vrstva 3: Comex

```text
existující datové a aplikační komponenty
→ tvorba stránek
→ rozložení
→ vazby
→ interakce
→ finální uživatelské rozhraní
```

Autoritativní repozitář:

```text
fxd-comex-authoring
```

---

# Převod současných oblastí

| Současná oblast | Cílový repozitář |
| --- | --- |
| `fxdReplicator_NET` | zůstává `fxdReplicator_NET` |
| `fxdIntranet_NET` | zůstává `fxdIntranet_NET` |
| produkční intranetové JS, XSL, CSS a stránky | `fxd-intranet-web` |
| `xds-design` | `fxd-xds-authoring` |
| `replication` | `fxd-xds-authoring` |
| `xds-doc-add` | specializovaná schopnost v `fxd-xds-authoring` |
| `intra-design` | `fxd-intranet-authoring` |
| budoucí skilly a agenti Comexu | `fxd-comex-authoring` |
| `fdt-templates` | zůstává `fdt-templates` |
| `documentation` | zůstává `documentation` |
| tato dokumentace a pomocné podklady ke správě repozitářů | `!repository-helper` |
| obecná samostatná složka `docs` | po migraci zrušit jako samostatnou tematickou oblast |

---

# Pravidla proti duplicitám

## Implementace versus používání

- produktový repozitář popisuje, jak je funkce implementována;
- authoring repozitář popisuje, jak ji agent nebo uživatel používá při tvorbě aplikace.

## Server versus klient

- MCP server a runtime provider patří k produktu;
- MCP klient, agentní workflow a skilly patří k authoringu.

## Programátorské skilly versus aplikační skilly

- programátorské skilly mění zdrojový kód produktu;
- aplikační skilly používají produkt k vytvoření nebo konfiguraci konkrétní aplikace.

## Hostitel versus znalost

- desktopový hostitel zobrazuje a propojuje;
- authoring repozitář vlastní znalost a rozhodování agenta.

## Kanonická dokumentace versus projektová dokumentace

- obecná platformní dokumentace patří do `documentation`;
- architektura a kontrakty konkrétního produktu patří k produktu;
- pracovní znalost pro agentní tvorbu patří do příslušného authoring repozitáře.

---

# Finální seznam autoritativních repozitářů

```text
fxdReplicator_NET
fxdIntranet_NET
fxd-intranet-web
fxd-xds-authoring
fxd-intranet-authoring
fxd-comex-authoring
fdt-templates
documentation
!repository-helper
```

Tato struktura respektuje současné zavedené pojmy Flexideo, odděluje produktový runtime od agentních schopností a současně podporuje dlouhodobý vývoj tří odlišných vrstev tvorby aplikace.
