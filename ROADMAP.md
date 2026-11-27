# macOS roadmap

See the [progress report](PROGRESS.md) for completed checks and open work.

## Primary path · 27 November 2026

**VIctory-macOS / D3DMetal first.** The V6 menu milestone is locally reported; the runtime is not integrated here. See [PROGRESS](PROGRESS.md), [tester thread #22](https://github.com/fabriziodee/Leonida-macOS/issues/22), and [pinned upstream and alternate backend candidates](docs/apple-silicon-backend-candidates-2026-11-27.md).

- [x] Document local reported 30 FPS menu at 720p; not a gameplay benchmark.
- [x] Record independent M4 Max integrated synthetic scene 9/9 and combined smoke script pass.
- [ ] Preserve and reproduce the local V6 baseline independently.
- [ ] Establish repeatable story-mode entry, visible world rendering and input using authorized local installations only.
- [ ] Establish audio, save/load, transitions and stable repeated sessions.
- [ ] Compare descriptor memoization, copy-back and memory pressure using independent original fixtures; promote only verified, license-compatible changes.
- [ ] Profile CPU/GPU and measure sustained frame pacing; 60 FPS is an aspirational target, not a verified result.

The older checklist below is retained as historical context. Alternate backends remain isolated; do not replace the known-good configuration.

## Immediate priorities · 25 November 2026

- [ ] Measure the opt-in [Low Storage Mode](docs/low-storage.md) for original synthetic tests on physical Apple Silicon; compare repeated-build disk usage without game data.

See the [current runtime evidence review](docs/runtime-evidence-2026-11-25.md). PRs #13 and #14 are merged; CI and No Game Data passed at `ea1ce88`. Full Runtime remains unresolved. No new hardware results.

- [ ] Validate hardware versus software adapter reporting and failed test-process exit handling with synthetic fixtures.
- [ ] Reproduce the merged cube on physical Apple Silicon and compare with a native Windows D3D12 synthetic reference.
- [ ] Evaluate two-plane alpha composition and sparse GPU write/copy-back correctness with original fixtures and CPU references. Measure memory and timing only after correctness.


- [x] Restore Python CI on main `5ffc62cc` and PR #14 `fce056f0` (seven jobs passed each).
- [ ] Resolve hosted macOS Runtime cache startup failure and verify full Runtime on the merged revision.
- [ ] Execute and independently validate the merged original synthetic cube from PR #13; do not count pending captures.
- [x] Record reported standalone desktop SDK asynchronous HTTP loopback validation with a synthetic localhost fixture. [SDK audit](docs/sdk-dependency-audit.md)
- [ ] Review public, license-compatible generic interoperability fixes from community continuations; reproduce with original synthetic fixtures before adopting. [External project and evidence review](docs/external-project-status-2026-11-24.md).
- [x] Obtain independent Apple Silicon reproduction of baseline synthetic host/loader and patched texture checks (reported M4 Max; see [issue #1](https://github.com/fabriziodee/Leonida-macOS/issues/1#issuecomment-7142660029)).
- [x] Repeat M4 Max f16/f32 fixtures with identified hardware adapter (25 + 16 cases reported PASS; [follow-up](https://github.com/fabriziodee/Leonida-macOS/issues/1#issuecomment-7144872577)).
- [ ] Repeat revised combined smoke script with positive hardware markers; WARP optional.
- [ ] Independently reproduce the integrated graphics checkpoint; no game boot claim until authorized, independently reproducible evidence exists.

Priorità: CI verde, riproduzione indipendente della scena sintetica, revisione dei fix generici con fixture originali. Il test HTTP è documentato; non equivale a integrazione console. Nessun utilizzo di copie non autorizzate.

- [ ] Document a reproducible Apple Silicon setup for the portable tools and synthetic GPU suite.
- [ ] Record MoltenVK results by chip, macOS version and driver. Distinguish missing features from regressions.
- [x] Verify both emulated wave64 mesh readbacks on the M1 Max with MoltenVK 1.4.2.
- [ ] Extend synthetic allocation and query coverage to other drivers, including a backend with working pipeline statistics.
- [ ] Verify the Windows runtime test suite through Wine on Apple Silicon. Track boot separately.
- [ ] Add macOS checks for the portable subset and send portable fixes upstream.

## VIctory / D3DMetal

- [ ] Validate public SDK candidate exports, ABI and actual behavior through synthetic fixtures. [Local audit](docs/sdk-dependency-audit.md)

- [x] Verify pre-Present swap-chain RGB samples in six synthetic frames (92,160/92,160), including full and rectangular render-target clears. [Evidence](experiments/xbox-backbuffer/README.md)
- [x] Execute a synthetic translated vertex/pixel shader pipeline using the Xbox PSO stream ABI and DrawInstanced; require nonzero host draw count and expected readback.
- [x] Verify indexed geometry with nonzero firstIndex and baseVertex, alternating quad placement and exact sampled RGB readback.
- [x] Verify D32_FLOAT depth writes, occlusion, clear and strict LESS through synthetic color readback.
- [x] Verify alpha and additive blending, channel write masks and opaque overwrite through sampled RGB readback.
- [x] Verify multipass render targets, GPU texture copies and whole-resource transitions.
- [x] Verify native pixel shader texture sampling at constant UV/LOD0 and dynamic descriptor bindings.
- [x] Verify spatial UV interpolation and texture orientation with equal clip-space w and point-clamp LOD0.
- [x] Verify varying-w perspective correction and bilinear filtering at a texel junction.
- [x] Verify four physical mip levels using separate RTV clears and explicit SRV views.
- [ ] Verify automatic LOD, mip generation, trilinear/anisotropic filtering and general subresource synchronization.
- [ ] Verify integrated compute dispatch with GPU output consumed by graphics.
- [ ] Render a combined textured 3D scene with depth, blending and shader-driven lighting.
- [ ] Measure sustained frame pacing, memory use, resource lifetime and repeatability.

- [x] Verify synthetic Xbox-style Device11 and PresentX-to-DXGI integration (3/3 successful presentations; expected exit 42). [Checkpoint](checkpoints/2026-11-24-xbox-graphics/README.md)
- [ ] Review preserved local patches and independently reproduce the checkpoint; this is not game boot validation.

- [x] Build the Windows x64 runtime and verify D3D12 capabilities in CrossOver.
- [x] Verify D3D12 command execution and all 16 RGBA8 pixels on readback.
- [x] Pass the synthetic loader tests and launch the synthetic entry probe.
- [x] Verify VIctory texture uploads and translated f16/f32 shaders on the hardware adapter.
- [ ] Confirm a compatible, authorized Xbox Series build is available as readable files.
- [ ] Record the first visible output or exact startup failure from a real boot attempt.
- [ ] Verify a recognizable menu responds to input and repeat the launch.
- [ ] After the menu milestone, assess loading into gameplay, rendering and memory use.

## Roadmap in italiano

Consulta lo [stato di avanzamento](PROGRESS.md#italiano) per i controlli conclusi e le attività aperte.

- [ ] Documentare una configurazione riproducibile su Apple Silicon per gli strumenti portabili e i test GPU sintetici.
- [ ] Raccogliere risultati MoltenVK per chip, versione macOS e driver, distinguendo funzionalità assenti e regressioni.
- [x] Verificare i pixel dei due mesh shader con wave64 emulata sul M1 Max con MoltenVK 1.4.2.
- [ ] Estendere i test sintetici di allocazione e query ad altri driver, incluso un backend con statistiche della pipeline funzionanti.
- [ ] Verificare la suite del runtime Windows tramite Wine e monitorare l’avvio separatamente.
- [ ] Aggiungere controlli macOS per i componenti portabili e proporre le correzioni al progetto originale.

### VIctory / D3DMetal

- [x] Verificare 92.160 campioni RGB su sei frame nel back buffer DXGI, inclusi clear integrali e rettangolari.
- [x] Eseguire vertex/pixel shader sintetici tradotti con pipeline stream Xbox e DrawInstanced; verificare draw sul dispositivo host e pixel attesi.
- [x] Verificare geometria indicizzata con firstIndex e baseVertex non nulli e readback esatto.
- [x] Verificare profondità D32_FLOAT, occlusioni, clear e confronto LESS con readback colore.
- [x] Verificare blending alpha/additivo, maschere di scrittura e modalità opaca.
- [x] Verificare multipass, copie GPU e transizioni di risorse intere.
- [x] Verificare texture sampling nel pixel shader a UV/LOD0 fissi e binding dinamici.
- [x] Verificare interpolazione UV e orientamento texture con w costante e point-clamp LOD0.
- [x] Verificare correzione prospettica con w variabile e filtro bilineare.
- [x] Verificare quattro livelli mip fisici con RTV e SRV esplicite.
- [ ] Verificare LOD automatico, generazione mipmap, filtro trilineare/anisotropico e sincronizzazione generale delle sottorisorse.
- [ ] Verificare dispatch compute integrato con output GPU consumato dalla grafica.
- [ ] Renderizzare una scena 3D con texture, profondità, blending e illuminazione tramite shader.
- [ ] Misurare frame pacing, memoria, durata delle risorse e ripetibilità.

- [x] Verificare Device11 e PresentX sintetici attraverso VIctory (3/3 presentazioni DXGI, uscita 42).
- [ ] Revisionare le patch locali conservate e riprodurre il checkpoint su un secondo host.

- [x] Compilare VIctory, verificare D3D12 e superare i test sintetici.
- [x] Verificare i comandi D3D12 e leggere correttamente tutti i 16 pixel RGBA8.
- [x] Verificare il caricamento di una texture attraverso VIctory e due shader tradotti sulla GPU.
- [ ] Confermare una build Xbox Series compatibile con file autorizzati e già leggibili.
- [ ] Registrare la prima schermata o l’errore preciso nel primo avvio reale.
- [ ] Verificare un menu riconoscibile, i comandi e un secondo avvio.
- [ ] Dopo il menu, misurare caricamento della partita, rendering e memoria.
