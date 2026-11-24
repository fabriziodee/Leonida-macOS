# Xbox back-buffer verification (experimental)

Next gate after the verified texture-copy/PresentX checkpoint. The diagnostic patch reads the **swap-chain back buffer** before Present, rather than the title texture. The original probe checks a four-quadrant image; the new synthetic Xbox program creates an RTV and issues full and rectangular GPU clears, yielding three different frames. The verifier checks every RGB sample in the upstream half-size 160x96 PNGs (92,160 across six images), CRCs, dimensions and positive/negative fixtures. Alpha, desktop scanout, 3D draw and game compatibility are not covered.

Run on the original M1 Max environment using `bash experiments/xbox-backbuffer/run.sh`. It uses a fresh isolated copy of the already patched VIctory source and offline Cargo dependencies; it does not replace the verified binary or alter the original sources. Missing diagnostics dependencies or capture output are failures, not passes. No game files required. The texture-copy GPU gate passed locally on 24 November 2026: 3/3 Present calls returned S_OK and all 46,080 sampled RGB pixels matched. The clear probe failed at link time (`_fltused`); this commit supplies the CRT-free floating-point marker. The corrected GPU clear gate also passed locally: 3/3 Present calls and 46,080/46,080 RGB samples matched, for a total of 92,160/92,160 across both programs. Next after this gate: a translated vertex/pixel shader pipeline and a real DrawInstanced with readback.

## Reported local evidence (24 November)

- Diagnostics build: 27.61 s; SHA-256 `bbccb2cf79bbbbcc41845c88f44564adf1266c10527a2138401601f4e2291639`.
- PNG verifier: six positive and eighteen negative cases passed.
- Original synthetic title: 4/4 imports, Device11, 3/3 successful DXGI Present calls, exit 42.
- Back-buffer captures: 15,360/15,360 sampled RGB pixels matched in each of three frames, total 46,080/46,080. These are pre-Present back-buffer samples, not desktop scanout.
- To resume a prior diagnostics build and reuse validated copy captures, set `LEONIDA_RESUME_DIR` and `LEONIDA_COPY_EVIDENCE_DIR` before running `run.sh`. The runner checks the runtime hash and revalidates saved PNGs without reexecuting the copy title.

## GPU clear result (24 November 2026)

Reported M1 Max / CrossOver / D3DMetal run at `e9467ae`: same diagnostics binary SHA-256 as above; copy captures revalidated without rerunning the GPU. The second synthetic title resolved four imports, created Device11, performed full and rectangular RTV clears and submitted three frames. Each captured back buffer matched 15,360 RGB samples. All three DXGI Present calls returned S_OK, title exited with 42, and the runner completed successfully.

```text
clear: frame 1: 15360/15360 RGB pixels matched
clear: frame 2: 15360/15360 RGB pixels matched
clear: frame 3: 15360/15360 RGB pixels matched
clear: BACKBUFFER PASS (46080 RGB pixels)
LEONIDA BACKBUFFER: PASS (92160 sampled RGB pixels)
```

Both programs reported zero draw/dispatch calls. This validates GPU clears, texture copies and pre-Present sampled RGB readback, not shader-driven geometry, desktop scanout, or real game execution. Original capture files remain local; this report transcribes the developer's terminal evidence.
