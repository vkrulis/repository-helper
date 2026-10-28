#!/usr/bin/env python3
"""Scaffold, audit and structural validation for agent-ready repositories."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Iterable

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "docs/agent-context/README.md",
    ".agents/README.md",
    ".agents/profiles/README.md",
    ".agents/skills/README.md",
    "toolkit/README.md",
    ".logs/README.md",
    ".agents/skills/maintain-work-log/SKILL.md",
    "toolkit/work-log/README.md",
    "toolkit/work-log/work-log.py",
]

PROHIBITED_TOOL_DIRS = [
    ".agents/tools",
    "tools",
    "scripts",
]

RECOMMENDED_FILES = [
    "resources/README.md",
]

KNOWN_AGENT_PATHS = {
    "AGENTS.md",
    "AGENTS.override.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
}

HELPER_ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_BUNDLES = {
    "work-log": [
        ".logs/README.md",
        ".agents/skills/maintain-work-log/SKILL.md",
        ".agents/skills/maintain-work-log/agents/openai.yaml",
        "toolkit/work-log/README.md",
        "toolkit/work-log/work-log.py",
    ],
    "decision-records": [
        "docs/agent-context/decisions/README.md",
        ".agents/skills/maintain-decision-records/SKILL.md",
        ".agents/skills/maintain-decision-records/agents/openai.yaml",
        ".agents/skills/maintain-decision-records/references/decision-record-template.md",
    ],
    "domain-inventories": [
        "docs/agent-context/domain/README.md",
        ".agents/skills/maintain-domain-inventories/SKILL.md",
        ".agents/skills/maintain-domain-inventories/agents/openai.yaml",
        "toolkit/domain/README.md",
    ],
    "project-documentation": [
        "docs/agent-context/project-documentation-capability.md",
        ".agents/skills/maintain-project-documentation/SKILL.md",
        ".agents/skills/maintain-project-documentation/agents/openai.yaml",
        ".agents/skills/maintain-project-documentation/references/project-documentation-model.md",
        "toolkit/skills/maintain-project-documentation/README.md",
        "toolkit/skills/maintain-project-documentation/project_documentation.py",
    ],
    "client-project": [
        "docs/project/README.md",
        "docs/project/assignment.md",
        "docs/project/analysis/README.md",
        "docs/project/design/README.md",
        "docs/project/client/README.md",
        "docs/project/traceability.md",
        "docs/project/epics/README.md",
        "resources/client-inputs/README.md",
        "resources/diagnostics/README.md",
        "resources/epics/README.md",
        "definitions/README.md",
        "definitions/data/README.md",
        "definitions/temps/README.md",
        "definitions/print-temps/README.md",
        "definitions/site-files/README.md",
        "artifacts/README.md",
        "artifacts/epics/README.md",
        "toolkit/epics/README.md",
        ".agents/skills/maintain-client-project-dimension/SKILL.md",
        ".agents/skills/maintain-client-project-dimension/agents/openai.yaml",
        ".agents/skills/maintain-client-project-dimension/references/project-memory.md",
    ],
    "client-offers": [
        "docs/project/offers/README.md",
        "resources/offers/README.md",
        "resources/offers/_template/README.md",
        "resources/offers/_template/meetings/README.md",
        "resources/offers/_template/client-files/README.md",
        "resources/offers/_template/images/README.md",
        "resources/offers/_template/references/README.md",
        "public/offers/README.md",
        "artifacts/offers/README.md",
        "toolkit/offers/README.md",
        "toolkit/offers/offer_tools.py",
        ".agents/skills/maintain-client-offers/SKILL.md",
        ".agents/skills/maintain-client-offers/agents/openai.yaml",
        ".agents/skills/maintain-client-offers/references/offer-manifest-template.md",
        "docs/agent-context/client-offers-capability.md",
    ],
    "missions": [
        "docs/missions/README.md",
        ".agents/skills/maintain-missions/SKILL.md",
        ".agents/skills/maintain-missions/agents/openai.yaml",
        ".agents/skills/maintain-missions/references/mission-template.md",
    ],
    "documentation-sync": [
        "docs/agent-context/documentation-sync-capability.md",
        ".agents/skills/maintain-documentation-sync/SKILL.md",
        ".agents/skills/maintain-documentation-sync/agents/openai.yaml",
        "toolkit/agent-infrastructure/validate_documentation_metadata.py",
    ],
    "development-testing": [
        "docs/agent-context/development-testing-capability.md",
        ".agents/skills/maintain-development-testing/SKILL.md",
        ".agents/skills/maintain-development-testing/agents/openai.yaml",
    ],
    "product-repository": [
        "docs/agent-context/product-repository-sync-capability.md",
        ".agents/skills/manage-product-repository/SKILL.md",
        ".agents/skills/manage-product-repository/agents/openai.yaml",
    ],
    "authoring-repository": [
        "docs/agent-context/repository-types.md",
        "docs/agent-context/authoring-repository-capability.md",
        "docs/agent-context/authoring-registry-current-state-contract.md",
        ".agents/skills/maintain-authoring-repository/SKILL.md",
        ".agents/skills/maintain-authoring-repository/agents/openai.yaml",
    ],
}

CAPABILITY_DEPENDENCIES = {
    "authoring-repository": ("product-repository", "development-testing"),
    "project-documentation": ("client-project",),
}

CAPABILITY_TEMPLATES = {
    "authoring-repository": {
        "templates/capabilities/authoring-repository/product/README.md": "product/README.md",
        "templates/capabilities/authoring-repository/product/skills/README.md": "product/skills/README.md",
        "templates/capabilities/authoring-repository/product/tools/README.md": "product/tools/README.md",
        "templates/capabilities/authoring-repository/product/contracts/README.md": "product/contracts/README.md",
        "templates/capabilities/authoring-repository/product/tests/README.md": "product/tests/README.md",
    },
}

CAPABILITY_RULES = {
    "work-log": (
        ".logs/YYYY/MM/YYYY-MM-DD.md",
        "Po každé materiální změně použijte skill `maintain-work-log` a přidejte stručný "
        "append-only záznam do `.logs/YYYY/MM/YYYY-MM-DD.md`; před předáním spusťte "
        "`python toolkit/work-log/work-log.py validate .`.",
    ),
    "decision-records": (
        "maintain-decision-records",
        "Při architektonicky významném rozhodnutí použijte skill `maintain-decision-records`. "
        "ADR ukládejte do `docs/agent-context/decisions/` a jeho vznik nebo změnu stavu "
        "vždy propojte s dnešním záznamem v `.logs/`.",
    ),
    "domain-inventories": (
        "maintain-domain-inventories",
        "Pro opakované mapovací průzkumy a sledování aktuálního stavu kódu použijte "
        "skill `maintain-domain-inventories`. Generované inventáře ukládejte do "
        "`docs/agent-context/domain/`, generátory do `toolkit/domain/` a aktualizujte "
        "je spolu se sledovanou změnou.",
    ),
    "project-documentation": (
        "maintain-project-documentation",
        "Aktuální dokumentaci klientské aplikace udržujte skillem "
        "`maintain-project-documentation`. V Project Memory patří současný výklad do "
        "`docs/`, zatímco zadání, evidence a historie změny zůstávají v `project/epics/`. "
        "Generovanou FDT referenci pod `docs/reference/fdt/` ručně neupravujte a XDS, "
        "intranetové settings ani COMEX nepřepisujte jen z dokumentačního nálezu.",
    ),
    "client-project": (
        "maintain-client-project-dimension",
        "Pro klientský implementační projekt udržujte zadání, analýzy, návrhy, potvrzené "
        "závěry a trasovatelnost v `docs/project/`; aktuální technickou a doménovou pravdu "
        "v `docs/agent-context/`, vstupy v `resources/` a ručně spravovaný definiční model "
        "(projektová XDS a *.xcf) v `definitions/`, povinně s podsložkami `definitions/data/`, "
        "`definitions/temps/`, `definitions/print-temps/` a `definitions/site-files/`. Pokud "
        "projektová XDS nebo *.xcf ještě nejsou k dispozici, upozorněte uživatele, že je třeba "
        "je dodat dodatečně. Použijte skill `maintain-client-project-dimension` při založení "
        "nebo materiální změně této struktury.",
    ),
    "client-offers": (
        "maintain-client-offers",
        "Capability `client-offers` je volitelné rozšíření klientského projektu. Pro každou nabídku "
        "oddělte původní podklady v `resources/offers/<offer-id>/`, ověřené závěry a trasovatelnost "
        "v `docs/project/offers/<offer-id>/`, explicitně publikovatelný HTML obsah v "
        "`public/offers/<offer-id>/` a odvozené reporty v `artifacts/offers/<offer-id>/`. "
        "Použijte skill `maintain-client-offers`; do repozitáře neukládejte příjemce, Access policy "
        "ani secrets. Publikace používá URL `/{project-slug}/{offer-slug}/` a je izolovaná po nabídce.",
    ),
    "missions": (
        "maintain-missions",
        "Když práce narazí na cíl přesahující jednu materiální změnu nebo s uživatelem "
        "zatím nesladěný rozsah, aktivně navrhněte založení mise skillem `maintain-missions`. "
        "Mise ukládejte do `docs/missions/NN-<slug>.md` dle "
        "`.agents/skills/maintain-missions/references/mission-template.md`, se stavem "
        "(`draft`/`reviewed`/`in-progress`/`done`/`deferred`/`rejected`) a polem `ADR:` "
        "propojeným na výsledný záznam v `docs/agent-context/decisions/`, jakmile z mise "
        "vzejde architektonicky významné rozhodnutí.",
    ),
}

CAPABILITY_RULES["documentation-sync"] = (
    "maintain-documentation-sync",
    "Pri zmene chovani nebo technickych detailu nejprve aktualizujte domenovou dokumentaci "
    "v `docs/agent-context/`, teprve potom obecnou dokumentaci v sourozeneckem Docusaurus "
    "repozitari. Pouzivejte vazby `general_documentation`, metadata `revised_by`/`revised_at` "
    "a pred predanim uzivatele upozornete na stav domenove revize, revize obecne dokumentace "
    "a publikace.",
)

CAPABILITY_RULES["development-testing"] = (
    "maintain-development-testing",
    "Pro zavedení nebo rozšíření automatického testování a diagnostiky použijte skill "
    "`maintain-development-testing`. Konkrétní runner, prostředí a CI dokumentujte v "
    "`docs/agent-context/testing.md`; izolovaná vývojová automatizace patří do "
    "`toolkit/development/`. Credentials, produkční data a generované testovací artefakty "
    "se necommitují; mutující scénáře vyžadují explicitní opt-in a resetovatelná data.",
)

CAPABILITY_RULES["product-repository"] = (
    "manage-product-repository",
    "Produktovou projekci zavádějte pouze na výslovné přání pomocí skillu "
    "`manage-product-repository`. Pracovní repozitář smí mít právě jednu z hranic "
    "`public/` nebo `product/`; pro synchronizovaný Product repository použijte `product/` "
    "a nikdy ji nekombinujte s `public/`. Nastavení cílového GitHub repository, branch mapping "
    "a oprávnění musí být explicitní; bez nich nevytvářejte automatické cross-repository workflow.",
)

CAPABILITY_RULES["decision-records"] = (
    "maintain-decision-records",
    "Při architektonicky významném rozhodnutí použijte skill `maintain-decision-records`. "
    "ADR ukládejte do `docs/agent-context/decisions/`, s globálním číslem a povinným polem "
    "`Scope: shared|<epic-id>`; jeho vznik nebo změnu stavu vždy propojte s dnešním záznamem v `.logs/`.",
)

CAPABILITY_RULES["client-project"] = (
    "maintain-client-project-dimension",
    "Nejprve rozlište helper-native layout a Project Memory podle project.yaml a .project-memory/. "
    "Memory zakládá MCP/šablona; její Current Truth a project/epics/EPIC-NNNN respektujte podle "
    "reference skillu, nevytvářejte druhé docs/project ani mise. Pro helper-native klientský "
    "implementační projekt udržujte zadání, analýzy, návrhy, potvrzené závěry a "
    "trasovatelnost v `docs/project/`; epiky v `docs/project/epics/<epic-id>/`; aktuální technickou "
    "a doménovou pravdu v `docs/agent-context/`, vstupy v `resources/` a ručně spravovaný definiční "
    "model v `definitions/`. `definitions/` je do přijatého rozhodnutí o jiné strategii jediný zdroj "
    "pravdy. Obsah specifický pro epik patří do `resources/epics/<epic-id>/`, "
    "`artifacts/epics/<epic-id>/` nebo `toolkit/epics/<epic-id>/`; definiční soubory přesouvejte jen "
    "když se nezmění jejich runtime cesta. Použijte skill `maintain-client-project-dimension` při "
    "založení nebo materiální změně této struktury.",
)

CAPABILITY_RULES["missions"] = (
    "maintain-missions",
    "Když práce narazí na dlouhodobý cíl, použijte skill `maintain-missions`. V helper-native klientském projektu "
    "mise představuje epik a její `Epic: <epic-id>` určuje podpůrnou vrstvu. Mise ukládejte do "
    "`docs/missions/NN-<epic-id>.md` dle šablony, se stavem a polem `ADR:` propojeným na výsledná "
    "rozhodnutí v `docs/agent-context/decisions/`.",
)

CAPABILITY_RULES["authoring-repository"] = (
    "maintain-authoring-repository",
    "Pro repozitář typu `authoring` používejte skill `maintain-authoring-repository`. "
    "Uveďte roli `specialist` nebo `orchestrator`; publikovatelný authoring produkt vytvářejte "
    "autoritativně přímo v `product/`, zatímco kořenové `.agents/skills/` slouží pouze údržbě "
    "workspace. Produktové skills neduplikujte mezi `product/skills/` a `.agents/skills/`. "
    "Flexideo-orchestrator je nadřazená authoring entita pro koordinované změny aplikace "
    "napříč vrstvami a specializované produkty načítá z jejich registrů, nekopíruje je. "
    "Cloudové registry používají `docs/agent-context/authoring-registry-current-state-contract.md`: "
    "stabilní cesty, Git jako historii a SHA-256 jako kontrolu obsahu, nikoli adresu.",
)

CAPABILITY_SKILLS = {
    "client-project": "maintain-client-project-dimension",
    "project-documentation": "maintain-project-documentation",
    "client-offers": "maintain-client-offers",
    "missions": "maintain-missions",
    "documentation-sync": "maintain-documentation-sync",
    "development-testing": "maintain-development-testing",
    "product-repository": "manage-product-repository",
    "authoring-repository": "maintain-authoring-repository",
}

SCAFFOLD = {
    "README.md": """# {name}\n\n{purpose}\n\n## Přehled\n\nTODO: Popište hlavní obsah a hranice repozitáře.\n\n## Rychlý start\n\nTODO: Doplňte instalační nebo spouštěcí postup.\n\n## Vývoj a validace\n\nTODO: Doplňte build, test a validační příkazy.\n\n## Dokumentace\n\n- Kontext projektu: `docs/agent-context/`\n- Pravidla agentů: `AGENTS.md`\n- Pracovní historie: `.logs/`\n- Profily: `.agents/profiles/`\n- Skills: `.agents/skills/`\n- Exaktní nástroje: `toolkit/`\n- Zdroje k analýze: `resources/`\n""",
    "AGENTS.md": """# Projektová pravidla\n\n## Zdroje pravdy\n\n- Kontext projektu: `docs/agent-context/`\n- Hlavní orientace: `README.md`\n- Vstupní zdroje k analýze: `resources/`\n- Chronologická pracovní historie: `.logs/YYYY/MM/YYYY-MM-DD.md`\n\n## Povinný pracovní postup\n\n1. Před změnou identifikujte dotčenou komponentu.\n2. Přečtěte relevantní kontext.\n3. Proveďte nejmenší odůvodněnou změnu.\n4. U zdrojů v `resources/` zachovejte původ, licenci a autoritativnost.\n5. Spusťte předepsané kontroly.\n6. Aktualizujte dokumentaci, pokud se změnilo chování.\n7. Po každé materiální změně vytvořte stručný záznam v `.logs/YYYY/MM/YYYY-MM-DD.md` pomocí skillu `maintain-work-log`; existující historii nepřepisujte a před předáním ji validujte.\n\n## Pracovní historie\n\n- Aktuální autoritativní znalost patří do `docs/agent-context/`, chronologie práce do `.logs/` a fyzické změny do Gitu.\n- Zápis musí uvést výsledek, změněné soubory, skutečně provedené validace a otevřenou práci.\n- Do logu nepatří secrets, produkční data, skryté uvažování ani celé výpisy nástrojů.\n\n## Validace\n\nTODO: Doplňte projektové příkazy.\n\n```bash\npython toolkit/work-log/work-log.py validate .\n```\n\n## Omezení\n\n- Neupravujte generované soubory přímo.\n- Neukládejte secrets nebo produkční data.\n- Neoznačujte práci za hotovou bez uvedení výsledků validace a bez aktuálního pracovního logu.\n""",
    "docs/agent-context/README.md": """# Agent context\n\nAutoritativní znalosti o projektu určené lidem i agentům.\n\nDoporučené dokumenty:\n\n- `architecture.md`\n- `development-rules.md`\n- `testing.md`\n- `security.md`\n- `domain/`\n- `decisions/`\n""",
    ".agents/README.md": """# `.agents`\n\nKanonická platformně nezávislá agentní vrstva.\n\n- `profiles/` – definice pracovníků.\n- `skills/` – opakovatelné postupy.\n\nSpustitelné a deterministické nástroje sem nepatří; jejich jediným kořenem je `toolkit/`.\n""",
    ".agents/profiles/README.md": """# Agent profiles\n\nKanonické platformně neutrální profily `<name>.agent.md`.\n\nPlatformní varianty se generují do příslušných konektorů.\n""",
    ".agents/skills/README.md": """# Agent Skills\n\nKaždý skill je složka `<name>/SKILL.md` s validním YAML frontmatter.\n""",
    "toolkit/README.md": """# Toolkit\n\nJediný kořen všech exaktních a spustitelných nástrojů projektu. Patří sem skripty, validátory, generátory, CLI wrappery, spustitelné balíčky a jejich podpůrné soubory.\n\nDoporučené podsložky:\n\n- `agent-infrastructure/` – validace a generování agentní vrstvy;\n- `domain/` – doménové nástroje projektu;\n- `development/` – build, test a vývojová automatizace;\n- `skills/<skill-name>/` – nástroj používaný pouze jedním skillem;\n- `runtime/` – generované nebo dodané spustitelné artefakty, pokud je projekt potřebuje.\n\nTODO: Doplňte dostupné příkazy a pravidla verzování artefaktů.\n""",
    "resources/README.md": """# Resources\n\nProjektové vstupy určené k vyhledávání, čtení nebo analýze.\n\nU každé skupiny zdrojů popište účel, formát, původ, licenci, autoritativnost a způsob aktualizace. Běhový kód ponechte ve standardní projektové cestě; podklady jediného skillu patří do jeho `references/` nebo `assets/`.\n""",
}


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "written"


