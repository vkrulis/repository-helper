#!/usr/bin/env python3
"""Render thin platform adapters from canonical repository agent profiles."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

GENERATED = "GENERATED FROM: {source}\nDO NOT EDIT DIRECTLY. Re-run toolkit/agent-infrastructure/render_platform_connectors.py."


def parse_profile(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    metadata = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    for key in ("name", "description"):
        if not metadata.get(key):
            raise ValueError(f"Missing {key}: {path}")
    return metadata, body


def profile_paths(root: Path, selected: list[str]) -> list[Path]:
    profiles = sorted((root / ".agents/profiles").glob("*.agent.md"))
    if not selected:
        return profiles
    wanted = set(selected)
    result = []
    for path in profiles:
        metadata, _ = parse_profile(path)
        if metadata["name"] in wanted or path.stem.replace(".agent", "") in wanted:
            result.append(path)
    missing = wanted - {parse_profile(p)[0]["name"] for p in result}
    if missing:
        raise ValueError(f"Unknown profiles: {', '.join(sorted(missing))}")
    return result


def ensure_write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        current = path.read_text(encoding="utf-8", errors="replace")
        if current == content:
            print(f"unchanged {path}")
            return
        raise FileExistsError(f"Refusing to overwrite {path}; use --force after reviewing diff")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"written   {path}")


def toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def render_codex(root: Path, profiles: list[Path], force: bool) -> None:
    config = root / ".codex/config.toml"
    if not config.exists():
        content = """# Project-scoped Codex configuration.\n# Keep model choice and personal defaults in ~/.codex/config.toml unless the project truly requires them.\n\n[agents]\nmax_depth = 1\n"""
        ensure_write(config, content, force=False)
    for source in profiles:
        meta, body = parse_profile(source)
        skills = meta.get("skills") or []
        context = (meta.get("context") or {}).get("required") or []
        restrictions = meta.get("restrictions") or []
        additions = []
        if context:
            additions.append("Required context:\n" + "\n".join(f"- {x}" for x in context))
        if skills:
            additions.append("Use these canonical skills when relevant:\n" + "\n".join(f"- {x}" for x in skills))
        if restrictions:
            additions.append("Instructional restrictions (enforce separately in sandbox/permissions):\n" + "\n".join(f"- {x}" for x in restrictions))
        instructions = body + ("\n\n" + "\n\n".join(additions) if additions else "")
        rel_source = source.relative_to(root).as_posix()
        content = (
            f"# GENERATED FROM: {rel_source}\n# DO NOT EDIT DIRECTLY. Re-run toolkit/agent-infrastructure/render_platform_connectors.py.\n"
            f"name = {toml_string(str(meta['name']))}\n"
            f"description = {toml_string(str(meta['description']))}\n"
            "developer_instructions = \"\"\"\n"
            f"{instructions}\n"
            "\"\"\"\n"
        )
        ensure_write(root / ".codex/agents" / f"{meta['name']}.toml", content, force)


