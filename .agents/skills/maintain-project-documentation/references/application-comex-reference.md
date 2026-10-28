# Aplikační a COMEX technická reference — detailní kontrakt obsahu

Tento dokument rozpracovává obsahové požadavky převzaté z
`client-application-documentation-proposal.md`. Jde o referenci pro návrh, audit,
pilot a budoucí generátor. Neznamená, že popsané rodiny `docs/reference/application`
a `docs/reference/comex` už mají implementovaného producenta.

## 1. Cílový technický pohled

Technická dokumentace má spojovat:

~~~text
FDT reference
    ↓
aplikační funkce
    ↓
UI nástroje a akce
    ↓
procesy
    ↓
projekce intranet → COMEX
    ↓
COMEX komponenty / stránky
~~~

Business vysvětlení je samostatná kurátorovaná vrstva v `docs/aplikace/`.

## 2. Navržené rodiny generované reference

~~~text
docs/reference/
├── application/
│   ├── index.md
│   ├── tree.md
│   ├── folders/<key>.md
│   ├── views/<key>.md
│   ├── tools/<key>.md
│   ├── actions/<key>.md
│   ├── processes/<key>.md
│   └── projections/<key>.md
├── comex/
│   ├── index.md
│   ├── pages/<key>.md
│   ├── components/<key>.md
│   ├── modifiers/<key>.md
│   └── templates/<key>.md
├── usage/
│   ├── index.md
│   ├── settings/<source-key>.md
│   └── actions/<action-key>.md
└── indexes/
    ├── usage/
    ├── application/
    └── comex/
~~~

Tyto cesty jsou návrhový obsah. Před přijetím společného packageru/manifestu je
kanonicky nevytvářejte; pracovní výstupy patří do stagingu.

## 3. Stabilní klíče

Soubor technické karty se pojmenovává bezpečným stabilním klíčem identity.

Nepoužívat jako jediný klíč:

- label;
- aktuální cestu ve stromu;
- samotné `tb-id`;
- samotné `auto_id`;
- samotný PDK bez scope;
- route nebo nice URL bez ověření zdroje.

Přesun nebo přejmenování má zachovat identitu a změnit jen popisné vlastnosti/cestu.

## 4. Společná hlavička každé technické karty

Každá karta má obsahovat:

- identitu;
- popisek;
- potvrzený účel nebo explicitní „neuveden“;
- application/instance/role/language scope;
- revize zdrojů;
- čas sběru;
- stav aktuálnosti;
- stav ověření;
- coverage;
- odkazy na zdroje;
- známé mezery.

Ruční business text musí mít vlastní revizi a regenerace technického indexu jej nesmí
přepsat.

## 5. Karta složky / x-item

Dokumentujte:

- document scope;
- oblast;
- druh;
- PDK;
- auto_id;
- rodiče a celou cestu;
- pořadí a děti;
- linky a záložky;
- procesní členství;
- raw access metadata;
- `on_comex`;
- integrace;
- `custom_page`;
- jazyky;
- funkci složky;
- `folder_properties/action` tlačítka, která nejsou child x-item.

Samotná hlavička nestačí k tvrzení o UI ani efektivní viditelnosti.

## 6. Karta přehledu / tabulky

Dokumentujte:

- zdrojový setting `(type,tb-id,user,language)`;
- všechny navigační konzumenty;
- případný linked zdroj;
- hlavní a pomocné selecty;
- podkladové FDT;
- view/pseudo typy;
- filtry a proměnné;
- řazení, grouping a součty;
- celý MTP kontext;
- předávání rodičovského/řádkového kontextu a klíčů;
- lokální transformace;
- editaci, založení a náhled;
- UI nástroje;
- procesní vazbu;
- projekci do COMEXu.

Podkladový typ nemusí být typem výsledného řádku.

## 7. Karta sloupce přehledu

Sloupec může být sekcí přehledu s kotvou; není nutný samostatný soubor.

