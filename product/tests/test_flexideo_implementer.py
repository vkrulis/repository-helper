"""Offline bridge/install contracts, with synthetic products and client projects."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PRODUCT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PRODUCT / "tools/agent-infrastructure"))
import flexideo_implementer_capability as capability
from product_paths import source_path

TOOL = source_path(PRODUCT, capability.FILES[-1])
CLI = PRODUCT / "tools/agent-infrastructure/repository_architecture.py"
spec = importlib.util.spec_from_file_location("implementer_activation", TOOL)
activation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activation)


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def memory(root, version="0.2"):
    for relative, text in {
        "README.md": "# Synthetic project\n", "AGENTS.md": "# Project-owned instructions\n",
        "project.yaml": "contract: flexideo-project/2\n",
        ".project-memory/schema-version": f"flexideo-project-memory/{version}\n",
        ".project-memory/epics.json": '{"revision": 5}\n',
        "context/baseline.md": "Project-owned context\n",
    }.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def synthetic_assembly(root):
    """Test the verifier invocation contract, not FCL's own integrity algorithm."""
    root.mkdir()
    for slot in activation.SLOTS:
        (root / slot).mkdir()
    (root / "AGENTS.md").write_text("# Product entry\n", encoding="utf-8")
    bootstrap = root / activation.BOOTSTRAP
    bootstrap.parent.mkdir(parents=True)
    bootstrap.write_text("# Synthetic FCL bootstrap\n", encoding="utf-8")
    (root / "assembly.lock.json").write_text(json.dumps({
        "schema_version": 1, "assembly_id": "a" * 20,
        "products": {slot: {} for slot in activation.SLOTS},
    }), encoding="utf-8")
    verifier = root / activation.VERIFIER
    verifier.parent.mkdir(parents=True)
    verifier.write_text(
        "import json,sys\nfrom pathlib import Path\n"
        "assert sys.argv[1:] == ['--assembly', str(Path.cwd()), 'verify']\n"
        "lock=json.loads(Path('assembly.lock.json').read_text())\n"
        "print(json.dumps({'status':'VERIFIED','assembly_id':lock['assembly_id']}))\n",
        encoding="utf-8",
    )
    return root


