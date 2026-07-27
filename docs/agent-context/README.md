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
- `migration-policy.md` – zásady bezpečné reorganizace.
- `platform-connector-scenarios.md` – předdefinované tenké konektory.
- `profile-schema.md` – kanonický formát `.agent.md` profilů.
- `repository-readme-guidelines.md` – minimální orientační dokumentace pro člověka.
