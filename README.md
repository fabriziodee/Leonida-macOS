# Leonida-macOS

**3r1’s experimental Apple Silicon compatibility branch of Leonida.** The focus is macOS GPU validation with Vulkan through MoltenVK, plus Wine-based testing of Leonida’s Windows runtime.

[Italiano](#italiano) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Upstream README](README.upstream.md)

## Status

*Updated 24 November 2026.*

**Apple Silicon synthetic graphics: ten verified experiment groups, 41 validated frames, 629,760 sampled RGB pixels within expected values, 88 executed host draws and 78 successful DXGI Present calls.** Reported local M1 Max / CrossOver / D3DMetal results using the same diagnostics runtime. These are synthetic compatibility checks, not a percentage of GTA VI compatibility. GTA VI has not been booted or demonstrated playable on this Mac.

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

Captures are half-resolution RGB readbacks of the actual DXGI back buffer before Present. Exact comparison except the documented one-unit UNORM rounding allowance for alpha blending and bilinear filtering. Original capture files remain local; no independent GPU reproduction in CI is claimed. See [PROGRESS](PROGRESS.md) for individual checkpoints and [ROADMAP](ROADMAP.md) for remaining work.

All ten verified experiment groups and their sources are consolidated in `main`. No game assets or binaries are included. The run scripts reproduce the original local environment; external testers must adapt paths and supply their own compatible diagnostics runtime. CI for the consolidated revision is separate from the local hardware results. The stable Status anchor was restored after the previous documentation link check failed.

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

**Stato aggiornato — 24 novembre 2026.** Su M1 Max con CrossOver e D3DMetal abbiamo verificato dieci gruppi di esperimenti sintetici: **629.760 campioni RGB conformi, 41 frame validati, 88 draw host eseguite e 78 Present DXGI riuscite**. Sono integrati in `main` i sorgenti e i risultati di back buffer, clear, shader RDNA2, geometria indicizzata, profondità, blending, multipass, texture sampling, UV, prospettiva/filtro bilineare e selezione di quattro livelli mip fisici. [Matrice completa](#status) · [Stato di avanzamento](PROGRESS.md) · [Roadmap](ROADMAP.md).

I risultati provengono dai test locali riportati, non da un test GPU indipendente in CI. Il readback RGB è a metà risoluzione e precede Present; per blending e filtro bilineare è ammessa la quantizzazione documentata. I file del gioco non sono stati utilizzati e l'avvio reale resta da verificare. Le istruzioni degli esperimenti sono riferite alla configurazione locale originale; altri tester devono adattare i percorsi.

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
