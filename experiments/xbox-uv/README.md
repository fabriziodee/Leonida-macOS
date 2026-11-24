# Xbox interpolated UV texture sampling (experimental)

Original synthetic VS exports position and TEXCOORD.xy; PS reads perspective-center barycentric interpolation and samples a bound texture at LOD0. Interleaved position/UV vertex buffer, two dynamically updated four-quadrant textures, point-clamp sampler and alternating descriptor tables. Final four frames must match the exact quadrant pattern (61,440 sampled RGB pixels), with eight successful presentations and 8/8 executed draws. Reported local compilation, translation and hardware validation passed at `568989914`. No SDK, game files or runtime rebuild. Run `bash experiments/xbox-uv/run.sh`. This is not mipmap, anisotropic filtering or actual game compatibility validation.

## Reported M1 Max result · 24 November 2026

```text
Host UV draws: 8/8 verified
uv: frame 5: 15360/15360 RGB pixels matched
uv: frame 6: 15360/15360 RGB pixels matched
uv: frame 7: 15360/15360 RGB pixels matched
uv: frame 8: 15360/15360 RGB pixels matched
LEONIDA UV: PASS (61440 sampled RGB pixels; host draws verified)
```

Both synthetic shaders translated (VS `d9cbdbe067286c0b`, PS `6a0661461cc79fbd`), 8/8 successful DXGI Present calls, title exit 42. Dynamic descriptors and spatial point-clamp sampling matched all four expected quadrant patterns. Original captures remain local. This verifies the tested UV path at equal clip-space w, not general perspective correction with varying w, mipmaps, linear filtering or real game boot.
