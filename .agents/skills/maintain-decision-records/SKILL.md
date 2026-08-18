---
name: maintain-decision-records
description: Konzervativně vyhodnocuje, vytváří, přijímá, odmítá a nahrazuje architektonické rozhodovací záznamy v docs/agent-context/decisions a propojuje je s denním pracovním logem. Použijte při volbě mezi dlouhodobými variantami ovlivňujícími strukturu, rozhraní, závislosti, zdroje pravdy, významné kvalitativní vlastnosti nebo obtížně vratné projektové konvence a při revizi či nahrazení existujícího ADR. Nepoužívejte automaticky pro každou materiální změnu, lokální opravu nebo mechanický refaktoring.
---

# Maintain decision records

## Rozhodovací brána

ADR navrhněte pouze tehdy, když existují alespoň dvě rozumné možnosti a rozhodnutí je současně dlouhodobé, průřezové, obtížně vratné nebo významně omezuje budoucí práci.

Posuďte čtyři otázky:

1. Existovaly skutečné alternativy?
2. Bude důvod rozhodnutí důležitý i za několik měsíců?
3. Ovlivňuje více částí projektu, veřejné rozhraní, zdroj pravdy nebo významnou kvalitativní vlastnost?
4. Mohl by někdo bez znalosti kontextu rozhodnutí později změnit opačným směrem?

- 0–1 kladná odpověď: ADR nevytvářejte; použijte pracovní log.
- 2 kladné odpovědi: ADR stručně navrhněte a vyžádejte přijetí, pokud rozhodnutí ještě nebylo schváleno.
- 3–4 kladné odpovědi: ADR zpravidla vytvořte; stav odvoďte pouze z doloženého rozhodnutí.

Velikost změny sama o sobě není důvodem pro ADR.

## Postup

### Scope a souběžné návrhy

Použijte globální čtyřmístné číslo ADR a povinné `Scope: shared|<epic-id>`. `shared` patří
celému projektu; epic-id musí odpovídat existující misi/epiku klientského projektu. Pokud mohou
autoři pracovat souběžně, ponechte návrhu pracovní název a konečné číslo přidělte při integraci.
Před přijetím ověřte jedinečnost čísla; přijaté ADR nepřečíslovávejte.

1. Přečtěte `docs/agent-context/decisions/README.md`, relevantní kontext a existující související ADR.
2. Určete další nepoužité monotónní číslo; čísla nikdy znovu nepoužívejte.
3. Použijte `references/decision-record-template.md` a vytvořte jeden záznam pro jedno rozhodnutí.
4. Oddělte fakta a omezení od rozhodnutí. Uveďte skutečně zvažované možnosti, důvody a pozitivní, negativní i neutrální důsledky.
5. Použijte stav `proposed`, pokud rozhodnutí nebylo doloženě přijato. Stav `accepted` nenastavujte pouze podle vlastní preference.
6. Přijatý nebo odmítnutý ADR významově nepřepisujte. Při změně vytvořte nový ADR, nastavte obousměrné odkazy `Nahrazuje` a `Nahrazeno` a starý označte `superseded`.
7. Po vzniku nebo změně stavu použijte `maintain-work-log` a přidejte přímý odkaz pomocí `--decision docs/agent-context/decisions/<soubor>.md`.
8. Spusťte validační příkazy repozitáře, minimálně validaci architektury a pracovního logu.

## Hranice obsahu

- ADR není implementační návod, přepis diskuse, issue ani changelog.
- Nezapisujte skryté uvažování, secrets, osobní nebo produkční data.
- Nevytvářejte nový lokální parametr, pravidlo nebo povinnost jen kvůli vyplnění šablony.
- Pokud rozhodnutí patří pouze jednomu modulu a je zřejmé z kódu, preferujte lokální dokumentaci a pracovní log.

## Výstup

Uveďte rozhodovací bránu, cestu a stav ADR, vazby na nahrazené záznamy, odkaz na denní log a výsledky validací.
