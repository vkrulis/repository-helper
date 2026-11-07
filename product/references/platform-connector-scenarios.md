# Tenké platformní konektory

Ověřeno k: **2026-07-21**

## Společné zásady

Platformní konektor:

1. odkazuje na `AGENTS.md` nebo jej zpřístupní nativním mechanismem,
2. zpřístupní kanonické skills z `.agents/skills/`,
3. převede vybrané profily z `.agents/profiles/`,
4. obsahuje pouze platformně specifické nastavení,
5. nevytváří druhý zdroj projektové znalosti,
6. označuje generované soubory,
7. neobsahuje secrets ani osobní konfiguraci.

Konektory jsou volitelné a vznikají pouze pro vybranou platformu. Pokud uživatel platformu neurčí:

1. v aktuálním prostředí Codex použijte Codex;
2. v jiném jednoznačně rozpoznaném prostředí nabídněte odpovídající platformu a potvrďte ji;
3. v neznámém prostředí se zeptejte;
4. vždy připusťte variantu bez konektoru.

Nikdy nevytvářejte sadu konektorů pro více platforem bez výslovného požadavku.

## Scénář: Codex

### Nativně použitelné společné vrstvy

- `AGENTS.md` je nativní instrukční soubor.
- `.agents/skills/` je nativní projektová cesta pro skills.

### Přidané soubory

```text
.codex/
├── config.toml
└── agents/
    └── <profile>.toml
```

### Pravidla

- `.codex/config.toml` obsahuje pouze projektové Codex nastavení.
- Nastavení modelu nevkládejte bez výslovného požadavku; model se mění rychleji než architektura repozitáře.
- Sandbox a approval policy vybírejte podle rizika projektu.
- Kanonický profil se převádí na TOML se základními poli `name`, `description` a `developer_instructions`.
- Logické capabilities se musí ručně nebo mapovací tabulkou převést na Codex sandbox, MCP a skills konfiguraci.

### Minimální konektor

Pro repozitář bez vlastních subagentů nemusí být kromě `AGENTS.md` a `.agents/skills/` potřeba žádný další soubor. `.codex/config.toml` přidávejte pouze při skutečné potřebě projektového nastavení.

## Scénář: Claude Code

### Nativní cesty

```text
CLAUDE.md
.claude/agents/*.md
.claude/skills/<skill>/SKILL.md
.claude/settings.json
```

### Přidané soubory

```text
CLAUDE.md
.claude/
├── agents/
├── skills/
└── settings.json       # jen při potřebě
```

### Pravidla

- `CLAUDE.md` importuje `AGENTS.md` pomocí `@AGENTS.md` a obsahuje jen Claude-specific doplnění.
- Profily se převádějí na Markdown s YAML frontmatter.
- Kanonické skills vždy zůstávají v `.agents/skills/`. Pokud Claude Code vyžaduje `.claude/skills/`, vytvořte platformní symlink nebo označenou generovanou kopii pouze na výslovné přání; nikdy ji nepovažujte za zdroj pravdy.
- Na Windows je výchozí bezpečná strategie generovaná kopie. Symlink použijte jen při spolehlivě nakonfigurovaném prostředí.
- Hooks a permissions patří do `.claude/settings.json`, nikoli do kanonického profilu jako falešné bezpečnostní garance.

## Scénář: Gemini CLI

### Nativní cesty

```text
GEMINI.md
.gemini/settings.json
.agents/skills/          # podporovaná interoperabilní cesta
```

### Přidané soubory

```text
GEMINI.md
.gemini/settings.json    # jen při potřebě
```

### Pravidla

- `GEMINI.md` importuje `AGENTS.md` pomocí `@AGENTS.md`.
- Gemini CLI podporuje `.agents/skills/` jako workspace alias, proto není potřeba kopie skills.
- `settings.json` lze použít k nastavení seznamu kontextových názvů, například `AGENTS.md` a `GEMINI.md`.
- Custom subagents se přidávají pouze tehdy, pokud je jejich aktuální nativní formát ověřen a mapování je bezeztrátové. Jinak zůstává profil kanonický a je používán jako reference pro hlavního agenta.

## Scénář: GitHub Copilot

### Nativní cesty

```text
AGENTS.md
.github/copilot-instructions.md
.github/agents/*.agent.md
```

### Přidané soubory

```text
.github/
├── copilot-instructions.md
└── agents/
    └── <profile>.agent.md
```

### Pravidla

- Copilot umí používat `AGENTS.md`; `.github/copilot-instructions.md` proto zůstává krátký a odkazuje na společná pravidla.
- Profily se převádějí na Markdown s YAML frontmatter.
- Nativní názvy tools se nesmějí zapisovat do kanonického profilu; mapují se až při generování.
- Rozdíly mezi GitHub.com, CLI a IDE se musí zohlednit v testu konektoru.

## Strategie synchronizace skills

| Platforma | Kanonická cesta funguje přímo | Doporučení |
|---|---:|---|
| Codex | Ano | Použít `.agents/skills/` přímo. |
| Gemini CLI | Ano | Použít `.agents/skills/` přímo. |
| Claude Code | Ne jako výchozí projektová cesta | Generovaná kopie nebo symlink do `.claude/skills/`. |
| GitHub Copilot | Závisí na povrchu a aktuální podpoře | Zachovat `.agents/skills/`; případný platformní export provádět podle aktuální dokumentace. |

## Test konektoru

Konektor je přijatelný pouze když:

- platforma načte společná pravidla,
- platforma vidí požadované skills,
- profil lze vybrat nebo delegovat,
- generovaný soubor ukazuje na svůj kanonický zdroj,
- neexistuje ručně editovaná duplicitní kopie znalostí,
- oprávnění odpovídají zvolenému scénáři,
- změna projde `validate-repository-architecture`.

## Oficiální zdroje použité při návrhu

- OpenAI Codex: AGENTS.md, Skills, Config basics, Subagents.
- Anthropic Claude Code: Memory/CLAUDE.md, Skills, Subagents, Settings.
- Gemini CLI: GEMINI.md, Agent Skills, Subagents.
- GitHub Copilot: Custom instructions, Custom agents, Agent Skills.
- Agent Skills open specification.

Před aktualizací generátorů používejte pouze aktuální oficiální dokumentaci.
