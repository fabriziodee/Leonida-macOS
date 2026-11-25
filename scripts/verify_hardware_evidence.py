"""Validate generic synthetic GPU fixture summaries, not application execution."""
import argparse
from pathlib import Path
import re
import sys

MARKER = re.compile(
    r"VIctory shader fixture: ([1-9][0-9]*) case\(s\) ran on the hardware adapter, "
    r"LUID ([0-9a-fA-F]{1,8}):([0-9a-fA-F]{1,8})(?![0-9a-zA-Z:])"
)
SUMMARY = re.compile(r"test result: ok\.\s+1 passed; 0 failed; 0 ignored(?:;|\s|$)")


def validate(log, calls, cases):
    """Return a normalized adapter LUID or raise on incomplete evidence."""
    if "no sm 6.6 hardware device" in log.lower():
        raise ValueError("hardware fixture skipped")
    if len(SUMMARY.findall(log)) != 1:
        raise ValueError("missing or ambiguous successful test summary")
    records = MARKER.findall(log)
    if len(records) != calls or sum(int(n) for n, _, _ in records) != cases:
        raise ValueError("unexpected hardware fixture counts")
    adapters = {(int(hi, 16), int(lo, 16)) for _, hi, lo in records}
    if len(adapters) != 1:
        raise ValueError("hardware adapter changed within the fixture")
    hi, lo = next(iter(adapters))
    return f"{hi:08x}:{lo:08x}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("f32", type=Path)
    parser.add_argument("f16", type=Path)
    args = parser.parse_args()
    try:
        a = validate(args.f32.read_text(encoding="utf-8", errors="replace"), 4, 25)
        b = validate(args.f16.read_text(encoding="utf-8", errors="replace"), 3, 16)
        if a != b:
            raise ValueError("hardware adapter changed between f32 and f16")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Hardware evidence FAIL: {exc}\n")
    print(f"Hardware evidence PASS: 41 cases, 7 calls, adapter LUID {a}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError, OSError):
        pass
    main()
