# macOS roadmap

See the [progress report](PROGRESS.md) for completed checks and open work.

- [ ] Document a reproducible Apple Silicon setup for the portable tools and synthetic GPU suite.
- [ ] Record MoltenVK results by chip, macOS version and driver. Distinguish missing features from regressions.
- [x] Verify both emulated wave64 mesh readbacks on the M1 Max with MoltenVK 1.4.2.
- [ ] Extend synthetic allocation and query coverage to other drivers, including a backend with working pipeline statistics.
- [ ] Verify the Windows runtime test suite through Wine on Apple Silicon. Track boot separately.
- [ ] Add macOS checks for the portable subset and send portable fixes upstream.

## VIctory / D3DMetal

- [x] Verify pre-Present swap-chain RGB samples in six synthetic frames (92,160/92,160), including full and rectangular render-target clears. [Evidence](experiments/xbox-backbuffer/README.md)
- [x] Execute a synthetic translated vertex/pixel shader pipeline using the Xbox PSO stream ABI and DrawInstanced; require nonzero host draw count and expected readback.
- [x] Verify indexed geometry with nonzero firstIndex and baseVertex, alternating quad placement and exact sampled RGB readback.
- [x] Verify D32_FLOAT depth writes, occlusion, clear and strict LESS through synthetic color readback.
- [x] Verify alpha and additive blending, channel write masks and opaque overwrite through sampled RGB readback.
- [ ] Extend to texture sampling and resource transitions.

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
- [ ] Estendere a texture e transizioni risorse.

- [x] Verificare Device11 e PresentX sintetici attraverso VIctory (3/3 presentazioni DXGI, uscita 42).
- [ ] Revisionare le patch locali conservate e riprodurre il checkpoint su un secondo host.

- [x] Compilare VIctory, verificare D3D12 e superare i test sintetici.
- [x] Verificare i comandi D3D12 e leggere correttamente tutti i 16 pixel RGBA8.
- [x] Verificare il caricamento di una texture attraverso VIctory e due shader tradotti sulla GPU.
- [ ] Confermare una build Xbox Series compatibile con file autorizzati e già leggibili.
- [ ] Registrare la prima schermata o l’errore preciso nel primo avvio reale.
- [ ] Verificare un menu riconoscibile, i comandi e un secondo avvio.
- [ ] Dopo il menu, misurare caricamento della partita, rendering e memoria.
