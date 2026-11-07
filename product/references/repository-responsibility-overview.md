# Rozdělení odpovědností Flexideo repozitářů

Stav posouzení: 2026-07-22

Tento dokument navrhuje, co má být autoritativním obsahem devíti souvisejících projektů. Vychází z jejich současných Markdown souborů, agentních skillů, hlavních adresářů a typů zdrojových souborů. Neprovádí přesuny; slouží jako rozhodovací mapa pro následné migrace.

Položkou `docs` je zde míněna samostatná složka `C:\flexideo\develop-sources\1-Replikator\docs`, nikoli vnořené dokumentační složky ostatních projektů.

## Stručný přehled

| Repozitář | Doporučená hlavní odpovědnost | Co do něj patří | Co do něj nepatří |
| --- | --- | --- | --- |
| `fxdReplicator_NET-VS22` | Vývoj GUI a Headless Replicatoru | VB.NET zdroje, řešení a projekty, sdílené replikační jádro, vestavěný XDS Designer, vývojové testy, technická architektura a skilly pro změny kódu | Uživatelské návody k provádění replikace, obecná tvorba XDS, zákaznické definice a tiskové šablony |
| `fdt-templates` | Tvorba tiskových šablon FDT | XSLT 1.0, anonymizované FDT/XML vstupy, tiskové HTML vzory, layoutové a transformační skilly, kurátorované XSL výstupy | Obecná tvorba XDS, runtime kód Replicatoru, produkční dokumenty a zákaznická data |
| `intra-design` | Návrh a poznání konfigurace intranetových přehledů | XML table settings, platformní JS/XSL důkazy, menu XMN, diagnostické logy, katalog schopností, scénáře a nástroje pro práci s přehledy | Vývoj desktopového Intranetu, obecná XDS syntaxe, běh replikace a obecná produktová dokumentace |
| `documentation` | Kanonické zdroje a transformační pipeline dokumentace Flexideo | Historické dokumentační XML, DTD/XSD/XSL, převod publikovaného HTML do Markdownu, čtečky, generované ukázky a dokumentační doménové skilly | Běhový kód platformy, pracovní návrhy XDS, zákaznické Confluence exporty a obecné vývojové poznámky Replicatoru |
| `replication` | Používání replikačního procesu a Headless Replicatoru | Koncept XDS → kompletace → DAD → role/pages → instalace, operátorské playbooky, CLI parametry, validační a instalační skilly, katalog ověřených chyb validátoru | Implementace VB.NET Replicatoru, obecná XDS encyklopedie, zákaznická aplikační data |
| `xds-design` | Návrh, editace a ověřování XDS | XDS reference, živé `schema.mxl`, terminologie, authoring workflow, schema reader, praktické návody, zadání a kurátorované XDS výstupy | Implementace Replicatoru, samotné provádění replikace, Confluence exportní pipeline a FDT tiskové XSLT |
| `xds-doc-add` | Zpětné doplňování dokumentace do existujících XDS | Export a indexace Confluence, extrakce XDS uzlů, obohacení `documentation`, aplikace změn, auditovatelné mezivýstupy a specializovaný skill | Obecná tvorba XDS od začátku, kanonická XDS reference, dlouhodobé ukládání necenzurovaných zákaznických exportů |
| `fxdIntranet_VS22` | Vývoj desktopového klienta/hostitele Flexideo Intranetu | WinForms shell s webovým ovládacím prvkem, přihlášení a komunikace se serverem, lokální nastavení, zoom, obnovení a životní cyklus klienta | Dokumentace konfigurace přehledů, návrh XDS, replikační workflow a obecná dokumentační pipeline |
| `docs` | Nemá zůstat samostatným tematicky neurčitým projektem | Dočasně pouze migrační rozcestník, než budou tři současné dokumenty přemístěny k vlastníkům | Nová autoritativní dokumentace; tu je třeba ukládat rovnou do konkrétního odpovědného repozitáře |

## Doporučené hranice podrobněji

### `fxdReplicator_NET-VS22`

Repozitář je autoritativní pro to, **jak je Replicator implementován**. Obsahuje WinForms projekt, Headless projekt a sdílené VB.NET třídy pro kompletaci XDS, tvorbu DAD, rolí, stránek a instalaci. Patří sem také implementace vestavěného XDS Designeru a budoucích strojových rozhraní, pokud jsou součástí produktu.

Dokumentace má být vývojářská: vrstvy tříd, GUI/Headless hranice, build, regresní rizika, veřejné kontrakty CLI a interní architektonická rozhodnutí. Operátorský návod „jak provést replikaci aplikace“ má být v `replication`; authoring pravidla XDS v `xds-design`.

