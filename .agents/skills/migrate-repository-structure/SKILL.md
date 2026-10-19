---
name: migrate-repository-structure
description: Citlivě a kontrolovaně převede existující repozitář do společné struktury README.md, AGENTS.md, docs/agent-context, .agents/profiles, .agents/skills, jednotného toolkit a resources. Použijte až po dokončeném auditu a schválení migrační mapy. Skill může provést i rozsáhlé přesuny a konsolidaci, ale musí zachovat význam, opravit odkazy, používat git mv, průběžně validovat a zastavit se před nejasnou nebo destruktivní změnou.
compatibility: Vyžaduje write přístup, Git a možnost spustit projektové validační příkazy.
metadata:
  version: "1.0"
  requires-prior-skill: audit-repository-structure
---

# Migrace struktury existujícího repozitáře

## Hranice Project Memory

Před obecnou migrací zkontrolujte `project.yaml` a `.project-memory/`. Strukturu Project
Memory řídí kontrakt Orchestrátoru; tento skill nepřesouvá její analytiku do
`docs/project/`, nezakládá paralelní mise ani nekonsoliduje Current Truth do
`docs/agent-context/`. Přechod Memory 0.1 → 0.2 patří řízenému migračnímu nástroji
s reviewed manifestem a připnutým head/blob SHA. Nejasnou budoucí verzi pouze zdokumentujte.

## Vstupní podmínky

Před změnami musí existovat:

- audit struktury,
- navržená cílová struktura,
- migrační mapa,
- vyřešené nebo výslovně odložené rozhodovací otázky,
- známý stav pracovního stromu,
- validační plán.

Pokud některá z těchto podmínek chybí, vraťte se k `audit-repository-structure`.

## Bezpečnostní brána

Zastavte se, pokud:

- pracovní strom obsahuje překrývající se necommitnuté změny,
- není jasný autoritativní dokument,
- přesun mění veřejné importy nebo deployment bez schválení,
- plán obsahuje `remove` bez explicitního potvrzení,
- nelze spustit žádnou relevantní validaci,
- repozitář obsahuje podezřelé secrets v přesouvaných souborech.

## Postup

### 1. Založte migrační záznam

Použijte `references/migration-plan-template.md` nebo existující schválený plán. Evidujte stav každé položky. Pro architektonicky významná rozhodnutí aktivujte `maintain-decision-records`; nevytvářejte paralelní migrační formát ADR. Pro architektonicky významná rozhodnutí aktivujte `maintain-decision-records`; nevytvářejte paralelní migrační formát ADR.

### 2. Vytvořte cílovou kostru

Nejdříve vytvořte cílové adresáře a orientační README bez přesouvání aplikačního kódu.

Primární typ určete podle `docs/agent-context/repository-types.md`. Pro typ `authoring`
nainstalujte capability `authoring-repository` a migrujte publikovatelný produkt do
`product/` až podle schválené mapy. Produktové skills pak udržujte pouze v
`product/skills/`; kořenové `.agents/skills/` ponechte pro údržbu workspace. Pro typ
`client-project` použijte capability `client-project`, pro `documentation`
`documentation-sync` a pro běžný runtime vývoj zachovejte standardní projektové cesty.

Pokud je z auditu zřejmé, že jde o vývoj webu samotného (ne o authoring, ne o
dokumentaci, ne o binární/desktopovou aplikaci — viz „Rozšíření pro webový vývoj"
v `repository-architecture.md`) a repozitář zatím nemá kořenovou `public/`, založte
ji a existující nasazovaný/publikovaný obsah do ní přesuňte přes `git mv`. Do
`AGENTS.md` zapište stručně konkrétní účel `public/` v tomto projektu. Pokud
repozitář už vlastní obdobný web-root vzor pod jiným názvem se zavedeným významem,
nepřejmenovávejte jej bez explicitního schválení.

Jestliže uživatel výslovně požaduje Product Repository Sync, použijte místo tohoto
postupu capability `product-repository` a skill `manage-product-repository`.
Před přesunem ověřte, že v cíli nevznikne souběh `public/` a `product/`; tyto dvě
hranice jsou vzájemně výlučné.

Nainstalujte kanonické repository schopnosti:

```bash
python toolkit/agent-infrastructure/repository_architecture.py install-capability <target> --name work-log
python toolkit/agent-infrastructure/repository_architecture.py install-capability <target> --name decision-records
```

Tím distribuujte pracovní log, konzervativní ADR metodiku a odpovídající pravidla v `AGENTS.md`. Existující varianty bez kontroly nepřepisujte; `--force` použijte pouze po porovnání.

### 3. Konsolidujte společná pravidla

