"""Host storage tests using original temporary fixtures only."""
import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import hybrid_storage as hs


class HybridStorageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve()
        self.data = root / "external data"
        self.local = root / "local state"
        self.data.mkdir()
        self.local.mkdir()
        self.fixture = self.data / "fixture.txt"
        self.fixture.write_text("original", encoding="utf-8")

    def test_reject_same_filesystem_and_overlap(self):
        with self.assertRaisesRegex(ValueError, "different mounted"):
            hs.layout(self.data, self.local, 0)
        with self.assertRaisesRegex(ValueError, "overlap"):
            hs.layout(self.data, self.data, 0)

    def test_invalid_reserve(self):
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            hs.layout(self.data, self.local, -1)

    def run_with_layout(self, command=(), free=16 * hs.GIB, reserve=16 * hs.GIB):
        with mock.patch.object(hs, "layout",
                               return_value=(self.data, self.local, self.local, None, free, reserve)):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return hs.run(self.data, self.local, 16, command)

    def test_plan_and_insufficient_space_are_read_only(self):
        self.assertEqual(self.run_with_layout(), 0)
        with mock.patch.object(hs.subprocess, "run") as spawn:
            self.assertEqual(self.run_with_layout(["unused"], free=0), 1)
            spawn.assert_not_called()
        self.assertEqual(list(self.local.iterdir()), [])
        self.assertEqual(self.fixture.read_text(encoding="utf-8"), "original")

    def test_environment_exit_and_cleanup(self):
        child = ("import os, pathlib, sys; "
                 "p=pathlib.Path(os.environ['TMPDIR']); "
                 "c=pathlib.Path(os.environ['XDG_CACHE_HOME']); "
                 "d=pathlib.Path(os.environ['LEONIDA_DATA_ROOT']); "
                 "assert p.parent == c.parent == pathlib.Path.cwd(); "
                 "assert (d/'fixture.txt').read_text() == 'original'; "
                 "assert os.environ['TMP'] == os.environ['TEMP'] == str(p); "
                 "(p/'temporary').write_text('scratch'); "
                 "(c/'persistent').write_text('cache'); sys.exit(17)")
        self.assertEqual(self.run_with_layout([sys.executable, "-I", "-c", child]), 17)
        self.assertEqual(sorted(p.name for p in self.local.iterdir()), ["host-cache"])
        self.assertEqual((self.local / "host-cache" / "persistent").read_text(), "cache")
        self.assertEqual(list(self.data.iterdir()), [self.fixture])

    def test_reject_cache_symlink(self):
        try:
            (self.local / "host-cache").symlink_to(self.data, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks unavailable")
        with self.assertRaisesRegex(ValueError, "symlinked"):
            hs.cache_directory(self.local)


if __name__ == "__main__":
    unittest.main()
