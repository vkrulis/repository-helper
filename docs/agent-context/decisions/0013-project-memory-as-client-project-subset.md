# ADR-0013: Project Memory jako analytická podmnožina klientského projektu

- Stav: accepted
- Datum: 2026-11-02
- Scope: shared
- Vlastník: správci Repository-helper
- Nahrazuje: [ADR-0009](0009-project-memory-consumer-support.md) — částečně: ruší výklad Project Memory jako alternativního celého layoutu klientského repozitáře.
- Nahrazeno: —

## Kontext a problém

ADR-0009 správně oddělilo MCP-vlastněnou analytiku od helper-native analytického stromu,
ale instalátor z toho odvodil příliš úzký výsledek: do Project Memory distribuoval jen
orientační skill. Repozitář pak postrádal `definitions/` a další neanalytické znaky
klientské implementace, přestože jeho primárním typem zůstával `client-project`.

Uživatel 2026-11-02 výslovně upřesnil, že Project Memory musí být pouze podmnožinou
klientského projektu.

## Rozhodovací kritéria

- zachovat jedinou analytickou pravdu a MCP vlastnictví stavových přechodů;
- vyjádřit, že repozitář realizuje jednu konkrétní klientskou aplikaci;
- zachovat jediný sdílený definiční model mimo epiky;
- nevytvářet skutečné XDS/XCF bez ověřeného zdroje.

## Zvažované možnosti

### Project Memory jako alternativní celý layout

Chrání analytiku, ale skrývá klientský implementační charakter a nematerializuje
definiční ani technické oblasti.

### Project Memory jako celý repozitář bez helper capability

Ponechává vše šabloně MCP, ale Repository-helper nemůže konzistentně validovat klientský
implementační obal.

### Project Memory jako analytická podmnožina klientského projektu

MCP nadále vlastní `project/`, `context/` a `.project-memory/`; helper spravuje pouze
neanalytický obal `definitions/`, technické `resources/` a provozní skill. Kořenové
`artifacts/` zůstává rezervované kontraktem Project Memory; cestu odvozených výstupů
určuje jejich producent.

## Rozhodnutí

Přijímá se třetí možnost. `client-project` je nadřazený typ a Project Memory je jeho
analytická podmnožina. Instalace capability do známé Memory materializuje klientský
implementační obal, doplní závazné pravidlo do `AGENTS.md` a zachová serverová metadata
i analytické oblasti beze změny. `docs/project/`, mise a globální analytický ADR registr
se do Memory nepřidávají.

`definitions/` má vždy podsložky `data/`, `temps/`, `print-temps/` a `site-files/`.
Skutečná projektová XDS a `*.xcf` zůstávají otevřeným vstupem, dokud není ověřen jejich
producent, původ a autorita.

## Důvody

Model přesně odděluje projektovou/implementační odpovědnost od analytického životního
cyklu. Umožňuje Replicatoru a Implementátorovi pracovat s jediným definičním kořenem,
aniž by helper duplikoval FAAM stav nebo měnil MCP kontrakt.

## Důsledky

Instalátor a validátor rozlišují klientský obal od analytické podmnožiny. Dosavadní
Project Memory instalace pouze se skillem je neúplná a musí znovu spustit capability
`client-project`. Provisioning, sémantické operace a validace Project Memory zůstávají
vlastnictvím Orchestrátoru/MCP.

## Navazující práce

Aktualizovat regresní testy a pilotně znovu instalovat capability do NPSG-project.
