# Orientace v existující Project Memory

Ověřeno proti lokálnímu kontraktu Orchestrátoru a ADR-0065 dne 2026-10-19.
Tato reference je čtecí interpretační pomůcka, nikoli šablona, schéma ani oprávnění k zápisu.
Autoritu drží `Flexideo-orchestrator/docs/agent-context/domain/project-memory-repository-contract.md`,
`product/contracts/project-v2.schema.json`, `project-memory-v0.2.schema.json` a odpovídající MCP.
Ve workspace používejte relativní sourozeneckou cestu `../Flexideo-orchestrator`.

## Rozpoznání a čtení

1. Ověřte `project.yaml`, `.project-memory/schema-version` a verzi šablony. Aktuální kombinace
   je Project 2 / Memory 0.2 / template 2.0.0. Heuristické rozpoznání helperem nedokazuje validitu.
2. Přečtěte sdílený `context/application-context.md`. Pro konkrétní změnu zvolte
   `project/epics/EPIC-NNNN/` a čtěte jeho baseline a `analysis/state.yaml` před další historií.
3. `.project-memory/epics.json` je serverový registr revize, current_epic a active_epic.
   Čtení epiku jej neaktivuje; filtr stránky není zapisovací scope. Registr ani idempotency
   markery ručně neopravujte.
4. Rozlišujte potvrzená fakta, hypotézy, inference, rozhodnutí a otevřené otázky. Historické
   potvrzení jiného epiku nepotvrzuje nový příběh. Ukončení analýzy nedokazuje realizaci.

## Mapa autorit

| Oblast | Význam a hranice |
| --- | --- |
| `project.yaml` | Identita jedné aplikace/projektu a lifecycle; repository binding a granty vlastní D1. |
| `context/` | Sdílená potvrzená Current Truth aplikace; promotion je řízená operace. |
| `project/epics/EPIC-NNNN/` | Lokální baseline, analysis, evidence, decisions (`DEC-*`), questions, reviews, sessions, checkpoints, architecture a artifacts/milestones. |
| `project/visions/` | Budoucí záměry; nejsou potvrzené požadavky ani Current Truth. |
| `application/` | Sdílená aplikační oblast; konkrétní evidence instancí a technických vazeb vyžaduje kontrakt producenta. Git údaj sám nedokazuje živý stav. |
| `definitions/` | Sdílené zdrojové definice; vlastnictví ručního zdroje a výstupu Replicatoru zjistěte u producenta. Neklonovat podle epiků. |
| `docs/` | Sdílená dokumentace aplikace. Není náhradním řízením analýzy. |
| `imports/` | Připnuté importy s proveniencí, např. schválený offer release; nejde o živou nabídku. |
| `.project-memory/` | Pouze serverová metadata a obnovitelné indexy, žádná druhá business pravda. |
| `.logs/` | Append-only pracovní chronologie, odlišná od Session, Checkpoint a Milestone. |
| `.agents/`, `toolkit/`, `AGENTS.md` | Provozní capability a pravidla šablony/správce, nikoli analytická paměť. |

Sdílený kód a regresní scénáře zachovávají své projektové cesty. Povolená oblast nemusí
být materializována; absence prázdné složky není chyba. Nevynucujte XDS/XCF ani čtyři
podsložky definitions u projektu, který teprve prochází analýzou.

## Zápisy a údržba

Project Memory vytváří MCP s verzovanou šablonou. Použijte odpovídající sémantickou MCP
operaci pro evidence, rozhodnutí, otázky, kontext, checkpoint a promotion. Pokud není
zapisující nástroj dostupný, připravte podnět s identitou epiku a zdrojem; nevytvářejte
náhradní `docs/project/assignment.md`, `docs/missions/` nebo obecný soubor místo operace.

`DEC-*` v analytické paměti a aplikační technické ADR jsou různé objekty. Nekopírujte
rozhodnutí do helperového globálního ADR registru a nepřidělujte mu číslo této řady.
Umístění sdílených technických ADR se řídí kontraktem projektu; `docs/architecture/decisions/`
je návrh konvence, nikoli povinný požadavek Memory 0.2.

Průvodce řídí analytické poznání; Replicator pracuje s technickými definicemi a výsledky;
Implementátor propojuje zadání s realizací. Čtení jedním nástrojem nezakládá právo měnit
oblast jiného. Replikace nepotvrzuje business akceptaci ani baseline.

MCP mutace už zapisuje denní log ve stejném commitu. Nedublujte ji ručním záznamem;
`maintain-work-log` použijte pro materiální práci mimo MCP. Historický log nebo milestone
nepovyšujte na aktuální stav. Runtime Execution Graph patří Work Control Plane.

## Generovaná reference a externí technický stav — návrh integrace

Konvence `docs/reference/` je návrhem pro **celý** balík Replicatoru:
`index.md`, `manifest.json`, `fdt/<typ>.md`, `fdt/index.md`,
`indexes/fdt/segments.jsonl` a `indexes/fdt/by-xds-id.json`. Jde o navrženou publikaci
v Project Memory, nikoli nově implementovaný publikační kontrakt helperu.

Při čtení existující sady ověřte producenta, úplnost a otisky podle jeho hashovací konvence,
identitu aplikace, roli, instanci/referenční zdroj, verzi a čas. Neznámé metadata označte jako
neověřené; nedoplňujte je odhadem. Markdown jednoho typu bez manifestu/indexů není kompletní
sada. Dokumentace sestaveného modelu není autorské XDS ani důkaz nasazení na PROD.

Generátor vlastní jen svůj vymezený podstrom a publikuje konzistentní sadu. Ruční architekturu
a business vysvětlení udržujte mimo něj. U `application/application.yaml`, `instances/`
a `snapshots/` nejprve ověřte schválený kontrakt; zde jsou pouze navrženým členěním.

Remote Version Store vlastní publikované historické verze, živá instance provozní stav.
Project Memory uchovává kontext a připnuté reference, nikoli jejich náhradní databázi.
Dynamický SQLite index zůstává externím obnovitelným indexem/read-only snapshotem; nezakládejte
jej jako povinný Git soubor. Spojení projekt → aplikace → instance → verze/snapshot/commit
musí být doložené, ne odvozené ze stejného názvu nebo posledního DEV buildu.

## Kompatibilita a validace

Memory 0.1 má analytické oblasti v kořeni (`baseline/`, `analysis/`, `evidence/`,
`decisions/` atd.). Jsou čitelné; neposouvejte je automaticky do prvního epiku.
Migrace vyžaduje reviewed manifest, přesný head a blob SHA. Helper-native slug epiku
není automaticky `EPIC-NNNN` a mise není jeho alternativní analytický stav.

`repository_architecture.py audit` poskytuje mechanickou mapu.
`repository_architecture.py validate` kontroluje u Memory pouze orientační vstupy,
výslovně ne sémantickou validitu. Tu ověřte odpovídajícím MCP nebo matching nástrojem
`product/tools/project-memory/project_memory_repository.py validate <repository>`
z Orchestrátoru; neinstalujte jeho kopii do projektu. Jeho případná omezení vůči
návrhům `docs/`/`definitions/` hlaste vlastníkovi, neobcházejte přesunem souborů.
