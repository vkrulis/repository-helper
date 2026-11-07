# Repository Skills – pracovní pravidla

## Účel repozitáře

Tento repozitář je kanonickým zdrojem přenositelných skills, profilů, dokumentace a deterministických nástrojů pro organizaci agent-ready repozitářů.

## Zdroje pravdy

- Publikovatelný produkt: `product/`
- Cílová architektura: `product/references/repository-architecture.md`
- Základní typy repozitářů: `product/references/repository-types.md`
- Migrační politika: `product/references/migration-policy.md`
- Platformní scénáře: `product/references/platform-connector-scenarios.md`
- Neutrální profilový formát: `product/references/profile-schema.md`
- Konvence README: `product/references/repository-readme-guidelines.md`

## Povinný pracovní postup

1. Rozlišujte znalost, pravidlo, profil, skill a nástroj.
2. Společnou znalost zapisujte pouze do `docs/agent-context/`.
3. Společná pravidla prostředí zapisujte do `AGENTS.md`.
4. Produktové profily a skills upravujte pouze v `product/profiles/` a `product/skills/`;
   kořenové `.agents/` je pouze interní kompatibilní vstup workspace.
5. Platformní konektory a profily vytvářejte pouze pro požadovanou platformu. Pokud platforma není určena, použijte Codex jen při práci v Codexu; jinak se zeptejte a nabídněte i možnost bez konektoru.
6. Každý skill musí zůstat úzce zaměřený na jednu práci.
7. Publikovatelné exaktní nástroje ukládejte výhradně do `product/tools/`; kořenový
   `toolkit/` je vyhrazen interním build/test/release nástrojům workspace. Žádné nástroje
   neukládejte do `.agents/` ani do `scripts/` uvnitř skillu.
8. Projektové vstupy určené k hledání, čtení nebo analýze ukládejte do `resources/`; běhový kód ponechte v jeho standardní cestě a přenositelné podklady jednoho skillu v jeho `references/`.
9. U zdrojů evidujte původ, licenci, formát a zda jsou ručně spravované, převzaté nebo generované.
10. Při architektonicky významném rozhodnutí použijte konzervativní skill `maintain-decision-records`; ADR ukládejte do `docs/agent-context/decisions/` a nevytvářejte jej pro běžné lokální změny.
11. Po každé materiální změně kódu, dokumentace, konfigurace, pravidel, struktury nebo nástrojů použijte skill `maintain-work-log` a přidejte stručný záznam do `.logs/YYYY/MM/YYYY-MM-DD.md`. Vznik nebo změnu stavu ADR vždy propojte s tímto záznamem. Existující historii nepřepisujte; pozdější předělávku zachyťte novým záznamem. Aktuální autoritativní znalost patří do `docs/agent-context/`, chronologická historie do `.logs/` a fyzická historie do Gitu.
12. Před předáním práce ověřte dnešní log a spusťte validaci celé kolekce.

## Povinná lokální aktualizace společného produktu

Po dokončené materiální změně `product/` a po jeho kontrolách aktivujte z kořene
Orchestrátoru celou sedmiproduktovou sestavu:

```powershell
python ../Flexideo-orchestrator/product/tools/local-implementer/assemble.py --sources-root .. --store ../../local-products/flexideo-implementer --activate
```

Sestavovač je jediný publisher stabilní instalace. Ověří Repository Foundation, FCL
a pět vrstev A–E a atomicky nahradí celý spravovaný obsah. Ruční dílčí kopírování
do instalace je zakázáno. Aktualizaci provádějte mezi relacemi a další práci nad
instalovaným produktem začněte v novém chatu načtením aktuálního `AGENTS.md`.

## Repository capability: client-project

Klientský projekt je nadřazený implementační celek. Existující Flexideo Project Memory
rozpoznaná podle `project.yaml` a `.project-memory/` je pouze jeho analytickou podmnožinou,
kterou zakládá MCP a verzovaná šablona. Helper doplňuje neanalytický klientský obal podle
`product/references/client-project-memory-compatibility.md`: jeden `definitions/` strom,
technické vstupy v `resources/` a provozní capability. Kořenové `artifacts/` v Project
Memory nematerializujte; cestu výstupů určuje kontrakt jejich producenta. Nevytvářejte
v ní druhé `docs/project/`, mise ani globální analytický ADR registr; Current Truth zůstává
v kontraktu Project Memory.

