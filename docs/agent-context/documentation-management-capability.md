# Přenositelná správa dokumentace

- Rozhodnutí: [ADR-0015](decisions/0015-project-documentation-runtime-ownership.md).
- Stav: lokálně implementovaná capability; Projects MVP publisher existuje v Orchestratoru,
  cílový Docusaurus builder v Orchestrátoru a živé piloty nejsou dokončené.
- Integrační architektura: [Orchestrator ADR-0079](../../../Flexideo-orchestrator/docs/agent-context/decisions/0079-project-documentation-platform-ownership.md).

Repository-helper vlastní obecné skills `search-markdown-content`,
`maintain-domain-knowledge`, `review-documentation-topology` a deterministický
Markdown vyhledávač v `toolkit/skills/search-markdown-content/`. Vznikly zobecněním
postupů Flexideo-Documentation; místní pravidla `public/supp-*`, XML a ADR zůstávají
v Documentation. Původní obecný vyhledávač byl převzat bez změny jeho AND/OR kontraktu.

## Vlastnictví

| Oblast | Vlastník |
| --- | --- |
| Platformní obsah, veřejný web a specifické importy | Flexideo-Documentation |
| Obecné dokumentační postupy a jejich lokální distribuce | Repository-helper |
| Obsah aplikace a jeho historie | Projektový Git repozitář |
| Project Memory význam, provisioning, repository binding a bezpečný interní Git adapter | Vlastník Project MCP/template |
| Privátní web, Documentation HTTP API, editor, oprávnění a publisher | Komponenta Projects v produktovém Orchestratoru |
| Integrační mise a koordinace | Orchestrator |
| Discovery, resolver a federovaná metadata | FCL; zdrojové skills zůstávají jejich vlastníkům |

Projektový Docusaurus builder, theme, search a build report jsou součástí produktového
Orchestrátoru. Helper distribuuje pouze skills, reference a read-only nástroje do
projektového repozitáře; neinstaluje runtime ani nepřipravuje publikační artefakt.
Podrobnou realizační práci řídí
[mise 31 Orchestratoru](../../../Flexideo-orchestrator/docs/orchestrator/missions/31-project-documentation.md).

## Instalace a aktualizace

Z kořene helperu:

```text
python toolkit/agent-infrastructure/repository_architecture.py install-capability <target> --name documentation-management
python toolkit/agent-infrastructure/repository_architecture.py validate <target>
```

Instalátor funguje offline. Přidává pouze allowlist tří skills s UI metadaty,
vyhledávač, profil `.agents/documentation.json` a manifest
`.agents/capabilities/documentation-management.json`. Nezakládá obsah, další
analytický strom ani konektor; nemění AGENTS, identitu, epiky, granty nebo MCP revizi.

Manifest eviduje zdrojový repozitář, Git revizi a SHA-256 každého instalovaného
souboru a samostatný digest normalizovaný pouze pro LF/CRLF. Zdrojové digesty označují
skutečné distribuované bajty pracovního stromu; samotná
revize nedokládá vydaný release. Kopie jsou distribuované a spravované, ne noví autoři.
Při aktualizaci lze nahradit jen soubor shodný s dříve zaznamenaným digestem.
Lokální či nespravovaný rozdíl odmítne celou operaci před prvním zápisem,
i s `--force`. Rozdíl nejprve posuďte a slučte; slepé přepsání není aktualizace.
Shodná opakovaná instalace nemění soubory. Git konverze LF/CRLF se neposuzuje jako
autorský konflikt. Při chybě zápisu obnoví již změněné soubory; případné selhání obnovy
výslovně ohlásí a operace skončí chybou.

Profil je lokálně vlastněná konfigurace; aktualizace jej nepřepisuje:

```json
{"contract":"repository-documentation/1","roots":["docs"],"generated_roots":["docs/reference"]}
```

Jiné repozitáře mohou mít více dokumentačních kořenů. V Project Memory 0.1/0.2
zůstává rozsah přesně `docs`; konfigurace neuděluje práva k zápisu a instalace
nevytváří samotné `docs/`. Neznámá či neúplná Memory se odmítne před zápisem.
Validátor helperu kontroluje instalované bajty a profil, nikoli sémantický stav Memory.

## DEV hranice a navazující práce

Tyto příkazy nevolají GitHub ani cloudové API a nic nenasazují. Změna zůstává na
`develop`. Případný pozdější pilot může použít pouze `projects-dev.flexideo.cloud`
a vyžaduje společné vyhodnocení s vlastníkem. Produkční `projects.flexideo.cloud`
se tímto nemění. FCL resolution a cílový Docusaurus builder v Orchestrátoru zůstávají navazující prací.
Orchestrator nyní obsahuje lokálně otestované Documentation HTTP API, online editor a
omezený bezpečný MVP publisher; jejich přítomnost v produktové projekci ještě nedokládá
DEV nasazení. Přítomnost tohoto skill balíku žádnou runtime schopnost nezpřístupňuje.
Veřejný Project MCP se podle ADR-0071 o dokumentační operace nerozšiřuje.
