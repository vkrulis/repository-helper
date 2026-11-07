# Politika bezpečné reorganizace existujícího repozitáře

## Cíl

Dosáhnout čisté cílové struktury bez ztráty významu, historie, funkčnosti nebo důvěryhodnosti dokumentace.

Radikální změna struktury je přípustná, ale pouze po prokazatelném pochopení stávajícího uspořádání.

## Povinné fáze

### 1. Inventura bez změn

Nejprve zmapujte:

- kořenové soubory a adresáře,
- stávající instrukční soubory (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions),
- skills, commands, prompts, agents a hooks,
- dokumentaci a její odkazy,
- build, test a deployment nástroje,
- generované soubory,
- CI/CD konfiguraci,
- symlinky a submoduly,
- tajné nebo lokální soubory,
- soubory ignorované Gitem,
- místa, která fungují jako faktický zdroj pravdy.

Během inventury nic nepřesouvejte.

### 2. Sémantická klasifikace

Každý relevantní soubor klasifikujte podle skutečného účelu, nikoli podle názvu:

- lidská orientace,
- společné pracovní pravidlo,
- projektová znalost,
- projektový zdroj k analýze,
- agentní profil,
- skill,
- nástroj agentní infrastruktury,
- doménový nebo vývojový nástroj projektu,
- platformní adaptér,
- platformní vynucení oprávnění,
- aplikační zdrojový kód,
- provozní nebo deployment konfigurace,
- generovaný obsah,
- archivní nebo zastaralý obsah.

### 3. Migrační mapa

Pro každý přesun evidujte:

| Zdroj | Cíl | Akce | Důvod | Riziko | Odkazy k opravě | Potvrzení |
|---|---|---|---|---|---|---|

Přípustné akce:

- `keep` – ponechat,
- `move` – přesunout,
- `merge` – sloučit do autoritativního souboru,
- `split` – rozdělit podle významu,
- `generate-adapter` – převést na odvozený konektor,
- `archive` – zachovat mimo aktivní strukturu,
- `remove` – odstranit až po výslovném potvrzení.

### 4. Řešení nejasností

Agent se má doptat pouze na rozhodnutí, která mohou významně změnit význam nebo provoz projektu, například:

- který ze dvou dokumentů je autoritativní,
- zda je platformní soubor ručně spravovaný nebo generovaný,
- zda je historický adresář stále používán,
- zda lze změnit veřejné cesty nebo importy,
- zda se mají přesouvat CI/deployment soubory,
- zda je možné přejmenovat externě odkazovaný soubor.

Otázky seskupte do krátkého rozhodovacího balíčku. Neptejte se na věci, které lze bezpečně zjistit z repozitáře.

### 5. Provedení po menších celcích

Doporučené pořadí:

1. přidat cílové adresáře a jejich README,
2. vytvořit nebo konsolidovat `AGENTS.md`,
3. přesunout kontextovou dokumentaci,
4. konsolidovat kanonické skills,
5. vytvořit kanonické profily,
6. konsolidovat všechny exaktní nástroje pod jediný kořen `toolkit/`: agentní infrastrukturu do `toolkit/agent-infrastructure/`, doménové nástroje do `toolkit/domain/`, vývojovou automatizaci do `toolkit/development/`, nástroje jediného skillu do `toolkit/skills/<skill-name>/` a spustitelné artefakty do `toolkit/runtime/`; existující význam kořenového `toolkit/` zachovat vhodnými podsložkami,
7. nainstalovat schopnosti `work-log` a `decision-records` pomocí `repository_architecture.py install-capability`, doplnit jejich pravidla do `AGENTS.md` a zachovat případné starší pracovní poznámky i ADR bez ztráty obsahu,
8. konsolidovat analyzované vstupy do `resources/` bez přesunu běhového kódu nebo testovacích fixtures jen podle názvu,
9. vytvořit pouze výslovně požadovaný platformní adaptér; v Codexu lze bez jiné preference zvolit Codex, v neznámém prostředí se nejprve zeptat,
10. opravit interní odkazy a skripty,
11. aktualizovat hlavní README,
12. spustit validace a projektové testy.

Používejte `git mv`, kdykoli je to praktické. Git historii rozpoznává heuristicky, ale explicitní přesuny zlepšují čitelnost změny.

### 6. Validace

Povinně ověřte:

- strukturu repozitáře,
- validitu všech skills a profilů,
- existenci všech odkazovaných souborů,
- synchronizaci všech požadovaných adaptérů,
- funkčnost build/test/CI příkazů,
- absenci nechtěných secrets,
- stav `git diff --stat` a `git status`,
- zda nebyly omylem přesunuty aplikační moduly.

## Stop podmínky

Migraci přerušte a vyžádejte rozhodnutí, pokud:

- hrozí ztráta dat nebo historie,
- není jasný zdroj pravdy,
- změna zasahuje veřejná API, importní cesty nebo deployment,
- testy nelze spustit a změna je široká,
- repozitář obsahuje necommitnuté změny, které se překrývají s migrací,
- nelze rozlišit generovaný a ručně spravovaný obsah,
- platformní konfigurace obsahuje credentials nebo osobní údaje.

## Zakázané zkratky

- Přesun podle názvu bez přečtení obsahu.
- Sloučení instrukčních souborů bez posouzení precedence.
- Kopírování stejné znalosti do `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` a Copilot instructions.
- Automatické mazání „duplicit“ bez potvrzení jejich zastaralosti.
- Přepis historie pomocí force push jako součást běžné reorganizace.
- Vytvoření platformního konektoru, který obsahuje plnou kopii projektu místo odkazu nebo generované tenké vrstvy.

## Požadovaný výsledek

Výsledný repozitář musí být:

- srozumitelný člověku z hlavního README,
- srozumitelný agentovi z `AGENTS.md` a kontextu,
- přenositelný mezi platformami,
- bez dvojích zdrojů pravdy,
- validovatelný automaticky,
- čistý v `git status`,
- funkčně ekvivalentní nebo s přesně popsanými záměrnými změnami.
