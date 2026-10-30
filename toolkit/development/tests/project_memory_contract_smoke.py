"""Optional smoke against the real sibling template and validator, with no network."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile


def run(script, *args):
    result = subprocess.run([sys.executable, "-X", "utf8", str(script), *map(str, args)],
                            capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("orchestrator", type=Path)
    args = parser.parse_args()
    owner = args.orchestrator.resolve() / "product/tools/project-memory/project_memory_repository.py"
    helper = Path(__file__).resolve().parents[3] / "toolkit/agent-infrastructure/repository_architecture.py"
    if not owner.is_file():
        parser.error("The owning Orchestrator validator is not available")
    with tempfile.TemporaryDirectory(prefix="helper-memory-smoke-") as directory:
        root = Path(directory) / "project"
        run(owner, "init", root, "--project-id", "prj_helper_smoke_0001", "--slug", "helper-smoke",
            "--title", "Synthetic helper smoke", "--repository-origin", "flexideo")
        run(owner, "validate", root)
        baseline = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        orientation = run(helper, "validate", root)
        if "semantic validation NOT RUN" not in orientation:
            raise RuntimeError("Helper must distinguish orientation from semantic validation")
        run(helper, "audit", root)
        run(helper, "install-capability", root, "--name", "client-project")
        run(helper, "install-capability", root, "--name", "documentation-management")
        run(helper, "validate", root)
        run(owner, "validate", root)
        for relative, content in baseline.items():
            if (root / relative).read_bytes() != content:
                raise RuntimeError(f"Template-owned file changed: {relative}")
        if (root / "docs/project").exists() or (root / "docs/missions").exists():
            raise RuntimeError("Unexpected second analytical tree")
    print("PASS: real MCP template remains valid and unchanged after helper reader and documentation installation")


if __name__ == "__main__":
    main()
