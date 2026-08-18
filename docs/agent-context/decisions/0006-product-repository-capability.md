# ADR-0006: Capability Product repository

- Stav: accepted
- Datum: 2026-08-18
- Scope: shared
- Vlastník: Repository-helper maintainers
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Vývojový workspace může obsahovat neveřejný kontext, zatímco oficiální produkt
má být samostatný GitHub repository. Dosavadní webová konvence `public/` tento
obousměrný, auditovatelný kontrakt nevyjadřuje a její souběh s novou hranicí by
byl nejednoznačný.

## Zvažované možnosti

### Možnost A — ponechat obecný `public/`

Jednoduché pro samostatné webové repozitáře, ale bez přesné product projekce a
bez pravidel pro bezpečnou synchronizaci dvou repozitářů.

### Možnost B — volitelná capability s hranicí `product/`

Zavést explicitní, instalovatelnou capability se striktní produktovou hranicí a
oddělit ji od běžného webového `public/`.

## Rozhodnutí

Přijímá se možnost B. Repository-helper poskytuje capability `product-repository`
a skill `manage-product-repository`. `product/` je allowlist produktového obsahu;
`public/` a `product/` se nesmějí v pracovním repozitáři vyskytovat současně.

Automatická synchronizace vyžaduje explicitní target, branch mapping, GitHub App,
dry-run, provenance a ochranu proti smyčkám. Bez těchto vstupů capability připraví
jen lokální hranici, nikoli automatické cross-repository zápisy.

## Důsledky

- Běžné webové repozitáře mohou nadále používat `public/`.
- Nové i existující repozitáře lze na `product/` převést pouze na výslovné přání
  a po kontrole původu obsahu.
- Instalátor capability distribuuje pravidlo, kontextový dokument a skill;
  konkrétní GitHub workflow zůstává až následným bezpečně nakonfigurovaným krokem.
