# Praktické zásady práce ve VS Code a repozitářích

Krátké předání zkušeností z dosavadní práce:

- **Nejdřív se zorientovat, potom měnit.** Ve VS Code otevřít správný workspace, ověřit kořen repozitáře a přečíst `README.md`, `AGENTS.md` a relevantní projektový kontext.
- **Každá věc má jednoho vlastníka.** Kód, dokumentaci, skills, nástroje i kontrakty ukládat do repozitáře, který za ně skutečně odpovídá. Nesouvisející znalost nekopírovat „pro pohodlí“.
- **Držet jeden zdroj pravdy.** Aktuální znalost patří do `docs/agent-context/`, pravidla do `AGENTS.md`, opakovatelný postup do `.agents/skills/`, spustitelné nástroje do `toolkit/` a historie práce do `.logs/` a Gitu.
- **Oddělit návrh od provedení.** Nejdřív zkontrolovat vstupy, rozsah a diff; teprve potom spouštět mutující, instalační nebo produkční kroky. Rizikové operace musí mít jasný cíl a potvrzení.
- **Respektovat rozpracovanou práci.** Před úpravou zkontrolovat `git status` a diff. Cizí nebo nesouvisející změny nevracet, nepřepisovat ani nepřibalovat do vlastní změny.
- **Používat přenositelné příkazy.** Spouštět je z popsaného pracovního adresáře, uvnitř repozitáře používat relativní cesty a nevázat postup na konkrétní počítač, pokud to nevyžaduje runtime.
- **Textová instrukce není zabezpečení.** Oprávnění musí vynucovat sandbox, operační systém, CI nebo server. Tokeny, osobní konfigurace a produkční data nepatří do repozitáře ani do chatu.
- **Automatizovat jen exaktní část.** Rozhodnutí a význam řeší člověk nebo agent; opakovatelné kontroly a převody nástroj. Platformní konektor má být tenký a nemá duplikovat znalost projektu.
- **Hotovo znamená ověřeno.** Spustit relevantní testy a validační příkazy, zkontrolovat diff a `git diff --check`, zapsat materiální změnu do pracovního logu a jasně uvést, co ověřeno nebylo.

Nejčastější problémy vznikaly z nejasného vlastnictví, duplicitních zdrojů, práce ve špatném kořeni, absolutních cest, skrytých vedlejších efektů a záměny „agent navrhl“ za „nástroj skutečně ověřil“. Řešením je malé množství jasných vrstev, čitelné změny a ověřitelný pracovní tok.