Helper-native klientský projekt vede epiky jako mise: jedna mise má `Epic: <epic-id>` a rozcestník
`docs/project/epics/<epic-id>/README.md`. Zdroje, artefakty a nástroje specifické pro epik patří
do odpovídajících `*/epics/<epic-id>/`; společný obsah zůstává v kořenech. `definitions/` je
jediný ručně spravovaný zdroj pravdy pro XDS, XCF a definiční obsah, dokud přijaté ADR neurčí jinak.

## ADR scope

ADR mají globální čtyřmístné číslo a povinné `Scope: shared|<epic-id>`. Pracovní návrhy mohou
vznikat souběžně pod dočasným názvem; konečné číslo se přiděluje při integraci a validátor odmítne
duplicitní číslo.

Pro klientský implementační projekt udržujte zadání a analytiku v autoritě zvoleného layoutu: helper-native používá `docs/project/` a `docs/agent-context/`, Project Memory používá `project/epics/` a `context/`. Oba layouty mají vstupy v `resources/` a jediný sdílený definiční model (projektová XDS a *.xcf) v `definitions/`, povinně s podsložkami `definitions/data/`, `definitions/temps/`, `definitions/print-temps/` a `definitions/site-files/`. Pokud projektová XDS nebo *.xcf ještě nejsou k dispozici, upozorněte uživatele, že je třeba je dodat dodatečně. Použijte skill `maintain-client-project-dimension` při založení nebo materiální změně této struktury.

Capability `domain-inventories` poskytuje skill `maintain-domain-inventories` pro
repozitáře, které potřebují živé inventáře aktuálního stavu kódu. Instalujte jej
do cíle přes `repository_architecture.py install-capability`; při aktualizaci
nejprve zkontrolujte lokální změny a teprve potom použijte `--force`.

## Repository capability: project-documentation

Pro aktuální dokumentaci klientské aplikace používejte skill `maintain-project-documentation`.
V Project Memory je `docs/` sdílená dokumentace současného stavu mimo epiky:
`project/epics/` drží zadání, analýzu, evidence, rozhodnutí a historii změny. Generovanou
FDT referenci pod `docs/reference/fdt/` ručně neupravujte. XDS, intranetové settings,
action registry ani COMEX jsou samostatné autority a dokumentační nález sám není povolením
je změnit. Capability lze instalovat i do rozpoznané Project Memory; installer tam přidá
jen skill, jeho referenci a read-only validační nástroj, nikoli druhý scaffold.

## Repository capability: documentation-sync

Při změně chování nebo technických detailů nejprve aktualizujte doménovou dokumentaci v `docs/agent-context/`, teprve potom obecnou dokumentaci v sourozeneckém Docusaurus repozitáři. Používejte skill `maintain-documentation-sync`, vazby `general_documentation`, metadata `revised_by`/`revised_at` a validator `product/tools/agent-infrastructure/validate_documentation_metadata.py`. Před předáním vždy uživatele upozorněte, zda byla provedena doménová revize, revize obecné dokumentace a publikace.

## Repository capability: development-testing

Pro vývojový repozitář, který zavádí nebo rozšiřuje automatické testování a diagnostiku, použijte `maintain-development-testing`. Capability je volitelná a frameworkově neutrální: konkrétní runner, testovací prostředí a CI dokumentujte v `docs/agent-context/testing.md`. Izolovaná vývojová automatizace patří do `toolkit/development/`; credentials, produkční data a generované testovací artefakty se necommitují. Mutující scénáře vyžadují explicitní opt-in a resetovatelná testovací data.

## Povinné kontroly

```bash
python product/tools/agent-infrastructure/validate_skill_collection.py product
python -m unittest discover -s product/tests -v
python product/tools/work-log/work-log.py validate .
```

## Bezpečnost a změny

- Nezapisujte credentials, tokeny, produkční data ani lokální osobní konfiguraci.
- Nepřepisujte existující soubory bez zobrazení rozdílu nebo explicitního režimu `--force`.
- Migrační nástroje nesmějí automaticky rozhodovat o nejednoznačných doménových přesunech.
- Při změně platformního scénáře uveďte datum ověření a zdroj.

