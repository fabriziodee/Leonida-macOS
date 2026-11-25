"""Synthetic CPU reference and verdict checks; no hardware or game files."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "experiments" / "xbox-scene"
BACKBUFFER = ROOT / "experiments" / "xbox-backbuffer" / "verify.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


scene = load("scene_reference", SCENE / "scene.py")
bb = load("backbuffer_reference", BACKBUFFER)


class SceneVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs = {(view, reverse): scene.raster(view, reverse)
                    for view in (0, 1) for reverse in (False, True)}

    def test_reference_coverage_and_order_independence(self):
        for view in (0, 1):
            a, b = self.refs[view, False], self.refs[view, True]
            self.assertEqual(a, b)
            self.assertEqual(len(a), 160 * 96)
            tested = sum(p is not None for p in a)
            fg = sum(p is not None and p != (0, 0, 0) for p in a)
            self.assertGreaterEqual(tested, 13500)
            self.assertGreaterEqual(fg, 1500)
            self.assertGreaterEqual(tested - fg, 1500)
        self.assertNotEqual(self.refs[0, False], self.refs[1, False])

    def test_verifier_accepts_reference_and_rejects_bad_draws_and_pixels(self):
        # These are generated CPU-only PNGs, not GPU captures.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "capture").mkdir()
            log = "\n".join(f"frame presented frame={n} draws={d} drawn={d}"
                            for n, d in ((1, 6), (2, 6), (4, 12), (8, 24)))
            (root / "execution.log").write_text(log, encoding="utf-8")
            raw = {}
            for n in (5, 6, 7, 8):
                ref = self.refs[((n - 1) >> 1) & 1, bool((n - 1) % 2)]
                raw[n] = bytes(c for p in ref for c in (p or (0, 0, 0)))
                (root / "capture" / f"frame-{n}.png").write_bytes(bb.png(raw[n]))

            def run():
                return subprocess.run([sys.executable, str(SCENE / "verify_scene.py"),
                                       str(BACKBUFFER), str(root)],
                                      capture_output=True, text=True, timeout=60)

            ok = run()
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            self.assertIn("LEONIDA SCENE: PASS", ok.stdout)
            (root / "execution.log").write_text(log.replace("drawn=24", "drawn=23"),
                                                encoding="utf-8")
            bad_draw = run()
            self.assertNotEqual(bad_draw.returncode, 0)
            self.assertIn("expected all 48 host draws", bad_draw.stdout + bad_draw.stderr)
            (root / "execution.log").write_text(log, encoding="utf-8")
            ref = self.refs[0, False]
            i = next(i for i, p in enumerate(ref) if p is not None)
            bad = bytearray(raw[5])
            bad[3 * i] ^= 255
            (root / "capture" / "frame-5.png").write_bytes(bb.png(bytes(bad)))
            bad_pixel = run()
            self.assertNotEqual(bad_pixel.returncode, 0)
            self.assertIn("FAIL: frame 5", bad_pixel.stdout + bad_pixel.stderr)


if __name__ == "__main__":
    unittest.main()
