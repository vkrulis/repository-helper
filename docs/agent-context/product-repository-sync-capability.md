# Product repository sync capability

Tato volitelná capability zavádí bezpečnou hranici mezi pracovním repozitářem a
oficiálním Product repository. Použijte ji pouze na výslovné přání uživatele.

## Kontrakt

```text
Workspace/product/**  ↔  Product repository /**
```

- `product/` je jediný synchronizovaný strom; funguje jako allowlist.
- V repozitáři typu `authoring` je `product/` zároveň autoritativní zdroj produktu.
  Product Repository Sync jej nekonstruuje ani neurčuje jeho obsah; pouze bezpečně
  přenáší ověřenou hranici. Build, test a release zůstávají oddělené.
- `public/` a `product/` nesmějí současně existovat. Před založením jedné hranice
  je nutné druhou bezpečně migrovat nebo výslovně odmítnout.
- Výchozí branch mapping je explicitní: `develop ↔ develop`, `main ↔ main`.
  Feature větve se automaticky nesynchronizují.
- Outbound publish i inbound import používají standardně Pull Request. Inbound
  nikdy přímo nezapisuje do `develop` ani `main` pracovního repozitáře.
- Automatická změna nese `sync-id`, směr, zdrojový repozitář, větev a SHA.
  Stejný vstup musí být idempotentní a nesmí spustit ping-pong synchronizaci.
- Při driftu nebo významovém konfliktu se synchronizace zablokuje; nesmí slepě
  přepsat jednu stranu.

## Konfigurace

Konfigurace patří do `.repo-manager/product-sync.yml` a obsahuje alespoň
`product.path: product`, cílový GitHub repository, explicitní mapování větví a
zvolený PR režim. Dokud není známý cílový repository a schválená autentizace,
workflow ani cross-repository zápis nevytvářejte.

Pro automatizaci preferujte GitHub App s minimálním oprávněním (`Contents`,
`Pull requests`, `Metadata`); nepoužívejte jako výchozí mechanismus osobní PAT.
Workflow musí mít explicitní minimální `permissions`, filtrovat pouze mapované
větve a serializovat běhy concurrency group.

Úplné implementační zadání a akceptační scénáře udržuje kanonický dokument
`docs/repository-product-sync-capability.md` v Repository-helperu.
