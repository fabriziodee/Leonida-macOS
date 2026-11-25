"""Synthetic, standard-library tests for the read-only storage preflight."""
import contextlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import low_storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "synthetic input.txt"
        self.source.write_bytes(b"fixture")

    def check(self, free, copies=(), reserve=0):
        with mock.patch.object(low_storage.shutil, "disk_usage",
                               return_value=mock.Mock(free=free)):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return low_storage.main(["--reserve-mib", str(reserve), "--",
                                         str(self.root), *map(str, copies)])

    def test_exact_boundary(self):
        self.assertEqual(self.check(7, [self.source]), 0)
        self.assertEqual(self.check(6, [self.source]), 1)

    def test_reserve_and_duplicate_copy(self):
        needed = low_storage.MIB + 14
        self.assertEqual(self.check(needed, [self.source, self.source], 1), 0)
        self.assertEqual(self.check(needed - 1, [self.source, self.source], 1), 1)

    def test_missing_and_directory_inputs(self):
        self.assertEqual(self.check(100, [self.root / "absent"]), 2)
        self.assertEqual(self.check(100, [self.root]), 2)

    def test_invalid_workspace(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(low_storage.main([str(self.source)]), 2)
            self.assertEqual(low_storage.main([str(self.root / "absent")]), 2)

    def test_negative_reserve_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            low_storage.main(["--reserve-mib", "-1", str(self.root)])
        self.assertEqual(raised.exception.code, 2)

    def test_preflight_is_read_only(self):
        before = list(self.root.iterdir())
        self.assertEqual(self.check(100, [self.source]), 0)
        self.assertEqual(self.check(0, [self.source]), 1)
        self.assertEqual(list(self.root.iterdir()), before)
        self.assertEqual(self.source.read_bytes(), b"fixture")

    @unittest.skipUnless(os.name != "nt" and Path("/bin/bash").is_file(), "POSIX smoke wrapper")
    def test_wrapper_refuses_then_delegates(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        probes = self.root / "runtime" / "test"
        probes.mkdir(parents=True)
        for name in ("victory_host_probe.cpp", "victory_entry_probe.cpp"):
            (probes / name).write_text("synthetic", encoding="utf-8")
        for name in ("low_storage.py", "run_victory_macos_smoke_low_storage.sh"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)
        runner = scripts / "run_victory_macos_smoke.sh"
        runner.write_text('#!/bin/bash\nprintf "DELEGATED: %s\\n" "$2"\nexit 17\n',
                          encoding="utf-8")
        bottles = self.root / "test bottles"
        (bottles / "Test Bottle" / "drive_c").mkdir(parents=True)
        env = dict(os.environ, LEONIDA_PYTHON=sys.executable)
        for name in ("VICTORY_GPU_TEST_EXE", "VICTORY_SHADER_TEST_EXE"):
            env.pop(name, None)
        command = ["/bin/bash", str(scripts / "run_victory_macos_smoke_low_storage.sh"),
                   str(bottles), "Test Bottle", str(self.source)]
        env["LEONIDA_STORAGE_RESERVE_MIB"] = str(10**15)
        blocked = subprocess.run(command, env=env, capture_output=True, text=True)
        self.assertEqual(blocked.returncode, 1, blocked.stderr)
        self.assertNotIn("DELEGATED", blocked.stdout)
        env["LEONIDA_STORAGE_RESERVE_MIB"] = "0"
        passed = subprocess.run(command, env=env, capture_output=True, text=True)
        self.assertEqual(passed.returncode, 17, passed.stderr)
        self.assertIn("DELEGATED: Test Bottle", passed.stdout)


if __name__ == "__main__":
    unittest.main()
