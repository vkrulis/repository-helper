# ADR-0007: Typy repozitářů a autoritativní authoring produkt

- Stav: accepted
- Datum: 2026-08-18
- Scope: shared
- Vlastník: Repository-helper maintainers
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Repository-helper uměl obecnou vývojovou strukturu a klientský projekt, ale neměl
autoritativní model authoring repozitáře. Nebylo proto jednoznačné, zda cílové skills
vznikají v interní `.agents/skills/`, až v build výstupu, nebo přímo v publikovatelném
stromu. Chyběla také trvalá hranice mezi specializovaným authoringem jedné vrstvy,
nadřazeným orchestrátorem, runtime vývojem, klientskou implementací a dokumentací.

## Zvažované možnosti

### Možnost A — jeden obecný model repozitáře

Zachovat pouze obecné složky a význam authoringu řešit lokálními konvencemi. Je to
jednodušší pro helper, ale vede k různým zdrojům pravdy a neumožňuje jednotnou migraci,
validaci ani publikaci authoring produktů.

### Možnost B — build kopíruje authoring skills z `.agents/skills/` do `product/`

Odděluje pracovní a distribuční strom, ale vytváří dvě podoby stejného obsahu a zvyšuje
riziko driftu. Kořenová `.agents/skills/` by navíc míchala produktové a údržbové skills.

### Možnost C — typová taxonomie a přímý autoritativní `product/`

Rozlišit čtyři primární typy a pro authoring vytvářet produkt přímo v `product/`.
Kořen ponechat pro interní kontext, údržbu, build a historii; synchronizaci a publikaci
stavět až nad ověřeným produktem.

## Rozhodnutí

Přijímá se možnost C.

Repository-helper autoritativně rozlišuje primární typy `development`, `authoring`,
`client-project` a `documentation`. Každý repozitář má právě jeden primární typ podle
svého autoritativního výstupu.

Authoring repository má roli `specialist` nebo `orchestrator`. Jeho publikovatelný
produkt vzniká přímo v `product/{skills,tools,contracts,tests}`. Produktové skills se
neduplikují v kořenovém `.agents/skills/`, který slouží pouze údržbě workspace.

`Flexideo-orchestrator` je nadřazená authoring entita: koordinuje finální tvorbu a úpravy
aplikací napříč vrstvami a načítá registry specializovaných authoring produktů. Jejich
skills ani doménovou implementaci nekopíruje do svého produktu.

Documentation repository je samostatný primární typ, byť je authoringu blízký. Sbírá a
konsoliduje dohledatelně ověřenou technickou/doménovou i uživatelskou dokumentaci, ale
nenahrazuje zdroje pravdy runtime, authoringu nebo klientského projektu.

## Důsledky

- Repository-helper distribuuje capability `authoring-repository` a skill
  `maintain-authoring-repository` včetně produktové kostry a validace.
- Authoring capability závisí na `product-repository` a `development-testing`.
- XDS authoring a další specializované authoring repozitáře se budou primárně slaďovat
  instalací a aktualizací capability z Repository-helperu.
- Build produktu validuje a balí `product/`; Product Repository Sync pouze synchronizuje
  jeho hranici a registr spotřebovává až ověřené vydání.
- Změna primárního typu repozitáře je architektonické rozhodnutí a vyžaduje ADR.
