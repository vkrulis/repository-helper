---
name: maintain-authoring-repository
description: Zakládá, klasifikuje, migruje a udržuje authoring repozitáře, jejich autoritativní product/ strom a hranice vůči runtime, klientským projektům, dokumentaci a nadřazenému orchestrátoru. Použijte pro specializovaný authoring jedné vrstvy i pro orchestrační authoring napříč vrstvami; nepoužívejte pro běžný vývoj runtime produktu ani pro klientský implementační projekt.
---

# Authoring repository

## Před změnou

1. Přečtěte `docs/agent-context/repository-types.md` a
   `docs/agent-context/authoring-repository-capability.md` z helperu nebo jejich
   instalované kopie v cílovém repozitáři.
   Při návrhu nebo revizi registry načtěte také
   `docs/agent-context/authoring-registry-current-state-contract.md`.
2. Určete primární typ repozitáře. Authoring repozitář vytváří a ověřuje přenositelné
   definice, konfigurace, skills, kontrakty nebo authoring nástroje; není runtime
   implementací ani jednou klientskou aplikací.
3. Určete authoring roli:
   - `specialist` vlastní jednu vymezenou vrstvu nebo oblast;
   - `orchestrator` analyzuje záměr, vybírá specialisty a koordinuje změnu napříč
     vrstvami, ale nekopíruje jejich detailní znalost.
4. U existujícího obsahově rozvinutého repozitáře nejprve použijte
   `audit-repository-structure`. Nejasné přesuny nebo změny zdroje pravdy vyžadují
   schválenou migrační mapu a případně ADR.

## Autoritativní organizace

- Kořen workspace drží interní kontext, maintenance skills, resources, build/test/release
  nástroje a pracovní historii.
- `product/` je jediný autoritativní zdroj publikovatelného authoring produktu.
- Produktové skills vznikají přímo v `product/skills/`; neudržujte jejich druhou
  commitnutou kopii v kořenových `.agents/skills/`.
- Sdílené produktové nástroje patří do `product/tools/`, strojově čitelné kontrakty do
  `product/contracts/` a produktové release testy/evaly do `product/tests/`.
- Reference, scripts a assets jediného produktového skillu zůstávají uvnitř jeho balíku.
  Obslužné a interní nástroje workspace patří pod kořenový `toolkit/`.
- `public/` a `product/` nesmějí v jednom workspace koexistovat.

Minimální strom vytvořte instalací capability, ne ručním kopírováním:

```text
python toolkit/agent-infrastructure/repository_architecture.py install-capability <target> --name authoring-repository
```

Capability instaluje i lokální product boundary a potřebný kontext. Cílový Product
repository, credentials a synchronizační workflow nevymýšlejte; doplňte je až při
výslovném požadavku pomocí `manage-product-repository`.

Registry standardně publikuje pouze aktuální validovaný stav na stabilních cestách.
Digest slouží k detekci změny, ověření integrity a resolution locku, nikoli jako
cloudový adresář. Odchylku od current-state kontraktu doložte samostatným ADR.

## Hranice rolí

### Specializovaný authoring

- Vlastní význam, workflow a validace své oblasti.
- Vydává vlastní verzované skills, contracts a případné tools.
- Od runtime repozitáře čerpá ověřená omezení a operace, ale nepřebírá jeho implementaci.
- Do klientského projektu předává výsledek a evidence; nepřebírá projektové zadání,
  akceptaci ani jediný projektový definiční model.

### Orchestration authoring

- Je nadřazenou authoring entitou pro koordinovanou tvorbu a úpravy celé aplikace.
- Udržuje analýzu záměru, routing, handoff kontrakty, discovery, lock a trace.
- Načítá registry produktů specializovaných authoring repozitářů podle vrstvy, role,
  verze a zralosti.
- Nevkládá do svého produktu kopie specializovaných skills ani doménové implementace;
  drží pouze orchestrační metodiku, kontrakty a resolver.

## Documentation vztah

Dokumentační repozitář je samostatný primární typ, i když je authoringu blízký. Sbírá a
konsoliduje ověřenou technickou/doménovou dokumentaci vrstev a může vydávat uživatelskou
dokumentaci. Není obecným skladištěm pracovních poznámek ani náhradním zdrojem pravdy pro
runtime či authoring. Synchronizaci znalostí řešte `maintain-documentation-sync`.

## Validace a předání

1. Ověřte, že produkt je samostatně čitelný a testovatelný bez interního workspace.
2. Spusťte produktové testy/evaly a validační příkazy repozitáře.
3. Spusťte `validate_skill_collection.py`, `repository_architecture.py validate`,
   `git diff --check` a validaci pracovního logu.
4. Uveďte roli authoringu, produktovou hranici, skutečně ověřené release evidence,
   neprovedenou publikaci a otevřené migrační kroky.
