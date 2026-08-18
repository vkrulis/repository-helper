# Architektonická rozhodnutí

Tato složka obsahuje stručné a trvalé záznamy architektonicky významných rozhodnutí (ADR). ADR vysvětluje kontext, zvažované možnosti, přijaté rozhodnutí a jeho důsledky; chronologický záznam provedené práce patří do `.logs/`.

## Kdy ADR vytvořit

ADR vytvořte střídmě: musí existovat alespoň dvě rozumné možnosti a rozhodnutí musí být dlouhodobé, průřezové, obtížně vratné nebo významně omezovat budoucí práci. Lokální opravy, mechanické refaktoringy a snadno vratné implementační detaily patří pouze do pracovního logu.

Použijte skill `maintain-decision-records`. Každý vznik nebo změnu stavu ADR propojte s odpovídajícím denním záznamem v `.logs/YYYY/MM/YYYY-MM-DD.md`.

## Konvence

- Každé ADR má povinné pole `Scope: shared|<epic-id>`.
- `shared` znamená rozhodnutí pro celý projekt; `<epic-id>` označuje rozhodnutí jednoho epiku.
- Globální číslo se přiděluje při integraci do sdílené větve. Pracovní návrh může mít dočasný název;
  duplicitní konečné číslo je validační chyba a řeší se před přijetím.

- Název souboru: `NNNN-strucny-nazev.md`; čísla jsou monotónní a znovu se nepoužívají.
- Jeden ADR popisuje jedno rozhodnutí.
- Stavy: `proposed`, `accepted`, `rejected`, `superseded`.
- Přijatý nebo odmítnutý záznam významově nepřepisujte.
- Změnu rozhodnutí zachyťte novým ADR a oba záznamy vzájemně propojte poli `Nahrazuje` a `Nahrazeno`.
