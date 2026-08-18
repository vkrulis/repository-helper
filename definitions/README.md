# Definice projektu

Kořenová složka ručně spravovaného definičního modelu konkrétní klientské implementace.
Přímo v této složce leží projektová zdrojová XDS (např. `<projekt>.xds`) a *.xcf soubory
s aplikačním nastavením projektu (např. `<projekt>.xcf`, `<projekt>_PROD.xcf`).

Tyto soubory nejsou generovány helperem — dodává je autor projektu nebo se přebírají z
existující implementace. Pokud při založení klientského rozměru ještě nejsou k dispozici,
založte přesto tuto složku i všechny povinné podsložky níže a výslovně upozorněte uživatele,
že projektovou XDS a *.xcf je třeba dodat dodatečně.

Povinné podsložky:

- `data/` – aplikační a doménová data napojená na definiční model (např. číselníky, role,
  historie, registry).
- `temps/` – pracovní a customizační šablony mimo tiskový výstup (např. XSL/XML úpravy
  chování a stylů).
- `print-temps/` – tiskové šablony (typicky XSL) používané při generování dokumentů.
- `site-files/` – webové a rolové soubory nasazované s aplikací.

Kompletované XDS, DAD a validační či replikační reporty jsou odvozené artefakty a patří do
`artifacts/` podle projektové strategie verzování, ne sem.
