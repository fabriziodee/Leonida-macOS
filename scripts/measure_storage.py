"""Sample volume free space around an original synthetic developer command."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import time


def measure(workspace, command, interval, *, disk_usage=shutil.disk_usage, spawn=subprocess.Popen):
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("interval must be finite and positive")
    path = Path(workspace).resolve(strict=True)
    if not path.is_dir() or not command:
        raise ValueError("existing workspace directory and command required")
    start = disk_usage(path).free
    minimum = start
    samples = 1
    begun = time.monotonic()
    child = spawn(command)
    error = None
    while True:
        try:
            code = child.wait(timeout=interval)
        except subprocess.TimeoutExpired:
            code = None
        try:
            end = disk_usage(path).free
            minimum = min(minimum, end)
            samples += 1
        except OSError as exc:
            error = str(exc)
        if code is not None:
            break
    if error is not None:
        raise OSError(f"storage sampling incomplete (child exit {code}): {error}")
    return {"start_free_bytes": start, "end_free_bytes": end,
            "minimum_sampled_free_bytes": minimum,
            "maximum_sampled_free_space_drop_bytes": start - minimum,
            "net_free_space_drop_bytes": start - end, "samples": samples,
            "interval_seconds": interval, "elapsed_seconds": round(time.monotonic() - begun, 3),
            "child_exit_code": code}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--interval", type=float, default=0.25)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        report = measure(args.workspace, command, args.interval)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Storage measurement failed: {exc}", file=sys.stderr)
        return 2
    print("STORAGE_REPORT " + json.dumps(report, sort_keys=True), file=sys.stderr)
    code = report["child_exit_code"]
    return code if code >= 0 else 128 - code


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError, OSError):
        pass
    sys.exit(main())
