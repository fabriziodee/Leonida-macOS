# Xbox pixel shader texture sampling (experimental)

Original RDNA2 pixel shader with native root tables and explicit-LOD image sample. Two RTV/SRV textures cleared with black borders and colored centers, point-clamp sampler, alternate descriptor-table binding and change texture contents. The final four captured frames must be red, green, blue, green (all 61,440 sampled RGB pixels), with 8/8 executed draws and successful presentations. This tests a constant UV at LOD0, resource/sampler descriptors and updated render-target sampling, not variable UV interpolation, filtering or mipmaps. Reuses verified runtime. No game files or SDK. Reported local compilation and hardware validation passed at `355bba36`. Run `bash experiments/xbox-sampling/run.sh`.

## Reported M1 Max result · 24 November 2026

```text
Host sampling draws: 8/8 verified
sampling: frame 5: 15360/15360 RGB pixels matched
sampling: frame 6: 15360/15360 RGB pixels matched
sampling: frame 7: 15360/15360 RGB pixels matched
sampling: frame 8: 15360/15360 RGB pixels matched
LEONIDA SAMPLING: PASS (61440 sampled RGB pixels; host draws verified)
```

Eight successful DXGI Present calls, expected title exit 42. Both shaders translated; PS hash `91c6de7cb69cb028`, two user-data dwords. Alternating descriptor bindings and changing render-target contents produced expected colors. Captures remain local; this is reported local evidence, not an independent GPU CI result. Variable UV, mipmaps, filtering and actual game execution remain unverified.
