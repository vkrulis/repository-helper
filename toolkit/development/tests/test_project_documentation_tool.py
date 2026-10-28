"""Tests for the portable project documentation read-only helper."""

from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "toolkit/skills/maintain-project-documentation/project_documentation.py"


def run_tool(root: Path, *args: str):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOL), *args, str(root)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


class ProjectDocumentationTool(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, relative: str, text: str):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def memory(self):
        self.write("project.yaml", "contract: flexideo-project/2\n")
        self.write(".project-memory/schema-version", "flexideo-project-memory/0.2\n")

    def fdt_reference(self):
        self.write("docs/index.md", "# Dokumentace\n")
        self.write("docs/reference/fdt/manifest.json", json.dumps({"format_version": 1}))
        self.write("docs/reference/fdt/index.md", "# FDT\n")
        self.write("docs/reference/fdt/fdt/index.md", "# Typy\n")
        self.write("docs/reference/fdt/fdt/kontakt.md", "# Kontakt\n")
        self.write("docs/reference/fdt/indexes/fdt/segments.jsonl", "{}\n")
        self.write("docs/reference/fdt/indexes/fdt/by-xds-id.json", "{}\n")

    def test_empty_repository_is_read_only_pass(self):
        before = list(self.root.rglob("*"))
        result = run_tool(self.root, "validate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, list(self.root.rglob("*")))

    def test_valid_reference_passes_with_classification_warning(self):
        self.memory()
        self.fdt_reference()
        result = run_tool(self.root, "validate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("documents.jsonl", result.stdout)

    def test_documents_index_accepts_explicit_classes(self):
        self.memory()
        self.fdt_reference()
        self.write(
            "docs/reference/fdt/indexes/fdt/documents.jsonl",
            json.dumps({"name": "kontakt", "document_class": "data"}) + "\n"
            + json.dumps({"name": "kontakt_view", "document_class": "view"}) + "\n"
            + json.dumps({"name": "pomocny", "document_class": "pseudo"}) + "\n",
        )
        result = run_tool(self.root, "inventory", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["fdt_reference"]["classes"],
            {"data": 1, "pseudo": 1, "view": 1},
        )

    def test_invalid_document_class_fails(self):
        self.fdt_reference()
        self.write(
            "docs/reference/fdt/indexes/fdt/documents.jsonl",
            json.dumps({"name": "kontakt", "document_class": "guess"}) + "\n",
        )
        result = run_tool(self.root, "validate")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("data/view/pseudo", result.stdout)

    def test_project_memory_rejects_helper_native_docs_project(self):
        self.memory()
        self.write("docs/project/assignment.md", "# Duplicate analysis\n")
        result = run_tool(self.root, "validate")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("must not contain helper-native docs/project", result.stdout)

    def test_proposal_reference_family_is_visible_but_not_claimed_implemented(self):
        self.memory()
        self.write("docs/index.md", "# Dokumentace\n")
        self.write("docs/reference/application/index.md", "# Application reference\n")
        result = run_tool(self.root, "inventory", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["reference_families"]["application"]["present"])
        self.assertEqual(report["reference_families"]["application"]["status"], "proposal")
        self.assertTrue(
            any("proposal-stage" in item for item in report["warnings"]),
            report["warnings"],
        )

    def test_curated_page_without_provenance_is_warning(self):
        self.write("docs/index.md", "# Dokumentace\n")
        self.write("docs/aplikace/funkce/fakturace.md", "# Fakturace\n\nPopis.\n")
        result = run_tool(self.root, "inventory", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        missing = report["curated_areas"]["aplikace"]["missing_provenance"]
        self.assertIn("docs/aplikace/funkce/fakturace.md", missing)

    def test_curated_page_with_provenance_passes_without_that_warning(self):
        self.write("docs/index.md", "# Dokumentace\n")
        self.write(
            "docs/aplikace/funkce/fakturace.md",
            "# Fakturace\n\n## Zdroje a aktuálnost\n\n- Ověřeno: 2026-10-28\n",
        )
        result = run_tool(self.root, "inventory", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["curated_areas"]["aplikace"]["missing_provenance"], [])


if __name__ == "__main__":
    unittest.main()