def project_memory_layout(root: Path) -> str | None:
    """Conservative routing hint, not a semantic YAML/schema validator.

    Any server metadata or Flexideo contract hint protects even incomplete and
    future repositories from the generic scaffold. Ordinary project.yaml files
    alone do not opt into Project Memory handling.
    """
    marker = root / ".project-memory/schema-version"
    identity = root / "project.yaml"
    identity_text = identity.read_text(encoding="utf-8-sig", errors="replace") if identity.is_file() else ""
    if not (root / ".project-memory").exists() and not any(
        hint in identity_text for hint in ("flexideo-project/", "flexideo-project-memory/")
    ):
        return None
    version = marker.read_text(encoding="utf-8-sig", errors="replace").strip() if marker.is_file() else ""
    return {"flexideo-project-memory/0.1": "0.1", "flexideo-project-memory/0.2": "0.2"}.get(version, "unknown")


def command_init(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if project_memory_layout(target) is not None:
        print("ACTION: Project Memory is provisioned by MCP and its versioned template; init refuses to change it, including with --force.", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    purpose = args.purpose or "TODO: Doplňte jednovětý účel projektu."
    changes: list[tuple[str, str]] = []
    for rel, template in SCAFFOLD.items():
        content = template.format(name=args.name, purpose=purpose)
        status = write_file(target / rel, content, args.force)
        changes.append((rel, status))
    for rel, status in changes:
        print(f"{status:7} {rel}")
    if any(status == "skipped" for _, status in changes):
        print("Existing files were preserved. Use --force only after reviewing them.")
    install_capability_bundle(target, "work-log", args.force)
    install_capability_bundle(target, "decision-records", args.force)
    install_capability_bundle(target, "documentation-sync", args.force)
    ensure_capability_rule(target, "work-log")
    ensure_capability_rule(target, "decision-records")
    ensure_capability_rule(target, "documentation-sync")
    return 0


def install_capability_bundle(target: Path, name: str, force: bool) -> list[tuple[str, str]]:
    changes = []
    for rel in CAPABILITY_BUNDLES[name]:
        source = HELPER_ROOT / rel
        destination = target / rel
        if source.resolve() == destination.resolve():
            status = "present"
        elif destination.exists() and not force:
            status = "skipped"
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            status = "written"
        changes.append((rel, status))
        print(f"{status:7} {rel}")
    for source_rel, destination_rel in CAPABILITY_TEMPLATES.get(name, {}).items():
        source = HELPER_ROOT / source_rel
        destination = target / destination_rel
        # Product files become target-owned authoring sources after installation.
        # Even a capability refresh must not overwrite their repository-specific content.
        if destination.exists():
            status = "present"
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            status = "written"
        changes.append((destination_rel, status))
        print(f"{status:7} {destination_rel}")
    return changes


def sync_existing_claude_skill(target: Path, name: str) -> int:
    """Synchronize a marked Claude skill copy with its canonical source."""
    claude_skills = target / ".claude/skills"
    source = target / ".agents/skills" / name
    if not claude_skills.is_dir() or not source.is_dir():
        return 0
    destination = claude_skills / name
    if destination.exists():
        marker = destination / ".generated-from"
        if not marker.is_file():
            print(
                f"ACTION: Refusing to overwrite manual Claude skill copy {destination}; "
                "review it and use the platform renderer explicitly.",
                file=sys.stderr,
            )
            return 1
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        else:
            shutil.rmtree(destination)
    shutil.copytree(source, destination)
    (destination / ".generated-from").write_text(
        f".agents/skills/{name}\n", encoding="utf-8"
    )
    print(f"synced   {destination}")
    return 0


def ensure_capability_rule(target: Path, name: str) -> int:
    agents = target / "AGENTS.md"
    marker, rule = CAPABILITY_RULES[name]
    if not agents.is_file():
        print(f"ACTION: Create AGENTS.md and add the {name} capability rule.")
        return 1
    content = agents.read_text(encoding="utf-8", errors="replace")
    if marker in content:
        print(f"present AGENTS.md {name} rule")
        return 0
    block = f"\n## Repository capability: {name}\n\n{rule}\n"
    agents.write_text(content.rstrip() + "\n" + block, encoding="utf-8")
    print(f"updated AGENTS.md {name} rule")
    return 0


def check_client_project_definitions(target: Path) -> None:
    """Warn when the project's own XDS/*.xcf files still need to be supplied."""
    definitions = target / "definitions"
    missing = []
    if not any(definitions.glob("*.xds")):
        missing.append("*.xds")
    if not any(definitions.glob("*.xcf")):
        missing.append("*.xcf")
    if missing:
        print(
            "ACTION: definitions/ has no project "
            + " and no ".join(missing)
            + " file(s) yet. Supply the real project file(s) and tell the user they still "
            "need to be added."
        )


def validate_offers(target: Path) -> list[str]:
    """Delegate offer-content checks to the portable client-offers tool."""
    tool = target / "toolkit/offers/offer_tools.py"
    if not tool.is_file():
        return []
    result = subprocess.run(
        [sys.executable, str(tool), "validate", "--quiet"],
        cwd=target,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    details = (result.stderr or result.stdout).strip().splitlines()
    return [f"Client-offers: {line}" for line in details] or ["Client-offers validation failed"]


def command_install_capability(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"Not a directory: {target}", file=sys.stderr)
        return 2
    layout = project_memory_layout(target)
    if layout is not None:
        if layout == "unknown" or args.name not in {"client-project", "project-documentation"}:
            print("ACTION: Project Memory supports only explicitly reviewed portable capabilities here. Allowed: client-project orientation and project-documentation; no files changed.", file=sys.stderr)
            return 2
        # No docs/project, missions, ADR registry, definitions scaffold, AGENTS
        # rules or server metadata: the MCP template owns the target structure.
        if args.name == "client-project":
            for rel in CAPABILITY_BUNDLES["client-project"]:
                if rel.startswith(".agents/skills/maintain-client-project-dimension/"):
                    print(f"{write_file(target / rel, (HELPER_ROOT / rel).read_text(encoding='utf-8'), args.force):7} {rel}")
            return sync_existing_claude_skill(target, "maintain-client-project-dimension")
        for rel in CAPABILITY_BUNDLES["project-documentation"]:
            if (
                rel.startswith(".agents/skills/maintain-project-documentation/")
                or rel.startswith("toolkit/skills/maintain-project-documentation/")
            ):
                print(f"{write_file(target / rel, (HELPER_ROOT / rel).read_text(encoding='utf-8'), args.force):7} {rel}")
        return sync_existing_claude_skill(target, "maintain-project-documentation")
    names = (*CAPABILITY_DEPENDENCIES.get(args.name, ()), args.name)
    status = 0
    for name in names:
        install_capability_bundle(target, name, args.force)
        status = ensure_capability_rule(target, name) or status
        status = sync_existing_claude_skill(
            target, CAPABILITY_SKILLS.get(name, name)
        ) or status
    if args.name == "client-project":
        check_client_project_definitions(target)
    if args.name == "client-offers" and not (target / "docs/project/README.md").is_file():
        print(
            "ACTION: client-offers extends a client project. Install client-project before using offers.",
            file=sys.stderr,
        )
    return status


def command_install_work_log(args: argparse.Namespace) -> int:
    args.name = "work-log"
    return command_install_capability(args)


def iter_files(root: Path) -> Iterable[Path]:
    ignored = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file():
            yield path


def classify_path(rel: str, project_memory: bool = False) -> str:
    p = rel.replace("\\", "/")
    name = Path(p).name
    if project_memory:
        if p == "project.yaml":
            return "Project Memory identity and lifecycle"
        for prefix, classification in (
            (".project-memory/", "server-owned Project Memory metadata"),
            ("project/epics/", "epic-local analytical memory"),
            ("project/visions/", "shared future intent; not Current Truth"),
            ("context/", "shared application Current Truth"),
            ("application/", "application identity and technical references"),
            ("definitions/", "source definitions; check producer ownership"),
            ("docs/reference/", "generated reference candidate; verify manifest and scope"),
            ("docs/architecture/", "shared application architecture documentation"),
            ("imports/", "pinned imports with provenance"),
        ):
            if p.startswith(prefix):
                return classification
        if p.split("/", 1)[0] in {"baseline", "analysis", "evidence", "decisions", "questions", "architecture", "reviews", "sessions", "checkpoints", "artifacts"}:
            return "legacy 0.1 semantic area; check declared contract"
    if p == "README.md":
        return "README"
    if name in {"AGENTS.md", "AGENTS.override.md"}:
        return "AGENTS rules"
    if p.startswith("docs/agent-context/"):
        return "agent context"
    if p.startswith(".logs/"):
        return "chronological work log"
    if p.startswith(".agents/profiles/") or p.endswith(".agent.md"):
        return "agent profile"
    if "/skills/" in f"/{p}" or name == "SKILL.md":
        return "skill"
    if p.startswith("toolkit/agent-infrastructure/"):
        return "agent infrastructure tool"
    if p.startswith("toolkit/"):
        return "exact project tool"
    if p.startswith(".agents/tools/") or p.startswith("tools/") or p.startswith("scripts/"):
        return "tool in prohibited legacy location"
    if "/scripts/" in f"/{p}" or p.startswith("bin/"):
        return "tool candidate outside toolkit"
    if p.startswith("resources/"):
        return "analysis resource"
    if p.startswith("product/"):
        return "authoritative product source"
    if p.startswith((".claude/", ".codex/", ".gemini/", ".github/")) or p in {"CLAUDE.md", "GEMINI.md"}:
        return "platform adapter/config"
    if p.startswith(("docs/", "documentation/", "manual/", "wiki/")):
        return "documentation candidate"
    return "unclassified"


def audit_markdown(root: Path) -> str:
    files = sorted(iter_files(root))
    layout = project_memory_layout(root)
    lines = [
        "# Repository structure inventory",
        "",
        f"- Root: `{root}`",
        f"- File count: {len(files)}",
        f"- Layout: {'Project Memory ' + layout if layout else 'helper-native / other (semantic review required)'}",
        "- Project Memory: MCP/template owns provisioning and semantic writes; helper inventory does not validate semantic state." if layout else "- Project Memory markers: not detected.",
        "",
        "This is a mechanical inventory. Semantic conclusions require reading the content.",
        "",
        "## Files",
        "",
        "| Path | Mechanical classification | Size |",
        "|---|---|---:|",
    ]
    for path in files:
        rel = path.relative_to(root).as_posix()
        lines.append(f"| `{rel}` | {classify_path(rel, layout is not None)} | {path.stat().st_size} |")
    lines += ["", "## Known instruction files", ""]
    found = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel in KNOWN_AGENT_PATHS or path.name in {"SKILL.md"} or rel.endswith(".agent.md"):
            found.append(rel)
    if found:
        lines.extend(f"- `{item}`" for item in found)
    else:
        lines.append("- None detected")
    return "\n".join(lines) + "\n"


def command_audit(args: argparse.Namespace) -> int:
    root = Path(args.target).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    report = audit_markdown(root)
    if args.output:
        out = Path(args.output)
        if not out.is_absolute():
            out = Path.cwd() / out
        out.write_text(report, encoding="utf-8")
        print(out)
    else:
        print(report, end="")
    return 0


def validate_project_memory_orientation(root: Path, layout: str) -> int:
    """Check routing prerequisites only; MCP owns document/index/state validity."""
    errors = []
    if layout == "unknown":
        errors.append("Unknown or missing Project Memory schema marker; consult the owning MCP/template, do not scaffold or migrate automatically")
    for rel in ("README.md", "project.yaml", ".project-memory/schema-version"):
        if not (root / rel).is_file() or (root / rel).stat().st_size == 0:
            errors.append(f"Missing or empty Project Memory orientation file: {rel}")
    for message in errors:
        print(f"ERROR: {message}")
    print("INFO: Project Memory semantic validation NOT RUN; use the owning MCP or the matching Orchestrator project_memory_repository.py validate command.")
    if layout == "0.1":
        print("WARN: Legacy Project Memory 0.1 is readable; migration requires a reviewed manifest and pinned head/blob SHA.")
    if (root / "docs/project").exists() or (root / "docs/missions").exists():
        print("WARN: Helper-native project/missions content coexists with Project Memory; review ownership without automatic moves.")
    print("FAIL: Project Memory orientation checks" if errors else f"PASS: Project Memory {layout} orientation checks only")
    return 1 if errors else 0


def command_validate(args: argparse.Namespace) -> int:
    root = Path(args.target).resolve()
    layout = project_memory_layout(root)
    if layout is not None:
        return validate_project_memory_orientation(root, layout)
    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"Missing required file: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"Required file is empty: {rel}")
    agents_path = root / "AGENTS.md"
    if agents_path.is_file() and ".logs/YYYY/MM/YYYY-MM-DD.md" not in agents_path.read_text(encoding="utf-8", errors="replace"):
        errors.append("AGENTS.md does not make .logs/YYYY/MM/YYYY-MM-DD.md work logging explicit")
    for rel in RECOMMENDED_FILES:
        path = root / rel
        if not path.is_file():
            warnings.append(f"Missing recommended file: {rel}")
        elif path.stat().st_size == 0:
            warnings.append(f"Recommended file is empty: {rel}")
    for rel in PROHIBITED_TOOL_DIRS:
        if (root / rel).exists():
            errors.append(f"Prohibited tool directory outside toolkit/: {rel}")
    for path in sorted((root / ".agents/skills").glob("*/scripts")):
        if path.exists():
            errors.append(
                "Executable skill tooling must be moved from "
                f"{path.relative_to(root).as_posix()} to toolkit/skills/<skill-name>/"
            )
    for platform_file in ["CLAUDE.md", "GEMINI.md"]:
        path = root / platform_file
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            if "AGENTS.md" not in text:
                warnings.append(f"{platform_file} does not reference AGENTS.md")
    if not any((root / ".agents/skills").glob("*/SKILL.md")):
        warnings.append("No project skills found; acceptable for a new repository.")
    if not any((root / ".agents/profiles").glob("*.agent.md")):
        warnings.append("No canonical profiles found; acceptable if no specialized role is needed.")
    client_skill = root / ".agents/skills/maintain-client-project-dimension/SKILL.md"
    client_project = root / "docs/project"
    if client_skill.exists() or client_project.exists():
        for rel in (
            "docs/project/README.md",
            "docs/project/assignment.md",
            "docs/project/analysis/README.md",
            "docs/project/design/README.md",
            "docs/project/client/README.md",
            "docs/project/traceability.md",
            "docs/project/epics/README.md",
            "resources/client-inputs/README.md",
            "resources/diagnostics/README.md",
            "resources/epics/README.md",
            "definitions/README.md",
            "definitions/data/README.md",
            "definitions/temps/README.md",
            "definitions/print-temps/README.md",
            "definitions/site-files/README.md",
            "artifacts/README.md",
            "artifacts/epics/README.md",
            "toolkit/epics/README.md",
        ):
            if not (root / rel).is_file():
                errors.append(f"Client-project capability is missing {rel}")
        if not client_skill.is_file():
            errors.append("Client-project capability is missing maintain-client-project-dimension/SKILL.md")
        if agents_path.is_file() and "maintain-client-project-dimension" not in agents_path.read_text(encoding="utf-8", errors="replace"):
            errors.append("AGENTS.md does not make client-project handling explicit")
        definitions_dir = root / "definitions"
        if definitions_dir.is_dir():
            if not any(definitions_dir.glob("*.xds")):
                warnings.append("definitions/ has no project *.xds file yet; supply it and notify the user.")
            if not any(definitions_dir.glob("*.xcf")):
                warnings.append("definitions/ has no project *.xcf file yet; supply it and notify the user.")
    project_docs_skill = root / ".agents/skills/maintain-project-documentation/SKILL.md"
    if project_docs_skill.exists():
        for rel in (
            ".agents/skills/maintain-project-documentation/SKILL.md",
            ".agents/skills/maintain-project-documentation/agents/openai.yaml",
            ".agents/skills/maintain-project-documentation/references/project-documentation-model.md",
            "toolkit/skills/maintain-project-documentation/README.md",
            "toolkit/skills/maintain-project-documentation/project_documentation.py",
        ):
            if not (root / rel).is_file():
                errors.append(f"Project-documentation capability is missing {rel}")
        if project_memory_layout(root) is None:
            if not (root / "docs/agent-context/project-documentation-capability.md").is_file():
                errors.append("Project-documentation capability is missing docs/agent-context/project-documentation-capability.md")
            if agents_path.is_file() and "maintain-project-documentation" not in agents_path.read_text(encoding="utf-8", errors="replace"):
                errors.append("AGENTS.md does not make project-documentation handling explicit")
    offers_skill = root / ".agents/skills/maintain-client-offers/SKILL.md"
    offers_root = root / "docs/project/offers"
    if offers_skill.exists() or offers_root.exists():
        if not client_project.exists():
            errors.append("Client-offers capability requires the client-project capability")
        for rel in (
            "docs/project/offers/README.md",
            "resources/offers/README.md",
            "resources/offers/_template/README.md",
            "resources/offers/_template/meetings/README.md",
            "resources/offers/_template/client-files/README.md",
            "resources/offers/_template/images/README.md",
            "resources/offers/_template/references/README.md",
            "public/offers/README.md",
            "artifacts/offers/README.md",
            "toolkit/offers/README.md",
            "toolkit/offers/offer_tools.py",
            "docs/agent-context/client-offers-capability.md",
        ):
            if not (root / rel).is_file():
                errors.append(f"Client-offers capability is missing {rel}")
        if not offers_skill.is_file():
            errors.append("Client-offers capability is missing maintain-client-offers/SKILL.md")
        if agents_path.is_file() and "maintain-client-offers" not in agents_path.read_text(encoding="utf-8", errors="replace"):
            errors.append("AGENTS.md does not make client-offers handling explicit")
        offers_errors = validate_offers(root)
        errors.extend(offers_errors)
    testing_skill = root / ".agents/skills/maintain-development-testing/SKILL.md"
    testing_context = root / "docs/agent-context/development-testing-capability.md"
    if testing_skill.exists() or testing_context.exists():
        for rel in (
            "docs/agent-context/development-testing-capability.md",
            ".agents/skills/maintain-development-testing/SKILL.md",
        ):
            if not (root / rel).is_file():
                errors.append(f"Development-testing capability is missing {rel}")
        if agents_path.is_file() and "maintain-development-testing" not in agents_path.read_text(encoding="utf-8", errors="replace"):
            errors.append("AGENTS.md does not make development-testing handling explicit")
    authoring_skill = root / ".agents/skills/maintain-authoring-repository/SKILL.md"
    authoring_context = root / "docs/agent-context/authoring-repository-capability.md"
    agents_text = (
        agents_path.read_text(encoding="utf-8", errors="replace")
        if agents_path.is_file()
        else ""
    )
    authoring_active = (root / "product").exists() and (
        authoring_skill.exists() or authoring_context.exists()
    )
    if authoring_active:
        for rel in (
            "docs/agent-context/repository-types.md",
            "docs/agent-context/authoring-repository-capability.md",
            "docs/agent-context/authoring-registry-current-state-contract.md",
            ".agents/skills/maintain-authoring-repository/SKILL.md",
            ".agents/skills/manage-product-repository/SKILL.md",
            ".agents/skills/maintain-development-testing/SKILL.md",
            "product/README.md",
            "product/skills/README.md",
            "product/tools/README.md",
            "product/contracts/README.md",
            "product/tests/README.md",
        ):
            if not (root / rel).is_file():
                errors.append(f"Authoring-repository capability is missing {rel}")
        if (root / "public").exists():
            errors.append("Authoring repository cannot contain both public/ and product/")
        if agents_path.is_file() and "maintain-authoring-repository" not in agents_text:
            errors.append("AGENTS.md does not make authoring-repository handling explicit")
        product_skills = {
            path.parent.name
            for path in (root / "product/skills").glob("*/SKILL.md")
        }
        workspace_skills = {
            path.parent.name
            for path in (root / ".agents/skills").glob("*/SKILL.md")
        }
        for duplicate in sorted(product_skills & workspace_skills):
            errors.append(
                "Authoring product skill is duplicated in product/skills and .agents/skills: "
                + duplicate
            )
    decisions_dir = root / "docs/agent-context/decisions"
    decision_skill = root / ".agents/skills/maintain-decision-records/SKILL.md"
    if decisions_dir.exists() or decision_skill.exists():
        if not (decisions_dir / "README.md").is_file():
            errors.append("Decision-record capability is missing docs/agent-context/decisions/README.md")
        if not decision_skill.is_file():
            errors.append("Decision-record capability is missing maintain-decision-records/SKILL.md")
        if agents_path.is_file() and "maintain-decision-records" not in agents_path.read_text(encoding="utf-8", errors="replace"):
            errors.append("AGENTS.md does not make decision-record handling explicit")
        adr_files = sorted(decisions_dir.glob("[0-9][0-9][0-9][0-9]-*.md"))
        log_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in sorted((root / ".logs").glob("????/??/????-??-??.md")))
        adr_ids: set[str] = set()
        for adr in adr_files:
            adr_text = adr.read_text(encoding="utf-8", errors="replace")
            adr_id = adr.name[:4]
            if adr_id in adr_ids:
                errors.append(f"Duplicate ADR number: {adr_id}")
            adr_ids.add(adr_id)
            if not adr_text.startswith(f"# ADR-{adr_id}:"):
                errors.append(f"Invalid ADR heading: {adr.relative_to(root).as_posix()}")
            status_match = re.search(r"(?m)^- Stav:\s*(proposed|accepted|rejected|superseded)\s*$", adr_text)
            if not status_match:
                errors.append(f"Missing or invalid ADR status: {adr.relative_to(root).as_posix()}")
            scope_match = re.search(r"(?m)^- Scope:\s*(shared|[a-z0-9]+(?:-[a-z0-9]+)*)\s*$", adr_text)
            if not scope_match:
                errors.append(f"Missing or invalid ADR Scope: {adr.relative_to(root).as_posix()}")
            for field in ("Nahrazuje", "Nahrazeno"):
                match = re.search(rf"(?m)^- {field}:\s*(.+)$", adr_text)
                if not match:
                    errors.append(f"Missing ADR field {field}: {adr.relative_to(root).as_posix()}")
                    continue
                for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", match.group(1)):
                    if not (adr.parent / link).resolve().is_file():
                        errors.append(f"Broken ADR {field} link in {adr.name}: {link}")
            if status_match and status_match.group(1) == "superseded":
                replaced = re.search(r"(?m)^- Nahrazeno:\s*(.+)$", adr_text)
                if not replaced or not re.search(r"\[[^]]+\]\([^)]+\)", replaced.group(1)):
                    errors.append(f"Superseded ADR must link to its replacement: {adr.name}")
            if adr.name not in log_text:
                errors.append(f"ADR is not linked from a daily work log: {adr.name}")
    missions_dir = root / "docs/missions"
    mission_skill = root / ".agents/skills/maintain-missions/SKILL.md"
    if missions_dir.exists() or mission_skill.exists():
        if not (missions_dir / "README.md").is_file():
            errors.append("Missions capability is missing docs/missions/README.md")
        if not mission_skill.is_file():
            errors.append("Missions capability is missing maintain-missions/SKILL.md")
        if agents_path.is_file() and "maintain-missions" not in agents_path.read_text(encoding="utf-8", errors="replace"):
            errors.append("AGENTS.md does not make missions handling explicit")
        mission_files = sorted(p for p in missions_dir.glob("[0-9][0-9]-*.md"))
        mission_numbers: set[str] = set()
        for mission in mission_files:
            number = mission.name[:2]
            if number in mission_numbers:
                errors.append(f"Duplicate mission number: {number}")
            mission_numbers.add(number)
            mission_text = mission.read_text(encoding="utf-8", errors="replace")
            if not mission_text.startswith("# Mise:"):
                continue
            status_match = re.search(
                r"(?m)^- Stav:\s*(draft|reviewed|in-progress|done|deferred|rejected)\s*$",
                mission_text,
            )
            if not status_match:
                errors.append(f"Missing or invalid mission Stav: {mission.relative_to(root).as_posix()}")
            epic_match = re.search(r"(?m)^- Epic:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", mission_text)
            if not epic_match:
                errors.append(f"Missing or invalid mission Epic: {mission.relative_to(root).as_posix()}")
            elif client_project.exists() and not (root / "docs/project/epics" / epic_match.group(1) / "README.md").is_file():
                errors.append(f"Mission epic has no project context: {epic_match.group(1)}")
            adr_field = re.search(r"(?m)^- ADR:\s*(.+)$", mission_text)
            if not adr_field:
                errors.append(f"Missing mission ADR field: {mission.relative_to(root).as_posix()}")
            else:
                for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", adr_field.group(1)):
                    if not (mission.parent / link).resolve().is_file():
                        errors.append(f"Broken mission ADR link in {mission.name}: {link}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN:  {message}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a minimal agent-ready repository scaffold")
    p_init.add_argument("target")
    p_init.add_argument("--name", required=True)
    p_init.add_argument("--purpose")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=command_init)

    p_audit = sub.add_parser("audit", help="Create a read-only mechanical inventory")
    p_audit.add_argument("target")
    p_audit.add_argument("--output")
    p_audit.set_defaults(func=command_audit)

    p_validate = sub.add_parser("validate", help="Validate the basic repository architecture")
    p_validate.add_argument("target")
    p_validate.set_defaults(func=command_validate)

    p_cap = sub.add_parser("install-capability", help="Install or update one canonical repository capability")
    p_cap.add_argument("target")
    p_cap.add_argument("--name", required=True, choices=sorted(CAPABILITY_BUNDLES))
    p_cap.add_argument("--force", action="store_true")
    p_cap.set_defaults(func=command_install_capability)

    p_logs = sub.add_parser("install-work-log", help="Deprecated alias for install-capability --name work-log")
    p_logs.add_argument("target")
    p_logs.add_argument("--force", action="store_true")
    p_logs.set_defaults(func=command_install_work_log)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
