---
name: maintain-documentation-sync
description: Systematicky propojuje doménovou dokumentaci repozitáře s obecnou dokumentací v samostatném Docusaurus repozitáři. Použijte po změně chování, rozhraní, konfigurace nebo technických detailů, které mohou ovlivnit veřejnou či obecnou dokumentaci, a při revizi existující dokumentační sekce.
---

# Maintain documentation sync

## Zdroj pravdy a pořadí

1. Nejprve ověřte aktuální chování v kódu, testech a doménové dokumentaci cílového repozitáře.
2. Aktualizujte doménovou dokumentaci v `docs/agent-context/` včetně technických detailů a odkazů na skutečné soubory.
3. Teprve potom vyhledejte dotčené stránky v sourozeneckém repozitáři obecné dokumentace, typicky v `public/`.
4. Opravte, doplňte nebo založte obecnou dokumentaci podle ověřeného doménového stavu. Nezaměňujte produktový záměr nebo schéma za ověřené chování.
5. Proveďte validační příkazy obecné dokumentace (minimálně její vlastní metadata validator a Docusaurus build, pokud je dostupný).
6. Publikaci na web nebo upload na hosting proveďte jen podle pravidel cílového dokumentačního repozitáře a výslovného rozsahu práce.

## Hlavička obecné dokumentace

Zachovejte existující `source`, `source_url` a `exported_at`. Každý soubor, který je touto revizí změněn, musí mít navíc:

```yaml
revised_by: "minor: correction"
revised_at: "2026-08-09T12:34:56+02:00"
```

`revised_by` není jméno autora. Používejte přesně jeden ze tří rozsahů `minor`, `substantial`, `structural` a stručný důvod po dvojtečce. Doporučená jednotná klíčová slova důvodu jsou `correction`, `extension` a `restructuring`; jiný důvod musí být stále krátký a věcný. `revised_at` je datum a čas zápisu v ISO 8601 včetně časového pásma.

Nově založené sekce mají:

```yaml
source: repository
repository: fxd-updater
source_url: "repository://fxd-updater/docs/agent-context/domain/..."
exported_at: "2026-08-09T12:34:56+02:00"
revised_by: "structural: extension"
revised_at: "2026-08-09T12:34:56+02:00"
```

`repository` je logický název repozitáře, nikoli název lokální složky.

## Vazba z doménové dokumentace

Do hlavičky každého relevantního doménového dokumentu přidejte pole `general_documentation` s jedním nebo více cíli oddělenými středníkem. Cíl je cesta od kořene documentation repozitáře, například:

```yaml
general_documentation: "public/supp-fxd-concept-cz/replication/index.md; public/supp-fxd-updater-cz/architecture/index.md"
```

Pokud se změna týká širšího tématu, zvažte další existující nebo novou sekci. Rozšíření vazeb, které mění významovou strukturu dokumentace, nejprve popište uživateli a vyžádejte si potvrzení.

## Bezpečnost a hranice

- Neaktualizujte obecnou dokumentaci před dokončením doménové revize.
- Nepřepisujte zdrojové exporty bez zachování jejich původu a licence.
- Nehádejte obsah stránky pouze podle názvu; vyhledejte skutečné odkazy a ověřte kód.
- Pokud není obecná dokumentace dostupná nebo je publikace blokovaná, dokončete bezpečně doménovou část a uživatele výslovně upozorněte na otevřený krok.
- Po materiální změně použijte `maintain-work-log`.

## Kontrola

Z kořene dokumentačního repozitáře spusťte validator nad právě změněnými soubory:

```text
python toolkit/agent-infrastructure/validate_documentation_metadata.py <documentation-root> --files public/<changed-file>.md --require-revision
```

Z kořene doménového repozitáře ověřte odkazy, pokud je dokumentační repozitář dostupný:

```text
python <repository-helper>/toolkit/agent-infrastructure/validate_documentation_metadata.py <domain-root> --domain-root docs/agent-context --public-root <documentation-root> --files docs/agent-context/domain/<changed-file>.md --require-links
```

Na závěr vždy uživatele upozorněte, zda byla provedena revize doménové dokumentace, obecné dokumentace a publikace.
