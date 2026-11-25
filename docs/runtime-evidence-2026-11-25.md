# Runtime evidence and priorities — 25 November 2026

AI-assisted source and CI review, 07:39 UTC snapshot. No new local hardware execution, external binaries or game content examined. This is clean-room interoperability research with original synthetic fixtures and public APIs; use only software for which the tester has authorization. No leaked files, protection workarounds, game-derived assets or proprietary traces.

## Current evidence

- Main [ea1ce88](https://github.com/fabriziodee/Leonida-macOS/commit/ea1ce88ed499026cfff6dc9b4fa7068c266b149c) incorporates PRs [#13](https://github.com/fabriziodee/Leonida-macOS/pull/13) and [#14](https://github.com/fabriziodee/Leonida-macOS/pull/14). [CI](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45516558755) and [No Game Data](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45516558768) succeeded. The earlier [Runtime](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45515301579) was cancelled; full Runtime not certified. Integrated cube GPU execution still pending; do not increment 5/8 checklist or existing local graphics totals.
- [VIctory status](https://github.com/Marvisak/VIctory): maintainers report Windows 11/RX 6700 XT menu at 30 FPS, intro with audio and incomplete 3D intro at 1–2 seconds/frame. This is an external report, not independently verified here and not a playable release.
- [VIctory-macOS](https://github.com/pragyaangaur/VIctory-macOS) reports 69 Metal shader checks passing; no independent real-title Mac evidence established in this review.
- [Original Leonida](https://github.com/ItsNotRexed/Leonida) and Reforge returned API 404. Indexed README pages may be stale. GitHub [published the 24 November takedown notice](https://github.com/github/dmca/blob/master/2026/11/2026-11-24-take-two.md) and says it processed the network of 3,007 repositories. Do not try to restore unavailable material, switch remotes to mirrors or copy disputed content. Review provenance and licensing; seek legal advice if necessary.

## Ranked generic improvements

| Priority | Public source | Proposed original synthetic acceptance test |
| --- | --- | --- |
| P0 | [VIctory-macOS fleet failure accounting](https://github.com/pragyaangaur/VIctory-macOS/commit/6e0123a86e3c08ace09b6914e6ccac0ad2b22294) | A deliberately failing test process cannot yield PASS even if some expected output appears. Report hardware versus software adapter and explicit skip reasons. |
| P0 | [VIctory hardware-only shader tests](https://github.com/Marvisak/VIctory/commit/ccfb02996eac831853e8324156f123eeff083e9d) | No physical GPU: mark hardware-only checks skipped, never PASS; on actual hardware a refused pipeline is a failure. Keep CPU reference regressions mandatory. |
| P1 | Existing integrated cube / Runtime CI | Execute the merged synthetic scene on M1 Max and independently on M4; verify reference pixels, depth, UV and draw counts. Resolve hosted Runtime separately; cache fallback must not mask compiler/test failures. |
| P1 | [VIctory-macOS overlay composite](https://github.com/pragyaangaur/VIctory-macOS/commit/85a17cffc8d06d190dc03052b24f6111a5d641b2) | Original two-plane fixture with opaque, transparent and half-alpha texels, mismatched resolutions and BGRA/RGBA handling; compare with CPU reference. |
| P2 | [VIctory dirty-page write tracking](https://github.com/Marvisak/VIctory/commit/cd94d35388765f85d4dd88f24d444e018c468ccd), [follow-up](https://github.com/Marvisak/VIctory/commit/940d32f69b22265690a0b5a15d6ded572ba33baf) | Synthetic buffers with sparse writes, atomics, page boundaries, consecutive submissions and copy-back ordering; compare all bytes against a full-copy reference and measure bytes copied, latency and peak memory. Do not presume speedup on Apple Silicon. |

Keep revision-pinned builds separate and require passing synthetic fixtures before adopting license-compatible changes. No patch imported in this review.

## Independent Windows reference and alternatives

Compare generic authorized synthetic workloads on native Windows x64/D3D12 and Apple Silicon CrossOver/D3DMetal; record exact source revisions, adapter, driver, frame/readback result, committed memory, GPU allocation and frame times. The Windows result isolates host translation from runtime behavior. Retain Leonida's Vulkan/MoltenVK experiments as an independent fallback rather than rewrite the runtime.

- [XCL](https://github.com/xcl-dev/xcl) at [568e7db](https://github.com/xcl-dev/xcl/commit/568e7db7729c8fa6c8f0f4b32d798faaf11462bb) reports an unnamed newer retail title with 30 FPS menus and about 5 FPS in its world on an NVIDIA integration branch. Identity not established by its README. GPL-2.0-only per prior audit: keep independent; do not copy code into GPL-3.0 project without license clearance.
- [XValkyrie](https://github.com/sammwyy/xvalkyrie) reports support for several other Xbox titles; no verified target-game or Apple Silicon result. Useful generic HLE comparison only.
- [Lichii](https://github.com/zortos293/Lichii) is a Switch 2 emulator, not an Xbox runtime. Review only relevant generic graphics-driver ideas against a matching observed regression.
- [AnyXboxX](https://github.com/loopersalty/AnyXboxX) has recent integration and batching changes; do not infer title execution from a wrapper, inherited data or tracker. No code adoption recommended without provenance, licensing and independent tests.

Prefer a small synthetic reproduction over adding another runtime. Keep game-specific boot and gameplay metrics explicitly unverified on this project; do not equate checklist completion with game compatibility.
