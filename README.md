# Repository Skills

Přenositelná sada Agent Skills pro zakládání, audit, citlivou reorganizaci a dlouhodobou údržbu repozitářů připravených pro práci lidí i AI agentů.

Balíček vychází z principů:

> **Jedno místo pravdy + volitelný tenký konektor pro zvolenou platformu.**
>
> **Znalost orientuje agenta, agent volí skill, skill řídí nástroj a nástroj provádí práci.**

Repository-helper rozlišuje čtyři primární typy repozitářů: `development`, `authoring`,
`client-project` a `documentation`. Authoring dále rozlišuje specializovanou roli a
nadřazený orchestrátor; referenčním orchestrátorem Flexideo je `Flexideo-orchestrator`.
Autoritativní pravidla jsou v `docs/agent-context/repository-types.md`.

U klientských projektů rozlišuje dosavadní helper-native layout a existující Flexideo
Project Memory. Tu zakládá MCP s verzovanou šablonou; helper poskytuje orientaci a
respektuje její epiky, Current Truth a vlastnictví oblastí. Rozsah, instalaci čtecího
skillu a vyhodnocení integračních návrhů popisuje
[kompatibilita s Project Memory](docs/agent-context/client-project-memory-compatibility.md).
Pro aktuální dokumentaci aplikace lze do Project Memory bezpečně instalovat také
`project-documentation`; tato capability nepřidává druhý analytický strom a nemění MCP
stavy ani provisioning.

## Co sada obsahuje

| Skill | Účel |
|---|---|
| `initialize-agent-ready-repository` | Založí nový repozitář podle společné platformně nezávislé struktury. |
| `audit-repository-structure` | Zmapuje stávající repozitář bez změn a navrhne cílové zařazení obsahu. |
| `migrate-repository-structure` | Po schválení plánu citlivě převede existující repozitář do cílové struktury. |
| `add-platform-connector` | Na přání přidá jeden tenký konektor pro Codex, Claude Code, Gemini CLI nebo GitHub Copilot. |
| `validate-repository-architecture` | Ověří strukturu, zdroje pravdy, skills, profily a platformní adaptéry. |
| `maintain-work-log` | Vytváří a prohledává povinnou chronologickou historii materiálních změn. |
| `import-legacy-work-logs` | Převádí historická podtémata do jednotného logu bez ztráty originálu a bez domýšlení faktů. |
| `maintain-decision-records` | Konzervativně spravuje ADR a propojuje je s pracovním logem. |
| `maintain-domain-inventories` | Udržuje regenerovatelné mapy aktuálního stavu kódu v `docs/agent-context/domain/`. |
| `maintain-documentation-sync` | Synchronizuje doménovou dokumentaci s obecnou Docusaurus dokumentací a eviduje revize. |
| `maintain-development-testing` | Zavádí bezpečný, vrstvený a frameworkově neutrální základ testování a diagnostiky. |
| `manage-product-repository` | Zavádí bezpečnou hranici a volitelnou synchronizaci `product/` do Product repository. |
| `maintain-authoring-repository` | Zakládá a udržuje specializovaný nebo orchestrační authoring repository s autoritativním produktem v `product/`. |
| `maintain-client-project-dimension` | Rozpoznává helper-native klientský projekt nebo Project Memory a udržuje kontext podle vlastnictví jejich oblastí. |
| `maintain-client-offers` | Volitelně zakládá a udržuje dohledatelné klientské HTML nabídky včetně validace a preview. |
| `maintain-project-documentation` | Udržuje aktuální dokumentaci klientské aplikace, odděluje ji od epiků a propojuje XDS/FDT/DAD, intranet a COMEX. |

## Cílová struktura repozitáře

```text
repository/
├── README.md
├── AGENTS.md
├── .logs/YYYY/MM/YYYY-MM-DD.md
├── docs/
│   └── agent-context/
├── .agents/
│   ├── profiles/
│   └── skills/
├── resources/
├── toolkit/                 # all exact and executable tools
└── optional adapter for the selected platform
```

Význam jednotlivých vrstev:

- `README.md` – základní orientace pro člověka.
- `AGENTS.md` – společná pravidla práce v repozitáři.
- `.logs/` – kanonická chronologická pracovní historie; aktuální stav patří do `docs/agent-context/` a fyzická historie do Gitu.
- `docs/agent-context/` – autoritativní znalosti o projektu.
- `.agents/profiles/` – kanonické, platformně neutrální definice konkrétních pracovníků.
- `.agents/skills/` – přenositelné opakovatelné postupy ve formátu Agent Skills.
- `toolkit/` – jediný kořen všech exaktních nástrojů; `agent-infrastructure/`, `domain/`, `development/`, `skills/` a `runtime/` oddělují odpovědnosti.
- `resources/` – projektové vstupy pro vyhledávání a analýzu, například data, XML, schémata, snapshoty nebo cizí zdrojový kód.
- `.codex/`, `.claude/`, `.gemini/`, `.github/` – volitelný tenký konektor pouze pro výslovně zvolenou platformu a její vynucení oprávnění.

