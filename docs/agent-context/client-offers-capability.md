# Klientské nabídky

Tato capability je pro helper-native klientský layout. Project Memory přijímá schválený
immutable offer release přes řízenou MCP promotion do `imports/offers/`; není to živá
nabídka a nevyžaduje instalaci zdejšího HTML/publikačního stromu. Viz
[kompatibilita](client-project-memory-compatibility.md).

## Účel a zdroje pravdy

`client-offers` je volitelné rozšíření `client-project`. Odděluje obchodní nabídku od implementačních epiků, takže klientský projekt může nabídky používat, ale nemusí.

```text
resources/offers/<offer-id>/       původní podklady
        ↓
docs/project/offers/<offer-id>/    ověřené závěry, návrh a trasovatelnost
        ↓
public/offers/<offer-id>/          jediný publikovatelný HTML obsah
        ↓
artifacts/offers/<offer-id>/       validační a publikační reporty
```

Nabídka má stabilní `offer_id`; `implementation_epic` je volitelné propojení po přijetí nabídky a nemění její identitu ani umístění.

## Manifest a životní cyklus

`docs/project/offers/<offer-id>/README.md` začíná YAML frontmatterem s `offer_id`, `project_slug`, `offer_slug`, `title`, `owner`, daty revize, `status`, `publication` a volitelným `implementation_epic`.

- Stav nabídky: `draft`, `internal-review`, `client-review`, `accepted`, `rejected`, `archived`.
- Stav publikace: `unpublished`, `published`, `withdrawn`.

URL je vždy odvozena: `https://nabidky.flexideo.cz/{project-slug}/{offer-slug}/`. `project_slug` a `offer_slug` jsou lowercase slugs a jejich dvojice je v repozitáři jedinečná.

## Podklady a bezpečnost

Každá kolekce v `resources/offers/<offer-id>/` obsahuje README nebo manifest s `source`, `received_at`, `owner`, `format`, `usage_rights`, `sensitivity`, `authoritative` a `related_offer_sections`. Poznámky ze schůzek patří do `meetings/`; do `docs/project/offers/` patří pouze zpracované a ověřené závěry.

Obsah `resources/` se nikdy automaticky nepublikuje. Do `public/` nepatří credentials, tokeny, hesla, privátní klíče, interní podklady ani seznam příjemců. Validace kontroluje základní stopy secrets, odkazy mimo nabídku, lokální soubory, existenci assetů a velikost balíčku.

## Publikační kontrakt

Hosting je sdílený: jednotlivý klientský repozitář publikuje pouze `public/offers/<offer-id>/` do R2 prefixu `/{project-slug}/{offer-slug}/`. Worker na `nabidky.flexideo.cz` obslouží tento prefix a kanonizuje URL s koncovým `/`. Jedna publikace nikdy nesestavuje ani nepřepisuje nabídky jiných repozitářů.

Cloudflare Access chrání URL před aplikací. Používá OTP spolu s explicitním seznamem povolených e-mailů, který je provozní konfigurací mimo Git. Manifest smí obsahovat pouze `access: email-otp` a volitelný technický `access_policy_ref`.

Budoucí `publish-offer --offer <id> --allow <email>` musí: validovat, sestavit deterministický balíček, nahrát jeden prefix, vytvořit či aktualizovat Access, ověřit chráněnou URL a uložit report. Aktualizace obsahu nesmí změnit Access policy bez výslovného požadavku.

## Nástroj

Z kořene cílového repozitáře:

```bash
python toolkit/offers/offer_tools.py init-offer --offer-id offer-2026-001 --project-slug project-slug --offer-slug offer-slug --title "Název nabídky"
python toolkit/offers/offer_tools.py validate --offer offer-2026-001
python toolkit/offers/offer_tools.py preview --offer offer-2026-001
```
