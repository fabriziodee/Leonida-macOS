"""CPU-only regression tests of synthetic hardware evidence classification."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_hardware_evidence.py"
spec = importlib.util.spec_from_file_location("hardware_evidence", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def log(counts, luid="00000000:000000ab"):
    return "\n".join(
        [f"VIctory shader fixture: {n} case(s) ran on the hardware adapter, LUID {luid}" for n in counts]
        + ["test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 3 filtered out"]
    )


class HardwareEvidenceTests(unittest.TestCase):
    def test_complete_with_optional_software_skip(self):
        self.assertEqual(mod.validate(log([5, 5, 7, 8]) + "\nWARP unavailable", 4, 25), "00000000:000000ab")

    def test_missing_call(self):
        with self.assertRaises(ValueError):
            mod.validate(log([5, 5, 15]), 4, 25)

    def test_wrong_count(self):
        with self.assertRaises(ValueError):
            mod.validate(log([5, 5, 7, 7]), 4, 25)

    def test_hardware_skip(self):
        with self.assertRaises(ValueError):
            mod.validate(log([5, 5, 7, 8]) + "\nno SM 6.6 hardware device", 4, 25)

    def test_mixed_adapter(self):
        data = log([5, 5, 7, 8]).replace("000000ab", "000000ac", 1)
        with self.assertRaises(ValueError):
            mod.validate(data, 4, 25)

    def test_failed_summary(self):
        with self.assertRaises(ValueError):
            mod.validate(log([5, 5, 7, 8]).replace("0 failed", "1 failed"), 4, 25)

    def test_cross_fixture_adapter_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.log", Path(tmp) / "b.log"
            a.write_text(log([5, 5, 7, 8]), encoding="utf-8")
            b.write_text(log([4, 5, 7], "0:AB"), encoding="utf-8")
            cmd = [sys.executable, "-I", str(SCRIPT), str(a), str(b)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            b.write_text(log([4, 5, 7], "0:AC"), encoding="utf-8")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("changed between", result.stderr)


if __name__ == "__main__":
    unittest.main()
