# macOS progress

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
has its own test results below. Gameplay, real shader rendering, memory use
during game startup and the wider Wine suite remain open.

[Run the synthetic smoke test](docs/victory-macos.md) ·
[Backend evidence](docs/macos-backends.md) ·
[Report a real boot attempt](https://github.com/fabriziodee/Leonida-macOS/issues/1)

## Italiano

**5 tappe verificate su 8 verso un menu funzionante di GTA VI su macOS.**
Il conteggio riguarda le tappe completate. La compatibilità del gioco
resta da verificare con un avvio reale.

Sul Mac M1 Max da 32 GB, con macOS 27.3 e CrossOver 26.3.0, VIctory è stato
compilato, D3D12 si è inizializzato con Shader Model 6.6, entrambi i test
sintetici del loader sono passati e il programma di prova si è avviato
con il codice di uscita atteso `42`. Il probe esteso ha verificato tutti
i 16 pixel dopo una clear D3D12 e una copia in un buffer di readback.

Restano tre tappe. Identificare file autorizzati e leggibili di una build Xbox
Series compatibile, osservare la prima schermata del gioco e verificare che
il menu risponda ai comandi in due avvii. La ricerca locale dei file è
terminata senza trovare un set compatibile. Gameplay e prestazioni restano
da misurare.

## Earlier Leonida Vulkan results · 23 November 2026

- **CrossOver 26.3 / MoltenVK 1.2.10.** The D3D12/Vulkan device test exercised the version-specific fallback. The runtime refused a pipeline statistics query heap with `E_NOTIMPL` because this driver reports support but fails to return usable counters. Other driver versions still use their advertised capability.
- **Native macOS / Mesa llvmpipe.** Five targeted tests passed for queue synchronization, occlusion, and replay queries. The Windows device test did not obtain a matching llvmpipe Vulkan device through Wine. Working pipeline statistics on a second backend remain to be verified.
- **Translator.** The semantic test run on the initial macOS code reported OK across 6,150 tests, with 4 skips and 1 expected failure.
- **Next.** Run the wider Wine runtime suite, verify pipeline statistics with a driver that returns usable counters, and document a reproducible Apple Silicon setup. GTA VI boot and gameplay remain unverified.

## Risultati precedenti di Leonida Vulkan

- **CrossOver 26.3 / MoltenVK 1.2.10.** Il test del dispositivo D3D12/Vulkan ha verificato la gestione specifica per questa versione. Il runtime ha rifiutato la creazione delle query di statistiche della pipeline con `E_NOTIMPL`, perché il driver dichiara il supporto ma non restituisce contatori utilizzabili. Le altre versioni del driver continuano a usare la funzionalità dichiarata.
- **macOS nativo / Mesa llvmpipe.** Superati cinque test mirati su sincronizzazione delle code, occlusione e query di replay. Il test Windows tramite Wine non ha trovato un dispositivo Vulkan llvmpipe compatibile. Rimane da verificare il funzionamento delle statistiche della pipeline su un secondo backend.
- **Traduttore.** La suite semantica eseguita sul codice macOS iniziale si è conclusa con esito OK su 6.150 test, con 4 saltati e 1 fallimento atteso.
- **Prossimi passi.** Eseguire la suite più ampia del runtime tramite Wine, verificare le statistiche su un driver che restituisce contatori utilizzabili e documentare la configurazione riproducibile su Apple Silicon. L’avvio e il gameplay di GTA VI restano da verificare.
