# Xbox perspective correction and linear filtering (experimental)

Reuse the verified UV shaders and exact diagnostics runtime. Two fullscreen triangles: one has varying clip-space w (right vertex w=2), the other samples the exact texture center. Frames 5–6 require perspective-correct point sampling of four-quadrant textures; the expected boundary is derived from the homogeneous interpolation formula and actual half-size capture sample coordinates. Frames 7–8 use a second sampler descriptor with bilinear filtering at the four-texel junction: all RGB channels must be 127 or 128. This distinguishes point sampling from linear filtering. Eight host draws, eight successful presentations, expected title exit 42 and 61,440 sampled RGB pixels required. No new runtime build, game files or SDK. Reported local compilation and hardware execution passed at `19801e7e`. Does not test mipmaps or anisotropic filtering. Run `bash experiments/xbox-perspective-filter/run.sh`.

## Reported M1 Max result · 24 November 2026

```text
Host perspective/filter draws: 8/8 verified
perspective/filter: frame 5: 15360/15360 RGB samples matched
perspective/filter: frame 6: 15360/15360 RGB samples matched
perspective/filter: frame 7: 15360/15360 RGB samples matched
perspective/filter: frame 8: 15360/15360 RGB samples matched
LEONIDA PERSPECTIVE FILTER: PASS (61440 sampled RGB pixels; host draws verified)
```

Both original UV shaders translated, eight successful DXGI Present calls, expected title exit 42. Frames 5–6 verified varying-w perspective-correct point sampling and frames 7–8 verified bilinear interpolation at the four-texel junction (RGB 127/128 allowed). Original captures remain local. No independent GPU CI reproduction or game boot. Runtime unchanged.
