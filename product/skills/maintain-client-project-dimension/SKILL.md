---
name: maintain-client-project-dimension
description: "Rozpoznává a udržuje klientský projektový kontext: helper-native implementaci nebo existující Flexideo Project Memory. Použijte pro orientaci, trasovatelnost a posouzení vlastnictví; Project Memory nezakládá ani nenahrazuje jeho MCP operace."
---

# Udržování klientského rozměru projektu

## Nejprve rozpoznejte layout

Přečtěte `project.yaml` a `.project-memory/schema-version`, pokud existují. Přítomnost
`.project-memory/` nebo Flexideo Project kontraktu znamená Project Memory či jeho neúplný
stav; samotný obecný `project.yaml` nestačí. Nejasnou nebo budoucí verzi nereorganizujte.

- **Project Memory 0.2 / Project 2 / template 2.0.0:** jde o analytickou podmnožinu
  klientského projektu. Načtěte [references/project-memory.md](references/project-memory.md),
  zachovejte jeho `project/`, `context/` a `.project-memory/`, ale klientský implementační
  obal udržujte mimo ně. Nevytvářejte `docs/project/`, mise ani druhou Current Truth.
- **Project Memory 0.1:** stejná reference popisuje čtecí kompatibilitu; migrace je samostatná
  řízená operace vlastníka kontraktu.
- **Helper-native:** níže uvedený postup zůstává pro dosavadní klientské implementace.
  Žádný projekt automaticky nepřevádějte na Project Memory.

## Společný klientský implementační obal

Oba layouty jsou klientský projekt a sdílejí neanalytické implementační oblasti:

- `definitions/` je jediný sdílený kořen zdrojových definic konkrétní aplikace;
- `resources/` jsou převzaté nebo diagnostické technické vstupy s proveniencí;
- odvozené implementační výstupy se ukládají podle kontraktu jejich producenta; kořenové
  `artifacts/` používejte jen v helper-native layoutu, protože Project Memory je rezervuje;
- `toolkit/` je jediný kořen exaktních projektových nástrojů.

Project Memory je uvnitř tohoto celku analytickou podmnožinou. Její přítomnost neruší
primární typ `client-project` ani společný `definitions/` strom. Skutečnou XDS a `*.xcf`
neodhadujte; pokud ještě chybějí, strukturu založte a chybějící zdroje výslovně hlaste.

## Analytické rozlišení

Pouze v helper-native layoutu platí:

- `docs/project/` je kurátorovaná stopa zadání, analýzy, návrhu, potvrzení a akceptace.
- `docs/agent-context/` je aktuální technická a doménová pravda.
- `definitions/` je zdrojový definiční model projektu: přímo v ní projektová
  XDS a *.xcf s aplikačním nastavením, povinně s podsložkami `data/`, `temps/`, `print-temps/`
  a `site-files/`; `artifacts/` jsou odvozené výstupy.
- `.logs/` je append-only chronologie a Git fyzická historie.

Nabídky nejsou povinnou součástí klientského projektu. Pokud projekt skutečně vytváří klientské
HTML nabídky, nainstalujte samostatnou capability `client-offers` a použijte
`maintain-client-offers`; nevytvářejte její složky ani publikační pravidla dekorativně.

Přečtěte `docs/agent-context/client-project-capability.md` z helperu nebo jeho přiloženou
kopii v cílovém projektu před založením nové struktury.

## Postup pro helper-native analytickou vrstvu

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
6. U zdrojového modelu zachovejte jednu autoritativní větev a evidujte jejího producenta.
   Generované výstupy nečistěte ani
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

### Projektové přihlašovací profily Flexideo

Pokud projekt používá Flexideo klienta, profil vybírejte přesně jako
`credentials/<DEV|TEST|CODE|PROD>/<account>.env` a předávejte přes
`--credentials-file`. Prostředí je uppercase, alias lowercase slug; role, principal
a instance jsou metadata uvnitř profilu. Jiné účty neprocházejte ani nepoužívejte
jako náhradu. Skutečné `.env` musí ignorovat Git (`/credentials/**/*.env`);
commitovat lze pouze anonymizované `.env.example` a dokumentaci.

Autoritou formátu a validace je `authoring-tools/contracts/flexideo-client-credentials.md`
z připnuté FCL sestavy. Konvence v2.2 rozlišuje `FLEXIDEO_AUTH_MODE`
(`http-basic`, `http-form`, `http-oauth`), `FLEXIDEO_SOLVE_AUTH_MODE`
(`http-basic`, `oauth-bearer`) a volitelnou `FLEXIDEO_LOGIN_URL`.
OAuth profil vyžaduje explicitní transport; existující Basic/Form profily zachovávají
výchozí Basic. Webová `/login` vynutí Basic i při OAuth defaultu, `/login/form`
formulář a `/login/oauth` OAuth; `/logon` použije serverový default.
Login URL patří ke stejnému originu/prefixu instance a neobsahuje secrets.
Její zobrazení/otevření provádí klient vrstvy D pomocí `--show-login`/`--open-login`.
Basic transport používá username/password, Bearer používá access token. Profily
automaticky nepřevádějte mezi mechanismy a neduplikujte jejich parser v helperu.

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
