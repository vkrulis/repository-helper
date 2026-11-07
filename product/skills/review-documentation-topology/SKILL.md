---
name: review-documentation-topology
description: Reviduje strukturu Markdown dokumentace, překryvy, rozpory a navigaci a navrhuje doložené přesuny či rozdělení. Použijte při reorganizaci dokumentační oblasti, nikoli jako náhradu správy analytického stavu projektu.
---

# Revize dokumentační struktury

Vymezte oblast podle README/AGENTS a místní `.agents/documentation.json`, pokud
existuje. Oddělte obsahovou autoritu, publikum, generované reference a publikované
cesty. Fyzické stáří souboru ani textová podobnost nerozhodují o autoritě.

- Pomocí `search-markdown-content` vyhledejte kandidáty a přečtěte celé stránky,
  rozcestníky, metadata a vazby. U každého nálezu uveďte konkrétní cestu a důkaz.
- Rozlišujte duplicitu, rozpor, zastaralost, nevhodné umístění a chybějící navigaci.
  Generovanou referenci posuzujte vůči producentovi a jeho zdrojové revizi.
- Připravte mapu zdroj → cíl → akce → autorita → odkazy → ověření. Historické
  doklady a samostatně užitečné pohledy zachovejte; nezakládejte druhou aktuální pravdu.
- Při nevyřešené prioritě nebo zásahu do veřejných cest předložte konkrétní varianty.
  Již schválenou migraci proveďte po malých celcích a ověřte odkazy i relevantní build.

Project Memory zakládá a migruje její vlastník. Tento skill nepřevádí epiky
do `docs/project/`, nemění `.project-memory/` ani nestanoví nové analytické ADR.
Změna struktury dokumentace není přijetím nového projektového významu.
Ve výsledku uveďte autoritativní cíle, zbývající nejasnosti a skutečné validace.
