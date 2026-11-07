# Mise (dlouhodobé cíle repozitáře)

## Účel a hranice

Tato capability dává repozitáři místo pro **návrh** střednědobých a dlouhodobých cílů, dřív než se rozhodne, jak přesně je realizovat. Hodí se, když práce narazí na něco velkého nebo nejasného — cíl, který nejde bezpečně provést jako jednu materiální změnu a zalogovat, ale zároveň o něm ještě neexistuje architektonické rozhodnutí.

Mise **není** ADR (rozhodnutí), pracovní log (historie) ani doménová znalost (aktuální pravda o kódu). Je to podklad k projití s uživatelem: cíl, proč na něm záleží, co už víme, a navrhovaný přístup — dokud se s uživatelem nesladí, nejde o závaznou informaci.

## Doporučený strom

```text
repository/
└── docs/
    └── missions/
        ├── README.md
        ├── 00-<sdileny-kontext>.md   (volitelné, viz níže)
        ├── 01-<mise>.md
        └── NN-<mise>.md
```

| Cesta | Obsah a pravidlo |
|---|---|
| `docs/missions/README.md` | Index: vztah k ostatním zdrojům pravdy, pracovní postup, tabulka aktuálních misí se stavem a prioritou. Udržuje se ručně. |
| `docs/missions/NN-<slug>.md` | Jedna mise = jeden dokument, formát dle `mission-template.md`. Číslo je dvoumístné, monotónní a znovu se nepoužívá. |
| `docs/missions/00-*.md` (volitelné) | Sdílený kontext využívaný více misemi (např. ověřený doménový model, na který se mise odkazují), aby se nedublovat napříč jednotlivými misemi. Nemusí mít formát jednotlivé mise, ale sdílí stejnou číselnou řadu. |

## Standardizovaný formát mise

```markdown
# Mise: <stručný název cíle>

- Stav: draft
- Priorita: TODO
- ADR: —

## Cíl
## Proč
## Co už víme
## Navrhovaný přístup
## Závislosti
## Otevřené otázky
## Definice hotovo (návrh)
```

Šablona: `.agents/skills/maintain-missions/references/mission-template.md`.

### Stav

Pevná sada hodnot pole `Stav` (mirror stylu `Stav` u ADR):

| Stav | Význam |
|---|---|
| `draft` | Nově založená mise, ještě neprošla revizí s uživatelem. |
| `reviewed` | Revize s uživatelem proběhla, směr je potvrzen. |
| `in-progress` | Realizace běží; pokud vzniklo architektonické rozhodnutí, pole `ADR:` na něj odkazuje. |
| `done` | Cíl mise byl naplněn. |
| `deferred` | Odloženo — zůstává platným budoucím kandidátem, ne zamítnuto. |
| `rejected` | Zamítnuto po revizi s uživatelem. |

Stavovou změnu zapisujte úpravou pole `Stav` (a případně `ADR`), ne přepisem `Cíl`/`Proč`. Zásadní změnu směru zachyťte novou misí a obě vzájemně odkažte.

## Kdy misi založit

Použijte skill `maintain-missions` a jeho rozhodovací bránu (čtyři otázky o přesahu za jednu změnu, nesladěném rozsahu, pravděpodobnosti ADR a strategickém významu). Agent má misi aktivně navrhnout uživateli, jakmile v průběhu práce takový cíl rozpozná — nečekat, až o to uživatel výslovně požádá.

## Životní cyklus

1. Založte misi se `Stav: draft`, jakmile rozhodovací brána skillu vyjde kladně.
2. Projděte misi s uživatelem; po potvrzení směru přepněte na `reviewed`.
3. Je-li součástí architektonicky významné rozhodnutí, aktivujte `maintain-decision-records`; vzniklý ADR zapište do pole `ADR:` mise a stav přepněte na `in-progress`.
4. Realizaci provádějte a logujte standardně (`maintain-work-log`); po dokončení nastavte `done`.
5. Pokud se v realizaci nepokračuje, nastavte `deferred` (dočasně) nebo `rejected` (trvale), s krátkým důvodem v textu mise.
6. Po každé stavové změně aktualizujte tabulku v `docs/missions/README.md` a zapište záznam do `.logs/`.

## Instalace a udržování

Nejprve založte základní strukturu helperem. Potom z kořene helperu spusťte:

```bash
python toolkit/agent-infrastructure/repository_architecture.py install-capability <cilovy-repozitar> --name missions
```

Příkaz nepřepisuje existující soubory. Před `--force` zkontrolujte lokální změny; aktualizuje pouze soubory capability, nikdy obsah existujících misí.

Agent má při založení nebo materiální změně mise použít skill `maintain-missions`, nikoli vytvářet ad-hoc dokumenty podle vlastního uvážení formátu.

## Kontrola

## Epiky v klientském projektu

Tato konvence platí pouze pro helper-native layout. Flexideo Project Memory používá
vlastní `project/epics/EPIC-NNNN/` a `project/visions/` přes sémantické MCP operace;
nevytvářejte souběžné `docs/missions/` pro stejné cíle.

V helper-native klientském projektu představuje jedna mise jeden epik. Název souboru má tvar
`NN-<epic-id>.md` a povinné metadata jsou `Epic`, `Stav`, `Priorita` a `ADR`. Ke každému epiku
založte rozcestník `docs/project/epics/<epic-id>/README.md`; obsah specifický pro epik patří do
`resources/epics/<epic-id>/`, `artifacts/epics/<epic-id>/` nebo `toolkit/epics/<epic-id>/`.
Společný obsah zůstává v projektových kořenech.

Z kořene helperu spusťte:

```bash
python toolkit/agent-infrastructure/validate_skill_collection.py <cilovy-repozitar>
python toolkit/agent-infrastructure/repository_architecture.py validate <cilovy-repozitar>
python <cilovy-repozitar>/toolkit/work-log/work-log.py validate <cilovy-repozitar>
```

Validátor architektury ověří přítomnost `docs/missions/README.md`, skillu, zmínku v `AGENTS.md`, jedinečnost čísel a u souborů s hlavičkou `# Mise:` platnost pole `Stav` a existenci souboru odkazovaného v poli `ADR:`. Nemůže posoudit, zda je obsah mise věcně správný nebo zda revize s uživatelem skutečně proběhla.
