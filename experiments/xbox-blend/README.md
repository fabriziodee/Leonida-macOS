# Xbox blending and write masks (experimental)

Reuse the validated runtime and original fullscreen triangle vertex shader. Generate a red pixel shader with alpha 0.5. Clear to blue and cycle four constant graphics pipeline streams: source-alpha/inverse-source-alpha, additive ONE/ONE, disabled blending with only green write enabled, and opaque overwrite. Final frames 5–8 must be half red/blue (127 or 128 allowed on the two nonzero channels due to UNORM quantization), magenta, blue, red. Eight host draws, eight successful Present calls and 61,440 RGB samples checked. Alpha channel itself is not captured. No game files, SDK or runtime rebuild. Reported local compilation and hardware validation passed at `c75ea247`. Run `bash experiments/xbox-blend/run.sh`.

## Reported M1 Max result · 24 November 2026

```text
Host blend draws: 8/8 verified
blend: frame 5: 15360/15360 RGB pixels within expected values
blend: frame 6: 15360/15360 RGB pixels within expected values
blend: frame 7: 15360/15360 RGB pixels within expected values
blend: frame 8: 15360/15360 RGB pixels within expected values
LEONIDA BLEND: PASS (61440 sampled RGB pixels; host draws verified)
```

Four host PSOs created, eight DXGI Present calls succeeded, expected title exit 42. Source alpha 0.5, additive, channel mask and opaque overwrite matched expected RGB values. Half-alpha channels allow 127 or 128; alpha itself is not captured. Original captures remain local. Runtime unchanged; no game boot verified.
