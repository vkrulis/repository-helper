#!/usr/bin/env python3
"""Scaffold, audit and structural validation for agent-ready repositories."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import shutil
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


def command_init(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
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
    ensure_capability_rule(target, "work-log")
    ensure_capability_rule(target, "decision-records")
    return 0


def install_capability_bundle(target: Path, name: str, force: bool) -> list[tuple[str, str]]:
    changes = []
    for rel in CAPABILITY_BUNDLES[name]:
        source = HELPER_ROOT / rel
        destination = target / rel
        if destination.exists() and not force:
            status = "skipped"
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            status = "written"
        changes.append((rel, status))
        print(f"{status:7} {rel}")
    return changes


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


def command_install_capability(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"Not a directory: {target}", file=sys.stderr)
        return 2
    install_capability_bundle(target, args.name, args.force)
    return ensure_capability_rule(target, args.name)


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


def classify_path(rel: str) -> str:
    p = rel.replace("\\", "/")
    name = Path(p).name
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
    if p.startswith((".claude/", ".codex/", ".gemini/", ".github/")) or p in {"CLAUDE.md", "GEMINI.md"}:
        return "platform adapter/config"
    if p.startswith(("docs/", "documentation/", "manual/", "wiki/")):
        return "documentation candidate"
    return "unclassified"


def audit_markdown(root: Path) -> str:
    files = sorted(iter_files(root))
    lines = [
        "# Repository structure inventory",
        "",
        f"- Root: `{root}`",
        f"- File count: {len(files)}",
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
        lines.append(f"| `{rel}` | {classify_path(rel)} | {path.stat().st_size} |")
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


def command_validate(args: argparse.Namespace) -> int:
    root = Path(args.target).resolve()
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
