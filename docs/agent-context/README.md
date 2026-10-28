# Agent context

Rychlý podklad pro týmové předání: [Praktické zásady práce ve VS Code a repozitářích](prakticke-zasady-prace-ve-vscode-a-repozitarich.md).

Tato složka obsahuje autoritativní znalosti potřebné pro pochopení a údržbu Repository Skills.

Popisuje současný stav. Chronologická historie práce patří do `.logs/YYYY/MM/YYYY-MM-DD.md`; fyzickou historii změn uchovává Git.

Neobsahuje definice konkrétních agentů ani podrobné provozní postupy. Ty patří do:

- `.agents/profiles/` – kdo práci vykonává,
- `.agents/skills/` – jak se vykonává opakovatelná práce,
- `toolkit/` – jediný kořen všech exaktních nástrojů včetně agentní infrastruktury, doménových a vývojových nástrojů.

## Obsah

- `repository-architecture.md` – cílový model repozitáře.
- `repository-types.md` – autoritativní taxonomie development, authoring, client-project a documentation repozitářů.
- `authoring-repository-capability.md` – produktová hranice a role specializovaného a orchestračního authoringu.
- `authoring-registry-current-state-contract.md` – společná stabilní cloudová topologie, digestová semantika a publish/resolve pravidla authoring registrů.
- `migration-policy.md` – zásady bezpečné reorganizace.
- `platform-connector-scenarios.md` – předdefinované tenké konektory.
- `profile-schema.md` – kanonický formát `.agent.md` profilů.
- `repository-readme-guidelines.md` – minimální orientační dokumentace pro člověka.
- `domain-capability.md` – přenositelný skill a postup pro živé inventáře aktuálního stavu kódu.
- `documentation-sync-capability.md` – pořadí revize doménové a obecné Docusaurus dokumentace a metadata revizí.
- `development-testing-capability.md` – volitelný, frameworkově neutrální základ vývojových testů a diagnostiky.
- `client-project-capability.md` – struktura a udržování klientského implementačního projektu.
- `client-project-memory-compatibility.md` – návrh a realizované rozpoznání Project Memory, vlastnictví oblastí a hranice vůči MCP/šabloně.
- `project-documentation-capability.md` – hranice aktuální projektové dokumentace vůči epikům a propojení XDS/FDT/DAD, intranetu a COMEXu.
- `testing.md` – lokální regrese ochrany Project Memory a kompatibility helper-native layoutu.
- `client-offers-capability.md` – volitelná vrstva klientských HTML nabídek a jejich izolované publikace.