Dokumentujte:

- identitu v settingu/selectu/MTP;
- alias a label;
- zdrojovou cestu nebo výraz;
- odkazy na FDT segmenty;
- výpočet/fázi;
- filtr/řazení;
- skryté technické použití;
- formátování;
- šablonu a parametry.

Alias není automaticky XDS ID. Vypočtený sloupec může používat více segmentů.

## 8. Karta UI nástroje

Dokumentujte:

- owning setting;
- přesnou pozici/ID;
- kontext řádek/náhled/tabulka/složka;
- typ operace;
- label;
- viditelnost a podmínky;
- defaultní chování;
- PDK/parametry;
- akci nebo cílový přehled/složku/FDT;
- potvrzení;
- výsledek/chybovou větev;
- návrat/refresh.

Rozlišujte:

1. explicitní COMEX tool;
2. legacy tlačítko;
3. implicitní/defaultní operaci.

## 9. Karta akce

Dokumentujte odděleně:

- PDK registrace;
- technické jméno;
- účel;
- zdrojový x-item/setting;
- lokální vs. registrovanou transformaci;
- call-type a parametry;
- `requires_pdk` nebo ekvivalent;
- input typy;
- output typy;
- matching typy;
- výstupní sloupce;
- volané akce;
- run-under identitu a oprávnění;
- prostředí;
- build/release/debug;
- platnost/archiv/smazání;
- vedlejší účinky;
- spouštěče.

Registrace, autorský setting a prováděný build jsou samostatné entity.

## 10. Karta procesu

Dokumentujte:

- kontejner `kind=p`;
- členské uzly podle procesní identity, ne podle navigačního rodiče;
- výstupní vazby a druh účinku;
- dokumentový typ každé relevantní hrany;
- přiřazené akce/registrace;
- automatické uzly;
- podmínky;
- koncové stavy;
- ruční vstupy;
- nevyřešené cíle.

Konfiguraci odlišujte od historie skutečně proběhlých případů.

## 11. Karta projekce intranet → COMEX

Dokumentujte:

- zdrojový x-item/funkční celek;
- oblast a kořeny generování;
- linked zdroj;
- zahrnutí/vynechání potomků;
- MTP;
- integrace;
- jazyky;
- `custom_page`;
- revizi generátoru;
- cílové rodiny `comex.*`;
- cílové soubory;
- nasazené otisky;
- stránky/komponenty, které výstup používají;
- nesoulady mezi autorským a nasazeným stavem.

## 12. Karta stránky / rámce

Dokumentujte:

- identitu a revizi CXD;
- route/nice URL podle skutečného zdroje;
- nadřazený frame/layout;
- navigaci/menu;
- komponenty a jejich sources;
- parametry;
- connection/event vazby;
- role a podmínky;
- jazyk;
- původ: generator / PageEdit / jiné;
- funkční scénáře;
- stav vizuálního/runtime ověření.

XSD validace sama nedokazuje funkční stránku.

## 13. Karta komponenty a modifikátoru

Oddělte:

1. definici/registr komponenty;
2. konkrétní instanci komponenty na stránce.

Dokumentujte:

- plný source;
- použitý modifikátor;
- parametry/defaulty;
- datový kontrakt;
- event kontrakt;
- backend zdroj;
- event targets;
- validační evidence;
- runtime evidence.

Nevytvářejte katalog podporovaných modifikátorů z názvů. Evidujte skutečně použité hodnoty.

## 14. Karta šablony

Rozlišujte nejméně čtyři účely:

### Sloupcová

- alias → view branch → template call;
- parametry;
- zdroj hodnoty odděleně od prezentace.

### Tabulková

- renderer celé tabulky;
- vstupní struktura;
- MTP;
- součty;
- custom template reference a její původ.

### Akční

- vykonávací XSLT/build kroky;
- zvlášť button/dialog/output template;
- odlišní konzumenti a revize.

### Stránková / komponentová

