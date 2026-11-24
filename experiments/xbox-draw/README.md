# Synthetic Xbox draw (verified synthetic rendering)

Original synthetic RDNA2 VS/PS containers generated from the publicly documented parser layout at VIctory-macOS f5660fd. No game shaders or Xbox SDK needed. Vertex shader exports POSITION, pixel shader exports magenta. Xbox PSO stream, descriptor heap, vertex buffer, viewport, scissor, render target and DrawInstanced exercise VIctory's actual graphics path. Eight frames allow for asynchronous pipeline creation; final three must match 46,080 sampled RGB pixels and host draw count must be nonzero. Clear is black, never the expected color. The previous verified diagnostics binary is reused by SHA-256. This is an experimental source-level implementation: compilation, both shader translations, creation of the host pipeline and execution of eight host draws have passed in the reported local run. Final pixel verification passed. Run `bash experiments/xbox-draw/run.sh` on the original Mac environment. No game boot or gameplay claims.

## Reported local execution, 24 November 2026

At `7261f464`, both generated shader containers translated successfully (vertex `f67703d307da9d19`, pixel `8472d4428327fa7d`). The host pipeline was created and queue statistics at frames 1, 2, 4 and 8 reported respectively 1, 1, 2 and 4 executed draws (8/8 total). All eight DXGI Present calls returned S_OK and the title exited with 42. Frames 6, 7 and 8 were saved. The original verifier reported a false negative at the log counter gate; the revised verifier strips ANSI escape sequences and requires the full eight-draw counter sequence. The corrected verifier passed two positive and two negative log-parser fixtures, verified 8/8 host draws and matched 15,360/15,360 sampled RGB pixels in each of frames 6, 7 and 8 (46,080/46,080 total). The original capture files remain local; this is reported terminal evidence, not an independent CI GPU run. No game boot claim.

```text
Draw log parser self-test: PASS (2 positive, 2 negative)
Host draws: 8/8 verified
draw: frame 6: 15360/15360 RGB pixels matched
draw: frame 7: 15360/15360 RGB pixels matched
draw: frame 8: 15360/15360 RGB pixels matched
LEONIDA SYNTHETIC DRAW: PASS (46080 sampled RGB pixels; host draws verified)
```
