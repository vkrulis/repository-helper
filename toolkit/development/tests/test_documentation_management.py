"""Observable installation and update invariants, using synthetic projects only."""
import importlib.util
import contextlib
import io
import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
MODULE = ROOT / "toolkit/agent-infrastructure/documentation_capability.py"
spec = importlib.util.spec_from_file_location("documentation_capability_tested", MODULE)
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)
CLI = ROOT / "toolkit/agent-infrastructure/repository_architecture.py"


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class DocumentationInstallation(unittest.TestCase):
    def setUp(self):
        output = contextlib.redirect_stdout(io.StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = self.base / "project"
        self.target.mkdir()
        self.source = self.base / "source"
        for relative in docs.FILES:
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"synthetic source {relative}\n", encoding="utf-8")

    def memory(self, version="0.2"):
        for relative, data in {
            "project.yaml": "contract: flexideo-project/2\n",
            "AGENTS.md": "Template-owned rules\n",
            "README.md": "Fixture\n",
            ".project-memory/schema-version": f"flexideo-project-memory/{version}\n",
            ".project-memory/epics.json": '{"revision":17}\n',
            "project/epics/EPIC-0001/analysis/state.yaml": "revision: 17\n",
            "context/application-context.md": "Confirmed context\n",
            "docs/reference/manifest.json": '{"producer":"fixture"}\n',
        }.items():
            path = self.target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data, encoding="utf-8")

    def test_known_memory_install_preserves_every_project_file_and_is_idempotent(self):
        self.memory()
        before = snapshot(self.target)
        self.assertEqual(docs.install(self.target, self.source, "0.2"), 0)
        after = snapshot(self.target)
        self.assertEqual({p: after[p] for p in before}, before)
        self.assertEqual(set(after) - set(before), set(docs.FILES) | {docs.PROFILE, docs.MANIFEST})
        manifest = json.loads(after[docs.MANIFEST])
        for relative in docs.FILES:
            self.assertEqual(manifest["files"][relative], docs.digest(after[relative]))
        self.assertEqual(docs.installation_errors(self.target, "0.2"), [])
        self.assertEqual(docs.install(self.target, self.source, "0.2"), 0)
        self.assertEqual(snapshot(self.target), after)

    def test_refresh_updates_only_baseline_bytes_and_preserves_target_profile(self):
        self.assertEqual(docs.install(self.target, self.source, None), 0)
        profile = self.target / docs.PROFILE
        profile.write_text(json.dumps({"contract":"repository-documentation/1", "roots":["manual", "guide"], "generated_roots":["manual/reference"]}), encoding="utf-8")
        original_profile = profile.read_bytes()
        changed = docs.FILES[-1]
        (self.source / changed).write_text("new source\n", encoding="utf-8")
        self.assertEqual(docs.install(self.target, self.source, None), 0)
        self.assertEqual((self.target / changed).read_bytes(), (self.source / changed).read_bytes())
        self.assertEqual(profile.read_bytes(), original_profile)
        self.assertEqual(docs.installation_errors(self.target, None), [])

    def test_drift_refuses_whole_update_and_validation_reports_it(self):
        self.memory()
        docs.install(self.target, self.source, "0.2")
        (self.target / docs.FILES[-1]).write_text("local change", encoding="utf-8")
        (self.source / docs.FILES[0]).write_text("upstream change", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(docs.install(self.target, self.source, "0.2"), 2)
        self.assertEqual(snapshot(self.target), before)
        self.assertTrue(docs.installation_errors(self.target, "0.2"))

    def test_unmanaged_conflict_and_missing_source_write_nothing(self):
        target_file = self.target / docs.FILES[-1]
        target_file.parent.mkdir(parents=True)
        target_file.write_text("local tool", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(docs.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)
        (self.source / docs.FILES[0]).unlink()
        self.assertEqual(docs.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)

    def test_profile_cannot_expand_memory_scope_and_malformed_manifest_is_preserved(self):
        self.memory()
        docs.install(self.target, self.source, "0.2")
        profile = self.target / docs.PROFILE
        profile.write_text(json.dumps({"contract":"repository-documentation/1", "roots":["project"], "generated_roots":[]}), encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(docs.install(self.target, self.source, "0.2"), 2)
        self.assertEqual(snapshot(self.target), before)
        (self.target / docs.MANIFEST).write_text('{"contract":"broken"}', encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(docs.install(self.target, self.source, "0.2"), 2)
        self.assertEqual(snapshot(self.target), before)

    def test_linked_destination_cannot_escape_or_write_anything(self):
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.target / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if os.name != "nt":
                self.skipTest(f"Symlink creation unavailable: {exc}")
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.target / ".agents"), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest(f"Symlink/junction creation unavailable: {exc}")
        self.assertEqual(docs.install(self.target, self.source, None), 2)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.target / "toolkit").exists())

    def test_io_failure_restores_prior_files(self):
        original_write = Path.write_bytes
        calls = 0
        def flaky_write(path, data):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("synthetic write failure")
            return original_write(path, data)
        before = snapshot(self.target)
        with patch.object(Path, "write_bytes", flaky_write):
            self.assertEqual(docs.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_git_line_endings_do_not_look_like_authored_drift(self):
        docs.install(self.target, self.source, None)
        for relative in docs.FILES:
            path = self.target / relative
            lf = path.read_bytes().replace(b"\r\n", b"\n")
            path.write_bytes(lf)
        self.assertEqual(docs.installation_errors(self.target, None), [])
        self.assertEqual(docs.install(self.target, self.source, None), 0)

    def test_failed_refresh_restores_existing_release_and_manifest(self):
        docs.install(self.target, self.source, None)
        before = snapshot(self.target)
        for relative in docs.FILES[:3]:
            (self.source / relative).write_bytes(b"updated source\n")
        original_write = Path.write_bytes
        calls = 0
        def fail_once(path, data):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("synthetic refresh failure")
            return original_write(path, data)
        with patch.object(Path, "write_bytes", fail_once):
            self.assertEqual(docs.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)

    def test_cli_supports_both_memory_versions_without_content_or_template_mutation(self):
        for version in ("0.1", "0.2"):
            with self.subTest(version=version):
                self.memory(version)
                before = snapshot(self.target)
                result = subprocess.run([sys.executable, "-X", "utf8", str(CLI), "install-capability", str(self.target), "--name", "documentation-management"], capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                after = snapshot(self.target)
                self.assertEqual({p: after[p] for p in before if p not in (docs.MANIFEST,)}, {p: data for p, data in before.items() if p not in (docs.MANIFEST,)})
                # Separate installation for the other layout; never migrate a real target.
                self.target = self.base / "other-project"
                self.target.mkdir(exist_ok=True)

    def test_recognized_but_incomplete_memory_is_refused_without_writes(self):
        self.memory()
        (self.target / "project.yaml").unlink()
        before = snapshot(self.target)
        command = [sys.executable, "-X", "utf8", str(CLI), "install-capability", str(self.target), "--name", "documentation-management", "--force"]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(snapshot(self.target), before)

    def test_cli_force_cannot_override_local_changes_or_unknown_memory(self):
        self.memory()
        command = [sys.executable, "-X", "utf8", str(CLI), "install-capability", str(self.target), "--name", "documentation-management", "--force"]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        (self.target / docs.FILES[0]).write_text("local skill", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(snapshot(self.target), before)
        (self.target / ".project-memory/schema-version").write_text("flexideo-project-memory/9.9", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(snapshot(self.target), before)


class MarkdownSearch(unittest.TestCase):
    def test_and_or_and_diacritics_and_generated_exclusion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "one.md").write_text("# Řízení\nImport a autentizace", encoding="utf-8")
            (root / "two.md").write_text("# Other\nOnly import", encoding="utf-8")
            (root / "site").mkdir()
            (root / "site/derived.md").write_text("Import autentizace", encoding="utf-8")
            command = [sys.executable, "-X", "utf8", str(ROOT / docs.FILES[-1]), "--root", str(root), "--query", "import + autentizace | rizeni", "--ignore-diacritics", "--json"]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual([item["path"] for item in data["results"]], ["one.md"])


if __name__ == "__main__":
    unittest.main()