- layout/prezentační kontrakt;
- vztah k registru komponent;
- nasazené CXD.

Modifikátor není synonymum šablony.

## 15. Projekce do COMEXu

Převodní inventář má zahrnout nejen `on_comex`.

Doložená pravidla:

- Creator pracuje s vybranými shared ID a povoleným rozsahem potomků;
- soukromé stromy nejsou zdrojem tohoto generování;
- MTP child se zpracovává ve skupině, ne jako samostatná navigační položka;
- záložka může převzít typ/ID/vlastnosti z cíle, ale původ záložky zůstává evidovaný;
- linked přehled přebírá obsah ze zdrojového settingu;
- integrovaný přehled může být součástí stránky složky;
- x-item a stránka nejsou nutně 1:1;
- `custom_page`, generator a PageEdit mají oddělené vlastnictví.

Minimální převodní seznam obsahuje:

- zdrojovou instanci;
- oblast;
- auto_id;
- PDK;
- celou cestu;
- skutečný zdroj settings;
- důvod zahrnutí/vynechání;
- cílovou rodinu `comex.*`;
- stránku;
- instanci komponenty;
- modifikátor;
- jazyk;
- hash/revizi zdroje a cíle;
- stav shody;
- stav ověření role.

Zahrňte i ručně vytvořené stránky a nenapojené komponenty.

## 16. Vazby na FDT

Přebírejte pouze ověřený odkaz na konkrétní FDT/segment a identitu FDT reference:

- application;
- version;
- role;
- digest/otisk.

Při více kandidátech nikdy neberte první shodu názvu bez kontextu.

### Přehled → FDT

Rozlišujte:

- zobrazení typu;
- podkladový zdroj;
- referenci/join;
- filtr;
- řazení;
- agregaci.

### Akce → FDT

Odděleně evidujte:

- input type = deklarované čtení typu;
- output type = deklarovaný zápis typu;
- matching type = nabídka/použitelnost;
- segmentové čtení/zápis z těla akce.

Output type neimplikuje zápis všech polí typu.

### UI nástroj → FDT

Může nabízet vytvoření/editaci/náhled. Nabídka neurčuje konkrétní zapsaná pole.

### Procesní výstup → FDT

Evidujte dokumentový typ i druh procesního účinku.

### Výpočet / akce → segment

Evidujte přesný source/target, podmínku a rozsah.

## 17. Typy hran

Společný graf má odlišit alespoň:

- navigation-parent;
- setting-link;
- bookmark-target;
- mtp-membership;
- process-membership;
- process-output;
- ui-open;
- ui-invoke;
- declared-action-call;
- static-action-call;
- type-read;
- type-write;
- type-matching;
- segment-usage;
- comex-projection;
- page-composition;
- template-use.

Názvy enumů nejsou tímto dokumentem závazné; závazné je významové oddělení.

## 18. Důkaz každé hrany

Každá hrana má mít:

- zdrojovou identitu;
- cílovou identitu nebo kandidáty;
- typ vztahu;
- podmínku;
- resolution status;
- artefakt;
- hash/revizi;
- přesný locator;
- čas sběru.

Zachovávejte například:

- `resolved`;
- `ambiguous`;
- `dynamic`;
- `missing`;
- `out-of-scope`;
- `text-only`.

Nedostupný nebo nepodporovaný zdroj není negativní důkaz.

## 19. Identitní pravidla

### X-item

`instance + document scope + area + PDK`; `auto_id` samostatně.

User scope vyžaduje konkrétního autora. PDK z `xishd` a `xiusr` nejsou totéž.

### Setting

`instance + setting type/area + tb-id + user + language`.

Navigační konzument může mít jiné ID než linked zdroj.

### Akce

Rozlišujte registraci, transform name, authoring setting a build.

### Proces

Rozlišujte process container, process node a automatic registration target.

### COMEX

Rozlišujte page identity, component instance a full component source.

### Data

