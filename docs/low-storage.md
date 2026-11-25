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
