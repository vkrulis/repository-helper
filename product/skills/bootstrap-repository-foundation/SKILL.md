---
name: bootstrap-repository-foundation
description: Vstupní skill produktu Repository Foundation. Rozpozná typ a stav cílového repozitáře a vybere nejmenší capability pro založení, audit, migraci, validaci nebo aktualizaci jeho struktury. Použij před strukturální změnou klientského, vývojového, authoringového nebo dokumentačního repozitáře; nezařazuje úkol do A–E.
---

# Bootstrap Repository Foundation

1. Urči cílový repozitář, požadovaný výsledek a zda jde o nový nebo existující obsah.
2. Přečti `../../references/repository-types.md` a pro Project Memory také
   `../../references/client-project-memory-compatibility.md`.
3. Pro nový obecný repozitář použij `initialize-agent-ready-repository`; pro existující
   obsah nejprve `audit-repository-structure` a až po schválené mapě
   `migrate-repository-structure`.
4. Pro klientský repozitář použij `maintain-client-project-dimension`. Project Memory je
   jeho analytická podmnožina; nevytvářej vedle ní `docs/project/` ani druhou Current Truth.
5. Instaluj jen capability potřebné pro aktuální fázi. Nabídky, dokumentace, inventáře,
   testování a Product Repository Sync nejsou automaticky součástí každého projektu.
6. Použij `tools/agent-infrastructure/repository_architecture.py` pro audit, instalaci
   a validaci. Před aktualizací spravovaných souborů zkontroluj jejich manifest a lokální
   změny; neznámý stav nepřepisuj.
7. Po materiální změně spusť projektové validace a přidej append-only pracovní log.
8. Pokud běh skutečně použil capability z FCL, načti `record-authoring-feedback` a před
   označením smysluplného checkpointu nebo úkolu za dokončený zapiš jeden validní
   Authoring Feedback Event do klientského denního logu. Pouhé načtení capability
   není použití; neodpovězené lidské hodnocení dokončení neblokuje.

Výstupem je rozpoznaný repository typ, zvolená capability, seznam změn, skutečně
provedené validace a otevřené vstupy. Authoringovou klasifikaci A–E předává FCL.
