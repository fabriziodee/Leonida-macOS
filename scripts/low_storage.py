"""Read-only storage preflight for original synthetic smoke-test inputs.

Counts logical bytes of the explicitly listed files (including repeated copies).
Does not traverse directories, reserve space, modify files or manage game data.
"""
import argparse
from pathlib import Path
import shutil
import stat
import sys

MIB = 1024 * 1024


def nonnegative(value):
    n = int(value)
    if n < 0:
        raise argparse.ArgumentTypeError("reserve must be nonnegative")
    return n


def inspect(workspace, copies, reserve_mib):
    if reserve_mib < 0:
        raise ValueError("reserve must be nonnegative")
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError("workspace must be an existing directory")
    copied = 0
    for path in copies:
        info = Path(path).stat()
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"expected a regular input file: {path}")
        copied += info.st_size
    free = shutil.disk_usage(workspace).free
    required = copied + reserve_mib * MIB
    return free, copied, required


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reserve-mib", type=nonnegative, default=1024)
    parser.add_argument("workspace", help="existing destination directory")
    parser.add_argument("copies", nargs="*", help="explicit synthetic test inputs to be copied")
    args = parser.parse_args(argv)
    try:
        free, copied, required = inspect(args.workspace, args.copies, args.reserve_mib)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Low Storage: invalid input: {exc}", file=sys.stderr)
        return 2
    print(f"Low Storage: free={free} bytes; input copies={copied} bytes; "
          f"reserve={args.reserve_mib * MIB} bytes; minimum={required} bytes", flush=True)
    if free < required:
        print("Low Storage: insufficient free space; smoke test not started.", file=sys.stderr)
        return 1
    print("Low Storage: preflight PASS (snapshot, not a disk quota).")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError, OSError):
        pass
    sys.exit(main())
