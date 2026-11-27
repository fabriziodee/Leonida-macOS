"""Opt-in host storage split for developer sessions; never copies input data."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

GIB = 1024 ** 3


def directory(value):
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError("expected an existing directory")
    return path


def layout(data_root, local_root, reserve_gib, workdir=None, wine_prefix=None):
    data, local = directory(data_root), directory(local_root)
    if reserve_gib < 0:
        raise ValueError("reserve must be nonnegative")
    if data == local or data in local.parents or local in data.parents:
        raise ValueError("data and local directories must not overlap")
    if data.stat().st_dev == local.stat().st_dev:
        raise ValueError("data and local root must be on different mounted filesystems")
    work = directory(workdir) if workdir else None
    prefix = directory(wine_prefix) if wine_prefix else None
    for path in (work, prefix):
        if path is not None and (path.stat().st_dev != local.stat().st_dev
                                 or path == data or data in path.parents or path in data.parents):
            raise ValueError("workdir and Wine prefix must be on the local filesystem, outside the data root")
    free = shutil.disk_usage(local).free
    return data, local, work, prefix, free, reserve_gib * GIB


def cache_directory(local):
    cache = local / "host-cache"
    if cache.is_symlink():
        raise ValueError("refusing a symlinked host-cache")
    cache.mkdir(mode=0o700, exist_ok=True)
    if not cache.is_dir() or cache.stat().st_dev != local.stat().st_dev:
        raise ValueError("host-cache must be a directory on the local filesystem")
    return cache


def run(data_root, local_root, reserve_gib, command=(), workdir=None, wine_prefix=None):
    data, local, work, prefix, free, reserve = layout(
        data_root, local_root, reserve_gib, workdir, wine_prefix)
    print("HYBRID_PREFLIGHT " + json.dumps({
        "local_free_bytes": free, "external_free_bytes": shutil.disk_usage(data).free,
        "reserve_bytes": reserve, "distinct_filesystems": True,
        "mode": "run" if command else "plan",
    }, sort_keys=True), flush=True)
    if free < reserve:
        print("Hybrid storage: insufficient local free space", file=sys.stderr)
        return 1
    if not command:
        return 0
    cache = cache_directory(local)
    # Keep the existing launcher arguments intact. This only affects programs
    # that honor the inherited host environment; no runtime cache hook is implied.
    env = dict(os.environ, XDG_CACHE_HOME=str(cache),
               LEONIDA_DATA_ROOT=str(data))
    if prefix is not None:
        env["WINEPREFIX"] = str(prefix)
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="session-", dir=local) as scratch:
        env.update(TMPDIR=scratch, TMP=scratch, TEMP=scratch)
        child = subprocess.run(command, env=env, cwd=work, check=False)
    end_free = shutil.disk_usage(local).free
    print("HYBRID_RESULT " + json.dumps({
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "child_exit_code": child.returncode, "local_end_free_bytes": end_free,
        "local_net_free_space_drop_bytes": free - end_free,
    }, sort_keys=True), flush=True)
    return child.returncode if child.returncode >= 0 else 128 - child.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--local-root", required=True, help="existing dedicated local directory")
    parser.add_argument("--reserve-gib", type=int, default=16,
                        help="minimum free-space snapshot, not a quota")
    parser.add_argument("--workdir", help="optional existing local runtime working directory")
    parser.add_argument("--wine-prefix", help="optional existing local Wine prefix; not a CrossOver bottle selector")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        return run(args.data_root, args.local_root, args.reserve_gib,
                   command, args.workdir, args.wine_prefix)
    except (OSError, ValueError, RuntimeError) as exc:
        print("Hybrid storage: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
