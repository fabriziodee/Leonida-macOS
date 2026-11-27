# Low Storage Mode (experimental developer tooling)

The opt-in mode covers **original synthetic smoke tests only**. It is not a
game launcher, an asset reader, an extraction shortcut, or proof of a smaller
game installation. No game files are needed or handled. The actual application
storage requirement is not established.

## Run the storage-aware smoke test

Use the existing prerequisites and dedicated D3DMetal bottle described in
[VIctory smoke test on Apple Silicon](victory-macos.md). The wrapper measures
free bytes on the resolved destination filesystem before any scratch directory
is created. It counts the logical sizes of the explicit synthetic input copies,
including the optional GPU and shader test binaries, and adds a configurable
reserve for temporary output and other writes.

```sh
LEONIDA_STORAGE_RESERVE_MIB=1024 \
  XWIN_DIR="$HOME/.local/share/xwin-sdk" \
  scripts/run_victory_macos_smoke_low_storage.sh /path/to/bottles TestBottle /path/to/victory.exe
```

The default reserve is 1024 MiB (a policy choice, not a measured requirement).
Raise it for larger tests. The check is a snapshot, not a quota or guarantee:
filesystem overhead, other processes, compiler output and runtime writes may
consume additional space. Exit 1 means insufficient space; exit 2 means
invalid input. After a successful preflight, the existing smoke test runs with
its original exit status, markers and scratch cleanup. Python 3 is required.
The wrapper does not move or delete existing data, change backend selection,
or skip any graphics checks.

For read-only diagnostics, pass an existing scratch destination and any
explicit synthetic inputs that will be copied:

```sh
python3 -I scripts/low_storage.py --reserve-mib 1024 -- /path/to/scratch /path/to/synthetic-input
```

## Reuse the developer build cache

The extended synthetic build example in the smoke guide uses a fresh
temporary Cargo target directory. For repeated builds of the same trusted
developer checkout and toolchain, optionally choose one persistent, dedicated
target directory instead. In that example replace the temporary
CARGO_TARGET_DIR assignment with the following lines:

```sh
export CARGO_TARGET_DIR="$HOME/Library/Caches/Leonida-macOS/synthetic-build"
mkdir -p "$CARGO_TARGET_DIR"
python3 -I "$leonida_root/scripts/low_storage.py" --reserve-mib 10240 -- "$CARGO_TARGET_DIR"
```

The 10 GiB build reserve is an illustrative adjustable threshold, not a bound
on Cargo's disk use. A persistent directory can reuse incremental artifacts;
it can also grow. Keep separate targets for incompatible configurations.
Select an existing writable local or mounted external volume if preferred,
then measure actual usage there. The mode deliberately does not evict caches,
remove SDKs, rewrite files, or assume APFS clone savings.

## Verification and limits

The standard-library suite uses temporary synthetic fixtures and mocked free
space, tests insufficient space and invalid paths, and checks that the POSIX
wrapper preserves the delegated exit status. Run:

```sh
python3 -I tests/test_low_storage.py
```

Physical Apple Silicon execution, repeated-build measurements, and peak disk
usage remain separate validation tasks. No claim is made about the reported
350 GB requirement or any reduction in game installation size.

## Hybrid host storage (experimental, opt-in)

The host session helper keeps an existing external input directory in place and
routes host temporary files and XDG-compatible caches to a dedicated local
directory. It checks that the two paths resolve to different mounted
filesystems and that the local volume has sufficient free space. Different
filesystem device IDs do not prove different physical disks.

On macOS, create a dedicated directory on the internal SSD, outside iCloud.
Replace the external directory with your existing developer input directory:

```sh
mkdir -p "$HOME/Library/Caches/Leonida-macOS/hybrid"
python3 -I scripts/hybrid_storage.py \
  --data-root "/Volumes/External/DeveloperInput" \
  --local-root "$HOME/Library/Caches/Leonida-macOS/hybrid" \
  --reserve-gib 16
```

Without a command this is a read-only preflight. To launch a trusted,
foreground developer command, append `--` followed by the original command
and arguments. Optionally supply an existing local working directory with
`--workdir`. A plain Wine session can explicitly select an existing local
prefix with `--wine-prefix`; do not use this option to select CrossOver
bottles. Configure the actual CrossOver bottle and runtime using their existing
supported settings. No existing bottle or runtime is migrated.

The child receives `TMPDIR`, `TMP`, `TEMP`, `XDG_CACHE_HOME` and
`LEONIDA_DATA_ROOT`; the last is only a handoff for an aware launcher, not an
automatic asset-path redirect. Host cache persists; a private session
temporary directory is removed after the foreground child exits. Do not use
the wrapper for detached launchers whose descendants continue using temporary
files. The helper does not copy, scan or delete input files.

The 16 GiB default is a minimum free-space snapshot, not a cache allocation,
quota or guarantee. The tool reports elapsed wall time, child exit status and
net local free-space change, not peak use or physical disk throughput. Repeat
the same command and compare the same boot milestone with and without the
wrapper. Keep backend, resolution and runtime version fixed. Distinguish
cold and warm caches.

This is the host-layout foundation, **not a DirectStorage read-through cache
or a shader-cache implementation**. Programs that ignore the inherited
environment will not have their caches redirected. The separate local
VIctory V6 integration is not included here; its actual storage and pipeline
hooks require review and local integration before any speedup is claimed.

Run the original synthetic tests:

```sh
python3 -I tests/test_hybrid_storage.py
```
