"""Offline synthetic regression tests for isolated public Git commit staging."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "stage_victory_gpu_copyback.py"
spec = importlib.util.spec_from_file_location("victory_stage", PATH)
stage_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage_mod)


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args],
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


class IsolatedStageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        subprocess.run(["git", "init", "-q", str(self.upstream)], check=True)
        git(self.upstream, "config", "user.name", "Synthetic Author")
        git(self.upstream, "config", "user.email", "author@local.invalid")
        (self.upstream / "buffer.txt").write_text("baseline\n", encoding="utf-8")
        git(self.upstream, "add", "buffer.txt")
        git(self.upstream, "commit", "-qm", "synthetic base")
        self.base = git(self.upstream, "rev-parse", "HEAD")
        (self.upstream / "buffer.txt").write_text("shader-marked\n", encoding="utf-8")
        git(self.upstream, "add", "buffer.txt")
        git(self.upstream, "commit", "-qm", "synthetic sparse update")
        self.first = git(self.upstream, "rev-parse", "HEAD")
        (self.upstream / "guard.txt").write_text("no duplicate save\n", encoding="utf-8")
        git(self.upstream, "add", "guard.txt")
        git(self.upstream, "commit", "-qm", "synthetic copy-back guard")
        self.second = git(self.upstream, "rev-parse", "HEAD")
        self.source = self.root / "source"
        subprocess.run(["git", "clone", "-q", str(self.upstream), str(self.source)],
                       check=True)

    def test_cherry_picks_both_and_keeps_dirty_source_untouched(self):
        git(self.source, "checkout", "--detach", self.base)
        (self.source / "local-untracked.txt").write_text("preserve", encoding="utf-8")
        before = git(self.source, "rev-parse", "HEAD")
        out = self.root / "safe-copy"
        report = stage_mod.stage(self.source, out, (self.first, self.second),
                                 min_free_mib=0)
        self.assertEqual(report["source_head"], before)
        self.assertEqual([item["status"] for item in report["changes"]],
                         ["cherry_picked", "cherry_picked"])
        self.assertEqual((out / "buffer.txt").read_text(), "shader-marked\n")
        self.assertEqual((out / "guard.txt").read_text(), "no duplicate save\n")
        self.assertTrue((out / "3r1-upstream-staging.json").is_file())
        self.assertEqual(git(self.source, "rev-parse", "HEAD"), before)
        self.assertEqual((self.source / "buffer.txt").read_text(), "baseline\n")
        self.assertEqual((self.source / "local-untracked.txt").read_text(), "preserve")

    def test_pins_already_present_are_not_reapplied(self):
        out = self.root / "up-to-date"
        report = stage_mod.stage(self.source, out, (self.first, self.second),
                                 min_free_mib=0)
        self.assertEqual([item["status"] for item in report["changes"]],
                         ["already_present", "already_present"])
        self.assertEqual(report["source_head"], report["staged_head"])

    def test_conflict_aborts_in_copy_only(self):
        git(self.source, "checkout", "--detach", self.base)
        git(self.source, "config", "user.name", "Local Author")
        git(self.source, "config", "user.email", "local@local.invalid")
        (self.source / "buffer.txt").write_text("divergent\n", encoding="utf-8")
        git(self.source, "add", "buffer.txt")
        git(self.source, "commit", "-qm", "local divergent change")
        prior = git(self.source, "rev-parse", "HEAD")
        out = self.root / "conflicting-copy"
        with self.assertRaises(stage_mod.StageError):
            stage_mod.stage(self.source, out, (self.first, self.second),
                            min_free_mib=0)
        self.assertEqual(git(self.source, "rev-parse", "HEAD"), prior)
        self.assertEqual((self.source / "buffer.txt").read_text(), "divergent\n")
        self.assertEqual(git(out, "status", "--porcelain"), "")
        self.assertFalse((out / "3r1-upstream-staging.json").exists())

    def test_rejects_destination_inside_source_or_existing(self):
        with self.assertRaises(stage_mod.StageError):
            stage_mod.stage(self.source, self.source / "new", min_free_mib=0)
        with self.assertRaises(stage_mod.StageError):
            stage_mod.stage(self.source, self.upstream, min_free_mib=0)

    def test_missing_commit_does_not_claim_success(self):
        out = self.root / "missing-pin"
        with self.assertRaises(stage_mod.StageError):
            stage_mod.stage(self.source, out, ("a" * 40, self.second),
                            min_free_mib=0)
        self.assertFalse((out / "3r1-upstream-staging.json").exists())


if __name__ == "__main__":
    unittest.main()
