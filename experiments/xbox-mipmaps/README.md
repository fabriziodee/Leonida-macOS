# Xbox mip-level render targets and SRV selection (experimental)

One 64x64 RGBA8 texture with four real mip levels (64, 32, 16, 8). Distinct RTVs clear each physical level with different colors; SRV rebasing selects a different level using the already verified constant-UV LOD0 shader. The first four frames rotate the palette, then the last four must be red, green, blue and white. Eight executed host draws and successful presentations, expected title exit 42 and 61,440 matching sampled RGB pixels required. Tests explicit mip views and render-to-mip sampling, not automatic LOD selection, generated mipmaps, trilinear/anisotropic filtering or arbitrary subresource barriers. Reuses the exact verified runtime and synthetic shader; no game assets. Reported local compilation and hardware run passed at `cd0c00fc`. Run `bash experiments/xbox-mipmaps/run.sh`.

## Reported local results · 24 November 2026

```text
Host mipmap draws: 8/8 verified
mipmap: frame 5: 15360/15360 RGB pixels matched
mipmap: frame 6: 15360/15360 RGB pixels matched
mipmap: frame 7: 15360/15360 RGB pixels matched
mipmap: frame 8: 15360/15360 RGB pixels matched
LEONIDA MIPMAP: PASS (61440 sampled RGB pixels; host draws verified)
```

Eight successful DXGI presentations and expected title exit 42; unchanged diagnostics runtime. Captures remain local. No actual game boot or independent GPU CI result.
