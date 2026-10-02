"""Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from verify_module import ModuleError, verify, verify_set


class ModuleVerifierTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "demo.jar"
        self.manifest = {"schemaVersion": 1, "id": "hello_demo", "name": "Hello Demo", "version": "1.0.0",
                         "apiVersion": 4, "entrypoint": "example.Demo", "documentation": {"en_us": "docs/en_us.json"}}
        self.docs = {"schemaVersion": 1, "moduleId": "hello_demo", "entries": [
            {"kind": "guide", "name": "Usage", "description": "Example usage"}]}

    def jar(self, extra=None):
        with zipfile.ZipFile(self.path, "w") as archive:
            archive.writestr("hzkmacros.module.json", json.dumps(self.manifest))
            archive.writestr("example/Demo.class", b"test stub")
            archive.writestr("docs/en_us.json", json.dumps(self.docs))
            for name, value in (extra or {}).items():
                archive.writestr(name, value)

    def test_accept(self):
        self.jar()
        self.assertEqual(verify(self.path)["docs"], 1)

    def test_reject_embedded_api(self):
        self.jar({"dev/hzk/hzkmacros/api/module/HzkModule.class": b"bad"})
        with self.assertRaisesRegex(ModuleError, "bundle"):
            verify(self.path)

    def test_reject_missing_entrypoint(self):
        self.manifest["entrypoint"] = "example.Missing"
        self.jar()
        with self.assertRaisesRegex(ModuleError, "entrypoint"):
            verify(self.path)

    def test_reject_invalid_doc_owner(self):
        self.docs["moduleId"] = "other_demo"
        self.jar()
        with self.assertRaisesRegex(ModuleError, "owner"):
            verify(self.path)

    def test_reject_duplicate_dependency(self):
        self.manifest["dependencies"] = {"modules": ["shared_demo", "shared_demo"]}
        self.jar()
        with self.assertRaisesRegex(ModuleError, "duplicated"):
            verify(self.path)

    def test_reject_missing_required_dependency_in_set(self):
        self.manifest["dependencies"] = {"modules": ["shared_demo"]}
        self.jar()
        self.assertEqual(verify(self.path)["required_modules"], ["shared_demo"])
        second = self.path.with_name("second.jar")
        manifest = dict(self.manifest, id="another_demo", dependencies={})
        docs = dict(self.docs, moduleId="another_demo")
        with zipfile.ZipFile(second, "w") as archive:
            archive.writestr("hzkmacros.module.json", json.dumps(manifest))
            archive.writestr("example/Demo.class", b"stub")
            archive.writestr("docs/en_us.json", json.dumps(docs))
        with self.assertRaisesRegex(ModuleError, "requires missing module"):
            verify_set([self.path, second])


    def test_reject_required_optional_overlap(self):
        self.manifest["dependencies"] = {"modules": ["shared_demo"], "optionalModules": ["shared_demo"]}
        self.jar()
        with self.assertRaisesRegex(ModuleError, "overlap"):
            verify(self.path)

    def test_reject_self_dependency(self):
        self.manifest["dependencies"] = {"modules": ["hello_demo"]}
        self.jar()
        with self.assertRaisesRegex(ModuleError, "depend on itself"):
            verify(self.path)

    def test_reject_unsafe_entry_path(self):
        self.jar({"../escape.txt": b"bad"})
        with self.assertRaisesRegex(ModuleError, "Unsafe JAR entry path"):
            verify(self.path)

    def test_reject_future_api(self):
        self.manifest["apiVersion"] = 99
        self.jar()
        with self.assertRaisesRegex(ModuleError, "apiVersion"):
            verify(self.path)

    def test_reject_duplicate_id_in_set(self):
        self.jar()
        second = self.path.with_name("second.jar")
        second.write_bytes(self.path.read_bytes())
        with self.assertRaisesRegex(ModuleError, "Duplicate module id"):
            verify_set([self.path, second])


if __name__ == "__main__":
    unittest.main()
