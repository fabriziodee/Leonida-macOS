"""Original CPU-only fixtures; no hardware or application assets."""
import importlib.util
from pathlib import Path
import random
import unittest

spec = importlib.util.spec_from_file_location("gpu_reference", Path(__file__).resolve().parents[1] / "scripts" / "gpu_reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


class ReferenceTests(unittest.TestCase):
    def test_alpha_endpoints_and_half(self):
        base = bytes([0, 0, 255, 255] * 3)
        overlay = bytes([255, 0, 0, 0, 255, 0, 0, 128, 255, 0, 0, 255])
        self.assertEqual(ref.composite_rgba(base, 3, 1, overlay, 3, 1),
                         bytes([0, 0, 255, 255, 128, 0, 127, 255, 255, 0, 0, 255]))

    def test_scale_and_orientation(self):
        base = bytes([0, 0, 0, 255] * 12)
        overlay = bytes([255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 255, 255, 255])
        red, green, blue, white = [overlay[i:i+4] for i in range(0, 16, 4)]
        self.assertEqual(ref.composite_rgba(base, 6, 2, overlay, 2, 2),
                         red * 3 + green * 3 + blue * 3 + white * 3)

    def test_invalid_composite(self):
        for base, w in [(bytes(4), 1), (bytes(3), 1), (bytes(4), 0)]:
            with self.assertRaises(ValueError):
                ref.composite_rgba(base, w, 1, bytes(4), 1, 1)

    def test_page_crossing_overlap_and_tail(self):
        old = bytes(37)
        new = bytearray(old)
        new[15:18] = b"abc"
        new[36] = 255
        result, copied = ref.dirty_copy(old, new, [(15, 3), (16, 1), (36, 1)], 16)
        self.assertEqual(result, new)
        self.assertEqual(copied, 37)

    def test_sparse_and_empty(self):
        old = bytes(100)
        new = bytearray(old)
        new[18] = 1
        self.assertEqual(ref.dirty_copy(old, new, [(18, 1)], 16), (bytes(new), 16))
        self.assertEqual(ref.dirty_copy(old, old, [(100, 0)], 16), (old, 0))
        self.assertNotEqual(ref.dirty_copy(old, new, [], 16)[0], new)

    def test_consecutive_random_submissions(self):
        rng = random.Random(73)
        previous = bytes(4099)
        for _ in range(50):
            current = bytearray(previous)
            writes = []
            for _ in range(7):
                start = rng.randrange(len(current))
                size = rng.randrange(min(80, len(current) - start) + 1)
                current[start:start+size] = bytes(rng.randrange(256) for _ in range(size))
                writes.append((start, size))
            actual, copied = ref.dirty_copy(previous, current, writes, 64)
            self.assertEqual(actual, current)
            self.assertLessEqual(copied, len(current))
            previous = actual

    def test_invalid_write(self):
        for writes in [[(-1, 1)], [(8, 1)], [(0, -1)]]:
            with self.assertRaises(ValueError):
                ref.dirty_copy(bytes(8), bytes(8), writes)
        with self.assertRaises(ValueError):
            ref.dirty_copy(bytes(8), bytes(7), [])


if __name__ == "__main__":
    unittest.main()