## Použití

### Repo-scoped použití

Zkopírujte vybrané skills do cílového repozitáře:

```text
TARGET_REPO/.agents/skills/
```

Codex a Gemini CLI tuto cestu načítají přímo. Pro Claude Code lze konektor vytvořit pomocí skillu `add-platform-connector`.

### Uživatelské použití

Celou sadu lze umístit do:

```text
~/.agents/skills/
```

nebo jednotlivé skills nainstalovat podle možností konkrétního klienta.

### Doporučený pracovní tok pro nový repozitář

1. Aktivujte `initialize-agent-ready-repository`.
2. Doplňte skutečné údaje do `README.md`, `AGENTS.md` a `docs/agent-context/`.
3. Popište vstupní zdroje v `resources/README.md`; pokud projekt žádné nemá, ponechte zde účel a pravidla pro jejich budoucí přidání.
4. Přidejte kanonické profily a projektové skills.
5. Přidejte konektor jen tehdy, když je požadován. Při práci v Codexu lze bez jiné preference použít Codex; v neznámém prostředí se zeptejte a nabídněte i variantu bez konektoru.
6. Spusťte `validate-repository-architecture`.

### Doporučený pracovní tok pro existující repozitář

1. Aktivujte `audit-repository-structure`.
2. Projděte migrační mapu a otevřené otázky.
3. Potvrďte nejednoznačné nebo rizikové přesuny.
4. Aktivujte `migrate-repository-structure`.
5. Přidejte pouze požadovaný platformní konektor, případně žádný.
6. Aktivujte `validate-repository-architecture` a spusťte projektové testy.

## Nástroje

Balíček obsahuje pomocné skripty v `toolkit/agent-infrastructure/`:

```bash
python toolkit/agent-infrastructure/repository_architecture.py audit /path/to/repository
python toolkit/agent-infrastructure/repository_architecture.py init /path/to/new-repository --name "Project Name"
python toolkit/agent-infrastructure/repository_architecture.py validate /path/to/repository
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name work-log
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name decision-records
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name domain-inventories
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name client-project
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name project-documentation
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name client-offers
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name documentation-sync
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name development-testing
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name product-repository
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name authoring-repository
# aktualizace již instalované capability po kontrole lokálních změn:
python toolkit/agent-infrastructure/repository_architecture.py install-capability /path/to/repository --name domain-inventories --force
python toolkit/agent-infrastructure/render_platform_connectors.py /path/to/repository --platform codex
python toolkit/agent-infrastructure/validate_skill_collection.py .
python toolkit/work-log/work-log.py validate .
```

Pokud cílový repozitář už obsahuje `.claude/skills/`, instalace capability
automaticky udržuje označenou Claude kopii synchronní s `.agents/skills/`.
Ručně upravené neoznačené kopie se nepřepisují.

Nástroje neřeší doménová rozhodnutí za uživatele. Automatizují pouze bezpečné a deterministické části práce.

## Platformní scénáře

Konektor je volitelný a vytváří se pouze pro zvolenou platformu. Pokud není preference uvedena a práce probíhá v Codexu, lze použít Codex. V jiném nebo neznámém prostředí je nutné se zeptat; platnou odpovědí je i žádný konektor. Nikdy se bez požadavku nevytvářejí konektory pro více platforem.

Codex konektor doplňuje zejména `.codex/config.toml` a případné profily v `.codex/agents/`. Samotné `AGENTS.md` a `.agents/skills/` často postačují, takže ani v Codexu není nutné vytvářet prázdnou či nepotřebnou konfiguraci.

Další podporované scénáře:

- Claude Code: `CLAUDE.md`, `.claude/agents/` a zpřístupnění kanonických skills v `.claude/skills/`.
- Gemini CLI: `GEMINI.md`, volitelná `.gemini/settings.json`; `.agents/skills/` je podporovaná interoperabilní cesta.
- GitHub Copilot: `.github/copilot-instructions.md` a `.github/agents/*.agent.md`.

Podrobnosti jsou v `docs/agent-context/platform-connector-scenarios.md`.

## Důležité zásady

- Starý soubor se nepřesouvá jen podle názvu; nejprve se určí jeho skutečná funkce.
- Migrační skill musí zachovat historii pomocí `git mv`, kdykoli je to praktické.
- Generované adaptéry se neupravují ručně.
- Citlivé hodnoty, tokeny a lokální osobní konfigurace se necommitují.
- Textová instrukce není bezpečnostní hranice; práva musí vynucovat platforma, sandbox, operační systém nebo CI.
- `docs/agent-context/` je dokumentace projektu, ne skladiště promptů.
- Všechny nástroje pod `toolkit/` musí být použitelné bez AI; `.agents/` nesmí obsahovat spustitelné nástroje.

## Stav konvencí

Platformní formáty se vyvíjejí. Scénáře v tomto balíčku byly ověřeny k **2026-07-21**. Před změnou generátorů zkontrolujte aktuální oficiální dokumentaci příslušné platformy.
