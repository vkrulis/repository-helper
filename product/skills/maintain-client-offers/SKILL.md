---
name: maintain-client-offers
description: "Zakládá a udržuje volitelný kontext klientských HTML nabídek: odděluje původní podklady, ověřené závěry, obsah nabídky, publikovatelný web a publikační stopu. Použijte při vytvoření, revizi, validaci, preview nebo přípravě publikace nabídky v klientském projektu; nepoužívejte pro běžnou implementaci bez nabídky."
---

# Udržování klientských nabídek

## Hranice Project Memory

Tato HTML offer capability je určena helper-native layoutu. V Project Memory nevytvářejte
`docs/project/offers/` ani publikační strom jako náhradu MCP promotion. Schválený immutable
offer release přenáší autorizovaná operace do `imports/offers/` se zdrojem a potvrzením;
import není živou nabídkou. Použijte kontrakt projektu a příslušný offer nástroj.

## Hranice capability

`client-offers` rozšiřuje již založený `client-project`; není povinnou součástí každého klientského projektu. Nabídka není epik a její `implementation_epic` je volitelná vazba, nikoli její identita.

- `resources/offers/<offer-id>/` drží převzaté podklady a každá kolekce má README s původem, oprávněním, citlivostí a autoritativností.
- `docs/project/offers/<offer-id>/` drží manifest, ověřené závěry, analýzu, návrh, akceptaci a trasovatelnost.
- `public/offers/<offer-id>/` je jediný explicitně publikovatelný HTML obsah.
- `artifacts/offers/<offer-id>/` drží reprodukovatelné validační a publikační reporty.

## Postup

1. Ověřte, že projekt má capability `client-project`, a přečtěte `docs/agent-context/client-offers-capability.md`.
2. Založte nabídku bez přepisování existujícího obsahu:

   ```bash
   python toolkit/offers/offer_tools.py init-offer --offer-id <offer-id> --project-slug <project-slug> --offer-slug <offer-slug> --title "<název>"
   ```

3. Ukládejte originální vstupy pouze do `resources/offers/<offer-id>/`; do projektové dokumentace zapisujte jen zpracované a ověřené závěry s odkazy na zdroj.
4. Udržujte frontmatter manifestu. URL je deterministicky `https://nabidky.flexideo.cz/{project_slug}/{offer_slug}/`; nezavádějte ručně spravované `published_url`.
5. Vedu dva nezávislé stavy: nabídku `draft|internal-review|client-review|accepted|rejected|archived` a publikaci `unpublished|published|withdrawn`.
6. Do repozitáře neukládejte e-maily příjemců, Cloudflare Access policy, API tokeny ani jiné secrets. Access je provozní konfigurace mimo repozitář; používá explicitní seznam povolených e-mailů a OTP.
7. Před preview nebo předáním spusťte validaci. Publikační workflow musí validaci provést znovu, synchronizovat jen jednu nabídku do jejího R2 prefixu a nesmí měnit Access policy bez explicitního požadavku.

## Kontrola

```bash
python toolkit/offers/offer_tools.py validate --offer <offer-id>
python toolkit/agent-infrastructure/repository_architecture.py validate .
python toolkit/work-log/work-log.py validate .
```

Preview spouštějte přes `python toolkit/offers/offer_tools.py preview --offer <offer-id>`; URL obsahuje stejnou cestu `/offers/<offer-id>/` jako publikovatelný obsah pod vlastním prefixem.

Po materiální změně nabídky, capability nebo nástroje použijte `maintain-work-log`.
