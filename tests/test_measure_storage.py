"""Original synthetic tests for the storage sampler."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import measure_storage


class StorageMeasurementTests(unittest.TestCase):
    def test_samples_and_child_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            child = mock.Mock()
            child.wait.side_effect = [subprocess.TimeoutExpired("fixture", 0.25), 17]
            usage = mock.Mock(side_effect=[mock.Mock(free=n) for n in (100, 40, 90)])
            report = measure_storage.measure(tmp, ["fixture"], 0.25,
                                             disk_usage=usage, spawn=mock.Mock(return_value=child))
        self.assertEqual(report["maximum_sampled_free_space_drop_bytes"], 60)
        self.assertEqual(report["net_free_space_drop_bytes"], 10)
        self.assertEqual(report["samples"], 3)
        self.assertEqual(report["child_exit_code"], 17)

    def test_invalid_interval_does_not_launch(self):
        spawn = mock.Mock()
        for interval in (0, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                measure_storage.measure(".", ["fixture"], interval, spawn=spawn)
        spawn.assert_not_called()

    def test_failed_sample_does_not_report_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            child = mock.Mock()
            child.wait.side_effect = [subprocess.TimeoutExpired("fixture", 0.25), 0]
            usage = mock.Mock(side_effect=[mock.Mock(free=100), OSError("sample"), mock.Mock(free=90)])
            with self.assertRaises(OSError):
                measure_storage.measure(tmp, ["fixture"], 0.25, disk_usage=usage,
                                        spawn=mock.Mock(return_value=child))
            self.assertEqual(child.wait.call_count, 2)

    def test_cli_preserves_child_output_and_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "measure_storage.py"),
                                     "--workspace", tmp, "--", sys.executable, "-c",
                                     "print('synthetic'); raise SystemExit(7)"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertEqual(result.stdout.strip(), "synthetic")
        report = json.loads(result.stderr.split("STORAGE_REPORT ", 1)[1])
        self.assertEqual(report["child_exit_code"], 7)
        self.assertGreaterEqual(report["samples"], 2)


if __name__ == "__main__":
    unittest.main()
