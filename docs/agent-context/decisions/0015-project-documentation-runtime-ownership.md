# ADR-0015: Projektový dokumentační runtime vlastní Orchestrátor

- Stav: accepted
- Datum: 2026-11-02
- Scope: shared
- Vlastník: správci Repository-helper
- Nahrazuje: [ADR-0012](0012-documentation-management-and-project-memory-installation.md)
- Nahrazeno: —
- Souvisí: [ADR-0010](0010-project-documentation-capability.md), [Orchestrator ADR-0079](../../../../Flexideo-orchestrator/docs/agent-context/decisions/0079-project-documentation-platform-ownership.md)

## Kontext a problém

ADR-0012 správně oddělilo přenositelné dokumentační postupy od klientského obsahu, ale budoucí společný Docusaurus builder přiřadilo Helperu. Projektový build, theme, search, editor, publikace a řízení přístupu tvoří jeden platformní produkt s provozním životním cyklem v Orchestrátoru. Helper nemá vlastní runtime produkt.

## Zvažované možnosti

- Ponechat provider-neutrální builder v Helperu: vznikne runtime závislost a produktová odpovědnost v distribuční infrastruktuře.
- Umístit celý Project Documentation Platform v Orchestrátoru a Helper ponechat jako dodavatele volitelných projektových dovedností a read-only kontrol.

## Rozhodnutí

Přijímá se druhá možnost. Orchestrátor vlastní Docusaurus builder, design, build kontrakt, search index, Documentation HTTP API, editor, privátní publisher a doručování. Helper vlastní pouze obecné repository skills, jejich instalaci, reference a deterministické read-only validační/inventory nástroje. Capability `project-documentation` nemění Project Memory, granty, MCP ani obsah projektu; její instalace neznamená dostupnost dokumentační služby.

Specializované authoring produkty A–E vytvářejí odborné příspěvky až v cílovém projektovém kontextu. FCL je pouze vybírá a předává. Autoritativní projektový Markdown a navigační metadata zůstávají v projektovém Git repozitáři.

## Důsledky

Helper nedostane Docusaurus závislosti, publikační pipeline, R2 adaptér ani `product/` pro dokumentaci. Existující přenositelné skills a bezpečná instalace do známé Project Memory zůstávají použitelné. Návrhy builderu v kontextové dokumentaci se přesměrují do Orchestrátoru.

## Navazující práce

Dokončit misi 31 Orchestrátoru, ověřit izolaci dvou projektů a zachovat veřejný Project MCP kontrakt.
