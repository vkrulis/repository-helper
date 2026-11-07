---
name: manage-product-repository
description: Zavede nebo bezpečně migruje explicitně požadovanou hranici product/ pro synchronizaci pracovního a GitHub Product repository. Použijte jen když uživatel chce Product Repository Sync; nepoužívejte pro běžný samostatný webový public/.
---

# Product repository

## Před změnou

1. Přečtěte `docs/agent-context/product-repository-sync-capability.md`.
2. Zjistěte stav Gitu, existenci `public/` a `product/`, cílový Product repository,
   mapované větve a dostupný způsob autentizace.
3. Pokud chybí cílový repository, GitHub App instalace nebo význam cílového obsahu,
   připravte pouze lokální hranici a konfiguraci bez automatického publish/importu;
   nevymýšlejte remote ani credentials.

## Zavedení a migrace

- Pracovní repozitář smí po dokončení obsahovat právě jednu z cest `public/` nebo
  `product/`. Pokud existují obě, zastavte se; nejprve bezpečně vyřešte jejich
  původ a obsah.
- Pro existující obsah použijte Git-preserving přesun. Při necommitnutých nebo
  vnořených Git repozitářích nejdříve doložte stav a přesouvejte jen po výslovném
  požadavku uživatele.
- `product/` nesmí obsahovat agentní infrastrukturu, interní dokumentaci ani
  pomocné nástroje pracovního repozitáře, pokud nejsou samy součástí produktu.
- V authoring repozitáři je `product/` současně autoritativním zdrojovým stromem produktu,
  nikoli až generovanou kopií. Produktové skills vznikají v `product/skills/`; kořenové
  `.agents/skills/` obsahují pouze údržbu workspace. Synchronizace strom pouze přenáší,
  zatímco build, testy a release evidence řeší authoring capability.
- Zaznamenejte konkrétní význam hranice a cílový způsob distribuce v architektuře
  repozitáře. U dlouhodobého rozdělení zdrojů pravdy zvažte ADR.

## Synchronizace GitHub

- Konfiguraci uložte do `.repo-manager/product-sync.yml` s `product.path: product`,
  explicitním targetem a branch mappingem. Výchozí `outbound` i `inbound` režim je
  `pull-request`; inbound nevytváří přímý zápis do chráněné větve.
- Automatizaci zapněte až po dry-run, ověření oprávnění GitHub App a ochran větví.
  Každý běh musí být branch-aware, idempotentní, auditovatelný a chráněný proti
  smyčce; při driftu či konfliktu vytvořte diagnostiku nebo PR, nikoli přepis.
- Nemíchejte sync workflow s produktovými build/release workflow. Produktové
  workflow, které mají být distribuovány, patří do `product/.github/`.

## Ověření a předání

Ověřte, že vedle sebe nezůstaly `public/` a `product/`, že se do produktové
projekce nedostaly soubory mimo její hranici a že dokumentace odpovídá skutečnému
remote a větvím. Spusťte projektové validace, `git diff --check` a pracovní log.
Uveďte, zda byla zavedena jen lokální hranice, nebo i bezpečně připravená GitHub
synchronizace, včetně neprovedených kroků.
