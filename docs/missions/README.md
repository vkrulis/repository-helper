# Mise

Tato složka obsahuje **návrhy** střednědobých a dlouhodobých cílů tohoto repozitáře — ne hotová rozhodnutí a ne pracovní historii. Mise popisuje cíl, proč na něm záleží, co už víme, a navrhovaný přístup k dosažení. Je to podklad k projití s uživatelem, ne autoritativní zdroj.

## Vztah k ostatním zdrojům pravdy

- Doménové znalosti ověřené a přijaté z mise patří do `docs/agent-context/domain/` (skill `maintain-domain-inventories`, je-li nainstalován).
- Architektonicky významné rozhodnutí vzešlé z mise se zapisuje jako ADR do `docs/agent-context/decisions/` (skill `maintain-decision-records`); mise na něj zpětně odkazuje polem `ADR:`.
- Provedená práce na misi se loguje standardně do `.logs/` (skill `maintain-work-log`).

Pracovní postup: **mise (`draft`) → review s uživatelem (`reviewed`) → ADR, je-li rozhodnutí architektonicky významné → systematická realizace (`in-progress` → `done`)**, případně `deferred`/`rejected`, pokud se dál nepokračuje.

## Kdy misi založit

Použijte skill `maintain-missions`. Misi navrhněte, jakmile cíl přesahuje jednu materiální změnu, má s uživatelem zatím nesladěný rozsah nebo přístup, pravděpodobně povede k architektonicky významnému rozhodnutí, nebo jde o dlouhodobý/strategický cíl repozitáře — ne o izolovanou opravu.

## Formát

Použijte `.agents/skills/maintain-missions/references/mission-template.md`. Název souboru: `NN-strucny-nazev.md` (dvoumístné, monotónní číslo v rámci této složky, čísla se znovu nepoužívají). Sdílený kontext využívaný více misemi (např. doménový model) může mít vlastní číslo ve stejné číselné řadě, i když sám nemá formát jednotlivé mise.

## Mise

| # | Mise | Stav | Priorita |
| --- | --- | --- | --- |
| 01 | [Jednotný authoring repository model](01-authoring-repository-capability.md) | in-progress | vysoká |

## Poznámka k údržbě

Tento index udržujte ručně v souladu se stavem jednotlivých misí.
