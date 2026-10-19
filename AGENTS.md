# Repository Skills – pracovní pravidla

## Účel repozitáře

Tento repozitář je kanonickým zdrojem přenositelných skills, profilů, dokumentace a deterministických nástrojů pro organizaci agent-ready repozitářů.

## Zdroje pravdy

- Cílová architektura: `docs/agent-context/repository-architecture.md`
- Základní typy repozitářů: `docs/agent-context/repository-types.md`
- Migrační politika: `docs/agent-context/migration-policy.md`
- Platformní scénáře: `docs/agent-context/platform-connector-scenarios.md`
- Neutrální profilový formát: `docs/agent-context/profile-schema.md`
- Konvence README: `docs/agent-context/repository-readme-guidelines.md`

## Povinný pracovní postup

1. Rozlišujte znalost, pravidlo, profil, skill a nástroj.
2. Společnou znalost zapisujte pouze do `docs/agent-context/`.
3. Společná pravidla prostředí zapisujte do `AGENTS.md`.
4. Kanonické profily upravujte pouze v `.agents/profiles/`.
5. Platformní konektory a profily vytvářejte pouze pro požadovanou platformu. Pokud platforma není určena, použijte Codex jen při práci v Codexu; jinak se zeptejte a nabídněte i možnost bez konektoru.
6. Každý skill musí zůstat úzce zaměřený na jednu práci.
7. Veškeré exaktní a spustitelné nástroje ukládejte výhradně pod kořenový `toolkit/`. Týká se to skriptů (`*.py`, `*.ps1`, `*.sh`, `*.bat` a dalších), validátorů, generátorů, CLI wrapperů, spustitelných balíčků i podpůrných souborů. Agentní infrastruktura patří do `toolkit/agent-infrastructure/`, doménové nástroje do `toolkit/domain/`, vývojové nástroje do `toolkit/development/` a nástroj jediného skillu do `toolkit/skills/<skill-name>/`. Pokud již projekt `toolkit/` používá, zachovejte jej a konflikt významů řešte vhodnými podsložkami. Žádné nástroje neukládejte do `.agents/`, kořenového `tools/` ani do `scripts/` uvnitř skillu.
8. Projektové vstupy určené k hledání, čtení nebo analýze ukládejte do `resources/`; běhový kód ponechte v jeho standardní cestě a přenositelné podklady jednoho skillu v jeho `references/`.
9. U zdrojů evidujte původ, licenci, formát a zda jsou ručně spravované, převzaté nebo generované.
10. Při architektonicky významném rozhodnutí použijte konzervativní skill `maintain-decision-records`; ADR ukládejte do `docs/agent-context/decisions/` a nevytvářejte jej pro běžné lokální změny.
11. Po každé materiální změně kódu, dokumentace, konfigurace, pravidel, struktury nebo nástrojů použijte skill `maintain-work-log` a přidejte stručný záznam do `.logs/YYYY/MM/YYYY-MM-DD.md`. Vznik nebo změnu stavu ADR vždy propojte s tímto záznamem. Existující historii nepřepisujte; pozdější předělávku zachyťte novým záznamem. Aktuální autoritativní znalost patří do `docs/agent-context/`, chronologická historie do `.logs/` a fyzická historie do Gitu.
12. Před předáním práce ověřte dnešní log a spusťte validaci celé kolekce.

## Repository capability: client-project

Nejprve rozlište helper-native layout a existující Flexideo Project Memory podle
`project.yaml` a `.project-memory/`. Project Memory zakládá MCP a verzovaná šablona;
helper poskytuje orientaci podle `docs/agent-context/client-project-memory-compatibility.md`.
Nevytvářejte v ní druhé `docs/project/`, mise ani globální analytický ADR registr.
Obecná pravidla znalostí v `docs/agent-context/` a klientské konvence níže platí pro
helper-native repozitáře; Current Truth Project Memory zůstává v jejím kontraktu.

Helper-native klientský projekt vede epiky jako mise: jedna mise má `Epic: <epic-id>` a rozcestník
`docs/project/epics/<epic-id>/README.md`. Zdroje, artefakty a nástroje specifické pro epik patří
do odpovídajících `*/epics/<epic-id>/`; společný obsah zůstává v kořenech. `definitions/` je
jediný ručně spravovaný zdroj pravdy pro XDS, XCF a definiční obsah, dokud přijaté ADR neurčí jinak.

## ADR scope

ADR mají globální čtyřmístné číslo a povinné `Scope: shared|<epic-id>`. Pracovní návrhy mohou
vznikat souběžně pod dočasným názvem; konečné číslo se přiděluje při integraci a validátor odmítne
duplicitní číslo.