## Definice hotovo

Změna je hotová pouze tehdy, když:

- odpovídá architektuře repozitáře,
- nevytváří druhý zdroj pravdy,
- všechny `SKILL.md` mají validní frontmatter,
- odkazy na soubory existují,
- všechny výslovně požadované generované konektory jsou synchronní,
- validační příkazy skončí úspěšně,
- README nebo kontextová dokumentace popisují uživatelsky významnou změnu.
- materiální změna je stručně zaznamenána v dnešním pracovním logu včetně změněných souborů, skutečně provedených validací a otevřené práce.

## Repository capability: client-offers

`client-offers` je volitelné rozšíření `client-project`, nikoli epik a nikoli povinná součást každé klientské implementace. U nabídky oddělte převzaté podklady v `resources/offers/`, ověřené závěry a trasovatelnost v `docs/project/offers/`, explicitně publikovatelný HTML obsah v `public/offers/` a odvozené reporty v `artifacts/offers/`. V tomto workspace použijte produktový skill `maintain-client-offers` a `product/tools/offers/offer_tools.py`; po instalaci capability do klientského repozitáře používá nástroj cílovou cestu `toolkit/offers/offer_tools.py`. Příjemce, Access policy a secrets do repozitáře nepatří.

## Repository capability: missions

V helper-native klientském projektu mise představuje epik, nikoli izolovaný úkol. Použijte název
`NN-<epic-id>.md`, metadata `Epic`, `Stav`, `Priorita`, `ADR` a společný append-only denní log.

Když práce narazí na cíl přesahující jednu materiální změnu nebo s uživatelem zatím nesladěný rozsah, aktivně navrhněte založení mise skillem `maintain-missions`. Mise ukládejte do `docs/missions/NN-<slug>.md` dle `product/skills/maintain-missions/references/mission-template.md`, se stavem (`draft`/`reviewed`/`in-progress`/`done`/`deferred`/`rejected`) a polem `ADR:` propojeným na výsledný záznam v `docs/agent-context/decisions/`, jakmile z mise vzejde architektonicky významné rozhodnutí.

## Repository capability: authoring-repository

Pro repozitář typu `authoring` používejte skill `maintain-authoring-repository`. Uveďte
roli `specialist` nebo `orchestrator`; publikovatelný authoring produkt vytvářejte
autoritativně přímo v `product/`, zatímco kořenové `.agents/skills/` slouží pouze údržbě
workspace. Produktové skills neduplikujte mezi `product/skills/` a `.agents/skills/`.
Flexideo-capability-library je authoring-resolution orchestrator: klasifikuje záměr,
načítá specializované produkty z jejich registrů a sestavuje minimální připnutý bundle,
ale změnu nevykonává. Flexideo-orchestrator je platformní a projektový orchestrátor a
mapu ani authoring bootstrap neduplikuje.
Cloudové registry používají `product/references/authoring-registry-current-state-contract.md`:
stabilní cesty, Git jako historii a SHA-256 jako kontrolu obsahu, nikoli adresu.

## Repository capability: flexideo-implementer

Pro lokální implementační úkol klientské aplikace použijte `activate-flexideo-implementer`.
Helper instaluje pouze zavaděč a jeho nástroj, umístění externího produktu patří
do uživatelského registru mimo repozitáře. FCL vlastní mapu a authoring resolution.
Samostatná instalace do známé Project Memory nemění projektová pravidla ani sémantický obsah;
aktivační výsledek vyžaduje explicitní načtení vrácených instrukcí a bootstrapu.

## Repository capability: documentation-management

Helper vlastní obecné skills `search-markdown-content`, `maintain-domain-knowledge` a
`review-documentation-topology`; jejich konfiguraci a spravovanou distribuci určuje
`product/references/documentation-management-capability.md`. Projektové a platformní
obsahy zůstávají jejich vlastníkům. Instalace do známé Project Memory přidává pouze
allowlist nástrojů a profil/manifest v .agents; nemění AGENTS, analytiku ani granty.
