# Leonida-macOS

**3r1’s experimental Apple Silicon compatibility branch of Leonida.** The focus is macOS GPU validation with Vulkan through MoltenVK, plus Wine-based testing of Leonida’s Windows runtime.

[Italiano](#italiano) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Upstream README](README.upstream.md)

## Status

**Multipass rendering verified:** 16/16 draws, eight successful presentations and 61,440/61,440 matching RGB samples across four frames. Two offscreen targets, explicit whole-resource transitions and GPU copies into the presentation target. Cumulative 384,000 validated samples across 25 frames. [Results](experiments/xbox-multipass/README.md). No actual game boot verified.

**Blending verified:** four host graphics pipelines, 8/8 draws, 8/8 successful DXGI presentations, 61,440/61,440 sampled RGB pixels within expected values across alpha, additive, write-mask and opaque modes. Cumulative synthetic graphics readback: 322,560 validated samples across 21 frames. [Blend results](experiments/xbox-blend/README.md). No game boot verified.

**Depth testing verified:** two graphics pipelines, 16/16 host draws, 8/8 successful DXGI presentations, 61,440/61,440 sampled RGB pixels matched across four depth-ordering cases. Cumulative synthetic readback: 261,120 samples across 17 validated frames. [Depth results](experiments/xbox-depth/README.md). No game boot verified.

**Indexed geometry verified:** 8/8 executed indexed draws, 61,440/61,440 sampled RGB pixels matched across four alternating quad frames, including nonzero firstIndex and baseVertex. Cumulative synthetic graphics readback: 199,680 matching RGB samples across 13 validated frames. [Evidence](experiments/xbox-indexed/README.md). No game boot verified.

**Synthetic RDNA2 graphics draw verified:** two original shaders translated, 8/8 host draws, 8/8 DXGI presentations and 46,080/46,080 sampled RGB pixels matched. Together with the previous back-buffer checks: 138,240 matching samples across nine validated frames. [Experiment and reported evidence](experiments/xbox-draw/README.md). No game boot or complex material validation; depth testing is documented above.

**New: verified Xbox back-buffer output.** Two synthetic Xbox titles produced six captured frames with 92,160/92,160 sampled RGB pixels matching, including full and rectangular render-target clears. [Reproduction and evidence](experiments/xbox-backbuffer/README.md). The subsequent synthetic draw experiment verifies basic shader-driven geometry, not game boot.

### Xbox Graphics First Present · 24 November 2026

On M1 Max with CrossOver/D3DMetal, a synthetic Xbox-style title resolved 4/4 imports, created D3D12.X Device11, submitted a texture copy and completed 3/3 PresentX-to-DXGI presentations (S_OK). The title returned the expected 42 and the runtime returned 0. Separate probes verified 180/180 DXGI presentations and 64/64 texture readback bytes. [Published source, patches and evidence](checkpoints/2026-11-24-xbox-graphics/README.md). No draw or dispatch in the integrated probe; GTA VI boot and visible game rendering are unverified. The milestone count remains 5/8.


**Hybrid runtime: 5 of 8 milestones verified (62.5% of the checklist) toward a responsive GTA VI menu.**
The VIctory build, CrossOver/D3DMetal host checks, two synthetic loader tests,
and synthetic launch passed. D3D12 clear and readback matched all 16 RGBA8 pixels. GTA VI boot and menu remain unverified.
Additional hardware checks passed: 64 texture bytes, two compute shader fixtures and a 32-lane texture lookup. Results are documented on the [experimental branch at `912df590`](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/PROGRESS.md); the experimental code and first checkpoint were merged in [PR #4](https://github.com/fabriziodee/Leonida-macOS/pull/4) after 12 successful checks and one skipped Wine job. The checklist is not a measure of playability or a prediction of success.

[Cross-platform CI fixes (PR #3)](https://github.com/fabriziodee/Leonida-macOS/pull/3) have been merged into `main`; all seven jobs returned for [the PR workflow](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45419718184) passed. This does not certify the experimental branch or a real game boot.

See the [test matrix](PROGRESS.md) and [request for Apple Silicon testers](https://github.com/fabriziodee/Leonida-macOS/issues/1).

- **GTA VI is not playable.** Boot and gameplay are unverified. The Windows runtime is tested through Wine on macOS. Portable tools and GPU tests can be built natively.
- This branch starts from upstream commit `561b65a83`. Local changes experiment with D3D12 resource allocation validation and add diagnostics for Vulkan pipeline statistics queries.
- In CrossOver 26.3, the D3D12/Vulkan device test exercised the workaround for MoltenVK 1.2.10: the runtime returns `E_NOTIMPL` for pipeline statistics query heaps on that driver. Vulkan query and runtime validation are ongoing. See the [progress report](PROGRESS.md).

- VIctory is also being evaluated through CrossOver and D3DMetal. The [synthetic smoke test](docs/victory-macos.md) checks the host and exercises the runtime entry path.
- On the M1 Max, MoltenVK also returned all 4,096 expected pixels for each of two emulated wave64 mesh shaders. [GPU results](PROGRESS.md#gpu-regressions-rechecked-on-24-november)

## Help wanted

No game files are needed for synthetic testing. We especially welcome independent M-series reproductions of the [extended smoke test](docs/victory-macos.md). We welcome Apple Silicon users who can run synthetic GPU tests, developers familiar with MoltenVK or Wine, and contributors who can improve the macOS setup instructions. Open an issue with your chip, macOS version, backend, exact commit and a minimal synthetic reproduction. See the [upstream testing guide](docs/testing.md) for available tests.

Share only original code, synthetic fixtures, and sanitized output. Keep game files, derived assets, executables, keys and private data local.

## Credits and license

Based on [ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida), originally hosted at `ItsNotRexed/Leonida`. See the [original credits](README.upstream.md#credits) and [GPL-3.0 license](LICENSE). Third-party components retain their own license notices.

## Italiano

**Multipass verificato:** 16/16 draw, 61.440/61.440 campioni RGB corretti, transizioni e copie tra render target. Totale 384.000 campioni in 25 frame. [Risultati](experiments/xbox-multipass/README.md).

**Blending verificato:** alpha 50%, additivo, maschera canali e opaco; 8/8 draw e 61.440/61.440 campioni RGB conformi. Totale cumulativo 322.560 in 21 frame. [Risultati](experiments/xbox-blend/README.md).

**Profondità verificata:** 16/16 draw host, 61.440/61.440 campioni RGB corretti; totale 261.120 in 17 frame. [Risultati](experiments/xbox-depth/README.md).

**Geometria indicizzata verificata:** 8/8 draw indicizzate, 61.440/61.440 campioni RGB corretti; totale 199.680 in 13 frame. [Risultati](experiments/xbox-indexed/README.md).

**Rendering sintetico RDNA2 verificato:** due shader tradotti, 8/8 draw host e 46.080/46.080 pixel RGB campionati corretti; totale con il checkpoint precedente 138.240. [Esperimento e risultati](experiments/xbox-draw/README.md). Non è un avvio del gioco.

**Back buffer Xbox verificato:** 92.160/92.160 pixel RGB campionati corretti in sei frame sintetici, inclusi clear integrali e rettangolari. [Test e risultati](experiments/xbox-backbuffer/README.md). La geometria sintetica di base è verificata nel nuovo esperimento; l'avvio del gioco resta da verificare.

**Aggiornamento 24 novembre:** percorso grafico Xbox sintetico integrato verificato: 4/4 import, Device11, 3/3 PresentX, uscita titolo 42. [Sorgenti, patch e log](checkpoints/2026-11-24-xbox-graphics/README.md). Nessun rendering 3D del gioco ancora verificato.

**Versione sperimentale 3r1 di Leonida per macOS su Apple Silicon.**

**Runtime ibrido: 5 tappe verificate su 8 (62,5% della checklist) verso un menu funzionante.** I test sintetici sono passati, incluso il readback D3D12 di 16 pixel. L’avvio del gioco e il menu restano da verificare. Consulta la [matrice dei test](PROGRESS.md#italiano) e la [richiesta di prove su Apple Silicon](https://github.com/fabriziodee/Leonida-macOS/issues/1).

I test hardware aggiuntivi hanno verificato 64 byte di texture, due shader di calcolo e una ricerca texture su 32 lane. I risultati sono documentati nel [branch sperimentale al commit `912df590`](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/PROGRESS.md); il codice sperimentale e il primo checkpoint sono stati integrati nella PR #4 dopo 12 controlli riusciti e un job Wine saltato. La percentuale non indica giocabilità né probabilità di successo. La [PR #3](https://github.com/fabriziodee/Leonida-macOS/pull/3) è stata integrata e i sette job restituiti dal [workflow della PR](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45419718184) sono passati.

Il lavoro si concentra sui test GPU con Vulkan tramite MoltenVK e sui test del runtime Windows tramite Wine.
Sul M1 Max, ciascuno dei due mesh shader di prova con wave64 emulata ha restituito tutti i 4.096 pixel attesi. [Risultati GPU](PROGRESS.md#gpu-regressions-rechecked-on-24-november)

- **GTA VI non è giocabile.** L’avvio e il gameplay non sono verificati. Gli strumenti portabili e i test GPU possono essere compilati nativamente.
- La base è il commit upstream `561b65a83`. Le modifiche locali sperimentano la validazione delle allocazioni D3D12 e aggiungono diagnostica per le query delle statistiche Vulkan.
- Con CrossOver 26.3 il test del dispositivo D3D12/Vulkan ha verificato che il runtime restituisce `E_NOTIMPL` per le query di statistiche della pipeline su MoltenVK 1.2.10. La verifica delle query Vulkan e del runtime prosegue. Consulta lo [stato di avanzamento](PROGRESS.md#italiano).

- In parallelo, il [test sintetico di VIctory](docs/victory-macos.md) verifica i requisiti grafici e il percorso di avvio del runtime in CrossOver con D3DMetal.

Per i test sintetici non servono file di gioco. Cerchiamo persone che possano eseguire test sintetici su Apple Silicon, lavorare su MoltenVK o Wine e migliorare la guida di configurazione. Nelle issue indica chip, versione macOS, backend, commit e passi per riprodurre il problema con dati sintetici. Condividi solo codice originale e output privo di dati riservati. Tieni in locale file di gioco, asset derivati, eseguibili e chiavi.

Il progetto deriva da [ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida), in origine `ItsNotRexed/Leonida`. Consulta i [crediti originali](README.upstream.md#credits), la [licenza GPL-3.0](LICENSE) e la [roadmap](ROADMAP.md).