Pro klientský implementační projekt udržujte zadání, analýzy, návrhy, potvrzené závěry a trasovatelnost v `docs/project/`; aktuální technickou a doménovou pravdu v `docs/agent-context/`, vstupy v `resources/` a ručně spravovaný definiční model (projektová XDS a *.xcf) v `definitions/`, povinně s podsložkami `definitions/data/`, `definitions/temps/`, `definitions/print-temps/` a `definitions/site-files/`. Pokud projektová XDS nebo *.xcf ještě nejsou k dispozici, upozorněte uživatele, že je třeba je dodat dodatečně. Použijte skill `maintain-client-project-dimension` při založení nebo materiální změně této struktury.

Capability `domain-inventories` poskytuje skill `maintain-domain-inventories` pro
repozitáře, které potřebují živé inventáře aktuálního stavu kódu. Instalujte jej
do cíle přes `repository_architecture.py install-capability`; při aktualizaci
nejprve zkontrolujte lokální změny a teprve potom použijte `--force`.

## Repository capability: documentation-sync

Při změně chování nebo technických detailů nejprve aktualizujte doménovou dokumentaci v `docs/agent-context/`, teprve potom obecnou dokumentaci v sourozeneckém Docusaurus repozitáři. Používejte skill `maintain-documentation-sync`, vazby `general_documentation`, metadata `revised_by`/`revised_at` a validator `toolkit/agent-infrastructure/validate_documentation_metadata.py`. Před předáním vždy uživatele upozorněte, zda byla provedena doménová revize, revize obecné dokumentace a publikace.

## Repository capability: development-testing

Pro vývojový repozitář, který zavádí nebo rozšiřuje automatické testování a diagnostiku, použijte `maintain-development-testing`. Capability je volitelná a frameworkově neutrální: konkrétní runner, testovací prostředí a CI dokumentujte v `docs/agent-context/testing.md`. Izolovaná vývojová automatizace patří do `toolkit/development/`; credentials, produkční data a generované testovací artefakty se necommitují. Mutující scénáře vyžadují explicitní opt-in a resetovatelná testovací data.

## Povinné kontroly

```bash
python toolkit/agent-infrastructure/validate_skill_collection.py .
python toolkit/agent-infrastructure/repository_architecture.py validate .
python toolkit/work-log/work-log.py validate .
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

`client-offers` je volitelné rozšíření `client-project`, nikoli epik a nikoli povinná součást každé klientské implementace. U nabídky oddělte převzaté podklady v `resources/offers/`, ověřené závěry a trasovatelnost v `docs/project/offers/`, explicitně publikovatelný HTML obsah v `public/offers/` a odvozené reporty v `artifacts/offers/`. Použijte `maintain-client-offers` a `toolkit/offers/offer_tools.py`; příjemce, Access policy a secrets do repozitáře nepatří.

## Repository capability: missions

V helper-native klientském projektu mise představuje epik, nikoli izolovaný úkol. Použijte název
`NN-<epic-id>.md`, metadata `Epic`, `Stav`, `Priorita`, `ADR` a společný append-only denní log.

Když práce narazí na cíl přesahující jednu materiální změnu nebo s uživatelem zatím nesladěný rozsah, aktivně navrhněte založení mise skillem `maintain-missions`. Mise ukládejte do `docs/missions/NN-<slug>.md` dle `.agents/skills/maintain-missions/references/mission-template.md`, se stavem (`draft`/`reviewed`/`in-progress`/`done`/`deferred`/`rejected`) a polem `ADR:` propojeným na výsledný záznam v `docs/agent-context/decisions/`, jakmile z mise vzejde architektonicky významné rozhodnutí.

## Repository capability: authoring-repository

Pro repozitář typu `authoring` používejte skill `maintain-authoring-repository`. Uveďte
roli `specialist` nebo `orchestrator`; publikovatelný authoring produkt vytvářejte
autoritativně přímo v `product/`, zatímco kořenové `.agents/skills/` slouží pouze údržbě
workspace. Produktové skills neduplikujte mezi `product/skills/` a `.agents/skills/`.
Flexideo-orchestrator je nadřazená authoring entita pro koordinované změny aplikace
napříč vrstvami a specializované produkty načítá z jejich registrů, nekopíruje je.
Cloudové registry používají `docs/agent-context/authoring-registry-current-state-contract.md`:
stabilní cesty, Git jako historii a SHA-256 jako kontrolu obsahu, nikoli adresu.