### `fdt-templates`

Repozitář je autoritativní pro to, **jak z FDT/XML vytvořit tisknutelné HTML**. Má obsahovat projektové XSLT konvence, vizuální systém dokladů, bezpečné anonymizované vstupy a hotové kurátorované šablony. Vstupní kontrakt konkrétní šablony musí být dohledatelný vedle příkladů nebo v její dokumentaci.

Nemá přebírat XDS authoring ani obecné CSS/HTML pokusy nesouvisející s tiskem FDT. Flexideo runtime rozšíření mají být přidávána pouze tehdy, když je cílové prostředí skutečně vyžaduje.

### `intra-design`

Repozitář je autoritativní pro to, **jak funguje a jak se navrhuje konfigurace přehledů Intranetu**. Současný obsah jasně ukazuje na table settings, `wrktabsetts.js`, zobrazovací XSL, menu XML/XMN, diagnostické logy a případové studie.

Patří sem interpretovaná dokumentace XML settingů, katalog podporovaných akcí, scénáře a exaktní nástroje pro analýzu či převod logů. Zdrojový JavaScript a XSL zde mají roli analytického důkazu nebo pracovního podkladu, ne hlavního runtime produktu. Vývoj samotného desktopového hostitele patří do `fxdIntranet_VS22`.

### `documentation`

Repozitář je autoritativní pro **zdrojové formáty dokumentace Flexideo a jejich publikační/převodní pipeline**. Stabilní číslované cesty s XML, DTD, XSD a XSL mají zůstat zachované, protože na sebe odkazují. Patří sem nástroje pro čtení dokumentačního XML a převod publikovaného HTML do Markdownu.

Nemá se stát obecným skladištěm každého Markdown dokumentu. Projektově specifická technická dokumentace má být u projektu, kterého se týká. Confluence exporty konkrétního zákazníka patří do řízeného workflow `xds-doc-add`, nikoli do kanonických zdrojů platformní dokumentace.

Poznámka k současnému stavu: spustitelné nástroje jsou stále pod `.agents/tools/`; podle nové metodiky mají být při další migraci přesunuty pod `toolkit/` a skilly na ně mají pouze odkazovat.

### `replication`

Repozitář je autoritativní pro to, **jak replikační proces používat a bezpečně řídit**. Má spojovat koncepční tok s praktickými playbooky:

```text
XDS → syntax-check → kompletace → DAD → role/pages → instalace
```

Patří sem přesná dokumentace parametrů `ReplicatorHeadless.exe`, bezpečnostní brány instalace, návratové kódy, diagnostika a katalog opakujících se validačních chyb. Kód a interní refaktoring Headless Replicatoru zůstávají v `fxdReplicator_NET-VS22`.

Tento projekt je vhodný jako domov uživatelských skillů `flexideo-replication`, `xds-headless-validate`, `replicator-headless-build` a `xds-validator-fixes`. Současná platformně vázaná `.claude/skills` má být při migraci převedena na kanonickou `.agents/skills` s případným tenkým konektorem.

### `xds-design`

Repozitář je autoritativní pro to, **jak XDS navrhovat a co jeho syntaxe znamená**. Má držet:

- živou strojovou mapu `resources/schema.mxl`;
- lidskou XDS referenci a terminologii;
- workflow tvorby dokumentů, oblastí, prvků, šablon a services;
- schema-reader pro přesné ověření povolených uzlů a vlastností;
- praktické návody, například `only-for`;
- kurátorované XDS návrhy a jejich doprovodnou dokumentaci.

Nemá duplikovat operátorské spuštění replikačních fází ani implementaci validátoru. Ověření přes Headless Replicator může volat jako externí nástroj, ale kontrakt jeho použití má vlastnit `replication`.

### `xds-doc-add`

Repozitář je autoritativní pro specializovaný proces **obohacení existujícího XDS o atributy `documentation`**. Jde o odlišnou práci od návrhu XDS: kombinuje již existující XDS, exportovaný business kontext, automaticky odvozená fakta a kontrolovanou aplikaci změn.

Patří sem deterministické kroky:

1. export a indexace Confluence;
2. extrakce uzlů XDS;
3. návrh dokumentace;
4. dry-run a lidská kontrola;
5. aplikace pouze do chybějících `documentation` atributů.

