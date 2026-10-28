---
name: maintain-project-documentation
description: "Udržuje aktuální projektovou dokumentaci klientské Flexideo aplikace v docs/, odděluje ji od epiků Project Memory a propojuje XDS/FDT/DAD, intranetové funkce, COMEX UI, procesy, integrace a provoz bez vytváření druhého zdroje pravdy."
---

# Udržování projektové dokumentace

## Kdy skill použít

Použijte jej, když je potřeba založit, doplnit, zrevidovat nebo aktualizovat dokumentaci
**současného stavu klientské aplikace**.

Vždy načtěte [referenční model](references/project-documentation-model.md).
Pokud práce zasahuje x-item/settings/akce/procesy, COMEX stránky/komponenty, technické
karty, usage mapu nebo refresh/coverage, načtěte také
[detail aplikační a COMEX reference](references/application-comex-reference.md).

## 1. Rozpoznejte projekt a hranici autority

1. Pokud existují `project.yaml` a `.project-memory/`, jde o Project Memory. Neměňte jeho
   analytický kontrakt.
2. `project/epics/EPIC-NNNN/` drží zadání, analýzu, evidence, rozhodnutí a historii změny.
3. `docs/` popisuje aktuální aplikaci: co existuje, jak je to propojeno a jak se to používá.
4. Do `docs/` nekopírujte otevřené otázky, checkpointy ani úplné Decision Records.
5. U helper-native projektu dodržte obdobnou hranici vůči `docs/project/`.

## 2. Rozlišujte kurátorovaný a generovaný obsah

Kurátorovaný aktuální výklad patří do:

~~~text
docs/
├── aplikace/
├── datovy-model/
├── procesy/
├── integrace/
└── provoz/
~~~

Generované nebo odvozené technické reference patří pod `docs/reference/` pouze tehdy,
když mají dohodnutého producenta, manifest/provenance a pravidla refresh.

Dnes je potvrzená rodina `docs/reference/fdt/`.

Rodiny `application/`, `comex/`, `usage/` a `indexes/` jsou návrhový směr.
Nevytvářejte je ručně jako kanonickou dokumentaci před přijetím packager kontraktu.
Pracovní pilotní výstup držte ve stagingu mimo `docs/reference/`.

## 3. Určete zdroj každého tvrzení

- **XDS** – autorita FDT a jejich vlastností.
- **FDT reference** – technická projekce XDS/FDT/DAD.
- **Intranet x-item/settings/registry/buildy** – autorita aplikační kompozice.
- **COMEX/CXD + registry** – autorita prezentační kompozice.
- **runtime instance** – evidence skutečného nasazení a viditelnosti.
- **Project Memory** – původ změny a potvrzený kontext.
- **doménová revize** – business účel, scénáře, odpovědnosti a akceptace.

Chybějící zdroj nepřekrývejte odhadem.

## 4. Datový model

Neopisujte ručně úplnou FDT strukturu.

Kurátorujte:

- business datové objekty;
- významné vztahy;
- stavové modely;
- číselníky;
- fyzické mapování jen tam, kde pomáhá porozumění.

Podkladové datové FDT berte z explicitní klasifikace producenta nebo ověřené XDS analýzy.
Pohledové a pseudo typy nejsou automaticky primární business entity.

## 5. Aplikační funkce

Do `docs/aplikace/` patří ruční výklad aktuální aplikace, zejména:

- architektura;
- strom a funkční oblasti;
- role/přístupy v míře doložené projektem;
- `funkce/<stable-key>.md`;
- `scenare/<stable-key>.md`.

Technické karty x-itemů, přehledů, sloupců, tools, akcí, procesů a COMEX projekcí
nepište ručně jako druhý katalog, pokud mají být regenerovatelné z instance.

## 6. Technické identity a vztahy

Nikdy neslučujte:

- PDK, auto_id a cestu x-item;
- navigační rodičovství a procesní členství;
- navigační konzument a linked settings source;
- registraci akce, authoring setting, transform name a build;
- process container a process node;
- COMEX page, component instance a component source;
- FDT, DAD/SQL tabulku a intranetový přehled.

U typed relation zachovejte podmínku, resolution status a evidence.

## 7. FDT použití

Rozlišujte:

- view → FDT/segment;
- action input type = deklarované čtení;
- action output type = deklarovaný zápis;
- action matching type = nabídka/použitelnost;
- UI tool → vytvoření/editace/náhled;
- process output → FDT + druh účinku;
- segmentové čtení/zápis z konkrétního výrazu/těla.

Output type neznamená zápis všech polí.

## 8. COMEX

`on_comex` samo o sobě není důkaz UI.

Při dokumentaci oddělte:

~~~text
source x-item/settings
→ generator projection
→ deployed CXD
→ runtime role/UI
~~~

Zahrňte i custom PageEdit stránky a komponenty, které nevznikly creator větví.

## 9. Coverage a aktuálnost

Každá technická odpověď nebo karta má nést scope, čas, zdrojové revize a mezery.

Nedostupný zdroj nebo neúplný sběr se nevyhodnocuje jako „nepoužívá se“.

Z „nenalezeno“ lze udělat „v tomto scope nepoužito“ až při doloženém úplném pokrytí.

## 10. Aktualizace po změně

Když epic nebo provozní změna mění skutečný stav:

1. určete dotčené vrstvy;
2. ověřte výslednou Current Truth;
3. obnovte FDT reference jen při změně definic;
4. settings/registry/buildy obnovte nezávisle na replikaci;
5. COMEX/PageEdit obnovte nezávisle na datovém modelu;
6. runtime ověřujte jen pro tvrzení o skutečné funkci/roli;
7. aktualizujte kurátorované `docs/`;
8. historii ponechte epiku a Gitu.

## 11. Procesy, integrace a provoz

### Procesy

Popisujte business průběh a explicitně jej mapujte na technické procesní kontejnery/uzly,
akce, FDT a UI.

### Integrace

Popište účel, protistranu, trigger/směr, autentizaci bez secrets, datový kontrakt, FDT,
akci/službu, chybové chování a provozní dohled.

### Provoz

Udržujte prostředí, deployment/release, monitoring, joby, zálohy, obnovu, incidenty,
troubleshooting a rollback. Rozlišujte definováno/vydáno/nasazeno.

## 12. Kvalita kurátorované stránky

Věcná stránka má obsahovat zdroje a aktuálnost:

~~~markdown
## Zdroje a aktuálnost

- Ověřeno: YYYY-MM-DD
- Scope: <projekt / aplikace / prostředí / role>
- Zdroj: <relativní odkaz nebo identita>
- Omezení: <co zdroj nedokazuje>
~~~

## 13. Validace

Spusťte:

~~~bash
python toolkit/skills/maintain-project-documentation/project_documentation.py validate .
python toolkit/skills/maintain-project-documentation/project_documentation.py inventory .
~~~

Potom spusťte validátor vlastníka Project Memory nebo cílového repozitáře.

## Bezpečnost

- Neukládejte credentials, session ani produkční osobní data.
- Administrátorské čtení není důkaz UI cílové role.
- XSD validace neprokazuje funkční stránku.
- Generované reference neupravujte ručně.
- Dokumentační nesoulad není automatické povolení měnit XDS, settings, registry ani COMEX.
