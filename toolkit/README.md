# Workspace toolkit

Tento kořen obsahuje pouze interní build/release automatizaci workspace.
Publikovatelné nástroje Repository Foundation jsou výhradně v `product/tools/`.

Produktové členění je popsáno v `product/README.md`. V kořenovém toolkitu zůstává
`development/` pro build, integrační testy a release automatizaci workspace.

Pokud projekt již kořenový `toolkit/` používá, zachová se a jednotlivé druhy nástrojů se oddělí vhodnými podsložkami. Nástroje nesmějí být ukládány do `.agents/`, kořenového `tools/`, kořenového `scripts/` ani do `scripts/` uvnitř skillu.

## Produktové nástroje

Bezpečný scaffold, inventura a základní strukturální validace.

```bash
python product/tools/agent-infrastructure/repository_architecture.py init <target> --name "Project"
python product/tools/agent-infrastructure/repository_architecture.py audit <target> --output audit.md
python product/tools/agent-infrastructure/repository_architecture.py validate <target>
```

`audit` pouze mapuje soubory a známé konvence. Sémantická klasifikace zůstává úkolem skillu a člověka.

## Pracovní log workspace

Vytváří, prohledává a ověřuje pracovní historii v `.logs/YYYY/MM/YYYY-MM-DD.md`.

```bash
python product/tools/work-log/work-log.py add . --title "Název" --summary "Výsledek"
python product/tools/work-log/work-log.py search . --query "téma"
python product/tools/work-log/work-log.py validate .
```

## `agent-infrastructure/render_platform_connectors.py`

Na výslovnou volbu vytváří jeden tenký konektor a převádí kanonické profily.

```bash
python product/tools/agent-infrastructure/render_platform_connectors.py <target> --platform codex
python product/tools/agent-infrastructure/render_platform_connectors.py <target> --platform claude --skills-mode copy
```

Parametr `--platform` je povinný. Workflow může zvolit Codex bez otázky pouze při práci v Codexu; samotný deterministický nástroj prostředí neodhaduje.

## `agent-infrastructure/validate_skill_collection.py`

Validuje skills, profily a odkazy.

```bash
python product/tools/agent-infrastructure/validate_skill_collection.py product
```

## Bezpečnost

- Nástroje standardně nepřepisují existující soubory.
- `--force` používejte až po kontrole diffu.
- Nástroje neukládají credentials ani nemění Git remote.
- Automatické nástroje nesmějí provádět sémanticky nejasné přesuny.

## Dokumentační capability

`product/tools/agent-infrastructure/documentation_capability.py` provádí lokální instalaci s
předběžnou kontrolou konfliktů a evidencí digestů; spouští jej repository_architecture.py.
`product/tools/skills/search-markdown-content/search_markdown.py` vyhledává Markdown pomocí AND/OR.
Podrobnosti jsou v [kontraktu capability](../product/references/documentation-management-capability.md).
