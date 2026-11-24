# Paths to the first GTA VI boot on Apple Silicon

Reviewed 24 November 2026. Local evidence is from an M1 Max with 32 GB,
macOS 27.3 and CrossOver 26.3.0. The D3DMetal-configured bottle passed the
synthetic D3D12 clear and readback, and VIctory reached the synthetic entry
point and reported exit status 42. The test covered command submission, a
fence and a copy to readback memory. Game shaders, video, presentation and
game input still require a run with an authorized, readable Xbox Series build.

## Project evidence

| Project | Latest evidence examined and relevance to the M1 Max | License and use |
| --- | --- | --- |
| [VIctory](https://github.com/Marvisak/VIctory) | The 23 November status reports 30 fps menus, intro video with audio and first-mission loading on Windows 11 / RX 6700 XT. The first title card renders, then the world is dark. The local macOS smoke test uses `d2a4bae1f495`. It covers the loader and host D3D12 with a synthetic target. | GPL-3.0-or-later. Continue using the existing separately built runtime. |
| [ProjectLeonida](https://github.com/ProjectLeonida/Leonida), [ItsNotRexed](https://github.com/ItsNotRexed/Leonida), [LeonidaReforge](https://github.com/LeonidaReforge/Leonida) | The indexed original docs and the independent continuation describe RDNA2 to SPIR-V, D3D12-to-Vulkan, wave64 emulation, and GPU BVH building. Native macOS tools and Vulkan tests are documented. The runtime is Windows x64. A previous local availability check could only resolve public forks. The reported [off-GitHub mirror](https://git.qilk.de/) did not yield a verifiable source revision in this review. | GPL-3.0 family. Recheck exact source revision and preserve attribution for any cherry-pick. Keep as a fallback for a D3DMetal-specific graphics blocker. |
| [Lichii / zortos293](https://github.com/zortos293/Lichii) | Switch 2 emulator. [PR #2354](https://github.com/zortos293/Lichii/pull/2354), also in a [public Gitea mirror](https://git.nite07.com/nite/Lichii/src/commit/e97adbec0d486ac1064ab6f64dd4375ac03ba4a6), addresses a recursive SPIRV-Cross stack overflow during MoltenVK pipeline creation, including synchronous pipeline creation, with 32 MiB worker stacks. [Issue #237](https://github.com/zortos293/Lichii/issues/237) traces post-video device loss to an attachmentless pass sized 32768×32768 on a device limited to 16384. | Use the measurements to diagnose equivalent traces in Leonida. Check the specific file license before code reuse. Both fixes concern the Vulkan path and neither failure has been observed in our current run. |
| [XCL](https://github.com/ivall/xcl) | RDNA2-to-DXIL and Xbox system-library replacement on Windows x64. The [GTA VI issue](https://github.com/ivall/xcl/issues/159) contains boot reports. The [Wine sparse-VRAM PR #877](https://github.com/ivall/xcl/pull/877) maps graphics allocations lazily and ensures GPU-written regions are backed. This offers a diagnostic lead for Wine address-space or graphics heap failures. No Apple Silicon menu was verified. | GPL-2.0-only. Keep source separate from GPL-3.0 code. |
| [TuxBox](https://github.com/brcly/TuxBox) | The project shows a player-selection prompt at 3840×2160 via Proton Experimental on x86-64 Linux. The reviewed setup uses an RTX 4070 Ti SUPER. [PR #35](https://github.com/brcly/TuxBox/pull/35) concerns XWayland presentation. Its Linux result leaves the macOS graphics and CPU paths open. | Apache-2.0. Can evaluate individual changes with notices if a matching blocker appears. |
| [americas-recomp](https://github.com/realdody/americas-recomp), [JamesCicada/GTAVI-Recomp](https://github.com/JamesCicada/GTAVI-Recomp) | The americas-recomp URL was indexed and returned 404 on direct inspection. Its current source and license could not be verified. JamesCicada documents an early PS5 path on AnyPS5 with no GTA VI test. It adds a different console runtime and graphics interface. | JamesCicada is GPL-2.0-only. No currently verified patch for the Xbox/D3DMetal path. |
| [Xbox2Windows](https://github.com/R0Y00/Xbox2Windows), [ProjectReCity](https://github.com/pixl27/ProjectReCity) | Xbox2Windows reports source-built executables and translated pixel shader outputs validated against hardware and WARP, with full-game startup open. ProjectReCity offers GPL-3.0-or-later Leonida-derived work on wave64 and Vulkan, with first-frame milestones open. | Compare shader discrepancies against their tests if a real shader fails. Check file licenses before any import. |
| [6stars](https://github.com/meetox80/6stars) | Native Swift/Metal engine using game data for independent map rendering. The project describes a separate implementation without the GTA VI executable or original pipelines. Its architecture does not supply the Xbox runtime or a route to the game's menu. | No reuse license verified. |
| [Palmetto](https://github.com/luizwidmer/palmetto), [Vyzerythe/Leonida](https://github.com/Vyzerythe/Leonida) | Earlier local review found a compute-pipeline blocker in Palmetto and a pre-boot status in the Leonida fork. Neither supplied a verified Mac menu. | GPL-3.0 family. Revisit specific commits against a local failure. |

The [PC Race tracker](https://vuyp.github.io/gta6-pc-race/) reports
five-star-recomp continuously presenting black frames and tracks Palmwave,
PercyScarlett and OpenScarlett. These reports are leads. A present count
alone does not establish visible pixels, a responsive menu or
Apple Silicon compatibility. The Cyberleeek/Cyberleek reports concern
alleged leaked game files. The review identified no licensed compatibility
change to integrate from that source. [Rockstar's release announcement](https://www.rockstargames.com/newswire/article/39akk424a9oo53/grand-theft-auto-vi-now-available)
lists PS5 and Xbox Series X|S.

## Architecture decision

### Public updates on 24 November

- PortWatch reports that a private CGBJ build entered the world on PC. Its article distinguishes the group's walking test from a 77-second clip with flat surfaces. The improvement in lighting appeared in a later clip shared by a third party. We found no public CGBJ source revision, frame-time capture or Apple Silicon run. [PortWatch report](https://portwatch-vi.xyz/news/2026-11-24-cgbj-in-game) · [Follow-up and embedded clips](https://www.tarreo.com/pc/gta-6-en-pc-cgbj-caminar-personajes/)
- The GPL-3.0-or-later macOS fork merged Marvisak's updated shader translator at `ffe310e` and carries the D3DMetal staging upload change. We built the fork for the existing CrossOver bottle. The local sine patch, test revisions and hardware checks are documented in the [M1 Max validation](victory-macos.md#texture-uploads-and-compute-shaders-on-the-m1-max). [Mac fork](https://github.com/pragyaangaur/VIctory-macOS/tree/f5660fdcfdd6eb5cb6495be47a23af9aa30f5617) · [Upstream waterfall-loop translation](https://github.com/Marvisak/VIctory/commit/ffe310eb2098e52169f4c44db5ffdabf43a72622)
- XCL corrected copy scratch ownership on new D3D12 command lists. Its Palmwave fork added capture of mesh draws starting at a selected frame. AnyXboxX merged work on RDNA2 image loads, stores and sampling. These are Windows-side leads for future traces. [XCL commit](https://github.com/ivall/xcl/commit/930e8b49c1c2ec683d22c724a398b39111cd0e56) · [Palmwave commit](https://github.com/fablinoo/palmwave/commit/5a54236f9674b01ef69f1a73ca83fe50c067d538) · [AnyXboxX PR](https://github.com/LooperSalty/AnyXboxX/pull/126)
- GitHub returned 404 for the two original Leonida locations. The Reforge continuation supplies the lane-selection and format-decoding fixes tested in our Vulkan branch. Lichii's current commit fixes a C++ include in its shader dependency. Its documented MoltenVK issues above remain driver-specific leads. [Validated Vulkan changes](../PROGRESS.md#gpu-regressions-rechecked-on-24-november) · [Lichii commit](https://github.com/zortos293/Lichii/commit/e6a904dd4c4890cacea60789a1b04ed3e12e4cc6)

### First boot on this Mac

Use VIctory and D3DMetal for the first authorized local boot. This path has a
working release binary, a verified synthetic entry point and a verified
D3D12 submission and readback on the target host. The upstream Windows
result makes menu and video behavior measurable targets. Keep Leonida and
MoltenVK available if a failure points to a D3DMetal limitation with an
existing Vulkan equivalent. A native Metal backend would also need an
Xbox GPU command interface and shader translation. No reviewed project
demonstrated that route executing the game on this hardware.

First capture the failing import, allocation, shader, video boundary or
present call from a real boot. The public fixes above have different
preconditions. Apply the relevant one once a local trace establishes it.
