# macOS progress

## Morning source and CI review · 25 November 2026

PR #13 and PR #14 merged at `ea1ce88`; [CI](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45516558755) and [No Game Data](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45516558768) passed. The preceding Runtime was cancelled; full Runtime and physical integrated-scene execution are still pending. External VIctory maintainers report incomplete 3D world rendering on Windows, not a result on this Mac. [Evidence review and generic synthetic test priorities](docs/runtime-evidence-2026-11-25.md). No new GPU execution, no proprietary content, no change to 5/8 or prior graphics totals. Historical entries below describe their respective revisions.

## Independent Apple Silicon reproduction · 24 November 2026

The [independent M4 Max report in issue #1](https://github.com/fabriziodee/Leonida-macOS/issues/1#issuecomment-7142660029) documents two synthetic VIctory runs on a second Apple Silicon generation. Host D3D12/SM 6.6, 16 RGBA pixels, synthetic entry and exit 42 were reported in both runs; patched-fork texture readback matched 64 bytes. The [instrumented follow-up](https://github.com/fabriziodee/Leonida-macOS/issues/1#issuecomment-7144872577) reports all 25 f32 and 16 f16 cases passing on the default hardware adapter with identical LUID; only WARP skipped. See [reproduction details](docs/victory-macos.md#independent-m4-max-reproduction--24-november-2026). Bash/Zsh is corrected. The smoke filter now requires every positive hardware marker and permits optional WARP skips; a fresh combined-script run is pending. This is contributor-reported evidence, not a CI or real game boot result. Existing graphics totals and 5/8 checklist are unchanged.

## Evening evidence review · 24 November 2026

- At `60a2344b`, the [SDK audit](docs/sdk-dependency-audit.md) records the independent synthetic GDK/LibHttpClient V5 loopback PASS (initialization, task queue, HTTP 200, response body/header, server request validation, exit 42). This is reported local evidence, not a new run, console ABI validation or runtime integration.
- [Main CI run 45465558110](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45465558110) failed. [PR #14 CI run 45482330471](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45482330471) failed in check, macos-python and stdlib-tests-linux; semantic, translator, viewer and change-scope jobs passed. These historical failures are superseded for the Python CI by seven successful jobs each on [main 5ffc62cc](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45487967063) and [PR #14 fce056f0](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45486274662). Runtime remains unresolved: [main Runtime](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45487354881) failed with sccache ServerBusy (egress limit); [PR Runtime](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45486274701) had Windows/Linux PASS and macOS cancelled. Do not merge until required checks pass.
- [PR #13](https://github.com/fabriziodee/Leonida-macOS/pull/13) contains an integrated synthetic textured cube with an independent CPU reference; local execution is pending. Existing 41-frame / 629,760-sample totals and 5/8 checklist remain unchanged.
- Public reports describe a Windows splash screen followed by a crash; this is not evidence of a responsive menu or gameplay, and not evidence for macOS. [External project and evidence review](docs/external-project-status-2026-11-24.md).
- The next compatibility work uses original synthetic fixtures and public SDK documentation only. No unauthorized builds or untrusted executables are accepted as inputs or evidence.

## Consolidated graphics validation · 24 November 2026

| Verified synthetic gate | Validated frames | RGB samples | Host draws |
| --- | ---: | ---: | ---: |
| [Back buffer / GPU clear](experiments/xbox-backbuffer/README.md) | 6 | 92,160 | 0 |
| [Synthetic RDNA2 draw](experiments/xbox-draw/README.md) | 3 | 46,080 | 8 |
| [Indexed geometry](experiments/xbox-indexed/README.md) | 4 | 61,440 | 8 |
| [Depth / occlusion](experiments/xbox-depth/README.md) | 4 | 61,440 | 16 |
| [Alpha / additive blending](experiments/xbox-blend/README.md) | 4 | 61,440 | 8 |
| [Multipass / resource transitions](experiments/xbox-multipass/README.md) | 4 | 61,440 | 16 |
| [Dynamic texture sampling](experiments/xbox-sampling/README.md) | 4 | 61,440 | 8 |
| [UV interpolation](experiments/xbox-uv/README.md) | 4 | 61,440 | 8 |
| [Perspective / bilinear filter](experiments/xbox-perspective-filter/README.md) | 4 | 61,440 | 8 |
| [Physical mip levels / SRV selection](experiments/xbox-mipmaps/README.md) | 4 | 61,440 | 8 |
| **Total** | **41** | **629,760** | **88** |

78 successful DXGI presentations across these ten groups; earlier standalone presenter probes excluded. Results reported from local hardware. Same diagnostic runtime SHA-256 `bbccb2cf79bbbbcc41845c88f44564adf1266c10527a2138401601f4e2291639`. Captures at 160×96 from 320×192 back buffers, before Present. No game files used; no verified game boot. All validated experiment sources integrated directly into main; consolidated CI is not yet certified.

## Xbox physical mip levels and SRV selection · 24 November 2026

Reported local M1 Max / CrossOver / D3DMetal run at `cd0c00fc`: four actual mip levels of one 64×64 RGBA8 texture, separate RTV clears and explicit SRV selection, 8/8 executed draws and Present calls, expected exit 42, 61,440/61,440 RGB samples matched. [Probe and results](experiments/xbox-mipmaps/README.md). Automatic LOD selection, generated mipmaps, trilinear/anisotropic filtering and general subresource synchronization remain unverified. Captures remain local; no independent GPU CI or actual game boot.

## Xbox perspective correction and bilinear filtering · 24 November 2026

Reported local M1 Max run at `19801e7e`: 8/8 executed host draws and successful DXGI presentations, expected title exit 42, 61,440/61,440 RGB samples within expected values. Frames 5–6 matched varying-w perspective correction, frames 7–8 matched the bilinear average at the four-texel junction (127/128 allowed). [Probe and evidence](experiments/xbox-perspective-filter/README.md). Physical mip views passed in the subsequent gate; automatic LOD, anisotropic filtering, broader resource synchronization, complex scenes and real game execution remain unverified.

## Xbox interpolated UV texture sampling · 24 November 2026

Reported local M1 Max / CrossOver / D3DMetal run at `568989914`: both synthetic shaders translated, 8/8 host draws, eight successful presentations, expected title exit 42, 61,440/61,440 RGB samples matched across four quadrant patterns. Cumulative 506,880 validated samples across 33 frames. [Probe and results](experiments/xbox-uv/README.md). Tested equal clip-space w, point-clamp at LOD0, alternating descriptor bindings and changing texture contents. Varying-w perspective correction and bilinear filtering passed in the subsequent gate; mipmaps and actual game boot remain unverified. Original captures remain local; no independent GPU CI result.

## Xbox texture sampling · 24 November 2026

Reported M1 Max / CrossOver / D3DMetal run at `355bba36`: two translated shaders, native PS descriptor tables, point-clamp sampler, dynamic render-target contents and bindings, 8/8 host draws and presentations, expected title exit 42. 61,440/61,440 matching sampled RGB pixels, cumulative 445,440 in 29 frames. [Probe and reported evidence](experiments/xbox-sampling/README.md). Constant UV at LOD0 only; variable UV, filtering and mipmaps remain open. Captures remain local; no real game boot or independent CI GPU test.

## Xbox multipass and whole-resource transitions · 24 November 2026

Reported local M1 Max / CrossOver / D3DMetal run at `9b109704`: 16/16 executed host draws, eight successful Present calls, expected title exit 42, 61,440/61,440 RGB samples matched. Two offscreen targets plus presentation texture; explicit whole-resource barriers and two GPU texture copies per frame. Cumulative 384,000 validated samples across 25 frames. [Probe and reported results](experiments/xbox-multipass/README.md). Captures remain local; no independent CI GPU run. Texture sampling passed in the subsequent gate; actual game boot remains unverified.

## Xbox blending and channel masks · 24 November 2026

Reported local M1 Max / CrossOver / D3DMetal run at `c75ea247`: four host PSOs, 8/8 draws, 8/8 successful DXGI presentations, expected title exit 42, 61,440/61,440 sampled RGB pixels within expected values (alpha 50% permits 127 or 128, other modes exact). Cumulative 322,560 validated samples across 21 frames. [Probe and reported evidence](experiments/xbox-blend/README.md). Alpha itself and complex material texture sampling not validated. Original captures remain local; no independent CI GPU test or game boot.

## Xbox depth ordering · 24 November 2026

Reported local M1 Max / CrossOver / D3DMetal run at `27824d08`: two host PSOs, 16/16 executed draws, eight successful presentations, expected title exit 42. D32_FLOAT, depth writes, clear to zero and strict LESS tested through color readback. Both near/far draw orders produced magenta, zero-depth clear produced black (intentional warning), equal depth retained green. 61,440/61,440 sampled RGB pixels matched; cumulative 261,120 samples across 17 frames. [Probe and results](experiments/xbox-depth/README.md). Original captures remain local. No independent CI GPU run or real game boot. Basic texture sampling and resource bindings passed in the later gate.

## Indexed Xbox geometry · 24 November 2026

Reported local M1 Max validation at `c36dae6b`: 16-bit index buffer, nonzero firstIndex and baseVertex, alternating left/right quads. Both shaders translated, 8/8 indexed draws and DXGI Present calls succeeded, title exit 42, 61,440/61,440 sampled RGB pixels matched in four frames. Cumulative 199,680 samples across 13 frames. [Probe and evidence](experiments/xbox-indexed/README.md). Depth testing passed in the subsequent gate; basic texture sampling passed later; complex render state remains pending. Original captures remain local; no real game boot or independent CI GPU result.

## Synthetic RDNA2 graphics draw · 24 November 2026

Reported local M1 Max / CrossOver / D3DMetal validation: original synthetic VS and PS translated, host graphics pipeline created, 8/8 DrawInstanced calls executed, 8/8 successful DXGI Present calls, expected title exit 42. Corrected ANSI-aware verifier passed four parser fixtures and matched 46,080/46,080 sampled RGB pixels across captured frames 6–8. Combined with the earlier texture-copy and GPU-clear gate, 138,240 sampled pixels matched. [Sources and reported evidence](experiments/xbox-draw/README.md). This is a fullscreen synthetic triangle, not game rendering. Captures remain local. Indexed geometry and depth ordering passed in subsequent gates.

## Verified Xbox back buffer · 24 November 2026

Reported local run on M1 Max using the diagnostics build and CrossOver/D3DMetal: six successful Present calls, 92,160/92,160 matching sampled RGB pixels (46,080 texture-copy and 46,080 render-target clear), two expected title exit codes 42. See [source and evidence](experiments/xbox-backbuffer/README.md). Captures are of the DXGI back buffer before Present at half resolution; alpha, display scanout and shader-driven draw calls are not validated. Original captures are local. No game files used. The subsequent synthetic draw gate above now verifies translated VS/PS, PSO creation and host draws.


## Xbox graphics presentation checkpoint · 24 November 2026

Reported local validation on Apple M1 Max (32 GB), using the existing CrossOver/D3DMetal bottle and a separate experimental build of the VIctory macOS fork based on `f5660fd` with existing local shader/texture fixes and additional presenter instrumentation.

| Probe | Result |
| --- | --- |
| Standalone D3D12/DXGI swap chain | 180/180 Present calls returned S_OK |
| Internal VIctory presenter | 3/3 successful DXGI Present calls; 64/64 texture readback bytes matched |
| Synthetic Xbox-style title through VIctory loader | 1 HLE + 3 host imports, zero missing |
| D3D12.X Device11, interface version 2.4 | Created; texture-copy commands submitted |
| Xbox PresentX to host DXGI | 3/3 Present calls returned 0x00000000, 320 × 192 RGBA8 |
| Synthetic title and runtime exit | Expected title code 42; runtime process code 0 |

An earlier PC-style integration probe failed at RegisterClassW because 11 Windows-specific imports were outside the console resolver's coverage. The successful replacement uses a synthetic Xbox-style executable and does not relax the import policy.

The developer saved a local checkpoint containing the probe source, diffs, logs and binary SHA-256 manifest. The source probes, patches, selected logs and SHA-256 manifest are now published in the [complete checkpoint](checkpoints/2026-11-24-xbox-graphics/README.md) in this integration revision. Pending Codex changes are preserved as patches, not integrated or CI-validated. These results are reported from the local session, not independently rerun by GitHub CI. The integrated probe copies a texture; its draw and dispatch counts are zero. Successful Present calls are not independent verification of visible pixel correctness, game shader execution, game boot or a responsive menu.

**Next priority:** a real boot trace with an authorized, compatible, readable local Xbox Series installation. No change to the existing eight-milestone count (5/8); the new probe strengthens evidence for the already completed runtime/GPU milestones.

**Italiano:** il programma sintetico attraversa il loader VIctory, D3D12.X Device11 e PresentX fino a DXGI con tre presentazioni riuscite e codice di uscita atteso 42. Non è un avvio del gioco. Il checkpoint locale è conservato; il prossimo passo resta un avvio reale con file autorizzati e compatibili.

## Repository status · 24 November 2026

The results below are reported from the experimental [`macos/d3dmetal-execution-probe` snapshot](https://github.com/fabriziodee/Leonida-macOS/commit/912df59021f09c0dd6b22d48b07293bd6485efaa). That snapshot and the first checkpoint were merged into main via [PR #4](https://github.com/fabriziodee/Leonida-macOS/pull/4) at `3e0df6a8`: 12 checks passed and the Wine matrix was skipped on `63336c80`. Local hardware evidence is not a CI result. The back-buffer experiment was merged in PR #5 after 8/8 checks passed. Later verified graphics experiments were integrated directly into main. The eight milestones are a checklist, not an estimate of game compatibility or probability of success.

[PR #3](https://github.com/fabriziodee/Leonida-macOS/pull/3) merged cross-platform CI fixes into `main` at `556d5b12101d`. All seven jobs returned for [the PR's Actions run](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45419718184) completed successfully (change-scope, translator-tests, macos-python, viewer-tests, check, stdlib-tests-linux and semantic-tests on Ubuntu). This is not a fresh full validation of the experimental branch or the game. The local GPU results below are documented test reports, not tests rerun during this documentation update.

**Immediate next step:** independently reproduce the synthetic smoke test on another Apple Silicon host; no game files are needed. For real boot validation, an authorized, compatible, readable local game installation remains necessary. The first visible game frame and responsive menu are still unverified.

## VIctory and D3DMetal · 24 November 2026

**5 of 8 milestones verified toward a responsive GTA VI menu on macOS.**
Each milestone counts once. This measures checklist completion. The chance
of reaching the menu and game compatibility remain unknown until a real test.

| Milestone | Result |
| --- | --- |
| Build the Windows x64 runtime | Passed. VIctory `d2a4bae1f495` built in release with Rust 1.98.1 and the xwin SDK. |
| Check host requirements | Passed on M1 Max, 32 GB, macOS 27.3, CrossOver 26.3.0 with D3DMetal selected. AVX2 detected, D3D12 device created, Shader Model 6.6 and Mesh Shader Tier 1 reported. |
| Execute D3D12 commands and read back pixels | Passed. In the D3DMetal-configured bottle, the host probe submitted an RGBA8 clear and copy, waited on a fence and verified all 16 pixels. Tested at `33829eca0`. |
| Verify the synthetic loader tests | Passed, 2/2. `loads_binds_and_calls_probe` and `maps_a_title_dll_the_title_loads_itself` covered import binding, loading a companion DLL and TLS thread notifications. The test harness used a prebuilt fixture under Wine. |
| Launch a synthetic program with the release runtime | Passed. `victory.exe run … --execute` resolved both imports and the program returned the expected code `42`. |
| Identify and verify a compatible local Xbox Series installation | Blocked. The local search found no authorized, compatible files already readable by VIctory. |
| Execute the GTA VI entry point and observe first visible output | Pending. Verify the build and record the first screen or the exact failure. |
| Reach a recognizable menu and verify input | Pending. Confirm the menu responds and reproduce the result on a second launch. |

These results cover the VIctory path. The existing Leonida Vulkan backend
has its own test results below. Gameplay, game shader rendering, memory use
during game startup and the wider Wine suite remain open.

With the macOS fork at `f5660fd`, VIctory's texture copy returned all 64
expected bytes on the M1 Max. An additional local correction preserved the
sign of zero through the translated sine instruction. Both the 16-bit and
32-bit compute shader fixtures passed on the hardware adapter. The updated
runtime also returned 42 from the synthetic entry point. [Source and reproduction](docs/victory-macos.md#texture-uploads-and-compute-shaders-on-the-m1-max)

The [upstream waterfall-loop shader](https://github.com/Marvisak/VIctory/commit/ffe310eb2098e52169f4c44db5ffdabf43a72622)
also passed on the M1 Max. In its 32-lane synthetic dispatch, even lanes
sampled the first texture and odd lanes the second. All 32 red-channel values matched.

[Run the synthetic smoke test](docs/victory-macos.md) ·
[Backend evidence](docs/macos-backends.md) ·
[Report a real boot attempt](https://github.com/fabriziodee/Leonida-macOS/issues/1)

## Italiano

**Aggiornamento grafico:** dieci gruppi di esperimenti, 629.760 campioni RGB conformi in 41 frame, 88 draw eseguite e 78 presentazioni DXGI riuscite. Prospettiva con w variabile e filtro bilineare verificati. Tutti i sorgenti sono in main. Quattro livelli mip fisici verificati; restano LOD automatico, compute integrato, scene complesse e stabilità; l'avvio reale del gioco non è verificato.

I risultati aggiornati provengono dal [branch sperimentale fissato al commit `912df590`](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/PROGRESS.md). La PR #4 è stata integrata dopo 12 controlli superati e un job Wine saltato; il back buffer è stato integrato nella PR #5 dopo 8/8 controlli riusciti; i successivi esperimenti verificati sono stati consolidati direttamente in main. La [PR #3](https://github.com/fabriziodee/Leonida-macOS/pull/3) è stata integrata e tutti i sette job restituiti dal [workflow della PR](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45419718184) sono terminati con successo. I test GPU locali sono risultati documentati, non rieseguiti durante questo aggiornamento. La priorità è una riproduzione indipendente su Apple Silicon con dati sintetici, seguita da un avvio reale solo in presenza di file autorizzati e compatibili.


**5 tappe verificate su 8 verso un menu funzionante di GTA VI su macOS.**
Il conteggio riguarda le tappe completate. La compatibilità del gioco
resta da verificare con un avvio reale.

Sul Mac M1 Max da 32 GB, con macOS 27.3 e CrossOver 26.3.0, VIctory è stato
compilato, D3D12 si è inizializzato con Shader Model 6.6, entrambi i test
sintetici del loader sono passati e il programma di prova si è avviato
con il codice di uscita atteso `42`. Il probe esteso ha verificato tutti
i 16 pixel dopo una clear D3D12 e una copia in un buffer di readback.
Il fork macOS aggiornato ha verificato anche i 64 byte della texture
caricata attraverso VIctory e i risultati dei due shader di calcolo.

Restano tre tappe. Identificare file autorizzati e leggibili di una build Xbox
Series compatibile, osservare la prima schermata del gioco e verificare che
il menu risponda ai comandi in due avvii. La ricerca locale dei file è
terminata senza trovare un set compatibile. Gameplay e prestazioni restano
da misurare.

## Leonida Vulkan

### GPU regressions rechecked on 24 November

The five pixel shaders covering ordered comparisons with NaN in f16 and f32
each returned all 4,096 expected pixels on the M1 Max with MoltenVK 1.4.2.
CI now requires these results on its MoltenVK runner. The change emits an
ordered less-than or greater-than for the RDNA2 `lg` predicate.
[Upstream implementation and tests](https://github.com/LeonidaReforge/Leonida/commit/5bc7e8b0a1e9c6d8875d8ad94f2cb3fbf26839f5)

On the M1 Max with native MoltenVK 1.4.2, `cs_w32_permlane_fi` returned
all eight expected lane values. The integer format fixture returned all
136 expected words. Its generated SPIR-V shrank from 301,652 to 239,632 bytes.
The changes incorporate the [lane selection fix by Gabriel](https://github.com/LeonidaReforge/Leonida/commit/5a78b4b7d982642f57c9d6248374933c4a13aaf1)
and the [format decoder by SashaTun](https://github.com/LeonidaReforge/Leonida/commit/9ad6cc8c833bf407629fec0fc7f55fb379bf38aa).

With `LEONIDA_W64_EMULATE=1` and `LEONIDA_MESH_COMPUTE=1`, the
`ms_wave_info_s3` and `ms_w64x_ballot` fixtures each returned all
4,096 expected pixels on MoltenVK. On Mesa llvmpipe 26.3.1 (arm64),
the native wave64 test reported its unsupported subgroup width.
The emulated `ms_wave_info_s3` draw on that driver returned the clear color.

### Results from 23 November

- **CrossOver 26.3 / MoltenVK 1.2.10.** The D3D12/Vulkan device test exercised the version-specific fallback. The runtime refused a pipeline statistics query heap with `E_NOTIMPL` because this driver reports support but fails to return usable counters. Other driver versions still use their advertised capability.
- **Native macOS / Mesa llvmpipe.** Five targeted tests passed for queue synchronization, occlusion, and replay queries. The Windows device test did not obtain a matching llvmpipe Vulkan device through Wine. Working pipeline statistics on a second backend remain to be verified.
- **Translator.** The semantic test run on the initial macOS code reported OK across 6,150 tests, with 4 skips and 1 expected failure.
- **Next.** Run the wider Wine runtime suite, verify pipeline statistics with a driver that returns usable counters, and document a reproducible Apple Silicon setup. GTA VI boot and gameplay remain unverified.

## Risultati precedenti di Leonida Vulkan

- **CrossOver 26.3 / MoltenVK 1.2.10.** Il test del dispositivo D3D12/Vulkan ha verificato la gestione specifica per questa versione. Il runtime ha rifiutato la creazione delle query di statistiche della pipeline con `E_NOTIMPL`, perché il driver dichiara il supporto ma non restituisce contatori utilizzabili. Le altre versioni del driver continuano a usare la funzionalità dichiarata.
- **macOS nativo / Mesa llvmpipe.** Superati cinque test mirati su sincronizzazione delle code, occlusione e query di replay. Il test Windows tramite Wine non ha trovato un dispositivo Vulkan llvmpipe compatibile. Rimane da verificare il funzionamento delle statistiche della pipeline su un secondo backend.
- **Traduttore.** La suite semantica eseguita sul codice macOS iniziale si è conclusa con esito OK su 6.150 test, con 4 saltati e 1 fallimento atteso.
- **Prossimi passi.** Eseguire la suite più ampia del runtime tramite Wine, verificare le statistiche su un driver che restituisce contatori utilizzabili e documentare la configurazione riproducibile su Apple Silicon. L’avvio e il gameplay di GTA VI restano da verificare.
