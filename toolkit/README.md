# Toolkit

Toto je jediný kořen všech exaktních a spustitelných nástrojů repozitáře. Patří sem skripty (`*.py`, `*.ps1`, `*.sh`, `*.bat` a další), validátory, generátory, CLI wrappery, spustitelné balíčky a jejich podpůrné soubory.

Nástroje se člení podle odpovědnosti:

- `agent-infrastructure/` – validace a generování agentní vrstvy;
- `domain/` – doménové nástroje projektu;
- `development/` – build, test a vývojová automatizace;
- `skills/<skill-name>/` – nástroj používaný pouze jedním skillem;
- `runtime/` – generované nebo dodané spustitelné artefakty, pokud je projekt potřebuje.
- `work-log/` – společný nástroj pro pracovní historii `.logs/`.

Pokud projekt již kořenový `toolkit/` používá, zachová se a jednotlivé druhy nástrojů se oddělí vhodnými podsložkami. Nástroje nesmějí být ukládány do `.agents/`, kořenového `tools/`, kořenového `scripts/` ani do `scripts/` uvnitř skillu.

## `agent-infrastructure/repository_architecture.py`

Bezpečný scaffold, inventura a základní strukturální validace.

```bash
python toolkit/agent-infrastructure/repository_architecture.py init <target> --name "Project"
python toolkit/agent-infrastructure/repository_architecture.py audit <target> --output audit.md
python toolkit/agent-infrastructure/repository_architecture.py validate <target>
python toolkit/agent-infrastructure/repository_architecture.py install-work-log <target>
```

`audit` pouze mapuje soubory a známé konvence. Sémantická klasifikace zůstává úkolem skillu a člověka.

## `work-log/work-log.py`

Vytváří, prohledává a ověřuje pracovní historii v `.logs/YYYY/MM/YYYY-MM-DD.md`.

```bash
python toolkit/work-log/work-log.py add . --title "Název" --summary "Výsledek"
python toolkit/work-log/work-log.py search . --query "téma"
python toolkit/work-log/work-log.py validate .
```

## `agent-infrastructure/render_platform_connectors.py`

Na výslovnou volbu vytváří jeden tenký konektor a převádí kanonické profily.

```bash
python toolkit/agent-infrastructure/render_platform_connectors.py <target> --platform codex
python toolkit/agent-infrastructure/render_platform_connectors.py <target> --platform claude --skills-mode copy
```

Parametr `--platform` je povinný. Workflow může zvolit Codex bez otázky pouze při práci v Codexu; samotný deterministický nástroj prostředí neodhaduje.

## `agent-infrastructure/validate_skill_collection.py`

Validuje skills, profily a odkazy.

```bash
python toolkit/agent-infrastructure/validate_skill_collection.py .
```

## Bezpečnost

- Nástroje standardně nepřepisují existující soubory.
- `--force` používejte až po kontrole diffu.
- Nástroje neukládají credentials ani nemění Git remote.
- Automatické nástroje nesmějí provádět sémanticky nejasné přesuny.

## Dokumentační capability

`agent-infrastructure/documentation_capability.py` provádí lokální instalaci s
předběžnou kontrolou konfliktů a evidencí digestů; spouští jej repository_architecture.py.
`skills/search-markdown-content/search_markdown.py` vyhledává Markdown pomocí AND/OR.
Podrobnosti jsou v [kontraktu capability](../docs/agent-context/documentation-management-capability.md).
