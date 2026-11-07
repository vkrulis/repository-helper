---
name: import-legacy-work-logs
description: Převádí historická vývojová podtémata, deníky a volné datované poznámky do jednotného pracovního indexu .logs/YYYY/MM/YYYY-MM-DD.md, aniž by měnil původní zdroje nebo domýšlel změněné soubory a validace. Použijte při migraci starších pracovních poznámek do schopnosti maintain-work-log, při opakovaném importu nových ročníků a při kontrole provenance importovaných záznamů.
---

# Import legacy work logs

## Zásady

1. Zachovejte původní soubory beze změny jako úplný historický zdroj.
2. Před importem explicitně určete rok každého zdroje; neodvozujte nejednoznačný rok potichu.
3. Datovaný blok převeďte do `.logs/YYYY/MM/YYYY-MM-DD.md` a přidejte stabilní ID a téma `legacy-import`.
4. Rozlište `done`, `partial`, `planned` a `blocked`; směs dokončené a otevřené práce označte `partial`.
5. Nedoložené změněné soubory uveďte jako neuvedené. Tvrzení „otestováno“ bez příkazu a výstupu označte jako historické tvrzení, nikoli nově ověřenou validaci.
6. Uveďte zdrojový soubor a řádek nebo jiný stabilní lokátor. Při rozporu má přednost originál a současný stav cílového repozitáře.
7. Převod proveďte idempotentním nástrojem. Existuje-li projektový převodník, použijte jej; jinak uložte nový deterministický nástroj do cesty předepsané cílovým repozitářem, typicky `toolkit/skills/import-legacy-work-logs/`.
8. Před zápisem spusťte suchý běh, po zápisu jej zopakujte a ověřte, že nevzniknou duplicity.
9. Nakonec spusťte `python toolkit/work-log/work-log.py validate .`.

## Mapování

- dokončená změna → odpovídající typ, stav `done`;
- dokončená i navazující práce → stav `partial` a sekce `Navazující práce`;
- pouhý plán → stav `planned`;
- nevyřešená překážka → `investigation`, stav `blocked`;
- analýza bez změny → `investigation`;
- URL a issue odkazy → sekce `Odkazy`.

Importovaný log je vyhledávací index, nikoli náhrada originálu, Gitu, aktuální dokumentace nebo důkazu provedené validace.
