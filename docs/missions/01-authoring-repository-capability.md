# Mise: Jednotný authoring repository model

- Epic: authoring-repository
- Stav: in-progress
- Priorita: vysoká
- ADR: [ADR-0007](../agent-context/decisions/0007-typy-repozitaru-a-authoring-produkt.md)

## Cíl

Udržovat v Repository-helperu autoritativní, instalovatelný a testovatelný model
specializovaných i orchestračních authoring repozitářů a postupně jím sjednotit
authoring repozitáře ekosystému Flexideo.

## Proč

Jednotný zdroj pravdy v `product/` umožní oddělit interní workspace od produktu,
spolehlivě testovat vydání a skládat schopnosti orchestrátoru z registrů jednotlivých
vrstev bez kopírování nebo driftu.

## Co už víme

- Základní typy a authoring role jsou přijaty v ADR-0007.
- Flexideo-orchestrator je nadřazená authoring entita.
- XDS authoring bude první specializovaný repozitář sjednocený stejným postupem.
- Product Repository Sync přenáší ověřený strom, ale není jeho buildem ani zdrojem.

## Navrhovaný přístup

1. Udržovat capability, skill, šablony a validaci v Repository-helperu.
2. Pilotně ji ověřit v Orchestrátoru.
3. Přes Helper postupně migrovat XDS a ostatní authoring repozitáře.
4. Standardizovat registry, resolver a release evidence pro skládání orchestrátoru.

## Závislosti

- `product-repository`
- `development-testing`
- registry a kontrakty jednotlivých authoring vrstev

## Otevřené otázky

- Přesné strojově čitelné schéma registru capability a kompatibility.
- Release/versioning politika napříč specializovanými produkty a orchestrátorem.
- Hranice a publikační model dokumentačního repozitáře.

## Definice hotovo (návrh)

- Orchestrátor a všechny aktivní authoring repozitáře používají instalovanou capability.
- Registry a kontrakty jsou validované a verzované.
- Orchestrátor umí bezpečně objevit a aktualizovat dostupné specializované schopnosti.
- Dokumentační větev modelu má potvrzený publikační a synchronizační kontrakt.
