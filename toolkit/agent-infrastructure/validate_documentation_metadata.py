#!/usr/bin/env python3
"""Validate revision metadata and cross-repository documentation links."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ISO8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
REVISION = re.compile(r"^(minor|substantial|structural):\s*\S(?:.*\S)?$")


def frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            continue
        value = match.group(2).strip().strip('"').strip("'")
        values[match.group(1)] = value
    return values


def validate(args: argparse.Namespace) -> int:
    errors: list[str] = []
    root = Path(args.root).resolve()
    public_root = Path(args.public_root).resolve() if args.public_root else None
    domain_root = Path(args.domain_root).resolve() if args.domain_root else None
    files = [Path(item).resolve() for item in args.files]
    for path in files:
        if not path.is_file():
            errors.append(f"Missing file: {path}")
            continue
        meta = frontmatter(path)
        if meta is None:
            errors.append(f"Missing YAML frontmatter: {path}")
            continue
        is_public = public_root is not None and path.is_relative_to(public_root)
        is_domain = domain_root is not None and path.is_relative_to(domain_root)
        if args.require_revision or is_public and "revised_at" in meta:
            for key in ("revised_by", "revised_at"):
                if not meta.get(key):
                    errors.append(f"{path}: missing {key}")
            if meta.get("revised_by") and not REVISION.match(meta["revised_by"]):
                errors.append(f"{path}: revised_by must use minor|substantial|structural: <reason>")
            if meta.get("revised_at") and not ISO8601.match(meta["revised_at"]):
                errors.append(f"{path}: revised_at is not ISO 8601 with timezone")
        if meta.get("source") == "repository" and not meta.get("repository"):
            errors.append(f"{path}: repository is required when source is repository")
        if args.require_links and is_domain:
            links = [item.strip() for item in meta.get("general_documentation", "").split(";") if item.strip()]
            if not links:
                errors.append(f"{path}: missing general_documentation")
            for link in links:
                if not link.startswith("public/"):
                    errors.append(f"{path}: documentation link must start with public/: {link}")
                elif public_root is not None and not (public_root / link).is_file():
                    errors.append(f"{path}: broken documentation link: {link}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: {len(files)} file(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Repository root; used for portable command documentation")
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--public-root")
    parser.add_argument("--domain-root")
    parser.add_argument("--require-revision", action="store_true")
    parser.add_argument("--require-links", action="store_true")
    return validate(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
