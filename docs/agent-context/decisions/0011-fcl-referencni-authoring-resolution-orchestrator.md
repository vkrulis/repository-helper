# ADR-0011: FCL je referenční authoring-resolution orchestrator

- Stav: accepted
- Datum: 2026-11-01
- Scope: shared
- Vlastník: správci Repository-helper
- Nahrazuje: [ADR-0007](0007-typy-repozitaru-a-authoring-produkt.md) — částečně v identitě a odpovědnosti referenčního orchestrátoru
- Nahrazeno: —

## Kontext a problém

ADR-0007 správně zavedlo primární typ `authoring`, produktovou hranici `product/` a role specialist/orchestrator. Jako referenčního authoring orchestrátora však určilo `Flexideo-orchestrator`, který mezitím vlastní rostoucí platformní a projektové služby: stránky, backend, účty, MCP a Project Memory. Capability mapa, bootstrap a resolution proto dostaly samostatný repozitář `Flexideo-capability-library`.

## Rozhodovací kritéria

- zachovat obecný authoring repository model;
- oddělit klasifikaci a resolution od platformní/runtime koordinace;
- určit jediný referenční produkt pro mapu a federované registry;
- nevydávat resolution za fyzické vykonání změny.

## Zvažované možnosti

- Ponechat jako referenci Flexideo Orchestrator a FCL chápat jen jako jeho knihovnu.
- Určit FCL jako referenční authoring-resolution orchestrator a Orchestrátor vést jako oddělený platformní a projektový produkt.

## Rozhodnutí

Přijímá se druhá možnost. Role `authoring/orchestrator` znamená klasifikaci záměru, federované discovery a sestavení minimálního připnutého capability bundle. Referenční implementací je `Flexideo-capability-library`. Resolution končí před vykonáním změny. `Flexideo-orchestrator` je platformní a projektový orchestrátor a authoringovou mapu, bootstrap ani skills nekopíruje.

## Důsledky

- Scaffoldovaná pravidla authoring capability odkazují na FCL.
- Obecná produktová hranice specialistů i orchestrátoru z ADR-0007 zůstává platná.
- FCL a specializované produkty používají federované registry a digestově připnuté locky.
- Vykonání změny, projektová pravda a runtime služby zůstávají mimo FCL.

## Navazující práce

- validovat aktualizovaný scaffold a skill kolekci;
- při dalších instalacích capability nevracet starou identitu Orchestrátoru;
- publikační kanál FCL řešit samostatným rozhodnutím.