class ManagedBridge(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.target = self.base / "client project"
        self.target.mkdir()
        self.source = self.base / "helper source"
        for relative in capability.FILES:
            target = source_path(self.source, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path(PRODUCT, relative), target)

    def test_standalone_install_preserves_both_memory_layouts_and_arbitrary_project(self):
        for layout in (None, "0.1", "0.2"):
            with self.subTest(layout=layout):
                target = self.target / str(layout)
                target.mkdir()
                if layout:
                    memory(target, layout)
                else:
                    (target / "README.md").write_text("Owned client repo", encoding="utf-8")
                before = snapshot(target)
                self.assertEqual(capability.install(target, self.source, layout), 0)
                after = snapshot(target)
                self.assertEqual({p: after[p] for p in before}, before)
                self.assertEqual(set(after) - set(before), {*capability.FILES, capability.MANIFEST})
                self.assertEqual(capability.installation_errors(target, layout), [])

    def test_idempotence_refresh_and_crlf(self):
        self.assertEqual(capability.install(self.target, self.source, None), 0)
        first = snapshot(self.target)
        self.assertEqual(capability.install(self.target, self.source, None), 0)
        self.assertEqual(snapshot(self.target), first)
        for relative in capability.FILES:
            path = self.target / relative
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertEqual(capability.installation_errors(self.target, None), [])
        source = source_path(self.source, capability.FILES[0])
        source.write_bytes(source.read_bytes() + b"\nUpdated guidance\n")
        self.assertEqual(capability.install(self.target, self.source, None), 0)
        self.assertEqual((self.target / capability.FILES[0]).read_bytes(), source.read_bytes())

    def test_local_edits_and_unmanaged_conflicts_are_never_overwritten(self):
        self.assertEqual(capability.install(self.target, self.source, None), 0)
        (self.target / capability.FILES[0]).write_text("Local edit", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(capability.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)
        self.assertTrue(capability.installation_errors(self.target, None))
        (self.target / capability.MANIFEST).unlink()
        before = snapshot(self.target)
        self.assertEqual(capability.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)

    def test_unknown_incomplete_layout_or_bad_manifest_has_no_writes(self):
        memory(self.target, "9.9")
        before = snapshot(self.target)
        self.assertEqual(capability.install(self.target, self.source, "unknown"), 2)
        self.assertEqual(snapshot(self.target), before)
        (self.target / "project.yaml").unlink()
        before = snapshot(self.target)
        self.assertEqual(capability.install(self.target, self.source, "0.2"), 2)
        self.assertEqual(snapshot(self.target), before)
        manifest = self.target / capability.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text("{}", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(capability.install(self.target, self.source, None), 2)
        self.assertEqual(snapshot(self.target), before)

    def test_failed_install_and_refresh_restore_all_files_and_directories(self):
        for refreshing in (False, True):
            with self.subTest(refreshing=refreshing):
                if refreshing:
                    capability.install(self.target, self.source, None)
                    for relative in capability.FILES:
                        source = source_path(self.source, relative)
                        source.write_bytes(source.read_bytes() + b"\nUpdated bytes\n")
                before = snapshot(self.target)
                original = Path.write_bytes
                calls = 0
                def fail_once(path, data):
                    nonlocal calls
                    calls += 1
                    if calls == 3:
                        raise OSError("synthetic write failure")
                    return original(path, data)
                with patch.object(Path, "write_bytes", fail_once):
                    self.assertEqual(capability.install(self.target, self.source, None), 2)
                self.assertEqual(snapshot(self.target), before)
                if not refreshing:
                    self.assertEqual(list(self.target.iterdir()), [])

    def test_linked_managed_directory_is_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.target / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("host cannot create directory symlinks")
        self.assertEqual(capability.install(self.target, self.source, None), 2)
        self.assertEqual(list(outside.iterdir()), [])

    def test_public_cli_installs_and_force_preserves_local_changes(self):
        memory(self.target)
        before = snapshot(self.target)
        command = [sys.executable, "-X", "utf8", str(CLI), "install-capability", str(self.target), "--name", "flexideo-implementer", "--force"]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual({p: snapshot(self.target)[p] for p in before}, before)
        (self.target / capability.FILES[-1]).write_text("Local tool", encoding="utf-8")
        before = snapshot(self.target)
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(snapshot(self.target), before)

    def test_default_client_install_refuses_bridge_conflict_before_scaffolding(self):
        memory(self.target)
        path = self.target / capability.FILES[0]
        path.parent.mkdir(parents=True)
        path.write_text("Local unmanaged skill", encoding="utf-8")
        before = snapshot(self.target)
        result = subprocess.run([
            sys.executable, "-X", "utf8", str(CLI), "install-capability", str(self.target),
            "--name", "client-project", "--force",
        ], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(snapshot(self.target), before)


class Activation(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.assembly = synthetic_assembly(self.base / "installed product with spaces")
        self.project = self.base / "unrelated project příklad"
        self.project.mkdir()
        self.registry = self.base / "user config/local-products.json"

    def test_empty_user_configuration_environment_still_uses_absolute_home_path(self):
        key = "LOCALAPPDATA" if os.name == "nt" else "XDG_CONFIG_HOME"
        with patch.dict(os.environ, {key: ""}):
            self.assertTrue(activation.default_registry().is_absolute())
            self.assertTrue(activation.default_registry().is_relative_to(Path.home()))

    def test_registration_is_verified_and_preserves_other_products(self):
        self.registry.parent.mkdir()
        self.registry.write_text(json.dumps({"schema_version": 1, "products": {"other": {"root": "keep"}}}), encoding="utf-8")
        before = snapshot(self.assembly)
        result = activation.register(self.assembly, self.registry)
        self.assertEqual(result["status"], "REGISTERED")
        value = json.loads(self.registry.read_text())
        self.assertEqual(value["products"]["other"], {"root": "keep"})
        self.assertEqual(snapshot(self.assembly), before)
        first = self.registry.read_bytes()
        activation.register(self.assembly, self.registry)
        self.assertEqual(self.registry.read_bytes(), first)

    def test_activation_is_read_only_and_returns_explicit_entrypoints(self):
        activation.register(self.assembly, self.registry)
        before = snapshot(self.base)
        result = activation.activate(self.project, self.registry)
        self.assertEqual(result["status"], "READY_FOR_BOOTSTRAP")
        self.assertEqual(result["project_root"], str(self.project.resolve()))
        self.assertEqual(result["execution"], "NOT_STARTED")
        self.assertEqual(result["bootstrap_path"], str(self.assembly / activation.BOOTSTRAP))
        self.assertEqual(snapshot(self.base), before)

    def test_installed_tool_works_from_other_cwd_without_helper_or_registry(self):
        capability.install(self.project, PRODUCT, None)
        copied_tool = self.project / capability.FILES[-1]
        result = subprocess.run([
            sys.executable, "-B", str(copied_tool), "activate", "--assembly", str(self.assembly),
        ], cwd=self.base, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["project_root"], str(self.project.resolve()))
        self.assertFalse(self.registry.exists())

    def test_missing_or_invalid_registry_is_not_guessed(self):
        with self.assertRaisesRegex(activation.ActivationError, "Register"):
            activation.activate(self.project, self.registry)
        self.registry.parent.mkdir()
        for value in ({"schema_version": 99, "products": {}}, {"schema_version": 1, "products": {activation.PRODUCT: {"root": "relative"}}}):
            self.registry.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(activation.ActivationError):
                activation.activate(self.project, self.registry)

    def test_invalid_assembly_does_not_create_registration_and_verify_failure_blocks(self):
        (self.assembly / activation.BOOTSTRAP).unlink()
        with self.assertRaises(activation.ActivationError):
            activation.register(self.assembly, self.registry)
        self.assertFalse(self.registry.parent.exists())
        (self.assembly / activation.BOOTSTRAP).write_text("Bootstrap", encoding="utf-8")
        (self.assembly / activation.VERIFIER).write_text("raise SystemExit(1)", encoding="utf-8")
        with self.assertRaises(activation.ActivationError):
            activation.activate(self.project, self.registry, assembly=self.assembly)

    def test_changed_session_or_assembly_during_verify_is_blocked(self):
        with self.assertRaises(activation.ActivationError) as caught:
            activation.activate(self.project, self.registry, assembly=self.assembly, expected="b" * 20)
        self.assertEqual(caught.exception.status, "ASSEMBLY_CHANGED")
        def swap(*_args, **_kwargs):
            lock = self.assembly / "assembly.lock.json"
            lock.write_text(lock.read_text().replace("a" * 20, "b" * 20), encoding="utf-8")
            return subprocess.CompletedProcess([], 0, json.dumps({"status": "VERIFIED", "assembly_id": "a" * 20}), "")
        with patch.object(activation.subprocess, "run", swap):
            with self.assertRaises(activation.ActivationError) as caught:
                activation.activate(self.project, self.registry, assembly=self.assembly)
        self.assertEqual(caught.exception.status, "ASSEMBLY_CHANGED")

    def test_registration_conflict_and_failed_atomic_write_preserve_registry(self):
        activation.register(self.assembly, self.registry)
        another = synthetic_assembly(self.base / "another product")
        before = self.registry.read_bytes()
        with self.assertRaises(activation.ActivationError):
            activation.register(another, self.registry)
        self.assertEqual(self.registry.read_bytes(), before)
        with patch.object(activation.os, "replace", side_effect=OSError("synthetic replace failure")):
            with self.assertRaises(OSError):
                activation.register(another, self.registry, replace=True)
        self.assertEqual(self.registry.read_bytes(), before)
        self.assertEqual(list(self.registry.parent.iterdir()), [self.registry])

    def test_project_inside_product_and_host_permission_error_are_reported(self):
        with self.assertRaises(activation.ActivationError):
            activation.activate(self.assembly, self.registry, assembly=self.assembly)
        with patch.object(activation, "registered_root", side_effect=PermissionError("synthetic")):
            self.assertEqual(activation.main(["activate", "--project", str(self.project)]), 2)


if __name__ == "__main__":
    unittest.main()