Při migraci podle `!repository-helper` mají skripty přejít z `node-documentation/scripts/` pod `toolkit/skills/xds-node-documentation/` nebo `toolkit/domain/`, skill do `.agents/skills/` a exporty do popsaných `resources/`. API klíče nesmějí být v souborech repozitáře. Reálné zákaznické exporty je třeba považovat za potenciálně citlivé a rozhodnout, zda vůbec mají být verzované.

### `fxdIntranet_VS22`

Repozitář je autoritativní pro **desktopovou WinForms aplikaci, která hostuje Flexideo Intranet**. Z aktuálního kódu je patrná odpovědnost za webový ovládací prvek, zoom, obnovu, životní cyklus okna, ukládání draftů, přihlášení a komunikaci s aplikačním serverem.

Patří sem build, runtime konfigurace, klientské přihlašování, síťová komunikace a technická dokumentace desktopového shellu. Výklad table settings a návrh přehledů patří do `intra-design`. Projekt zatím nemá Markdown orientaci ani standardní repository vrstvu a je kandidátem na samostatnou migraci.

### `docs`

Samostatná složka `1-Replikator/docs` dnes obsahuje tři hodnotné, ale tematicky rozdílné dokumenty. Obecný název nevytváří jasné vlastnictví a hrozí vznik paralelního zdroje pravdy. Doporučené zařazení:

| Současný dokument | Cílový vlastník | Důvod |
| --- | --- | --- |
| `headless-replicator-params.md` | `replication` | veřejné parametry a operátorský postup Headless Replicatoru |
| `MCP-pro-XDS-designer_MVP.md` | `fxdReplicator_NET-VS22` | architektura budoucího MCP/headless rozhraní a zásahy do implementace Designeru |
| `upgrade-reference-manual.md` | `fxdReplicator_NET-VS22` | vývojová reference dual-mode GUI/Headless architektury |

Po přesunu má `docs` přestat fungovat jako samostatný projekt. Dočasně může obsahovat pouze stručný migrační rozcestník se stavem přesunů a odkazy na nové kanonické cesty.

## Pravidla proti duplicitám

1. **Implementace versus použití:** `fxdReplicator_NET-VS22` popisuje interní konstrukci; `replication` veřejný a operátorský postup.
2. **XDS versus replikace:** `xds-design` určuje syntaxi a návrh XDS; `replication` jeho průchod replikačními fázemi.
3. **FDT tisk versus XDS:** `fdt-templates` pracuje s výslednými FDT/XML daty a tiskovým HTML; `xds-design` definuje strukturu dokumentových typů.
4. **Intranet runtime versus konfigurace:** `fxdIntranet_VS22` vlastní desktopový klient; `intra-design` význam a ovládání přehledových settingů.
5. **Platformní dokumentace versus zákaznický kontext:** `documentation` vlastní kanonické dokumentační zdroje Flexideo; `xds-doc-add` dočasně zpracovává externí kontext pro konkrétní XDS.
6. **Projektová dokumentace zůstává u projektu:** obecná složka `docs` není dlouhodobým vlastníkem žádné z uvedených oblastí.

## Doporučené pořadí dalších rozhodnutí

1. Přesunout tři dokumenty ze samostatného `docs` k navrženým vlastníkům a ponechat migrační rozcestník.
2. Migrovat `replication` na `.agents/skills`, `docs/agent-context`, `toolkit` a `.logs`; při tom sloučit jeho headless reference s `headless-replicator-params.md`.
3. Migrovat `xds-doc-add` a rozhodnout retenční pravidla pro Confluence exporty, ZIP, indexy a mezivýstupy.
4. Zavést standardní vývojovou strukturu pro `fxdIntranet_VS22` a zdokumentovat jeho veřejnou hranici vůči `intra-design`.
5. Dokončit migraci `documentation`, zejména přesun spustitelných nástrojů z `.agents/tools` do `toolkit`.
6. U projektů bez rozpoznaného Git repozitáře rozhodnout, zda mají být samostatnými Git repozitáři, nebo součástí společného nadřazeného repozitáře; do té doby nelze spolehlivě sledovat přesuny a nezávislou historii.

## Otevřené rozhodnutí s nejvyšším dopadem

Nejdůležitější zbývající otázkou není tematické rozdělení, ale hranice verzování: kromě `fxdReplicator_NET-VS22` nebyl při auditu žádný z uvedených kořenů rozpoznán jako Git repozitář. Je třeba rozhodnout, zda projekty pod `5-VS-code` mají mít samostatné Git historie, nebo zda budou spravovány v jednom nadřazeném repozitáři. Obsahové hranice navržené výše jsou použitelné v obou variantách.
