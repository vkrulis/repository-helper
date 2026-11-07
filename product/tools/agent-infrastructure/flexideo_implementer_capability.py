"""Managed, portable activation bridge; no product or Project Memory content copies."""
from __future__ import annotations

import json
from pathlib import Path
import re

from documentation_capability import checked_path, digest, encoded, source_revision, text_digest
from product_paths import source_path

FILES = (
    ".agents/skills/activate-flexideo-implementer/SKILL.md",
    ".agents/skills/activate-flexideo-implementer/agents/openai.yaml",
    "toolkit/skills/activate-flexideo-implementer/activate.py",
)
MANIFEST = ".agents/capabilities/flexideo-implementer.json"
CONTRACT = "repository-flexideo-implementer-installation/1"


def read_manifest(root: Path) -> dict | None:
    path = checked_path(root, MANIFEST)
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(value, dict) or value.get("contract") != CONTRACT
            or value.get("source_repository") != "Repository-helper"
            or value.get("layout") not in (None, "0.1", "0.2")
            or any(not isinstance(value.get(key), dict) or set(value[key]) != set(FILES)
                   for key in ("files", "text_digests"))
            or any(not isinstance(item, str) or not re.fullmatch(r"sha256:[a-f0-9]{64}", item)
                   for key in ("files", "text_digests") for item in value[key].values())):
        raise ValueError("Invalid Flexideo Implementer installation manifest; review before reinstalling")
    return value


def installation_errors(root: Path, layout: str | None) -> list[str]:
    if not (root / MANIFEST).exists():
        return []
    try:
        manifest = read_manifest(root)
        if manifest["layout"] != layout:
            return ["Flexideo Implementer installation layout changed; review before reinstalling"]
        errors = []
        for relative, expected in manifest["files"].items():
            path = checked_path(root, relative)
            if not path.is_file() or (digest(path.read_bytes()) != expected
                    and text_digest(path.read_bytes()) != manifest["text_digests"][relative]):
                errors.append(f"Flexideo Implementer managed file is missing or changed: {relative}")
        return errors
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"Flexideo Implementer installation: {exc}"]


def install(target: Path, product: Path, layout: str | None) -> int:
    target, product = target.resolve(), product.resolve()
    try:
        if layout not in (None, "0.1", "0.2"):
            raise ValueError("Unknown Project Memory layout; no files changed")
        if layout is not None:
            for relative in ("README.md", "project.yaml", ".project-memory/schema-version"):
                path = checked_path(target, relative)
                if not path.is_file() or not path.read_bytes().strip():
                    raise ValueError(f"Incomplete Project Memory orientation: {relative}")
            if (target / ".project-memory/schema-version").read_text(encoding="utf-8-sig").strip() != f"flexideo-project-memory/{layout}":
                raise ValueError("Project Memory marker changed; reload before installing")
        previous = read_manifest(target)
        if previous and previous["layout"] != layout:
            raise ValueError("Installation layout changed; review before reinstalling")
        payload = {relative: source_path(product, relative).read_bytes() for relative in FILES}
        for relative, content in payload.items():
            path = checked_path(target, relative)
            if path.exists() and text_digest(path.read_bytes()) != text_digest(content):
                if (not previous or (digest(path.read_bytes()) != previous["files"][relative]
                        and text_digest(path.read_bytes()) != previous["text_digests"][relative])):
                    raise ValueError(f"Local/unmanaged change; reconcile before reinstalling: {relative}")
        payload[MANIFEST] = encoded({
            "contract": CONTRACT, "source_repository": "Repository-helper",
            "source_revision": source_revision(product), "layout": layout,
            "source_state": "digests identify installed working-tree bytes; revision alone is not a release",
            "files": {relative: digest(data) for relative, data in payload.items()},
            "text_digests": {relative: text_digest(data) for relative, data in payload.items()},
        })
        destinations = {relative: checked_path(target, relative) for relative in payload}
        changes = {relative: data for relative, data in payload.items()
                   if not destinations[relative].exists() or destinations[relative].read_bytes() != data}
        backups = {relative: destinations[relative].read_bytes() if destinations[relative].exists() else None for relative in changes}
        created_dirs, attempted = set(), []
        try:
            for relative, data in changes.items():
                path = destinations[relative]
                for parent in path.parents:
                    if parent == target or parent.exists():
                        break
                    created_dirs.add(parent)
                path.parent.mkdir(parents=True, exist_ok=True)
                attempted.append(relative)
                path.write_bytes(data)
        except OSError as write_error:
            rollback_errors = []
            for relative in reversed(attempted):
                path = destinations[relative]
                try:
                    if backups[relative] is None:
                        path.unlink(missing_ok=True)
                    elif path.read_bytes() != backups[relative]:
                        path.write_bytes(backups[relative])
                except OSError as exc:
                    rollback_errors.append(f"{relative}: {exc}")
            for directory in sorted(created_dirs, key=lambda p: len(p.parts), reverse=True):
                try:
                    if directory.exists():
                        directory.rmdir()
                except OSError as exc:
                    rollback_errors.append(f"{directory}: {exc}")
            if rollback_errors:
                raise OSError(f"{write_error}; rollback incomplete: {'; '.join(rollback_errors)}") from write_error
            raise
        for relative in payload:
            print(f"{'written' if relative in changes else 'present':7} {relative}")
        print("PASS: activation bridge installed; product location is configured separately on each computer")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 2
