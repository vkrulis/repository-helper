# Doménová znalost

Tato složka obsahuje trvalé mapy aktuálního stavu projektu, nikoli chronologii
práce nebo důvody architektonických rozhodnutí.

## Pravidla

- Fakta, která lze deterministicky spočítat, generujte nástrojem pod
  `toolkit/domain/`.
- Generovaný výstup ukládejte jako `*.generated.md` a neupravujte jej ručně.
- Kontext, význam sloupců, baseline a falešné poplachy popište v ručně psaném
  dokumentu vedle výstupu.
- Nový dokument odkažte z `docs/agent-context/README.md`.
- Inventář aktualizujte spolu se změnou sledovaného zdrojového souboru.

Podrobný pracovní postup je v kanonickém skillu
`maintain-domain-inventories`.
