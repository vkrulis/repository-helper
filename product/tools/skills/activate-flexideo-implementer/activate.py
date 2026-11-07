#!/usr/bin/env python3
"""Locate and verify a local Implementer; leave bootstrap loading to the agent."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PRODUCT = "flexideo-implementer"
SLOTS = {"fcl", "xds-authoring", "intranet-authoring", "comex-authoring", "authoring-tools", "server-solving"}
BOOTSTRAP = "fcl/skills/resolve-flexideo-authoring-request/SKILL.md"
VERIFIER = "fcl/tools/local-library/library.py"


class ActivationError(ValueError):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


def default_registry() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData/Local") / "Flexideo/local-products.json"
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "Flexideo/local-products.json"


def read_registry(path: Path, *, required: bool = True) -> dict:
    if not path.exists():
        if required:
            raise ActivationError("NOT_CONFIGURED", f"Register {PRODUCT} on this computer first: {path}")
        return {"schema_version": 1, "products": {}}
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ActivationError("INVALID_REGISTRY", "Local product registry is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("products"), dict):
        raise ActivationError("INVALID_REGISTRY", "Unknown local product registry contract")
    return value


def registered_root(path: Path) -> Path:
    record = read_registry(path)["products"].get(PRODUCT)
    if record is None:
        raise ActivationError("NOT_CONFIGURED", f"No {PRODUCT} registered in {path}")
    if not isinstance(record, dict) or not isinstance(record.get("root"), str) or not Path(record["root"]).is_absolute():
        raise ActivationError("INVALID_REGISTRY", "The registered product root must be an absolute path")
    return Path(record["root"])


def verify(root: Path) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ActivationError("ASSEMBLY_NOT_FOUND", f"No installed assembly at {root}")
    try:
        before = (root / "assembly.lock.json").read_bytes()
        lock = json.loads(before)
    except (FileNotFoundError, UnicodeError, json.JSONDecodeError) as exc:
        raise ActivationError("INVALID_ASSEMBLY", "Missing or invalid assembly.lock.json") from exc
    if (not isinstance(lock, dict) or lock.get("schema_version") != 1
            or not isinstance(lock.get("assembly_id"), str)
            or not isinstance(lock.get("products"), dict) or set(lock["products"]) != SLOTS):
        raise ActivationError("INVALID_ASSEMBLY", "Expected a locked FCL assembly with all five layer slots")
    for relative in ("AGENTS.md", BOOTSTRAP, VERIFIER):
        if not (root / relative).is_file():
            raise ActivationError("INVALID_ASSEMBLY", f"Missing entrypoint: {relative}")
    try:
        checked = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(root / VERIFIER), "--assembly", str(root), "verify"],
            cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        raise ActivationError("VERIFICATION_FAILED", "Assembly verification timed out") from exc
    try:
        evidence = json.loads(checked.stdout)
    except json.JSONDecodeError as exc:
        raise ActivationError("VERIFICATION_FAILED", "Assembly verifier did not return JSON; check host access") from exc
    if checked.returncode != 0 or not isinstance(evidence, dict) or evidence.get("status") != "VERIFIED":
        raise ActivationError("VERIFICATION_FAILED", "Assembly integrity verification failed; run its verify command for details")
    if evidence.get("assembly_id") != lock["assembly_id"] or (root / "assembly.lock.json").read_bytes() != before:
        raise ActivationError("ASSEMBLY_CHANGED", "Assembly changed during verification; restart activation")
    return {"assembly_root": str(root), "assembly_id": lock["assembly_id"]}


def register(root: Path, registry: Path, *, replace: bool = False) -> dict:
    evidence = verify(root)  # Do not create even a directory for an invalid installation.
    value = read_registry(registry, required=False)
    record = value["products"].get(PRODUCT)
    if record is not None:
        current = registered_root(registry).resolve()
        if current != Path(evidence["assembly_root"]) and not replace:
            raise ActivationError("REGISTRATION_CONFLICT", "A different installation is registered; review and use --replace")
    value["products"][PRODUCT] = {**(record or {}), "root": evidence["assembly_root"]}
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if not registry.exists() or registry.read_bytes() != data:
        registry.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=registry.parent, prefix=".local-products-", suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(data)
            os.replace(temporary, registry)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return {"status": "REGISTERED", "registry": str(registry), **evidence}


def activate(project: Path, registry: Path, *, assembly: Path | None = None, expected: str | None = None) -> dict:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise ActivationError("INVALID_PROJECT", "Client project directory does not exist")
    root = (assembly if assembly is not None else registered_root(registry)).expanduser().resolve()
    if project.is_relative_to(root):
        raise ActivationError("INVALID_PROJECT", "Client project must be outside the distributed assembly")
    evidence = verify(root)
    if expected is not None and evidence["assembly_id"] != expected:
        raise ActivationError("ASSEMBLY_CHANGED", "The session's pinned assembly is no longer active; use a new chat")
    return {
        "status": "READY_FOR_BOOTSTRAP", "project_root": str(project), **evidence,
        "project_instructions": [str(project / name) for name in ("AGENTS.md", "AGENTS.override.md") if (project / name).is_file()],
        "instructions_path": str(root / "AGENTS.md"), "bootstrap_path": str(root / BOOTSTRAP),
        "loading": "EXPLICIT_AGENT_READ_REQUIRED", "execution": "NOT_STARTED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    registration = commands.add_parser("register", help="Register a verified installation for this computer/user")
    registration.add_argument("--root", required=True, type=Path)
    registration.add_argument("--replace", action="store_true")
    activation = commands.add_parser("activate", help="Verify a product and return explicit bootstrap entrypoints")
    activation.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[3])
    activation.add_argument("--assembly", type=Path, help="Explicit installation override; does not change the registry")
    activation.add_argument("--expected-assembly", help="Previously pinned assembly ID for a session preflight")
    for command in (registration, activation):
        command.add_argument("--registry", type=Path, default=None, help="Explicit registry override (default: per-user local configuration)")
    args = parser.parse_args(argv)
    registry = (args.registry if args.registry is not None else default_registry()).expanduser().absolute()
    try:
        result = register(args.root, registry, replace=args.replace) if args.command == "register" else activate(
            args.project, registry, assembly=args.assembly, expected=args.expected_assembly,
        )
    except ActivationError as exc:
        result = {"status": exc.status, "message": str(exc), "execution": "NOT_STARTED"}
    except PermissionError:
        result = {"status": "BLOCKED_HOST_ACCESS", "message": "Host cannot access the project, registry or local product", "execution": "NOT_STARTED"}
    except OSError as exc:
        result = {"status": "LOCAL_IO_ERROR", "message": str(exc), "execution": "NOT_STARTED"}
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["status"] in {"REGISTERED", "READY_FOR_BOOTSTRAP"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
