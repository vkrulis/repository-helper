#!/usr/bin/env python3
"""Validate Agent Skills, canonical profiles and their local references."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_PATH = re.compile(r"`((?:references|assets)/[^`]+)`")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    meta = yaml.safe_load(match.group(1)) or {}
    return meta, match.group(2)


def validate_skill(path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        meta, body = parse_frontmatter(path)
    except Exception as exc:
        return [f"{path}: {exc}"], []
    name = meta.get("name")
    desc = meta.get("description")
    expected = path.parent.name
    if not isinstance(name, str) or not name:
        errors.append(f"{path}: missing name")
    else:
        if name != expected:
            errors.append(f"{path}: name '{name}' does not match directory '{expected}'")
        if not SKILL_NAME.fullmatch(name):
            errors.append(f"{path}: invalid skill name '{name}'")
        if len(name) > 64:
            errors.append(f"{path}: name exceeds 64 characters")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{path}: missing description")
    elif len(desc) > 1024:
        errors.append(f"{path}: description exceeds 1024 characters")
    elif len(desc) < 60:
        warnings.append(f"{path}: description may be too vague for reliable triggering")
    if len(body.splitlines()) > 500:
        warnings.append(f"{path}: SKILL.md exceeds 500 lines; move details to references")
    refs = set(CODE_PATH.findall(body))
    for target in MD_LINK.findall(body):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        refs.add(target.split("#", 1)[0])
    for rel in sorted(refs):
        candidate = (path.parent / rel).resolve()
        try:
            candidate.relative_to(path.parent.resolve())
        except ValueError:
            warnings.append(f"{path}: reference leaves skill directory: {rel}")
        if not candidate.exists():
            errors.append(f"{path}: missing referenced resource: {rel}")
    return errors, warnings


def validate_profile(path: Path, root: Path, skills: set[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        meta, _ = parse_frontmatter(path)
    except Exception as exc:
        return [f"{path}: {exc}"], []
    for field in ("name", "description"):
        if not meta.get(field):
            errors.append(f"{path}: missing {field}")
    for skill in meta.get("skills") or []:
        if skill not in skills:
            errors.append(f"{path}: unknown skill '{skill}'")
    required = ((meta.get("context") or {}).get("required") or [])
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"{path}: missing required context '{rel}'")
    for capability in meta.get("capabilities") or []:
        if not isinstance(capability, str) or ":" not in capability:
            warnings.append(f"{path}: capability '{capability}' is not namespaced/logical")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.repository).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    skill_paths = sorted((root / ".agents/skills").glob("*/SKILL.md"))
    skills = {p.parent.name for p in skill_paths}
    if not skill_paths:
        warnings.append("No skills found in .agents/skills")
    for path in skill_paths:
        e, w = validate_skill(path, root)
        errors.extend(e)
        warnings.extend(w)

    profile_paths = sorted((root / ".agents/profiles").glob("*.agent.md"))
    names: set[str] = set()
    for path in profile_paths:
        e, w = validate_profile(path, root, skills)
        errors.extend(e)
        warnings.extend(w)
        try:
            meta, _ = parse_frontmatter(path)
            name = meta.get("name")
            if name in names:
                errors.append(f"{path}: duplicate profile name '{name}'")
            if name:
                names.add(name)
        except Exception:
            pass

    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN:  {item}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: {len(skill_paths)} skill(s), {len(profile_paths)} profile(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
