# Development-testing capability

Tato volitelná capability dává vývojovému repozitáři společný, ale frameworkově neutrální základ pro automatické testy a diagnostiku. Není součástí klientského projektu a nepředepisuje konkrétní test runner, CI ani technologii aplikace.

## Zdroje pravdy a hranice

- Produkční kód a jeho stávající testy zůstávají v jejich runtime konvenci; nepřesouvejte je jen kvůli této capability.
- Dokumentovaný testovací záměr, rizika a lokální pravidla patří do `docs/agent-context/testing.md`.
- Vývojová automatizace, izolované balíčky a jejich konfigurace patří do `toolkit/development/`.
- Credentials, produkční data, video, trace, screenshoty a reporty nejsou zdrojový kód. Ukládejte je lokálně nebo do řízeného úložiště artefaktů a ignorujte je Gitem.

## Doporučený model

Zvolte nejmenší vrstvu, která ověří konkrétní riziko. Nezakládejte end-to-end test jako náhradu za rychlejší test jednotky nebo integračního rozhraní.

| Vrstva | Účel | Typický důkaz |
|---|---|---|
| unit | čistá pravidla a transformace | rychlý test bez externího systému |
| integration | kontrakt modulu, API nebo persistence | řízená fixture či testovací služba |
| workflow | chování uživatele nebo celého procesu | reprodukovatelný scénář |
| regression | dříve nalezená chyba | nejmenší scénář, který chybu odliší |
| probe | krátkodobé zjištění příčiny | diagnostický artefakt; po zjištění odstranit nebo povýšit |

Pro samostatný testovací balíček používejte `toolkit/development/<test-suite>/`. Uvnitř zachovejte čitelné oddělení `tests/`, `fixtures/`, `support/`, `test-data/` a ignorovaných `test-results/` či `playwright-report/` podle zvoleného runneru. Nevyžadujte tuto strukturu tam, kde framework poskytuje lepší nativní konvenci; vždy ji zdokumentujte v `docs/agent-context/testing.md`.

Scénáře označujte stabilním významem, například `smoke`, `workflow`, `regression`, `known-bug`, `probe` a `mutating`. Konkrétní syntaxi tagu určuje runner. `known-bug` je reprodukce dosud neopravné vady a nesmí se vydávat za zelený regresní test.

## Bezpečné provádění

1. Testujte přednostně v odděleném prostředí a s neprodukčními účty a daty.
2. Nemutující scénáře nechte jako výchozí. Scénář, který vytváří, mění nebo maže data, vyžaduje explicitní opt-in proměnnou (např. `TEST_ALLOW_MUTATION=1`), resetovatelná data a jasné označení.
3. Do repozitáře ukládejte pouze `.env.example` bez hodnot. Skutečné `.env` a exporty cookies, tokenů či hesel ignorujte Gitem.
4. Fixture musí být minimální, dohledatelná a bez osobních či produkčních dat. Popište její původ a resetovací postup.
5. Zachycujte diagnostiku úměrně riziku: chyby aplikace, selhané požadavky, konzolové chyby a při selhání trace nebo screenshot. Artefakty před sdílením zkontrolujte na citlivý obsah.
6. CI přidávejte až pro stabilní, opakovatelné a izolované scénáře. Neopakovatelný probe ani známou chybu do povinné zelené brány nezařazujte.

## Životní cyklus vady

`probe` → minimální reprodukce → `known-bug` → oprava → `regression` → případně stabilní CI scénář.

Při každém kroku zachovejte jediný jasný důkaz problému. Nekopírujte secrets, celé trace ani produkční odpovědi do pracovního logu nebo ADR.
