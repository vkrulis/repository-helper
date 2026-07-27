# Cílová architektura agent-ready repozitáře

## Základní model

> **Znalost orientuje agenta, agent volí skill, skill řídí nástroj a nástroj provádí práci.**

Nad celým tokem stojí `AGENTS.md`, který stanoví společná pravidla prostředí.

```text
                    ┌─────────────────────┐
                    │      AGENTS.md      │
                    │ společná pravidla   │
                    └──────────┬──────────┘
                               │
                               ▼
┌─────────────────────┐    ┌──────────────────────┐
│ docs/agent-context/ │───▶│ .agents/profiles/   │
│ znalost projektu    │    │ role a odpovědnost  │
└─────────────────────┘    └──────────┬───────────┘
          │                           │ používá
          │                           ▼
          └──────────────────▶ ┌──────────────────┐
                              │ .agents/skills/  │
                              │ postup           │
                              └────────┬─────────┘
                                       │ spouští
                                       ▼
                              ┌──────────────────┐
                              │ toolkit/agent-infrastructure/   │
                              │ provedení        │
                              └──────────────────┘
```

## Normativní cílová struktura

```text
repository/
├── README.md
├── AGENTS.md
│
├── .logs/
│   ├── README.md
│   └── YYYY/MM/YYYY-MM-DD.md
│
├── docs/
│   └── agent-context/
│       ├── README.md
│       ├── architecture.md
│       ├── development-rules.md
│       ├── testing.md
│       ├── security.md
│       ├── domain/
│       └── decisions/
│
├── .agents/
│   ├── README.md
│   ├── profiles/
│   │   ├── README.md
│   │   └── <name>.agent.md
│   └── skills/
│       ├── README.md
│       ├── maintain-work-log/SKILL.md
│       └── <skill-name>/
│           ├── SKILL.md
│           ├── references/
│           └── assets/
│
├── resources/
│   ├── README.md
│   └── ... project-specific analysis inputs
│
├── toolkit/
│   ├── README.md
│   ├── agent-infrastructure/
│   ├── domain/
│   ├── development/
│   ├── work-log/
│   ├── skills/<skill-name>/
│   └── runtime/
│
└── optional platform adapter
    └── only for an explicitly selected/current platform
```

Složky mohou být prázdné jen krátkodobě během inicializace. Prázdná složka se v Gitu neuchovává, proto má obsahovat alespoň `README.md` nebo `.gitkeep`; preferován je smysluplný `README.md`.

## Význam vrstev

### `README.md`

Lidský vstupní bod. Musí rychle odpovědět:

- co repozitář obsahuje,
- pro koho je,
- jak jej spustit nebo použít,
- kde hledat podrobnosti,
- jak ověřit změnu.

README není duplicitní architektonická dokumentace. Odkazuje na ni.

### `.logs/`

Kanonická chronologická pracovní historie. Denní záznamy jsou stručné, append-only a odkazují na změněné soubory i skutečně provedené validace. Pozdější předělávka vytváří nový záznam; starý se nemaže. `.logs/` nenahrazuje aktuální znalost v `docs/agent-context/`, Git ani release changelog.

### `AGENTS.md`

Společná pravidla práce v repozitáři:

- povinnost zaznamenat každou materiální změnu do `.logs/YYYY/MM/YYYY-MM-DD.md`,

- zdroje pravdy,
- povinný pracovní tok,
- build/test/validation příkazy,
- zakázané nebo rizikové operace,
- definice hotovo,
- pravidla dokumentace.

Má být stručný a závazný. Detailní vysvětlení patří do `docs/agent-context/`.

### `docs/agent-context/`

Autoritativní znalost projektu:

- architektura a komponenty,
- doménové pojmy,
- technická omezení,
- konvence,
- rozhodnutí a jejich důvody v `decisions/`; jejich vznik nebo změna stavu se odkazuje z `.logs/`,
- testovací strategie,
- zdroje pravdy.

Obsah má být užitečný lidem i agentům. Nejde o skrytou konfiguraci konkrétního AI klienta.

### `.agents/profiles/`

Kanonické platformně neutrální definice pracovníků:

- role a odpovědnost,
- kdy profil použít,
- požadovaný kontext,
- dostupné skills,
- logické schopnosti,
- omezení,
- očekávaný výstup.

Tato cesta je vědomá projektová konvence. Platformní adaptéry se z profilů generují pouze na přání pro zvolenou platformu.

### `.agents/skills/`

Opakovatelné postupy ve formátu Agent Skills. Každý skill je samostatná složka s povinným `SKILL.md`.

Skill má:

- jednu jasně vymezenou práci,
- explicitní vstupy a výstupy,
- rozhodovací body,
- bezpečnostní omezení,
- validační postup,
- odkazy na reference pouze tehdy, kdy je má agent číst.

### `toolkit/`

Jediný kořen všech exaktních a spustitelných nástrojů. Patří sem skripty, validátory, generátory, CLI wrappery, spustitelné balíčky i jejich podpůrné soubory. Nástroje nesmějí být rozptýlené v `.agents/`, kořenovém `tools/`, kořenovém `scripts/` ani ve `scripts/` uvnitř skillu.

Doporučené členění:

- `toolkit/agent-infrastructure/` – správa agentní infrastruktury;
- `toolkit/domain/` – doménové nástroje projektu;
- `toolkit/development/` – build, test a vývojová automatizace;
- `toolkit/skills/<skill-name>/` – nástroj používaný pouze jedním skillem;
- `toolkit/runtime/` – generované nebo dodané spustitelné artefakty.

