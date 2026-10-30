# ADR-0010: Přenositelná dokumentační capability a instalace do Project Memory

- Stav: accepted
- Datum: 2026-10-29
- Scope: shared
- Vlastník: správci Repository-helper
- Nahrazuje: [ADR-0009](0009-project-memory-consumer-support.md) — částečně: rozšiřuje allowlist instalací o documentation-management.
- Nahrazeno: —

## Kontext a problém

Documentation konsoliduje platformní obsah. Mise privátní projektové dokumentace
kombinovala obecnou údržbu, projektový obsah a Projects runtime. FCL zatím není
dostupným distribučním mechanismem a nepřebírá autorství produktových skills.
ADR-0009 dovolovalo v Memory pouze orientační čtecí instalaci.

Uživatel 2026-10-29 výslovně schválil rozdělení odpovědností, přenos mise do
Orchestratoru, zobecnění postupů v helperu a rozšíření instalátoru. Rozsah je
lokální develop příprava bez produkce; piloty a migrace projektů budou společné.

## Zvažované možnosti

- Ponechat vše v Documentation: směšuje platformní obsah s klientským runtime.
- Převést vše do Orchestratoru: vytváří vlastníka obecných odborných postupů v koordinátoru.
- Oddělit obecnou capability helperu, obsah projektů a službu Projects; Orchestrator koordinuje.

## Rozhodnutí

Přijímá se třetí možnost. Helper je autoritou obecných dokumentačních skills a
nástrojů. Project Git vlastní obsah, Project MCP/template projektové významové
kontrakty a komponenta Projects oprávnění, web, editor a privátní publisher.
Documentation si ponechává platformní obsah i veřejný Docusaurus publisher.
Sdílený generický builder je budoucí volitelný nástroj helperu.

Do rozpoznané Memory 0.1/0.2 lze explicitně instalovat documentation-management.
Allowlist se omezuje na distribuované skills/nástroj a jejich profil a manifest
v .agents; nemění obsah, AGENTS ani serverová metadata. Unknown layout se odmítá.
Aktualizace ověřuje předchozí digesty a odmítá místní změny i s force.
Profil je cílově vlastněný a v Memory neumožňuje rozšířit kořen mimo docs.

## Důsledky

Obecné postupy mají jednoho autora a budoucí FCL může jejich distribuci nahradit
bez změny autority. Přibývá spravovaná lokální kopie a povinnost řešit konflikty.
Instalace nedokládá funkční dokumentační API, builder, oprávnění ani publikaci.
Provisioning a sémantická validace z ADR-0009 zůstávají beze změny.

## Navazující práce

Offline regrese instalace a kompatibility; následně společné projektové piloty.
Cloudová acceptance pouze na projects-dev.flexideo.cloud. Produkční nasazení
ani hromadná migrace nejsou tímto schváleným řezem.
