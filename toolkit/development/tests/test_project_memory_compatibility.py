"""Regressions: helper must preserve MCP-owned project memory and native support."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "toolkit/agent-infrastructure/repository_architecture.py"


def run_cli(root, *args):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), args[0], str(root), *args[1:]],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class ProjectMemoryCompatibility(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def memory(self, version="0.2"):
        for relative, text in {
            "README.md": "# Synthetic orientation fixture\n",
            "AGENTS.md": "# Template-owned rules\n",
            "project.yaml": f"contract: flexideo-project/{'2' if version == '0.2' else '1'}\n",
            ".project-memory/schema-version": f"flexideo-project-memory/{version}\n",
            ".project-memory/epics.json": '{"revision": 7}\n',
            "context/application-context.md": "Confirmed shared context\n",
            "project/epics/EPIC-0001/decisions/DEC-0001-sample.md": "Historical decision\n",
            "docs/reference/manifest.json": '{"producer": "synthetic"}\n',
        }.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def test_audit_is_read_only_and_maps_memory_areas(self):
        self.memory()
        before = snapshot(self.root)
        result = run_cli(self.root, "audit")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Project Memory 0.2", result.stdout)
        self.assertIn("epic-local analytical memory", result.stdout)
        self.assertIn("shared application Current Truth", result.stdout)
        self.assertIn("generated reference candidate", result.stdout)
        self.assertEqual(snapshot(self.root), before)

    def test_orientation_does_not_claim_semantic_validity_or_require_native_scaffold(self):
        self.memory()  # Deliberately not a semantically valid FAAM repository.
        before = snapshot(self.root)
        result = run_cli(self.root, "validate")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("semantic validation NOT RUN", result.stdout)
        self.assertIn("orientation checks only", result.stdout)
        self.assertEqual(snapshot(self.root), before)

    def test_force_init_is_refused_without_mutation(self):
        self.memory()
        before = snapshot(self.root)
        for force in ([], ["--force"]):
            result = run_cli(self.root, "init", "--name", "Wrong scaffold", *force)
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(snapshot(self.root), before)

    def test_install_only_distributes_portable_reader_and_preserves_template(self):
        self.memory()
        before = snapshot(self.root)
        result = run_cli(self.root, "install-capability", "--name", "client-project")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = snapshot(self.root)
        for relative, data in before.items():
            self.assertEqual(after[relative], data, relative)
        additions = set(after) - set(before)
        self.assertEqual(additions, {
            ".agents/skills/maintain-client-project-dimension/SKILL.md",
            ".agents/skills/maintain-client-project-dimension/agents/openai.yaml",
            ".agents/skills/maintain-client-project-dimension/references/project-memory.md",
        })
        # A second install cannot overwrite a local reader customization by default.
        skill = self.root / ".agents/skills/maintain-client-project-dimension/SKILL.md"
        skill.write_text("Local customization\n", encoding="utf-8")
        before_retry = snapshot(self.root)
        self.assertEqual(run_cli(self.root, "install-capability", "--name", "client-project").returncode, 0)
        self.assertEqual(snapshot(self.root), before_retry)

    def test_project_documentation_capability_is_non_semantic_and_portable(self):
        self.memory()
        before = snapshot(self.root)
        result = run_cli(self.root, "install-capability", "--name", "project-documentation")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = snapshot(self.root)
        for relative, data in before.items():
            self.assertEqual(after[relative], data, relative)
        additions = set(after) - set(before)
        self.assertEqual(additions, {
            ".agents/skills/maintain-project-documentation/SKILL.md",
            ".agents/skills/maintain-project-documentation/agents/openai.yaml",
            ".agents/skills/maintain-project-documentation/references/project-documentation-model.md",
            "toolkit/skills/maintain-project-documentation/README.md",
            "toolkit/skills/maintain-project-documentation/project_documentation.py",
        })
        self.assertFalse((self.root / "docs/index.md").exists())
        self.assertFalse((self.root / "docs/project").exists())
        self.assertEqual(
            run_cli(self.root, "install-capability", "--name", "project-documentation").returncode,
            0,
        )

    def test_incompatible_capabilities_cannot_write_even_with_force(self):
        self.memory()
        before = snapshot(self.root)
        for name in ("missions", "decision-records", "client-offers", "authoring-repository", "work-log", "domain-inventories", "documentation-sync", "development-testing", "product-repository"):
            with self.subTest(capability=name):
                result = run_cli(self.root, "install-capability", "--name", name, "--force")
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual(snapshot(self.root), before)

    def test_legacy_memory_is_readable_without_migration(self):
        self.memory("0.1")
        baseline = self.root / "baseline/baseline-story.md"
        baseline.parent.mkdir()
        baseline.write_text("Legacy baseline\n", encoding="utf-8")
        before = snapshot(self.root)
        result = run_cli(self.root, "validate")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Legacy Project Memory 0.1", result.stdout)
        self.assertEqual(run_cli(self.root, "install-capability", "--name", "client-project").returncode, 0)
        for relative, data in before.items():
            self.assertEqual(snapshot(self.root)[relative], data, relative)

    def test_unknown_and_incomplete_memory_never_fall_back_to_native(self):
        for marker in ("flexideo-project-memory/9.9\n", ""):
            with self.subTest(marker=marker):
                self.memory()
                (self.root / ".project-memory/schema-version").write_text(marker, encoding="utf-8")
                before = snapshot(self.root)
                self.assertEqual(run_cli(self.root, "validate").returncode, 1)
                self.assertEqual(run_cli(self.root, "install-capability", "--name", "client-project", "--force").returncode, 2)
                self.assertEqual(run_cli(self.root, "install-capability", "--name", "project-documentation", "--force").returncode, 2)
                self.assertEqual(run_cli(self.root, "init", "--name", "Wrong", "--force").returncode, 2)
                self.assertEqual(snapshot(self.root), before)

    def test_identity_hint_alone_protects_partial_provisioning(self):
        (self.root / "project.yaml").write_text('{contract: "flexideo-project/2"}\n', encoding="utf-8")
        before = snapshot(self.root)
        self.assertEqual(run_cli(self.root, "init", "--name", "Wrong", "--force").returncode, 2)
        self.assertEqual(run_cli(self.root, "validate").returncode, 1)
        self.assertEqual(snapshot(self.root), before)

    def test_native_project_with_unrelated_yaml_still_installs_and_validates(self):
        (self.root / "project.yaml").write_text("name: ordinary-project\n", encoding="utf-8")
        self.assertEqual(run_cli(self.root, "init", "--name", "Native fixture").returncode, 0)
        result = run_cli(self.root, "install-capability", "--name", "client-project")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "docs/project/assignment.md").is_file())
        self.assertTrue((self.root / "definitions/print-temps/README.md").is_file())
        result = run_cli(self.root, "validate")
        self.assertEqual(result.returncode, 0, result.stdout)
        # Native validation remains active: removing assignment is still an error.
        (self.root / "docs/project/assignment.md").unlink()
        self.assertEqual(run_cli(self.root, "validate").returncode, 1)


if __name__ == "__main__":
    unittest.main()
