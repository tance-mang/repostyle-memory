import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("repostyle", Path(__file__).resolve().parents[1] / "scripts/repostyle.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RepoStyleTests(unittest.TestCase):
    def test_nested_override(self):
        self.assertEqual(m.merge({"a": {"b": 1, "c": 2}}, {"a": {"b": 3}}), {"a": {"b": 3, "c": 2}})

    def test_mixed_repository(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "SKILL.md").touch()
            Path(d, "package.json").write_text("{}")
            self.assertEqual(m.inspect(d)["types"], ["application", "skill"])

    def test_unknown_no_git(self):
        with tempfile.TemporaryDirectory() as d:
            result = m.inspect(d)
            self.assertEqual(result["types"], ["unknown"])
            self.assertNotEqual(result["head"]["exit_code"], 0)

    def test_project_overrides_profile(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "profile.json").write_text('{"language":"en","tone":"plain"}')
            Path(d, ".repostyle.json").write_text('{"language":"zh-CN"}')
            rules = m.inspect(d, Path(d, "profile.json"))["rules"]
            self.assertEqual((rules["language"], rules["tone"]), ("zh-CN", "plain"))

    def test_invalid_profile(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "bad.json")
            p.write_text("[]")
            with self.assertRaises(ValueError):
                m.config(p)

    def test_unborn_git_and_untracked(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", d], check=True, capture_output=True)
            Path(d, "README.md").write_text("hello")
            r = m.inspect(d)
            self.assertNotEqual(r["head"]["exit_code"], 0)
            self.assertIn("README.md", r["status"]["stdout"])

    def test_failed_command_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "result.json")
            self.assertEqual(m.record(d, [sys.executable, "-c", "print('actual output'); raise SystemExit(3)"], out), 3)
            r = json.loads(out.read_text())
            self.assertEqual(r["status"], "command_failed")
            self.assertIn("actual output", r["stdout"])

    def test_success_does_not_invent_test_count(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "result.json")
            self.assertEqual(m.record(d, [sys.executable, "-c", "pass"], out), 0)
            r = json.loads(out.read_text())
            self.assertEqual(r["status"], "command_succeeded")
            self.assertNotIn("tests_passed", r)

    def test_cli_preserves_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "result.json")
            out.write_text("original")
            p = subprocess.run([sys.executable, str(Path(m.__file__)), "record", "--output", str(out), "--", sys.executable, "-c", "pass"], capture_output=True)
            self.assertEqual(p.returncode, 2)
            self.assertEqual(out.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
