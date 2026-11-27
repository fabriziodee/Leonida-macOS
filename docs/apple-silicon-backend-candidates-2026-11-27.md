# Apple Silicon backend and upstream candidate review — 27 November 2026

## Primary integration

Keep the locally reported V6 menu configuration (VIctory-macOS baseline `3f4b775`, M1 Max, 32 GB, macOS 27.3 / CrossOver 26.3) untouched. The local operator report records repeated 30 FPS at 720p, not verified gameplay. No V6 code is published here. See [progress](../PROGRESS.md) and [tester thread](https://github.com/fabriziodee/Leonida-macOS/issues/22).

## Pinned references — independent experiments, not bundled dependencies

| Priority | Project / reviewed revision | Reason and synthetic acceptance gate |
| --- | --- | --- |
| 1 | [VIctory-macOS `31485db9`](https://github.com/pragyaangaur/VIctory-macOS/commit/31485db90f954d86bef631bba8647d8355ce089d) | Opt-in descriptor table memoization. Compare disabled vs verification mode vs enabled on original repeated-draw/descriptor-mutation fixtures; require zero verification discrepancies and exact RGB results before performance comparison. Do not enable in V6 by default. |
| 2 | [Mullion `0f22b2c3`](https://github.com/dttdrv/mullion/tree/0f22b2c3f1e0d9f7a7707ed720406644eccc20f7) | Independent D3D12-on-Metal implementation (LGPL-2.1-or-later, upstream declaration). Compare original D3D12 resource lifetime, descriptor binding, synchronization and pixel readback tests in an isolated environment. |
| 3 | [MetalVulkan `eda88e6a`](https://github.com/metalsharp/MetalVulkan/tree/eda88e6a9328593316d67d16b26496e27148a55f) | Alternative VKD3D-Proton/MoltenVK stack; check feature and numerical differences with the same original fixtures. Project orchestration is AGPL-3.0; individual components retain their licenses. Keep independent. |
| 4 | [MetalSharp-Wine `dbe54236`](https://github.com/metalsharp/MetalSharp-Wine/tree/dbe542360adcaf42edb720811965d424ae3931cf) | Separate Wine/Rosetta/FEX host comparison. Only consider when profiling identifies a CPU or compatibility bottleneck. Do not replace CrossOver or mix DLLs from different builds. |

Existing [MacBox](https://github.com/aykhanium/MacBox) and [XCL](https://github.com/xcl-dev/xcl) remain independent references, not a merged runtime. XCL GPL-2.0-only code must not be combined with GPL-3.0-only/or-later code absent compatible permission. DXC and Microsoft's [DirectX samples](https://github.com/microsoft/DirectX-Graphics-Samples) remain independent validation references.

## Acceptance gates

1. Preserve exact known-good host/runtime revisions, source provenance and local configuration; record hash and backend version. No proprietary input, executable, key or dump in Git.
2. Compare original compute, descriptor, resource-transition, texture, and scene fixtures across candidates. Require correct numerical readback, no device loss, and bounded fence waits.
3. Record independent menu reproduction and, with authorized installations only, whether story-mode entry and visible world rendering are reproducible. Do not infer success from Present counts.
4. Verify input, audio, save/load, and repeated transitions; record stable session duration and reproducible failures.
5. Compare median/p95/p99 frame time, memory pressure, CPU/GPU bottleneck and cold/warm runs only after correctness. Aim for sustained 60 FPS (16.67 ms frame budget) on target hardware without claiming it is achievable yet.

All candidates are references, not adopted binaries or imported source. No new local hardware execution was performed for this review. Retain the source licenses and check the full pinned tree before adoption. Never include unauthorized game data or use takedown mirrors as source.
