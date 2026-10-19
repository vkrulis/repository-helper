---
name: maintain-client-project-dimension
description: "Rozpoznává a udržuje klientský projektový kontext: helper-native implementaci nebo existující Flexideo Project Memory. Použijte pro orientaci, trasovatelnost a posouzení vlastnictví; Project Memory nezakládá ani nenahrazuje jeho MCP operace."
---

# Udržování klientského rozměru projektu

## Nejprve rozpoznejte layout

Přečtěte `project.yaml` a `.project-memory/schema-version`, pokud existují. Přítomnost
`.project-memory/` nebo Flexideo Project kontraktu znamená Project Memory či jeho neúplný
stav; samotný obecný `project.yaml` nestačí. Nejasnou nebo budoucí verzi nereorganizujte.

- **Project Memory 0.2 / Project 2 / template 2.0.0:** načtěte
  [references/project-memory.md](references/project-memory.md) a pokračujte pouze podle ní.
  Nevytvářejte `docs/project/`, mise ani druhou Current Truth; zakládá MCP a jeho šablona.
- **Project Memory 0.1:** stejná reference popisuje čtecí kompatibilitu; migrace je samostatná
  řízená operace vlastníka kontraktu.
- **Helper-native:** níže uvedený postup zůstává pro dosavadní klientské implementace.
  Žádný projekt automaticky nepřevádějte na Project Memory.

## Základní rozlišení — pouze helper-native

- `docs/project/` je kurátorovaná stopa zadání, analýzy, návrhu, potvrzení a akceptace.
- `docs/agent-context/` je aktuální technická a doménová pravda.
- `resources/` jsou převzaté nebo diagnostické vstupy s původem.
- `definitions/` je ručně spravovaný zdrojový definiční model projektu: přímo v ní projektová
  XDS a *.xcf s aplikačním nastavením, povinně s podsložkami `data/`, `temps/`, `print-temps/`
  a `site-files/`; `artifacts/` jsou odvozené výstupy.
- `.logs/` je append-only chronologie a Git fyzická historie.

Nabídky nejsou povinnou součástí klientského projektu. Pokud projekt skutečně vytváří klientské
HTML nabídky, nainstalujte samostatnou capability `client-offers` a použijte
`maintain-client-offers`; nevytvářejte její složky ani publikační pravidla dekorativně.

Přečtěte `docs/agent-context/client-project-capability.md` z helperu nebo jeho přiloženou
kopii v cílovém projektu před založením nové struktury.

## Postup

### Epiková vrstva

Založte epik pouze pro dlouhodobé ucelené podtéma. V klientském projektu jej vede mise a její
epic-id. Udržujte rozcestník `docs/project/epics/<epic-id>/README.md` s odkazy na misi, domain
context, ADR se stejným `Scope`, zdroje, artefakty, nástroje a dotčené definiční cesty.
`definitions/` zůstává jediným ručně spravovaným zdrojem pravdy; hlavní XDS, XCF ani soubory s
pevnou runtime cestou nedělte ani nekopírujte podle epiků.

1. Zjistěte, zda už existuje diagnostika, analýza, schválené zadání, zdrojový model nebo
   klientské podklady. Pokud je repozitář obsahově rozvinutý, nejprve použijte audit struktury.
2. Založte nebo aktualizujte jedno `docs/project/assignment.md`; doložená fakta a hypotézy
   viditelně odlište. Nikdy nevytvářejte druhé zadání jen proto, že formální podklad přišel později.
3. Zařaďte každý materiál podle funkce, ne podle názvu: závěr do `docs/project/analysis/`,
   současná doménová znalost do `docs/agent-context/domain/`, syrový důkaz do `resources/`.
4. Před implementací doplňte trasovatelnost požadavek → doména → zdrojový soubor →
   ověření. Odkazujte, nekopírujte.
5. U návrhů layoutů evidujte zdroj, vlastníka, revizi a datum ověření. Do repozitáře ukládejte
   jen oprávněné exporty a vysvětlení jejich vztahu k implementaci.
6. U zdrojového modelu zachovejte jednu ručně spravovanou větev. Generované výstupy nečistěte ani
   nepřepisujte bez doloženého generátoru a rozhodnuté strategie verzování.
   Založte `definitions/` vždy povinně se všemi čtyřmi podsložkami `definitions/data/`,
   `definitions/temps/`, `definitions/print-temps/` a `definitions/site-files/` — a to i tehdy,
   když projektová XDS (`definitions/<projekt>.xds`) nebo *.xcf s aplikačním nastavením
   (`definitions/<projekt>.xcf`) ještě nejsou k dispozici. V takovém případě po převodu repa na
   repo klientského projektu výslovně upozorněte uživatele, že tyto soubory je třeba dodat
   dodatečně.
7. Pro sdílené authoring nástroje použijte jejich kanonický repozitář a do projektu zapište jen
   závislost, kompatibilitu a konkrétní výsledek. Nekopírujte jejich znalost ani runtime.
8. U architektonicky významné volby použijte `maintain-decision-records`; po každé materiální
   změně použijte `maintain-work-log`.

## Bezpečnost a předání

- Neukládejte osobní, produkční ani přístupová data bez výslovného oprávnění a odpovídajícího
  technického vynucení.
- Klientské potvrzení shrňte s odkazem na zdroj; nepoužívejte repozitář jako archiv komunikace.
- Před předáním ověřte trasovatelnost, aktuálnost zadání, akceptaci a skutečně provedené validace.

## Kontrola

Spusťte projektové validace a z kořene helperu minimálně:

```text
python toolkit/agent-infrastructure/validate_skill_collection.py <cilovy-repozitar>
python toolkit/agent-infrastructure/repository_architecture.py validate <cilovy-repozitar>
python <cilovy-repozitar>/toolkit/work-log/work-log.py validate <cilovy-repozitar>
```
