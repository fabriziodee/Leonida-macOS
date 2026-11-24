# Leonida-macOS

**3r1’s experimental Apple Silicon compatibility branch of Leonida.** The focus is macOS GPU validation with Vulkan through MoltenVK, plus Wine-based testing of Leonida’s Windows runtime.

[Italiano](#italiano) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Upstream README](README.upstream.md)

## Status

### Xbox Graphics First Present · 24 November 2026

On M1 Max with CrossOver/D3DMetal, a synthetic Xbox-style title resolved 4/4 imports, created D3D12.X Device11, submitted a texture copy and completed 3/3 PresentX-to-DXGI presentations (S_OK). The title returned the expected 42 and the runtime returned 0. Separate probes verified 180/180 DXGI presentations and 64/64 texture readback bytes. [Published source, patches and evidence](https://github.com/fabriziodee/Leonida-macOS/tree/macos/3r1-xbox-graphics-checkpoint-20261124-165045/checkpoints/2026-11-24-xbox-graphics). No draw or dispatch in the integrated probe; GTA VI boot and visible game rendering are unverified. The milestone count remains 5/8.


**Hybrid runtime: 5 of 8 milestones verified (62.5% of the checklist) toward a responsive GTA VI menu.**
The VIctory build, CrossOver/D3DMetal host checks, two synthetic loader tests,
and synthetic launch passed. D3D12 clear and readback matched all 16 RGBA8 pixels. GTA VI boot and menu remain unverified.
Additional hardware checks passed: 64 texture bytes, two compute shader fixtures and a 32-lane texture lookup. Results are documented on the [experimental branch at `912df590`](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/PROGRESS.md); the experimental code has not been merged into `main`. The checklist is not a measure of playability or a prediction of success.

[Cross-platform CI fixes (PR #3)](https://github.com/fabriziodee/Leonida-macOS/pull/3) have been merged into `main`; all seven jobs returned for [the PR workflow](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45419718184) passed. This does not certify the experimental branch or a real game boot.

See the [test matrix](PROGRESS.md) and [request for Apple Silicon testers](https://github.com/fabriziodee/Leonida-macOS/issues/1).

- **GTA VI is not playable.** Boot and gameplay are unverified. The Windows runtime is tested through Wine on macOS. Portable tools and GPU tests can be built natively.
- This branch starts from upstream commit `561b65a83`. Local changes experiment with D3D12 resource allocation validation and add diagnostics for Vulkan pipeline statistics queries.
- In CrossOver 26.3, the D3D12/Vulkan device test exercised the workaround for MoltenVK 1.2.10: the runtime returns `E_NOTIMPL` for pipeline statistics query heaps on that driver. Vulkan query and runtime validation are ongoing. See the [progress report](PROGRESS.md).

- VIctory is also being evaluated through CrossOver and D3DMetal. The [synthetic smoke test](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/docs/victory-macos.md) checks the host and exercises the runtime entry path.
- On the M1 Max, MoltenVK also returned all 4,096 expected pixels for each of two emulated wave64 mesh shaders. [GPU results](PROGRESS.md#gpu-regressions-rechecked-on-24-november)

## Help wanted

No game files are needed for synthetic testing. We especially welcome independent M-series reproductions of the [extended smoke test](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/docs/victory-macos.md). We welcome Apple Silicon users who can run synthetic GPU tests, developers familiar with MoltenVK or Wine, and contributors who can improve the macOS setup instructions. Open an issue with your chip, macOS version, backend, exact commit and a minimal synthetic reproduction. See the [upstream testing guide](docs/testing.md) for available tests.

Share only original code, synthetic fixtures, and sanitized output. Keep game files, derived assets, executables, keys and private data local.

## Credits and license

Based on [ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida), originally hosted at `ItsNotRexed/Leonida`. See the [original credits](README.upstream.md#credits) and [GPL-3.0 license](LICENSE). Third-party components retain their own license notices.

## Italiano

**Aggiornamento 24 novembre:** percorso grafico Xbox sintetico integrato verificato: 4/4 import, Device11, 3/3 PresentX, uscita titolo 42. [Sorgenti, patch e log](https://github.com/fabriziodee/Leonida-macOS/tree/macos/3r1-xbox-graphics-checkpoint-20261124-165045/checkpoints/2026-11-24-xbox-graphics). Nessun rendering 3D del gioco ancora verificato.

**Versione sperimentale 3r1 di Leonida per macOS su Apple Silicon.**

**Runtime ibrido: 5 tappe verificate su 8 (62,5% della checklist) verso un menu funzionante.** I test sintetici sono passati, incluso il readback D3D12 di 16 pixel. L’avvio del gioco e il menu restano da verificare. Consulta la [matrice dei test](PROGRESS.md#italiano) e la [richiesta di prove su Apple Silicon](https://github.com/fabriziodee/Leonida-macOS/issues/1).

I test hardware aggiuntivi hanno verificato 64 byte di texture, due shader di calcolo e una ricerca texture su 32 lane. I risultati sono documentati nel [branch sperimentale al commit `912df590`](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/PROGRESS.md); il codice sperimentale non è ancora integrato in `main`. La percentuale non indica giocabilità né probabilità di successo. La [PR #3](https://github.com/fabriziodee/Leonida-macOS/pull/3) è stata integrata e i sette job restituiti dal [workflow della PR](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45419718184) sono passati.

Il lavoro si concentra sui test GPU con Vulkan tramite MoltenVK e sui test del runtime Windows tramite Wine.
Sul M1 Max, ciascuno dei due mesh shader di prova con wave64 emulata ha restituito tutti i 4.096 pixel attesi. [Risultati GPU](PROGRESS.md#gpu-regressions-rechecked-on-24-november)

- **GTA VI non è giocabile.** L’avvio e il gameplay non sono verificati. Gli strumenti portabili e i test GPU possono essere compilati nativamente.
- La base è il commit upstream `561b65a83`. Le modifiche locali sperimentano la validazione delle allocazioni D3D12 e aggiungono diagnostica per le query delle statistiche Vulkan.
- Con CrossOver 26.3 il test del dispositivo D3D12/Vulkan ha verificato che il runtime restituisce `E_NOTIMPL` per le query di statistiche della pipeline su MoltenVK 1.2.10. La verifica delle query Vulkan e del runtime prosegue. Consulta lo [stato di avanzamento](PROGRESS.md#italiano).

- In parallelo, il [test sintetico di VIctory](https://github.com/fabriziodee/Leonida-macOS/blob/912df59021f09c0dd6b22d48b07293bd6485efaa/docs/victory-macos.md) verifica i requisiti grafici e il percorso di avvio del runtime in CrossOver con D3DMetal.

Per i test sintetici non servono file di gioco. Cerchiamo persone che possano eseguire test sintetici su Apple Silicon, lavorare su MoltenVK o Wine e migliorare la guida di configurazione. Nelle issue indica chip, versione macOS, backend, commit e passi per riprodurre il problema con dati sintetici. Condividi solo codice originale e output privo di dati riservati. Tieni in locale file di gioco, asset derivati, eseguibili e chiavi.

Il progetto deriva da [ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida), in origine `ItsNotRexed/Leonida`. Consulta i [crediti originali](README.upstream.md#credits), la [licenza GPL-3.0](LICENSE) e la [roadmap](ROADMAP.md).
