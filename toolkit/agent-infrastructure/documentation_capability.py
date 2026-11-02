"""Managed, offline documentation skills; no Project Memory semantic writes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

SKILLS = ("search-markdown-content", "maintain-domain-knowledge", "review-documentation-topology")
FILES = tuple(
    f".agents/skills/{skill}/{relative}"
    for skill in SKILLS for relative in ("SKILL.md", "agents/openai.yaml")
) + ("toolkit/skills/search-markdown-content/search_markdown.py",)
MANIFEST = ".agents/capabilities/documentation-management.json"
PROFILE = ".agents/documentation.json"
CONTRACT = "repository-documentation-installation/1"
DEFAULT_PROFILE = {
    "contract": "repository-documentation/1",
    "roots": ["docs"],
    "generated_roots": ["docs/reference"],
}


def digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def text_digest(content: bytes) -> str:
    """Ignore Git LF/CRLF conversion, retaining every other source byte."""
    return digest(content.replace(b"\r\n", b"\n"))


def encoded(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def checked_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative or ":" in relative:
        raise ValueError(f"Invalid managed path: {relative}")
    candidate = root.joinpath(*path.parts)
    for current in (candidate, *candidate.parents):
        if current == root:
            break
        if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
            raise ValueError(f"Refusing linked managed path: {relative}")
    if not candidate.resolve().is_relative_to(root):
        raise ValueError(f"Managed path escapes target: {relative}")
    if candidate.exists() and not candidate.is_file():
        raise ValueError(f"Expected a file: {relative}")
    return candidate


def profile_errors(value: dict, layout: str | None) -> list[str]:
    errors = []
    if not isinstance(value, dict) or value.get("contract") != "repository-documentation/1":
        return ["Unknown documentation profile contract"]
    roots = value.get("roots")
    generated = value.get("generated_roots")
    if not isinstance(roots, list) or not roots or not isinstance(generated, list):
        return ["Documentation roots/generated_roots must be lists; roots cannot be empty"]
    for relative in roots + generated:
        if (not isinstance(relative, str) or not relative or relative in (".", "/")
                or PurePosixPath(relative).is_absolute() or ".." in PurePosixPath(relative).parts
                or "\\" in relative or ":" in relative):
            errors.append(f"Invalid documentation root: {relative!r}")
    if errors:
        return errors
    if layout is not None and roots != ["docs"]:
        errors.append("Project Memory documentation scope must remain exactly docs")
    if any(not any(PurePosixPath(item).is_relative_to(PurePosixPath(root)) for root in roots) for item in generated):
        errors.append("Generated roots must be inside documentation roots")
    return errors


def read_manifest(root: Path) -> dict | None:
    path = checked_path(root, MANIFEST)
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(value, dict) or value.get("contract") != CONTRACT
            or value.get("source_repository") != "Repository-helper"
            or not isinstance(value.get("files"), dict) or set(value["files"]) != set(FILES)
            or not isinstance(value.get("text_digests"), dict) or set(value["text_digests"]) != set(FILES)
            or any(not isinstance(item, str) or not item.startswith("sha256:") or len(item) != 71
                   for item in (*value["files"].values(), *value["text_digests"].values()))):
        raise ValueError("Invalid documentation installation manifest; resolve it before updating")
    return value


def source_revision(helper: Path) -> str | None:
    result = subprocess.run(["git", "-C", str(helper), "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def installation_errors(root: Path, layout: str | None) -> list[str]:
    """Check installed bytes and local configuration, never semantic PM state."""
    if not (root / MANIFEST).exists():
        return []
    try:
        manifest = read_manifest(root)
        if manifest["layout"] != layout:
            return ["Documentation installation layout changed; review before reinstalling"]
        errors = []
        for relative, expected in manifest["files"].items():
            path = checked_path(root, relative)
            if not path.is_file() or (digest(path.read_bytes()) != expected
                    and text_digest(path.read_bytes()) != manifest["text_digests"][relative]):
                errors.append(f"Documentation managed file is missing or changed: {relative}")
        profile = json.loads(checked_path(root, PROFILE).read_text(encoding="utf-8"))
        return errors + profile_errors(profile, layout)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"Documentation installation: {exc}"]


def install(target: Path, helper: Path, layout: str | None) -> int:
    """Preflight the entire allowlist, then write with rollback on I/O failure.

    Managed files may refresh only from the previously recorded digest. Local or
    unmanaged edits are conflicts, including when the caller supplies --force.
    The profile is target-owned and is never overwritten by an update.
    """
    target, helper = target.resolve(), helper.resolve()
    if layout not in (None, "0.1", "0.2"):
        print("ERROR: Unknown Project Memory layout; no files changed")
        return 2
    try:
        if layout is not None:
            for relative in ("README.md", "project.yaml", ".project-memory/schema-version"):
                path = checked_path(target, relative)
                if not path.is_file() or not path.read_bytes().strip():
                    raise ValueError(f"Incomplete Project Memory orientation: {relative}")
            if (target / ".project-memory/schema-version").read_text(encoding="utf-8-sig").strip() != f"flexideo-project-memory/{layout}":
                raise ValueError("Project Memory marker changed; reload before installing")
        previous = read_manifest(target)
        if previous and previous.get("layout") != layout:
            raise ValueError("Documentation installation layout changed; review before reinstalling")
        payload = {relative: checked_path(helper, relative).read_bytes() for relative in FILES}
        conflicts = []
        for relative, content in payload.items():
            destination = checked_path(target, relative)
            if destination.exists() and text_digest(destination.read_bytes()) != text_digest(content):
                baseline = previous["files"].get(relative) if previous else None
                text_baseline = previous["text_digests"].get(relative) if previous else None
                if digest(destination.read_bytes()) != baseline and text_digest(destination.read_bytes()) != text_baseline:
                    conflicts.append(relative)
        if conflicts:
            raise ValueError("Local/unmanaged changes; review and reconcile before reinstalling: " + ", ".join(conflicts))
        profile_path = checked_path(target, PROFILE)
        profile_bytes = profile_path.read_bytes() if profile_path.exists() else encoded(DEFAULT_PROFILE)
        errors = profile_errors(json.loads(profile_bytes.decode("utf-8")), layout)
        if errors:
            raise ValueError("; ".join(errors))
        manifest = {
            "contract": CONTRACT,
            "source_repository": "Repository-helper",
            "source_revision": source_revision(helper),
            "source_state": "content digests identify installed working-tree bytes; revision alone is not a release",
            "layout": layout,
            "files": {relative: digest(content) for relative, content in payload.items()},
            "text_digests": {relative: text_digest(content) for relative, content in payload.items()},
            "profile": PROFILE,
        }
        payload[PROFILE] = profile_bytes
        payload[MANIFEST] = encoded(manifest)
        # Resolve every destination before creating any directories or files.
        destinations = {relative: checked_path(target, relative) for relative in payload}
        changes = {relative: data for relative, data in payload.items()
                   if not destinations[relative].exists() or destinations[relative].read_bytes() != data}
        backups = {relative: destinations[relative].read_bytes() if destinations[relative].exists() else None for relative in changes}
        created_dirs = set()
        attempted = []
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
                    directory.rmdir()
                except OSError as exc:
                    rollback_errors.append(f"{directory}: {exc}")
            if rollback_errors:
                raise OSError(f"{write_error}; rollback incomplete: {'; '.join(rollback_errors)}") from write_error
            raise
        for relative in payload:
            print(f"{'written' if relative in changes else 'present':7} {relative}")
        print("PASS: documentation skills installed offline; no content, grants, MCP state or deployment changed")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 2