FDT, DAD array/SQL table a intranet view jsou samostatné entity.

## 20. Pracovní postup sběru

1. Ukotvit application/version/role/instance scope.
2. Vymezit corporate/public/shared a potřebné user autory/jazyky.
3. Projít celý požadovaný strom, ne jen textové shody.
4. Načíst funkční celky včetně MTP a linked zdrojů.
5. Připojit registr akcí a buildy.
6. Sestavit procesní vztahy.
7. Doložit projekci do COMEXu a PageEdit-only prvky.
8. Rozlišit FDT reference a stav cíle.
9. Vytvořit technické karty, reverse indexy a coverage.
10. Připojit ruční business výklad a samostatně ověřit role/UI.

Skill sám žádný live collector neimplementuje; používá dostupné specialisty/readery.

## 21. Povinné obousměrné dotazy budoucího indexu

### FDT/segment →

- přehledy;
- sloupce;
- filtry/výpočty;
- action input/output/matching;
- process nodes;
- COMEX pages.

### X-item/větev →

- parents/children;
- settings source;
- MTP;
- tools;
- actions;
- FDT;
- UI projections.

### Akce →

- kdo ji nabízí/spouští;
- co volá;
- co čte/zapisuje;
- process/trigger;
- source;
- build.

### Page/component →

- backend;
- FDT;
- tools;
- modifiers;
- templates;
- downstream pages;
- reverse consumers.

## 22. Refresh a invalidace

| Změna | Obnovit / zneplatnit |
| --- | --- |
| nová FDT reference / jiná role | resolution a všechna dotčená usages |
| save settingu / změna hlavičky / přesun | setting, MTP/link consumers, projections |
| registrace/build akce | interface, calls, types, availability, process links |
| COMEX regeneration / PageEdit / template | projection, deployed CXD, components, modifiers, consumers |
| parser/resolver rules | znovu vyhodnotit uložené zdroje |

Refresh nemusí čekat na replikaci.

Smazání potvrďte až po úplném úspěšném sběru stejného scope. Výpadek nebo denied access
nesmí vytvořit falešné smazání.

## 23. Coverage

Coverage evidujte po kolekcích a parserových dialektech:

- expected;
- fetched;
- missing;
- denied;
- parse-error;
- unsupported;
- changed-during-scan;
- excluded.

„Nenalezeno“ není automaticky „nepoužívá se“.

## 24. Požadované výsledné pohledy

Nad jednou mapou má být možné vytvořit:

1. mapu aplikace;
2. katalog funkcí;
3. mapu použití FDT;
4. registr akcí a návazností;
5. katalog COMEX UI;
6. katalog projekcí a šablon;
7. zprávu o změně a mezerách.

Všechny diagramy a rejstříky mají vznikat ze stejné odvozené mapy.

## 25. Pilot a přijetí

První pilot má zahrnout alespoň:

- jeden skutečný FDT;
- jednu celou větev;
- přehled s MTP nebo linkem;
- ruční akci;
- procesní uzel;
- COMEX stránku;
- dvě role;
- použitý modifikátor;
- sloupcovou nebo tabulkovou šablonu.

Přijetí musí doložit obousměrnou trasu:

~~~text
FDT → view/column/action/process/page
page → component/backend/FDT/source evidence
~~~

Statický graf se nevydává za runtime průběh.

## 26. Vlastnictví

- **XDS authoring**: význam XDS/FDT návazností.
- **Intranet authoring**: hlavičky, settings, akce a parsery.
- **COMEX authoring**: kompozice stránek, komponent a kontroly CXD.
- **Replicator**: životní cyklus společného indexu, packager a distribuční kontrakt.
- **Orchestrátor**: koordinace kontraktů a handoff.
- **Klientský projekt**: účel, scénáře, odpovědnosti a akceptace.

Přenositelná project-documentation capability tyto znalosti nekope do sebe; pouze stanoví,
jak je klientský projekt používá.
