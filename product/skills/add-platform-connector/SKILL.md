---
name: add-platform-connector
description: Na výslovnou volbu přidá nebo obnoví jeden tenký platformní konektor nad kanonickými AGENTS.md, .agents/profiles a .agents/skills. Podporuje Codex, Claude Code, Gemini CLI a GitHub Copilot. Použijte po založení nebo reorganizaci repozitáře, při změně AI klienta nebo když je potřeba odstranit duplicitní platformní instrukce; nevytvářejte konektor bez volby uživatele nebo jednoznačně známého aktuálního prostředí.
compatibility: Vyžaduje write přístup. Pro automatické generování je doporučen Python 3 a PyYAML.
metadata:
  version: "1.1"
---

# Přidání tenkého platformního konektoru

## Volba platformy

Vytvořte právě jeden konektor pouze tehdy, když je platforma požadovaná nebo jednoznačně odpovídá aktuálnímu prostředí:

- pracujete-li aktuálně v Codexu a uživatel nemá jinou preferenci, zvolte `codex`;
- v jiném nebo neznámém prostředí se zeptejte, kterou platformu použít;
- nabídněte i možnost nevytvářet žádný konektor;
- nikdy bez výslovného požadavku nevytvářejte konektory pro více platforem.

Podporované hodnoty:

```text
codex
claude
gemini
github-copilot
```

## Vstupní kontrola

Ověřte existenci:

```text
AGENTS.md
.agents/profiles/
.agents/skills/
docs/agent-context/platform-connector-scenarios.md
```

Pokud společná vrstva chybí, nejprve použijte `initialize-agent-ready-repository` nebo dokončete migraci.

## Společný postup

1. Načtěte aktuální scénář z `docs/agent-context/platform-connector-scenarios.md`.
2. Zjistěte existující platformní konfiguraci a zda je ručně spravovaná.
3. Porovnejte ji s kanonickými zdroji.
4. Ověřte, že zvolená platforma odpovídá přání uživatele nebo aktuálnímu Codex prostředí, a vyberte nejtenčí konektor.
5. Před přepsáním existujícího souboru zobrazte rozdíl nebo vyžádejte potvrzení.
6. Generované soubory označte zdrojem a zákazem ruční editace.
7. Nezapisujte model, credentials, MCP endpointy nebo široká oprávnění bez explicitního požadavku.
8. Spusťte platformní i obecnou validaci.

## Codex scénář

- Použijte kořenový `AGENTS.md` přímo.
- Použijte `.agents/skills/` přímo.
- `.codex/config.toml` vytvářejte jen při skutečné projektové konfiguraci.
- Vybrané profily generujte do `.codex/agents/<name>.toml`.
- Povinná pole Codex profilu: `name`, `description`, `developer_instructions`.
- Logické restrictions nepovažujte za vynucené, pokud nejsou mapovány na sandbox nebo permissions.

## Claude Code scénář

- Vytvořte `CLAUDE.md` s importem `@AGENTS.md`.
- Profily generujte do `.claude/agents/<name>.md`.
- Kanonické skills ponechte v `.agents/skills/`. Do `.claude/skills/` je zpřístupněte pouze jako platformní symlink nebo označenou generovanou kopii, pokud to uživatel výslovně požaduje.
- Na Windows preferujte generovanou kopii; na podporovaném prostředí lze použít symlink.
- Claude-specific permissions a hooks patří do `.claude/settings.json`.

## Gemini CLI scénář

- Vytvořte `GEMINI.md` s importem `@AGENTS.md`.
- `.agents/skills/` používejte přímo.
- `.gemini/settings.json` přidávejte jen pro skutečnou konfiguraci, například seznam context filenames.
- Profily nepřevádějte do neověřeného formátu. Pokud generátor nemá aktuální mapování, ponechte kanonický profil a vypište varování.

## GitHub Copilot scénář

- Zachovejte `AGENTS.md` jako společný zdroj.
- `.github/copilot-instructions.md` má být krátký platformní doplněk.
- Profily generujte do `.github/agents/<name>.agent.md`.
- Tools mapujte podle konkrétního Copilot povrchu; nepředpokládejte stejnou podporu ve všech IDE, CLI a GitHub.com.

## Doporučený generátor

```bash
python toolkit/agent-infrastructure/render_platform_connectors.py <repository> --platform codex
```

Volitelně:

```bash
python toolkit/agent-infrastructure/render_platform_connectors.py <repository> \
  --platform claude \
  --profile repository-architect \
  --skills-mode copy
```

Před použitím režimu `--force` vždy zkontrolujte diff.

## Výstup

Vraťte:

- zvolenou platformu,
- vytvořené a změněné soubory,
- mapování profilových polí,
- nepřevedené vlastnosti a varování,
- strategii zpřístupnění skills,
- kroky pro ověření konektoru.

## Akceptace

Načtěte `references/connector-checklist.md` a projděte všechny relevantní body.
