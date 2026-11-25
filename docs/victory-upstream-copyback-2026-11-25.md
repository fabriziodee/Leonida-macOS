# VIctory sparse GPU copy-back: isolated upstream adoption — 25 November 2026

**Status: candidate integration script committed, not run on the M1 Max.** The current production/synthetic D3DMetal binary is deliberately unchanged. This document is about public, original-source interoperability work: it contains no game data, binaries, access keys or proprietary traces.

## Authors and public upstream repositories

- [Marvisak/VIctory](https://github.com/Marvisak/VIctory) — **Marvisak and contributors**, public GPL-3.0 codebase. [Commit `cd94d353`](https://github.com/Marvisak/VIctory/commit/cd94d35388765f85d4dd88f24d444e018c468ccd) marks GPU-written pages through shader views and narrows copy-back comparisons; [follow-up `940d32f6`](https://github.com/Marvisak/VIctory/commit/940d32f69b22265690a0b5a15d6ded572ba33baf) prevents a page's own copy-back from rearming a redundant save. Both changes modify the VIctory runtime, *not* the Leonida Python/Vulkan translation pipeline.
- [fxceless/victory-fork](https://github.com/fxceless/victory-fork) — **fxceless and acknowledged contributors**, GPL-3.0, report Windows 11 world rendering, character textures and input at low frame rates (not an Apple Silicon result). The fork explicitly credits [myokex](https://github.com/myokex), Spexivus, joroyt and Joshua Odom for guard and memory fixes. These authors are **credited as external sources**, not silently added as repository collaborators.
- [pragyaangaur/VIctory-macOS](https://github.com/pragyaangaur/VIctory-macOS) — Apple Silicon reference for standalone synthetic tests. The historical [hardware-only detection issue](https://github.com/Marvisak/VIctory/commit/ccfb02996eac831853e8324156f123eeff083e9d) motivated our already integrated adapter-evidence checks.
- [LooperSalty/AnyXboxX](https://github.com/LooperSalty/AnyXboxX) — independent Windows wrapper/reference, not a drop-in Mac runtime. [luizwidmer/palmetto](https://github.com/luizwidmer/palmetto) is a different Vulkan/Windows path; review its licensing and provenance before any future adoption.

**Provenance:** only identified public GPL-3.0 VIctory commits are staged. Do not restore, mirror or import source from the original Leonida repository removed in the Take-Two takedown. Confirm any compatibility and attribution obligations before publishing third-party source changes.

## What has been implemented

New `scripts/stage_victory_gpu_copyback.py` stages the above two *actual upstream commits* in chronological order into a fresh, independent local Git clone. It does not copy or edit the existing CrossOver bottle, patched VIctory working tree, local caches, or known-good executable. It checks SHA identity, commit ancestry, storage, and destination safety, attempts sequential `cherry-pick -x` (preserves the original author), and **fails explicitly on conflicts**, aborting the partial cherry-pick in the disposable copy. A JSON provenance report is written only after both changes stage successfully.

With a local Git checkout containing a known-good VIctory source and an existing separate output parent:

```sh
python3 -I scripts/stage_victory_gpu_copyback.py \
  --source "$HOME/Developer/your-existing-VIctory-git-clone" \
  --output "$HOME/Developer/VIctory-Copyback-Stage-20261125" \
  --fetch
```

The `--fetch` flag fetches **public VIctory source into the isolated clone only**, not into the original checkout. Without `--fetch`, the two commits must already exist in that Git object database. The destination must not exist. By default at least 1 GiB free is required on its volume (a conservative policy check, not an estimated build requirement). Existing uncommitted source modifications are preserved, not imported into the staging clone: back them up separately and reconcile any required local patches in isolation. Keep the original runtime binary pinned by its SHA.

Run offline synthetic staging tests on any machine with Git and Python:

```sh
python3 -I tests/test_stage_victory_gpu_copyback.py -v
python3 -I tests/test_gpu_reference.py -v
```

## Acceptance gate before installing a new runtime on M1 Max

1. Ensure both upstream commits apply to the *actual* macOS presenter fork without skipped changes; resolve conflicts by reviewing the Rust sources and existing local modifications. The existing runtime at the pinned SHA must remain available for rollback.
2. Compile the candidate in an **isolated build target** under the existing licensed Rust/xwin setup. Log source SHA, complete Cargo output, SHA-256 of the candidate, and exact CrossOver/D3DMetal versions. Never replace the known-good binary in place.
3. Run original synthetic sparse-buffer cases: one page, tail page, page-boundary writes, repeated stores/atomics, host/CPU writes while GPU work is pending, alternate views of the same page, multiple consecutive submissions, and error-path cleanup. Compare every output byte to an independent full-copy reference, not only a success marker. The existing `scripts/gpu_reference.py` / `tests/test_gpu_reference.py` form a CPU starting point, not proof of GPU correctness.
4. Re-run the integrated Xbox synthetic scene under CrossOver/D3DMetal with a **separately supplied candidate runtime SHA**. Preserve the reference acceptance gates (8 Present, 48 host draws, 58,560 RGB samples, exit 42), and test both fresh and warm VIctory caches. Ensure no software/WARP adapter was silently selected.
5. Only after correct pixel results, record time spent in copy-back, bytes/pages copied, committed and peak memory, and mean/p95 frame time for the same scene with baseline and candidate across repeated runs. Report a regression if any capture differs. Windows GPU FPS claims do not transfer automatically to the M1 Max.

**Not implemented or verified yet:** applying the runtime candidate on the user's physical M1 Max, completing its Rust build, rerunning the GPU scene, measuring speedups, or booting GTA VI. Those steps require access to the actual local modified VIctory source and hardware. No real game data is used or required for these acceptance tests.