def render_claude(root: Path, profiles: list[Path], force: bool, skills_mode: str) -> None:
    claude_md = """<!-- GENERATED THIN ADAPTER. Source of shared rules: AGENTS.md -->\n\n@AGENTS.md\n\n# Claude Code specific notes\n\n- Canonical agent profiles are stored in `.agents/profiles/`.\n- Canonical skills are stored in `.agents/skills/`.\n- Do not duplicate project knowledge in this file.\n"""
    ensure_write(root / "CLAUDE.md", claude_md, force)
    for source in profiles:
        meta, body = parse_profile(source)
        rel_source = source.relative_to(root).as_posix()
        skills = meta.get("skills") or []
        front = {
            "name": meta["name"],
            "description": meta["description"],
        }
        if skills:
            front["skills"] = skills
        content = (
            f"<!-- {GENERATED.format(source=rel_source)} -->\n"
            "---\n"
            f"{yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()}\n"
            "---\n\n"
            f"{body}\n"
        )
        ensure_write(root / ".claude/agents" / f"{meta['name']}.md", content, force)
    source_skills = root / ".agents/skills"
    target_skills = root / ".claude/skills"
    if skills_mode == "none":
        print("skills    not exposed to Claude (--skills-mode none)")
    elif skills_mode == "copy":
        target_skills.mkdir(parents=True, exist_ok=True)
        for skill in source_skills.iterdir() if source_skills.exists() else []:
            if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                continue
            target = target_skills / skill.name
            if target.exists():
                if not force:
                    raise FileExistsError(f"Refusing to replace {target}; use --force")
                if target.is_symlink() or target.is_file():
                    target.unlink()
                else:
                    shutil.rmtree(target)
            shutil.copytree(skill, target)
            marker = target / ".generated-from"
            marker.write_text(f".agents/skills/{skill.name}\n", encoding="utf-8")
            print(f"copied    {target}")
    elif skills_mode == "symlink":
        target_skills.mkdir(parents=True, exist_ok=True)
        for skill in source_skills.iterdir() if source_skills.exists() else []:
            if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                continue
            target = target_skills / skill.name
            if target.exists() or target.is_symlink():
                if not force:
                    raise FileExistsError(f"Refusing to replace {target}; use --force")
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            relative = Path(os.path.relpath(skill, target.parent))
            target.symlink_to(relative, target_is_directory=True)
            print(f"symlinked {target} -> {relative}")


def render_gemini(root: Path, force: bool) -> None:
    gemini_md = """<!-- GENERATED THIN ADAPTER. Source of shared rules: AGENTS.md -->\n\n@AGENTS.md\n\n# Gemini CLI specific notes\n\n- Use canonical workspace skills from `.agents/skills/`.\n- Canonical agent profiles are stored in `.agents/profiles/`.\n- Do not duplicate project knowledge in this file.\n"""
    ensure_write(root / "GEMINI.md", gemini_md, force)
    settings = root / ".gemini/settings.json"
    if not settings.exists():
        content = '{\n  "context": {\n    "fileName": ["AGENTS.md", "GEMINI.md"]\n  }\n}\n'
        ensure_write(settings, content, force=False)


def render_copilot(root: Path, profiles: list[Path], force: bool) -> None:
    instructions = """<!-- GENERATED THIN ADAPTER. Shared rules live in AGENTS.md. -->\n\nFollow the repository-wide rules in `AGENTS.md`.\nUse `docs/agent-context/` as the source of project knowledge, `.agents/profiles/` as the canonical agent definitions, `.agents/skills/` as reusable workflows, and `toolkit/` as the single root for all deterministic tools.\nDo not duplicate those sources here.\n"""
    ensure_write(root / ".github/copilot-instructions.md", instructions, force)
    for source in profiles:
        meta, body = parse_profile(source)
        rel_source = source.relative_to(root).as_posix()
        front = {
            "name": meta["name"],
            "description": meta["description"],
        }
        content = (
            f"<!-- {GENERATED.format(source=rel_source)} -->\n"
            "---\n"
            f"{yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()}\n"
            "---\n\n"
            f"{body}\n"
        )
        ensure_write(root / ".github/agents" / f"{meta['name']}.agent.md", content, force)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository")
    parser.add_argument(
        "--platform",
        choices=["codex", "claude", "gemini", "github-copilot"],
        required=True,
        help="Explicit target platform; the tool never creates connectors implicitly.",
    )
    parser.add_argument("--profile", action="append", default=[], help="Profile name; repeatable. Default: all")
    parser.add_argument("--skills-mode", choices=["copy", "symlink", "none"], default="copy")
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.repository).resolve()
    if not (root / "AGENTS.md").is_file():
        print("Missing AGENTS.md", file=sys.stderr)
        return 2
    try:
        profiles = profile_paths(root, args.profile)
        if args.platform == "codex":
            render_codex(root, profiles, args.force)
        elif args.platform == "claude":
            render_claude(root, profiles, args.force, args.skills_mode)
        elif args.platform == "gemini":
            render_gemini(root, args.force)
        else:
            render_copilot(root, profiles, args.force)
    except (ValueError, FileExistsError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