- Vytvořte nebo upravte kořenový `AGENTS.md`.
- Sloučte pouze skutečně společná pravidla.
- Platformní zvláštnosti ponechte v konektorech.
- Odstraňte duplicity až poté, co je nový zdroj pravdy úplný a odkazy jsou opravené.

### 4. Přesuňte projektovou znalost

Použijte `git mv` pro:

- architekturu,
- vývojové konvence,
- testovací návody,
- doménové reference,
- rozhodovací záznamy.

Rozdělte smíšené soubory, pokud kombinují znalost, pracovní pravidla a platformní prompt. Každý nový fragment musí mít jasný účel.

### 5. Konsolidujte skills

- Rozpoznejte opakovatelné postupy ve starých prompts, commands a runboocích.
- Každý skill musí řešit jednu práci.
- Vytvořte validní YAML frontmatter.
- Dlouhé reference přesuňte do `references/`.
- Veškerou deterministickou logiku přesuňte pod `toolkit/`; nástroj jediného přenositelného skillu patří do `toolkit/skills/<skill-name>/`, nikoli dovnitř `.agents/skills/`.

### 6. Konsolidujte profily

- Z platformních agentů odvoďte neutrální profil v `.agents/profiles/`.
- Zachovejte roli, odpovědnost, skills, capabilities, restrictions, context a outputs.
- Nativní názvy nástrojů nepřenášejte do kanonických capabilities.

### 7. Přesuňte nástroje

Všechny exaktní nástroje konsolidujte pod kořenový `toolkit/`. Použijte `toolkit/agent-infrastructure/` pro správu agentní vrstvy, `toolkit/domain/` pro doménové nástroje, `toolkit/development/` pro build/test automatizaci, `toolkit/skills/<skill-name>/` pro nástroj jediného skillu a `toolkit/runtime/` pro spustitelné artefakty. Pokud již `toolkit/` existuje, zachovejte jeho význam a konflikt řešte podsložkami. Odstraňte nástroje z `.agents/tools/`, kořenového `tools/`, kořenového `scripts/` a skillových `scripts/` až po opravě všech odkazů.

Při změně cesty opravte:

- dokumentaci,
- CI,
- Makefile/package scripts,
- hooks,
- skills,
- importy,
- testy.

### 8. Konsolidujte zdroje k analýze

- Projektové datové vstupy, schémata, snapshoty a cizí či historický zdrojový kód určený k analýze konsolidujte do `resources/`, pokud tím nerozbijete existující veřejné cesty.
- Běhový nebo sestavovaný kód nepřesouvejte ze `src/` jen proto, že jej lze analyzovat.
- Testovací fixtures ponechte v konvenci testovacího frameworku, pokud nemají širší projektové využití.
- Vytvořte `resources/README.md` a evidujte původ, licenci, formát, autoritativnost a způsob aktualizace.
- Podklady výhradně jednoho přenositelného skillu ponechte v jeho `references/` nebo `assets/`.

### 9. Obnovte platformní konektory

Aktivujte `add-platform-connector` pouze pro požadovanou platformu. Při práci v Codexu lze bez jiné preference zvolit Codex; v jiném nebo neznámém prostředí se zeptejte a připusťte variantu bez konektoru. Nikdy automaticky nevytvářejte více konektorů.

Staré platformní soubory odstraňte nebo archivujte až po ověření nového konektoru.

### 10. Aktualizujte hlavní README

README musí odpovídat výsledné skutečné struktuře a uvést:

- rychlý start,
- build/test/validation,
- odkazy na kontext,
- umístění agentních pravidel a skills.

### 11. Validujte po každém celku

Po významné skupině změn spusťte nejmenší relevantní kontrolu. Na konci spusťte:

- `validate-repository-architecture`,
- projektové testy,
- build nebo lint,
- kontrolu odkazů, pokud je dostupná,
- `git status`, `git diff --stat` a cílenou kontrolu diffu.

## Zásada čistého výsledku

Nenechávejte dlouhodobě:

- souběžně starou a novou strukturu,
- neoznačené generované kopie,
- odkazy na neexistující cesty,
- prázdné platformní adresáře,
- nevyřešené `TODO` bez vlastníka nebo rozhodovacího záznamu.

Přechodná kompatibilita je přípustná pouze s časově omezeným a zdokumentovaným plánem odstranění.

## Výstup

Uveďte:

- provedené přesuny a konsolidace,
- záměrně ponechané odchylky,
- opravené vazby,
- neprovedené položky a důvod,
- výsledky všech validací,
- doporučený commit breakdown.

Před finálním předáním nechte výsledek zkontrolovat profilem `repository-migration-reviewer`, je-li dostupný.
