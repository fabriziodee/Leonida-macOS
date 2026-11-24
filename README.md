# Leonida-macOS

**3r1’s experimental Apple Silicon compatibility branch of Leonida.** The focus is macOS GPU validation with Vulkan through MoltenVK, plus Wine-based testing of Leonida’s Windows runtime.

[Italiano](#italiano) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md) · [Upstream README](README.upstream.md)

## Status

- **GTA VI is not playable.** Boot and gameplay are unverified. The Windows runtime is tested through Wine on macOS. Portable tools and GPU tests can be built natively.
- This branch starts from upstream commit `561b65a83`. Local changes experiment with D3D12 resource allocation validation and add diagnostics for Vulkan pipeline statistics queries.
- In CrossOver 26.3, the D3D12/Vulkan device test exercised the workaround for MoltenVK 1.2.10: the runtime returns `E_NOTIMPL` for pipeline statistics query heaps on that driver. Vulkan query and runtime validation are ongoing. See the [progress report](PROGRESS.md).

- VIctory is also being evaluated through CrossOver and D3DMetal. The [synthetic smoke test](docs/victory-macos.md) checks the host and exercises the runtime entry path.

## Help wanted

We welcome Apple Silicon users who can run synthetic GPU tests, developers familiar with MoltenVK or Wine, and contributors who can improve the macOS setup instructions. Open an issue with your chip, macOS version, backend, exact commit and a minimal synthetic reproduction. See the [upstream testing guide](docs/testing.md) for available tests.

Share only original code, synthetic fixtures, and sanitized output. Keep game files, derived assets, executables, keys and private data local.

## Credits and license

Based on [ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida), originally hosted at `ItsNotRexed/Leonida`. See the [original credits](README.upstream.md#credits) and [GPL-3.0 license](LICENSE). Third-party components retain their own license notices.

## Italiano

**Versione sperimentale 3r1 di Leonida per macOS su Apple Silicon.** Il lavoro si concentra sui test GPU con Vulkan tramite MoltenVK e sui test del runtime Windows tramite Wine.

- **GTA VI non è giocabile.** L’avvio e il gameplay non sono verificati. Gli strumenti portabili e i test GPU possono essere compilati nativamente.
- La base è il commit upstream `561b65a83`. Le modifiche locali sperimentano la validazione delle allocazioni D3D12 e aggiungono diagnostica per le query delle statistiche Vulkan.
- Con CrossOver 26.3 il test del dispositivo D3D12/Vulkan ha verificato che il runtime restituisce `E_NOTIMPL` per le query di statistiche della pipeline su MoltenVK 1.2.10. La verifica delle query Vulkan e del runtime prosegue. Consulta lo [stato di avanzamento](PROGRESS.md#italiano).

- In parallelo, il [test sintetico di VIctory](docs/victory-macos.md) verifica i requisiti grafici e il percorso di avvio del runtime in CrossOver con D3DMetal.

Cerchiamo persone che possano eseguire test sintetici su Apple Silicon, lavorare su MoltenVK o Wine e migliorare la guida di configurazione. Nelle issue indica chip, versione macOS, backend, commit e passi per riprodurre il problema con dati sintetici. Condividi solo codice originale e output privo di dati riservati. Tieni in locale file di gioco, asset derivati, eseguibili e chiavi.

Il progetto deriva da [ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida), in origine `ItsNotRexed/Leonida`. Consulta i [crediti originali](README.upstream.md#credits), la [licenza GPL-3.0](LICENSE) e la [roadmap](ROADMAP.md).
