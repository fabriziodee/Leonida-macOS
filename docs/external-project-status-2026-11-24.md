# External evidence and project status — 24 November 2026

AI-assisted review of public reports and the macOS repository; no external binary, game package or proprietary data was downloaded, inspected or executed.

| Subject | Evidence | Decision |
| --- | --- | --- |
| Orchid video circulating on social media | Self-reported PS5 gameplay and FPS, without a reproducible build or independent confirmation located in this review. The public MythosOfs/Orchid project describes Nintendo Switch 2, not PS5. | Unverified; do not install or adopt. |
| Original Leonida | PC Gamer reports a Windows splash screen followed by a crash and departure of original leads. | Historical report, not playable or macOS boot evidence. |
| LeonidaReforge and Leonida Legacy | Public community continuation repositories; no independent gameplay verification established by this review. Existing macOS progress already cites specific Reforge regression fixes. | Review provenance, license and generic synthetic regressions only; no automatic upstream replacement. |
| Unofficial leaked Xbox build reports | Press reports an unauthorized distribution; filenames and transfer sizes are not proof of integrity, authenticity or authorization. | Out of scope; do not acquire, execute, distribute or integrate. |
| macOS main | 41 synthetic frames, 629,760 sampled RGB pixels within expected values, 88 host draws, 78 DXGI Present calls reported; desktop SDK loopback PASS separately. | Keep 5/8 checklist unchanged; no real game boot verified. |
| CI and open PRs | Main CI at 60a2344b failed; PR #14 still has failed CI jobs; PR #13 synthetic integrated cube awaits execution. | Prioritize existing PR validation, no merge or claimed new GPU result. |

## Sources

- [PC Gamer, 24 November 2026 — original leadership and splash-screen report](https://www.pcgamer.com/games/grand-theft-auto/gta-6-recomp-leaders-bail-out-as-take-two-cracks-down-on-illicit-efforts-to-get-the-game-running-on-pc/)
- [Public Orchid project description](https://github.com/MythosOfs/Orchid)
- [LeonidaReforge public repository](https://github.com/LeonidaReforge/Leonida)
- [Leonida Legacy public repository](https://github.com/ProjectLeonidaL/leonida)
- [Main CI](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45465558110) · [PR #14 CI](https://github.com/fabriziodee/Leonida-macOS/actions/runs/45482330471) · [PR #13](https://github.com/fabriziodee/Leonida-macOS/pull/13)
- [Local evidence](../PROGRESS.md) · [SDK audit](sdk-dependency-audit.md) · [Roadmap](../ROADMAP.md)

No new hardware tests were performed by this review. The project is experimental interoperability research, not an official port or a game distribution.
