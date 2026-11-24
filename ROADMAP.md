# macOS roadmap

See the [progress report](PROGRESS.md) for completed checks and open work.

- [ ] Document a reproducible Apple Silicon setup for the portable tools and synthetic GPU suite.
- [ ] Record MoltenVK results by chip, macOS version and driver. Distinguish missing features from regressions.
- [ ] Extend synthetic allocation and query coverage to other drivers, including a backend with working pipeline statistics.
- [ ] Verify the Windows runtime test suite through Wine on Apple Silicon. Track boot separately.
- [ ] Add macOS checks for the portable subset and send portable fixes upstream.

## VIctory / D3DMetal

- [x] Verify synthetic Xbox-style Device11 and PresentX-to-DXGI integration (3/3 successful presentations; expected exit 42). [Checkpoint](https://github.com/fabriziodee/Leonida-macOS/tree/macos/3r1-xbox-graphics-checkpoint-20261124-165045/checkpoints/2026-11-24-xbox-graphics)
- [ ] Review preserved local patches and independently reproduce the checkpoint; this is not game boot validation.

- [x] Build the Windows x64 runtime and verify D3D12 capabilities in CrossOver.
- [x] Pass the synthetic loader tests and launch the synthetic entry probe.
- [ ] Confirm a compatible, authorized Xbox Series build is available as readable files.
- [ ] Record the first visible output or exact startup failure from a real boot attempt.
- [ ] Verify a recognizable menu responds to input and repeat the launch.
- [ ] After the menu milestone, assess loading into gameplay, rendering and memory use.

## Roadmap in italiano

Consulta lo [stato di avanzamento](PROGRESS.md#italiano) per i controlli conclusi e le attività aperte.

- [ ] Documentare una configurazione riproducibile su Apple Silicon per gli strumenti portabili e i test GPU sintetici.
- [ ] Raccogliere risultati MoltenVK per chip, versione macOS e driver, distinguendo funzionalità assenti e regressioni.
- [ ] Estendere i test sintetici di allocazione e query ad altri driver, incluso un backend con statistiche della pipeline funzionanti.
- [ ] Verificare la suite del runtime Windows tramite Wine e monitorare l’avvio separatamente.
- [ ] Aggiungere controlli macOS per i componenti portabili e proporre le correzioni al progetto originale.

### VIctory / D3DMetal

- [x] Verificare Device11 e PresentX sintetici attraverso VIctory (3/3 presentazioni DXGI, uscita 42).
- [ ] Revisionare le patch locali conservate e riprodurre il checkpoint su un secondo host.

- [x] Compilare VIctory, verificare D3D12 e superare i test sintetici.
- [ ] Confermare una build Xbox Series compatibile con file autorizzati e già leggibili.
- [ ] Registrare la prima schermata o l’errore preciso nel primo avvio reale.
- [ ] Verificare un menu riconoscibile, i comandi e un secondo avvio.
- [ ] Dopo il menu, misurare caricamento della partita, rendering e memoria.
