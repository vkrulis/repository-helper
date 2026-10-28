#!/usr/bin/env python3
"""Read-only validation and inventory for Flexideo project documentation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

CORE_AREAS = ("aplikace", "datovy-model", "procesy", "integrace", "provoz", "reference")
ANALYTICAL_NAMES = {
    "epics", "visions", "evidence", "decisions", "questions",
    "sessions", "checkpoints", "analysis", "baseline",
}
FDT_REQUIRED = (
    "manifest.json",
    "index.md",
    "fdt/index.md",
    "indexes/fdt/segments.jsonl",
    "indexes/fdt/by-xds-id.json",
)
DOCUMENT_CLASSES = {"data", "view", "pseudo"}


def is_project_memory(root: Path) -> bool:
    marker = root / ".project-memory/schema-version"
    return marker.is_file()


def read_memory_version(root: Path) -> str | None:
    marker = root / ".project-memory/schema-version"
    if not marker.is_file():
        return None
    return marker.read_text(encoding="utf-8", errors="replace").strip()


def safe_relative(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def validate_fdt_reference(root: Path, errors: list[str], warnings: list[str]) -> dict:
    fdt_root = root / "docs/reference/fdt"
    info = {"present": fdt_root.is_dir(), "documents": 0, "classes": {}}
    if not fdt_root.exists():
        return info
    if not fdt_root.is_dir():
        errors.append("docs/reference/fdt must be a directory")
        return info

    for relative in FDT_REQUIRED:
        if not (fdt_root / relative).is_file():
            errors.append(f"FDT reference is missing {relative}")

    manifest = fdt_root / "manifest.json"
    manifest_data = None
    if manifest.is_file():
        try:
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid FDT manifest.json: {exc}")
        if isinstance(manifest_data, dict):
            owned = manifest_data.get("owned_files")
            if owned is not None:
                if not isinstance(owned, list):
                    errors.append("FDT manifest owned_files must be a list when present")
                else:
                    for value in owned:
                        if not isinstance(value, str) or not safe_relative(value):
                            errors.append(f"Unsafe FDT owned_files entry: {value!r}")
                            continue
                        if not (fdt_root / value).is_file():
                            errors.append(f"FDT manifest-owned file is missing: {value}")

    fdt_dir = fdt_root / "fdt"
    if fdt_dir.is_dir():
        info["documents"] = len([p for p in fdt_dir.glob("*.md") if p.name != "index.md"])

    documents_index = fdt_root / "indexes/fdt/documents.jsonl"
    if documents_index.is_file():
        classes: dict[str, int] = {}
        for number, raw in enumerate(documents_index.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                item = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"documents.jsonl line {number}: {exc}")
                continue
            if not isinstance(item, dict):
                errors.append(f"documents.jsonl line {number}: object expected")
                continue
            kind = item.get("document_class")
            if kind not in DOCUMENT_CLASSES:
                errors.append(
                    f"documents.jsonl line {number}: document_class must be data/view/pseudo"
                )
                continue
            classes[kind] = classes.get(kind, 0) + 1
            name = item.get("name")
            if not isinstance(name, str) or not name.strip():
                errors.append(f"documents.jsonl line {number}: missing document name")
        info["classes"] = classes
    else:
        warnings.append(
            "FDT reference has no indexes/fdt/documents.jsonl; data/view/pseudo "
            "classification must come from the producer or verified XDS analysis."
        )
    return info


def validate(root: Path) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    root = root.resolve()
    docs = root / "docs"
    memory = is_project_memory(root)
    version = read_memory_version(root)

    if memory and (docs / "project").exists():
        errors.append(
            "Project Memory must not contain helper-native docs/project; "
            "analytical scope belongs to project/epics/."
        )

    if docs.exists() and not docs.is_dir():
        errors.append("docs must be a directory")
    elif docs.is_dir():
        if not (docs / "index.md").is_file():
            warnings.append("docs/ exists but docs/index.md is missing")
        for name in sorted(ANALYTICAL_NAMES):
            path = docs / name
            if path.exists():
                warnings.append(
                    f"docs/{name}/ looks analytical; verify that it does not duplicate Project Memory."
                )

    fdt = validate_fdt_reference(root, errors, warnings)
    report = {
        "project_memory": memory,
        "memory_version": version,
        "docs_present": docs.is_dir(),
        "fdt_reference": fdt,
    }
    return errors, warnings, report


def inventory(root: Path) -> dict:
    root = root.resolve()
    docs = root / "docs"
    errors, warnings, report = validate(root)
    areas = {}
    if docs.is_dir():
        for name in CORE_AREAS:
            area = docs / name
            areas[name] = {
                "present": area.is_dir(),
                "markdown_files": len(list(area.rglob("*.md"))) if area.is_dir() else 0,
            }
    report["areas"] = areas
    report["errors"] = errors
    report["warnings"] = warnings
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    p_validate = commands.add_parser("validate", help="Validate project documentation boundaries")
    p_validate.add_argument("repository", nargs="?", default=".")

    p_inventory = commands.add_parser("inventory", help="Inventory current project documentation")
    p_inventory.add_argument("repository", nargs="?", default=".")
    p_inventory.add_argument("--json", action="store_true", dest="as_json")

    args = parser.parse_args()
    root = Path(args.repository)

    if args.command == "validate":
        errors, warnings, report = validate(root)
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARN:  {item}")
        mode = report["memory_version"] or "helper-native/other"
        if errors:
            print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s); layout={mode}")
            return 1
        print(f"PASS: project documentation boundary; {len(warnings)} warning(s); layout={mode}")
        return 0

    report = inventory(root)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Project Memory: {report['project_memory']} ({report['memory_version'] or '-'})")
        print(f"docs/: {report['docs_present']}")
        for name, area in report["areas"].items():
            print(f"{name:14} present={area['present']} markdown={area['markdown_files']}")
        fdt = report["fdt_reference"]
        print(
            "FDT reference: "
            f"present={fdt['present']} documents={fdt['documents']} classes={fdt['classes']}"
        )
        for item in report["errors"]:
            print(f"ERROR: {item}")
        for item in report["warnings"]:
            print(f"WARN:  {item}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