Pokud má existující projekt již kořenový `toolkit/`, použije se beze změny kořene a jednotlivé významy se oddělí vhodnými podsložkami.

#### `toolkit/agent-infrastructure/`

Deterministické nástroje určené výhradně ke správě agentní infrastruktury a použitelné bez AI:

- validátory,
- generátory,
- validátory profilů a skills,
- synchronizační skripty,
- generátory platformních konektorů,
- pomocníci pro migraci agentní architektury,
- příkazy pro CI.

### `resources/`

Doporučené projektové úložiště vstupů, které lidé, agenti nebo nástroje čtou, prohledávají či analyzují, ale které nejsou běhovou logikou repozitáře. Typicky jde o:

- XML, JSON, CSV a jiné datové korpusy,
- schémata, protokoly a strojově čitelné definice,
- snapshoty dokumentace nebo exporty,
- vzorky a referenční artefakty,
- cizí nebo historický zdrojový kód určený k analýze, nikoli k sestavení jako hlavní aplikace.

Nový repozitář má `resources/README.md` založit rovnou. Pro existující repozitář je složka volitelná: vytvářejte ji jen když pro ni existuje skutečný nebo očekávaný účel.

V `resources/README.md` uveďte původ, licenci, aktualizační postup, formáty, autoritativnost a případná omezení velikosti či citlivosti. Neukládejte sem secrets ani produkční osobní data.

Nezaměňujte vrstvy:

- běhový a sestavovaný kód patří do standardní projektové cesty, typicky `src/`;
- projektové analyzované vstupy patří do kořenového `resources/`;
- podklady svázané pouze s jedním přenositelným skillem patří do `.agents/skills/<skill>/references/` nebo `assets/`;
- testovací fixture patří do konvence daného testovacího frameworku, pokud nemá širší analytické použití.

### Platformní adaptéry

Platformní adaptér je volitelný. Nevytvářejte automaticky adaptéry pro všechny podporované platformy. Pokud uživatel platformu neurčí, použijte Codex pouze tehdy, když aktuální pracovní prostředí je Codex; v jiném nebo neznámém prostředí se zeptejte, zda chce Codex, jinou platformu, nebo žádný adaptér.

Adaptéry obsahují pouze:

- nativní vstupní instrukční soubory,
- převod kanonických profilů,
- zpřístupnění kanonických skills,
- platformní sandbox, oprávnění, hooks nebo MCP konfiguraci.

Nesmějí se stát druhým zdrojem projektových znalostí.

### Přenositelnost dokumentovaných příkazů

Příkazy v `README.md`, `AGENTS.md`, skills a projektové dokumentaci musí být přenositelné mezi pracovními stanicemi:

- uveďte pracovní adresář, ze kterého se příkaz spouští;
- pro soubory ve stejném repozitáři používejte cesty relativní ke kořeni repozitáře;
- pro nástroje v dohodnutém sourozeneckém repozitáři používejte relativní sourozeneckou cestu;
- nevkládejte strojově nebo uživatelsky specifické absolutní cesty, pokud je nevyžaduje externí runtime;
- nezbytnou absolutní cestu pojmenujte jako konfigurovatelný vstup a její důvod zdokumentujte.

Relativní cesta nesmí skrývat nejasný předpoklad o rozložení workspace. Pokud příkaz závisí na sourozeneckém repozitáři, dokumentace musí očekávané rozložení výslovně uvést.

## Autoritativní versus odvozené soubory

### Ručně editované zdroje pravdy

```text
README.md
AGENTS.md
docs/agent-context/
.agents/profiles/
.agents/skills/
toolkit/
```

### Typicky odvozené soubory

```text
.codex/agents/*.toml
.claude/agents/*.md
.claude/skills/*
.github/agents/*.agent.md
.github/copilot-instructions.md
CLAUDE.md
GEMINI.md
```

Platformní konfigurace obsahující skutečná nastavení může být ručně spravovaná, ale musí být zřetelně oddělena od generovaného obsahu.

## Rozhodovací pravidla

### Znalost nebo pravidlo?

- Popisuje to, **jak projekt funguje** → `docs/agent-context/`.
- Stanoví to, **jak se má v repozitáři pracovat** → `AGENTS.md`.

### Profil nebo skill?

- Potřebujete jinou roli, kontext, odpovědnost nebo oprávnění → profil agenta.
- Potřebujete opakovatelný postup, který může využít více rolí → skill.

### Skill nebo tool?

- Je potřeba úsudek, pořadí kroků a práce s kontextem → skill.
- Je potřeba přesná opakovatelná operace pro správu agentní vrstvy → `toolkit/agent-infrastructure/`.
- Je potřeba přesná doménová operace projektu → `toolkit/domain/`.
- Je potřeba build, test nebo vývojová automatizace → `toolkit/development/`.
- Je potřeba nástroj pouze pro jeden skill → `toolkit/skills/<skill-name>/`.

## Povolené odchylky

Cílová struktura není samoúčelná. Odchylka je přípustná, pokud:

1. má jasný důvod,
2. je popsána v `docs/agent-context/decisions/`,
3. nevytváří duplicitní zdroj pravdy,
4. platformní konektor zůstává tenký,
5. validační nástroj ji umí rozpoznat nebo ignorovat záměrně.
