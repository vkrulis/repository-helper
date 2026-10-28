---
name: maintain-project-documentation
description: "Udržuje aktuální projektovou dokumentaci klientské Flexideo aplikace v docs/, odděluje ji od epiků Project Memory a propojuje XDS/FDT/DAD, intranetové komponenty, COMEX UI, procesy, integrace a provoz bez vytváření druhého zdroje pravdy."
---

# Udržování projektové dokumentace

## Kdy skill použít

Použijte jej, když je potřeba založit, doplnit, zrevidovat nebo aktualizovat dokumentaci
**současného stavu klientské aplikace**.

Nejprve načtěte [referenční model](references/project-documentation-model.md). Ten je
normativní pro hranici mezi Project Memory a dokumentací i pro vztah XDS/FDT, intranetu a
COMEXu.

## 1. Rozpoznejte projekt a hranici autority

1. Pokud existují `project.yaml` a `.project-memory/`, jde o Project Memory. Čtěte její
   verzi, ale neměňte její analytický kontrakt.
2. `project/epics/EPIC-NNNN/` obsahuje zadání, analýzu, evidence, rozhodnutí a historii změny.
3. `docs/` popisuje pouze aktuální aplikaci: co existuje, jak je to propojeno a jak se to používá.
4. Nikdy nekopírujte do `docs/` otevřené otázky, pracovní hypotézy, checkpointy ani úplné
   rozhodovací záznamy. Je-li původ důležitý, odkažte na epic/Decision.

U helper-native klientského projektu dodržte obdobnou hranici vůči `docs/project/`.

## 2. Nejdřív zjistěte zdroje

Pro každé tvrzení určete vlastníka:

- **XDS** – definiční autorita FDT a jejich vlastností;
- **`docs/reference/fdt/`** – generovaná reference Replicatoru, ne editační zdroj;
- **Intranet x-item + saved settings + registry** – autorita kompozice složek, přehledů,
  akcí a procesních uzlů;
- **COMEX/CXD** – odvozená/provozní projekce komponent a stránek;
- **runtime instance** – evidence skutečného nasazení a viditelnosti;
- **Project Memory** – původ změny a potvrzený kontext.

Chybějící zdroj nepřekrývejte odhadem. Výslovně označte, co je doložené a co je potřeba
ověřit.

## 3. Udržujte jeden současný dokumentační strom

Preferovaný strom:

~~~text
docs/
├── index.md
├── aplikace/
├── datovy-model/
├── procesy/
├── integrace/
├── provoz/
└── reference/fdt/
~~~

Nevytvářejte všechny podsložky dekorativně. Materializujte jen skutečně potřebné stránky.

### Aplikace

Do `docs/aplikace/` patří architektura, hlavní funkční oblasti, navigační strom, technické
karty intranetových komponent a jejich projekce do COMEXu.

U jedné komponenty oddělte:

- x-item identitu a navigační umístění;
- owning saved setting a případné linky;
- používané FDT;
- MTP/pomocné přehledy;
- akce/transformace a registry;
- procesní členství a výstupní vztahy;
- COMEX stránku/komponenty;
- role, podmínky a míru ověření viditelnosti.

Navigační strom, procesní graf, settings link a action-call graf nejsou jedna vazba.

### Datový model

Neopisujte ručně úplnou FDT strukturu. Začněte generovanou referencí a kurátorujte:

- business datové objekty;
- významné vztahy;
- životní/stavové modely;
- číselníky;
- vazbu na DAD/fyzickou reprezentaci.

Podkladové datové FDT berte z explicitní klasifikace producenta nebo ověřené XDS analýzy.
Nehádejte je podle labelu. Pohledové a pseudo typy dokumentujte jako projekce/pomocné typy,
ne jako primární business entity.

### Procesy

`docs/procesy/` popisuje business nebo uživatelský průběh současného systému. Není to
mechanická kopie x-item procesu. Odkazujte na dotčené FDT, přehledy, akce a procesní uzly.

### Integrace

U integrace popište účel, systém protistrany, trigger/směr, autentizaci, datový kontrakt,
vstupní/výstupní FDT, akci/službu, chybové chování a provozní dohled. Tajné hodnoty sem
nepatří.

### Provoz

Udržujte prostředí, deployment/release tok, monitoring, joby/plánované úlohy, zálohy,
obnovu, incidentní postupy a známé provozní závislosti. Konfiguraci popisujte bez secrets.

## 4. Aktualizace po epiku

Když epic mění skutečné chování aplikace:

1. nejprve zjistěte potvrzený výsledný stav;
2. aktualizujte dotčené stránky `docs/` na nový současný obraz;
3. starý stav neponechávejte jako paralelní „verzi dokumentace“;
4. historii ponechte epiku a Gitu;
5. pokud se změnily XDS/FDT, nejprve obnovte producentem vlastněnou referenci;
6. pokud se změnil intranet/COMEX, znovu ověřte dotčené settings/registry/CXD nebo explicitně
   uveďte, že runtime projekce ještě ověřena nebyla.

## 5. Generované reference

`docs/reference/fdt/` je produkovaný balík. Neupravujte jeho Markdown ručně.

Budoucí `docs/reference/intranet/` nebo `docs/reference/comex/` zakládejte pouze tehdy,
až existuje dohodnutý producent, manifest a pravidla úplnosti. Skill je sám nevyrábí.

## 6. Validace

Spusťte:

~~~bash
python toolkit/skills/maintain-project-documentation/project_documentation.py validate .
python toolkit/skills/maintain-project-documentation/project_documentation.py inventory .
~~~

Potom spusťte validátor vlastníka Project Memory nebo běžné projektové validace.

## Bezpečnost

- Nikdy nezapisujte credentials, session, osobní produkční data ani privátní runtime payload.
- Administrátorský read účet není důkaz viditelnosti cílové uživatelské role.
- `on_comex`, XDS access metadata ani existence registrace samy nedokazují efektivní runtime.
- Generované reference nepřepisujte ručně.
- Neprovádějte automatickou změnu XDS, settings, akcí nebo COMEXu jen proto, že dokumentace
  odhalila nesoulad; to je samostatný authoring úkol.
