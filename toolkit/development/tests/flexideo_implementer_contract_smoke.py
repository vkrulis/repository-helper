"""Install into a temporary client and activate an explicit real product, offline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HELPER = Path(__file__).resolve().parents[3]
TOOL = "toolkit/skills/activate-flexideo-implementer/activate.py"


def run(*args, cwd):
    result = subprocess.run([sys.executable, "-B", "-X", "utf8", *map(str, args)],
                            cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assembly", type=Path, required=True)
    args = parser.parse_args()
    assembly = args.assembly.resolve()
    with tempfile.TemporaryDirectory(prefix="flexideo-activation-smoke-") as temporary:
        base = Path(temporary)
        project = base / "client project with spaces"
        project.mkdir()
        original = {
            "README.md": "# Synthetic client fixture\n",
            "AGENTS.md": "# Project-owned rules\n",
            "project.yaml": "contract: flexideo-project/2\n",
            ".project-memory/schema-version": "flexideo-project-memory/0.2\n",
            ".project-memory/epics.json": '{"revision": 7}\n',
        }
        for relative, content in original.items():
            path = project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode("utf-8"))
        run(HELPER / "toolkit/agent-infrastructure/repository_architecture.py",
            "install-capability", project, "--name", "flexideo-implementer", cwd=HELPER)
        registry = base / "local user config/local-products.json"
        registered = json.loads(run(project / TOOL, "register", "--root", assembly,
                                    "--registry", registry, cwd=base))
        # No --project and an unrelated cwd: the installed tool must retain its client.
        activated = json.loads(run(project / TOOL, "activate", "--registry", registry,
                                   "--expected-assembly", registered["assembly_id"], cwd=base))
        if activated["status"] != "READY_FOR_BOOTSTRAP" or activated["project_root"] != str(project.resolve()):
            raise RuntimeError("Wrong activation result or client root")
        if activated["assembly_root"] != str(assembly) or activated["execution"] != "NOT_STARTED":
            raise RuntimeError("Wrong assembly or execution state")
        for key in ("instructions_path", "bootstrap_path"):
            path = Path(activated[key])
            if not path.is_relative_to(assembly) or not path.read_text(encoding="utf-8").strip():
                raise RuntimeError("Missing readable product entrypoint")
        for relative, content in original.items():
            if (project / relative).read_bytes() != content.encode("utf-8"):
                raise RuntimeError(f"Project-owned file changed: {relative}")
        if (project / "fcl").exists() or (project / "docs/project").exists():
            raise RuntimeError("Unexpected product copy or analytical scaffold")
        run(HELPER / "toolkit/agent-infrastructure/repository_architecture.py",
            "validate", project, cwd=HELPER)
        print(json.dumps({"status": "PASS", "assembly_id": activated["assembly_id"],
                          "scenario": "temporary Memory 0.2, isolated registry, unrelated cwd, real FCL verify",
                          "project_content": "PRESERVED", "model_host_acceptance": "NOT_RUN",
                          "live_instance_execution": "NOT_RUN"}, indent=2))


if __name__ == "__main__":
    main()
